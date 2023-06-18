#!/usr/bin/env python3
"""Module to expose the inference code as an API service"""
from functools import lru_cache
from fastapi import FastAPI
import pandas as pd
import joblib

from sms_classification_inference_data import SpamClassificationRequest, SpamClassificationResponse
from message_preprocessor import MessagePreprocessor
import constants as c

vectorizer    = joblib.load(c.VECTORIZER_JOBLIB)
classifier    = joblib.load(c.CLASSIFIER_JOBLIB)
label_encoder = joblib.load(c.LABEL_ENCODER_JOBLIB)

message_preprocessor = MessagePreprocessor()
app = FastAPI()

@lru_cache()
def preprocess_message(input_data):
    """Combines all the preprocessing steps into one function
       lru_cache returns previous output if input is the same"""
    input_data      = pd.Series(input_data)
    clean_text      = message_preprocessor.clean_text(input_data)
    tokenize_test   = message_preprocessor.tokenize(clean_text)
    go_text         = message_preprocessor.remove_stop_words(tokenize_test)
    lemmatized_text = message_preprocessor.lemmatize(go_text)
    (_, X)          = message_preprocessor.vectorize(lemmatized_text, vectorizer)
    return X


@app.post('/api/v1/real-time-inference')
async def real_time_inference(request: SpamClassificationRequest) -> SpamClassificationResponse:
    """function for the real-time-inference endpoint.
       Runs the same preprocessing techniques in training
       and uses the training model artifacts for prediction"""

    messages = tuple(request.messages) #to make it cacheable
    X = preprocess_message(messages)

    y = classifier.predict(X)
    y = label_encoder.inverse_transform(y)

    output = pd.DataFrame(
        {
            'body' : messages,
            'label': pd.Series(y)
        }
    )
    response = {}
    response['response'] = output.to_dict('records')
    return response


@app.get('/api/v1/health-check', status_code=200)
async def health_check():
    """health check endpoint just to check if server is available"""
    return
