# -*- UTF-8 -*-

"""
- author: Floriane Chiffoleau
- date: January 2022
- description: Creating from a CSV a list of titles for an XML index
- input: CSV file
- output: TXT file
- usage :
    ======
    python name_of_this_script.py arg1
    arg1: csv of the titles
"""

import csv
import sys

with open(sys.argv[1], 'r', encoding='UTF-8') as csvfile:
    print("reading from " + sys.argv[1])
    index = csv.DictReader(csvfile, delimiter=';')
    processed_text_as_list = []
    for row in index:
        header = list(row.keys())
        entity = row[header[0]]
        identifier = row[header[1]]

        text = f"""
        <biblStruct xml:id="{identifier}">
                    <monogr>
                        <title level="">{entity}</title>
                        <imprint>
                            <pubPlace/>
                            <date/>
                        </imprint>
                    </monogr>
                </biblStruct>
        """

        processed_text_as_list.append(text)
        new_text = "".join(processed_text_as_list)

with open(sys.argv[1].replace("csv", "txt"), 'w', encoding='utf8') as file:
    file.write(new_text)
    print("creating " + sys.argv[1].replace("csv", "txt"))
