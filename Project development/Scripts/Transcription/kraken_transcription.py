# -*- UTF-8 -*-

"""
- author: Floriane Chiffoleau
- date: May 2020
- description: Image transcription using kraken and a transcription model 
(it is recommended to have previously created a kraken environment and to activate it to run the command)
- input: images
- output: transcribed texts
"""

import os
import subprocess
import sys

images = sys.argv[1]
file = os.listdir(images)
texts = sys.argv[2]

for img in file:
    complete_path = f"{images}/{img}"
    output = f"{texts}/{img.replace('.JPG', '.txt')}"
    subprocess.run(["kraken", "-i", complete_path, output, "binarize", "segment", "ocr", "--model", sys.argv[3]])
    # The subprocess command allows the reproduction of the command line for a kraken transcription but with variables.  
    # Those variables are used to call the content of folders instead of trancribing one image at a time.  