from datetime import datetime
import datetime
import string
import random

def code_document():
    length = 16
    lowercaseLetters = string.ascii_lowercase
    upercaseLetters = string.ascii_uppercase
    numbers = "012346789"
    characters = lowercaseLetters + upercaseLetters + numbers
    chain = ""
    for _ in range(length):
        chain += random.SystemRandom().choice(characters)
    return chain

def code_order():
    length = 24
    lowercaseLetters = string.ascii_lowercase
    upercaseLetters = string.ascii_uppercase
    numbers = "012346789"
    characters = lowercaseLetters  + upercaseLetters + numbers
    chain = ""
    for _ in range(length):
        chain += random.SystemRandom().choice(characters)
    return chain

def date_document():
    now = datetime.datetime.now()
    date_now = now.strftime("%Y-%m-%d")
    return date_now

def datetime_document():
    now = datetime.datetime.now()
    date_now = now.strftime("%m/%d/%Y-%H:%M:%S")
    return date_now

def url_category(data):
    chain = str(data)
    chain1 = chain.lower()
    chain2 = chain1.replace("á", "a").replace("é", "e").replace("í", "i").replace("ú", "u").replace("ó", "o")
    chain3 = chain2.replace(" ", "-")
    chainf = chain3.replace("-y-", "-&-")
    return chainf

def total_array(array,value):
    m = 0
    x = value
    for data in array:
        n = data[x]
        m = m + n
    total = m
    return total