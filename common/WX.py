import requests, json
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import base64
import json
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import algorithms


def get_token1():
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={0}&secret={1}'.format('wxd588bd61d89043bf', 'cf0d1d7f520ef877cbfbe60beb1e06c7')
    res = requests.get(url)
    try:
        access_token = res.json()['access_token']
    except:
        access_token = False
    return access_token


def applyQD(access_token, count, name):
    url = 'https://api.weixin.qq.com/intp/marketcode/applycode?access_token={}'.format(access_token)
    data = {'code_count': count, 'isv_application_id': name}
    res = requests.post(url, data=json.dumps(data))
    try:
        res = res.json()
    except:
        res = False
    return res



def checkQD(access_token, apply_id, name):
    url = 'https://api.weixin.qq.com/intp/marketcode/applycodequery?access_token={}'.format(access_token)
    data = {'application_id': apply_id, 'isv_application_id': name}
    res = requests.post(url, data=json.dumps(data))
    try:
        res = res.json()
    except:
        res = False
    return res

def downloadQD(access_token, apply_id, code_start, code_end):
    url = 'https://api.weixin.qq.com/intp/marketcode/applycodedownload?access_token={}'.format(access_token)
    data = {'application_id': apply_id, 'code_start': code_start, 'code_end':code_end}
    res = requests.post(url, data=json.dumps(data))
    try:
        res = res.json()
    except:
        res = False
    return res

def decrypt(encryptedData, iv, sessionKey):
    encryptedData = base64.b64decode(encryptedData)
    cipher = AES.new(sessionKey, AES.MODE_CBC, iv)
    d = cipher.decrypt(encryptedData)
    # unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    return d

# d = decrypt(res, 'mh2kzWD4hjDwVW7S'.encode('utf-8'), 'mh2kzWD4hjDwVW7S'.encode('utf-8'))

file_path = '/home/ly/jwtserver/test.txt'