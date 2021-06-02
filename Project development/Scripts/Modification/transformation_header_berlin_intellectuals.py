
# -*- UTF-8 -*-

"""
- author: Floriane Chiffoleau
- date: June 2021
- description: Modifications made to the header of XML files to make them TEI compliant and homogeneous
- input: folder of XML files
- output: folder with corrected XML files
- usage :
    ======
    python name_of_this_script.py arg1 arg2 arg3
    arg1: folder with XML files
    arg2: new folder for corrected XML files
    arg3: date of the execution of the description
"""

import os
import re
import sys
from bs4 import BeautifulSoup

for root, dirs, files in os.walk(sys.argv[1]):
    for filename in files:
        with open(sys.argv[1] + filename, 'r') as xml_file:
            print("reading from "+sys.argv[1] + filename)
            tree = xml_file.read()
            #Change the attributes when it is not correct (@when for <docDate> and @when-iso for <change>)
            tree = tree.replace('docDate when-iso', 'docDate when')
            tree = tree.replace('change when=', 'change when-iso=')

            soup = BeautifulSoup(tree, 'xml')
            
            #Add an <authority> tag in the publication statement to have a valid XML file
            publication = soup.find("publicationStmt").find("availability")
            authority = soup.new_tag("authority")
            authority.string = "Humboldt-Universität zu Berlin"
            publication.insert_before(authority)

            #Add an <editorialDecl> in the <projectDesc> when it is missing to add the next tags
            edit = soup.find("editorialDecl")
            if edit == None:
                projectDesc = soup.find("projectDesc")
                new_change = soup.new_tag("editorialDecl")
                projectDesc.insert_after(new_change)

            #Transform the <hyphenation> tag, by changing the <seg> in <p> or by adding new information with new <p> tags
            hyphen = soup.find("hyphenation")
            if hyphen == None:
                edit = soup.find("editorialDecl")
                new_change = soup.new_tag("hyphenation", eol="hard")
                edit.insert(1, new_change)

            if hyphen != None:
                for seg in hyphen.find_all("seg"):
                    seg.name = "p"

            new_change = soup.new_tag("p")
            new_change["xml:lang"] = "fr"
            new_change.string = "Toutes les coupures de mots pour fin de ligne (indiquées principalement avec un double tiret) ont été enlevées."
            hyphen = soup.find("hyphenation")
            hyphen.insert(1, new_change)

            new_change = soup.new_tag("p")
            new_change["xml:lang"] = "en"
            new_change.string = "All the end-of-line hyphenation (made with a double hyphen) have been removed."
            hyphen = soup.find("hyphenation")
            hyphen.insert(2, new_change)

            #Transform the <correction> tag, by changing the <seg> in <p> or by adding new information with new <p> tags
            correction = soup.find("correction")
            if correction != None:
                for seg in correction.find_all("seg"):
                    seg.name = "p"

            if correction == None:
                edit = soup.find("editorialDecl")
                new_change = soup.new_tag("correction")
                edit.append(new_change)

                new_change = soup.new_tag("p")
                new_change["xml:lang"] = "fr"
                new_change.string = "Aucune correction"
                correction = soup.find("correction")
                correction.append(new_change)

                new_change = soup.new_tag("p")
                new_change["xml:lang"] = "en"
                new_change.string = "No correction"
                correction = soup.find("correction")
                correction.append(new_change)

                new_change = soup.new_tag("p")
                new_change["xml:lang"] = "de"
                new_change.string = "Keine Korrekturen."
                correction = soup.find("correction")
                correction.append(new_change)

            #Transform the <normalization> tag, by changing the <seg> in <p> or by adding new information with new <p> tags
            norm = soup.find("normalization")
            if norm != None:
                for seg in norm.find_all("seg"):
                    for p in seg.find_all("p"):
                        p.unwrap()
                    seg.name = "p"
            if norm == None:
                edit = soup.find("editorialDecl")
                new_change = soup.new_tag("normalization")
                edit.append(new_change)

                new_change = soup.new_tag("p")
                new_change["xml:lang"] = "fr"
                new_change.string = "Aucune normalisation"
                norm = soup.find("normalization")
                norm.append(new_change)

                new_change = soup.new_tag("p")
                new_change["xml:lang"] = "en"
                new_change.string = "No normalization"
                norm = soup.find("normalization")
                norm.append(new_change)

                new_change = soup.new_tag("p")
                new_change["xml:lang"] = "de"
                new_change.string = "Keine Normalisierung."
                norm = soup.find("normalization")
                norm.append(new_change)

            #Transform <seg> tags (incorrect in TEI) in the tag correspondant to its parent (the only acceptable tag in those cases)
            for measure in soup.find_all("measure"):
                if measure.attrs["type"] == "folio":
                    for seg in measure.find_all("seg"):
                        seg.name = "measure"

            material = soup.find("material")
            if material != None:
                for seg in material.find_all("seg"):
                    seg.name = "material"

            #Transform <seg> tags (incorrect in TEI) in <p> tag (everytime the tag is available in multiple languages)
            for foliation in soup.find_all("foliation"):
                if foliation != None:
                    for seg in foliation.find_all("seg"):
                        seg.name = "p"

            accMat = soup.find("accMat")
            if accMat != None:
                for seg in accMat.find_all("seg"):
                    seg.name = "p"

            seal = soup.find("sealDesc")
            if seal != None:
                for seg in seal.find_all("seg"):
                    seg.name = "p"

            acquisition = soup.find("acquisition")
            if acquisition != None:
                for seg in acquisition.find_all("seg"):
                    seg.name = "p"

            origin = soup.find("origin")
            if origin != None:
                for seg in origin.find_all("seg"):
                    seg.name = "p"

            for handNote in soup.find_all("handNote"):
                if handNote != None:
                    for seg in handNote.find_all("seg"):
                        seg.name = "p"

            condition = soup.find("condition")
            if condition != None:
                for seg in condition.find_all("seg"):
                    seg.name = "p"

            #Transform <seg> tags (incorrect in TEI) in <bibl> tag (for the bibliography)
            bibl = soup.find("bibl")
            if bibl != None:
                for seg in bibl.find_all("seg"):
                    seg.name = "bibl"

            #Suppress langages other than english and put it directly into the parent tag (<msIdentifier> or <affiliation>) instead of in a <seg> tag (incorrect in TEI)
            manuscript = soup.find("msIdentifier")
            for tags in manuscript.find_all("seg"):
                if tags.attrs["xml:lang"] != "en":
                    tags.decompose()
            for tag in manuscript.find_all():
                for seg in tag.find_all("seg"):
                    seg.unwrap()

            affiliation = soup.find("affiliation")
            for tags in affiliation.find_all("seg"):
                if tags.attrs["xml:lang"] != "en":
                    tags.decompose()
            for tag in affiliation.find_all():
                for seg in tag.find_all("seg"):
                    seg.unwrap()

            #Unified the reference (when it is not) for the name of the organisation (if it is always the same)
            org = affiliation.find('orgName')
            del org['ref']
            org["ref"] = '#hu.berlin'
            #print(org)

            #Add information about the projectDesc and tag it in multiple languages
            projectDesc = soup.find("projectDesc")
            p = projectDesc.find("p")
            p["xml:lang"] = "de"
            p.string = "Nachwuchsgruppe Berliner Intellektuelle 1800-1830"
            
            new_change = soup.new_tag("p")
            new_change["xml:lang"] = "fr"
            new_change.string = "Groupe de recherche junior du Berlin intellectuel des années 1800-1830"
            projectDesc.append(new_change)

            new_change = soup.new_tag("p")
            new_change["xml:lang"] = "en"
            new_change.string = "Junior research group of Berlin intellectuals 1800-1830"
            projectDesc.append(new_change)

            #Add a unified title fo the collection, as well as a new tag if there are none
            series = soup.find("seriesStmt")
            main = series.find("title", type="main")
            if main == None:
                new_change = soup.new_tag("title", type="main")
                new_change.string = "Briefe und Texte aus dem intellektuellen Berlin um 1800"
                series.insert(1, new_change)
            else: 
                main.string = "Briefe und Texte aus dem intellektuellen Berlin um 1800"

            #Suppress the linebreak that could be present in the title of the title statement
            main_title = soup.find("titleStmt")
            for title in main_title.find_all("title"):
                lb = title.find("lb")
                if lb != None:
                    lb.replace_with(" ")

            #Add a revisionDesc if it is missing
            revision = soup.find("revisionDesc")
            if revision == None :
                profile = soup.find("profileDesc")
                new_change = soup.new_tag("revisionDesc")
                profile.insert_after(new_change)
                revision = soup.find("revisionDesc")

            #Add an entry in the revisionDesc to document the changes made with the script
            new_change = soup.new_tag("change", who="#floriane.chiffoleau")
            new_change['when-iso'] = sys.argv[3]
            new_change.string = "Upgrading TEI encoding (header)"
            revision.insert(0, new_change)

            #Clear the blank space left because of the suppression of some tags
            text = str(soup)
            text = text.replace('>\n\n', '>')
            text = text.replace('\n\n<', '<')

        with open(sys.argv[2] + filename,"w") as file_out:
            print("writing to "+sys.argv[2] + filename)
            file_out.write(text)