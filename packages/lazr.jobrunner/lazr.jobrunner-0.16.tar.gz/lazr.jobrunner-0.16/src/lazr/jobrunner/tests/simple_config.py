BROKER_URL = "amqp://"
CELERY_RESULT_BACKEND = "amqp"
CELERY_IMPORTS = ("lazr.jobrunner.tests.test_celerytask", )
CELERYD_CONCURRENCY = 1
