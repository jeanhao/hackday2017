#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Crypto.Cipher import AES
import base64
PADDING = '\0'
key = '515d541e91fc1876'
iv = '7af85d0837e2a7d4'

def aes_encrypt(source):
    pad_it = lambda s: s+(16 - len(s)%16)*PADDING  
    generator = AES.new(key, AES.MODE_CBC, iv)
    crypt = generator.encrypt(pad_it(source))   
    return base64.b64encode(crypt)

def aes_decrypt(crypt):
    generator = AES.new(key, AES.MODE_CBC, iv)
    recovery = generator.decrypt(base64.b64decode(crypt))
    return recovery.rstrip(PADDING)

def match(source,crypt):
    return source == aes_decrypt(crypt)
