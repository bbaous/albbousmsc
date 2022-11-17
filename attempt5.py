#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Python program to convert .tsv file to .csv file


# Importing necessary libraries
import pandas as pd
import re
import argparse
import numpy as np

'''
Parse input arguments
usage : ./attempt5.py  --file1 file_pairA_1.tsv --file2 file_pairA_2.tsv
'''
# reads input from command line --
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

    # Execute the parse_args() method
    args = my_parser.parse_args()
    return args

# Convert a tsv to csv file
def writeToFile(InputFile, OutputFile):
    # reading given tsv file
    with InputFile as tsv_file:
        with OutputFile as csv_file:
            for line in tsv_file:
                # Replace every tab with comma
                # Writing into csv file
                csv_file.write(re.sub("\t", ",", line))
        csv_file.close()
    # output
    print("Successfully made csv file")


# Reading the input tsv files
input_file1 = open(readInputArgument().file1, 'r')
input_file2 = open(readInputArgument().file2, 'r')

''' Creating the filenames for the output csv files
    (same filename as the input tsv files with a csv extention )
'''
output1 = input_file1.name.partition('.')[0]+".csv"
output2 = input_file2.name.partition('.')[0]+".csv"

# Trying to open csv files and if they do not exist create them.
try:
    output_file1 = open(output1, 'w')
    print("File Exists")
except IOError:
    output_file1 = open(output1, 'w')
    print("File Created")

try:
    output_file2 = open(output2, 'w')
    print("File Exists")
except IOError:
    output_file2 = open(output2, 'w')
    print("File Created")

# Add two dataframe columns
def addColumns(FirstColumn, SecondColumn):
    return FirstColumn+SecondColumn

# Divide two df -replacing 0 on the second df with 1 to remove NaN
def findMean(FirstColumn, SecondColumn):
    return FirstColumn.divide(SecondColumn).fillna(0)

# Convert input input tsv file to csv
writeToFile(InputFile=input_file1, OutputFile=output_file1)
writeToFile(InputFile=input_file2, OutputFile=output_file2)

# Load the output files
csvfile1 = pd.read_csv(output1)
csvfile2 = pd.read_csv(output2)

# print untouched columns into output
result00 = csvfile1[["Scaffold"]].copy()
result01 = csvfile1[["Position"]].copy()

# Add column 3 in csv 1 to column 3 in second csv (add ref_allele_counts)
result02 = addColumns(csvfile1['Ref_Allele_Count'],
                      csvfile2['Ref_Allele_Count'])

# Add column 4 in csv 1 to column 4 in second csv (add alt_allele_cunts)
result03 = addColumns(csvfile1['Alt_Allele_Count'],
                      csvfile2['Alt_Allele_Count'])

# Add column 5 in csv 1 to column 5 in second csv (add cover depth)
result04 = addColumns(csvfile1['Coverage_Depth'], csvfile2['Coverage_Depth'])

# Find the mean between alt_allele frequencies in csv1 and csv2
result05 = findMean(result03, result04)
result05.name = result03.name

# Writing the results to a csv file
with open('output.csv', 'w') as f:
    pd.concat([result00, result01, result02, result03,
              result04, result05], axis=1).to_csv(f)
