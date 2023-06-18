#!/usr/bin/env python3
"""Module holding constants used in training and inference code for SMS classification"""
import os

RAW_FILE = '../data/SMSSpamCollection'
MODEL_DIRECTORY = '../model/'

VECTORIZER_JOBLIB    = os.path.join(MODEL_DIRECTORY, 'vectorizer.joblib')
CLASSIFIER_JOBLIB    = os.path.join(MODEL_DIRECTORY, 'classifier.joblib')
LABEL_ENCODER_JOBLIB = os.path.join(MODEL_DIRECTORY, 'label_encoder.joblib')

TOKENIZER_JOBLIB            = os.path.join(MODEL_DIRECTORY, 'tokenizer.joblib')
KERAS_LABEL_ENCODER_JOBLIB  = os.path.join(MODEL_DIRECTORY, 'keras_label_encoder.joblib')
KERAS_CLASSIFIER            = os.path.join(MODEL_DIRECTORY, 'keras_classifier.h5')
