from datetime import timedelta

# values unique to service_layer
DESTINATION_PREFIX = "/data/"
REDIS_SERVER = "redis.local"

# standard celeryconfig.py values
BROKER_URL = "redis://{hostname}:6379/0".format(hostname=REDIS_SERVER)
BROKER_TRANSPORT_OPTIONS = {'fanout_prefix': True, 'fanout_patterns': True, 'visibility_timeout': 480}
CELERY_RESULT_BACKEND = BROKER_URL

CELERYBEAT_SCHEDULE = {
    'update_all-on-interval': {
        'task': 'service_layer.tasks.update_all', # notice that the complete name is needed
        'schedule': timedelta(seconds=60),
        #'schedule': timedelta(minutes=1),
        'args': ('config.yml',)
    },
}

CELERY_TIMEZONE = 'UTC'
