# -*- coding: UTF-8 -*-
__author__ = 'Jürgen Weichand'
__version__ = '1.0.0'

'''
Python-Skript für automatisierte Tests über die GDI-DE Testsuite API
Basiert auf: https://wiki.gdi-de.org/download/attachments/78577688/2015-03-02_sven_boehme_testsuite_api_minimal_beispiel.py
'''

from suds.client import Client as SudsClient
import time
import os
import requests


basedir = '../ak-geodienste/'
baseurl = 'https://raw.githubusercontent.com/JuergenWeichand/ak-geodienste/master/'

testmapping = {}
has_failure = False

for dirpath, dirnames, files in os.walk(basedir):
    for name in files:

        # Überprüfung aller XML-Dateien
        if name.lower().endswith('.xml'):
            xmlfilename = (os.path.join(dirpath, name))
            url = baseurl + xmlfilename.replace(basedir, '')

            response = requests.get(url).text
            testklassen = []

            if ('MD_Metadata' in response):
                testklassen = [15, 16]
            #elif ('WMT_MS_Capabilities' in response):
                #testklassen = [18, 20]

            for testklasse in testklassen:

                # Starte Tests
                credentials = {'userName': 'wei_github', 'pass': u'testtest'}

                proxies = {}
                client = SudsClient('http://testsuite.gdi-de.org/gdi/download?id=wsdl', proxy=proxies)

                #getTestClass
                parameter_get_test_class = {'testClassID': testklasse}
                parameter_get_test_class.update(credentials)
                testclass = client.service.getTestClass(**parameter_get_test_class)
                print '[Testklasse ' + testclass.Name + ']\n' + url


                # setTestConfiguration
                parameter_set_test_configuration = {'name': name,
                                                    'description': url,
                                                    'notify': 'NO',
                                                    'url': url,
                                                    'saveReport': 'NO',
                                                    'tk_ID': testklasse,
                                                    'confClassID': '',  # ?
                                                    'sourceType': 'URL'}

                parameter_set_test_configuration.update(credentials)
                test_config_id = client.service.setTestConfiguration(**parameter_set_test_configuration)


                # startTestConfiguration
                parameter_start_test_configuration = {'testConfID': test_config_id}
                parameter_start_test_configuration.update(credentials)
                report_id = client.service.startTestConfiguration(**parameter_start_test_configuration)

                # getTestStatus
                parameter_get_test_status = {'testConfId': test_config_id}
                parameter_get_test_status.update(credentials)

                isrunning = True
                while isrunning:
                    if client.service.getTestStatus(**parameter_get_test_status) != 'Running':
                        isrunning = False
                    else:
                        time.sleep(0.5)

                #getTestReport
                parameter_get_test_report = {'reportID': report_id}
                parameter_get_test_report.update(credentials)
                test_report = client.service.getTestReport(**parameter_get_test_report)
                for k, item in enumerate(test_report.item):

                    # Iteriere über die einzelnen Tests...
                    for l, singleTest in enumerate(item.singleTests):

                        if singleTest.result == 'FAIL':
                            has_failure = True
                            if hasattr(singleTest, 'messages'):
                                print(singleTest.messages)

                if not has_failure:
                    print('Okay!\n')
                else:
                    print('\n')

                #deleteTestConfiguration
                parameter_delete_test_configuration = {'testConfID': test_config_id}
                parameter_delete_test_configuration.update(credentials)
                client.service.deleteTestConfiguration(**parameter_delete_test_configuration)


if has_failure:
    exit (1)
