
# -*- UTF-8 -*-

"""
- author: Floriane Chiffoleau
- date: June 2021
- description: This script is meant to provide some example of information retrieval and modifications that can be made inside an index of persons (<person>) to made it TEI compliant and/or improve it
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

    #Add a new <change> tag in the <revisionDesc>
    revision = soup.find("revisionDesc")
    new_change = soup.new_tag("change", who="#floriane.chiffoleau")
    new_change['when-iso'] = sys.argv[3]
    new_change.string = "Modified/corrected some tags"
    revision.insert(0, new_change)

    #Retrieve all the relation dispersed in the tree, print them in the terminal and suppress them from the tree
    for grp in soup.find_all("relationGrp"):
        print(grp)
        grp.decompose()
    print("DECOMPOSED")
    for relation in soup.find_all("relation"):
        print(relation)
        relation.decompose()    
    print("DECOMPOSED")


    for person in soup.find_all("person"):
        #Put in variable some elements from the tree that are child of the <person> tag
        pers = person.get("xml:id")
        persName = person.find("persName")
        surname = person.find("surname")
        forename = person.find("forename")
        birth = person.find("birth")
        death = person.find("death")
        #Put the content of <event> in a paragraph tag, as it should be
        for event in person.find_all("event"):
            if event != None:
                new_event = soup.new_tag("event")
                event.wrap(new_event)
        for event in person.find_all("event"):
            for p in event.find_all("event"):
                if p != None:
                    p.name = "p"

        #Retrieve the persons where the <persName> only contains text and no surname or forename encoded
        if surname == None and forename == None:
            print(pers)
        
        #Retrieve the persons who does not have birthdate but do have birthplace
        if birth != None:
            bdate = birth.find("date")
            bplace = birth.find("placeName") 
            if bdate == None and bplace != None:
                print(pers)

        #Retrieve the persons who have no data for birth AND death
        if death == None and birth == None:
           print(pers)

        #Search the tree for birthdate and deathdate where the string of the date is either YYYY, -YYYY or DD MM YYYY
        #Suppress the string in any case to harmonize and does not put extra unnecessary data
        #Retrieve the cases where the date is in the YYYY or -YYYY format to transform the attribute from @when-iso to @when with a find/replace and a Python dictionary
        if birth != None:
            for date in birth.find_all("date", string=re.compile(r'^(-?[0-9]{1,4})$')):
                date.string = ""
                print(date)
            for date in birth.find_all("date", string=re.compile(r'^([0-9]{1,2}.? ?[A-Za-zÀ-ÖØ-öø-ÿ-]+ ?[0-9]{2,4})$')):
                date.string = ""
        if death != None:
            for date in death.find_all("date", string=re.compile(r'^(-?[0-9]{1,4})$')):
                date.string = ""
                print(date)
            for date in death.find_all("date", string=re.compile(r'^([0-9]{1,2}.? ?[A-Za-zÀ-ÖØ-öø-ÿ-]+ ?[0-9]{2,4})$')):
                date.string = ""

    text = str(soup)
    #Suppress the extra whitespaces added because of the decomposed() method
    text = text.replace('\n\n\n', ' ')
    text = text.replace('>\n\n', '>')
    text = text.replace('\n\n<', '<')


with open(sys.argv[2],"w") as file_out:
    print("writing to "+sys.argv[2])
    file_out.write(text)
    #file_out.write(str(soup))

