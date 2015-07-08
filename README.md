# Beispielsammlung AK Geodaten GDI-DE 

* Beispiele für Handlungsempfehlung Darstellungsdienste [1]
* Beispiele für Handlungsempfehlung Downloaddienste [2]


[![Build Status](https://travis-ci.org/JuergenWeichand/ak-geodienste.svg)](https://travis-ci.org/JuergenWeichand/ak-geodienste)

## Automatisierte Tests

Bei **jeder** Änderung im Repositorium werden folgende Tests über travisci.org automatisiert durchgeführt.

### 1. Wohlgeformtheit der XML-Dateien
Alle XML-Dateien im Repositorium müssen **wohlgeformt** sein.  Die Überprüfung erfolgt über das Testskript `python/test-xml-wellformed.py`.

### 2. Validität der XML-Dateien 
Alle XML-Dateien im Repositorium müssen **valide** sein. Die Validierung erfolgt gegen die unter `schemaLocation` eingetragenen Schemata. Die Überprüfung erfolgt über das Testskript `python/test-xml-validate.py`.

### 3. GDI-DE Testsuite
Alle im Repositorium vorhandenen ISO19139-**Metadaten** werden automatisch mit der Testsuite der GDI-DE [3] überprüft. Die Überprüfung erfolgt über das Testskript `python/test-testsuite.py`.
Hierbei sind folgende Testklassen zu absolvieren:

* Metadaten | Metadata: ISO and GDI-DE
* Metadaten | Metadata: INSPIRE

Nur `Fehler` führen zu einem fehlerhaften Build-Prozess.

## Links

[1] http://www.geoportal.de/SharedDocs/Downloads/DE/GDI-DE/Handlungsempfehlungen_INSPIRE_Darstellungsdienste.pdf

[2] http://www.geoportal.de/SharedDocs/Downloads/DE/GDI-DE/Handlungsempfehlungen_Inspire_Downloadservices1_1.pdf

[3] http://testsuite.gdi-de.org/gdi/
