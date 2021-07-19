
# -*- UTF-8 -*-

"""
- author: Floriane Chiffoleau
- date: July 2021
- description: Extracting metadata from XML files into the terminal
- input: XML files
- usage :
    ======
    python name_of_this_script.py arg1
    arg1: name of the folder containing the XML files
"""

import os
import sys
from bs4 import BeautifulSoup

for root, dirs, files in os.walk(sys.argv[1]):
    for filename in files:
        with open(sys.argv[1] + filename, 'r') as xml_file:
            soup = BeautifulSoup(xml_file, 'xml')

            #Create a separation for each file
            print("[")

            #Print the titles of the file with separation after each
            title_fr = soup.find("title", attrs={"xml:lang": "fr"})
            print(title_fr.string + "$$")
            title_en = soup.find("title", attrs={"xml:lang": "en"})
            print(title_en.string + "$$")
            title_de = soup.find("title", attrs={"xml:lang": "de"})
            print(title_de.string + "$$")

            #Print the genre of the file if there is one with separation after
            for doc_type in soup.find_all("title", type="genre"):
                if doc_type != None:
                    print(doc_type.string)
                else:
                    print("Not given")

            print("$$")

            #Print the different type of author for the document with separation after
            writer = soup.find("correspAction", type='sent')
            author = soup.find("author")
            if writer != None:
                persName = writer.find("persName")
                orgName = writer.find("orgName")
                if persName != None:
                    print(persName.string + "$$")
                else:
                    print(orgName.string + "$$")
            elif author != None:
                persName = author.find("persName")
                print(persName.string + "$$")
            else:
                print("No author" + "$$")

            #Print the writing date of the file 
            date = soup.find("docDate")
            if date != None:
                print(str(date) + "$$")
            else:
                print("Inconnue" + "$$")

            #Print the language(s) of the file with separation only after the loop to have all the language(s) in one cell
            for lang in soup.find_all("language"):
                print(lang['ident'])

            print("$$")

            #Print the topic(s) of the file with separation only after the loop to have all the topic(s) in one cell
            for topic in soup.find_all('title', type="topic"):
                print(topic.string)

            print("$$")

            #Print the institution responsible for the file
            institution = soup.find("institution")
            print(institution.string)

            #End the separation between file
            print("]")