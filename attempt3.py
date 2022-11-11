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

# Trying to open csv files and if do not exist create them.
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

# Add two dataframe columns


def addColumns(FirstColumn, SecondColumn):
    return FirstColumn+SecondColumn

# Divide two df -replacing 0 with one to remove NaN


def findMean(FirstColumn, SecondColumn):
    SecondColumn.replace(to_replace=0, value=1,  inplace=True)
    return FirstColumn/SecondColumn


# Convert input input tsv file to csv
writeToFile(InputFile=input_file1, OutputFile=output_file1)
writeToFile(InputFile=input_file2, OutputFile=output_file2)

csvfile1 = pd.read_csv(readInputArgument().output1)
csvfile2 = pd.read_csv(readInputArgument().output2)
# add column 3 in csv 1 to column 3 in second csv (add ref_allele_counts)
result = addColumns(csvfile1['Ref_Allele_Count'], csvfile2['Ref_Allele_Count'])

# add column 4 in csv 1 to column 4 in second csv (add alt_allele_cunts)
result2 = addColumns(csvfile1['Alt_Allele_Count'],
                     csvfile2['Alt_Allele_Count'])

# add column 5 in csv 1 to column 5 in second csv (add cover depth)
result3 = addColumns(csvfile1['Coverage_Depth'], csvfile2['Coverage_Depth'])

# Find the mean between alt_allele frequencies in csv1 and csv2
result4 = findMean(result2, result3)

#Writing the results to a csv file 
with open('output.csv', 'w') as f:
    pd.concat([result, result2, result3, result4], axis=1).to_csv(f)
