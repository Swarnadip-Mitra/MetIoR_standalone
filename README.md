# MetIoR_standalone
GitHub repository for standalone version of MetIoR, a meta predictor for prediction of intrinsic disorder in RNA binding proteins.


README file for MetIoR - a meta predictor to predict intrinsic disorder in RNA binding proteins.

Contents of this repository:

1. The main MetIoR program - "metior_base.py"
2. Folder containing the five component predictors of MetIoR - "preds"
3. The 10 model files of MetIoR generated as .pkl files by Python pickle library - "mod_dump[N].pkl" (N - 1 through 10)
4. Sample input file - "input.fasta"
5. Sample output file corresponding to disorder meta prediction of "input.fasta" - "sample_output.txt"

Files to be generated upon successful execution of "metior_base.py":

1. Output file - "output.txt" will be generated upon successful run of "metior_base.py"

-----------------------------
INSTRUCTIONS FOR INSTALLATION
-----------------------------

1. Software requirements:-

1.1 Ensure that a Python is installed in your system.

MetIoR meta predictor program is a simple python script, that calls other scripts corresponding to its component predictors.
ENSURE THAT A PYTHON INTERPRETOR IS ALREADY INSTALLED (Python 3.x preferred) and CAN BE READILY INVOKED from the terminal/command prompt.

1.2 Install the following Python libraries that are dependencies of MetIoR

MetIoR's dependencies (all Python libraries):-

(i) os
(ii) pandas
(iii) pickle
(iv) joblib

ENSURE THAT ALL THE ABOVE PYTHON LIBRARIES (dependencies of machine learning based programs like MetIoR) ARE INSTALLED AND CAN BE READILY IMPORTED.
All the above libraries are installable through python package installer - PIP.
"os" - python library comes autoinstalled with most versions of python.

--------------------
INSTRUCTIONS FOR USE
--------------------

1. Ensure that all software requirements including Python interpreter and all Python libraries that are MetIoR's dependencies (mentioned above) are properly installed.

2. Place your input (fasta) file IN THIS SAME DIRECTORY ("metior_base.py", "mod_dump[1 to 10].pkl", "preds" folder and your input fasta file must be in the same directory).
Input (fasta) file must have ".fasta" extension.

3. Please MODIFY THE FIRST LINE OF THE PROGRAM "metior_base.py" - change the "inputfilename" variable to the name of your fasta input file with extension (.fasta).
Example - if your fasta file is "P31483.fasta",
then change the first line of the program which is by default " inputfilename='input.fasta' " to " inputfilename='P31483.fasta' "

4. PLEASE MODIFY THE LINES WHERE YOUR SYSTEM PYTHON IS INVOKED - the MetIoR main program is a Python script "metior_base.py" which runs the component predictor scripts.
These component predictor scripts are also Python scripts. Hence, MetIoR will invoke your system Python in its code.
YOUR SYSTEM PYTHON WILL IS INVOKED IN LINES - 89, 100 and 113. The name of the invocable system python is by default kept as "python3",
but if your system python is invocable through some other name like "python" or something else, then please change these lines accordingly.

Example -  current line 89 is :-

iupred3_long_out=os.popen('python3 iupred3.py ../../../'+inputfilename+' long').read()

But if your system python is invoked by "python" instead of "python3", then change the line to:-

iupred3_long_out=os.popen('python iupred3.py ../../../'+inputfilename+' long').read()


5. Please do not modify any of the contents or locations of the files in the "preds" folder and the ten model files "mod_dump[1 to 10].pkl".

6. Execute the Python script "metior_base.py" from the terminal/command prompt.

Example usage syntax:-

$python3 metior_base.py

7. The output of meta prediction will be generated in "output.txt" file in the same directory.
