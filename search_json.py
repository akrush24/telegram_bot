#!/usr/bin/env python3
import sys, json, argparse, re

from pprint import pprint
from passwd import HomeDir
#HomeDir = '/home/akrush/telegram_bot/'

def search_vm_json( args ):
    argslist = args.split()
    parser = argparse.ArgumentParser( )
    parser.add_argument('-ip', dest='ip',  help="guest ip")
    parser.add_argument('-mac', dest='mac',  help="guest mac")
    parser.add_argument('-esxi', dest='esxi',  help="esxi host")
    parser.add_argument('-status', dest='status',  help="vm power status")
    parser.add_argument('-note', dest='note',  help="note")
    parser.add_argument('-name', dest='name',  help="vm name")
    parser.add_argument('-path', dest='path',  help="vm storage path")
    parser.add_argument('-snap', dest='snap',  help="vm whitch snapshots")
    parser.add_argument('-all', dest='all',  help="full info", action='store_true')
    args = parser.parse_args( argslist )

    jsonfile = HomeDir + 'inventory_json/vmware.json'
    json_data=open(jsonfile)
    jdata = json.load(json_data)
    json_data.close()

    res = {}
    for key, value in jdata.items():
        if args.name is not None and re.match( args.name , value['Name'] ):
            res[key] = value
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
                res[key] = value

        elif args.mac is not None and ( re.match( args.mac,  str( value['macaddress'] ) ) or args.mac in value['Note'] ):
            res[key] = value
        elif args.esxi is not None and args.status is None and re.match( args.esxi,  str( value['esxi'] )):
            res[key] = value
        elif args.esxi is not None and args.status == '1' and re.match( args.esxi,  str( value['esxi'] ) ) and value['Status'] == "poweredOn":
            res[key] = value
        elif args.esxi is not None and args.status == '0' and re.match( args.esxi,  str( value['esxi'] ) ) and value['Status'] == "poweredOff":
            res[key] = value
        elif args.note is not None and re.findall( args.note,  str( value['Note'] ) ):
            res[key] =  value
        elif args.path is not None and re.match( args.path, str( value['path'] ) ):
            res[key] = value
        elif args.snap is not None and len(value['snapshot']) > int(args.snap):
            res[key] = value
    return ( res )

#print (str(search_vm_json('-esxi ars-vm12.srv.local -status 1')))
