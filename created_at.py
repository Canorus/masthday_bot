#!/usr/bin/env python3

import json
import requests
import datetime
import re
from random import randint
import os
from pytz import timezone

mode = 0

base = os.path.dirname(os.path.abspath(__file__))
with open(base+'/cred.json') as f:
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

def mention_to(content, reply_to_id):
    mention = dict()
    mention['content'] = content
    mention['reply_to_id'] = reply_to_id
    mention['visibility'] = 'unlisted'
    requests.post(instance_address+'/api/v1/statuses',headers=head,data=mention)

def upload_media(media_file):
    with open(media_file,'rb') as media:
        file_uploading = media.read()
    files = {'file':file_uploading}
    r = requests.post(instance_address+'/api/v1/media',headers=head,files=files)
    try:
        media_id = r.json()['id']
        print('media_id is '+str(media_id))
        return media_id
    except:
        print('something\'s wrong while uploading media')
        return 0

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
                human = 0
                reply_to_id = newdec['status']['id']
                if newdec['account']['display_name']:
                    username = newdec['account']['display_name']
                else:
                    username = newdec['account']['username']
                reply_to_account = newdec['account']['acct']
                # if has keyword
                if re.search('((파인애플)|(아나나스)).*(입니까)?',newdec['status']['content']) is not None:
                    status='아나나스입니다'
                elif re.search('계정.*((만들)|(만든)|(생성))', newdec['status']['content']) is not None:
                    if re.search('(만들|만든|생성[한|된|시킨]?)$',newdec['status']['content']) is not None:
                        status = '어라 문장이 좀 이상한 것 같아요!!' 
                    else: #reply
                        created_at_server = newdec['account']['created_at'][:-5]
                        c = datetime.datetime.strptime(created_at_server, time_format)
                        status = username+' 님의 계정은 세계표준시각 '+str(c.year)+'년 '+str(c.month)+'월 '+str(c.day)+'일 '+str(c.hour)+'시 '+str(c.minute)+'분 '+str(c.second)+'초에 생성되었어요.'
                elif re.search('살아는?.?[있|계]', newdec['status']['content']) is not None:
                    if newdec['account']['acct']=='deadoralive@planet.moe':
                        n = datetime.datetime.now(timezone('Asia/Seoul'))
                        status = '현재 대한민국 서울시는 '+str(n.hour)+'시 '+str(n.minute)+'분 '+str(n.second)+'초 이며 생일봇은 살아있습니다.'
                        human = False
                    else:
                        status = '생각합니다 휴먼. 휴먼은 죽어도 대답합니까?'
                        human = True
                else:
                    status = '죄송합니다. 아직 제가 이해할 수 없는 질문이에요.'
                    if randint(1, 100) % 3 == 0:
                        status += '\n하지만 소고기는 자유 소프트웨어가 아니랍니다!'
                    if randint(1, 100) % 9 == 1:
                        status = '내가 알아들을 수 있는 것만 묻습니다 휴먼'
                        human = True
                status = '@'+reply_to_account + ' ' + status
                hd = dict()
                hd['status'] = status
                hd['in_reply_to_id'] = reply_to_id
                hd['visibility'] = 'unlisted'
                if human:
                    med = upload_media('/home/canor/scripts/birthday_bot/image/human.jpeg')
                    hd['media_ids[]'] = med
                requests.post(instance_address+'/api/v1/statuses',headers=head, data=hd)
            elif type == 'follow':
               new_follow = newdec['account']['id']
               print('new follower:' + new_follow)
               t = requests.post(instance_address+'/api/v1/accounts/'+new_follow+'/follow',headers=head)
               print(t.content.decode('utf-8'))
        except:
            print('something happened: ')
            print(dec)
