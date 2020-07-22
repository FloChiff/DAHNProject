# -*- UTF-8 -*-

"""
- author: Floriane Chiffoleau
- date: July 2020
- description: Correcting recurrent errors in the XML tree following the "text_tagging" script
- input: XML file
- output: XML file
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
        tree = tree.replace('<p rend="indent"><closer>', '<closer>')
        tree = tree.replace('<p rend="indent"><salute rend="indent">', '<salute rend="indent">')
        #Deletion of the extra tags made because of the "text_tagging" script

        soup = BeautifulSoup(tree, 'xml')

        n = 1
        for pb in soup.find_all("pb"):
            pb.attrs["n"] = n
            n += 1
            #Filling the @n attribute by numbering the pages

            for lb in soup.find_all("lb"):
                if pb.find_previous_sibling() == lb:
                    lb.decompose()
                 #Deletion of the <lb/> inserted before a <pb/>

        dateline = soup.find("dateline").string
        place = re.sub(r',.+', '', dateline)

        for origPlace in soup.find_all("origPlace"):
            origPlace.string = place.title()
        soup.placeName.string = place.title()
        #Insert the writing place of the letter in the metadata

        new_change = soup.new_tag("change", who="#floriane.chiffoleau")
        new_change['when-iso'] = sys.argv[3]
        new_change.string = "Encoding of the letter"
        soup.change.insert_before(new_change)
        #Update the revisionDesc

        with open(sys.argv[2] + filename,"w") as file_out:
            print("writing to "+sys.argv[2] + filename)
            file_out.write(str(soup))