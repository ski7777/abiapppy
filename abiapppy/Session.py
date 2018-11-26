#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#

import requests


class Session(requests.Session):

    def __init__(self, *args, **kwargs):
        # initialize callBefore/callAfter lists
        self.callBefore = []
        self.callAfter = []
        # initialize Session
        super().__init__(*args, **kwargs)

    def request(self, *args, **kwargs):
        # iterate over callBefores
        for cb, parent in self.callBefore:
            # call function and get the arguments again
            args, kwargs = cb(parent, args, kwargs)
        # make request
        req = requests.Session.request(self, *args, **kwargs)
        # iterate ove callAfters
        for ca, parent in self.callAfter:
            # call function
            ca(parent, req)
        # return request
        return(req)

    def addCallBefore(self, parent):
        # define the true decorator
        def addCallBeforeDecorator(cb):
            # append to callBefore
            self.callBefore.append((cb, parent))
        # return true decorator
        return addCallBeforeDecorator

    def addCallAfter(self, parent):
        # define the true decorator
        def addCallAfterDecorator(ca):
            # append callAfter
            self.callAfter.append((ca, parent))
        # return true decorator
        return addCallAfterDecorator
