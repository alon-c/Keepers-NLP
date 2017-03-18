'''
Created on Feb 12, 2017

@author: Alon
'''
# -*- coding: utf-8 -*-

import classifier
import csv
import os
import tools
import matplotlib.pyplot as plt

#This file deal with all that concern the two levels classification
# create testing files
# create classifiers
# calculate accuracies
# generate graphs


# demander si lors de l'apprentissage il faut prendre les meme phrases

# create a list of classifiers for the two levels classification
def create_list_classifiers_two_levels(filename):
    files = os.listdir('../training_csv_files')
    filename = filename.split('/')
    filename = filename[len(filename) - 1]
    filename = filename.split('.')[0]
    print(filename)
    for file in files:
        if file.__contains__(filename+'_bad') or file.__contains__(filename+'_0_1'):
            nb = file.split('_')
            nb = nb[len(nb) - 1]
            nb = nb.split('.')[0]
            name_classifier = file.split('.csv')[0] + '_classifier_' + nb
            classifier.create_classifier('../training_csv_files/' + file, name_classifier,nb)


#give accuracies with the two levels classification
def accuracy_two_levels(testing_file, classifier_name, classifier_bad):

    with open(testing_file) as csvfile:
            n_row = 0
            counter = 0
            counter_get_2 = 0 
            reader = csv.reader(csvfile)
            false_alerts_counter = 0  # number of predictions is 1,2 or 3 and the actual class is 0
            misplaced_alerts_counter = 0  # number of 
            missed_alerts_counter = 0  # number of predictions is 0 and the actual class is 1,2 or 3
            A = 0  # All that the prediction is different of 0
            T_1_2_3 = 0
            T_0 = 0
            # star process 
            for row in reader:
                    n_row += 1  # number of examples into the file 
                    actual_sentence = row[0]  # string of the example
                    actual_class = row[1]  # example that we already know  the class
                    print('O_1_classifier name :' ,classifier_name)                       
                    answer_class = classifier.classify(classifier_name, actual_sentence)  # classified class with more confidence 
                   
                    if answer_class == '1':
                        counter_get_2 += 1
                        # when the prediction is different of 0
                        A += 1
                        # API CALL TO THE LEVEL-CLASSIFIER 
                        answer_class = classifier.classify(classifier_bad, actual_sentence)
                        #print('bad classifier name :' ,classifier_bad) 
                    print("Actual Class: ",actual_class," ","Response Class: ",answer_class,"\n")
                    
                    if actual_class == '0':
                        T_0 += 1
                     
                    # if the prediction is right  
                    if actual_class == answer_class:  
                        counter = counter + 1
                        # good prediction different of 0 (misplaced_alert)
                        if actual_class != '0': 
                            misplaced_alerts_counter += 1  
                            
                    # if the prediction is wrong        
                    else :
                        print(actual_class,answer_class)
                        # when the class is 0 and the prediction is different of 0(false alert)
                        if actual_class == '0':
                            false_alerts_counter += 1
                        # when the actual class is 1,2 or 3 and it predict 0
                        if answer_class == '0': #else is ok too i think need to see 
                            missed_alerts_counter += 1
            
            accuracy = (counter / n_row) * 100
            
            print('A : ', A)
            print('false alerts counter :' ,false_alerts_counter)
            print('missed alerts counter :', missed_alerts_counter)
            print('misplaced alerts counter :', misplaced_alerts_counter)
            
            false_alerts = (false_alerts_counter / A) *100
            misplaced_alerts = ((A - misplaced_alerts_counter)/A)  * 100
            T_1_2_3 = n_row - T_0
            print('T_1_2_3 : ' , T_1_2_3)
            missed_alert = (missed_alerts_counter/T_1_2_3) * 100
            
            print("Results: ", "\n" , "Number of examples: ", n_row, "\n", "Number of hits: ", counter, '\n', "Accuracy: ", accuracy, "%", '\n', "False Alerts: ", false_alerts, "%", '\n', "Missed Alerts: ", missed_alert, "%" "misplaced Alerts: ", misplaced_alerts, "%", '\n');   
            
    return accuracy, false_alerts, misplaced_alerts, missed_alert


# give the accuracies of all the classifiers for the testing_file
# return a dictionary per accuracy with the classifier and his accuracy for the two levels classification
def create_data_two_levels(testing_file, nb):
    classifiers = classifier.list_classifiers_name_id()
    accuracies = list()
    false = list()
    misplaced = list()
    missed = list()
    data_accur = dict()
    data_false = dict()
    data_misplaced = dict()
    data_missed = dict()
    for num in nb:
        for classifi in classifiers:
            if(classifi.__contains__(str(num))):
                if(classifi.__contains__('0_1')):
                    classifier_0_1 = classifi
                if(classifi.__contains__('bad_' + str(num))):
                    classifier_bad = classifi
        print(num)
        print(classifier_0_1)
        print(classifier_bad)
        accur, false_alerts, misplaced_alerts, missed_alert = accuracy_two_levels(testing_file, classifier_0_1, classifier_bad)
        accuracies.append(accur)
        misplaced.append(misplaced_alerts)
        missed.append(missed_alert)
        false.append(false_alerts)
        data_accur[num] = accur
        data_false[num] = false_alerts
        data_misplaced[num] = misplaced_alerts
        data_missed[num] = missed_alert
    return data_accur, data_false, data_misplaced, data_missed

# print(create_data_two_levels(file_name))
 

# create 4 graphs 
# one for each kind of accuracy
def create_graphs_two_levels(testing_file, nb):
    data_accur, data_false, data_misplaced, data_missed = create_data_two_levels(testing_file, nb)
    print(data_accur)
    print(data_false)
    print(data_misplaced)
    print(data_missed)
    xlabel = 'percent of the file'
    ylabel = 'accuracy'
    fig1 = plt.figure(1)
    fig1.canvas.set_window_title('Accuracy')
    tools.show_graph(data_accur, 'Accuracy', xlabel, ylabel)
    fig2 = plt.figure(2)
    fig2.canvas.set_window_title('False Alerts')
    tools.show_graph(data_false, 'False Alerts', xlabel, ylabel)
    fig3 = plt.figure(3)
    fig3.canvas.set_window_title('misplaced Alerts')
    tools.show_graph(data_misplaced, 'misplaced Alerts', xlabel, ylabel)
    fig4 = plt.figure(4)
    fig4.canvas.set_window_title('Missed Alerts')
    tools.show_graph(data_missed, 'Missed Alerts', xlabel, ylabel)
    plt.show()
