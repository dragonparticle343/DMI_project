from datetime import datetime
import datetime, string, random

def code_doc(num):
    length = num
    lowercaseLetters = string.ascii_lowercase
    upercaseLetters = string.ascii_uppercase
    numbers = "012346789"
    characters = lowercaseLetters + upercaseLetters + numbers
    chain = ""
    for _ in range(length):
        chain += random.SystemRandom().choice(characters)
    return chain

def datetime_doc():
    now = datetime.datetime.now()
    date_now = now.strftime("%m/%d/%Y-%H:%M:%S")
    return date_now

def date_string(string, start, end):
    time = datetime.datetime.strptime(string, start)
    date = time.strftime(end)
    return date

def total_array(array,value):
    m = 0
    x = value
    for data in array:
        n = data[x]
        m = m + n
    total = m
    return total