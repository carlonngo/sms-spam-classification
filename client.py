#!/usr/bin/env python3
import requests
from pprint import pprint

URL = 'http://127.0.0.1:8000/api/v1/real-time-inference'

print("SPAM and HAM")
payload = {
    'messages': [
        "If you don't, your prize will go to another customer. T&C at www.t-c.biz 18+ 150p/min Polo Ltd Suite 373 London W1J",
        "Did u fix the teeth?if not do it asap.ok take care."
    ]
}
resp = requests.post(URL, json=payload)
pprint(resp.json())

print("ALL HAM")
payload = {
    'messages': [
        "And how you will do that, princess? :)",
        "I have gone into get info bt dont know what to do",
        "Yeah, probably here for a while",
        "Sent me ur email id soon",
    ]
}
resp = requests.post(URL, json=payload)
pprint(resp.json())

print("ALL SPAM")
payload = {
    'messages': [
        "PRIVATE! Your 2003 Account Statement for <fone no> shows 800 un-redeemed S. I. M. points. Call 08715203656 Identifier Code: 42049 Expires 26/10/04",
        "YOU ARE CHOSEN TO RECEIVE A £350 AWARD! Pls call claim number 09066364311 to collect your award which you are selected to receive as a valued mobile customer.",
        "Someonone you know is trying to contact you via our dating service! To find out who it could be call from your mobile or landline 09064015307 BOX334SK38ch"
    ]
}
resp = requests.post(URL, json=payload)
pprint(resp.json())

print("MALFORMED REQUEST")
payload = {
    'mess': [
        "PRIVATE! Your 2003 Account Statement for <fone no> shows 800 un-redeemed S. I. M. points. Call 08715203656 Identifier Code: 42049 Expires 26/10/04",
        "YOU ARE CHOSEN TO RECEIVE A £350 AWARD! Pls call claim number 09066364311 to collect your award which you are selected to receive as a valued mobile customer.",
        "Someonone you know is trying to contact you via our dating service! To find out who it could be call from your mobile or landline 09064015307 BOX334SK38ch"
    ]
}
resp = requests.post(URL, json=payload)
pprint(resp.json())

print("MALFORMED REQUEST 2")
payload = [
        "PRIVATE! Your 2003 Account Statement for <fone no> shows 800 un-redeemed S. I. M. points. Call 08715203656 Identifier Code: 42049 Expires 26/10/04",
        "YOU ARE CHOSEN TO RECEIVE A £350 AWARD! Pls call claim number 09066364311 to collect your award which you are selected to receive as a valued mobile customer.",
        "Someonone you know is trying to contact you via our dating service! To find out who it could be call from your mobile or landline 09064015307 BOX334SK38ch"
]
resp = requests.post(URL, json=payload)
pprint(resp.json())