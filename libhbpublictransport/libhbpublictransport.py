import os
import urllib.parse
import urllib.request
import json
import xml.etree.ElementTree as ET
import datetime as DT
    
class VBN(object):
    SERVERPATH="https://fahrplaner.vbn.de/hafas/mgate.exe/dl"

    def getStationId(self, name):
        # generate xml request
        data = ET.Element('ReqC')
        data.set('ver', '1.1')
        data.set('prod', 'String')
        data.set('lang', 'DE')
        lvreq = ET.SubElement(data,'LocValReq', {'id': '001',
                                                'maxNr': '20',
                                                'sMode': '1'})
        ET.SubElement(lvreq,'ReqLoc', {'type': 'ST',
                                        'match': name})
        data = ET.tostring(data, encoding="iso-8859-1")
        # send request
        req = urllib.request.Request(self.SERVERPATH, data)
        with urllib.request.urlopen(req) as response:
            content = response.read()
        # parse result
        content = ET.fromstring(content)
        return str(content[0][0].attrib['externalId'])
    
    def getScheduleForStation(self, stationid):
        # get todays date and time
        today = DT.datetime.now()
        # generate xml request
        data = ET.Element('ReqC')
        data.set('ver', '1.1')
        data.set('prod', 'String')
        data.set('lang', 'DE')
        streq = ET.SubElement(data,'STBReq', {'boardType': 'DEP'})
        time = ET.SubElement(streq,'Time')
        time.text = today.strftime("%H:%M:%S")
        ET.SubElement(streq,'Today')
        ET.SubElement(streq,'TableStation', {'externalId': stationid})
        pf = ET.SubElement(streq,'ProductFilter')
        pf.text = "1111111111111111"
        data = ET.tostring(data, encoding="iso-8859-1")
        # send request
        req = urllib.request.Request(self.SERVERPATH, data)
        with urllib.request.urlopen(req) as response:
            content = response.read()
        # parse result
        content = ET.fromstring(content)
        for entry in content.findall('./STBResIPhone/Entries/StationBoardEntry'):
            print(entry.attrib)
        return False

