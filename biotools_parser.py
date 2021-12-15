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
        "url": "https://bio.tools/api/t?page=1&q=COVID-19&sort=score", #this link only shows page 1
        "name": "COVID-19 related biotools",
        "curationDate": now.strftime("%Y-%m-%d, %H:%M:%S")
    }
    return(curatedBy)

def get_biotools_id(biotools_id):
    '''Get biotools ids
    bio.tools url:
    https://bio.tools/api/t?page=1&q=COVID-19&sort=score
    Parse through the website pages
    pull out biotoolsID
    '''
    # define total number of tools from web count info
    url = 'https://bio.tools/api/t'
    payloads = {'format': 'json', 'q': 'COVID-19', 'sort':'score'}
    response = requests.get(url, params=payloads, timeout=5).json()
    count = response['count']
    list_num = len(response['list'])
    
    rounds = round(count/list_num) + 1
    
    # loop through the pages to get biotoolsID
    biotools_list = []
    for page in range(1, rounds):
        try:
            payloads_all = {'format': 'json', 'page': page, 'q': 'COVID-19', 'sort': 'score'}
            biotool_response = requests.get(url, params=payloads_all, timeout=5)
            biotool_json = biotool_response.json()
            bio_response_list = biotool_json['list']
            biotools_list.extend(biotool_json)
        except:
            biotools_list.extend(None)
    
    biotools_id = []
    for n in range(0, len(biotools_list)):
        if len(biotools_list) > 0:
            try:
                biotools_id.append(biotools_list[n]['biotoolsID'])
            except:
                biotools_id.append(None)
        
        time.sleep(1)
    return(biotools_id)

def get_git_bioschemas(biotools_bioschema):
    '''Get corresponding bioschemas
    github url: 
    https://github.com/bio-tools/content/tree/master/data/
    '''
    # pull bioschema from github with corresponding biotoolsID
    repos_list = []
    for id in biotools_id:
        if len(biotools_id) > 0:
            try:
                git_url = f'https://raw.githubusercontent.com/bio-tools/content/master/data/{id}/{id}.bioschemas.jsonld'
                git_response = requests.get(git_url, timeout=5)
                git_json = git_response.json()
                repos_list.append(git_json)
            except:
                repos_list.append(None)

        time.sleep(1)
    return(repos_list)


