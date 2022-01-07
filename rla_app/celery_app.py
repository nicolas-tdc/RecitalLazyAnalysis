"""This files handles plugging Celery app to broker and backend"""

from __future__ import absolute_import
from celery import Celery

app = Celery('rla_app',
             broker='INSERT_BROKER',
             backend='INSERT_BACKEND',
             include=['rla_app.tasks'])
