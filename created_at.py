#!/usr/bin/env python3

import json
import requests
import datetime
import re
from random import randint

mode = 0

base = '/volume1/homes/canor/scripts/birthday_bot/'
with open(base+'cred.json') as f:
    cred = json.load(f)

acc = cred[0][1]['cred']['access_token']
head = {'Authorization': 'Bearer ' + acc}  # Authorization
prev = ''  # for renewing data everday
congs = []  # already congratulated
time_format = '%Y-%m-%dT%H:%M:%S'  # time format declared for reuse
instance_address = 'https://twingyeo.kr'

# connect to home timeline
uri_user = instance_address+'/api/v1/streaming/user'
r_user = requests.get(uri_user, headers=head, stream=True)
print('connected..')
for l in r_user.iter_lines():
    dec = l.decode('utf-8')
    if dec == 'event: notification':
        mode = 1
    elif dec == 'event: update':
        mode = 0
    elif dec == ':thump':
        mode = 0
    if mode:  # event: notification
        try:
            newdec = json.loads(dec.replace('data: ', ''))
            if newdec['account']['bot']:
                raise
            try:
                type = newdec['type']
            except:
                pass
            if type == 'mention':
                reply_to_id = newdec['status']['id']
                if newdec['account']['display_name']:
                    username = newdec['account']['display_name']
                else:
                    username = newdec['account']['username']
                reply_to_account = newdec['account']['acct']
                # if has keyword 계정 + 만들 / 생성
                if re.search('계정.*((만들)|(만든)|(생성))', newdec['status']['content']) is not None:
                    # reply
                    created_at_server = newdec['account']['created_at'][:-5]
                    c = datetime.datetime.strptime(created_at_server, time_format)
                    status = username+' 님의 계정은 세계표준시각 '+str(c.year)+'년 '+str(c.month)+'월 '+str(c.day)+'일 '+str(c.hour)+'시 '+str(c.minute)+'분 '+str(c.second)+'초에 생성되었어요.'
                else:
                    status = '죄송합니다. 아직 제가 이해할 수 없는 질문이에요.'
                    if randint(1, 100) % 3 == 0:
                        status += '\n하지만 소고기는 자유 소프트웨어가 아니랍니다!'
                status += ' @'+reply_to_account
                hd = dict()
                hd['status'] = status
                hd['in_reply_to_id'] = reply_to_id
                hd['visibility'] = 'unlisted'
                t = requests.post(instance_address+'/api/v1/statuses', headers=head, data=hd)
            elif type == 'follow':
                # follow back
                pass
        except:
            print('exception occured: ')
            #print(dec)
