from datetime import date
from oauth2client.client import SignedJwtAssertionCredentials
from datetime import tzinfo, timedelta, datetime
import dateutil.parser as dp
import datetime as DT
import requests
import json
import argparse
import gspread
import datetime

import urllib3
urllib3.disable_warnings()

# run: python3 commitcount.py --username <username> --password <password> --org <org>
commandline = argparse.ArgumentParser(prog='PROG')
commandline.add_argument('--username')
commandline.add_argument('--password')
commandline.add_argument('--org')
args = commandline.parse_args()

auth = (args.username,args.password)

def gspreedauthorized():
    json_key = json.load(open('creds.json'))
    scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

    credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)

    file = gspread.authorize(credentials)
    sheet = file.open("SukuLab repo commit count").sheet1
    return sheet

def updatecommit(length, repos, row):
    sheet = gspreedauthorized()
    arr = []
    for i in range (len(sheet.row_values(1))):
        if repos == sheet.row_values(1)[i]:
            arr.append(repos)

    if len(arr) == 0:
        sheet.update_cell(1, len(sheet.row_values(1))+1, repos)
        
    else:
        sheet.update_cell(row, len(sheet.row_values(row))+1, length)

def update(repos, row_count, col_count, since):
    url = "https://api.github.com/repos/"+args.org+"/"+repos+"/branches"
    data = requests.get(url, auth=auth)
    print (repos)

    for j in range (len(data.json())):
        if data.json()[j]["name"] == "feature":
            url = "https://api.github.com/repos/"+args.org+"/"+str(repos)+"/commits?sha="\
                  +str(data.json()[j]['commit']['sha'])+"&since="+str(since)
            res = requests.get(url, auth=auth)
            print (len(res.json()))
            sheet = gspreedauthorized()
            sheet.update_cell(col_count, row_count, len(res.json()))

def commitcount():
    repos = json.load(open("repolist.json", 'r'))
    sheet = gspreedauthorized()
    row = len(sheet.col_values(1))+1
    sheet.update_acell('A'+str(len(sheet.col_values(1))+1), str(date.today()))
    sheet.update_acell('B'+str(len(sheet.col_values(1))), str(0))
    t = datetime.datetime.today().isoformat()
    parsed_t = dp.parse(t)
    t_in_seconds = parsed_t.strftime('%s')
    since = DT.datetime.utcfromtimestamp(int(t_in_seconds)-86400).isoformat()

    for row_count in range (len(sheet.col_values(1))):
        if len(sheet.row_values(1)) != len(sheet.row_values(row_count+1)):
            print (len(sheet.row_values(row_count+1)), len(sheet.row_values(1))+1)
            for var in range (len(sheet.row_values(row_count+1)), len(sheet.row_values(1))+1):
                time = sheet.cell(row_count+1, 1).value
                yourdate = datetime.datetime.strptime(time, '%Y-%m-%d')
                t = yourdate.isoformat()
                parsed_t = dp.parse(t)
                t_in_seconds = parsed_t.strftime('%s')
                since = DT.datetime.utcfromtimestamp(int(t_in_seconds)-86400).isoformat()
                update(sheet.cell(1, var).value, var, row_count+1, since)

commitcount()

# python3 commitcount.py --username richhamseth --password  --org Git2Swarm
