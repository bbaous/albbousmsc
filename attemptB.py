#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 14:12:52 2022

@author: alexandrabaousi
"""

import pandas as pd
import re
import argparse


'''
Parse input arguments
usage : ./attemptB.py  --file1 file_pairB_1.tsv --file2 file_pairB_2.tsv
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

# Convert input input tsv file to csv
writeToFile(InputFile=input_file1, OutputFile=output_file1)
writeToFile(InputFile=input_file2, OutputFile=output_file2)

# Load the output files
csvfile1 = pd.read_csv(output1)
csvfile2 = pd.read_csv(output2)
  
# using merge function by setting how='inner'
with open('output2.csv', 'w') as f:
    pd.merge(csvfile1, csvfile2, 
                   on=['Scaffold','Position'], 
                   how='inner').to_csv(f)
    
# find relationship between columns in this csv and calculate - done 
# put them in a new csv 
# in this csv append the 3 missing rows from csv1 and csv2

# Add two dataframe columns
def addColumns(FirstColumn, SecondColumn):
    return FirstColumn+SecondColumn.fillna(0)

# Divide two df -replacing 0 on the second df with 1 to remove NaN
def findMean(FirstColumn, SecondColumn):
    #SecondColumn.replace(to_replace=0, value=1,  inplace=True)
    return FirstColumn.divide(SecondColumn).fillna(0)


csvfile3 = pd.read_csv("output2.csv")

result00 = csvfile3[["Scaffold"]].copy()
result01 = csvfile3[["Position"]].copy()

result1 = addColumns(csvfile3['Ref_Allele_Count_x'],
                      csvfile3['Ref_Allele_Count_y'])

result2 = addColumns(csvfile3['Alt_Allele_Count_x'],
                      csvfile3['Alt_Allele_Count_y'])

result3 = addColumns(csvfile3['Coverage_Depth_x'], 
                     csvfile3['Coverage_Depth_y'])

result4 = findMean(result2, result3)
result4.name = result2.name

# Writing the results to a new csv file
with open('output2b.csv', 'w') as f:
    pd.concat([result00, result01, result1, result2,
              result3, result4], axis=1).to_csv(f)
    
# in that new csv file, append the 3 missing rows from the other two 
# put them in the right order 

with open('output2c.csv', 'w') as f:
    pd.merge(csvfile1, csvfile2, 
                   on=['Position', 'Scaffold'], 
                   how='outer').to_csv(f)

# this is for outputc 
csvfile4 = pd.read_csv("output2c.csv")

result00 = csvfile4[["Scaffold"]].copy()
result01 = csvfile4[["Position"]].copy()

result1 = addColumns(csvfile4['Ref_Allele_Count_x'],
                      csvfile4['Ref_Allele_Count_y'])

result2 = addColumns(csvfile4['Alt_Allele_Count_x'],
                      csvfile4['Alt_Allele_Count_y'])

result3 = addColumns(csvfile4['Coverage_Depth_x'],
                     csvfile4['Coverage_Depth_y'])

result4 = findMean(result2, result3)

# Writing the results to a new csv file
with open('output2d.csv', 'w') as f:
    pd.concat([result00, result01, result1, result2,
              result3, result4], axis=1).to_csv(f)
    
# this messes up the last value and column names  
# i need to rename the columns from the random set numbers 
# this doesnt work

data_import = pd.read_csv('output2d.csv',         
                          skiprows = 1,
                          names = ['Scaffold', 'Position', 
                                   'Ref_Allele_Count', 'Alt_Allele_Count',
                                   'Coverage_Depth', 'Alt_Allele_Frequency'])


