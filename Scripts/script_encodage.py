# -*- UTF-8 -*-

"""
- author: Floriane Chiffoleau
- date: June 2020
- description: Encoding a corpus with some basic XML tags
- input: plain text
- output: tagged text
"""

import os
import re
import sys

def tagging_paragraph(text):
    """ Add paragraph tags in a text
    
    :param text str: text that has to be modify
    :returns: text encoded with paragraph tags
    :rtype: str
    """
    punctuation = "!\"»?."  
    # This variable contains all the punctuation signs that indicates a phrase ending
    # and a need for an ending paragraph tag

    for sign in punctuation:
        text = text.replace(sign + "\n", sign + '</p>\n<p rend="indent">')
        text = text.replace(sign + " \n", sign + '</p>\n<p rend="indent">')
    # This function can add unnecessary paragraph tag that will have to be suppress afterwards
    return text


def page_numbering(text):
    """ Add tags to the page numbering

    :param text str: text that has to be modify
    :returns: page numbering encoded with corresponding tags
    :rtype: str
    """

    if "-" in text[:1]:
        text = text.replace("- ", '<pb n="" facs=".JPG"/><note type="foliation" place="top">- ')
        text = text.replace(" -\n", ' -</note> ')
    return text


def closing_tag(text):
    """ Add closing tags for some of the recurring terms from the dictionary

    :param text str: text that has to be modify
    :returns: closing tags for some lines
    :rtype: str
    """

    if "<head>" in text:
        text = text.replace("\n", '</head>\n<opener>')
    if '<address rend="align(left)"><addrLine>' in text:
        text = text.replace("\n", "</addrLine></address>\n")
    if '<signed rend="align(right)"' in text:
        text = text.replace("\n", "</signed>\n")
    return text


linebreak = {
    '-\n': '<lb break="no"/>',
    ' \n': '<lb/> ',
    "'\n": "'<lb/>"
}

recurring_terms = {
    "SÉNAT": '<fw type="letterhead" place="align(left)" corresp="#entete-senat"><hi rend="underline">SÉNAT</hi></fw>',
    "LETTRE": "<head>LETTRE",
    "Mon cher Butler,": '<salute rend="indent">Mon cher Butler,</salute></opener><p rend="indent">',
    "à Monsieur le": '<address rend="align(left)"><addrLine>à Monsieur le',
    "Votre affectueusement dévoué": '<closer><signed rend="align(right)">Votre affectueusement dévoué',
    "D'Estournelles": '<signed rend="align(right)" hand="#annotation">D’Estournelles'
}


## ------ START OF THE SCRIPT ------ ##

for root, dirs, files in os.walk(sys.argv[1]):
    for filename in files:
        with open(sys.argv[1] + filename, 'r') as file_in:
            print("reading from "+sys.argv[1] + filename)
            f = file_in.read()
            f = f.replace("\n", "\n$")
            # This sign is added to help split the text afterwards while preserving the newlines.
            with open(sys.argv[2] + filename.replace(".txt", ".xml"), "w") as file_out:
                print("writing to "+sys.argv[2] + filename.replace(".txt", ".xml"))
                for text in f.split('$'):
                    text = text.replace("’", "'")
                    text = page_numbering(text)
                    for key, value in recurring_terms.items():
                        text = text.replace(key, value) 
                    text = closing_tag(text)
                    text = tagging_paragraph(text)
                    for key, value in linebreak.items():
                        text = text.replace(key, value)
                    if ">" not in text:
                        text = text.replace("\n","<lb/> ")
                        # This replacement is not put in the dictionnary because it needs to be made after all the others.
                        # This way, it ensures that only the forgotten end of line with no tags are encoded.
                    file_out.write(text)