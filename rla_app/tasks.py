"""This file handles celery tasks for text analysis."""

from __future__ import absolute_import

from celery_app import app

from collections import Counter
from math import floor, log
import re


# @app.task()
def rla_zipf_task(text):
    """
    :param text:
    :return: Celery Task to create Zipf's Law text analysis.
    """

    formatted = rla_format_text(text)
    words_freq = rla_word_frequencies(formatted)
    if words_freq:
        # old_account = db.query(models.Account).filter(models.Account.id == id)
        # if not old_account.first():
        #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        #                         detail=f'old_account with the id {id} is not available')
        # old_account.update({'name': name, 'deposits_made': deposits_made, 'total ': total})
        # db.commit()
        return rla_calculate_zipf(words_freq)
    else:
        return {'No words found.'}


def rla_calculate_zipf(words_freq):
    """
    :param words_freq:
    :return: Compare Zipf Law's prediction with actual words frequencies for full text.
    """

    zipf = {
        'average_diff': {},
        'word_data': []
    }
    full_num_diff = 0
    full_percentage_diff = 0

    for key, word in enumerate(words_freq):
        word_data = rla_word_zipf(word, key, words_freq[0][1])
        zipf['word_data'].append(word_data)
        full_num_diff += abs(word_data['numeric_diff'])
        full_percentage_diff += word_data['percentage_diff']

        max_average_exponent = floor(log(len(words_freq), 10))
        for i in range(1, max_average_exponent + 1):
            if key == (10 ** i) - 1:
                zipf['average_diff']['numeric_' + str(10 ** i)] = full_num_diff / 10 ** i
                zipf['average_diff']['percentage_' + str(10 ** i)] = full_percentage_diff / 10 ** i

    zipf['average_diff']['numeric_full'] = full_num_diff / len(words_freq)
    zipf['average_diff']['percentage_full'] = full_percentage_diff / len(words_freq)

    return zipf


def rla_word_zipf(word, key, first_frequency):
    """
    :param word:
    :param key:
    :param first_frequency:
    :return: Compare Zipf's Law's prediction with actual single word frequency.
    """

    zipf_freq = first_frequency / (key + 1)
    numeric_diff = word[1] - zipf_freq
    percentage_diff = (word[1] / zipf_freq) * 100
    return {
        'word': word[0],
        'rank': key + 1,
        'freq': word[1],
        'zipf_freq': zipf_freq,
        'numeric_diff': numeric_diff,
        'percentage_diff': percentage_diff,
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
