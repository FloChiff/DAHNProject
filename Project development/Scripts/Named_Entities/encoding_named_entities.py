# -*- UTF-8 -*-

"""
- author: Floriane Chiffoleau
- date: January 2022
- description: Annotating a corpus with named entities
- input: TEI-XML files
- output: Named entities encoded TEI-XML files
- usage :
    ======
    python name_of_this_script.py arg1 arg2 arg3

    arg1: folder of the corpus in XML format
    arg2: folder of the corpus in XML format
    arg3: arg3: date of the execution of the script in the YYYY-MM-DD format

"""

import os
import re
import sys
from bs4 import BeautifulSoup
#Calling the functions to use for the annotation of the text
from function_persName import persName
from function_placeName import placeName
from function_orgName import orgName
from function_title import title

for root, dirs, files in os.walk(sys.argv[1]):
    for filename in files:
        with open(sys.argv[1] + filename, 'r') as file_in:
            print("reading from "+sys.argv[1] + filename)
            soup = BeautifulSoup(file_in, 'xml')

        #Prologue of our XML file
        declaration = '<?xml version="1.0" encoding="utf-8"?>\n<?xml-model href="../../Guidelines/out/Documentation-Correspondance.rng" type="application/xml" schematypens="http://relaxng.org/ns/structure/1.0"?>\n<TEI xmlns="http://www.tei-c.org/ns/1.0">'
        end = "</TEI>"
        header = soup.find("teiHeader")
        revision = soup.find("revisionDesc")
        new_change = soup.new_tag("change", who="#floriane.chiffoleau")
        new_change['when-iso'] = sys.argv[3]
        new_change.string = "Encoding of the named entities"
        revision.insert(0, new_change)
        body = soup.find("text")
        text = str(body)
        text = persName(text)
        text = placeName(text)
        text = title(text)
        text = orgName(text)

        with open(sys.argv[2] + filename, "w") as file_out:
            print("writing to " + filename)
            #Recreating the XML tree
            file_out.write(declaration)
            file_out.write(str(header))
            file_out.write(text)
            file_out.write(end)