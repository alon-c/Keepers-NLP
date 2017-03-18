'''
Created on Feb 7, 2017

@author:Alon
'''
# -*- coding: utf-8 -*-

import csv
import random
from mpmath import rand


#file = "../csv_files/ownDB_good_level_of_bad.csv"
#target_file = "../training_csv_files/training_"

# select a training set that takes random rows from a csv file
def select_training_sentences_random(file, p):
    f = open(file, 'r')
    
    # number of the line in the source file
    lines = f.readlines()
    numline = len(lines)
    
    # p percent of the number of the lines in the source file
    b = int(numline * p)
    
    # the training set with b entry
    set = list()
    
    # list of the index of the selected rows in the source file
    numbers = list()
    
    # take b line from the source file and make a set with b entry
    while b > 0 :
        # pick a random number to select a line
        rand = random.randint(1, numline)
        # select the random line
        row = (lines[rand - 1].strip('\n'))
        # take only the line that are not in the set already
        if not(numbers.__contains__(rand)):
            r = row.split(',')
            # fix the comma problem
            # if a comma is in a sentences
            while not(r[1].isnumeric()):
                r[0] += r[1]
                r[1] = r[2]
                r.pop(2)
            r[1] = int(r[1])
            numbers.append(rand)
            set.append(r) 
            # print (r)
            b -= 1
    return set
    
# print (select_training_sentences_random(0.5))

# create a csv file with the rows that selected by select_training_sentences_random(p)
def create_training_file_random(file, p, target_file):
    set = select_training_sentences_random(file, p)
    # create a new file and put all the set on it line by line
    with open(target_file, 'w' , newline='') as f:
        writer = csv.writer(f)
        for i in range(len(set)):
            writer.writerow(set[i])
      
        
# create_training_file_random(0.3,target_file)

# select a training set that have 50% of several levels of bad(1,2,3) and 50% good(0)
# if the source file have an odd number of row it take one more of good 
def select_training_sentences_balance_good_bad(file, p):
    # problem to use dialog api because of the name of the PC that is in hebrew
    # filename = askopenfile('.')
    
    f = open(file, 'r')
    
    # number of the line in the source file
    lines = f.readlines()
    numline = len(lines)
    
    # print(p)
    # p percent of the number of the lines in the source file
    b = int(numline * p)
    balance = int(b / 2)
    
    # the training set with b entry
    set = list()
    
    # list of the index of the selected rows in the source file
    numbers = list()
    numbers_good = list()
    numbers_bad = list()

    #fix the issue is the number of rows is odd    
    fix = 0
    if b % 2 != 0:
        fix = 1
    
    # take b line from the source file and make a set with b entry
    while b > 0 :
        # pick a random number to select a line
        rand = random.randint(1, numline)
        # select the random line
        row = (lines[rand - 1].strip('\n'))
        # take only the line that are not in the set already
        if not(numbers.__contains__(rand)):
            r = row.split(',')
            
            # fix the comma problem : if a comma is in a sentences
            while not(r[1].isnumeric()):
                r[0] += r[1]
                r[1] = r[2]
                r.pop(2)
                
            r[1] = int(r[1])
    
            # if b is odd it take one more good
            if r[1] == 0 and len(numbers_good) < balance + fix:
                
                numbers_good.append(rand)
                numbers.append(rand)
                set.append(r) 
                # print (r)
                b -= 1
                
            if r[1] != 0 and len(numbers_bad) < balance :
                numbers_bad.append(rand)
                numbers.append(rand)
                set.append(r) 
                b -= 1
    f.close()
    
    return set
    
# print (select_training_sentences_balance_good_bad('../csv_files/ownDB_good_level_of_bad_BAD.csv',0.5))
# print (select_training_sentences_balance_good_bad('../csv_files/test.csv',0.5))

# create a csv file with the rows that selected by select_training_sentences_balance_good_bad(source,p)

def create_training_file_balance_good_bad(source, p, target_file):
    set = select_training_sentences_balance_good_bad(source, p)
    # print (len(set))
    # create a new file and put all the set on it line by line
    with open(target_file, 'w' , newline='') as f:
        writer = csv.writer(f)
        for i in range(len(set)):
            writer.writerow(set[i])
        
# create_training_file_balance_good_bad(file,0.5, target_file+'0_1.csv')

# read a csv file and return a list of the good and a list of the bad sentences 
def extract_good_and_bad(file):
    
    # problem to use dialog api because of the name of the PC that is in hebrew
    # filename = askopenfile('.')
    set_good = []
    set_bad = []
    nb_lines = 0
    nb_1 = 0
    nb_2 = 0
    nb_3 = 0
 
    with open(file, 'rt') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            nb_lines += 1
            # fix the comma problem
            # if a comma is in a sentences
            r = row
            while not(r[1].isnumeric()):
                r[0] += r[1]
                r[1] = r[2]
                r.pop(2)
            r[1] = int(r[1])
            
            if r[1] == 0 :
                set_good.append((r[0], r[1]))
            else :
                if r[1] == 1 :
                    nb_1 += 1
                if r[1] == 2 :
                    nb_2 += 1
                if r[1] == 3 :
                    nb_3 += 1
                    
                set_bad.append((r[0], r[1]))
                
    print('number of samples :', len(set_bad) + len(set_good))
    print('number of good :', len(set_good))
    print('number of bad :', len(set_bad))
    print('number of low :', nb_1)
    print('number of medium :', nb_2)
    print('number of heavy :', nb_3)
    
    return set_good, set_bad, nb_lines

#extract_good_and_bad('../csv_files/DoronEnglish_158_23_69_66.csv')

# read a csv file and return 2 dict
# one with all the sentences and their classes (0 1)
# one with only the bad sentences with their classes(1 2 3)
def extract_good_and_bad_0_1_and_bad(file):
    
    # problem to use dialog api because of the name of the PC that is in hebrew
    # filename = askopenfile('.')
    set_0_1 = []
    set_bad = []
    
    with open(file, 'rt') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            # fix the comma problem
            # if a comma is in a sentences
            r = row
            while not(r[1].isnumeric()):
                r[0] += r[1]
                r[1] = r[2]
                r.pop(2)
                
            r[1] = int(r[1])
            
            if r[1] == 0 :
                set_0_1.append((r[0], r[1]))
            else :
                set_0_1.append((r[0], 1))
                set_bad.append((r[0], r[1]))
    
    return set_0_1, set_bad

# print(extract_good_and_bad_0_1_and_bad(file))

# create 2 files
# the first with 0 1
# the second with 1 2 3
def create_file_0_1_and_bad(source):
    target = source.split('.csv')[0]
    target_0_1 = target + '_0_1.csv'
    target_bad = target + '_bad.csv'
    set_good, set_bad = extract_good_and_bad_0_1_and_bad(source)
    print(len(set_good))
    print(len(set_bad))
    with open(target_0_1, 'w', newline='') as t :
        writer = csv.writer(t)
        for good in set_good:
            # print(good)
            writer.writerow([good[0], good[1]])
    with open(target_bad, 'w', newline='') as t :
        writer = csv.writer(t)
        for bad in set_bad:
            # print(bad)
            writer.writerow(bad)
    return target_0_1, target_bad

# create_file_0_1_and_bad(file)
      
# take a p percent of the file with p_bad percent of bad sentences and the rest of good   
def select_training_file_balance_good_level_of_bad_percent_bad(file, p, p_bad):
    set_good, set_bad, nb_lines = extract_good_and_bad(file)

    nb_select = int(nb_lines * p)
    nb_bad = int(nb_select * p_bad)
    nb_good = nb_select - nb_bad
    new_file = list()
    
    for i in range(nb_bad):
        rand = set_bad.pop()
        new_file.append(rand)
        
      
    for i in range(nb_good):
        rand = set_good.pop()
        new_file.append(rand)
    
    return new_file
        
# select_training_file_balance_good_level_of_bad_percent_bad('textEnglish9.csv', 0.5, 0.1)

def create_training_file_balance_good_level_of_bad_percent_bad(file, p, p_bad, target_file):
    set = select_training_file_balance_good_level_of_bad_percent_bad(file, p, p_bad)
    # create a new file and put all the set on it line by line
    with open(target_file, 'w' , newline='') as f:
        writer = csv.writer(f)
        for i in range(len(set)):
            # print(set[i])
            writer.writerow(set[i])

# create_training_file_balance_good_level_of_bad_percent_bad('textEnglish9.csv', 0.5, 0.5, 'textEnglish9_test.csv')

# creating 1 training file for each number in nb with the percent of the number
# for the one level classifier
def create_training_files(file, nb):
    name = file.split('.csv')[0]
    name = name.split('/')
    name = name[len(name) - 1]
    training = '../training_csv_files/' + name + '_'
    for i in nb:
        name = training + str(i) + '.csv'
        print(name)
        create_training_file_balance_good_bad(file, i / 100.0, name)
 
# nb = [5, 10, 15,20,30,40]
# create_training_files('textEnglish9.csv', nb)

# creating 2 training files for each number in nb with the percent of the number
# one for the 0 1 classifier one for the bad level classifier
def create_training_files_0_1_and_bad(file, nb):
    # creates_files_0_1_and_bad(file)
    target_0_1, target_bad = create_file_0_1_and_bad(file)
    name = file.split('.csv')[0]
    name = name.split('/')
    name = name[len(name) - 1]
    training_0_1 = '../training_csv_files/' + name + '_0_1_'
    training_bad = '../training_csv_files/' + name + '_bad_'
   
    for i in nb:
        name_0_1 = training_0_1 + str(i) + '.csv'
        name_bad = training_bad + str(i) + '.csv'
        create_training_file_balance_good_bad(target_0_1, i / 100.0, name_0_1)
        create_training_file_random(target_bad, i / 100.0, name_bad)


        
