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

    def loadLoginPage(self):
        self.session.get(self.url.getLoginURL())
