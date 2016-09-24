import os
import sys
import urllib.parse
import urllib.request
import json
import xml.etree.ElementTree as ET
import datetime as DT
import re
    
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
        try:
            stid = content[0][0].attrib['externalId']
        except KeyError:
            print("Keine Station gefunden. Sry :(")
            sys.exit(-1)
        return stid
        
    
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
        data = ET.tostring(data, encoding="iso-8859-1")
        # send request
        req = urllib.request.Request(self.SERVERPATH, data)
        with urllib.request.urlopen(req) as response:
            content = response.read()
        # parse result
        content = ET.fromstring(content)
        exportdata = {}
        entries = []
        for entry in content.findall('./STBResIPhone/Entries/StationBoardEntry'):
            scheduled = self.__HafasTimeToDatetime(entry.attrib['scheduledTime']).strftime("%Y-%m-%d %H:%M:%S")
            if 'actualTime' in entry.attrib:
                actual = self.__HafasTimeToDatetime(entry.attrib['actualTime']).strftime("%Y-%m-%d %H:%M:%S")
            else:
                actual = scheduled
            entrydata = {'scheduled': scheduled,
                        'actual': actual,
                        'type': entry.attrib['category'],
                        'number': entry.attrib['number'],
                        'direction': entry.attrib['direction'],
            }
            entries.append(entrydata)
        exportdata = { 'entries': entries,
                        'lastupdate': today.strftime("%d.%m.%Y %H:%M:%S")}
        return json.dumps(exportdata, indent=4, separators=(',', ': '))

    def __HafasTimeToDatetime(self, time):
        p = re.compile('^\d+d')
        m = p.match(time)
        dtoday = DT.date.today()
        days = 0
        if m:
            days = int(m.group().rstrip('d'))
            time = re.sub(p,'',time)
        dtime = DT.datetime.strptime(time, "%H:%M")
        dt = DT.datetime.combine(dtoday, dtime.time())
        dt = dt + DT.timedelta(days=days)
        return dt            
