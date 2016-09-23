import os
import urllib.parse
import urllib.request
import json
import xml.etree.ElementTree as ET
    
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
        # generate xml request
        data = ET.Element('ReqC')
        data.set('ver', '1.1')
        data.set('prod', 'String')
        data.set('lang', 'DE')
        streq = ET.SubElement(data,'STBReq', {'boardType': 'DEP'})
        time = ET.SubElement(streq,'Time')
        time.tail = "Bla"
        data = ET.tostring(data, encoding="iso-8859-1")
        print(data)
        
        return False

    


    def __fetchBifyForStreetAndNumber(self,street,number,addition=''):
        street = urllib.parse.quote(street,encoding="ISO-8859-1")
        number = urllib.parse.quote(number,encoding="ISO-8859-1")
        if addition != '':
            addition = urllib.parse.quote(addition,encoding="ISO-8859-1")
            url = self.SERVERPATH + "?strasse={}&hausnummer={}&zusatz={}".format(street,number,addition)
        else:
            url = self.SERVERPATH + "?strasse={}&hausnummer={}".format(street,number)
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            content = response.read()
        content = content.decode("ISO-8859-1")
        content = content.replace("<nobr><br>","</nobr>")#Hack for parsing siblings
