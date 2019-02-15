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

def getcount(repos, sha, until):
    count = 0
    value = 1
    page = 0
    while value == 1:
        url = "https://api.github.com/repos/"+args.org+"/"+str(repos)+"/commits?sha="\
              +str(sha)+"&until="+str(until)+"&page="+str(page+1)+"&per_page=100"
        res = requests.get(url, auth=auth)
        if len(res.json()) != 0:
            page = page+1
            count = count+len(res.json())
        else:
            value = value+1
    print (repos)
    print (count)
    return count


def getcountsince(repos, sha, since, until):
    count = 0
    value = 1
    page = 0
    while value == 1:
        url = "https://api.github.com/repos/"+args.org+"/"+str(repos)+"/commits?sha="\
              +str(sha)+"&since="+str(since)+"&until="+str(until)+"&page="+str(page+1)+"&per_page=100"
        res = requests.get(url, auth=auth)
        if len(res.json()) != 0:
            page = page+1
            count = count+len(res.json())
        else:
            value = value+1
    print (repos)
    print (count)
    return count

def update(repos, row_count, col_count, since, until):
    url = "https://api.github.com/repos/"+args.org+"/"+repos+"/branches"
    data = requests.get(url, auth=auth)
    print (repos)
    branch = []

    for j in range (len(data.json())):
        if data.json()[j]["name"] == "feature" or (data.json()[j]["name"]).split('/')[0] == "feature":
            count = getcount(repos, data.json()[j]['commit']['sha'], until)
            #sheet = gspreedauthorized()
            print (str(repos)+"respos:****************"+str(data.json()[j]["name"]))
            cell = [col_count, row_count, repos, count, data.json()[j]['commit']['sha']]
            branch.append(cell)
            #sheet.update_cell(col_count, row_count, count)
    print (branch)
    if len(branch) >= 1:
        count = 0
        for i in range(len(branch)):
            count = count+int(getcountsince(repos, branch[i][4], since, until))
            #total = getcount(repos, branch[i][4], since)
            total = int(branch[i][3])-count
        print (count, repos)
        sheet = gspreedauthorized()
        #sheet.update_cell(col_count, row_count, total+count)

    else:
        count = getcount(repos, branch[0][4], branch[0][3])
        sheet = gspreedauthorized()
        print (count, repos)
        #sheet.update_cell(col_count, row_count, count)


def commitcount():
    repos = json.load(open("repolist.json", 'r'))
    sheet = gspreedauthorized()
    row = len(sheet.col_values(1))+1
    sheet.update_acell('A'+str(len(sheet.col_values(1))+1), str(date.today()))
    sheet.update_acell('B'+str(len(sheet.col_values(1))), str(0))
    t = datetime.datetime.today().isoformat()

    for row_count in range (len(sheet.col_values(1))):
        if len(sheet.row_values(1)) != len(sheet.row_values(row_count+1)):
            for var in range (len(sheet.row_values(row_count+1)), len(sheet.row_values(1))+1):
                time = sheet.cell(row_count+1, 1).value
                yourdate = datetime.datetime.strptime(time, '%Y-%m-%d')
                t = yourdate.isoformat()
                parsed_t = dp.parse(t)
                t_in_seconds = parsed_t.strftime("%s")
                since = DT.datetime.utcfromtimestamp(int(t_in_seconds)-86400).isoformat()
                
                update(sheet.cell(1, var).value, var, row_count+1, since, t)

commitcount()
