# Data Plugin of ComputationalTools relevant to COVID-19 in outbreak-info

This repository is for creating a data plugin from bio.tools computational tool list in outbreak.info

## Files and Folders

### biotoolID_github_parser.py
[biotoolID_github_parser.py](biotoolID_github_parser.py) is the parser to pull all bio.tool IDs relevant to COVID-19 from [bio.tool resource list](https://bio.tools/api/t?format=json&page=1&q=COVID-19&sort=score) and get the raw biotools.json from [GitHub Bioinformatics Tools Ecosystem contents repository](https://github.com/bio-tools/content/tree/master/data) by matching the bio.tool IDs obtained from original resource list

Can also check for the raw biotools.json that are not on github but with original resource list

### [New_Parsing folder](New_Parsing/)

A folder with all files related to new parser with raw biotool.json

[new_biotool_parser.py](New_Parsing/new_biotool_parser.py) (just started) is a python file used to convert the property from raw biotool.json to outbreak.info schemas

[bio_tools_original.json](New_Parsing/bio_tools_original.json) is the original raw json file obtained from Elixir bio.tools resource list

[ids_not_in_gihub.txt](New_Parsing/ids_not_in_github.txt) contains the bio.tool IDs that are not in GitHub repository but avaliable in original bio.tool resource list

[biotools_covid_bioschema.json](New_Parsing/biotools_covid_bioschema.json) is the json file contains the raw biotool.json obtained from GitHub repository

### [pandas_and_plots folder](New_Parsing/pandas_and_plots/)

A brief summary of flattened raw biotool.json in csv files to investigate the types and diversity of the schema properties

[biotool.json_pandas.py](New_Parsing/pandas_and_plots/biotool.json_pandas.py) is a python file used to export the flattened json using pandas package to csv files

[biotool_panda_df.csv](New_Parsing/pandas_and_plots/biotool_panda_df.csv) is a csv file includes entire raw biotool json properties

[biotool_property_check.csv](New_Parsing/pandas_and_plots/biotool_property_check.csv) is a csv file includes specific properties that are useful for analysis

[biotool_property_frequency.Rmd](New_Parsing/pandas_and_plots/biotool_property_frequency.Rmd) is a Rmd file with codes for generating the plots of specific properties

[biotool_property_frequency.html](New_Parsing/pandas_and_plots/biotool_property_frequency.html) is a html file has brief summary of specific properties with plots

### [Old_Parsing folder](Old_Parsing/)

A folder with all files related to old parser with old bioschemas.jsonld files (The original structure is no longer available now)

[bioschemas_matching_template folder](Old_Parsing/bioschemas_matching_template/) has the property mapping structure guide

[bioschemas_property_match.py](Old_Parsing/bioschemas_property_match.py) is a python file used to parse through and convert schema properties to outbreak.info schemas (**The code no longer apply to the new bioschemas.jsonld files found from GitHub Bioinformatics Tools Ecosystem contents repository**)

[Biotools_Plugin.ipynb](Old_Parsing/Biotools_Plugin.ipynb) is a jupiter notebook contains half of the contents for converting old bioschemas.jsonld files

[revised_biotool_format.json](Old_Parsing/revised_biotool_format.json) is a json file contains all converted old bioschemas.jsonld files to outbreak.info compatible schemas






