import json
from json import tool

# Open the file from raw github 
file1 = open('/Users/lucyzhang1116/Documents/GitHub/BioTools_Plugin/New_Parsing/biotools_covid_bioschema.json')
data = json.load(file1)


def schema(entry):
    '''Transform biotool json to outbreak.info json schema
    '''

    tool_list = []
    jsonld = {}   

    # Add @context
    context = {
        "@context": {
            "outbreak": "https://discovery.biothings.io/view/outbreak/",
            "schema": "http://schema.org/",
            "bioschemas": "https://discovery.biothings.io/view/bioschemas"
        }
    }


    tools = {}
    tool_list = []

    for elem in entry:
        if isinstance(elem, dict):
            if 'additionDate' in elem.keys():
                tools['dateCreated'] = elem['additionDate']
            if 'biotoolsID' in elem.keys():
                tools['@id'] = elem['biotoolsID']
            if 'description' in elem.keys():
                tools['description'] = elem['description']
            if 'documentation' in elem.keys():
                tools['softwareHelp'] = elem['documentation']

                tool_list.append(tools)
                

                print(tool_list[0:1])

                

                





    return(json.dumps(jsonld, indent=2))

print(schema(data))
                



   
    
    
