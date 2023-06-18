#!/usr/bin/env python3
"""Module holding constants used in training and inference code for SMS classification"""
import os

RAW_FILE = '../data/SMSSpamCollection'
MODEL_DIRECTORY = '../model/'

VECTORIZER_JOBLIB    = os.path.join(MODEL_DIRECTORY, 'vectorizer.joblib')
CLASSIFIER_JOBLIB    = os.path.join(MODEL_DIRECTORY, 'classifier.joblib')
LABEL_ENCODER_JOBLIB = os.path.join(MODEL_DIRECTORY, 'label_encoder.joblib')
