# How to do a transcription (with eScriptorium)

In the context of the DAHN project, we used eScriptorium, the interface created for the OCR software Kraken, to do the segmentation, transcription and post-OCR correction of our corpus. To do that correctly and easily, we develop many things (scripts, models, etc.) and established steps to follow.

1. Import images from your corpus on [eScriptorium](http://traces6.paris.inria.fr/)
2. Apply the segmentation model ([path](https://github.com/FloChiff/DAHNProject/blob/master/Project%20development/Training/Segmentation/models/modelsegpec_4717.mlmodel) to a model for typescript documents)
3. Correct the segmentation by checking the missing segmentation lines, non-considered start- and end-of-line and split lines
4. Apply the transcription model ([path](https://github.com/FloChiff/DAHNProject/blob/master/Project%20development/Training/Text%20Recognition/models/finetune_modelpec_9360_NFC.mlmodel) to a model for typescript documents written in French)
5. Correct again the segmentation by checking wrongly placed points and noise
6. *Optional step: if you want to keep the segmentation of your file (to keep track), you can, once it’s corrected, export it from eScriptorium (“Export; manual; Alto|PageXML”)*
7. Once again, apply the transcription model so that it consider the changes made in the segmentation
8. Export the transcription in your prefered XML format : ALTO (“Export; name-of-the-model; Alto”) or PAGE (“Export; name-of-the-model; Pagexml”)
9. Search wrongly transcribed and incorrect words in the exported XML files by using one of these scripts : for [ALTO](https://github.com/FloChiff/DAHNProject/blob/master/Project%20development/Scripts/Correction/spellcheck_texts_XMLALTO.py) or for [PAGE](https://github.com/FloChiff/DAHNProject/blob/master/Project%20development/Scripts/Correction/spellcheck_texts_PAGEXML.py)
(**Attention : the only dictionary available in the repository is for french texts. To work with other languages, you can download new dictionnaries [here](https://github.com/hermitdave/FrequencyWords) but you will have to transform the TEXT file in JSON.**)
10. Correct the produced dictionaries (one for each XML file) manually and by using the corresponding images
11. Integrate every dictionary in a single file entitled “dictionary” (as it is named in the next script)
12. Apply the corrections from the dictionary by using the corresponding [script](https://github.com/FloChiff/DAHNProject/blob/master/Project%20development/Scripts/Correction/text_correction_XML.py) for XML files
13. Correct manually the remaining errors in the text, like in step 10
14. Compress the folder content in a ZIP file
15. Import on eScriptorium the transcription from the ZIP file and with a clear name (example: “corrected_transcript”)
16. *Optional step: if you want the transcription in a text format, export it (“Export; name-of-the-imported-file; text”), which will produce a single file that contains the whole transcription.*
