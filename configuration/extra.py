####
## Place custom configuration overrides here.
## This file is loaded after configuration.py.
## See https://docs.netbox.dev/en/stable/configuration/
####

## Example: custom plugins
# from netbox.configuration.configuration import PLUGINS
# PLUGINS.append('my_plugin')

## Example: S3 media storage
# STORAGES = {
#     'default': {
#         'BACKEND': 'storages.backends.s3boto3.S3Boto3Storage',
#         'OPTIONS': {
#             'access_key': '<access_key>',
#             'secret_key': '<secret_key>',
#             'bucket_name': 'netbox',
#             'region_name': 'us-east-1',
#         }
#     },
#     'staticfiles': {
#         'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
#     }
# }
