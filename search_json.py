#!/usr/bin/env python3
import sys, json, argparse, argcomplete, re
from pprint import pprint

parser = argparse.ArgumentParser()
parser.add_argument('-ip', dest='ip',  help="guest ip")
parser.add_argument('-mac', dest='mac',  help="guest mac")
parser.add_argument('-esxi', dest='esxi',  help="esxi host")
parser.add_argument('-note', dest='note',  help="note")
parser.add_argument('-name', dest='name',  help="vm name")
parser.add_argument('-path', dest='path',  help="vm storage path")
args = parser.parse_args()
argcomplete.autocomplete(parser)

jsonfile = 'vmware.json'

json_data=open(jsonfile)
jdata = json.load(json_data)

for key, value in jdata.items():
    if args.name is not None and re.match( args.name , key ):
        print ( "vmname: " + key)
        pprint ( value )
    #if args.ip is not None and ( re.match( args.ip+"'", str( value['guest ip'] ) ) or args.ip in value['Note']):
    if args.ip is not None:
        inip = 0 # переменная обозначающая то что мы в цикле нашли нужный ip адрес
        for i in value['guest ip']:
            if re.match( args.ip, i ):
                inip = 1
        if inip != 1: # если ip не найдет пробуем его найти в Note у машины
            if re.findall( args.ip,  str( value['Note'] ) ):
                inip = 1

        if inip == 1:
            print ( "vmname: " + key)
            pprint ( value )

    elif args.mac is not None and ( re.match( args.mac,  str( value['macaddress'] ) ) or args.mac in value['Note'] ):
        print ( "vmname: " + key)
        pprint ( key + value )
    elif args.esxi is not None and re.match( args.esxi,  str( value['esxi'] ) ):
        print ( "vmname: " + key)
        pprint ( value )
    elif args.note is not None and re.findall( args.note,  str( value['Note'] ) ):
        print ( "vmname: " + key)
        pprint ( value )
    elif args.path is not None and re.match( args.path, str( value['path'] ) ):
        print ( "vmname: " + key)
        pprint ( value )

#pprint ( jdata )
json_data.close()
