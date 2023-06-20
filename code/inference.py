#!/usr/bin/env python3
"""module containing the Inference Classes"""
from abc import ABC, abstractmethod
from typing import Tuple
import numpy as np
import pandas as pd
import joblib
from tensorflow.keras.models import load_model
from keras_preprocessing.sequence import pad_sequences
from message_preprocessor import MessagePreprocessor

class Inference(ABC):
    """Base class for Inference"""
    def __init__(self, classifier:str, vectorizer:str, label_encoder:str) -> None:
        self._classifier    = joblib.load(classifier)
        self._vectorizer    = joblib.load(vectorizer)
        self._label_encoder = joblib.load(label_encoder)


    @abstractmethod
    def preprocess(self, messages: Tuple[str]):
        """abstract method for preprocessing messages into vectors.
           Subclasses are required to implement this"""


    @abstractmethod
    def predict(self, X):
        """abstract method for predictions.
           Subclasses are required to implement this"""


class MachineLearningInference(Inference):
    """Class for ML inference"""
    _message_preprocessor = MessagePreprocessor()

    def preprocess(self, messages: Tuple[str]):
        """Combines all the preprocessing steps into one function
        lru_cache returns previous output if input is the same"""
        messages        = pd.Series(messages)
        clean_text      = self._message_preprocessor.clean_text(messages)
        tokenize_test   = self._message_preprocessor.tokenize(clean_text)
        go_text         = self._message_preprocessor.remove_stop_words(tokenize_test)
        lemmatized_text = self._message_preprocessor.lemmatize(go_text)
        (_, X)          = self._message_preprocessor.vectorize(lemmatized_text, self._vectorizer)
        return X


    def predict(self, X):
        """predict and inverse the label"""
        y = self._classifier.predict(X)
        y = self._label_encoder.inverse_transform(y)
        return y


class DeepLearningInference(Inference):
    """Class for DL inference"""
    def __init__(self, classifier:str, vectorizer:str, label_encoder:str) -> None:
        self._classifier    = load_model(classifier)
        self._vectorizer    = joblib.load(vectorizer)
        self._label_encoder = joblib.load(label_encoder)


    def _get_keras_input_seq_len(self) -> int:
        """Gets the expected input sequence len of the keras model"""
        config  = self._classifier.get_config()
        max_len = config["layers"][0]["config"]["batch_input_shape"][1]
        return max_len


    def preprocess(self, messages: Tuple[str]):
        """Converts input string to sequences and adds padding
        so that it will be compatible with the keras model"""
        messages = pd.Series(messages)
        sequences  = self._vectorizer.texts_to_sequences(messages)
        expect_sequence_len = self._get_keras_input_seq_len()
        sequences  = pad_sequences(sequences, maxlen=expect_sequence_len)
        return sequences


    def predict(self, X):
        """predict and inverse the label"""
        y = self._classifier.predict(X)
        y = np.round(y).astype(int)
        y = self._label_encoder.inverse_transform(y)
        return y
