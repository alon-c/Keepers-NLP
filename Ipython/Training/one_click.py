import training
import classifier
import one_level_accuracy
import tools
import two_levels_accuracy

import sys
import matplotlib.pyplot as plt

filename = '../csv_files/DoronEnglish_1032_649_383_42_100_241.csv'
nb = [15, 30, 50, 60]

# running all the experience with the first approach and gives report with the matching results
def exe_1_level(file_name, nb):
    print(file_name)
    print(nb)
    for NLCAccount in classifier.NLC_ACCOUNTS:
        NLC = classifier.NLCClassifier(NLCAccount[0], NLCAccount[1])
        NLC.delete_all_classifiers()
    training.create_training_files(file_name, nb)
    one_level_accuracy.create_list_classifiers_one_level(file_name)
    print(NLC.list_classifiers_name_id())
    one_level_accuracy.create_report_one_level(file_name, nb)

# running all the experience with the second approach and gives report with the matching results
def exe_2_levels(file_name, nb):
    print(file_name)
    print(nb)
    for NLCAccount in classifier.NLC_ACCOUNTS:
        NLC = classifier.NLCClassifier(NLCAccount[0], NLCAccount[1])
        NLC.delete_all_classifiers()
    training.create_training_files_0_1_and_bad(file_name, nb)
    two_levels_accuracy.create_list_classifiers_two_levels(file_name)
    print(NLC.list_classifiers_name_id())
    two_levels_accuracy.create_report_two_levels(file_name, nb)
 
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

# Main
if __name__ == '__main__':
    try:
        if sys.argv[1] == 'one_level':
            exe_1_level(filename, nb)
        elif sys.argv[1] == 'two_level':
            exe_2_levels(filename, nb)
        else:
            print('wrong option passed!.')
            print ('Usage: \'python {0} <one_level | two_level>'.format(sys.argv[0]))
            sys.exit(0)
    except IndexError:
        print ('Usage: \'python {0} <one_level | two_level>'.format(sys.argv[0]))
        sys.exit(0)
