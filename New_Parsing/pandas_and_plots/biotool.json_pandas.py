from asyncio import as_completed
import json
from json import tool
from sqlite3 import Row
from tkinter import N
import pandas as pd

# Open the file from raw github 
file1 = open('/Users/lucyzhang1116/Documents/GitHub/BioTools_Plugin/New_Parsing/biotools_covid_bioschema.json')
data = json.load(file1)
pd_data = data #make a json file for pandas

# Use pandas to flatten the properties
df = pd.json_normalize(data)
df.to_csv('biotool_panda_df.csv')

#print(type(data)) #list
#print(type(data[1])) #dict
#print(data[1].keys())
#dict_keys(['additionDate', 'biotoolsCURIE', 'biotoolsID', 'collectionID', 'confidence_flag', 
#'credit', 'description', 'editPermission', 'function', 'homepage', 'lastUpdate', 'name', 
#'owner', 'publication', 'toolType', 'topic'])
#print(data[1]['credit'])
    
publication_list = []   
for tool_dict in pd_data:
    if 'credit' not in tool_dict.keys():
        tool_dict.update({'credit':None})
    else:
        for key_value in tool_dict['credit']:
            keys = ['typeEntity', 'typeRole']
            if not key_value.keys() & {'typeEntity', 'typeRole'}:
                key_value.update({'typeEntity':None, 'typeRole':None})
    if 'accessibility' not in tool_dict.keys():
        tool_dict.update({'accessibility':None})
    if 'owner' not in tool_dict.keys():
        tool_dict.update({'owner':None})

    if 'publication' not in tool_dict.keys():
        tool_dict.update({'publication':None})
    else:
        for elem in tool_dict.get('publication'):
            if 'doi' in elem.keys():
                tools = tool_dict.get('biotoolsID')
                publication_list.append(tools)

#print(len(publication_list)) #209




# Put flattened biotool json to csv for R analysis
flat_property_check = pd.json_normalize(
    data, 'credit', ['biotoolsID', 'accessibility', 'owner', 'publication'])
flat_property_check.to_csv('biotool_property_check.csv')


           
        

        

