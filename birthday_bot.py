#!/usr/bin/env python3
import json
import requests
import csv
import datetime
import pytz
import os

base = os.path.dirname(os.path.abspath(__file__)) + '/'
with open(base+'cred.json') as f:
    cred = json.load(f)

acc = cred[0][1]['cred']['access_token']
head = {'Authorization': 'Bearer ' + acc}  # Authorization
prev = ''  # for renewing data everday
congs = []  # already congratulated
time_format = '%Y-%m-%dT%H:%M:%S' # time format declared for reuse
instance_address = 'https://twingyeo.kr'

# connect to local timeline
uri_local = instance_address+'/api/v1/streaming/public/local'
r_local = requests.get(uri_local, headers=head, stream=True)
print('connected..')
for l in r_local.iter_lines():
    dec = l.decode('utf-8')
    try:
        #print('dec type: '+str(type(dec)))
        # strip off unnecessary part
        newdec = json.loads(dec.replace('data: ', ''))
        try:
            with open(base+'congratulated.txt') as f:
                for line in f:
                    # bring already congratulated members
                    congs.append(line.replace('\n', ''))
        except:
            congs = []
        account = newdec['account']
        # server time is in UTC, local time in KST(Asia/Seoul), converting UTC to KST
        created_at_server = account['created_at'][:-5]
        print('created_at_server: '+created_at_server)
        #time_format = '%Y-%m-%dT%H:%M:%S' # declared outside
        created_at_server_object = datetime.datetime.strptime(
            created_at_server, time_format)
        print('settings timezone')
        kst_format = pytz.timezone('Asia/Seoul')
        utc_format = pytz.timezone('UTC')
        created_at_server_object = utc_format.localize(created_at_server_object)  # now created_at_server has utc timezone
        print('created_at_server_object')
        created_at_local = kst_format.normalize(created_at_server_object.astimezone(
            kst_format)).isoformat()[:-6]  # converted value, last 6 chars are +09:00
        iso_today = datetime.datetime.today().isoformat()[:-7]
        print('created_at_local is '+str(created_at_local))
        print('iso_today is '+str(iso_today))
        # same created date but not in congs
        if created_at_local[5:10] == iso_today[5:10] and account['acct'] not in congs:
            instance = account['url'].split('/')[2]  # get instance address
            # calculate how many years have passed
            n = int(iso_today[:4]) - int(created_at_local[:4])
            hd = dict()
            if n > 0:  # more than a year
                hd['status'] = account['display_name']+' 님이 ' +instance+ '에 가입하신 지 '+str(n)+' 주 년이 되셨습니다. 축하합니다.'
            else:  # new member!
                if account['display_name'] == '':
                    hd['status'] = account['username'] + ' 님이 '+instance+'에 새로 오셨습니다. 환영합니다.'
                else:
                    hd['status'] = account['display_name'] + ' 님이 '+instance+'에 새로 오셨습니다. 환영합니다.'
            hd['visibility'] = 'unlisted'  # in comply to Twingyeo rules
            msg = requests.post(
                'https://twingyeo.kr/api/v1/statuses/', headers=head, data=hd)
            congs.append(account['acct'])  # add to congs
            with open(base+'congratulated.txt', 'w') as f:
                for cong in congs:
                    # update already congratulated members
                    f.write(cong+'\n')
    except:
        if dec == ':thump':
            pass
        elif datetime.datetime.today().day != prev:
            f = open(base+'congratulated.txt', 'w')
            f.close()  # new day, new members to congratulate
            prev = datetime.datetime.today().day
        else:
            print('error occured: '+dec)
