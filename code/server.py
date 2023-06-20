#!/usr/bin/env python3
"""Module to expose the inference code as an API service"""
from typing import Tuple
from functools import lru_cache
from fastapi import FastAPI
import pandas as pd

from sms_classification_inference_data import SpamClassificationRequest, SpamClassificationResponse
from inference import Inference, MachineLearningInference, DeepLearningInference
import constants as c

ml_inference = MachineLearningInference(c.CLASSIFIER_JOBLIB,
                                        c.VECTORIZER_JOBLIB,
                                        c.LABEL_ENCODER_JOBLIB)
deep_inference = DeepLearningInference(c.KERAS_CLASSIFIER,
                                       c.TOKENIZER_JOBLIB,
                                       c.KERAS_LABEL_ENCODER_JOBLIB)
app = FastAPI()


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


@lru_cache
def infer(messages:Tuple[str], inference:Inference) -> SpamClassificationResponse:
    """Generic inference function using inference interfaces"""
    X = inference.preprocess(messages)
    y = inference.predict(X)

    y = format_spam_classification_resp(messages, pd.Series(y))
    return y


@app.post('/api/v1/real-time-inference')
async def real_time_inference(request: SpamClassificationRequest) -> SpamClassificationResponse:
    """function for the real-time-inference endpoint.
       Runs the same preprocessing techniques in training
       and uses the training model artifacts for prediction"""
    messages = tuple(request.messages) #to make it cacheable
    return infer(messages, ml_inference)


@app.post('/api/v2/real-time-inference')
async def deep_real_time_inference(request: SpamClassificationRequest)-> SpamClassificationResponse:
    """function for the real-time-inference v2 endpoint.
       Converts message body to sequence and uses a keras
       model artifact for prediction"""
    messages = tuple(request.messages) #to make it cacheable
    return infer(messages, deep_inference)


@app.get('/api/v1/health-check', status_code=200)
async def health_check():
    """health check endpoint just to check if server is available"""
    return
