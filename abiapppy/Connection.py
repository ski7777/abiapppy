#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#

from bs4 import BeautifulSoup
from .Session import Session
from .URL import URL

class Connection:

    def __init__(self, url, email, password, verify=True):
        self.url = URL(url)
        self.session = Session()

        @self.session.addCallAfter(self)
        def getToken(self, req):
            try:
                self.csrfmiddlewaretoken = BeautifulSoup(
                    req.text, features='lxml').find('input').get('value')
            except AttributeError:
                pass

        @self.session.addCallBefore(self)
        def addToken(self, args, kwargs):
            if 'data' in kwargs:
                kwargs['data']['csrfmiddlewaretoken'] = \
                    self.csrfmiddlewaretoken
            return args, kwargs

        self.session.verify = verify
        self.csrfmiddlewaretoken = ''
        self.loadLoginPage()
        self.login(email, password)

    def loadLoginPage(self):
        self.session.get(self.url.getLoginURL())

    def login(self, email, password):
        payload = {
            'email': email,
            'password': password
        }
        req = self.session.post(self.url.getLoginURL(), data=payload)
        if req.status_code != 200:
            raise ValueError
        if len(req.history) > 0:
            if req.history[0].status_code == 302:
                return
        raise ValueError

    def logout(self):
        self.session.get(self.url.getLogoutURL())

