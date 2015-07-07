#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Jürgen Weichand'
__version__ = '1.0.0'

from lxml import etree
import os

basedir = '../'

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
                        print 'Validiere ' + xmlfilename + ' gegen ' + etree.tostring(xsddoc)
                        xsd = etree.XMLSchema(etree.XML(etree.tostring(xsddoc)))
                        xsd.assertValid(xmldoc)
                    except etree.DocumentInvalid as e:
                        print(e)
                        exit(1)



print 'Alle XML-Dateien sind valide!'
exit(0)