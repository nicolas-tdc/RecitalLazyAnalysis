"""This file handles tests for zipf calculations task."""

import tasks


def test_rla_word_frequencies():
    expected = [('unit', 2), ('testing', 1)]
    test = tasks.rla_word_frequencies('unit unit testing')
    assert expected == test


def test_rla_format_text():
    expected = 'unit testing'
    test = tasks.rla_format_text('unit-123 */tes__ting!...')
    assert expected == test


def test_rla_word_zipf():
    expected = {'numeric_diff': 0, 'percentage_diff': 100}
    test = tasks.rla_word_zipf(('testing', 10), 9, 100)
    assert expected == test


def test_rla_calculate_zipf():
    expected = {'numeric_diff': 0, 'percentage_diff': 100}
    test = tasks.rla_calculate_zipf([('unit', 2), ('testing', 1)])
    assert expected == test


def test_rla_zipf_task():
    expected = {'No words found.'}
    test = tasks.rla_zipf_task('', '', 1)
    assert expected == test
