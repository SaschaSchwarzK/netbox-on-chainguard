# NetBox on Chainguard

CVE-clean NetBox Docker images built on [Chainguard Python](https://images.chainguard.dev/directory/image/python/overview).

Supports the NetBox releases listed in [`versions.json`](versions.json). Uses [granian](https://github.com/emmett-framework/granian) (WSGI/uvloop) instead of gunicorn.

## Image versions

Each image has an immutable downstream revision tag such as `4.6.8-r2` or
`4.7.2-r0`. The revision is incremented whenever that NetBox release is rebuilt
with a patched base image or dependency set. Moving convenience tags such as
`4.7.2` point to the newest revision; `latest` points to the newest configured
NetBox release.

`versions.json` is the single editable build matrix. Add a new entry at the end
when NetBox publishes a release, or remove an entry when it is no longer
supported:

```json
{"version": "4.7.3", "revision": 0}
```

Every version also has a matching file in `security-requirements/`. These
overrides replace vulnerable upstream pins while retaining the dependency
release line supported by that NetBox version.

### Released images and current vulnerabilities

This table is generated from Grype and Trivy scans of the published immutable
images. It is refreshed immediately after a release and by the nightly scan. A
clean release has no critical or high findings; medium and low findings remain
visible here and in its release notes.

<!-- released-images:start -->
| NetBox | Image | Critical | High | Medium | Low | Current vulnerabilities |
|---|---|---:|---:|---:|---:|---|
| 4.7.3 | `ghcr.io/saschaschwarzk/netbox-on-chainguard:4.7.3-r3` | 0 | 0 | 0 | 0 | ✅ None |
| 4.7.2 | `ghcr.io/saschaschwarzk/netbox-on-chainguard:4.7.2-r3` | 0 | 0 | 0 | 0 | ✅ None |
| 4.7.1 | `ghcr.io/saschaschwarzk/netbox-on-chainguard:4.7.1-r3` | 0 | 0 | 0 | 0 | ✅ None |
| 4.7.0 | `ghcr.io/saschaschwarzk/netbox-on-chainguard:4.7.0-r3` | 0 | 0 | 0 | 0 | ✅ None |
| 4.6.10 | `ghcr.io/saschaschwarzk/netbox-on-chainguard:4.6.10-r3` | 0 | 0 | 0 | 0 | ✅ None |
| 4.6.9 | `ghcr.io/saschaschwarzk/netbox-on-chainguard:4.6.9-r3` | 0 | 0 | 0 | 0 | ✅ None |
| 4.6.8 | `ghcr.io/saschaschwarzk/netbox-on-chainguard:4.6.8-r3` | 0 | 0 | 0 | 0 | ✅ None |
<!-- released-images:end -->

## Build arguments

| Argument | Description | Example |
|---|---|---|
| `NETBOX_VERSION` | NetBox release version | `4.7.0` |

The Dockerfile uses `cgr.dev/chainguard/python:latest-dev` for the build stage and `cgr.dev/chainguard/python:latest` for the runtime stage (the free public images). For production, both will be referenceable via a `.baseimage.lock` file or as build arguments.

## Local build

```sh
docker buildx build \
  --build-arg NETBOX_VERSION=4.7.0 \
  -t netbox-chainguard:4.7.0 \
  --load .
```

## Local run (docker compose)

```sh
export NETBOX_VERSION=4.7.0
docker compose up -d
```

NetBox will be available at http://localhost:8080.

Default credentials (dev only — change in `env/netbox.env`): `admin` / `admin`

## Security properties

- Non-root UID 65532, GID 0 (root group, no root privileges)
- No login shell (`/sbin/nologin`)
- No package manager in final image (Chainguard distroless-style)
- Read-only filesystem at runtime (no shell, no write access outside mounted volumes)
- Chainguard base has near-zero CVEs by design
- SBOM + provenance via `docker/build-push-action`

## Configuration

Mount custom config files into `/etc/netbox/config/`. All `*.py` files in that directory are loaded automatically after `configuration.py`.

See `configuration/extra.py` for examples (plugins, custom storage backends, etc.).

---

## Differences from netbox-docker

This project is inspired by [netbox-community/netbox-docker](https://github.com/netbox-community/netbox-docker) but differs in several significant ways.

### Base image

| | netbox-docker | netbox-on-chainguard |
|---|---|---|
| Base OS | Debian (bookworm) | Chainguard Python (Wolfi/Alpine-based) |
| Build stage | `debian:bookworm-slim` | `cgr.dev/chainguard/python:latest-dev` |
| Runtime stage | `debian:bookworm-slim` | `cgr.dev/chainguard/python:latest` |
| CVE surface | Moderate (Debian packages) | Near-zero (Chainguard hardened) |
| Shell in runtime | `/bin/bash` present | No shell at all |
| Package manager in runtime | `apt` present | No package manager |

### Runtime user

| | netbox-docker | netbox-on-chainguard |
|---|---|---|
| UID | 999 (`netbox`, created at build) | 65532 (`nonroot`, pre-existing in Chainguard image) |
| GID | 0 (root group) | 0 (root group) |
| Shell | `/bin/false` | `/sbin/nologin` (Chainguard default) |
| User created at build | Yes (`useradd`) | No (already exists in base image) |

### Entrypoint and scripts

netbox-docker uses shell scripts (`docker-entrypoint.sh`, `launch-netbox.sh`, `health.sh`). This project replaces all of them with Python scripts because the Chainguard runtime image contains no shell:

| netbox-docker | netbox-on-chainguard |
|---|---|
| `docker-entrypoint.sh` (bash) | `entrypoint.py` (Python) |
| `launch-netbox.sh` (bash) | `launch.py` (Python, `os.execv`) |
| `health.sh` (bash + curl) | `health.py` (Python `urllib`) |

### Web server

Both projects use [granian](https://github.com/emmett-framework/granian) with uvloop as the WSGI server (gunicorn is removed). Configuration is identical.

### Package installation

| | netbox-docker | netbox-on-chainguard |
|---|---|---|
| Installer | `uv` (copied from `ghcr.io/astral-sh/uv`) | `uv` (pre-installed in Chainguard dev image) |
| NetBox source | Cloned/copied from local path | Downloaded from GitHub releases tarball at build time |
| `collectstatic` | Run at build time | Run at build time |

### LDAP support

netbox-docker includes `django-auth-ldap` in `requirements-container.txt`. This project **does not** — `python-ldap` (a C extension that `django-auth-ldap` depends on) cannot be built with Chainguard's cross-compilation toolchain due to a linker sysroot issue (`libldap.a` is not compiled with `-fPIC`).

LDAP authentication is an **opt-in** feature in NetBox. It is not required for any other functionality including OIDC, SAML, or SSO. Users who need LDAP must build a custom image layer on top of this one.

### Read-only filesystem and plugin requirements

**This is the most important operational difference.**

The Chainguard runtime image has no shell and no package manager. The filesystem is effectively read-only at runtime — there is no way to `pip install` anything after the image is built.

**All Python packages must be present at build time.** This includes:

- NetBox plugins
- Any Python dependencies of those plugins
- Any optional NetBox features that require additional packages (e.g. `django-auth-ldap`, custom storage backends)

Add everything to `requirements-container.txt` before building:

```txt
# requirements-container.txt
dulwich==1.2.14
granian[uvloop]==2.8.2
python3-saml==1.16.0
--no-binary lxml
--no-binary xmlsec
sentry-sdk[django]==2.69.1

# Example: add plugins and their dependencies here
# netbox-bgp==0.14.0
# netbox-topology-views==4.1.1
```

Then enable the plugin in `configuration/extra.py`:

```python
from netbox.configuration.configuration import PLUGINS, PLUGINS_CONFIG
PLUGINS.append('netbox_bgp')
PLUGINS_CONFIG['netbox_bgp'] = {}
```

Attempting to reference a plugin that is not installed in the venv will cause NetBox to fail at startup with `ImproperlyConfigured`.

### Shared library handling

The Chainguard runtime image is minimal and does not include all shared libraries that Python C extensions require. This project explicitly copies the following libraries from the build stage into the runtime image to support `psycopg[c]` (the PostgreSQL C driver):

- `libpq.so.5` — PostgreSQL client library
- `libgssapi_krb5.so.2`, `libkrb5.so.3`, `libk5crypto.so.3`, `libkrb5support.so.0` — Kerberos (required by libpq)
- `libcom_err.so.2`, `libkeyutils.so.1` — Kerberos support libs
- `libldap.so.2`, `liblber.so.2` — LDAP (required by libpq for GSSAPI)
- `libsasl2.so.3` — SASL (required by libldap)

`libssl.so.3` and `libcrypto.so.3` are already present in the Chainguard Python runtime image.

### What is intentionally omitted

Compared to netbox-docker, the following are not included and not planned:

| Feature | Reason |
|---|---|
| LDAP auth (`django-auth-ldap`) | Cannot build `python-ldap` C extension with Chainguard cross-toolchain |
| `openssh-client` | Not needed for core NetBox functionality |
| `bzip2` | Not needed |
| Debian system Python | Replaced by Chainguard's Python |
| `apt`/`apk` in runtime | Intentionally absent (security property) |
