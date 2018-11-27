#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#

from abiapppy.ExamplesBase import ExamplesBase
from tabulate import tabulate

example = ExamplesBase('Invitation Code Table')
con = example.getAbiapp()

students = con.getStudents()
tabledata = []
for s in students:
    if s['access'] == 'invited':
        tabledata.append(
            [s['id'], s['firstname'], s['lastname'], con.getInvitationCode(s['id'])])

print(tabulate(tabledata, headers=[
      'ID', 'Firstname', 'Lastname', 'Invitation Code']))
