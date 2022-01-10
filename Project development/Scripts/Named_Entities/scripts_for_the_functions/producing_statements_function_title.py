# -*- UTF-8 -*-

"""
- author: Floriane Chiffoleau
- date: January 2022
- description: Creating from a CSV a series of statements for titles for a Python function
- input: CSV file
- output: Python file
- usage :
    ======
    python name_of_this_script.py arg1
    arg1: csv of the titles
"""

import csv
import re
import sys

with open(sys.argv[1], 'r', encoding='UTF-8') as csvfile:
    print("reading from " + sys.argv[1])
    index = csv.DictReader(csvfile, delimiter=';')
    processed_text_as_list = []
    processed_encoding_as_list = []
    for row in index:
        header = list(row.keys())
        entity = row[header[0]]
        identifier = row[header[1]]

        regex = f"""
        {identifier} = re.compile(r"{entity}")
        """

        processed_text_as_list.append(regex)
        new_text = "".join(processed_text_as_list)
        #Remove unecessary spaces
        new_text = re.sub(r"\n +\n", "\n", new_text)

        #Change the type according to what you need
        encoding = f"""
        text = re.sub({identifier}, r'<title ref="#{identifier}" type="pec">\g<0></title>', text)
        """
        processed_encoding_as_list.append(encoding)
        new_encoding = "".join(processed_encoding_as_list)
        #Remove unecessary spaces
        new_encoding = re.sub(r"\n +\n", "\n", new_encoding)

with open(sys.argv[1].replace("csv", "py"), 'w', encoding='utf8') as file:
    file.write(new_text)
    file.write(new_encoding)
    print("creating " + sys.argv[1].replace("csv", "py"))
