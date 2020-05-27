# -*- UTF-8 -*-

"""
- author: Floriane Chiffoleau
- date: May 2020
- description: Encoding a corpus with some basic XML tags
- input: plain text
- output: tagged text
"""

import sys
import re

def non_indented_paragraph(text):
    """ Add paragraph tag in a text when it is not indented
    
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


def indented_paragraph(text):
    """ Add paragraph tag in a text when it is indented
    
    :param text str: text that has to be modify
    :returns: text encoded with paragraph tags
    :rtype: str
    """

    if "<" not in text[:10]:
       text = text.replace('\t', '<p rend="indent">')
    else:
       text = text.replace('\t', '')
    # Some lines with tabulation in the text have already been tagged
    # So it's important to not double-tagged them while also suppressing this tabulation 

    punctuation = "!\"»?."
    # This variable contains all the punctuation signs that indicates a phrase ending
    # and a need for an ending paragraph tag

    for sign in punctuation:
        text = text.replace(sign + "\n", sign + "</p>")
        text = text.replace(sign + " \n", sign + "</p>")
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

recurring_terms = {
    "LETTRE": "<head>LETTRE",
    "SÉNAT": '<fw type="letterhead" place="align(left)" corresp="#entete-senat"><hi rend="underline">SÉNAT</hi></fw>',
    "PARIS,": '<dateline rend="align(right)"><placeName>PARIS</placeName>, <date when-iso="">',
    "LE MANS,": '<dateline rend="align(right)"><placeName>LE MANS</placeName>, <date when-iso="">',
    "Mon cher Butler,": '<salute rend="indent">Mon cher Butler,</salute></opener>',
    "à Monsieur le Président Nicholas Murray BUTLER.": '<note rend="align(left)"><address><addrLine>à Monsieur le Président Nicholas Murray BUTLER.</addrLine></address></note>',
    "à Monsieur le Président N. Murray BUTLER.": '<note rend="align(left)"><address><addrLine>à Monsieur le Président N. Murray BUTLER.</addrLine></address></note>',
    "à Monsieur le Président N.Murray BUTLER.": '<note rend="align(left)"><address><addrLine>à Monsieur le Président N.Murray BUTLER.</addrLine></address></note>',
    "à Monsieur le Président Nicholas Murray BUTLER,": '<address rend="align(left)"><addrLine>à Monsieur le Président Nicholas Murray BUTLER,</addrLine>',
    "à Monsieur le Président N. Murray BUTLER,": '<address rend="align(left)"><addrLine>à Monsieur le Président N. Murray BUTLER,</addrLine>',
    "à Monsieur le Président N.Murray BUTLER,": '<address rend="align(left)"><addrLine>à Monsieur le Président N.Murray BUTLER,</addrLine>',
    "NEW-YORK.": "<addrLine>NEW-YORK.</addrLine></address></closer>",
    "Votre affectueusement dévoué,": '<closer><signed rend="align(right)">Votre affectueusement dévoué,</signed>',
    "D'Estournelles de Constant": '<signed rend="align(right)" hand="#annotation">D’Estournelles de Constant</signed>'
}


linebreak = {
    '-\n': '<lb break="no"/>',
    ' \n': '<lb/> ',
    "'\n": "'<lb/>"
}

## ------ START OF THE SCRIPT ------ ##


with open(sys.argv[1], 'r') as file_in:
    print("reading from "+sys.argv[1])
    f = file_in.read()
    f = f.replace("\n\n", "\n")
    f = f.replace("\n", "\n£")
    # This sign is added to help split the text afterwards while preserving the newlines.
    with open(sys.argv[2], "w") as file_out:
        for text in f.split('£'):
            text = text.replace("’", "'")
            text = page_numbering(text)
            for key, value in recurring_terms.items():
                text = text.replace(key, value)      
            if "<head>" in text:
                text = text.replace(".\n", '.</head>\n<opener>')
            if '<dateline' in text:
                text = text.replace(".", '.</date></dateline>')
            #text = non_indented_paragraph(text)
            text = indented_paragraph(text)
            # Apply one function or the other according to the structure of the submitted text
            for key, value in linebreak.items():
                text = text.replace(key, value)
            if ">" not in text:
                text = text.replace("\n","<lb/> ")
                # This replacement is not put in the dictionnary because it needs to be made after all the others.
                # This way, it ensures that only the forgotten end of line with no tags are encoded.
            file_out.write(text)
        print("writing to "+sys.argv[2])

