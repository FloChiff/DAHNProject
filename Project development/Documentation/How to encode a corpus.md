# How to encode a corpus

In the context of the DAHN project, few steps have been put in place to quickly encode a corpus of multiple files.
Some parts have to be made manually, but most of the encoding will be done automatically, which represents a huge time saver.

1. Encoding of the metadata with a script and a CSV file

    When encoding a corpus, there are usually many elements similar for several files or even for all: the corpus is kept in the same institution, it is encoded for a unique project, the editorial rules are the same for all, etc.
    In order not to encode those informations one by one, this [Python script](https://github.com/FloChiff/DAHNProject/blob/master/Project%20development/Scripts/Encoding/encoding_files.py) allows you to do a template for the encoding of your metadata and to fill a CSV with the informations you have on your corpus so that it fills every header in one shot, while creating your XML files.
    The case study for this repository is a correspondence, so the [CSV](https://github.com/FloChiff/DAHNProject/blob/master/Project%20development/Scripts/Encoding/metadata/correspondence_metadata.csv) contains informations such as letter numbering, dates in many langages or pages for each letter. 
    
    However, as it is visible in the template, not every information can be completed by the CSV so the rest will have to be filled in the final step, when proofreading your encoding.
    
1. Encoding of the body with a script and regular expression

    In parallel, while you create your TEI XML metadata-encoded files, you can also generate the encoding of your texts. 
    To do so, you can use the [text_tagging script](https://github.com/FloChiff/DAHNProject/blob/master/Project%20development/Scripts/Encoding/text_tagging.py), created to generally encode a text, while also encoding precise parts of texts.
    To know more on how to use this script, see the [documentation](https://github.com/FloChiff/DAHNProject/blob/master/Project%20development/Documentation/Documentation%20for%20the%20text_tagging%20script.ipynb) written for it.

1. Merge of the two files

    With the first step, you create a TEI XML file with no content in the body and with the second, you create a XML file with no TEI structure. Now, you just need to join them by copying/pasting the content of the XML file with the text encoded in the `body` tag of the TEI XML file created in the first step.

1. Corrections of recurring errors with a script

    After several executions of the previous script, few recurring errors start to appear because of the way the script works. A [correction script](https://github.com/FloChiff/DAHNProject/blob/master/Project%20development/Scripts/Encoding/correcting_recurrent_errors.py) has been written to automatically correct those errors rather than having to do it manually.
    It also encodes new information that need the combination of metadata and text content to be added.
    It also adds a new `change` tag with the date corresponding to the execution of the script (because added in the command line, via the content of the script). 
    
    This script has been written after encountering recurring errors in the encoding of the study corpus but it is not a mandatory step. However, some part of it, like the numbering of the `pb` or the encoding of the `change` tag can be useful. 
    It also can be adapted to your own need and your own recurring errors, whether you need find/replace changes or search in an XML tree corrections.

1. Proofreading and manual encoding of the rest of the documents

    Once all the scripts have been executed and the text is encoded according to what was automatically defined, it is essential to proofread the encoding, to be sure that there are no misplaced tags, errors in the encoding or some other kind of problems. 
    It will also be necessary to encode manually the rest of the documents, since not all tags can be added manually and some parts need precise human work to be correctly encoded.
