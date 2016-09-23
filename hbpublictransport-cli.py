#!/usr/bin/env python
# -*- coding: utf-8 -*-
from libhbpublictransport.libhbpublictransport import VBN
import getopt
import sys



def usage():
    text = """usage:
        -S	--station	station name
        -h	--help		help"""
    print(text)

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "S:h", ["station=","help"])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    station = ""
    for o, a in opts:
        if o in ("-S", "--station"):
            station = a
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        else:
            assert False, "unhandled option"

    v = VBN()
    print(v.getScheduleForStation(v.getStationId(station)))

if __name__ == "__main__":
    main()
