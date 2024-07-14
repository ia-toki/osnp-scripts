import csv
import requests

results = {}

def process_submission(id):
    print('Processing submission {}'.format(id), flush=True)

    url = 'https://api.judgels/v2/contests/submissions/programming/id/{}'.format(id)
    headers = {
        'Authorization': 'Bearer xxx'
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(vars(response))
        return


    data = response.json()

    username = data['profile']['username']
    problemAlias = data['problemAlias']

    latestGrading = data['data']['submission']['latestGrading']
    results[username][problemAlias]['score'] = latestGrading['score']

    details = latestGrading['details']
    if details:
        for result in details['subtaskResults']:
            results[username][problemAlias]['subtask{}_score'.format(result['id'])] = min(1, int(result['score']))
        
        for tgResult in details['testDataResults']:
            for tcResult in tgResult['testCaseResults']:
                if tcResult['score'] == '*':
                    for subtaskId in tcResult['subtaskIds']:
                        if subtaskId > 0:
                            results[username][problemAlias]['subtask{}_correct_cases'.format(subtaskId)] += 1
    

usernames = []
with open('contestants.csv', 'r') as file:
    reader = csv.reader(file)
    header = next(reader)
    for row in reader:
        usernames.append(row[0])

for username in usernames:
    results[username] = {}    
    for problemAlias in ['A', 'B', 'C', 'D', 'E', 'F']:
        results[username][problemAlias] = {
            'score': 0,
            'subtask1_score': 0,
            'subtask1_correct_cases': 0,
            'subtask2_score': 0,
            'subtask2_correct_cases': 0
        }

# TODO fill the submission ID range here
for id in range(1, 5825+1):
    process_submission(id)

with open('results.csv', 'w') as file:
    writer = csv.writer(file)

    for username in usernames:
        row = [username]

        for problemAlias in ['A', 'B', 'C', 'D', 'E', 'F']:
            res = results[username][problemAlias]
            row.extend([
                res['subtask1_score'],
                res['subtask2_score']
            ])
        writer.writerow(row)

with open('results_detailed.csv', 'w') as file:
    writer = csv.writer(file)

    for username in usernames:
        row = [username]

        for problemAlias in ['A', 'B', 'C', 'D', 'E', 'F']:
            res = results[username][problemAlias]
            row.extend([
                res['subtask1_correct_cases'],
                res['subtask2_correct_cases']
            ])
        writer.writerow(row)
