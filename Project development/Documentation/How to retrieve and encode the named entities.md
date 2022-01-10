# How to retrieve and encode the named entities

In order to have a corpus thoroughly encoded, it is important to also work on the named entities (NE) of the corpus. This can be an arduous task, especially with a pretty long source material. To help with that, I created several scripts, to ease the harvesting and encoding of the NE of the corpus.

Requirements:
- Transcriptions in a text format
- TEI XML encoded files
- The Python library [spaCy](https://spacy.io)

__1. Retrieve the NE from the texts with a basic model__  
The first step is entirely automatic, since the [script](https://github.com/FloChiff/DAHNProject/blob/master/Project%20development/Scripts/Named_Entities/finding_named_entities.py) will be doing everything you need (i.e. retrieving the entities). For our case work, we are working with a french corpus so the script will be calling the french trained pipelines but spaCy also have many more languages [models](https://spacy.io/models) to work with. For the script, it is only necessary to call the folder where the corpus is (a text format can be preferable because a raw text made the harvesting easier) and to give a name to the output file.

__2. Clean the resulting files__  
This is probably the longest task because it requires to go several times from one file to another and to correct a lot manually.

_1.Clean the output file of the first script_  
The first script have produced an output file that need to be slightly corrected, in order to move on to the next step. Those corrections can be made automatically by using regex in the find/replace tool of the text editor:
- Replace \n (newline) by a space (Supress the breaklines present in some NE retrieved by spaCy)
- Replace \t (tab) by \n (newline) (Process to separate by newlines each entity of the file; it can take a certain time if there is a lot of entities)
- Search the following regex `[^,]\n` (See if there are still breaklines inside an entity itself)
- Replace `"- ` by `"` (Preprocessing before the import in the spreadsheet)

_2.Remove the duplicates from the output file_  
Once those correction are made, it is possible to copy/paste the content of the file in the list `text` of the script [removing_duplicates.py](https://github.com/FloChiff/DAHNProject/blob/master/Project%20development/Scripts/Named_Entities/removing_duplicates.py). It is possible that there is still some errors, mostly due to air quotes that can have been harvested in a named entity, which will create an error when executing the script (some text editor will highlight it for you in the Python file to correct it before executing the script). After executing the script, the number of entities in the file will normally be largely shorten (ours was divided by three), since many entities would have been written and labeled the same from one file to another.

_3.Sort and clean the output file thoroughly_  
To correct more easily and with some help the output file, we will copy/paste it in a spreadsheet (we are using Microsoft Office Excel but most of the steps also work with LibreOffice Calc).
In the previous script, we replace the space before the label by a tabulation, which is a way to create two columns in the spreadsheet. This separated the entity from the label, which will help sort and clean the file.

There are several ways to quickly suppress incorrect harvested entities:
- Sort alphabetically the entities to supress dates or others things not meant to be an entity
- Sort alphabetically the labels and see notably the "MISC" and its content
- Use the highlighting of cells to highlight duplicate value and see if there are some that are duplicate but with different label (Excel can group all the highlighted cells together, which makes it easier to suppress them or not, even though it is not case sensitive so some might looks similar but are not. Calc can't group the hilighted cells but is case sensitive so the only cells colored will be the one with different label and not different ways to write it).

Attention : in Excel, if you still have duplicates, do not use Data/Table Tools/Remove duplicates because it is not case sensitive and it will consider that "PAUL" and "Paul" are equivalent even though it is not written the same way.

Finally, you will surely have to read the spreadsheet entry by entry to eliminate the remaining errors in the identification of NE.

After cleaning our output file, we went from 7000 entities to about 2500 and now, we will have to do the last "cleaning" of the file, by pooling a large part of the entities.

__3. Pool the different forms of a same entity__  
This step might be the most difficult part, especially if you are not familiar with regular expressions (Here is a website that can help [https://regexr.com/](https://regexr.com/))

Once the output file has been cleaned, it can be practical to separate the file by tab (one tab = one label) in order to work with the entities more easely.
To help with the encoding that will be made afterwards, it can be useful to regroup the various forms of a singular entity by using regular expressions.
For example, in our corpus, one city has been written in six different forms : 
- Clermont Créans
- Clermont-Créans
- CLERMONT-CRÉANS
- Clérmont-Créans
- Créans
- CRÉANS

To make sure that all of thoses cases are encoded in our corpus, we can use the following regex:  
"((c|C)(l(e|é)rmont|LERMONT)(-| ))?C(réans|R(É|E)ANS)"

Sometimes, it can be difficult to quickly find all the forms of one entity, due to a pronoun, determinant, first name, etc., in front of the main part of the entity, notably with the persons, where it can be found at one point of the alphabet with the first letter of the surname and at another point, further down, with the first letter of the first name (For example, "Caillaux" would be at the "C" but also at the "J" with "Joseph Caillaux"). To help in this situation, I recommand a little pre-processing of the entities, by putting all of the elements mentioned earlier at the end of the main part of the entity in parenthesis.
Example:
- "Joseph Caillaux" --> "Caillaux (Joseph )"
- "J. Caillaux" --> "Caillaux (J. )"
- "J.Caillaux" --> "Caillaux (J.)"

That way, all the forms of Caillaux would be at the letter "C", next to each other, which will help to pool the various writings in a regular expression.

Warning: it is important to be attentive of what will be suggested as an entity to encode because if it is something that is commonly found in a text, the regex will encode it even if it is not what we are looking for.
For example, a city like "Pau" will be a problem because all of the "Paul" in the text will be encoded with it. In those cases, it can be better to leave it behind and encode it manually or be prepared to verify all of the instances of the entity to see if it is needed to keep or remove them.

Once all the entities are ready, the next step is to give them an identifier. The easiest way is to start the spreadsheet with `"letter for the entity" + 0001` and to just extend it to the last entity (p0001 for person, l0001 for location, etc.).

__4. Create the statements for the script and add the entities in their respective index__  
This new step requires to create CSV files of the entities (one for each label) and their identifiers (see for example the [CSV](https://github.com/FloChiff/DAHNProject/tree/master/Project%20development/Scripts/Named_Entities/csv_of_the_entities) of d'Estournelles corpus).
Then, we will have two sets of scripts to execute:
- [one set](https://github.com/FloChiff/DAHNProject/tree/master/Project%20development/Scripts/Named_Entities/scripts_for_the_functions) will create the series of statements that will encode the entities in the corpus
- [one set](https://github.com/FloChiff/DAHNProject/tree/master/Project%20development/Scripts/Named_Entities/scripts_for_the_indexes) will create the entries and tags for the entity in the index

Each set contains four scripts, one for each type of entity (person, place, organization, title). They don't differ very much from one another; it is usually the content of the tag for the encoding (index or corpus) that changes.
Executing those scripts is pretty simple because the CSV is the only element required in the command line (the output file will be named like the CSV; only the extension changes, with Python for the statements and TXT for the index).

The output of the scripts for the index will have to be copy/paste inside the indexes that have been or will be created for the exploited corpus.

The output of the scripts for the statements will have to be copy/paste inside the function created for the last script and called in the module importation.

__5. Apply the NE encoding script to the corpus__  
Finally, once we have all our NE, inside their own functions and our corpus of XML files, we can add them to the encoding, by applying the script [encoding_named_entities.py](https://github.com/FloChiff/DAHNProject/blob/master/Project%20development/Scripts/Named_Entities/encoding_named_entities.py). It will read the XML file, recreate it, add a new line to the revisionDesc and add the NE in the encoding of the body.

The script have been developed by taken into account the fact that the corpus has already been encoded but it is still possible to use only part of it at the same time of the general encoding of the corpus. In the [text_tagging](https://github.com/FloChiff/DAHNProject/blob/master/Project%20development/Scripts/Encoding/text_tagging.py) script, it is possible to add the functions in the module importation and the following snippet of code after the line `text = text.replace("€", "")` (line 114):
`text = persName(text)`  
`text = placeName(text)`  
`text = title(text)`  
`text = orgName(text)`

__6. Manually correct the errors that could have been created during the encoding__  
After encoding the NE, it is possible that there are still some errors or oversights, that will need to be corrected. 
Here are few examples of what you may encounter:
- During the pooling of the same entity, it is possible that two different NE have been grouped together, as it would have been of the only way to encode it (For example "Tunis(ie)?" that can be "Tunis" or "Tunisie" and "S(énat|ÉNAT|ENAT)( (a|A)méricain)?" that can be the "Sénat" (french) or the "Sénat Américain"). To do that, we choose to remove the identifier in the @ref and now, all the identifier linked to that are missing and need to be added (I created a [script](https://github.com/FloChiff/DAHNProject/blob/master/Project%20development/Scripts/Named_Entities/retrieving_unreferenced_named_entities.py) to recover quicker all the empty @ref in the corpus)
- In an opposite way, sometimes, it is possible to encode the same entity with two distinct identifiers, because the writing was wrong or the second first name looked like a surname, etc.. In that case, it will be needed to choose a unique identifier (usually the one most encoded), delete the second entry in the index and change the wrong one for the one chosen. 
- As it can be difficult to know exactly if an entity is relevant or not, it is possible to find, during the research of information for the indexes, that some thing encoded as a NE with an identifier is completly wrong and does not belong in the index. In that case, it is necessary to remove it from the index and delete its presence in the corpus.
- Because of an XML tag added inside the NE (in the case where you encoded the NE after doing the general encoding), the NE could have been encoded but only partially (because it recognized part of the regex). It will be better, for the quality of the corpus, to fix that and extend the NE to its full form.
