import csv
import os
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

usernameToToken = {}
aliasToProblemJid = {
    'A': 'JIDPROGxxx',
    'B': 'JIDPROGxxx',
    'C': 'JIDPROGxxx',
    'D': 'JIDPROGxxx',
    'E': 'JIDPROGxxx',
    'F': 'JIDPROGxxx'
}
contestJid = 'JIDCONTxxx'

with open('tokens.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        username = row[0]
        token = row[1]
        usernameToToken[username] = token

def submit(username, problemAlias, gradingLanguage, filename, solution, cnt):
    multi_part = MultipartEncoder(
        fields={
            'contestJid': contestJid,
            'problemJid': aliasToProblemJid[problemAlias],
            'gradingLanguage': gradingLanguage,
            'sourceFiles.source': (filename, solution, 'application/octet-stream')
        }
    )

    headers = {
        'Authorization': 'Bearer ' + usernameToToken[username],
        'Content-Type': multi_part.content_type
    }

    url = 'https://api.judgels/v2/contests/submissions/programming'

    print('Submitting {} - {} - {} ... '.format(problemAlias, cnt, username), end='')
    response = requests.post(url, data=multi_part, headers=headers)
    print(response.status_code, flush=True)


for problemAlias in aliasToProblemJid.keys():
    cnt = 0
    for dirname in sorted(os.listdir('../by-problem/{}'.format(problemAlias))):
        if dirname.startswith('.'):
            continue

        username = dirname.split(' - ')[0]
        for filename in os.listdir('../by-problem/{}/{}'.format(problemAlias, dirname)):
            if filename.endswith('_textresponse'):
                continue

            gradingLanguage = ''
            if filename.endswith('.c'):
                gradingLanguage = 'C'
            else:
                gradingLanguage = 'Cpp20'
            
            with open('../by-problem/{}/{}/{}'.format(problemAlias, dirname, filename), 'rb') as file:
                solution = file.read()
            
            cnt += 1

            submit(username, problemAlias, gradingLanguage, filename, solution, cnt)
