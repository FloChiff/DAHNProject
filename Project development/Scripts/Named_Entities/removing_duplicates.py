# -*- UTF-8 -*-

"""
- author: Floriane Chiffoleau
- date: January 2022
- description: Annotating a corpus with named entities
- output: TXT file
- usage :
    ======
    python name_of_this_script.py arg1
    arg1: List of entities without duplicates

"""

import os
import re
import sys

#The content of the list will be the content of the output file of the finding_named_entities script 
text = []

entities = set(text)
entities = str(entities)
#Supress the elements that made it a Python list
entities = re.sub(r"{('|\")|('|\")}", "", entities)
entities = re.sub("\", (\"|')", '\n', entities)
entities = re.sub("', (\"|')", '\n', entities)
#Transform the space in tab to help with the migration on the spreadsheet
entities = re.sub(r' LOC\n', '\tLOC\n', entities)
entities = re.sub(r' PER\n', '\tPER\n', entities)
entities = re.sub(r' ORG\n', '\tORG\n', entities)
entities = re.sub(r' MISC\n', '\tMISC\n', entities)
with open(sys.argv[1], "w") as file_out:
    file_out.write(entities)
    print("writing the output file")