
# -*- UTF-8 -*-

"""
- author: Floriane Chiffoleau
- date: June 2021
- description: This script is meant to provide some example of modifications that can be made inside an index of organisations (<org>) to made it TEI compliant and/or improve it
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
    tree = xml_file.read()

    #Translate from deutsch to english recurrent terms from the tree
    tree = tree.replace(">Dekan", ">Dean")
    tree = tree.replace(">Oberpräsident", ">Chief President")
    tree = tree.replace(">Oberpräsident", ">Chief President")
    tree = tree.replace(">Polizeipräsident", ">Police chief")
    tree = tree.replace(">Innenminister", ">Interior minister")
    tree = tree.replace(">Universitätsrektor als Stellvertreter", ">University rector as deputy")
    tree = tree.replace(">Direktor", ">Director")
    tree = tree.replace(">Ordentliche Mitglieder", ">Ordinary members")
    tree = tree.replace(">Außerordentliche Mitglieder", ">Associate members")
    tree = tree.replace(">Lehrer", ">Teacher")
    tree = tree.replace(">Rektor", ">Rector")
    tree = tree.replace(">Mitglied", ">Member")

    soup = BeautifulSoup(tree, 'xml')

    #Add an <authority> tag to the tree if it is missing, to have a valid file
    publication = soup.find("publicationStmt").find("availability")
    authority = soup.new_tag("authority")
    authority.string = "Humboldt-Universität zu Berlin"
    publication.insert_before(authority)

    #The file is written in deutsch so we specify it in the <orgName> tag when it is not specified
    for org in soup.find_all("org"):
        orgName = org.find("orgName")
        attr = orgName.get("xml:lang")
        if attr == None:
            orgName["xml:lang"] = "de"

    #Search a specific part of the tree, by using a regex to find the value of the id (one or more values)
    #Add the english translation of the name of the organization
    #The date is added manually afterwards
    for org in soup.find_all("org", attrs={"xml:id": re.compile(r'(g002)[2-9]{1}')}):
        orgName = org.find("orgName")
        new_change = soup.new_tag("orgName")
        new_change["xml:lang"] = "en"
        new_change.string = 'Professors at the Philosophical Faculty of the Berlin University for the'
        date = soup.new_tag("date")
        date["when-iso"] = ""
        date.string = "academic year"
        new_change.append(date)
        orgName.insert_after(new_change)
    for org in soup.find_all("org", attrs={"xml:id": "g0030"}):
        orgName = org.find("orgName")
        new_change = soup.new_tag("orgName")
        new_change["xml:lang"] = "en"
        new_change.string = 'Professors at the Philosophical Faculty of the Berlin University for the'
        date = soup.new_tag("date")
        date["when-iso"] = ""
        date.string = "academic year"
        new_change.append(date)
        orgName.insert_after(new_change)


    for org in soup.find_all("org", attrs={"xml:id": re.compile(r'(g00)[4|5][0|2|4|6|8]')}):
        orgName = org.find("orgName")
        new_change = soup.new_tag("orgName")
        new_change["xml:lang"] = "en"
        new_change.string = 'Ordinary Members of the Philology Seminar at the Berlin University'
        date = soup.new_tag("date")
        date["when-iso"] = ""
        date.string = "summer term"
        new_change.append(date)
        orgName.insert_after(new_change)
    for org in soup.find_all("org", attrs={"xml:id": re.compile(r'(g00)(36|38|60|62)')}):
        orgName = org.find("orgName")
        new_change = soup.new_tag("orgName")
        new_change["xml:lang"] = "en"
        new_change.string = 'Ordinary Members of the Philology Seminar at the Berlin University'
        date = soup.new_tag("date")
        date["when-iso"] = ""
        date.string = "summer term"
        new_change.append(date)
        orgName.insert_after(new_change)
    for org in soup.find_all("org", attrs={"xml:id": re.compile(r'(g00)[4|5][1|3|5|7|9]')}):
        orgName = org.find("orgName")
        new_change = soup.new_tag("orgName")
        new_change["xml:lang"] = "en"
        new_change.string = 'Ordinary Members of the Philology Seminar at the Berlin University'
        date = soup.new_tag("date")
        date["when-iso"] = ""
        date.string = "winter term"
        new_change.append(date)
        orgName.insert_after(new_change)
    for org in soup.find_all("org", attrs={"xml:id": re.compile(r'(g00)(35|37|39|61)')}):
        orgName = org.find("orgName")
        new_change = soup.new_tag("orgName")
        new_change["xml:lang"] = "en"
        new_change.string = 'Ordinary Members of the Philology Seminar at the Berlin University'
        date = soup.new_tag("date")
        date["when-iso"] = ""
        date.string = "winter term"
        new_change.append(date)
        orgName.insert_after(new_change)


    for org in soup.find_all("org", attrs={"xml:id": re.compile(r'(g009)[1|3|5|7|9]')}):
        orgName = org.find("orgName")
        new_change = soup.new_tag("orgName")
        new_change["xml:lang"] = "en"
        new_change.string = 'Extraordinary Members of the Philology Seminar at the Berlin University'
        date = soup.new_tag("date")
        date["when-iso"] = ""
        date.string = "summer term"
        new_change.append(date)
        orgName.insert_after(new_change)
    for org in soup.find_all("org", attrs={"xml:id": re.compile(r'(g0)(087|089|101|103|105)')}):
        orgName = org.find("orgName")
        new_change = soup.new_tag("orgName")
        new_change["xml:lang"] = "en"
        new_change.string = 'Extraordinary Members of the Philology Seminar at the Berlin University'
        date = soup.new_tag("date")
        date["when-iso"] = ""
        date.string = "summer term"
        new_change.append(date)
        orgName.insert_after(new_change)
    for org in soup.find_all("org", attrs={"xml:id": re.compile(r'(g009)[0|2|4|6|8]')}):
        orgName = org.find("orgName")
        new_change = soup.new_tag("orgName")
        new_change["xml:lang"] = "en"
        new_change.string = 'Extraordinary Members of the Philology Seminar at the Berlin University'
        date = soup.new_tag("date")
        date["when-iso"] = ""
        date.string = "winter term"
        new_change.append(date)
        orgName.insert_after(new_change)
    for org in soup.find_all("org", attrs={"xml:id": re.compile(r'(g0)(086|088|100|102|104)')}):
        orgName = org.find("orgName")
        new_change = soup.new_tag("orgName")
        new_change["xml:lang"] = "en"
        new_change.string = 'Extraordinary Members of the Philology Seminar at the Berlin University'
        date = soup.new_tag("date")
        date["when-iso"] = ""
        date.string = "winter term"
        new_change.append(date)
        orgName.insert_after(new_change)
    for org in soup.find_all("org", attrs={"xml:id": re.compile(r'(g010)[6|7|8|9]')}):
        orgName = org.find("orgName")
        new_change = soup.new_tag("orgName")
        new_change["xml:lang"] = "en"
        new_change.string = 'Extraordinary Members of the Philology Seminar at the Berlin University'
        date = soup.new_tag("date")
        date["when-iso"] = ""
        date.string = "winter term and/or summer term"
        new_change.append(date)
        orgName.insert_after(new_change)

    #Add a new <change> tag in the <revisionDesc>
    revision = soup.find("revisionDesc")
    change = revision.find('change')
    new_change = soup.new_tag("change", who="#floriane.chiffoleau")
    new_change['when-iso'] = sys.argv[3]
    new_change.string = "Added translations for some tags"
    revision.insert(0, new_change)


with open(sys.argv[2],"w") as file_out:
    print("writing to "+sys.argv[2])
    file_out.write(str(soup))