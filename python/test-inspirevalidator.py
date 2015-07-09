# -*- coding: UTF-8 -*-
__author__ = 'Jürgen Weichand'
__version__ = '1.0.0'

'''
Python-Skript für automatisierte Tests über den INSPIRE Geoportal Metadata Validator
http://inspire-geoportal.ec.europa.eu/validator2/
'''

import requests
import os
from lxml import etree

inspire_validator_url = 'http://inspire-geoportal.ec.europa.eu/GeoportalProxyWebServices/resources/INSPIREResourceTester'

basedir = '../ak-geodienste/'
baseurl = 'https://raw.githubusercontent.com/JuergenWeichand/ak-geodienste/master/'

has_exception = False

for dirpath, dirnames, files in os.walk(basedir):
    for name in files:
        if ('.xml' in name):
            xmlfilename = (os.path.join(dirpath, name))
            url = baseurl + xmlfilename.replace(basedir, '')
            response = requests.get(url)

            # Überprüfung Metadaten mit dem InspireValidator
            if 'MD_Metadata' in response.text:

                print 'Prüfe mit InspireValidator ' + url
                response = requests.post(inspire_validator_url, timeout=240, headers={"Accept":"application/xml"}, files=dict(resourceRepresentation=url))
                xmlstring = response.text.replace('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>', '') #Hack
                xmldoc = etree.XML(xmlstring)
                exceptions = xmldoc.xpath('//ns2:GeoportalExceptionMessage/ns2:Message', namespaces={'ns2':'http://inspire.ec.europa.eu/schemas/geoportal/1.0'})
                for exception in exceptions:
                    has_exception = True
                    print exception.text
                # print etree.tostring(xmldoc, pretty_print=True)
                if len(exception) == 0:
                    print 'Okay!\n'
                else:
                    print '\n'

if has_exception:
    # exit(1)
    exit(0) # Nur zur Information!
