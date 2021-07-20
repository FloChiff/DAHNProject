
# -*- UTF-8 -*-

"""
- author: Floriane Chiffoleau
- date: July 2021
- description: Writing the metadata to import a new file to NAKALA by using a CSV
- input: CSV files
- output: Python files
- usage :
    ======
    python name_of_this_script.py arg1 arg2
    arg1: name of the folder containing the CSV files
    arg2: name of the folder containing the Python files
"""

import csv
import os
import sys

for root, dirs, files in os.walk(sys.argv[1]):
    for filename in files:
        with open(sys.argv[1] + filename, 'r', encoding='UTF-8') as csvfile:
            print("reading from " + sys.argv[1] + filename)
            index = csv.DictReader(csvfile, delimiter=',')
            processed_text_as_list = []
            for row in index:
                header = list(row.keys())
                file = row[header[0]]
                title_fr = row[header[1]]
                title_en = row[header[2]]
                title_de = row[header[3]]
                genre = row[header[4]]
                author = row[header[5]]
                date = row[header[6]]
                languages = row[header[7]]
                topic = row[header[8]]
                rights_holder = row[header[9]]
                accessRights = row[header[10]]
                collection = row[header[11]]

                json = f""" {file} = {{
                "status": "published",
                    "metas": [
                        {{
                          "value": "{title_fr}",
                          "lang": "fr",
                          "typeUri": "http://www.w3.org/2001/XMLSchema#string",
                          "propertyUri": "http://nakala.fr/terms#title"
                        }},
                        {{
                          "value": "{title_en}",
                          "lang": "en",
                          "typeUri": "http://www.w3.org/2001/XMLSchema#string",
                          "propertyUri": "http://nakala.fr/terms#title"
                        }},
                        {{
                          "value": "{title_de}",
                          "lang": "de",
                          "typeUri": "http://www.w3.org/2001/XMLSchema#string",
                          "propertyUri": "http://nakala.fr/terms#title"
                        }},
                        {{
                          "value": "{date}",
                          "lang": null,
                          "typeUri": "http://www.w3.org/2001/XMLSchema#string",
                          "propertyUri": "http://nakala.fr/terms#created"
                        }},
                        {{
                          "value": "CC-BY-NC-ND-4.0",
                          "lang": null,
                          "typeUri": "http://www.w3.org/2001/XMLSchema#string",
                          "propertyUri": "http://nakala.fr/terms#license"
                        }},
                        {{
                          "value": "{genre}",
                          "lang": null,
                          "typeUri": "http://www.w3.org/2001/XMLSchema#anyURI",
                          "propertyUri": "http://nakala.fr/terms#type"
                        }},
                        {{
                          "value": "{topic}",
                          "lang": null,
                          "typeUri": "http://www.w3.org/2001/XMLSchema#string",
                          "propertyUri": "http://purl.org/dc/terms/subject"
                        }},
                        {{
                          "value": "Laurent Romary*Anne Baillot*Floriane Chiffoleau",
                          "lang": null,
                          "typeUri": null,
                          "propertyUri": "http://purl.org/dc/terms/contributor"
                        }},
                        {{
                          "value": "{languages}",
                          "lang": null,
                          "typeUri": "http://www.w3.org/2001/XMLSchema#string",
                          "propertyUri": "http://purl.org/dc/terms/language"
                        }},
                        {{
                          "value": "{accessRights}",
                          "lang": null,
                          "typeUri": null,
                          "propertyUri": "http://purl.org/dc/terms/accessRights"
                        }},
                        {{
                          "value": "{rights_holder}",
                          "lang": null,
                          "typeUri": null,
                          "propertyUri": "http://purl.org/dc/terms/rightsHolder"
                        }},
                        {{
                          "value": {{ {author}
                          }},
                          "propertyUri": "http://nakala.fr/terms#creator"
                        }}
                      ],
                      "files": [
                        {{
                          "sha1": "string"
                        }}
                      ],
                      "collectionsIds": [
                        "{collection}",
                        "10.34847/nkl.8479g2z4"
                      ],
                      "rights": [
                        {{
                          "id": "fd5b8766-d997-11eb-99d1-5254000a365d",
                          "role": "ROLE_ADMIN"
                        }}
                      ]
                    }}
                """
                processed_text_as_list.append(json)
                new_text = "".join(processed_text_as_list)

                #Replace the name of the author with all the identifier from NAKALA
                new_text = new_text.replace('"value": {{ August Boeckh', '"value": {{\n "givenname": "August",\n"surname": "Boeckh",\n"orcid": null,\n"authorId": "f8517f91-25e1-49b8-8560-60e6e36ffdec"')
                new_text = new_text.replace('"value": {{ Adelbert von Chamisso', '"value": {{\n "givenname": "Adelbert",\n"surname": "von Chamisso",\n"orcid": null,\n"authorId": "ca05bca8-73c3-4db5-896f-9aa3be30bc0f"')
                new_text = new_text.replace('"value": {{ Johann Albrecht Euler', '"value": {{\n "givenname": "Johann Albrecht",\n"surname": "Euler",\n"orcid": null,\n"authorId": "4d69045f-3cf9-4a3e-a72a-8509fc140787"')
                new_text = new_text.replace('"value": {{ Dorothea Tieck', '"value": {{\n "givenname": "Dorothea",\n "surname": "Tieck",\n "orcid": null,\n "authorId": "9d363964-5aeb-4ee7-adae-25b86058b4db"')
                new_text = new_text.replace('"value": {{ Ludwig Tieck', '"value": {{\n "givenname": "Ludwig",\n"surname": "Tieck",\n"orcid": null,\n "authorId": "460f3662-eb79-4849-a0c4-cc510d5ee6fc"')
                new_text = new_text.replace('"value": {{ Adolf von Buch', '"value": {{\n "givenname": "Adolf",\n"surname": "von Buch",\n"orcid": null,\n"authorId": "402c269b-2007-4531-8be0-bf02624f9c3a"')
                
                #Replace the characters used to make a valid file
                new_text = new_text.replace("*", "\\r\\n")
                
        with open(sys.argv[2] + filename.replace(".csv", ".py"), 'w', encoding='utf8') as file:
            file.write(new_text)
            print("creating " + sys.argv[2] + filename)