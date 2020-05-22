import csv
import glob
import os
import shutil
import re
from pyrouge import Rouge155

#Create file
open('data.txt', 'w+')
open('data.csv', 'w+')

file_type = '.csv'
print(file_type)

#Initialize Rouge
r = Rouge155()
r.system_dir = '/home/alex/rouge_test/GS'     #This is the path to the Gold Standard Labels
r.model_dir = '/home/alex/rouge_test/Test'     #This is the path to the Model Generated Labels

#Initialize file locations
tf_dir  = r.model_dir
gs_dir  = r.system_dir

#Initalize file locations
tf_files = os.listdir(tf_dir)
gs_files = os.listdir(gs_dir)

#============================
#Format the test files (model summaries)
#convert from testfile.csv to testfile.A.001.txt
#============================
index = []
for file in tf_files:
    if file_type in file:
        index.append(file.replace(file_type, ''))
        with open(tf_dir + '/' + file) as t:
            text = t.read()
        file = file.replace('.', '.A.001.')
        file = file.replace(file_type, '.txt')

        f = open(r.model_dir + '/' + file, 'w+')
        f.write(text)
        f.close()

#===============================
#Format the Gold Standard files (system summaries)
#convert from testfile.csv to testfile.A.001
#===============================
for file in tf_files:
    if file_type in file:
        with open(gs_dir + '/' + file) as t:
            text = t.read()
        file = file.replace('.', '.001.')
        file = file.replace(file_type, '.txt')

        f = open(r.system_dir + '/' + file, 'w+')
        f.write(text)
        f.close()

#===============================
#Perform the Pyrouge measurement
#===============================
to_csv = {}
for items in index:
    r.system_filename_pattern  = items + '.(\d+).txt'
    r.model_filename_pattern   = items + '.[A-Z].#ID#.txt'
    output = r.convert_and_evaluate()
    with open('data.txt', 'a+') as t:
        t.write(items + '\n')
        t.write(output)
    output_dict = r.output_to_dict(output)
    to_csv.update({items:output_dict})

with open('data.csv', 'a+') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in to_csv.items():
        writer.writerow([key, value])

print(output_dict)