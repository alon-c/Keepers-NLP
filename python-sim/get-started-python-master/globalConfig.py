# This is the global config for the 'Python Simulator'

debug=False

# Connection status constants
CONN_UP = 'conn_online'
CONN_DOWN = 'conn_offline'

# paths and files
CSV_FILE = 'Conversation_and_messages30.csv'

# This is the PSQL properties

psql_setup = True # flag to setup the psql tables from the 'ConversationsAndMessages' csv file

# the connection details
PSQL_URLDict = {
	'database': 'kyviurvb',
	'user': 'kyviurvb',
	'password': 'lpoJjzv0Um4ICVu6x42OvSXaqdngvb24',
	'host': 'qdjjtnkv.db.elephantsql.com',
	'port': 5432
}
