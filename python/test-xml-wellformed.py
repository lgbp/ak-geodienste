#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Jürgen Weichand'
__version__ = '1.0.0'

from lxml import etree
import os

has_exception = False

for dirpath, dirnames, files in os.walk('../'):
    for name in files:
        if name.lower().endswith('.xml'):
            xmlfilename = (os.path.join(dirpath, name))
            with open(xmlfilename) as xmlfile:
                try:
                    print 'Prüfe Wohlgeformtheit ' + xmlfilename
                    doc = etree.parse(xmlfile)
                    print 'Okay!\n'
                except etree.XMLSyntaxError as e:
                    has_exception = True
                    msg = xmlfilename + ' : ' + e.message
                    print(msg)
                    print '\n'

if has_exception:
    exit(1)