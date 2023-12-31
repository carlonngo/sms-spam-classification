#!/usr/bin/env python3
"""Module for MessagePreprocessor class"""
import re
import html
from typing import List,Tuple
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

class MessagePreprocessor():
    """Class to package string preprocessing functionalities for NLP"""
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()


    def _clean_text(self, text: str) -> str:
        text = html.unescape(text)
        alphabet_string = re.sub("[^A-Za-z ]", " ", text)
        return alphabet_string.lower()


    def _remove_stop_words(self, text: List[str]) -> List[str]:
        stop_words = stopwords.words("english")
        filtered_text = [word for word in text if word not in stop_words]

        return filtered_text


    def _lemmatize(self, text: List[str]) -> List[str]:
        lemmas = [self.lemmatizer.lemmatize(word) for word in text]
        return lemmas


    def _dummy_analyzer(self, text: List[str]) -> List[str]:
        return text


    def clean_text(self, text:pd.Series) -> pd.Series:
        """Removes html and special characters present in a Series String"""
        return text.apply(self._clean_text)


    def tokenize(self, text:pd.Series) -> pd.Series:
        """Converts sentences into list of words"""
        return text.apply(word_tokenize)


    def remove_stop_words(self, text:pd.Series) -> pd.Series:
        """Removes common stop words from list of words"""
        return text.apply(self._remove_stop_words)


    def lemmatize(self, text:pd.Series) -> pd.Series:
        """Gets the rootword of words in a sentence using Lemmatization"""
        return text.apply(self._lemmatize)


    def vectorize(self, text:pd.Series,
                  vectorizer:TfidfVectorizer=None) -> Tuple[TfidfVectorizer, pd.Series]:
        """Converts list of words to numerical numpy array"""
        if not vectorizer:
            vectorizer = TfidfVectorizer(analyzer=self._dummy_analyzer)
            features = vectorizer.fit_transform(text)
        else:
            features = vectorizer.transform(text)

        vectorized_text = features.toarray()
        return (vectorizer, vectorized_text)
