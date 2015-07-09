#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Jürgen Weichand'
__version__ = '1.0.0'

from lxml import etree
import os

basedir = '../'

has_exception = False

for dirpath, dirnames, files in os.walk(basedir):
    for name in files:

        # Überprüfung aller XML-Dateien
        if name.lower().endswith('.xml'):
            xmlfilename = (os.path.join(dirpath, name))

            # XML mit lxml verarbeiten
            with open(xmlfilename) as xmlfile:
                xmldoc = etree.parse(xmlfilename)


                # für lxml alle Schemata (schemaLocations) in einem temporären Schema vereinen (über Import)

                schemaLocation = xmldoc.getroot().get("{http://www.w3.org/2001/XMLSchema-instance}schemaLocation")
                if schemaLocation:
                    locations = schemaLocation.split()
                    xsddoc = etree.Element("schema", attrib={
                            "elementFormDefault": "qualified",
                            "version": "1.0.0",
                        }, nsmap={
                        None: "http://www.w3.org/2001/XMLSchema"
                        }
                    )
                    # ergänze Imports
                    for i in range(0,len(locations)):
                        if not i % 2:
                            etree.SubElement(xsddoc, "import", attrib={
                                "namespace": locations[i],
                                "schemaLocation": locations[i+1]
                                }
                            )

                    # Validierung der XML-Datei gegen das temporäre Schema
                    try:
                        print 'Prüfe Validität ' + xmlfilename + ' gegen:'
                        print etree.tostring(xsddoc,pretty_print=True)
                        xsd = etree.XMLSchema(etree.XML(etree.tostring(xsddoc)))
                        xsd.assertValid(xmldoc)
                        print 'Okay!\n'
                    except etree.DocumentInvalid as e:
                        has_exception = True
                        print(e)
                        print '\n'

if has_exception:
    exit(1)