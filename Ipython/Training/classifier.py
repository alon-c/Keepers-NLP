'''
Created on Feb 8, 2017

@author: Alon
'''
# -*- coding: utf-8 -*-

#===============================================================================
# SCRIPTS FOR CREATE NEW CLASSIFIERS FROM THE WATSON NLC SERVICE AND MANIPULATE IT
# THE INPUT FOR CREATE A CLASSIFIER MUST BE A .CSV FILE 
#===============================================================================



import json
import time
from watson_developer_cloud import NaturalLanguageClassifierV1
import os
from datashape.coretypes import null
import codecs


#classifier_id='cedf17x168-nlc-3397' 
#classifier_smallexp_id = 'cedec3x167-nlc-4394'

NLC_ACCOUNTS = (("e457cd66-3148-4a8b-877a-3dfaba378639", # NLC username
    "iQ73gqox40ee"), # NLC password
    ("4dcdb500-6f07-468b-9067-c02541e76bc9",
    "M2N3PY1zkY1O"),
    ("0db6e975-a152-4110-805b-8dd4a26b73c5",
    "ta61OZiyJqXK"),
    ("d0cc4100-578e-4001-b187-0ade6eb0ede1",
    "tJ32bilsEUzV"),
    ("d0b24ee1-5c32-49a6-9f2e-eb1f95ecdf92",
    "TEhcyL1QkM2f"),
    ("81484241-55e3-47a0-9ff3-4ac9c3d0c141",
    "NJW4N0vu6B6K"),
    ("e47df151-8882-4204-b880-0b83215caf09",
    "0V0stc6xWH5c"),
    ("500c121d-e031-4d4d-88ce-4d33d514ec49",
    "nAyw20hkiZMO"),
    ("52bc8bfd-dc87-49d5-9f6a-1838c899ea8a",
    "Hdr34NQk2dbf"))


#nlc_usr = '96e6ee96-1661-4aae-9956-c07db9eef464'
#nlc_psw = 'v2nb6hPx87JH'

#file = "training_set.csv"
#nameDir = '../training_csv_files/'

class NLCClassifier:
    def __init__(self, nlc_usr, nlc_psw):
        self.natural_language_classifier = NaturalLanguageClassifierV1(
          username=nlc_usr,
          password=nlc_psw)

# Create a new classifier train with the training_file
    # The training data must have at least five records (rows) and no more than 15,000 records
    def create_classifier(self, training_file, name, nb = None):
        print ('Name of the new classifier : ' , name)
        print('Training with',nb , 'percent with the file', training_file)
        print(self.list_classifiers_name_id())
        print(len(self.list_classifiers_name_id()))
        #with open(training_file, 'rb') as f:
        with codecs.open(training_file, 'rb',encoding='utf-8', errors='ignore') as training_data:
                t = time.clock()
                classifier = self.natural_language_classifier.create(
                            training_data=training_data,
                            name=name,
                        language='en')
                t = time.clock() - t
        print('creating time : ' + str(t))
        status = self.get_status(name)
        t = time.clock()
        while status != 'Available':
            status = self.get_status(name)
        t = time.clock() - t
        print('traning time : ' + str(t))
        return classifier

    # create_classifier('../training_csv_files/training_50.csv','class1')


    # return a list of ids of the classifiers available
    def list_classifiers_id(self):
        classifiers = self.natural_language_classifier.list()
        list_classifiers = list()
        x = json.dumps(classifiers, indent=2)
        jsonparser = json.loads(x)
        classi = jsonparser['classifiers']
        for i in range(len(classi)):
            list_classifiers.append(classi[i]['classifier_id'])
        return list_classifiers

    # print(list_classifiers_id())

    # return a of dictionary with ids and names of the classifiers available
    def list_classifiers_name_id(self):
        classifiers = self.natural_language_classifier.list()
        list_classifiers = dict()
        x = json.dumps(classifiers, indent=2)
        jsonparser = json.loads(x)
        classi = jsonparser['classifiers']
        for i in range(len(classi)):
            list_classifiers[classi[i]['name']] = classi[i]['classifier_id']
        return list_classifiers

# print(list_classifiers_name_id())


    # delete all the classifiers available by the name
    def delete_all_classifiers(self):
        ids = self.list_classifiers_name_id()
        for id in ids:
            self.natural_language_classifier.remove(ids[id])
    
# delete_by_name_classifiers()

# print(list_classifiers_name_id())

    # delete a classifiers by his name
    def delete_classifier_by_name(self, nameself):
        names = self.list_classifiers_name_id()
        self.natural_language_classifier.remove(names[name])

    # delete a classifiers by his id
    def delete_classifier_by_id(self, id):
        self.natural_language_classifier.remove(id)
    
    # delete_by_id_classifiers('')

    #get the id of a classifier by his name
    def get_id_classifier(self, name):
        ids = self.list_classifiers_name_id()
        return ids[name]

    #get the status of a classifier by his name
    def get_status(self, name):
        id = self.get_id_classifier(name)
        return self.natural_language_classifier.status(id)['status']
        
    # class a sentence with the classifier who named classifier_name
    def classify(self, classifier_name, sentence):
        classifiers = self.list_classifiers_name_id()
    
        # API CALL 
    #    natural_language_classifier = NaturalLanguageClassifierV1(
    #    username=nlc_usr, password=nlc_psw)
        t = time.clock()
        classes = self.natural_language_classifier.classify(classifiers[classifier_name], sentence)
        t = time.clock() - t
        print('API call time : ' , str(t))
        myjson = json.dumps(classes)
                 
        # Parsing 
        jsonparser = json.loads(myjson);  # parse the ans of the api
        answer_class = jsonparser["classes"][0]["class_name"]  # classified class with more confidence 
                
        return answer_class



