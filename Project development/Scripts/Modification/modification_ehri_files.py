# -*- UTF-8 -*-

import os
import re
import sys
from bs4 import BeautifulSoup

for root, dirs, files in os.walk(sys.argv[1]):
    for filename in files:
        with open(sys.argv[1] + filename, 'r') as xml_file:
            #print("reading from "+sys.argv[1] + filename)
            soup = BeautifulSoup(xml_file, 'xml')

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
            titre.string = sys.argv[4]
            series.append(titre)

            profileDesc = soup.find("profileDesc")
            encoding = soup.new_tag("encodingDesc")
            profileDesc.insert_before(encoding)
            project = soup.new_tag("projectDesc")
            encoding.append(project)

            new_change = soup.new_tag("p")
            new_change["xml:lang"] = "fr"
            new_change.string = "L'encodage de ce document s'est fait dans le cadre du travail sur les éditions en ligne EHRI"
            project.append(new_change)

            new_change = soup.new_tag("p")
            new_change["xml:lang"] = "en"
            new_change.string = "The encoding of this document is part of the work on the EHRI Online Editions"
            project.append(new_change)

            new_change = soup.new_tag("p")
            new_change["xml:lang"] = "de"
            new_change.string = "Die Kodierung dieses Dokuments ist Teil der Arbeit an den EHRI Online Editions"
            project.append(new_change)

            #Add a <revisionDesc>
            revision = soup.find("revisionDesc")
            if revision == None :
                profile = soup.find("profileDesc")
                new_change = soup.new_tag("revisionDesc")
                profile.insert_after(new_change)
                revision = soup.find("revisionDesc")

            new_change = soup.new_tag("change", who="#ehri")
            new_change['when-iso'] = sys.argv[6]
            new_change.string = "Encoding of the file"
            revision.insert(0, new_change)

            new_change = soup.new_tag("change", who="#floriane.chiffoleau")
            new_change['when-iso'] = "2024-05-27"
            new_change.string = "Upgrading TEI encoding"
            revision.insert(0, new_change)


            #Suppress the list of named entities from the XML files to print them in the terminal
            #(Useful to then create unique indexes)
            sourceDesc = soup.find("sourceDesc")
            liste = sourceDesc.find("list")
            if liste != None:
                liste.decompose()
            listPlace = soup.find("listPlace")
            if listPlace != None:
                listPlace.decompose()
            listPerson = soup.find("listPerson")
            if listPerson != None:
                listPerson.decompose()
            listOrg = soup.find("listOrg")
            if listOrg != None:
                listOrg.decompose()

            #Insert the text in a <div> with a @type
            body = soup.find("body")
            new_body = soup.new_tag("body")
            body.wrap(new_body)
            body = soup.find("body")
            div = body.find("body")
            div.name = "div"
            new_div = soup.new_tag("div")
            div.wrap(new_div)
            div = soup.find("div")
            div["type"] = "transcription"
            div1 = div.find("div")
            div1["type"] = sys.argv[3]
            language = soup.find("language")
            if language:
                ident = language["ident"]
                div1["xml:lang"] = ident
            if language == None:
                langusage = soup.new_tag("langUsage")
                profileDesc.append(langusage)
                language = soup.find("langUsage")
                lang = soup.new_tag("language")
                language.append(lang)
                lang["ident"] = ""

            publisher = soup.find("publisher")
            publisher.name = "authority"

            manuscript = soup.find("msIdentifier")
            if manuscript:
                repository = manuscript.find('repository')
                if repository != None:
                    country = manuscript.find('country')
                    country.decompose()
                    institution = soup.new_tag("institution")
                    repository.wrap(institution)
                    location = soup.find("institution")
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
                    repository = soup.find("repository")
                    repository.name = "orgName"
                    repo = repository.get("ref")
                    if repo == "https://portal.ehri-project.eu/institutions/cz-006030":
                        street.string = "Loretánské náměstí 5"
                        postcode.string = "110 00"
                        settlement.string = "Prague"
                        country.string = "Czech Republic"
                        country["ref"] = "https://portal.ehri-project.eu/countries/cz"
                    if repo == "https://portal.ehri-project.eu/institutions/cz-002286":
                        street.string = "Archivní 2257/4"
                        postcode.string = "149 00"
                        settlement.string = "Prague"
                        country.string = "Czech Republic"
                        country["ref"] = "https://portal.ehri-project.eu/countries/cz"
                    if repo == "https://portal.ehri-project.eu/institutions/at-001965":
                        street.string = "Landhausplatz 1"
                        postcode.string = "3109"
                        settlement.string = "St. Pölten"
                        country.string = "Austria"
                        country["ref"] = "https://portal.ehri-project.eu/countries/at"
                    if repo == "https://portal.ehri-project.eu/institutions/sk-003250":
                        street.string = "Drotárska cesta 42, P.O.BOX 115"
                        postcode.string = "817 01"
                        settlement.string = "Bratislava"
                        country.string = "Slovakia"
                        country["ref"] = "https://portal.ehri-project.eu/countries/sk"
                    if repo == "https://portal.ehri-project.eu/institutions/cz-002230":
                        street.string = "Palachovo náměstí 1."
                        postcode.string = "625 00"
                        settlement.string = "Brno"
                        country.string = "Czech Republic"
                        country["ref"] = "https://portal.ehri-project.eu/countries/cz"
                    if repo == "https://portal.ehri-project.eu/institutions/us-005578":
                        street.string = "100 Raoul Wallenberg Place, S.W."
                        postcode.string = "DC 20024-2126"
                        settlement.string = "Washington"
                        country.string = "United States of America"
                        country["ref"] = "https://portal.ehri-project.eu/countries/us"
                    if repo == "https://portal.ehri-project.eu/institutions/gb-003348":
                        street.string = "29 Russell Square"
                        postcode.string = "WC1B 5DP"
                        settlement.string = "London"
                        country.string = "United Kingdom"
                        country["ref"] = "https://portal.ehri-project.eu/countries/gb"
                    if repo == "https://portal.ehri-project.eu/institutions/at-001860":
                        street.string = "Landhaus alt, Europaplatz 1"
                        postcode.string = "7000"
                        settlement.string = "Eisenstadt"
                        country.string = "Austria"
                        country["ref"] = "https://portal.ehri-project.eu/countries/at"
                    if repo == "https://portal.ehri-project.eu/institutions/cz-002291":
                        street.string = "Klášter 81"
                        postcode.string = "664 61"
                        settlement.string = "Rajhrad"
                        country.string = "Czech Republic"
                        country["ref"] = "https://portal.ehri-project.eu/countries/cz"
                    if repo == "https://portal.ehri-project.eu/institutions/at-001982":
                        street.string = "Altes Rathaus, Wipplingerstr. 6-8"
                        postcode.string = "1010"
                        settlement.string = "Vienna"
                        country.string = "Austria"
                        country["ref"] = "https://portal.ehri-project.eu/countries/at"
                    if repo == "https://portal.ehri-project.eu/institutions/at-001985":
                        street.string = "Desider-Friedmann-Platz 1"
                        postcode.string = "1010"
                        settlement.string = "Vienna"
                        country.string = "Austria"
                        country["ref"] = "https://portal.ehri-project.eu/countries/at"
                    if repo == "https://portal.ehri-project.eu/institutions/at-001980":
                        street.string = " Nottendorfer Gasse 2"
                        postcode.string = "1030"
                        settlement.string = "Vienna"
                        country.string = "Austria"
                        country["ref"] = "https://portal.ehri-project.eu/countries/at"
                    if repo == "https://portal.ehri-project.eu/institutions/cz-002279":
                        street.string = "U Staré školy 141/1"
                        postcode.string = "110 00"
                        settlement.string = "Prague"
                        country.string = "Czech Republic"
                        country["ref"] = "https://portal.ehri-project.eu/countries/cz"
                    if repo == "https://portal.ehri-project.eu/institutions/il-002781":
                        street.string = "The Edmond J. Safra Campus on Giv'at Ram"
                        postcode.string = "91010"
                        settlement.string = "Jerusalem"
                        country.string = "Israel"
                        country["ref"] = "https://portal.ehri-project.eu/countries/il"
                    if repo == "https://portal.ehri-project.eu/institutions/il-002798":
                        street.string = "Har Hazikaron"
                        postcode.string = "P.O.B. 3477"
                        settlement.string = "Jerusalem"
                        country.string = "Israel"
                        country["ref"] = "https://portal.ehri-project.eu/countries/il"
                    if repo == "https://portal.ehri-project.eu/institutions/us-005522":
                        street.string = "8601 Adelphi Road"
                        postcode.string = "MD 20740-6001"
                        settlement.string = "Maryland"
                        country.string = "United States of America"
                        country["ref"] = "https://portal.ehri-project.eu/countries/us"
                    if repo == "https://portal.ehri-project.eu/institutions/dk-002313":
                        street.string = "Rigsdagsgaarden 9"
                        postcode.string = "DK-1218"
                        settlement.string = "Copenhagen"
                        country.string = "Denmark"
                        country["ref"] = "https://portal.ehri-project.eu/countries/dk"
                    if repo == "https://portal.ehri-project.eu/institutions/jp-006512":
                        street.string = "Sumitomo Fudosan Hongo Building 10F"
                        postcode.string = "3-22-5"
                        settlement.string = "Tokyo"
                        country.string = "Japan"
                        country["ref"] = "https://portal.ehri-project.eu/countries/jp"
                    if repo == "https://portal.ehri-project.eu/institutions/it-002863":
                        street.string = "Piazzale della Farnesina, 1"
                        postcode.string = "00196"
                        settlement.string = "Roma"
                        country.string = "Italy"
                        country["ref"] = "https://portal.ehri-project.eu/countries/it"
                    if repo == "https://portal.ehri-project.eu/institutions/hu-002737":
                        street.string = "Dohány u. 2"
                        postcode.string = "1077"
                        settlement.string = "Budapest"
                        country.string = "Hungary"
                        country["ref"] = "https://portal.ehri-project.eu/countries/hu"
                    if repo == "https://portal.ehri-project.eu/institutions/pl-003146":
                        street.string = "Tłomackie 3/5"
                        postcode.string = "00-090"
                        settlement.string = "Warsaw"
                        country.string = "Poland"
                        country["ref"] = "https://portal.ehri-project.eu/countries/pl"
                    if repo == "https://portal.ehri-project.eu/institutions/de-002409":
                        street.string = "Grosse Allee 5-9"
                        postcode.string = "34454"
                        settlement.string = "Bad Arolsen"
                        country.string = "Germany"
                        country["ref"] = "https://portal.ehri-project.eu/countries/de"
                    if repo == "https://portal.ehri-project.eu/institutions/at-001982":
                        street.string = "Altes Rathaus, Wipplingerstr. 6-8"
                        postcode.string = "1010"
                        settlement.string = "Vienna"
                        country.string = "Austria"
                        country["ref"] = "https://portal.ehri-project.eu/countries/at"
                    if repo == "https://portal.ehri-project.eu/institutions/at-001990":
                        street.string = "Gasometer D, Guglgasse 14 Postfach: Rathaus, A-1082 Vienna"
                        postcode.string = "1010"
                        settlement.string = "Vienna"
                        country.string = "Austria"
                        country["ref"] = "https://portal.ehri-project.eu/countries/at"
            
             
            bibl = soup.find("bibl")
            if bibl:
                textlang = bibl.find("textLang")
                if textlang == None:
                    tl = soup.new_tag("textLang")
                    bibl.append(tl)
                    tl.string = "Original in ..."
                    tl["mainLang"] = "..."
            

            #Fix some remaining mistakes in the XML file
            text = str(soup)
            text = re.sub(r'\n\n', '', text)
            text = re.sub(r'</titleStmt>\n?<respStmt>', r'\n<respStmt>', text)
            text = re.sub(r'</respStmt>\n?<publicationStmt>', r'</respStmt>\n</titleStmt>\n<publicationStmt>', text)
            text = re.sub(r'</sponsor>\n?<publicationStmt>', r'</sponsor>\n</titleStmt>\n<publicationStmt>', text)
            text = text.replace('" xmlns', '_EN" xmlns')
            text = text.replace("<TEI", '<?xml-model href="https://gitlab.inria.fr/dh-projects/workflow-ehri/-/raw/main/ODD/out/ODD-EHRI.rng" type="application/xml" schematypens="http://relaxng.org/ns/structure/1.0"?><TEI')
            text = re.sub(r'<\?xml-model href="http://www.tei-c\.org/release/xml/tei/custom/schema/relaxng/tei_all.rng" type="application/xml" schematypens="http://relaxng.org/ns/structure/1.0"\?><!--EHRI ODT to TEI convertor: .+-->', "", text)
            text = text.replace("EN_EN", "EN")

        with open(sys.argv[2] + filename.replace(".xml", sys.argv[5]),"w") as file_out:
            #print("writing to "+sys.argv[2] + filename)
            file_out.write(text)
            #file_out.write(str(soup))