#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from pymsgbox import prompt
result = prompt(text='My Text', title='My Title', default='Default Text')
print(result)
