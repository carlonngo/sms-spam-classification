#!/usr/bin/env python3
import re
import pandas as pd
import html
from typing import List,Tuple
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer

class MessagePreprocessor():
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
        return text.apply(self._clean_text)
    

    def tokenize(self, text:pd.Series) -> pd.Series:
        return text.apply(word_tokenize)
    

    def remove_stop_words(self, text:pd.Series) -> pd.Series:
        return text.apply(self._remove_stop_words)
    

    def lemmatize(self, text:pd.Series) -> pd.Series:
        return text.apply(self._lemmatize)


    def vectorize(self, text:pd.Series, vectorizer:TfidfVectorizer=None) -> Tuple[TfidfVectorizer, pd.Series]:
        if not vectorizer:
            vectorizer = TfidfVectorizer(analyzer=self._dummy_analyzer)
            X = vectorizer.fit_transform(text)
        else:
            X = vectorizer.transform(text)

        vectorized_text = X.toarray()
        return (vectorizer, vectorized_text)
