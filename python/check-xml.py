#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Jürgen Weichand'
__version__ = '1.0.0'

from lxml import etree
import os

for dirpath, dirnames, files in os.walk('../'):
    for name in files:
        if name.lower().endswith('.xml'):
            xmlfilename = (os.path.join(dirpath, name))
            with open(xmlfilename) as xmlfile:
                try:
                    print 'Prüfe ' + xmlfilename
                    doc = etree.parse(xmlfile)
                except etree.XMLSyntaxError as e:
                    msg = xmlfilename + ' : ' + e.message
                    print(msg)
                    exit(1)

print 'Alle XML-Dateien sind wohlgeformt!'
exit(0)