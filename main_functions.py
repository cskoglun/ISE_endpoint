#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""ISE_endpoints Console Script.

Copyright (c) 2019 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.

"""

import sys

__author__ = "Christina Skoglund"
__email__ = "cskoglun@cisco.com"
__version__ = "1"
__copyright__ = "Copyright (c) 2019 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import http.client
import base64
import ssl
import json
from pprint import pprint
import argparse

HOST = "change"
USER = "change"
PASSWORD = "change"

# Encode HTTP Basic authentication
ise_user_pwd = str.encode(':'.join((USER, PASSWORD)))
basic_auth_encoded = bytes.decode(base64.b64encode(ise_user_pwd))

# Define headers
headers = {
    'Content-Type': "application/json",
    'Accept': "application/json",
    'ERS-Media-Type': "identity.endpoint.1.2",
    'Authorization': "Basic {}".format(basic_auth_encoded),
    'Cache-Control': "no-cache"
    }

def ISE_connect(CRUD,url,payload):
    conn = http.client.HTTPSConnection(HOST, port=9060, context = ssl._create_unverified_context())
    conn.request(CRUD, url, headers=headers, body=payload)
    res = conn.getresponse()
    data_bytes = res.read()
    if res.status == 200:
        decoded_data = data_bytes.decode()
        json_data = json.loads(decoded_data)
        print("Operation success")
        return json_data
    elif res.status == 201:
        print("POST operation success")
    elif res.status == 204:
        print("DELETE operation success.")
    else: 
        print("\n Oups... Error code: ", res.status)

def get_endpoints():
    CRUD = "GET"
    url = "/ers/config/endpoint"
    payload = None
    json_data = ISE_connect(CRUD,url,payload)
    return json_data

def create_endpoint(mac_address,name,description):    
    payload_dict = {
        "ERSEndPoint" : {
            "name" : "{}".format(name),
            "description" : "{}".format(description),
            "mac" : "{}".format(mac_address),
            "staticProfileAssignment" : False,
            "staticGroupAssignment" : True,
            "portalUser" : "portalUser",
            "customAttributes" : {
                "customAttributes" : {
                    "key1" : "value1",
                    "key2" : "value2"
                    }
                }
            }
        }
    payload = json.dumps(payload_dict)
    CRUD = "POST"
    url = "/ers/config/endpoint"
    create = ISE_connect(CRUD,url,payload)

def get_endpoint_id():
    data = get_endpoints()
    EP_ID = None
    for i in range(0,len(data['SearchResult']['resources'])):
        if data['SearchResult']['resources'][i]['name'] == mac:
            EP_ID = data['SearchResult']['resources'][i]['id']
    return EP_ID

def delete_endpoint(mac):
    data = get_endpoints()
    EP_ID = None
    for i in range(0,len(data['SearchResult']['resources'])):
        if data['SearchResult']['resources'][i]['name'] == mac:
            EP_ID = data['SearchResult']['resources'][i]['id']  

    if EP_ID == None:
        print("\n OBS!! Seems like endpoint does not exist \n")
    else:
        CRUD = "DELETE"
        url = "/ers/config/endpoint/{}".format(EP_ID)
        payload = None
        delete = ISE_connect(CRUD,url,payload)

def update_endpoint(endpoint_id,mac,name,description):
    payload = {
        "ERSEndPoint" : {
            "id" : "{}".format(endpoint_id),
            "name" : "{}".format(name),
            "description" : "{}".format(description),
            "mac" : "{}".format(mac),
            "profileId" : "test",
            "staticProfileAssignment" : False,
            "staticGroupAssignment" : True,
            "portalUser" : "portalUser",
            "customAttributes" : {
                "customAttributes" : {
                    "key1" : "value1",
                    "key2" : "value2"
                    }
                }   
            }
        }
    data_payload = json.dumps(payload)
    try:
        CRUD = "PUT"
        url = "/ers/config/endpoint/{}".format(endpoint_id)
        put_operation = ISE_connect(CRUD,url,data_payload)
        print(put_operation)
    except:
        print("Error with conn request")

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('--create_EP',
                            help='Create new enpoint in ISE')
    parser.add_argument('--update_EP',
                            help='Update endpoint in ISE')                        
    parser.add_argument('--delete_EP',
                            help='Update endpoint in ISE') 

    if len(sys.argv[1:]) == 0:
            parser.print_help()
            parser.exit()

    args = parser.parse_args()

    if args.create_EP:
        mac = str(input("MAC address: "))
        name = str(input("Name of EP: "))
        description = str(input("Description of EP: "))
        create_endpoint(mac,name,description)
        print("\n The new endpoint ID is: \n",get_endpoint_id())

    if args.update_EP:
        mac = str(input("MAC address: "))
        name = str(input("New name of EP: "))
        description = str(input("New description of EP: "))
        update_endpoint(get_endpoint_id(),mac,name,description)

    if args.delete_EP:
        mac = str(input("(OBS:DELETE) MAC address: "))
        answer = str(input("Are you SURE you want to delete EP with MAC: {} [yes/no]".format(mac)))
        if answer == "yes":
            delete_endpoint(mac)
        else:
            print("\nDELETE operation aborted\n")



