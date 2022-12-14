#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Python program to convert .tsv file to .csv file
# Importing necessary libraries
import csv
import numpy as np
import pandas as pd
import re
import argparse
import json


def readInputArgument():

    my_parser = argparse.ArgumentParser(description='File to be loaded:')

    my_parser.add_argument('--input',
                           '-i',
                           metavar='input',
                           type=str,
                           help='the file to be loaded')

    my_parser.add_argument('--output',
                           '-o',
                           metavar='output',
                           help='Output file .',
                           )
    # Execute the parse_args() method
    args = my_parser.parse_args()

    return args


input_file = open(readInputArgument().input, 'r')
output_file = open(readInputArgument().output, 'w')
#input_file = open(readInputArgument().file1, 'r')


def readInputArguments():
    parser = argparse.ArgumentParser()
    # note type arg, used to load json string
    parser.add_argument('-l', '--list', type=json.loads,
                        help='the files to be loaded')
    args = parser.parse_args()
    print(args.list)
    # print(args.list[0])
    return args.list[0]


#input_file = open(readInputArguments(), 'r')

# reading given tsv file
with input_file as myfile:
    with output_file as csv_file:
        for line in myfile:

            # Replace every tab with comma
            fileContent = re.sub("\t", ",", line)

            # Writing into csv file
            csv_file.write(fileContent)

# output
print("Successfully made csv file")

# reading second given tsv file
with open("file_pairA_2.tsv", 'r') as myfile:
    with open("file_pairA_2.csv", 'w') as csv_file:
        for line in myfile:

            # Replace every tab with comma
            fileContent = re.sub("\t", ",", line)

            # Writing into csv file
            csv_file.write(fileContent)

# output
print("Successfully made second csv file")


# merge the files
# add column 3 in csv 1 to column 3 in second csv (add ref_allele_counts)
csvfile = pd.read_csv('file_pairA_1.csv')
csvfile1 = pd.read_csv('file_pairA_2.csv')

result = csvfile['Ref_Allele_Count'] + csvfile1['Ref_Allele_Count']
print(result)

# add column 4 in csv 1 to column 4 in second csv (add alt_allele_counts)
result2 = csvfile['Alt_Allele_Count'] + csvfile1['Alt_Allele_Count']
print(result2)

# add column 5 in csv 1 to column 5 in second csv (add cover depth)
result3 = csvfile['Coverage_Depth'] + csvfile1['Coverage_Depth']
print(result3)


# find the mean between alt_allele frequencies in csv1 and csv2 - remember to add if to disqualify 0
# - if didnt work and i keep getting NaN
# legit no ifs worked ffs

result4 = result2 / result3

try:
    result4 = result2 / result3
except ZeroDivisionError:
    result4 = 0

# tried to replace NaN with 0
# doestnt work

df = result4
df.replace(np.nan, 0)

print(result4)


# print output into a csv (or a tsv lol)
# this code doesnt work

result = {}
with open('output1.csv', 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    for row in result.items():
        csvwriter.writerow(row)
