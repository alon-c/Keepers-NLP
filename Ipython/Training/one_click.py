'''
Created on Feb 12, 2017

@author: Alon
'''
import training
import classifier
import one_level_accuracy
import tools
import two_levels_accuracy
import matplotlib.pyplot as plt

filename = '../csv_files/DoronEnglish_1032_649_383_42_100_241.csv'
nb = [15, 30, 50, 60]

# running all the experience with the first approach and gives 4 graphs with accuracies
# one graph per accuracy
def exe_1_level(file_name, nb):
def    print(file_name)
    print(file_name)
    print(nb)
    classifier.delete_all_classifiers()
    training.create_training_files(file_name, nb)
    one_level_accuracy.create_list_classifiers_one_level(file_name)
    print(classifier.list_classifiers_name_id())
    one_level_accuracy.create_graphs_one_level(file_name, nb)

# print(classifier.list_classifiers_name_id())
# classifier.delete_by_id_classifiers()
# exe_1_level(filename, nb)  

# running all the experience with the second approach and gives 4 graphs with accuracies
# one graph per accuracy
def exe_2_levels(file_name, nb):
    # print(file_name)
    # print(nb)
    classifier.delete_all_classifiers()
    training.create_training_files_0_1_and_bad(file_name, nb)
    two_levels_accuracy.create_list_classifiers_two_levels(filename)(file_name)
    print(classifier.list_classifiers_name_id())
    two_levels_accuracy.create_graphs_two_levels(file_name, nb)

# exe_2_levels(filename, nb)  
 
# running all the experience with both approaches and gives 4 graphs with accuracies
# one graph per accuracy
def one_graphs(file_name, nb):
    print(file_name)
    print(nb)
    
    classifier.delete_all_classifiers()
    training.create_training_files(file_name, nb)
    one_level_accuracy.create_list_classifiers_one_level(file_name)
    data_accur, data_false, data_missplaced, data_missed = one_level_accuracy.create_data_one_level(file_name, nb)
    
    classifier.delete_all_classifiers()
    training.create_training_files_0_1_and_bad(file_name, nb)
    two_levels_accuracy.create_list_classifiers_two_levels(file_name)
    data_accur2, data_false2, data_missplaced2, data_missed2 = two_levels_accuracy.create_data_two_levels(file_name, nb)
    
    xlabel = 'percent of the data'
    ylabel = 'accuracy'
    fig1 = plt.figure(1)
    fig1.canvas.set_window_title('Accuracy')
    tools.show_two_graphs(data_accur, data_accur2, 'Accuracy', xlabel, ylabel)
    fig2 = plt.figure(2)
    fig2.canvas.set_window_title('False Alerts')
    tools.show_two_graphs(data_false, data_false2, 'False Alerts', xlabel, ylabel)
    fig3 = plt.figure(3)
    fig3.canvas.set_window_title('Missplaced Alerts')
    tools.show_two_graphs(data_missplaced, data_missplaced2, 'Missplaced Alerts', xlabel, ylabel)
    fig4 = plt.figure(4)
    fig4.canvas.set_window_title('Missed Alerts')
    tools.show_two_graphs(data_missed, data_missed2, 'Missed Alerts', xlabel, ylabel)
    plt.show()
    
one_graphs(filename, nb) 
