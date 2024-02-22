# -*- UTF-8 -*-

"""
- author: Floriane Chiffoleau
- date: October 2022
- description: Encoding a corpus with some basic XML tags
- input: XML ALTO files
- output: An XML file with tagged text
- usage :
    python encoding_texts_from_alto.py arg1 arg2

    arg1: directory storing all XML ALTO files to be processed
    arg2: XML file containing the tagged version of the transcription

"""

import os
import re
import sys

from bs4 import BeautifulSoup
from function_persName import persName
from function_placeName import placeName
from function_orgName import orgName
from function_title import titleName


LINEBREAK = {
    '-\n': '-<lb break="no"/>',
    ' \n': '<lb/> ',
    "'\n": "'<lb/>"
}

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

def tagging_regex(text):
    """Apply tags to the regex
    :param text str: text that has to be modify
    :returns: text encoded with the right tags for the regex
    :rtype: str
    """

    #This series of statements contains regex of recurrent terms from the corpus
    image_title = re.compile(r'FRAD072_12J([0-9]+)_lettre1([0-9]+)(_annexe([0-9]+))?_([0-9]+).jpg')
    writingplace = re.compile(r'££Molitor££')
    letter = re.compile(r'^(Annexe à ma )?L(ETTRE N|ettre n)° ?1.?[0-9]+ ?.?')
    senate = re.compile(r'^S((E|É)NAT|énat)')
    status = re.compile(r'^P(ersonnelle|ERSONNELLE)')
    dateline = re.compile(r'^[A-Za-zÀ-ÖØ-öø-ÿ-]+(( |-)[A-Za-zÀ-ÖØ-öø-ÿ-]+)?, (le )?[0-9]* [A-Za-zÀ-ÖØ-öø-ÿ-]+ 19[1-2][0-9] ?.?')
    salute = re.compile(r'^Mon cher Butler ?,')
    page_numbering = re.compile(r'- ?[0-9]* ?-')
    address = re.compile(r'^(à )?Monsieur le Président N(.)?(icholas)? ?Murray BUTLER(.|,)?')
    addrline = re.compile(r'^(à )?(NEW) ?(-| )? ?(YORK).?$')
    signature = re.compile(r'^Votre [A-Za-zÀ-ÖØ-öø-ÿ-]+ dévoué.?')
    signature2 = re.compile(r'^(A|a)ffectueusement (à vous|votre),?')
    name = re.compile(r"(D|d)'E(stournelles|STOURNELLES)( de C(onstant|ONSTANT))? ?.?")
    annexe = re.compile(r'^[0-9]* ?(A|a)nnexe(s)?.?')
    steps = re.compile(r'^([0-9]*|[A-Z]*)°')
    handnote = re.compile(r'££.+££')
    strikethrough = re.compile(r'(x|X){2,}')
    deletion = re.compile(r'€[A-Za-zÀ-ÖØ-öø-ÿ-]*€')
    postscript = re.compile(r'^P. ?S(.|,)-?')

    #This series of statements contains the encoding for the declared recurrent terms from the corpus
    text = re.sub(image_title, r'\n<pb facs="\g<0>" n=""/>', text)
    text = re.sub(writingplace, r'<note place="top(left)" hand="#annotation"><placeName ref="#l0005">\g<0></placeName></note>', text)
    text = re.sub(letter, r'<head rend="center underline">\g<0></head><opener>', text)
    text = re.sub(senate, r'<fw type="letterhead" place="margin" corresp="#lh-senat"><hi rend="underline">\g<0></hi></fw>', text)
    text = re.sub(status, r'<fw place="align(left)"><hi rend="underline">\g<0></hi></fw>', text)
    text = re.sub(dateline, r'<dateline rend="align(right)">\g<0></dateline>\n<title rend="align(center)">', text)
    text = re.sub(salute, r'</title>\n<salute rend="indent">\g<0></salute></opener><p rend="indent">', text)
    text = re.sub(page_numbering, r'<note type="foliation" place="top">\g<0></note>',text)
    text = re.sub(address, r'<address><addrLine rend="margin">\g<0></addrLine>', text)
    text = re.sub(addrline, r'<addrLine rend="indent"><hi rend="underline">\g<0></hi></addrLine></address>', text)
    text = re.sub(signature, r'<closer><signed rend="align(right)">\g<0></signed>', text)
    text = re.sub(signature2, r'<closer><signed rend="align(right)">\g<0></signed>', text)
    text = re.sub(name, r'<signed rend="align(right)" hand="#annotation">\g<0></signed>', text)
    text = re.sub(annexe, r'<postscript><p rend="bottom">\g<0></p></postscript>', text)
    text = re.sub(steps, r'<p rend="indent">\g<0>', text)
    text = re.sub(handnote, r'<add hand="#annotation">\g<0></add>', text)
    text = re.sub(strikethrough, r'<del rend="strikethrough">\g<0></del>', text)
    text = re.sub(deletion, r'<del rend="strikethrough">\g<0></del>', text)
    text = re.sub(postscript, r'<postscript><label>\g<0></label><p rend="indent">', text)
    return text

processed_transcription_as_list = []
for root, dirs, files in os.walk(sys.argv[1]):
    for filename in sorted(files):
        input_file = sys.argv[1] + filename
        with open(input_file, 'r') as fh_page:
            print(f"Processing {input_file}".replace("/Users/fchiffol/Documents/Projet_DAHN/Process_steps/Transcriptions/", ""))
            soup_page = BeautifulSoup(fh_page, "xml")
            # Looking for the sourceDoc in the transformed page xml
            title = soup_page.find('fileName').string + '\n'
            processed_transcription_as_list.append(title)
            # Looking for the transcription in the transformed page xml
            for transcription in soup_page.findAll("String"):
                content = transcription["CONTENT"] + '\n'
                processed_transcription_as_list.append(content)
file = "".join(processed_transcription_as_list)
file = file.replace("\n", "\n$")
#This sign is added to help split the text afterwards while preserving the newlines.
processed_text_as_list = []
text_as_list = file.split('$')
for text in text_as_list:
    text = text.replace("’", "'")
    text = tagging_regex(text)
    text = tagging_paragraph(text)
    for key, value in LINEBREAK.items():
        text = text.replace(key, value)
    if ">" not in text:
        text = text.replace("\n","<lb/> ")  
    text = text.replace("£", "")
    text = text.replace("€", "")
    #Suppress the two signs that are used in the transcription to signify deletion and handwritten text
    text = persName(text)
    text = placeName(text)
    text = titleName(text)
    text = orgName(text)
    processed_text_as_list.append(text)
new_text = "".join(processed_text_as_list)

with open(sys.argv[2], "w") as file_out:
    print(f"Writing in {sys.argv[2]}")
    file_out.write(new_text)