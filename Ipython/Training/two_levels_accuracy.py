import classifier
import tools
from threadWrapper import wrapperInputs_two, classifierTask_two, trainingTask

import csv
import os
import matplotlib.pyplot as plt

###
# represents the two level classification for the 'NLC tool'
#
# Author: Alon Cohen Zada
###

# -*- coding: utf-8 -*-

#This script deals with all that concerns the two levels classification:
# create testing files
# create classifiers
# calculate accuracies
# generate report


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

            threads = [] # threads list
            i = 0 # thread number
            for NLCAccount in classifier.NLC_ACCOUNTS:
                threads.append(trainingTask(i, NLCAccount, file, name_classifier, nb))
                i += 1

            for  thread in threads:
                thread.start()

            for  thread in threads:
                thread.join()

#give accuracies with the two levels classification
def accuracy_two_levels(testing_file, classifier_name, classifier_bad):
    n_row = 0
    inputs = [] # list of inputs from the file
    with open(testing_file) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                    n_row += 1  # number of examples in the file
                    inputs.append(row) # appending the rows from the file to a list

    # Start process
    WI = wrapperInputs_two()
    WI.inputs = inputs
    threads = []
    i = 0
    for NLCAccount in classifier.NLC_ACCOUNTS:
        threads.append(classifierTask_two(i, WI, classifier_name, NLCAccount[0], NLCAccount[1], classifier_bad))
        print ('i', i)
        print ('account name:', NLCAccount[0])
        i += 1

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    counter = WI.counter
    counter_get_2 = WI.counter_get_2
    false_alerts_counter = WI.false_alerts_counter  # number of predictions is 1,2 or 3 and the actual class is 0
    misplaced_alerts_counter = WI.misplaced_alerts_counter  # number of 
    missed_alerts_counter = WI.missed_alerts_counter  # number of predictions is 0 and the actual class is 1,2 or 3
    A = WI.A # All that the prediction is different of 0
    T_1_2_3 = WI.T_1_2_3
    T_0 = WI.T_0

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
    NLC = classifier.NLCClassifier(classifier.NLC_ACCOUNTS[0][0], classifier.NLC_ACCOUNTS[0][1])
    classifiers = NLC.list_classifiers_name_id()
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

	# this function creates a csv file witch can be opend with excel and read as a table for the results
def create_report_two_levels(testing_file, nb):
    res_accur, res_false, res_misplaced, res_missed = create_data_two_levels(testing_file, nb)

    # printing the dicts of the results
    print ('---\nprinting results\n---')
    print(res_accur)
    print(res_accur.keys())
    print(res_accur.values())
    print(res_false)
    print(res_false.keys())
    print(res_false.values())
    print(res_misplaced)
    print(res_misplaced.keys())
    print(res_misplaced.values())
    print(res_missed)
    print(res_missed.keys())
    print(res_missed.values())
    # printing to a CSV file
    target_file = testing_file + '-res.csv'
    myfile = open(target_file , 'w')
    wr = csv.writer(myfile )

    # write percent headlines
    headLines = []
    headLines.append('percent')
    headLines.extend(res_accur.keys())
    wr.writerow(headLines)

    #write Accuracys
    tmp =[]
    tmp.append('Accuracy')
    tmp.extend(res_accur.values())
    wr.writerow(tmp)

    # write False Alerts
    tmp = []
    tmp.append('False Alerts')
    tmp.extend(res_false.values())
    wr.writerow(tmp)

    # write misplaced Alerts
    tmp = []
    tmp.append('misplaced Alerts')
    tmp.extend(res_misplaced.values())
    wr.writerow(tmp)

    # write Missed Alerts
    tmp = []
    tmp.append('Missed Alerts')
    tmp.extend(res_missed.values())
    wr.writerow(tmp)
