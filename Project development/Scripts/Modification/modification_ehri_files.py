import os
import re
import sys
from bs4 import BeautifulSoup

for root, dirs, files in os.walk(sys.argv[1]):
    for filename in files:
        with open(sys.argv[1] + filename, 'r') as xml_file:
            print("reading from "+sys.argv[1] + filename)

            text = xml_file.read()

            #Add the RELAX NG to link the XML file to our ODD documentation
            text = text.replace('href="http://www.tei-c.org/release/xml/tei/custom/schema/relaxng/tei_all.rng"', 'href="../../Guidelines/out/Documentation-Correspondance.rng"')
            
            #Replace the references in the text by the new ID that will be established later in the script and other minor corrections
            text = text.replace('ref="https://portal.ehri-project.eu/keywords/ehri_terms-', 'ref="#t')
            text = re.sub(r'ref="https://portal.ehri-project.eu/keywords/ehri_(camps|ghettos)-', 'ref="#l', text)
            text = text.replace('ref="https://portal.ehri-project.eu/authorities/ehri_pers-', 'ref="#p')
            text = text.replace('ref="https://portal.ehri-project.eu/authorities/ehri_cb-', 'ref="#g')
            text = text.replace('ref="https://portal.ehri-project.eu/keywords/terezin-terms-keyword-jmp-', 'ref="#t')
            text = re.sub(r'ref="http(s)?://www.geonames.org/[0-9]{1,}/', 'ref="#', text)
            text = text.replace('.html', '')
            text = re.sub(r'ref="https://portal.ehri-project.eu/(authorities/)?terezin-victims-person-iti-', 'ref="#p', text)
            text = re.sub(r'ref="http(s)?://(en|de).wikipedia.org/wiki/', 'ref="#', text)
            text = re.sub(r'ref="http(s)?://www.holocaust.cz/databaze-obeti/obet/[0-9]{1,}-', 'ref="#', text)
            text = re.sub(r'ref="https://portal.ehri-project.eu/keywords/terezin-places-place-(iti|jmp)-', 'ref="#l', text)
            text = text.replace('/"', '"')
            text = text.replace("> ,", '>,')
            text = text.replace("> .", ">.")
            text = text.replace("> )", ">)")


            soup = BeautifulSoup(text, 'xml')

            #Add a <revisionDesc>
            revision = soup.find("revisionDesc")
            if revision == None :
                profile = soup.find("profileDesc")
                new_change = soup.new_tag("revisionDesc")
                profile.insert_after(new_change)
                revision = soup.find("revisionDesc")

            new_change = soup.new_tag("change", who="#ehri")
            new_change['when-iso'] = "2020"
            new_change.string = "Encoding of the file"
            revision.insert(0, new_change)

            new_change = soup.new_tag("change", who="#floriane.chiffoleau")
            new_change['when-iso'] = sys.argv[3]
            new_change.string = "Upgrading TEI encoding"
            revision.insert(0, new_change)


            edition = soup.find("editionStmt")
            for author in edition.find_all("author"):
                tag = soup.new_tag("resp")
                tag.string = "Edited by"
                author.name = "respStmt"
                author.insert(0, tag)
            edit = edition.find("edition")
            edit.name = "respStmt"
            edit.string.wrap(soup.new_tag("orgName"))
            tag = soup.new_tag("resp")
            tag.string = "Edited by"
            edit.insert(0, tag)
            edition.unwrap()


            #Add additional informations about the corpus
            titleStmt = soup.find("titleStmt")
            title = titleStmt.find("title")
            title["xml:lang"] = "en"
            tag = soup.new_tag("title")
            tag["xml:lang"] = "fr"
            titleStmt.append(tag)
            principal = soup.new_tag("principal")
            titleStmt.append(principal)
            affiliation = soup.new_tag("affiliation")
            principal.append(affiliation)
            orgName = soup.new_tag("orgName")
            orgName.string = "European Holocaust Research Infrastructure"
            affiliation.append(orgName)

            source = soup.find("sourceDesc")
            series = soup.new_tag("seriesStmt")
            source.insert_before(series)
            titre = soup.new_tag("title", type="main")
            titre.string = "EHRI Edition of Early Holocaust Testimonies"
            series.append(titre)

            profileDesc = soup.find("profileDesc")
            encoding = soup.new_tag("encodingDesc")
            profileDesc.insert_before(encoding)
            project = soup.new_tag("projectDesc")
            encoding.append(project)

            new_change = soup.new_tag("p")
            new_change["xml:lang"] = "fr"
            new_change.string = "L'encodage de ce document s'est fait dans le cadre du projet 'EHRI Edition of Early Holocaust Testimonies'"
            project.append(new_change)

            new_change = soup.new_tag("p")
            new_change["xml:lang"] = "en"
            new_change.string = "The encoding of this document is part of the project 'EHRI Edition of Early Holocaust Testimonies'"
            project.append(new_change)

            
            #Add extra information in the manuscript identifier
            manuscript = soup.find("msIdentifier")
            repository = manuscript.find('repository')
            country = manuscript.find('country')
            country.decompose()
            location = soup.new_tag("location")
            manuscript.insert(0, location)
            address = soup.new_tag("address")
            location.append(address)
            street = soup.new_tag("street")
            address.append(street)
            postcode = soup.new_tag("postCode")
            address.append(postcode)
            settlement = soup.new_tag("settlement")
            address.append(settlement)
            country = soup.new_tag("country")
            address.append(country)
            repo = repository.get("ref")
            if repo == "https://portal.ehri-project.eu/institutions/hu-002737":
                street.string = "Dohány u. 2"
                postcode.string = "1077"
                settlement.string = "Budapest"
                country.string = "Hungary"
                country["ref"] = "https://portal.ehri-project.eu/countries/hu"
            if repo == "https://portal.ehri-project.eu/institutions/cz-002279":
                street.string = "U Staré školy 141/1"
                postcode.string = "110 00"
                settlement.string = "Prague"
                country.string = "Czech Republic"
                country["ref"] = "https://portal.ehri-project.eu/countries/cz"
            if repo == "https://portal.ehri-project.eu/institutions/gb-003348":
                street.string = "29 Russell Square"
                postcode.string = "WC1B 5DP"
                settlement.string = "London"
                country.string = "United Kingdom"
                country["ref"] = "https://portal.ehri-project.eu/countries/gb"
            if repo == "https://portal.ehri-project.eu/institutions/il-002798":
                street.string = "Har Hazikaron"
                postcode.string = "P.O.B. 3477"
                settlement.string = "Jerusalem"
                country.string = "Israel"
                country["ref"] = "https://portal.ehri-project.eu/countries/il"
            if repo == "https://portal.ehri-project.eu/institutions/pl-003146":
                street.string = "Tłomackie 3/5"
                postcode.string = "00-090 "
                settlement.string = "Warsaw"
                country.string = "Poland"
                country["ref"] = "https://portal.ehri-project.eu/countries/pl"

            
            #To add only if needed for named entities display
            body = soup.find("body")
            for persName in body.find_all("persName"):
                persName["type"] = "ehri"
            for orgName in body.find_all("orgName"):
                orgName["type"] = "ehri"
            for placeName in body.find_all("placeName", type=None):
                placeName["type"] = "ehri"

            #Insert the text in a <div> with a @type
            body = soup.find("body")
            new_body = soup.new_tag("body")
            body.wrap(new_body)
            body = soup.find("body")
            div = body.find("body")
            div.name = "div"
            div["type"] = "testimony"

            
            #Search for list of named entities and define an ID according to links given from the web
            listPlace = soup.find("listPlace")
            listPerson = soup.find("listPerson")
            listOrg = soup.find("listOrg")
            if listPlace != None:
                for place in listPlace.find_all('place'):
                    link = place.find("link")
                    target = link.get("target")
                    place["xml:id"] = target
            if listPerson != None:
                for person in listPerson.find_all('person'):
                    link = person.find("link")
                    if link != None:
                        target = link.get("target")
                        person["xml:id"] = target
            if listOrg != None:
                for org in listOrg.find_all('org'):
                    link = org.find("link")
                    if link != None:
                        target = link.get("target")
                        org["xml:id"] = target
            sourceDesc = soup.find("sourceDesc")
            liste = sourceDesc.find("list")
            if liste != None:
                for item in liste.find_all("item"):
                    if item != None:
                        link = item.find("link")
                        if link != None:
                            target = link.get("target")
                            item["xml:id"] = target


            #Clean the ID so that it only have the number as a reference (similar regex than those from above)
            text = str(soup)
            text = text.replace('xml:id="https://portal.ehri-project.eu/keywords/ehri_terms-', 'xml:id="t')
            text = re.sub(r'xml:id="https://portal.ehri-project.eu/keywords/ehri_(camps|ghettos)-', 'xml:id="l', text)
            text = text.replace('xml:id="https://portal.ehri-project.eu/authorities/ehri_pers-', 'xml:id="p')
            text = text.replace('xml:id="https://portal.ehri-project.eu/authorities/ehri_cb-', 'xml:id="g')
            text = text.replace('xml:id="https://portal.ehri-project.eu/keywords/terezin-terms-keyword-jmp-', 'xml:id="t')
            text = re.sub(r'xml:id="http(s)?://www.geonames.org/[0-9]{1,}/', 'xml:id="', text)
            text = re.sub(r'xml:id="https://portal.ehri-project.eu/(authorities/)?terezin-victims-person-iti-', 'xml:id="p', text)
            text = re.sub(r'xml:id="http(s)?://(en|de).wikipedia.org/wiki/', 'xml:id="', text)
            text = re.sub(r'xml:id="http(s)?://www.holocaust.cz/databaze-obeti/obet/[0-9]{1,}-', 'xml:id="', text)
            text = re.sub(r'xml:id="https://portal.ehri-project.eu/keywords/terezin-places-place-(iti|jmp)-', 'xml:id="l', text)
            

            #Suppress the list of named entities from the XML files to print them in the terminal
            #(Useful to then create unique indexes)
            soup = BeautifulSoup(text, 'xml')
            sourceDesc = soup.find("sourceDesc")
            liste = sourceDesc.find("list")
            print(liste)
            liste.decompose()
            listPlace = soup.find("listPlace")
            print(listPlace)
            listPlace.decompose()
            listPerson = soup.find("listPerson")
            print(listPerson)
            listPerson.decompose()
            listOrg = soup.find("listOrg")
            print(listOrg)
            if listOrg != None:
                listOrg.decompose()

            
            #Fix some remaining mistakes in the XML file
            text = str(soup)
            text = re.sub(r'\n\n', '', text)
            text = re.sub(r'</titleStmt>\n<respStmt>', r'\n<respStmt>', text)
            text = re.sub(r'</respStmt>\n<publicationStmt>', r'</respStmt>\n</titleStmt>\n<publicationStmt>', text)
            


        with open(sys.argv[2] + filename,"w") as file_out:
            print("writing to "+sys.argv[2] + filename)
            file_out.write(text)
            #file_out.write(str(soup))