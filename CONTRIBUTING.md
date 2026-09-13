# Contributing

## Local setup

```sh
git clone https://github.com/<org>/netbox-on-chainguard.git
cd netbox-on-chainguard

cp env/netbox.env.example env/netbox.env
cp env/postgres.env.example env/postgres.env
# Edit both files and fill in real values — they are gitignored
```

## Building

```sh
export NETBOX_VERSION=4.7.0
docker buildx build --build-arg NETBOX_VERSION=${NETBOX_VERSION} -t netbox-chainguard:${NETBOX_VERSION} --load .
```

## Running locally

```sh
docker compose up -d
```

## Adding plugins

All plugins and their Python dependencies must be added to `requirements-container.txt` **before** building the image. The runtime filesystem is read-only — nothing can be installed after the image is built.

1. Add the plugin and any dependencies to `requirements-container.txt`
2. Enable the plugin in `configuration/extra.py`
3. Rebuild the image

## Pull requests

- Keep changes focused — one concern per PR
- Test locally with `docker compose up` before opening a PR
- The build workflow runs on every PR (build only, no push)
- The scan workflow can be triggered manually to verify CVE status
