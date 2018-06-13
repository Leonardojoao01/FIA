#!/usr/bin/env python
# -*- coding: utf-8 -*-

file = open('log4.txt', 'r').read().split('\n')

aux = 0
date = ""

for line in file :
    if aux != 3:
        #print("Entrou")
        date = date + line + " "
        aux +=1
    if aux >2:
        #print("ELSE")
        print(date)
        date = ""
        aux = 0