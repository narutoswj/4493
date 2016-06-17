# -*- coding: utf-8 -*-
import pyquery
import pymongo
import datetime
import os
import sys

from pyquery import PyQuery as pq
print (pq('http://www.4493.com/xingganmote/index-2.htm')('.clearfix').html())
html = pq('http://www.4493.com/xingganmote/index-2.htm')('.clearfix')('li')
j = 1
for i in html:
    print j
    print pq(i).html()
    j = j + 1