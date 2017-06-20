import classifier

import threading
import time

###
# represents the classification training and testing task (for one and two levels classification approaches) with multi threading for the 'NLC tool'
#
# Author: Alon Cohen Zada
###

# -*- coding: utf-8 -*-


""" Testing - one level approach"""
class wrapperInputs:
    inputs = []
    counter = 0
    false_alerts_counter = 0  # number of predictions is 1,2 or 3 and the actual class is 0
    misplaced_alerts_counter = 0  # number of 
    missed_alerts_counter = 0  # number of predictions is 0 and the actual class is 1,2 or 3
    A = 0  # All that the prediction is different of 0
    T_1_2_3 = 0
    T_0 = 0

threadLock = threading.Lock()
class classifierTask (threading.Thread):
    def __init__(self, tNum, wrapperInputs, classifier_name, nlc_usr, nlc_pass):
        threading.Thread.__init__(self)

        self.tNum = tNum # assign thread number
        self.wrapperInputs = wrapperInputs
        self.classifier_name = classifier_name

        self.NLCClassifier = classifier.NLCClassifier(nlc_usr, nlc_pass)

    def run(self):
        while 1:
            threadLock.acquire()
            if len(self.wrapperInputs.inputs) <= 0:
                threadLock.release()
                return 
            tmpInput = self.wrapperInputs.inputs.pop()
            print('thread number: {0}'.format(self.tNum))
            threadLock.release()

            actual_sentence = tmpInput[0]  # string of the example (input/ message)
            actual_class = tmpInput[1]  # the classified class for the matching input

            # afther getting the input from the list send it to the NLC
            answer_class = self.NLCClassifier.classify(self.classifier_name, actual_sentence)
            print("Actual Class: ", actual_class, " ", "Response Class: ", answer_class, "\n")

            threadLock.acquire()
            # when the prediction is different of 0
            if answer_class != '0':
                self.wrapperInputs.A += 1

            if actual_class == '0':
                self.wrapperInputs.T_0 += 1

            if actual_class == answer_class:  # asking for a hit
                self.wrapperInputs.counter += 1
                # good prediction different of 0(misplaced_alert)
                if actual_class != '0': 
                    self.wrapperInputs.misplaced_alerts_counter += 1  
            # if the prediction is wrong        
            else :
                # when the class is 0 and the prediction is different of 0(false alert)
                if actual_class == '0':
                    self.wrapperInputs.false_alerts_counter += 1
                # when the actual class is 1,2 or 3 and it predict 0
                if answer_class == '0':  # else is ok too i think need to see 
                    self.wrapperInputs.missed_alerts_counter += 1
            threadLock.release()

""" Testing - Two level approach"""

class wrapperInputs_two:
    inputs = []
    counter = 0
    counter_get_2 = 0
    false_alerts_counter = 0  # number of predictions is 1,2 or 3 and the actual class is 0
    misplaced_alerts_counter = 0  # number of 
    missed_alerts_counter = 0  # number of predictions is 0 and the actual class is 1,2 or 3
    A = 0  # All that the prediction is different of 0
    T_1_2_3 = 0
    T_0 = 0

threadLock1 = threading.Lock()
class classifierTask_two (threading.Thread):
    def __init__(self, tNum, wrapperInputs, classifier_name, nlc_usr, nlc_pass, classifier_bad):
        threading.Thread.__init__(self)

        self.tNum = tNum # assign thread number
        self.wrapperInputs = wrapperInputs
        self.classifier_name = classifier_name
        self.classifier_bad = classifier_bad

        self.NLCClassifier = classifier.NLCClassifier(nlc_usr, nlc_pass)

    def run(self):
        while 1:
            threadLock1.acquire()
            if len(self.wrapperInputs.inputs) <= 0:
                threadLock1.release()
                return 
            tmpInput = self.wrapperInputs.inputs.pop()
            print('thread number: {0}'.format(self.tNum))
            threadLock1.release()

            actual_sentence = tmpInput[0]  # string of the example (input/ message)
            actual_class = tmpInput[1]  # the classified class for the matching input

            # afther getting the input from the list send it to the NLC
            answer_class = self.NLCClassifier.classify(self.classifier_name, actual_sentence)  # classified class with more confidence 

            threadLock1.acquire()
            if answer_class == '1':
                self.wrapperInputs.counter_get_2 += 1
                # when the prediction is different of 0
                self.wrapperInputs.A += 1
                threadLock1.release()

                # API CALL TO THE LEVEL-CLASSIFIER 
                answer_class = self.NLCClassifier.classify(self.classifier_bad, actual_sentence)
                threadLock1.acquire()
                        #print('bad classifier name :' ,classifier_bad) 
            print("Actual Class: ",actual_class," ","Response Class: ",answer_class,"\n")

            if actual_class == '0':
                self.wrapperInputs.T_0 += 1
                     
        # if the prediction is right  
            if actual_class == answer_class:  
                self.wrapperInputs.counter += 1
                # good prediction different of 0 (misplaced_alert)
                if actual_class != '0': 
                    self.wrapperInputs.misplaced_alerts_counter += 1
            # if the prediction is wrong        
            else:
##                print(actual_class,answer_class)
                # when the class is 0 and the prediction is different of 0(false alert)
                if actual_class == '0':
                    self.wrapperInputs.false_alerts_counter += 1
                # when the actual class is 1,2 or 3 and it predict 0
                if answer_class == '0': #else is ok too i think need to see 
                    self.wrapperInputs.missed_alerts_counter += 1
            threadLock1.release()

""" Training - Both approaches """

threadLock0 = threading.Lock()
class trainingTask (threading.Thread):
    def __init__(self, tNum, NLCAccount, file, name_classifier, nb):
        threading.Thread.__init__(self)

        self.tNum = tNum
        self.NLCAccount = NLCAccount
        self.file = file
        self.name_classifier = name_classifier
        self.nb = nb

    def run(self):
        threadLock0.acquire()
        print ('Training task, thread number: {0}'.format(self.tNum))
        threadLock0.release()
        NLC = classifier.NLCClassifier(self.NLCAccount[0], self.NLCAccount[1])
        NLC.create_classifier('../training_csv_files/' + self.file, self.name_classifier, self.nb)
