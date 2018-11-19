#!/usr/bin/env python3

import json
import requests
import csv
import os
import datetime

base = '/volume1/homes/canor/scripts/birthday_bot/'
with open(base+'cred.json') as f:
    cred = json.load(f)

acc = cred[0][1]['cred']['access_token']
head = {'Authorization':'Bearer '+ acc} # Authorization
prev = '' # for renewing data everday 
congs = [] # already congratulated

uri_local = 'https://twingyeo.kr/api/v1/streaming/public/local' # connect to local timeline
r_local = requests.get(uri_local,headers=head,stream=True)
print('connected..')
for l in r_local.iter_lines():
    dec = l.decode('utf-8')
    try:
        #print('dec type: '+str(type(dec)))
        newdec = json.loads(dec.replace('data: ','')) # strip off unnecessary part
        try:
            with open(base+'congratulated.txt') as f:
                for line in f:
                    congs.append(line.replace('\n','')) # bring already congratulated members
        except:
            congs = []
        account = newdec['account']
        if account['created_at'][5:10] == datetime.datetime.today().isoformat()[5:10] and account['username'] not in congs: # same created date but not in congs
            instance = account['url'].split('/')[2] # get instance address
            n = int(datetime.datetime.today().isoformat()[:4]) - int(account['created_at'][:4]) # calculate how many years have passed
            hd = dict()
            if n > 0: # more than a year
                hd['status'] = account['display_name']+' 님이 '+instance+'에 가입하신 지 '+str(n)+' 주 년이 되셨습니다. 축하합니다.'
            elif n == 0: # new member!
                hd['status'] = account['display_name']+' 님이 '+instance+'에 새로 오셨습니다. 환영합니다.'
            hd['visibility'] = 'unlisted' # in comply to Twingyeo rules
            msg = requests.post('https://twingyeo.kr/api/v1/statuses/',headers=head,data=hd)
            congs.append(account['username']) # add to congs
            with open(base+'congratulated.txt','w') as f:
                for cong in congs:
                    f.write(cong+'\n') # update already congratulated members
    except:
        if dec == ':thump':
            pass
        elif datetime.datetime.today().day != prev:
            f = open(base+'congratulated.txt','w')
            f.close() # new day, new members to congratulate
            prev = datetime.datetime.today().day
        else:
            print(dec)
