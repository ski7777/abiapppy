#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#

import json

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

    def getStudents(self):
        return(self.parsePersonsList(self.url.getStudentsListURL()))

    def getTeachers(self):
        return(self.parsePersonsList(self.url.getTeachersListURL()))

    def parsePersonsList(self, url):
        persons = []
        # load page
        req = self.session.get(url)
        # load html
        rawdata = BeautifulSoup(req.text, features='lxml')
        # iterate over persons
        for p in rawdata.findAll('div', {'class': 'person'}):
            # get basic data
            person = {
                'id': p.get('data-id'),
                'type': p.get('data-persontype')
            }
            # iterate over some fields (Type one)
            for f in p.findAll('div', {'class': 'edit-group-inline'}):
                # get name of field (Method one)
                n = f.get('data-name')
                # if this fails
                if n is None:
                    # get name of field (Method two)
                    n = f.find(
                        'label').text[::-1].replace(':', '', 1)[::-1].strip()
                # try to find data
                for t in ['a', 'div', 'span']:
                    # check whether this is the invitation status field
                    if 'user' in f['class']:
                        # add data to user
                        n = 'access'
                        if 'invited' in f['class']:
                            person[n] = 'invited'
                        elif 'fb' in f['class']:
                            person[n] = 'facebook'
                        else:
                            person[n] = 'password'
                    # try to get the data and save it
                    try:
                        person[n] = f.find(
                            t, {'class': 'val'}).text.strip()
                    except AttributeError:
                        pass
            # iterate over some fields (Type two)
            for f in p.findAll(lambda tag: tag.name == 'div'
                               and 'data-editable' in tag.attrs):
                # get name and value of field and save it
                person[f.get('name')] = f.text.strip()
            persons.append(person)
        return(persons)

    def getInvitationCode(self, sid):
        # generate data
        payload = {
            'id': sid
        }
        # load json
        data = json.loads(self.session.post(
            self.url.getInvitationCodeURL(), data=payload).text)
        # try to find and return code
        if 'type' in data:
            if data['type'] == 'invite':
                return(data['code'])
        # if not found (due error) raise ValueError
        raise ValueError
