"""A standard implementation of celeryconfig.

See:
http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html#entries
http://celery.readthedocs.org/en/latest/configuration.html#example-configuration-file
"""

from datetime import timedelta
from const import REDIS_SERVER

BROKER_URL = 'redis://{hostname}:6379/0'.format(hostname=REDIS_SERVER)
BROKER_TRANSPORT_OPTIONS = {
    'fanout_prefix': True, 'fanout_patterns': True, 'visibility_timeout': 480
}
CELERY_RESULT_BACKEND = BROKER_URL

CELERYBEAT_SCHEDULE = {
    'update_all-on-interval': {
        'task': 'service_layer.tasks.update_all',  # complete name is needed
        'schedule': timedelta(seconds=10),
        'args': (),
    },
}

CELERY_TIMEZONE = 'UTC'
