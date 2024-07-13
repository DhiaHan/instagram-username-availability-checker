import os
import re
import random
import string
import requests
from datetime import datetime

baseLink = 'https://www.instagram.com/'
requestSubLink = 'api/v1/web/accounts/web_create_ajax/attempt/'
requestLink = os.path.join(baseLink, requestSubLink)  

def extractCsrftoken(session):
    requestUrl = 'https://www.instagram.com/'
    session.headers.update({
        'authority':'www.instagram.com',
        'method':'GET',
        'path':'/',
        'scheme':'https',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding':'gzip, deflate, br, zstd',
        'Accept-Language':'fr',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
    })
    response = session.get(requestUrl)
    pattern = r'csrf_token":"([^"]+)"'
    csrftoken = re.search(pattern, response.text).group(1)
    return csrftoken

def checkUsernameAvailability(session, username):
    requestUrl = 'https://www.instagram.com/api/v1/web/accounts/web_create_ajax/attempt/'
    session.headers.update({
        'authority':'www.instagram.com',
        'method':'POST',
        'path':'/api/v1/web/accounts/web_create_ajax/attempt/',
        'scheme':'https',
        'Accept':'*/*',
        'Accept-Encoding':'gzip, deflate, br, zstd',
        'Accept-Language':'fr',
        'Content-Type':'application/x-www-form-urlencoded',
        'Origin':'https://www.instagram.com',
        'Priority':'u=1, i',
        'Referer':'https://www.instagram.com/accounts/emailsignup/',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
        'X-Csrftoken': csrftoken,
        'X-Requested-With':'XMLHttpRequest'
    })
    randomEmail = ''.join(random.choices(string.ascii_lowercase, k=15)) + '@gmail.com'
    randomPassword = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase, k=16))
    randomFirstName = ''.join(random.choices(string.ascii_lowercase, k=8)) + ' ' + ''.join(random.choices(string.ascii_lowercase, k=5))
    requestPayload = {
        'enc_password': '#PWD_INSTAGRAM_BROWSER:0:{}:{}'.format(int(datetime.now().timestamp()), randomPassword),
        'email': randomEmail,
        'first_name': randomFirstName,
        'username': username,
        'opt_into_one_tap': 'false'
    }
    response = session.post(requestUrl, data=requestPayload)
    return response.json()

session = requests.session()
csrftoken = extractCsrftoken(session)
username = ''
while username != '-1':
    username = str(input("Username: "))
    data = checkUsernameAvailability(session, username)
    if 'errors' in data.keys():
        print(data['errors']['username'][-1]['code'].replace('_', ' '))
        continue
    else:
        print('Username is not taken.')
### WORKS PERFECTLY
