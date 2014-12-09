#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from geventhttpclient import HTTPClient, URL
from flask import Flask, request, redirect, abort

import settings

app = Flask(__name__)

def get_client_addr():
    if not request.headers.getlist("X-Real-IP"):
        ip = request.remote_addr
    else:
        ip = request.headers.getlist("X-Real-IP")[0]
    return ip

def check_recaptcha(secret, resp, ip):
    try:
        url = URL('https://www.google.com/recaptcha/api/siteverify?secret=%s&response=%s&ip=%s' % (secret, resp, ip))
        http = HTTPClient.from_url(url)
        response = http.get(url.request_uri)
        if response.status_code == 200:
            raw_res = response.read()
            res = json.loads(raw_res)
            if res.get('success'):
                return True
    except:
        pass
    return False

@app.route('/', methods=['POST'])
def handler():
    domain = request.headers.get('Testcookie-Domain', '')
    nexturl = request.headers.get('Testcookie-Nexturl', '/')
    cookie_name = request.headers.get('Testcookie-Name')
    cookie_val = request.headers.get('Testcookie-Value')
    secret = settings.RE_SECRETS.get(domaiin)
    if not cookie_name or not cookie_val or not secret:
        abort(500)
    ip = get_client_addr()
    if check_recaptcha(secret, request.form['g-recaptcha-response'], ip):
        resp = redirect(nexturl)
        resp.set_cookie(cookie_name, cookie_val)
        return resp
    return redirect(nexturl)

if __name__ == '__main__':
    import logging

    logging.basicConfig(level=logging.DEBUG)

    app.debug = True

    app.run('localhost', 10101)
