#!/usr/bin/env python3
"""Pydantic data classes to help define data format/schema,
   expecations and perform validations"""
from typing import List
from pydantic import BaseModel

class SpamClassificationRequest(BaseModel):
    """schema that defines the expected schema of input payload"""
    messages: List[str]

class SingleResponse(BaseModel):
    """schema that defines the expected output per message"""
    body: str
    label: str

class SpamClassificationResponse(BaseModel):
    """schema that defines the expected response"""
    response: List[SingleResponse]
