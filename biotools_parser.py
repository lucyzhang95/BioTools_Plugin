import os
import json
import urllib3
import time
from datetime import datetime

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import pathlib

DEFAULT_TIMEOUT = 5 # seconds

class TimeoutHTTPAdapter(HTTPAdapter):
    '''Request nicely
    Ginger wrote the request functions
    '''
    def __init__(self, *args, **kwargs):
        self.timeout = DEFAULT_TIMEOUT
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)

## Set time outs, backoff, retries
httprequests = requests.Session()
retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["HEAD", "GET", "OPTIONS"]
)
adapter = TimeoutHTTPAdapter(timeout=5,max_retries=retry_strategy)
httprequests.mount("https://", adapter)
httprequests.mount("http://", adapter)


def cureationObject():
    '''Get source cureation
    The outbrak.info format of cureation can be found:
    https://discovery.biothings.io/view/outbreak/ComputationalTool
    '''
    now = datetime.now()
    cureatedBy = {
        "@type": "Organization",
        "identifier" : "elixier bio.tools",
        "url": "https://bio.tools/api/t?q=COVID-19&sort=score",
        "name": "bio.tools",
        "curationDate": now.strftime("%Y-%m-%d")
    }
    return(cureatedBy)

#print(cureationObject())

def infectiousAgent():
    infectiousAgent = {
        "@type": "DefinedTerm",
        "name": "SARS-CoV-2",
        "identifier": "NCBITaxon_2697049",
        "url": "http://purl.obolibrary.org/obo/NCBITaxon_2697049" 
        }
    return(infectiousAgent)
    
def infectiousDisease():
    infectiousDisease = {
        "@type": "DefinedTerm",
        "name": "COVID-19",
        "identifier": "MONDO_0100096",
        "url": "http://purl.obolibrary.org/obo/MONDO_0100096"
        }
    return(infectiousDisease)

def get_biotools_id():
    '''Get biotools ids
    bio.tools url:
    https://bio.tools/api/t?page=1&q=COVID-19&sort=score
    Parse through the json pages
    pull out biotoolsID from the list per page
    '''
    # Get total biotools count
    url = 'https://bio.tools/api/t'
    queries = {'format': 'json', 'q': 'COVID-19', 'sort':'score'}
    response = requests.get(url, params=queries, timeout=5).json()
    count = response['count']
    list_len = len(response['list'])
    
    rounds = round(count/list_len)
    
    biotools_id = []
    
    page = 0
    while page < rounds:
        page += 1
        queries_all = {
            'format': 'json', 
            'page': page, 
            'q': 'COVID-19', 
            'sort': 'score'}
        biotool_response = requests.get(url, params=queries_all, timeout=5)
        biotools_json = biotool_response.json()
        
        for value in biotools_json['list']:
            ids = value['biotoolsID']
            biotools_id.append(ids)

        time.sleep(1)
    return(biotools_id)

def get_git_bioschemas():
    '''Get corresponding bioschemas
    github url: 
    https://github.com/bio-tools/content/tree/master/data/
    '''
    # pull bioschema from github with corresponding biotoolsID
    repos_list = []
    git_ids = get_biotools_id()
    for id in git_ids:
        if len(git_ids) > 0:
            try:
                git_url = f'https://raw.githubusercontent.com/bio-tools/content/master/data/{id}/{id}.bioschemas.jsonld'
                git_response = requests.get(git_url, timeout=5)
                git_json = git_response.json()
                repos_list.append(git_json)
            except:
                repos_list.append(None)

        time.sleep(1)
    return(repos_list)

#print(len(get_git_bioschemas()))


