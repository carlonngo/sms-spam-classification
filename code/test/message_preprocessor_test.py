#!/usr/bin/env python3
"""pytest module to perform unit testing on the MessagePreprocessor class"""
import pytest
from pandas.testing import assert_series_equal
from message_preprocessor import MessagePreprocessor
import message_preprocessor_test_constants as c

@pytest.mark.parametrize(
    'raw_text_series, expected_cleaned_text_series',
    [
        (
            c.RAW_TEXT_SERIES,
            c.CLEANED_TEXT_SERIES
        ),
    ]
)
def test_clean_text(raw_text_series, expected_cleaned_text_series):
    """Asserts the result of clean_text() to expected_cleaned_text_series"""
    message_preprocessor = MessagePreprocessor()
    cleaned_test = message_preprocessor.clean_text(raw_text_series)
    assert_series_equal(cleaned_test, expected_cleaned_text_series)


@pytest.mark.parametrize(
    'cleaned_text_series, expected_tokenized_text_series',
    [
        (
            c.CLEANED_TEXT_SERIES,
            c.TOKENIZED_TEXT_SERIES
        ),
    ]
)
def test_tokenize_text(cleaned_text_series, expected_tokenized_text_series):
    """Asserts the result of tokenize() to expected_tokenized_text_series"""
    message_preprocessor = MessagePreprocessor()
    tokenized_text_series = message_preprocessor.tokenize(cleaned_text_series)
    assert_series_equal(tokenized_text_series, expected_tokenized_text_series)


@pytest.mark.parametrize(
    'tokenized_text_series, expected_go_text_series',
    [
        (
            c.TOKENIZED_TEXT_SERIES,
            c.GO_TEXT_SERIES
        ),
    ]
)
def test_remove_stop_words(tokenized_text_series, expected_go_text_series):
    """Asserts the result of remove_stop_words() to expected_go_text_series"""
    message_preprocessor = MessagePreprocessor()
    go_text_series = message_preprocessor.remove_stop_words(tokenized_text_series)
    assert_series_equal(go_text_series, expected_go_text_series)


@pytest.mark.parametrize(
    'go_text_series, expected_lemmatized_text_series',
    [
        (
            c.GO_TEXT_SERIES,
            c.LEMMATIZED_TEXT_SERIES
        ),
    ]
)
def test_lemmatize(go_text_series, expected_lemmatized_text_series):
    """Asserts the result of lemmatize() to expected_lemmatized_text_series"""
    message_preprocessor = MessagePreprocessor()
    lemmatized_text_series = message_preprocessor.lemmatize(go_text_series)
    assert_series_equal(lemmatized_text_series, expected_lemmatized_text_series)
