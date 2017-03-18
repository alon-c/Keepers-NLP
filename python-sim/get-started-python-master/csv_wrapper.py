import csv

import globalConfig as config

def loadCsv():
	messages_list = []
	f = open(config.CSV_FILE, 'rt')
	reader = csv.reader(f)
	for row in reader:
	    print (row)
	    print (row[2])
	    messages_list.append(row)
	f.close()

	return messages_list
