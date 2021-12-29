from __future__ import absolute_import
from celery import Celery

app = Celery('rla_app',
             broker='amqp://ntdc:ntdc123@localhost:5672//',
             backend='redis://:ntdc123@localhost:6379/0',
             include=['rla_app.tasks'])
