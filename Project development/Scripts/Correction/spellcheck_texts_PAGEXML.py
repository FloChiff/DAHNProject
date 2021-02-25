# -*- UTF-8 -*-

"""
- author: Floriane Chiffoleau
- date: February 2021
- description: Recovering orthographic errors in PAGE XML files
- input: PAGE XML files
- output: Python dictionnaries
- usage :
    ======
    python name_of_this_script.py arg1 arg2 arg3

    arg1: folder of the PAGE XML files
    arg2: folder for the Python dictionnaries
    arg3: local dictionary adapted to the content's language of the PAGE XML
    
"""


import os
import re
import sys
from bs4 import BeautifulSoup
from spellchecker import SpellChecker

def suppress_punctuation(text):
    """ Suppress punctuation in a text
    
    :param text str: Text to clean up
    :returns: Text without punctuation
    :rtype: str
    """
    punctuation = "!:;\",?'’."
    for sign in punctuation:
        text = text.replace(sign, " ")
    return text

spell = SpellChecker(language=None, local_dictionary=sys.argv[3], case_sensitive=True)
#With 'case_sensitive=True', we precise that all the words are processed as they are written in the text
#This means that all the uppercase words will be considered wrong but that helps correct them
#To use that technique, we have to call a local dictionnary

for root, dirs, files in os.walk(sys.argv[1]):
    for filename in files:
        dictionary = {}
        with open(sys.argv[1] + filename, 'r') as xml_file:
            print("reading from "+sys.argv[1] + filename)
            soup = BeautifulSoup(xml_file, 'xml')
        for unicode in soup.find_all('Unicode'):
            content = unicode.string
            content = suppress_punctuation(content)
            words = content.split()
            misspelled = spell.unknown(words)
            for word in misspelled:
                dictionary[word] = spell.correction(word)
        with open(sys.argv[2].strip() + "/Dict" + filename.replace(".xml", ".py"),"w") as file_out:
            print("writing to "+ sys.argv[2] + "/Dict" + filename.replace(".xml", ".py"))
            file_out.write(filename.replace(".xml", "") +" = ")
            file_out.write(str(dictionary).replace("',", "',\n"))