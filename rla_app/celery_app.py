from __future__ import absolute_import
from celery import Celery

app = Celery('rla_app',
             broker='amqp://ntdc:ntdc123@localhost/ntdc_vhost',
             backend='rpc://',
             include=['rla_app.tasks'])
