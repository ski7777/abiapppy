#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#

import argparse

from .Connection import Connection


class ExamplesBase:
    def __init__(self, desc=None):
        self.parser = argparse.ArgumentParser(description='Abiapppy example')
        self.parser.add_argument(
            'url', help='aiapp.net URL')
        self.parser.add_argument(
            'mail', help='User E-Mail address')
        self.parser.add_argument(
            'password', help='User password')
        if desc is not None:
            self.setDescription(desc)
        self.addArgument = self.parser.add_argument

    def parse(self):
        return(self.parser.parse_args())

    def getAbiapp(self):
        args = self.parse()
        return(Connection(args.url, args.mail, args.password))

    def setDescription(self, name):
        self.parser.description = name

    def __getattr__(self, name):
        return(getattr(self.parse(), name))
