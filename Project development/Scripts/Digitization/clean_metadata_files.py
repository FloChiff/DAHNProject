
# -*- UTF-8 -*-

"""
- author: Floriane Chiffoleau
- date: September 2021
- description: Cleaning the metadata files extracted from NAKALA API
- input: JSON files
- output: Python files
- usage :
    ======
    python name_of_this_script.py arg1 arg2
    arg1: name of the folder containing the JSON files
    arg2: name of the folder containing the Python files
"""

import os
import re
import sys   


#This series of statements contains regex of recurrent occurences from the import files
mandatory = re.compile(r'\n +{\n +"value": ".+",\n +"lang": ("fr"|"en"|"de"|null),\n +"typeUri": "http://www.w3.org/2001/XMLSchema#(string|anyURI)",\n +"propertyUri": "http://nakala.fr/terms#(title|type|created|license)"\n +},')
metadata = re.compile(r'\n +{\n +"value": ".+",\n +"lang": (".+"|null),\n +"typeUri": ("http://www.w3.org/2001/XMLSchema#string"|null),\n +"propertyUri": "http://purl.org/dc/terms/.+"\n +},')
creator = re.compile(r'\n +{\n +"value": {\n +"givenname": ".+",\n +"surname": ".+",\n +"orcid": null,\n +"authorId": ".+"\n +},\n +"propertyUri": "http://nakala.fr/terms#creator"\n +}')
unknown = re.compile(r'{\n +"value": null,\n +"lang": null,\n +"typeUri": null,\n +"propertyUri": "http://nakala.fr/terms#created"\n +},')
embargo1 = re.compile(r'\n +"embargoed": "[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\+[0-9]{2}:[0-9]{2}",\n +"description": null,\n +"humanReadableEmbargoedDelay": \[]')
embargo2 = re.compile(r'\n +"status": "published",\n +"fileEmbargoed": false,\n +')
extra1 = re.compile(r'\n +"extension": "jpg",\n +"size": [0-9]{6,8},\n +"mime_type": "image/jpeg",\n +')
extra2 = re.compile(r'\n +"version": [0-9],\n +"files": +\[')
extra3 = re.compile(r' +"identifier": ".+",\n +"metas": \[\n +\]\n +},\n +{')
uri = re.compile(r' +],"uri": "https://doi.org/')
intro = re.compile(r'"total": [0-9]{1,},\n +"currentPage": [0-9]{1,},\n +"lastPage": [0-9]{1,},\n +"limit": [0-9]{1,},\n +"data": \[')
dico1 = re.compile(r' +{\n +"name": ')
dico2 = re.compile(r' ?,"sha1"')

for root, dirs, files in os.walk(sys.argv[1]):
    for filename in files:
        with open(sys.argv[1] + filename, 'r') as file_in:
            print("reading from "+sys.argv[1] + filename)
            text = file_in.read()

            text = re.sub(mandatory, "", text)
            text = re.sub(metadata, "", text)
            text = re.sub(creator, "", text)
            text = re.sub(unknown, "", text)
            text = re.sub(embargo1, "", text)
            text = re.sub(embargo2, "", text)
            text = re.sub(extra1, "", text)
            text = re.sub(extra2, "", text)
            text = re.sub(extra3, "", text)
            text = re.sub(uri, '"', text)
            text = re.sub(intro, "", text)
            text = re.sub(dico1, "", text)
            text = re.sub(dico2, "", text)
            
        with open(sys.argv[2] + filename.replace(".json", ".py"),"w") as file_out:
            print("writing to "+sys.argv[2] + filename)
            file_out.write(text)