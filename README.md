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

This repository contains three folders, each whith one or multiple XML or HTML files in it:


- The "Guidelines" folder contains the TEI documentation that will be used to encode our corpus documents. This documentation is available in XML and HTML. The folder itself has two subfolders :
  - The "out" folder contains the Relax NG transformation of the documentation, linked to the XML file(s) of the "Transcription" folder.
  - The "illustrations" folder contains pictures used to illustrate the use of some tags on the documentation. 
- The "Indexes" folder contains five indexes (persons, places, organizations, contributors and works) that will be link to our XML transcription files.
- The "Transcription" folder contains the XML encoding files of our corpus letters.
