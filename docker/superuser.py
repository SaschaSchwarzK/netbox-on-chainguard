import sys
from os import environ

from django.conf import settings
from users.choices import TokenVersionChoices
from users.models import Token, User


def _read_secret(secret_name: str, default: str | None = None) -> str | None:
    try:
        with open('/run/secrets/' + secret_name, encoding='utf-8') as f:
            return f.readline().strip()
    except OSError:
        return default


su_name = environ.get('SUPERUSER_NAME', 'admin')
su_email = environ.get('SUPERUSER_EMAIL', 'admin@example.com')
su_password = _read_secret('superuser_password', environ.get('SUPERUSER_PASSWORD'))
su_api_token = _read_secret('superuser_api_token', environ.get('SUPERUSER_API_TOKEN'))
su_api_key = _read_secret('superuser_api_key', environ.get('SUPERUSER_API_KEY'))

if User.objects.filter(username=su_name).exists():
    print(f'User "{su_name}" already exists.')
    sys.exit(0)

if not su_password:
    print('No superuser password provided. Set SUPERUSER_PASSWORD. Skipping.')
    sys.exit(0)

u = User.objects.create_superuser(su_name, su_email, su_password)
if not settings.API_TOKEN_PEPPERS:
    print(f'Superuser created: {su_name} / {su_email} (no API token: API_TOKEN_PEPPERS not set)')
elif su_api_key and su_api_token:
    t = Token.objects.create(user=u, token=su_api_token, version=TokenVersionChoices.V2, key=su_api_key)
    print(f'Superuser created: {su_name} / {su_email}, API auth header prefix: {t.get_auth_header_prefix()}')
else:
    print(f'Superuser created: {su_name} / {su_email} (no API token: SUPERUSER_API_TOKEN/KEY not set)')
