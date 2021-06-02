# DAHN Project: Digital Edition of historical manuscripts

## Structure of the repository

- Correspondence
  - Berlin Intellectuals
    - Corpus
    - Indexes
  - Guidelines
  - Paul d'Estournelles de Constant
    - Corpus
    - Indexes
- Project Development
  - Documentation
  - Scripts
    - Correction
    - Encoding
    - Modification
    - Transcription
  - Training
    - Ground Truth
    - Segmentation
      - Logs
      - Models
    - Text Recognition
      - Logs
      - Models
- .gitignore
- README.md

##  Presentation of the project

The DAHN project is a project between the University of Le Mans, the EHESS and INRIA, and with the partnership of the Ministry of Higher Education, Research and Innovation. Its goal is to create a program for digital scientific edition of corpus of letter exchanges, with, as a basis, the correspondence of Paul d’Estournelles de Constant, senator of Sarthe and 1909 Nobel Peace Prize. The work is to be made in two steps : first, refreshing an already existing numeric environment to let in that new edition. Then, adding the correspondence of d’Estournelles, while documenting the methodology and the actions made. The first editorial platform (from [Lettres et Textes](https://www.berliner-intellektuelle.eu)) was first developed between 2010 and 2016 and enabled the creation of a data model that combines genetic edition and named entities network. Though on a precise subject, it was thought to be a generic tool that allows transverse research on egodocuments and printed corpus, from every modern or contemporary period and in all imaginable European situations on those periods.

## Content of the repository

This repository contains files related to the development of the DAHN project and the corpus attached to it.

### Correspondence
This folder contains the two main corpus of our project: 
- the **correspondence of Paul d'Estournelles de Constant**, study corpus for the development of our program for digital scientific edition of corpus, with the transcription of the letters and the indexes attached to it.
- the **correspondence of Berlin intellectuals**, with transcriptions updated to fit the new version of the TEI Guidelines and corrected indexes, that follows what is established on the encoding guidelines.

Finally, the folder also contains encoding guidelines, developed according to the TEI Guidelines and what has be done for the two previously mentioned corpus. Those encoding guidelines are specific to egodocuments and it provides precision sometimes not given in the TEI Guidelines and choices made for the encoding. Those guidelines present both header and body, as well as indexes and specific parts of the encoding (dates, named entities, substitutions, etc.)

The guidelines are available in three formats: XML, HTML and PDF. 

### Project development
This folder contains three elements, essential for the development of the project.

#### Training
Before intiating the transcription of the corpus, it was important to develop models, first for the segmentation of the images, then for the transcription.
By using the OCR software Kraken, through its interface eScriptorium, we developed ground truth that were later used to train models. 
This folder contains those ground truth, the models subsequently developed for the segmentation and the transcription of our corpus (Paul d'Estournelles), as well as their report logs.

#### Scripts
With the DAHN project, we aim to create a program for the digital scientific edition of corpus. To do so, we have to follow several steps and some of them requires Python script to effectively work.
In here, there are scripts for three parts of the program: transcription, post-processing and encoding. 
For the transcription, there is a script to transcribe with Kraken by using a command line, instead of the eScriptorium interface.
For post-processing, there are scripts to help correcting the text after ocerisation. There is two types of scripts: one that search errors and one that correct them. The scripts are available for XML types files (PAGE and ALTO) and TEXT files.
Finally, for encoding, there are three scripts: one to encode metadata, one to encode texts and one to correct recurring errors due to the previously mentioned script.
There also is a fourth folder : modification. This one does not contain files linked directly to the program of the digital edition of corpus but is related to the edition. This folder contains scripts for the update and transformation of already TEI XML encoded files (transcriptions, indexes) that must be added to the last part of the program : the publication.

#### Documentation
There are many elements in the *Project development* folder that requires help to use it correctly and easily. 
We then provide documentation for the most obscure part, in order to favorise the reuse of what we developed, without having to decipher it beforehand. 
Thus, there are documentation for the process of segmentation/transcription/post-processing, as well as explanation for running the scripts.
