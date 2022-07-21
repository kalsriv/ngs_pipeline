#!/usr/bin/python
import os
import json
import re
from sys import argv

samples=argv[2]
output = {
	"sample_captures": {},
	"Diagnosis": {},
	"sample_type": {},
	"subject": {},
	"library": {},
	"sample_references": {},
	"sample_RNASeq": {},
	"RNASeq": {},
}

#patientIndex=0
#TypeIndex=1
#DiagnosisIndex=2
#captureIndex=4
#FCIDIndex=5
#libraryIndex=6
#normRefIndex=7
#rnaRefIndex=8

### Column headers in current txt input file
#custom ID
#Type
#Diagnosis
#Type of sequencing
#Enrichment step
#FCID
#Library ID
#Matched normal
#Matched RNA-seq lib
#Case Name
f = open(argv[1], 'r')
for line in f:
	line = line.rstrip()
	column = line.split("\t")
	if re.search("custom ID", line):
		patientIndex	=column.index('custom ID')
		TypeIndex	=column.index('Type')
		DiagnosisIndex	=column.index('Diagnosis')
		captureIndex	=column.index('Enrichment step')
		FCIDIndex	=column.index('FCID')
		libraryIndex	=column.index('Library ID')
		normRefIndex	=column.index('Matched normal')
		rnaRefIndex	=column.index('Matched RNA-seq lib')
	column[captureIndex] =column[captureIndex].lower()
	# Change it to work with current pipeline
	if column[TypeIndex]  == 'tumor RNA':
		column[TypeIndex] = 'RNASeq'
	elif column[TypeIndex]  == 'tumor DNA':
		column[TypeIndex] = 'Tumor'
	elif column[TypeIndex] in ['normal DNA', 'blood DNA']:
		column[TypeIndex] = 'Normal'


	for sample in samples.split(','):
		if column[patientIndex] == sample:
			output["sample_captures"][column[libraryIndex]]=column[captureIndex]
			output["Diagnosis"][column[libraryIndex]]=column[DiagnosisIndex]
			output["sample_type"][column[libraryIndex]]=column[TypeIndex]
			if column[normRefIndex]:
				output["sample_references"][column[libraryIndex]]=[column[normRefIndex]]
			if column[rnaRefIndex]:
				output["sample_RNASeq"][column[libraryIndex]] =[column[rnaRefIndex]]
			output["library"][column[libraryIndex]] = (
				[f"{column[libraryIndex]}_{column[FCIDIndex]}"]
				if column[FCIDIndex]
				else [column[libraryIndex]]
			)

			if 'Normal' in column[TypeIndex] or 'Tumor' in column[TypeIndex]:
				if column[patientIndex] in output["subject"].keys():
					output["subject"][column[patientIndex]].append(column[libraryIndex])
				else:	
					output["subject"][column[patientIndex]]=[column[libraryIndex]]
			elif column[patientIndex] not in output["RNASeq"].keys():
				output["RNASeq"][column[patientIndex]]=[column[libraryIndex]]
			else:
				output["RNASeq"][column[patientIndex]].append(column[libraryIndex])


print(json.dumps(output, sort_keys=True, indent=4))
