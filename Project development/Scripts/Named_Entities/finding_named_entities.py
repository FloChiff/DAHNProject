# -*- UTF-8 -*-

"""
- author: Floriane Chiffoleau
- date: January 2022
- description: Retrieving the named entities from a corpus
- input : TXT files
- output: TXT file
- usage :
    ======
    python name_of_this_script.py arg1 arg2
    arg1: folder of the transcription in a text format
    arg2: text file with a list of entities with their label

"""

import os
import sys
import spacy
#Call as a Python package the french trained pipeline to use with spaCy
import fr_core_news_lg
nlp = spacy.load('fr_core_news_lg')

for root, dirs, files in os.walk(sys.argv[1]):
    for filename in files:
        with open(sys.argv[1] + filename, 'r') as file_in:
            file = file_in.read()
        processed_text_as_list = []
        doc = nlp(file)
        for ent in doc.ents:
            #text refers to the entity found and label to the type of entity
            text = "\"" + ent.text + " " + ent.label_ + "\",\t"
            processed_text_as_list.append(text)
        new_text = "".join(processed_text_as_list)

        with open(sys.argv[2], "a") as file_out:
            #Warning: the output file is in a "add" mode, which mean that it will add entities, file after file
            #If you need to redo this step and execute the script again, it will be better to delete the content of the file before
            file_out.write(new_text)
            print("currently writing the entities from " + filename)