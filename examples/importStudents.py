#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#

import csv
import os

from abiapppy.ExamplesBase import ExamplesBase

example = ExamplesBase('Google Contacts Students Importer')
example.addArgument('csvfile')
example.addArgument('--execute')
con = example.getAbiapp()
path = os.path.abspath(os.path.join(os.getcwd(), example.csvfile))

if not example.execute:
    print("Please set --execute! This is just a test run!")
with open(path) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row['Custom Field 1 - Value'] == 'M':
            sex = 'male'
        else:
            sex = 'female'
        print('Adding', ' '.join([row['Given Name'], row['Additional Name']]),
              row['Family Name'], 'with sex', sex, 'as student.')
        if example.execute:
            con.addStudent(' '.join(
                [row['Given Name'], row['Additional Name']]), row['Family Name'], sex, 'student')
