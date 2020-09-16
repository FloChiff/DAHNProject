# DAHN Project

## Digital Edition of historical manuscripts (correspondences)

The DAHN project is a project between the University of the Mans, the EHESS and INRIA, and with the partnership of the Ministry
                        of Higher Education, Research and Innovation. Its goal is to create a program for digital scientific edition of corpus of
                        letter exchanges, with, as a basis, the correspondence of Paul d’Estournelles de Constant, senator of Sarthe and 1909 Nobel
                        Peace Prize. The work is to be made in two steps : first, refreshing an already existing numeric environment to let in that
                        new edition. Then, adding the correspondence of d’Estournelles, while documenting the methodology and the actions made. The
                        first editorial platform (from [Lettres et Textes](https://www.berliner-intellektuelle.eu)) was first
                        developed between 2010 and 2016 and enabled the creation of a data model that combines genetic edition and named entities
                        network. Though on a precise subject, it was thought to be a generic tool that allows transverse research on egodocuments and
                        printed corpus, from every modern or contemporary period and in all imaginable European situations on those periods.

## Content of the repository

This repository contains all the files related to the DAHN Project and the correspondance of Paul d’Estournelles de Constant.

It is divided into two folders:
- **Correspondence**: it contains all the files related to the corpus (guidelines, indexes and corpus)
- **Project development**: it contains all the files involved in the evolution and the realization of the project (scripts, models, etc.). The training files are put into specific folders, depending on whether they are for segmentation or transcription. The scripts are indexed according to the part of the process they belong to : correction, encoding or transcription.

## How to do a transcription

1. Import images from your corpus on [eScriptorium](http://lectaurep.paris.inria.fr/)
2. Apply the segmentation model ([path](https://github.com/FloChiff/DAHNProject/blob/master/Project%20development/Training/Segmentation/models/modelsegpec_4717.mlmodel) to a model for typescript documents)
3. Correct the segmentation by checking the missing segmentation lines, non-considered start- and end-of-line and split lines
4. Apply the transcription model ([path](https://github.com/FloChiff/DAHNProject/blob/master/Project%20development/Training/Text%20Recognition/models/modelpec_9290_NFC.mlmodel) to a model for documents written by typewriter in French)
5. Correct again the segmentation by checking wrongly placed points and noise
6. Optional step: if you want to keep the segmentation of your file (to keep track), you can, once it’s corrected, export it from eScriptorium (“Export; manual; Alto”)
7. Once again, apply the transcription model so that it consider the changes made in the segmentation
8. Export the transcription in ALTO (“Export; name-of-the-model; Alto”)
9. Search wrongly transcribed and incorrect words in the exported ALTO files by using the following [script](https://github.com/FloChiff/DAHNProject/blob/master/Project%20development/Scripts/Correction/spellcheck_texts.py)
10. Correct manually and by using the corresponding images the produced dictionaries (one for each ALTO file)
11. Integrate every dictionary in a single file entitled “dictionary” (as it is named in the next script)
12. Apply the corrections from the dictionary by using the corresponding [script](https://github.com/FloChiff/DAHNProject/blob/master/Project%20development/Scripts/Correction/text_correction.py) 
13. Correct manually the remaining errors in the text, by using the corresponding images like before
14. Compress the folder content in a ZIP file
15. Import on eScriptorium the transcription from the ZIP file and with a clear name (example: “corrected-transcript”)
16. Optional step: if you want the transcription in a text format, export it (“Export; name-of-the-imported-file; text”), which will produce a single file that contains the whole transcription.