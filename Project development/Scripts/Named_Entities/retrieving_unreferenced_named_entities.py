# -*- UTF-8 -*-

"""
- author: Floriane Chiffoleau
- date: January 2022
- description: Retrieving unreferenced named entities (persName, placeName, orgName)
- input: XML files
- output: TXT files
- usage :
    ======
    python name_of_this_script.py arg1
    arg1: folder of the files with the unreferenced named entities

Warning: the created TXT files add information from the XML, one file after the other and does not rewrite the output file
If you execute this script several times, the output will be completed and never rewritten, which gives the risk of having the
same information over and over.
"""

import os
import re
import sys
from bs4 import BeautifulSoup

accolade = re.compile(r'(\[|\])')
linebreak = re.compile("Name>, ")
space = re.compile(r'\n +')

for root, dirs, files in os.walk(sys.argv[1]):
    for filename in files:
        with open(sys.argv[1] + filename, 'r') as xml_file:
            soup = BeautifulSoup(xml_file, 'xml')

            body = soup.find("body")
            
        liste = [person for person in body.find_all("persName", ref="")]
        liste_person = [string for string in set(liste)]
        liste_person = str(liste_person)
        liste_person = re.sub(linebreak, "Name>\n", liste_person)
        liste_person = re.sub(accolade, "", liste_person)
        liste_person = re.sub(space, "", liste_person)

        with open(sys.argv[2] + "person.txt", "a") as file_out:
            print("writing to person.txt")
            file_out.write(str(liste_person)+"\n")

        liste = [place for place in body.find_all("placeName", ref="")]
        liste_place = [string for string in set(liste)]
        liste_place = str(liste_place)
        liste_place = re.sub(linebreak, "Name>\n", liste_place)
        liste_place = re.sub(accolade, "", liste_place)
        liste_place = re.sub(space, "", liste_place)

        with open(sys.argv[2] + "place.txt", "a") as file_out:
            print("writing to place.txt")
            file_out.write(liste_place+"\n")

        liste = [org for org in body.find_all("orgName", ref="")]
        liste_org = [string for string in set(liste)]
        liste_org = str(liste_org)
        liste_org = re.sub(linebreak, "Name>\n", liste_org)
        liste_org = re.sub(accolade, "", liste_org)
        liste_org = re.sub(space, "", liste_org)

        with open(sys.argv[2] + "org.txt", "a", encoding='utf-8') as file_out:
            print("writing to org.txt")
            file_out.write(liste_org+"\n")

        liste = [title for title in body.find_all("title", ref="")]
        liste_title = [string for string in set(liste)]
        liste_title = str(liste_title)
        liste_title = re.sub(linebreak, "Name>\n", liste_title)
        liste_title = re.sub(accolade, "", liste_title)
        liste_title = re.sub(space, "", liste_title)

        with open(sys.argv[2] + "title.txt", "a", encoding='utf-8') as file_out:
            print("writing to title.txt")
            file_out.write(liste_title+"\n")