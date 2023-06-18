#!/usr/bin/env python3
"""Module to expose the inference code as an API service"""
from functools import lru_cache
from fastapi import FastAPI
import numpy as np
import pandas as pd
import joblib
from tensorflow.keras.models import load_model
from keras_preprocessing.sequence import pad_sequences

from sms_classification_inference_data import SpamClassificationRequest, SpamClassificationResponse
from message_preprocessor import MessagePreprocessor
import constants as c

vectorizer    = joblib.load(c.VECTORIZER_JOBLIB)
classifier    = joblib.load(c.CLASSIFIER_JOBLIB)
label_encoder = joblib.load(c.LABEL_ENCODER_JOBLIB)
tokenizer           = joblib.load(c.TOKENIZER_JOBLIB)
keras_label_encoder = joblib.load(c.KERAS_LABEL_ENCODER_JOBLIB)
keras_classifier    = load_model(c.KERAS_CLASSIFIER)

message_preprocessor = MessagePreprocessor()
app = FastAPI()

@lru_cache()
def preprocess_message(input_data: tuple):
    """Combines all the preprocessing steps into one function
       lru_cache returns previous output if input is the same"""
    input_data      = pd.Series(input_data)
    clean_text      = message_preprocessor.clean_text(input_data)
    tokenize_test   = message_preprocessor.tokenize(clean_text)
    go_text         = message_preprocessor.remove_stop_words(tokenize_test)
    lemmatized_text = message_preprocessor.lemmatize(go_text)
    (_, X)          = message_preprocessor.vectorize(lemmatized_text, vectorizer)
    return X


@lru_cache()
def get_keras_input_seq_len() -> int:
    """Gets the expected input sequence len of the keras model"""
    config  = keras_classifier.get_config()
    max_len = config["layers"][0]["config"]["batch_input_shape"][1]
    return max_len


@lru_cache()
def text_to_sequence(input_data: tuple):
    """Converts input string to sequences and adds padding
       so that it will be compatible with the keras model"""
    input_data = pd.Series(input_data)
    sequences  = tokenizer.texts_to_sequences(input_data)
    expect_sequence_len = get_keras_input_seq_len()
    sequences  = pad_sequences(sequences, maxlen=expect_sequence_len)
    return sequences

def format_spam_classification_resp(messages: tuple,
                                    label: pd.Series) -> SpamClassificationResponse:
    """Helper function to format output of predictions into SpamClassificationResponse"""
    output = pd.DataFrame(
        {
            'body' : messages,
            'label': label
        }
    )
    response = {}
    response['response'] = output.to_dict('records')
    return response

@app.post('/api/v1/real-time-inference')
async def real_time_inference(request: SpamClassificationRequest) -> SpamClassificationResponse:
    """function for the real-time-inference endpoint.
       Runs the same preprocessing techniques in training
       and uses the training model artifacts for prediction"""

    messages = tuple(request.messages) #to make it cacheable
    X = preprocess_message(messages)

    y = classifier.predict(X)
    y = label_encoder.inverse_transform(y)

    response = format_spam_classification_resp(messages, pd.Series(y))
    return response


@app.post('/api/v2/real-time-inference')
async def deep_real_time_inference(request: SpamClassificationRequest)-> SpamClassificationResponse:
    """function for the real-time-inference v2 endpoint.
       Converts message body to sequence and uses a keras
       model artifact for prediction"""

    messages = tuple(request.messages) #to make it cacheable
    X = text_to_sequence(messages)

    y = keras_classifier.predict(X)
    y = np.round(y).astype(int)
    y = keras_label_encoder.inverse_transform(y)

    response = format_spam_classification_resp(messages, pd.Series(y))
    return response


@app.get('/api/v1/health-check', status_code=200)
async def health_check():
    """health check endpoint just to check if server is available"""
    return
