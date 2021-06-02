
# -*- UTF-8 -*-

"""
- author: Floriane Chiffoleau
- date: June 2021
- description: This script is meant to provide some example of modifications that can be made inside an index of bibliographies (<biblStruct>) to made it TEI compliant and/or improve it
- input: XML file
- output: XML file
- usage :
    ======
    python name_of_this_script.py arg1 arg2 arg3
    arg1: name of the index
    arg2: new name for the index
    arg3: date of the execution of the description
"""

import re
import sys
from bs4 import BeautifulSoup

with open(sys.argv[1], 'r') as xml_file:
    print("reading from "+sys.argv[1])

    soup = BeautifulSoup(xml_file, 'xml')

    #Add an <authority> tag to the tree if it is missing, to have a valid file
    publication = soup.find("publicationStmt").find("availability")
    authority = soup.new_tag("authority")
    authority.string = "Humboldt-Universität zu Berlin"
    publication.insert_before(authority)

    #Retrieve the <relation> tags dispersed in the tree, print them in the terminal and suppress them from the tree
    for relation in soup.find_all("relation"):
    	print(relation)
        relation.decompose()    
    print("DECOMPOSED")

    #Add a new <change> tag to the <revisionDesc>
    revision = soup.find("revisionDesc")
    change = revision.find('change')
    new_change = soup.new_tag("change", who="#floriane.chiffoleau")
    new_change['when-iso'] = sys.argv[3]
    new_change.string = "Upgrading TEI encoding"
    revision.insert(0, new_change)


    for monogr in soup.find_all("monogr"):
        #The <monogr> tag requires at least a title and an imprint to be conform in the tree
        #If one of those elements is missing, it is added as empty tags in the tree
        title = monogr.find('title')
        if title == None:
            titre = soup.new_tag("title")
            monogr.append(titre)
        imprint = monogr.find("imprint")
        if imprint == None:
            new_imprint = soup.new_tag("imprint")
            monogr.append(new_imprint)
            pubPlace = soup.new_tag("pubPlace")
            new_imprint.append(pubPlace)
            publisher = soup.new_tag("publisher")
            new_imprint.append(publisher)
            date = soup.new_tag("date")
            new_imprint.append(date)
        #Change the name of the tag to be conform with what is expected inside the <imprint> tag 
        #and according to the content of the <extent> tag as observed in the modified file
        extent = imprint.find("extent")
        if extent != None:
            extent.name = "biblScope"

        #Search the <publisher> tag where it has an @type attribute, which is not accepted in XML TEI
        #A note is created, which have the corresponding information in it and the attribute is deleted
        publisher = imprint.find("publisher", type="commission")
        if publisher != None :
            tag = soup.new_tag("note")
            tag.string = "Commission"
            imprint.append(tag)
            del publisher["type"]

    tree = str(soup)
    #One of the attribute was given a wrong value so the correction is made with a simple find/replace
    tree = tree.replace('<title level="p"', '<title level="u"')

with open(sys.argv[2],"w") as file_out:
    print("writing to "+sys.argv[2])
    file_out.write(tree)