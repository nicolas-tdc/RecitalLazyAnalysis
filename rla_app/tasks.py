from __future__ import absolute_import

from celery_app import app


@app.task()
def count_letters(text):
    count = len(text)
    return count

# If count_letters or count_words high enough, process Zipf's law

# Language used

# Politeness

