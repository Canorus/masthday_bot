#!/usr/bin/python3

import json
import requests
import datetime
import re
from random import randint
import os
from pytz import timezone

mode = 0
base = os.path.dirname(os.path.abspath(__file__)) + '/'
with open(base+'cred.json') as f:
    cred = json.load(f)

acc = cred[0][1]['cred']['access_token']
head = {'Authorization':'Bearer '+acc}
time_format = '%Y-%m-%dT%H:%M:%S'
instance_address = 'https://twingyeo.kr'

# connect to home timeline
uri_user = instance_address+'/api/v1/streaming/user'
r_user = requests.get(uri_user, headers=head, stream=True)
print('connected..')

def mention_to(content, reply_to_id):
    mention = dict()
    mention['content'] = content
    mention['reply_to_id'] = reply_to_id
    mention['visibility'] = 'unlisted'
    requests.post(instance_address+'/api/v1/statuses',headers=head,data=mention)

for l in r_user.iter_lines():
    dec = l.decode('utf-8')
    if dec == 'event: notification':
        mode = 1
    elif dec =='event: update':
        mode = 0
    elif dec == ':thump':
        mode = 0
    if mode:
        try:
            newdec = json.loads(dec.replace('data: ',''))
            if newdec['account']['bot']:
                raise
            try:
                type = newdec['type']
            except:
                pass
            if type == 'mention':
                reply_to_id = newdec['status']['id']
                reply_to_account = newdec['account']['acct']
                print(newdec)
                if re.search('((파인애플)|(아나나스)).*(입니까)?',newdec['status']['content']) is not None:
                   status = '아나나스입니다'
                elif re.search('살아는?.?[있|계]', newdec['status']['content']) is not None:
                    n = datetime.datetime.now(timezone('Asia/Seoul'))
                    status = '현재 대한민국 서울시는 '+str(n.hour)+'시 '+str(n.minute)+'분 '+str(n.second)+'초 이며 생일봇은 살아있습니다.'
                else:
                    status = '죄송합니다. 아직 제가 이해할 수 없는 질문이에요.'
                    if randint(1,100) %3 == 0:
                        status += '\n하지만 소고기는 자유 소프트웨어가 아니랍니다!'
                    if randint(1,100) % 19 == 1:
                        status = '내가 알아들을 수 있는 것만 묻습니다 휴먼'
                status = '@'+reply_to_account+' '+status
                hd = dict()
                hd['status'] = status
                hd['in_reply_to_id'] = reply_to_id
                hd['visibility'] = 'unlisted'
                r = requests.post(instance_address+'/api/v1/statuses',headers=head,data=hd)
            elif type == 'follow':
                new_follow = newdec['account']['id']
                print('new follower: ' + new_follow)
                t = requests.post(instance_address + '/api/v1/accounts/'+new_follow+'/follow',headers=head)
                print(t.content.decode('utf-8'))
        except:
            print('something\'s wrong')
            print(dec)
