import json

# Open the json file with all collected bio.tools bioschema
file1 = open('/Users/lucyzhang1116/Documents/GitHub/BioTools_Plugin/Schema_properties/biotools_covid_bioschema.json')
data = json.load(file1)
#print(len(data))

# Check hasPublication strings
with open('hasPublication_list.txt', 'w+') as f, open('no_hasPublication_list.txt', 'w+') as f2:
    for eachitem in data:
        graph = eachitem.get('@graph')
        #print(type(graph), len(graph))
        #print(graph)
        
        dict_key = 'hasPublication'
        publication_result = []
        ids_pub = []
        ids_no_pub = []
        
        if dict_key in graph.keys():
            ids_yes = graph['@id']
            ids_pub.append(ids_yes)
            
            pub_content = graph['hasPublication']
            publication_result.append(pub_content)
            n = '\n'
            #print(f"'{ids}' with {publication_result} has hasPublication")
            f.write(f"{ids_pub} with {publication_result}{n}")
            #wc -l hasPublication_list.txt (169 hasPublication_list.txt)

        else:
            ids_no = graph['@id']
            ids_no_pub.append(ids_no)
            #print(f"'{ids}' does not have hasPublication"
            f2.write(f"'{ids_no_pub} does not have hasPublication'{n}")
            #wc -l no_hasPublication_list.txt (57 no_hasPublication_list.txt)


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

def transform_property():
    '''Convert property names for outbreak.info schema format
    Delete excessive properties in @context
    Change properties in @graph
    '''
    for item in data:
        # Delete properties in @context
        context = item.get('@context')
        prop_remove = ('description', 'name', 'identifier', 
        'sameAs', 'homepage', 'toolType', 'primaryContact', 'author', 
        'provider', 'contributor', 'funder', 'hasPublication', 'hasTopic',
        'hasOperation', 'hasInputData', 'hasOutputData', 'license',
        'version', 'isAccessibleForFree', 'operatingSystem', 'hasApiDoc',
        'hasGenDoc', 'hasTermsOfUse', 'conformsTo')
        
        for key in prop_remove:
            if key in context:
                context.pop(key, None)
        #print(context)
    
    def switch_key(new_key, old_key):
        # function to convert old keys to new keys in @graph
        for graph in data:
            graph_context = graph.get('@graph')
            if isinstance(graph_context, dict):
                if old_key in graph_context:
                    graph_context[new_key] = graph_context[old_key]
                    del graph_context[old_key]
                else:
                    pass
    
    switch_key('softwareHelp', 'hasGenDoc')
    switch_key('isRelatedto', 'hasPublication')
    switch_key('featureList', 'hasOperation')
    switch_key('applicationSubCategory', 'hasTopic')
    switch_key('output', 'hasOutputData')
    switch_key('input', 'hasInputData')

    for item in data:
        graph_content = item.get('@graph')

        if 'isAccessibleForFree' in graph_content.keys():
            del graph_content['isAccessibleForFree']
        
        graph_content['infectiousAgent'] = infectiousAgent()
        graph_content['infectiousDisease'] = infectiousDisease()

        # Adjust contents in @graph/isRelatedto
        if isinstance(graph_content, dict):
            hasPublication = 'isRelatedto'
            if hasPublication in graph_content:
                isRelatedto = graph_content['isRelatedto']
                for citation in isRelatedto:
                    if not isinstance(citation, dict):
                        if citation.startswith('pubmed'):
                            strings = citation.split(':')[1]

                    elif isinstance(citation, dict):
                        citation['@type'] = 'outbreak:Publication'
                        citation['url'] = citation['@id']
                        del citation['@id']
                        citation['doi'] = citation['url']
                        citation['doi'] = citation['doi'].replace('https://doi.org/', '')
                        citation['pmid'] = strings   

            else:
                pass

            if hasPublication in graph_content:
                isRelatedto = graph_content['isRelatedto']
                for publication in isRelatedto:
                    if not isinstance(publication, dict): #only looping through the first item (pubmed)
                        #print(publication)
                        isRelatedto.remove(publication)
                        
                        '''
                        When tried to use the above code, cannot remove pmcid, but removed pubmed
                        Not sure why it is 
                        Since print(publication) shows both pubmed and pmcid
                        but remove only iterate through the first item which is "pubmed"
                        '''

                for publication in isRelatedto: #looping through other part (pmcid) and remove it
                    if not isinstance(publication, dict):
                        isRelatedto.remove(publication)
                    
            # Adjust contents in @graph/softwareHelp
            hasGenDoc = 'softwareHelp'
            if hasGenDoc in graph_content:
                software = graph_content['softwareHelp']
                for doc in software:
                    if isinstance(doc, dict):
                        doc['url'] = doc['@id']
                        del doc['@id']
                        doc['@type'] = 'CreativeWork'
            else:
                pass

            # Adjust contents in @graph/hasOperation
            hasOperation = 'featureList'
            if hasOperation in graph_content:
                hasOperation = graph_content['featureList']
                for lists in hasOperation:
                    if isinstance(lists, dict):
                        lists['@type'] = 'DefinedTerm'
                        lists['url'] = lists['@id']
                        del lists['@id']

                        lists['identifier'] = lists['url']
                        lists['identifier'] = lists['identifier'].replace('http://edamontology.org/', '')
            else:
                pass

            # Adjust contents in @graph/hasTopic
            hasTopic = 'applicationSubCategory'
            if hasTopic in graph_content:
                hasTopic = graph_content['applicationSubCategory']
                for topics in hasTopic:
                    if isinstance(topics, dict):
                        topics['@type'] = 'DefinedTerm'
                        topics['url'] = topics['@id']
                        del topics['@id']

                        topics['identifier'] = topics['url']
                        topics['identifier'] = topics['identifier'].replace('http://edamontology.org/', '')
            else:
                pass

            hasOutputData = 'output'
            if hasOutputData in graph_content:
                hasOutputData = graph_content['output']
                for output in hasOutputData:
                    if isinstance(output, dict):
                        del output['sameAs']
                        del output['@id']
                        output['@type'] = output['@type'].replace('bsct:', '')
                        output['url'] = output['identifier']
                        output['identifier'] = output['identifier'].replace('http://edamontology.org/', '')
            else:
                pass

            hasInputData = 'input'
            if hasInputData in graph_content:
                hasInputData = graph_content['input']
                for inputs in hasInputData:
                    if isinstance(inputs, dict):
                        del inputs['sameAs']
                        del inputs['@id']
                        inputs['@type'] = inputs['@type'].replace('bsct:', '')
                        inputs['url'] = inputs['identifier']
                        inputs['identifier'] = inputs['identifier'].replace('http://edamontology.org/', '')
            else:
                pass

    return(json.dumps(data, indent=2))


with open('revised_biotool_format.json', 'w+') as f3:
    f3.write(transform_property())





        

    
        













