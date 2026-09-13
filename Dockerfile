# syntax=docker/dockerfile:1
# ─── Build stage (python:latest-dev — has shell, apk, uv, gcc) ───────────────
FROM cgr.dev/chainguard/python:latest-dev AS builder

USER root

ARG NETBOX_VERSION

RUN apk add --no-cache \
      build-base \
      postgresql-17-dev \
      libpq-17 \
      libxml2-dev \
      libxslt-dev \
      xmlsec-dev \
      xmlsec-openssl \
      openssl-dev \
      pkgconf \
      tini \
    && uv venv /opt/netbox/venv

WORKDIR /build
RUN wget -qO- "https://github.com/netbox-community/netbox/archive/refs/tags/v${NETBOX_VERSION}.tar.gz" \
    | tar xz --strip-components=1

COPY requirements-container.txt /requirements-container.txt

ENV VIRTUAL_ENV=/opt/netbox/venv
RUN sed -i '/gunicorn/d' requirements.txt \
    && sed -i 's/social-auth-core/social-auth-core[all]/g' requirements.txt \
    && sed -i 's/django-storages/django-storages[azure,boto3,dropbox,google,libcloud,sftp]/g' requirements.txt \
    && uv pip install \
         -r requirements.txt \
         -r /requirements-container.txt

# Copy netbox source into final layout
RUN cp -r /build /opt/netbox/src

# Copy container-specific files over the netbox source
COPY docker/configuration.py /opt/netbox/src/netbox/netbox/configuration.py
COPY docker/granian.py       /opt/netbox/src/netbox/netbox/granian.py
COPY configuration/          /etc/netbox/config/

# Run collectstatic at build time (needs shell + venv)
WORKDIR /opt/netbox/src/netbox
RUN mkdir -p local static media reports scripts \
    && SECRET_KEY="dummyKeyWithMinimumLength-------------------------" \
       /opt/netbox/venv/bin/python manage.py collectstatic --no-input \
    && echo "build: chainguard-${NETBOX_VERSION}" > local/release.yaml

# Collect runtime shared libs needed by psycopg_c (libpq + full transitive chain)
RUN apk add --no-cache \
      libpq-17 \
      krb5-libs \
      libcom_err \
      keyutils-libs \
      libldap-2.7 \
      cyrus-sasl-heimdal-libs \
    && mkdir /runtime-libs \
    && cp -P \
         /usr/lib/libpq.so.5* \
         /usr/lib/libgssapi_krb5.so.2* \
         /usr/lib/libkrb5.so.3* \
         /usr/lib/libk5crypto.so.3* \
         /usr/lib/libkrb5support.so.0* \
         /usr/lib/libcom_err.so.2* \
         /usr/lib/libkeyutils.so.1* \
         /usr/lib/libldap.so.2* \
         /usr/lib/liblber.so.2* \
         /usr/lib/libsasl2.so.3* \
         /runtime-libs/

# Fix ownership for nonroot (65532) / root group (0)
RUN chown -R 65532:0 /opt/netbox/src/netbox/media \
                     /opt/netbox/src/netbox/reports \
                     /opt/netbox/src/netbox/scripts \
                     /opt/netbox/src/netbox/static \
                     /opt/netbox/src/netbox/local \
    && chmod -R g+w  /opt/netbox/src/netbox/media \
                     /opt/netbox/src/netbox/reports \
                     /opt/netbox/src/netbox/scripts

# ─── Runtime stage (python:latest — no shell, minimal attack surface) ─────────
FROM cgr.dev/chainguard/python:latest

COPY --from=builder /usr/bin/tini          /usr/bin/tini
COPY --from=builder /runtime-libs          /usr/lib/
COPY --from=builder /opt/netbox/venv       /opt/netbox/venv
COPY --from=builder /opt/netbox/src        /opt/netbox
COPY --from=builder /etc/netbox/config     /etc/netbox/config

COPY docker/entrypoint.py  /opt/netbox/entrypoint.py
COPY docker/launch.py      /opt/netbox/launch.py
COPY docker/health.py      /opt/netbox/health.py
COPY docker/superuser.py   /opt/netbox/superuser.py

ENV LANG=C.utf8 \
    PATH=/opt/netbox/venv/bin:$PATH \
    VIRTUAL_ENV=/opt/netbox/venv \
    UV_NO_CACHE=1

USER 65532

ENTRYPOINT ["/usr/bin/tini", "--", "/opt/netbox/venv/bin/python", "/opt/netbox/entrypoint.py"]
CMD ["/opt/netbox/venv/bin/python", "/opt/netbox/launch.py"]

HEALTHCHECK --interval=15s --timeout=3s --start-period=90s \
    CMD ["/opt/netbox/venv/bin/python", "/opt/netbox/health.py"]

LABEL org.opencontainers.image.title="NetBox on Chainguard" \
      org.opencontainers.image.description="CVE-clean NetBox image based on Chainguard Python" \
      org.opencontainers.image.source="https://github.com/netbox-community/netbox" \
      org.opencontainers.image.licenses="Apache-2.0"
