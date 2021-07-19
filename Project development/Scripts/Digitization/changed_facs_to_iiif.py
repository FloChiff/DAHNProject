
# -*- UTF-8 -*-

"""
- author: Floriane Chiffoleau
- date: July 2021
- description: Changing the content of the @facs attribute to match the IIIF link
- input: XML files
- output: XML files
- usage :
    ======
    python name_of_this_script.py arg1 arg2 arg3
    arg1: name of the folder containing the XML files
    arg2: name of the folder containing the XML files
    arg3: ate of the execution of the script in the YYYY-MM-DD format
"""

import os
import re
import sys
from bs4 import BeautifulSoup                 

dico = {}

for root, dirs, files in os.walk(sys.argv[1]):
    for filename in files:
        with open(sys.argv[1] + filename, 'r') as xml_file:
            print("reading from "+sys.argv[1] + filename)
            text = xml_file.read()

            #Replace the content of the facs with its IIIF link
            for cle, valeur in dico.items():
                if cle in text:
                   text = text.replace(cle, valeur)

            soup = BeautifulSoup(text, 'xml')

            #Add a new information in the revisionDesc
            revision = soup.find("revisionDesc")
            new_change = soup.new_tag("change", who="#floriane.chiffoleau")
            new_change['when-iso'] = sys.argv[3]
            new_change.string = "Changed the content of the @facs to match the IIIF link"
            revision.insert(0, new_change)
            
        with open(sys.argv[2] + filename,"w") as file_out:
            print("writing to "+sys.argv[2] + filename)
            file_out.write(str(soup))