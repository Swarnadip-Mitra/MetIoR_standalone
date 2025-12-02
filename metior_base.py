inputfilename='input.fasta' ##### Please modify this variable to the name of your fasta file (include the ".fasta" extension) e.g. "P31483.fasta"
##### Your fasta file must be in the same directory as this program along with the ten "mod_dump[1 to 10].pkl" files and the "preds" folder
##### Output will be produced in the file "output.txt" in this same directory.


import os,pandas as pd,pickle
from joblib import Parallel,delayed
import joblib



if not inputfilename.endswith('.fasta'):
	print('Please use .fasta extension for input file. Program terminated. Please retry.')


######################### Reading input.fasta ##########################
f=open(inputfilename)
flines=f.readlines()
f.close()

######################### Removing blank lines from input.fasta ########
flines_no_blanks=[]
for line in flines:
	if line not in ['','\n',' ',' \n']:
		flines_no_blanks.append(line)

######################### Reconstructing input.fasta ###################
f=open(inputfilename,'w')
for line in flines_no_blanks:
	a=f.write(line)
f.close()

######################### Reading modified input.fasta #################
f=open(inputfilename)
fasta_seq=f.read()
f.close()

######################### Checking for improper fasta formats ##########

standard_aminoacids=['Q','W','E','R','T','Y','I','P','A','S','D','F','G','H','K','L','C','V','N','M']

fasta_empty_flag=False
fasta_invalid_char_flag=False
fasta_header_sign_missing_flag=False

if fasta_seq in [None,'',' ','\n',' \n']:
	fasta_empty_flag=True

fasta_header_line=fasta_seq.split('\n')[0]
fasta_remaining_lines=fasta_seq.split('\n')[1:]
if fasta_remaining_lines[-1] in ['',' ','\n']:
	fasta_remaining_lines=fasta_remaining_lines[:-1]

if fasta_header_line[0]!='>':
	fasta_header_sign_missing_flag=True

for line in fasta_remaining_lines:
	for letter in line:
		if letter in standard_aminoacids or letter=='\n':
			pass
		else:
			fasta_invalid_char_flag=True
			break
	if fasta_invalid_char_flag:
		break

#################### Improper input - program termination ##############

if fasta_empty_flag==False and fasta_invalid_char_flag==False and fasta_header_sign_missing_flag==False:
	pass
else:
	improper_input_generic_message='Improper input detected. Program terminated.'
	f=open('output.txt','w')
	a=f.write(improper_input_generic_message)
	f.close()
	print('\n'+improper_input_generic_message)
	exit(-1)

################### FASTA check successful #############################

current_location=os.getcwd()

################# Running component predictors #########################

################# 1. IUPred3-long

os.chdir('preds/iupred3/iupred3')

iupred3_long_out=os.popen('python3 iupred3.py ../../../'+inputfilename+' long').read() ## Please change "python3" to the appropriate name of the python interpreter on your system
iupred3_long_lines=iupred3_long_out.split('\n')
if iupred3_long_lines[-1] in ['',' ','\n']:
	iupred3_long_lines=iupred3_long_lines[:-1]
iupred3_long_lines=iupred3_long_lines[12:]
iupred3_long_scores=[]
for line in iupred3_long_lines:
	iupred3_long_scores.append(float(line.split('\t')[-1]))

################# 2. IUPred3-short

iupred3_short_out=os.popen('python3 iupred3.py ../../../'+inputfilename+' short').read() ## Please change "python3" to the appropriate name of the python interpreter on your system
iupred3_short_lines=iupred3_short_out.split('\n')
if iupred3_short_lines[-1] in ['',' ','\n']:
	iupred3_short_lines=iupred3_short_lines[:-1]
iupred3_short_lines=iupred3_short_lines[12:]
iupred3_short_scores=[]
for line in iupred3_short_lines:
	iupred3_short_scores.append(float(line.split('\t')[-1]))

################# 3. Aiupred

os.chdir('../../aiupred/aiupred')

aiupred_out=os.popen('python3 aiupred.py -i ../../../'+inputfilename).read() ## Please change "python3" to the appropriate name of the python interpreter on your system
aiupred_lines=aiupred_out.split('\n')
if aiupred_lines[-1] in ['',' ','\n']:
	aiupred_lines=aiupred_lines[:-1]
aiupred_lines=aiupred_lines[13:]
aiupred_scores=[]
for line in aiupred_lines:
	aiupred_scores.append(float(line.split('\t')[-1]))

################# 4. IsUnstruct-long

os.chdir('../../isunstruct')

os.system('./IsUnstruct ../../'+inputfilename) 
if os.path.exists('input.iul'):
	f=open('input.iul')
elif os.path.exists(inputfilename[:-6]+'.iul'):
	f=open(inputfilename[:-6]+'.iul')
else:
	print('IsUnstruct-long execution not possible. Program terminated')
	exit(-2)
iul_lines=f.readlines()
f.close()
if iul_lines[-1] in ['',' ','\n']:
	iul_lines=iul_lines[:-1]
iul_lines=iul_lines[4:]
iul_scores=[]
for line in iul_lines:
	iul_scores.append(float(line.split()[-1]))
if os.path.exists('input.iul'):
	os.remove('input.iul')
elif os.path.exists(inputfilename[:-6]+'.iul'):
	os.remove(inputfilename[:-6]+'.iul')

################# 5. IsUnstruct-short

if os.path.exists('input.ius'):
	f=open('input.ius')
elif os.path.exists(inputfilename[:-6]+'.ius'):
	f=open(inputfilename[:-6]+'.ius')
else:
	print('IsUnstruct-short execution not possible. Program terminated')
	exit(-3)
ius_out=f.read()
f.close()
ius_lines=ius_out.split('\n')
ius_scores=[]
for line in ius_lines:
	if line.startswith('probability'):
		temp=list(''.join(line[17:-5].split()))
		for each in temp:
			ius_scores.append(0.1*int(each))
if os.path.exists('input.ius'):
	os.remove('input.ius')
elif os.path.exists(inputfilename[:-6]+'.ius'):
	os.remove(inputfilename[:-6]+'.ius')

os.chdir(current_location)

################ Meta prediction step ##################################

X_input=[]
for i in range(len(iul_scores)):
	X_input.append([iupred3_long_scores[i],iupred3_short_scores[i],aiupred_scores[i],iul_scores[i],ius_scores[i]])

X_in=pd.DataFrame(X_input)
y_outs=[]

foldnum=1
for i in range(10):
	rfc_from_dump=joblib.load('mod_dump'+str(i+1)+'.pkl')
	y_out=rfc_from_dump.predict_proba(X_in)
	y_outs.append(y_out)
	foldnum+=1

y_class1_mean_probabs=[]
for i in range(len(y_outs[0])):
	y_class1_mean_probabs.append(0)

for i in range(len(y_class1_mean_probabs)):
	for j in range(len(y_outs)):
		y_class1_mean_probabs[i]+=y_outs[j][i][-1]
	y_class1_mean_probabs[i]/=len(y_outs)
	y_class1_mean_probabs[i]=round(y_class1_mean_probabs[i],3)

##################### Output preparation ###############################
outp='MetIoR disorder meta-prediction for '+inputfilename+'\n'
outp+='AA=Amino acid; D/O=Disorder/Order; M=MetIoR; P1=IUPred3-long; P2=IUPred3-short; P3=Aiupred; P4=IsUnstruct-long; P5=IsUnstruct-short\n'
outp+='Sl no.\t\tAA\t\tD/O\t\tM\t\tP1\t\tP2\t\tP3\t\tP4\t\tP5\n'
outp+='-----------------------------------------------------------------------------------------------------------------------------------------------\n'
seqs=[]
for i in fasta_remaining_lines:
	for j in i:
		seqs.append(j)

dos=[]
for i in y_class1_mean_probabs:
	if i<0.5:
		dos.append('O')
	else:
		dos.append('D')

iup3ls=[]
iup3ss=[]
aiups=[]
iuls=[]
iuss=[]
for i in range(len(iul_scores)):
	iup3ls.append(round(iupred3_long_scores[i],3))
	iup3ss.append(round(iupred3_short_scores[i],3))
	aiups.append(round(aiupred_scores[i],3))
	iuls.append(round(iul_scores[i],3))
	iuss.append(round(ius_scores[i],3))

for i in range(len(seqs)):
	outp+=str(i+1)+'\t\t'+seqs[i]+'\t\t'+dos[i]+'\t\t'+str(y_class1_mean_probabs[i])+'\t\t'+str(iup3ls[i])+'\t\t'+str(iup3ss[i])+'\t\t'+str(aiups[i])+'\t\t'+str(iuls[i])+'\t\t'+str(iuss[i])+'\n'

f=open('output.txt','w')
a=f.write(outp)
f.close()

if os.name=='posix':
	os.system('clear')
elif os.name=='nt':
	os.system('cls')
print('Disorder meta-prediction obtained successfully in file \"output.txt\"')
