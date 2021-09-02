# How to add IIIF links to XML files

In the context of the DAHN project, we decide, for the digitization phase, to use a IIIF server to host our images. We decided on NAKALA, a tool developed by Huma Num that we already used to store some of our datas and that will be used to deploy our web application.  
The Berlin intellectuals' corpus already have images in JPG or TIFF format, referenced in the @facs attribute, but they are only available locally, so we have to add them to NAKALA.   
Here, I will explain the differents steps I've taken to add those images in NAKALA with the right data and then, to add the new links in the XML files.

Requirements:
- NAKALA account (via Huma Num)
- TEI XML encoded files
- Images (jpg, tif, etc.)  


__1. Retrieve metadata from XML files to insert them in a CSV file__

In NAKALA, it is necessary to provide metadata with the images imported (author, title, license, type, date and optionally more). Those information can easily be retrieved from the XML files in which the images are used. For our metadata, we chose eights elements, the content of which changes from one file to the other:
- Title (english, french and deutsch)
- Author
- Date
- Type (= "genre" in the XML)
- Language(s)
- Topic(s)
- Rights holder
- Access rights

They also are two other metadata required in our importation but they are always the same : license (CC-BY-NC-ND-4.0) and contributor (the members of the project)

To extract those data, I am using a [Python script](https://github.com/FloChiff/DAHNProject/blob/master/Project%20development/Scripts/Digitization/extract_metadata_from_files.py), that will print in the terminal all the information demanded, separated from one file to the others by brackets and between each metadata with a specific symbol ($$). Then, all I have to do is retrieve the content in the terminal, put it in a CSV file and transform the symbols into quotation marks and/or commas or semicolons to have a valid CSV file.

Once it is created, you also have to add the collection in which the data will be inserted. In our case, to ease our work with a good classification, we did one CSV for each author (containing 15 to 50 files), so a collection for each author.


__2. Fill the metadata following the model given by NAKALA__

Once the CSV are created, we can use it to fill the metadata that will accompanied the import of the images into NAKALA. To do so, I use a [script](https://github.com/FloChiff/DAHNProject/blob/master/Project%20development/Scripts/Digitization/writing_nakala_metadata.py) that extracts the information from the CSV according to the columns and then fill the model for NAKALA metadata using f-strings. 
It will produce a Python file containing all the metadata from the CSV, filled in its corresponding key and separated by braces {} and filename (usually the filename relates to the file in which the metadata has been extracted).

__3. Import the image(s) with the correspondant metadata__

The next step is to import the image(s) and its metadata in [NAKALA](https://nakala.fr). To do so, I am using the [API](https://api.nakala.fr/doc), by adding one of the images from the XML file in "POST:/datas/uploads". Then, I retrieve the identifier given in "sha1". I copy/paste it in the metadata part dedicated to it: "files/sha1". Finally, I copy/paste all the metadata of the file in "POST:/datas" and execute it, until I have a 201 code ("Created"). Then, if the file have more than one picture, I can add it by using "POST:/datas/{identifier}/files" in the API or by using the interface (easier if there are many files to add at once).

__4. Modify XML files with a Python dictionary containing the old and new @facs ID__

The last step will consist of collecting the new facs ID to change it in the XML files. To do so easily, I will be using the authors collections we stored the images in. In our case, some images, from one author to the other, have the same name, like "00000002.jpg" will be find in two different authors. Because of this, it will be not useful to collect all the images at once (as we can do because there are all part of the same collection "Berlin intellectual's papers") so we will retrieve them, author collection by author collection. We do it by using the API with "GET:/collections/{identifier}/datas". Once we have all the images, we can clean the file(s), first with a [Python script of regex](https://github.com/FloChiff/DAHNProject/blob/master/Project%20development/Scripts/Digitization/clean_metadata_files.py) that I wrote and second with some manual correction, to only have the old @facs ID and their new one as key and value of a Python dictionary. Finally, using a find/replace [script](https://github.com/FloChiff/DAHNProject/blob/master/Project%20development/Scripts/Digitization/changed_facs_to_iiif.py) I wrote and the dictionary, we can change the @facs in the XML files.
