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

    def getAdminURL(self):
        return(self.url + '/administration')

    def getClassURL(self):
        return(self.getAdminURL() + '/stufe')

    def getPersonsURL(self):
        return(self.getClassURL() + '/personen')

    def getAddPersonURL(self):
        return(self.getPersonsURL() + '/hinzufuegen')

    def getInvitationCodeURL(self):
        return(self.getPersonsURL() + '/einladen')

    def getDeletePersonURL(self):
        return(self.getPersonsURL() + '/loeschen')

    def getStudentsListURL(self):
        return(self.getClassURL() + '/schuelerliste')

    def getTeachersListURL(self):
        return(self.getClassURL() + '/lehrerliste')
