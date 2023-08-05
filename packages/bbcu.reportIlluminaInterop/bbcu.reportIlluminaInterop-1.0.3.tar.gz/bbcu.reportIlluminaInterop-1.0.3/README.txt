Package: bbcu.reportIlluminaInterop

The package creates file with statistics of sequencing run (HiSeq or NextSeq machines of illumina).

The run command is:

run-sav-stat.py --input-folder INPUT_FOLDER --output-file OUTPUT_FILE

INPUT_FOLDER - Run folder of the machine. Need to looked like this: 180717_NB551168_0163_AHF727BGX7
OUPUT_FILE   - Your name for the output file (with .txt extension).


=====================================================================

Example of output files are under "examples" folder.

You can convert it to pdf with the commnad: 

pandoc -o OUTPUT_FILE.pdf  --variable=geometry:landscape OUTPUT_FILE


=====================================================================


Developed by Refael Kohen (refael.kohen@gmail.com)

Bioinformatics unit at Life Sciences Core Facilities (LSCF),

Weizmann Institute of Science 

Based on the Python package interop. 
