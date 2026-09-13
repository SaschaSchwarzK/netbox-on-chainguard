#!/opt/netbox/venv/bin/python
"""Health check — replaces health.sh."""
import os
import sys
import urllib.request
import urllib.error

port = os.environ.get("GRANIAN_PORT", "8080")
try:
    urllib.request.urlopen(f"http://localhost:{port}/login/", timeout=3)
except urllib.error.HTTPError:
    pass  # any HTTP response (including 302) means the app is up
except Exception:
    sys.exit(1)
