# -*- UTF-8 -*-

"""
- author: Floriane Chiffoleau
- date: July 2020
- description: Correcting recurrent errors in the XML tree following the "text_tagging" script
- input: XML file
- output: XML file
"""

import os
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

        with open(sys.argv[1] + filename.replace(".xml", "_changed.xml"),"w") as file_out:
            print("writing to "+sys.argv[1] + filename.replace(".xml", "_changed.xml"))
            file_out.write(str(soup))