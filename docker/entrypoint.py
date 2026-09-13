#!/opt/netbox/venv/bin/python
"""Container entrypoint: waits for DB, runs migrations, creates superuser, then execs CMD."""
import os
import subprocess
import sys
import time

WORKDIR = "/opt/netbox/netbox"
PYTHON = "/opt/netbox/venv/bin/python"
MANAGE = [PYTHON, "manage.py"]

os.chdir(WORKDIR)
os.umask(0o002)


def manage(*args, **kwargs):
    return subprocess.run([*MANAGE, *args], **kwargs)


# Wait for DB
timeout = int(os.environ.get("MAX_DB_WAIT_TIME", 30))
interval = int(os.environ.get("DB_WAIT_TIMEOUT", 3))
elapsed = 0

while elapsed < timeout:
    result = manage("showmigrations", capture_output=True)
    if result.returncode == 0:
        break
    last_line = (result.stdout + result.stderr).decode().strip().splitlines()
    print(last_line[-1] if last_line else "DB not ready")
    print(f"Waiting on DB... ({elapsed}s / {timeout}s)")
    time.sleep(interval)
    elapsed += interval
else:
    print(f"DB not ready after {timeout}s, aborting.")
    sys.exit(1)

# Migrate if needed
if manage("migrate", "--check", capture_output=True).returncode != 0:
    print("Applying database migrations")
    manage("migrate", "--no-input", check=True)
    manage("trace_paths", "--no-input", check=True)
    manage("remove_stale_contenttypes", "--no-input", check=True)
    manage("clearsessions", check=True)
    manage("reindex", "--lazy", check=True)

# Create superuser
if os.environ.get("SKIP_SUPERUSER") == "true":
    print("Skipping superuser creation")
else:
    with open("/opt/netbox/superuser.py", "rb") as f:
        manage("shell", "--no-startup", "--no-imports", "--interface", "python",
               input=f.read(), check=True)

print("Initialisation done.")

# Exec CMD
os.execv(sys.argv[1], sys.argv[1:])
