import requests
import json
import time

'''
print(type(info['list']))
print(type(info['list'][3]))
'info' the whole document is an object=dictionary
'list' is an array=list,
'biotoolsID' is a dictionary within list
info_list = info['list']
print(len(info_list))
10 elements in the info_list

with open('bio_tools.json', 'w') as f:
    json.dump(info, f, indent=2)

'''

url = 'https://bio.tools/api/t'
payloads = {'format': 'json', 'q': 'COVID-19', 'sort':'score'}
r = requests.get(url, params=payloads, timeout=5).json()
count = r['count']
list_num = len(r['list'])

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
else:
    rounds = round(numbers)
#print(rounds)

biotools_id = []
biotools_description = []

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
    
    for content in biotools_json['list']:
        descriptions = content['description']
        biotools_description.append(descriptions)

#print(len(biotools_description))
#print(len(biotools_id))

# Pull out correspondant repositories from github json url
repos_list = []
id_notin_git = []
for id in biotools_id:
    if len(biotools_id) > 0:
        try:
            git_url = f'https://raw.githubusercontent.com/bio-tools/content/master/data/{id}/{id}.bioschemas.jsonld'
            git_response = requests.get(git_url, timeout=5)
            git_json = git_response.json()
            repos_list.append(git_json)
        except:
            id_notin_git.append(id)
            
    time.sleep(1)

with open('biotools_covid_bioschema.json', 'w+') as f:
    json.dump(repos_list, f, indent=2)

with open('ids_not_in_github.txt', 'w+') as f2:
    seconds = time.time()
    time = time.ctime(seconds)
    new_line = '\n'
    f2.write(f'{time} {new_line} {id_notin_git} {new_line} There are in total {len(id_notin_git)} ids.')




