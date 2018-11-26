#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#


class URL:
    def __init__(self, url):
        self.url = url

    def getLoginURL(self):
        return(self.url + '/login')

    def getLogoutURL(self):
        return(self.url + '/logout')

