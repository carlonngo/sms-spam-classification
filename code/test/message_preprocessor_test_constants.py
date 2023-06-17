#!/usr/bin/env python3
import pandas as pd

RAW_TEXT_SERIES = pd.Series(
    [
        'A Message with no Special characters',
        'A Message with... special characters',
        'A Message with &lt;#&gt; html'
    ]
)

CLEANED_TEXT_SERIES = pd.Series(
    [
        'a message with no special characters',
        'a message with    special characters',
        'a message with     html'
    ]
)

TOKENIZED_TEXT_SERIES = pd.Series(
    [
        ['a', 'message', 'with', 'no', 'special', 'characters'],
        ['a', 'message', 'with', 'special', 'characters'],
        ['a', 'message', 'with', 'html']
    ]
)

GO_TEXT_SERIES = pd.Series(
    [
        ['message', 'special', 'characters'],
        ['message', 'special', 'characters'],
        ['message', 'html']
    ]
)

LEMMATIZED_TEXT_SERIES = pd.Series(
    [
        ['message', 'special', 'character'],
        ['message', 'special', 'character'],
        ['message', 'html']
    ]
)