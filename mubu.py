#!/usr/bin/env python3
import json
import re
import sys

import requests

from thebrain import Node, Brainy

headers = {
    'sec-fetch-mode': 'cors',
    'dnt': '1',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'x-requested-with': 'XMLHttpRequest',
    'cookie': 'data_unique_id=5a9abc99-420f-4f87-8904-b7a8d96693ef; reg_entrance=https^%^3A^%^2F^%^2Fmubu.com^%^2Fexplore; _ga=GA1.2.221918959.1573280449; _gid=GA1.2.271604722.1573280449; user_persistence=2b982041-cf40-4926-9091-9a48b822e623; s_v_web_id=fef5683481191d2710eb1c09a159f4b7; csrf_token=ca3bd65c-214e-4a6b-9391-fac4ded3604b; SESSION=Y2Y1Zjg2MDgtNWQ5Ni00OTI3LWE3NzktZjhjYTBkZWI2MTI3; RT=^\\^z=1^&dm=mubu.com^&si=k8ugh5sldm8^&ss=k2s407d6^&sl=2^&tt=0^&obo=2^&r=b8eca20abd57ca9daeacbb6ff0d6a259^&ul=xos2^&hd=xqgq^\\^',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'referer': 'https://mubu.com/doc/explore/25839',
    'authority': 'mubu.com',
    'sec-fetch-site': 'same-origin',
    'origin': 'https://mubu.com',
}

data = {
    'docId': '%s'
}

url = 'https://mubu.com/doc/explore/%s'
docId = re.search(r'var\sdocId\s=\s\'(.+?)\'', requests.get(url % sys.argv[1]).text).group(1)
data['docId'] = docId
response = requests.post('https://mubu.com/api/document/view/get', headers=headers, data=data)
obj = json.loads(response.text)
root = Node(obj['data']['name'])
defs = json.loads(obj['data']['definition'])


def creation(source, target, depth=0):
    if type(source) is list:
        for s in source:
            children = target.children
            children.append(Node())
            creation(s, children[-1], depth + 1)
    else:
        target.name = source['text']
        if 'class="content-link"' in target.name:
            target.links = re.search(r'a.+?href="(.+?)"', target.name).group(1)
            target.name = re.sub(r'<a.+?/a>', '', target.name)

        target.name = target.name.replace('|', '')
        target.name = target.name.replace('&lt;', '')
        target.name = target.name.replace('&gt;', '')
        target.name = target.name.replace('&amp;', '')
        target.name = re.sub(r'<span.+?>', '', target.name)
        target.name = re.sub(r'</span>', '', target.name)
        target.name = re.sub(r'^[0-9\.]+?[^0-9\.]', '', target.name)
        if 'note' in source.keys():
            target.note = source['note']

        target.depth = depth
        if 'children' in source.keys():
            sources = source['children']
            if len(sources) > 0:
                creation(sources, target, depth)


creation(defs['nodes'], root)
Brainy(root).write()
