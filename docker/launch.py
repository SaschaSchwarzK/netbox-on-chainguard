#!/opt/netbox/venv/bin/python
"""Exec granian WSGI server — replaces launch.sh."""
import os

os.execv(
    "/opt/netbox/venv/bin/granian",
    [
        "granian",
        "--host", "::",
        "--interface", "wsgi",
        "--no-ws",
        "--respawn-failed-workers",
        "--loop", "uvloop",
        "--log",
        "--log-level", "info",
        "--access-log",
        "--working-dir", "/opt/netbox/netbox/",
        "--static-path-route", "/static",
        "--static-path-mount", "/opt/netbox/netbox/static/",
        "--static-path-dir-to-file", "index.html",
        "--pid-file", "/tmp/granian.pid",
        "--workers", os.environ.get("GRANIAN_WORKERS", "4"),
        "--port", os.environ.get("GRANIAN_PORT", "8080"),
        "netbox.granian:application",
    ],
)
