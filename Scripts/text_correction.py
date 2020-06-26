# -*- UTF-8 -*-

"""
- author: Floriane Chiffoleau
- date: June 2020
- description: Correcting orthographic errors in XML ALTO files
- input: text files and a Python dictionary
- output: corrected text files
"""

import os
import sys
import re
import dictionary
#The dictionary must be in the same place as the script in the tree structure.


for root, dirs, files in os.walk(sys.argv[1]):
    for filename in files:
        with open(sys.argv[1] + filename, 'r') as file_in:
            print("reading from "+sys.argv[1] + filename)
            with open(sys.argv[2] + filename,"w") as file_out:
                print("writing to "+sys.argv[2] + filename)
                correction_dictionary = eval("dictionary." + filename.replace(".xml", ""))
                for text in file_in:
                    for cle, valeur in correction_dictionary.items():
                        if cle in text:
                            text = text.replace(cle, valeur)
                    file_out.write(text)
