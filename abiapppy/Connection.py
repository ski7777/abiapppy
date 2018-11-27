#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#

from bs4 import BeautifulSoup

from .Session import Session
from .URL import URL

genders = {
    'male': 'm',
    'female': 'f'
}
rawgenders = dict([(v, k) for k, v in genders.items()])
permissions = {
    'blocked': '0',
    'student': 'U',
    'editor': 'E',
    'admin': 'A'
}
rawpermissions = dict([(v, k) for k, v in permissions.items()])


class Connection:

    def __init__(self, url, email, password, verify=True):
        # initialize URL
        self.url = URL(url)
        # initialize Session
        self.session = Session()
        # set SSL verification
        self.session.verify = verify
        # set empty csrfmiddlewaretoken
        self.csrfmiddlewaretoken = ''
        # define call to extract csrfmiddlewaretoken

        @self.session.addCallAfter(self)
        def getToken(self, req):
            try:
                # get token
                self.csrfmiddlewaretoken = BeautifulSoup(
                    req.text, features='lxml').find(
                    'input', {'name': 'csrfmiddlewaretoken'}).get('value')
            except AttributeError:
                # ignore errors
                pass

        # define call to add csrfmiddlewaretoken and ajax=1 to every request
        @self.session.addCallBefore(self)
        def prepareData(self, args, kwargs):
            # add only if data in request
            if 'data' in kwargs:
                if isinstance(kwargs['data'], dict):
                    kwargs['data']['csrfmiddlewaretoken'] = self.csrfmiddlewaretoken
                    kwargs['data']['ajax'] = '1'
            # return new arguments
            return args, kwargs

        # start login procedure
        self.loadLoginPage()
        self.login(email, password)

    def loadLoginPage(self):
        self.session.get(self.url.getLoginURL())

    def login(self, email, password):
        # build login data
        payload = {
            'email': email,
            'password': password
        }
        # try to login
        req = self.session.post(self.url.getLoginURL(), data=payload)
        # expected status code is 200 with one redirect (302)
        # if something goes wrong raise ValueError
        if req.status_code == 200 and len(req.history) == 1:
            if req.history[0].status_code == 302:
                return
        raise ValueError

    def logout(self):
        self.session.get(self.url.getLogoutURL())

    def addStudent(self, firstname, lastname, sex, permission):
        # generate data
        payload = {
            'firstname': firstname,
            'lastname': lastname,
            'sex': genders[sex],
            'role': permissions[permission],
            'persontype': 'S'
        }
        # execute it!
        self.addPerson(payload)

    def addPerson(self, payload):
        # add person (student/teacher)
        self.session.post(self.url.getAddPersonURL(), data=payload)

    def deletePerson(self, pid):
        # generate data
        payload = {
            'id': pid
        }
        # execute it!
        self.session.post(self.url.getDeletePersonURL(), data=payload)

    # all the three are the same
    deleteStudent = deleteTeacher = deletePerson
