"""This file handles celery tasks for text analysis."""

from __future__ import absolute_import

from rla_app.celery_app import app

from collections import Counter
import re

from rla_app.rla_api import crud, schemas


@app.task()
def rla_zipf_task(db, text, analysis_id):
    """
    :param text:
    :param db:
    :param analysis_id:
    :return: Celery Task to analyse Zipf's Law and upadate text analysis.
    """

    formatted = rla_format_text(text)
    words_freq = rla_word_frequencies(formatted)

    if words_freq:
        zipf = rla_calculate_zipf(words_freq)
        # Update text analysis with zipf calculations.
        analysis_crud_data = schemas.TextAnalysisPatch
        analysis_crud_data.id = analysis_id
        analysis_crud_data.numeric_diff = zipf['numeric_diff']
        analysis_crud_data.percentage_diff = zipf['percentage_diff']
        return crud.rla_patch_text_analysis(db, analysis_crud_data)

    else:
        return {'No words found.'}


def rla_calculate_zipf(words_freq):
    """
    :param words_freq:
    :return: Compare Zipf Law's prediction with actual words frequencies for full text.
    """

    zipf = {}
    num_diff = 0
    percentage_diff = 0

    for key, word in enumerate(words_freq):
        word_data = rla_word_zipf(word, key, words_freq[0][1])
        num_diff += abs(word_data['numeric_diff'])
        percentage_diff += word_data['percentage_diff']

    # Calculate average values
    zipf['numeric_diff'] = num_diff / len(words_freq)
    zipf['percentage_diff'] = percentage_diff / len(words_freq)

    return zipf


def rla_word_zipf(word, key, first_frequency):
    """
    :param word:
    :param key:
    :param first_frequency:
    :return: Compare Zipf's Law's prediction with actual single word frequency.
    """

    zipf_freq = first_frequency / (key + 1)

    return {
        'numeric_diff': word[1] - zipf_freq,
        'percentage_diff': (word[1] / zipf_freq) * 100,
    }


def rla_format_text(text):
    """
    :param text:
    :return: Removes all characters except letters and spaces from the text.
    """

    pat = re.compile(r'[^a-zA-Z ]+')
    if isinstance(text, str):
        return re.sub(pat, '', text)
    else:
        return re.sub(pat, '', text.decode('utf-8'))


def rla_word_frequencies(text):
    """
    :param text:
    :return: Create a list of tuples containing the most frequent words and their frequencies in descending order.
    """

    words = text.split()
    return Counter(words).most_common()
