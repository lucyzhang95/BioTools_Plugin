import requests
import json
import time


'''Parsing Content Summary
Json format
an object=dictionary
an array=list
'biotoolsID' is a dictionary within the list
'''

url = 'https://bio.tools/api/t'
payloads = {'format': 'json', 'q': 'COVID-19', 'sort':'score'}
r = requests.get(url, params=payloads, timeout=5).json()
count = r['count']
list_num = len(r['list'])


# Two methods to get the biotool IDs from 'https://bio.tools/api/t?page=1&q=COVID-19&sort=score'
# One is using for loop and the other one is using while loop
# I used while loop in this case

'''
# Method 1 with for loop

rounds = round(count/list_num) + 1

biotools_list = []
for page in range(1, rounds):
    try:
        payloads_all = {'format': 'json', 'page': page, 'q': 'COVID-19', 'sort': 'score'}
        biotool_response = requests.get(url, params=payloads_all, timeout=5)
        biotool_json = biotool_response.json()
        bio_response_list = biotool_json['list']
        biotools_list.append(bio_response_list)
    except:
        biotools_list.extend(None)
print(biotool_response.url)
'''


# Method 2 with while loop
numbers = count/list_num
if numbers%1 < 0.5:
    rounds = round(numbers) + 1
elif numbers%1 == 0.5:
    rounds = round(numbers) + 1
else:
    rounds = round(numbers)
#print(rounds)

biotools_id = []

page = 0
while page < rounds:
    page += 1
    payloads_all = {
    'format': 'json', 
    'page': page, 
    'q': 'COVID-19', 
    'sort': 'score'}
    biotool_response = requests.get(url, params=payloads_all, timeout=5)
    biotools_json = biotool_response.json()

    for value in biotools_json['list']:
        ids = value['biotoolsID']
        biotools_id.append(ids)
    
    with open('bio_tools_original.json', 'w') as f:
        json.dump(biotools_json, f, indent=2)

#print(len(biotools_description))
#print(len(biotools_id))

# Pull out correspondant repositories from github json url
repos_list = []
id_notin_git = []
for id in biotools_id:
    if len(biotools_id) > 0:
        try:
            git_url = f'https://raw.githubusercontent.com/bio-tools/content/master/data/{id}/{id}.biotools.json'
            git_response = requests.get(git_url, timeout=5)
            git_json = git_response.json()
            repos_list.append(git_json)
        except:
            id_notin_git.append(id)
            
    time.sleep(1)

with open('biotools_covid_bioschema.json', 'w+') as f1:
    json.dump(repos_list, f1, indent=2)

# biotool IDs not found on github or ID names not matching
with open('ids_not_in_github.txt', 'w+') as f2:
    seconds = time.time()
    time = time.ctime(seconds)
    new_line = '\n'
    f2.write(f'{time} {new_line} {id_notin_git} {new_line}') 
    f2.write(f'There are in total {len(repos_list) + len(id_notin_git)} tools. {len(id_notin_git)} tools not on github.')




