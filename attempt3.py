#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Python program to convert .tsv file to .csv file
# Importing necessary libraries
import csv
import numpy as np
import pandas as pd
import re
import argparse
import os
import gc
import io

def readInputArgument():

    my_parser = argparse.ArgumentParser(description='File to be loaded:')

    my_parser.add_argument('--file1',
                           '-f1',
                           metavar='file1',
                           type=str,
                           help='the file1 to be loaded')
    
    my_parser.add_argument('--file2',
                           '-f2',
                           metavar='file2',
                           type=str,
                           help='the file2 to be loaded')
    
    my_parser.add_argument('--output1',
                           '-o1',
                           metavar='output1',
                           help='Output1 file to write ',
                           )

    my_parser.add_argument('--output2',
                           '-o2',
                           metavar='output2',
                           help='Output2 file to write ',
                           )

    # Execute the parse_args() method
    args = my_parser.parse_args()
    return args

#Convert a tsv to csv file 
def writeToFile(InputFile, OutputFile):

    # reading given tsv file
    with InputFile as tsv_file:
        with OutputFile as csv_file:
            print ("Within the lool ")
            print(InputFile)
            print (OutputFile)        
            for line in tsv_file:
                # Replace every tab with comma
                # Writing into csv file
                csv_file.write(re.sub("\t", ",", line))
        csv_file.close()
        OutputFile.close()
        InputFile.close()
                      
                
    # output
    print("Successfully made csv file")
    gc.collect()
    del InputFile,OutputFile,line



def writeToFile2(InputFile, OutputFile):
    # reading given tsv file
    csv_table=pd.read_table(InputFile,sep='\t')
    # converting tsv file into csv
    csv_table.to_csv(OutputFile,index=False)              
                
    # output
    print("Successfully made csv file")
  



input_file1 = open(readInputArgument().file1, 'r')
input_file2 = open(readInputArgument().file2, 'r')

try:
    output_file1 = open(readInputArgument().output1, 'w')
    print("File Exists")
except IOError:
    output_file1 = open(readInputArgument().output1, 'w')
    print("File Created")


try:
    output_file2 = open(readInputArgument().output2, 'w')
    print("File Exists")
except IOError:
    output_file2 = open(readInputArgument().output2, 'w')
    print("File Created")


writeToFile(InputFile=input_file1, OutputFile=output_file1)
writeToFile(InputFile=input_file2, OutputFile=output_file2)




# merge the files
# add column 3 in csv 1 to column 3 in second csv (add ref_allele_counts)
#csvfile1 = pd.read_csv(readInputArgument().output1)
#csvfile2 = pd.read_csv(readInputArgument().output2)

#result = csvfile1['Ref_Allele_Count'] + csvfile2['Ref_Allele_Count']
#print(csvfile1['Ref_Allele_Count'])
#print(csvfile2['Ref_Allele_Count'])

# add column 4 in csv 1 to column 4 in second csv (add alt_allele_counts)
#result2 = csvfile1['Alt_Allele_Count'] + csvfile2['Alt_Allele_Count']
#print(result2)

# add column 5 in csv 1 to column 5 in second csv (add cover depth)
#result3 = csvfile1['Coverage_Depth'] + csvfile2['Coverage_Depth']
#print(result3)


# find the mean between alt_allele frequencies in csv1 and csv2 - remember to add if to disqualify 0
# - if didnt work and i keep getting NaN
# legit no ifs worked ffs

#result4 = result2 / result3

#try:
#    result4 = result2 / result3
#except ZeroDivisionError:
#    result4 = 0

# tried to replace NaN with 0
# doestnt work

#df = result4
#df.replace(np.nan, 0)

#print(result4)


# print output into a csv (or a tsv lol)
# this code doesnt work

result = {}
with open('output1.csv', 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    for row in result.items():
        csvwriter.writerow(row)
