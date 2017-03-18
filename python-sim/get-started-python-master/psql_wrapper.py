import psycopg2
import traceback

import globalConfig as config
from csv_wrapper import loadCsv

class PSQLConnector:
	def __init__(self, URLDict):
		print ('trying to connect to psql db')
		print (URLDict)

		self._PSQLDict = URLDict
		self._conn = None
		self._connection_status = config.CONN_DOWN
		self._cur = None

		try:
		#    conn = psycopg2.connect("dbname='kyviurvb' user='dbuser' host='localhost' password='dbpass'")
			connCmd = 'host={0} user={1} password={2} dbname={3} port={4}'.format(URLDict['host'], URLDict['user'], URLDict['password'], URLDict['database'], URLDict['port'])
			print (connCmd)
			self._conn = psycopg2.connect(connCmd)
		except psycopg2.Error as e:
			print ("I am unable to connect to the database")
			print (e)
			print(e.pgcode)
			print (e.pgerror)
			print (traceback.format_exc())
			self._conn = None

		if self._conn != None:
#			self._cur = self._conn.cursor()
			self._connection_status = config.CONN_UP
			print ('Connected to psql successfully')
		else:
			print("unable to connect is null")
			self._connection_status = config.CONN_DOWN


	def close(self):
		if self._conn == None or self._connection_status == config.CONN_DOWN:
			return

		if self._cur != None:
			self._cur.close()
			self._cur = None

		self._conn.close()

	# setup the db tables and values via csv file
	def setupDB(self):
		if self._connection_status == config.CONN_DOWN:
			return

		if config.psql_setup == False:
			return

		self._messages_list = loadCsv()
		print (' in setupe')
		print (self._messages_list[0][0])

#		self.create_classification_table()
#		self.create_conversation_table()
#		self.create_message_table()
#		self.create_test_conversation_type_table()
#		self.create_test_table()
#		self.create_test_message_table()

	def create_classification_table(self):
		if self._connection_status == config.CONN_DOWN:
			return

		if self._cur != None:
			self._cur.close()
			self._cur = None

		self._cur = self._conn.cursor()
		self._cur.execute("select exists(select * from information_schema.tables where table_name=%s)", ('classification_table',))
		self._conn.commit()
		if self._cur.fetchone()[0] == True:
			print('true is db')
			if self._cur !=None:
				self._cur.close()
				self._cur = None
			return

		if self._cur != None:
			self._cur.close()
			self._cur = None

		print('in calssfication create table')
		self._cur = self._conn.cursor()
		if self._cur != None:
			print ('create classification table curr not null')

		try:
			self._cur.execute("CREATE TABLE classification_table (classification_id serial PRIMARY KEY, classification varchar(30));")
		except: # Exception:
			print ('cannot create classification table')
			if self._cur != None:
				self._cur.close()
				self._cur = None

		self._conn.commit()

		if self._cur != None:
						self._cur.close()
						self._cur = None

		self._cur = self._conn.cursor()

		if self._cur == None:
			print ('cur is None')
		self.__NEGATIVE_SOFT_VALUE = self._cur.execute("INSERT INTO classification_table(classification) VALUES(%s) RETURNING classification_id;", ('negative-soft',))
#		self._conn.commit()
		self.__NEGATIVE_HARD_VALUE = self._cur.execute("INSERT INTO classification_table(classification) VALUES(%s) RETURNING classification_id;", ('negative-hard',))
#		self._conn.commit()
		self.__NP_VALUE = self._cur.execute("INSERT INTO classification_table(classification) VALUES(%s) RETURNING classification_id;", ('nutral/positive',))
		self._conn.commit()

		if self._cur != None:
			self._cur.close()
			self._cur = None

	def create_conversation_table(self):
		if self._connection_status == config.CONN_DOWN:
			return

		if self._cur != None:
			self._cur.close()
			self._cur = None

		self._cur = self._conn.cursor()

		self._cur.execute("select exists(select * from information_schema.tables where table_name=%s)", ('conversation_table',))
		self._conn.commit()
		if self._cur.fetchone()[0] == True:
			self._cur.close()
			self._cur = None
			return

		if self._cur != None:
			self._cur.close()
			self._cur = None

		self._cur = self._conn.cursor()

		self._cur.execute("CREATE TABLE conversation_table (conversation_id integer PRIMARY KEY, classification_id integer, constraint fk_conversations_classifications foreign key (classification_id) REFERENCES classification_table (classification_id));")
		self._conn.commit()

		if self._cur !=None:
			self._cur.close()
			self._cur = None

		self._cur = self._conn.cursor()

		for row in self._messages_list:
			if row[-1].startswith('negative-soft'):
			self._cur.execute("INSERT INTO conversation_table(conversation_id, classification_id) VALUES(%s, %s) RETURNING conversation_id;", (row[1], self.__NEGATIVE_SOFT_VALUE,))
			if row[-1].startswith('negative-hard'):
			self._cur.execute("INSERT INTO conversation_table(conversation_id, classification_id) VALUES(%s, %s) RETURNING conversation_id;", (row[1], self.__NEGATIVE_HARD_VALUE,))
			if row[-1].startswith('nutral/positive'):
			self._cur.execute("INSERT INTO conversation_table(conversation_id, classification_id) VALUES(%s, %s) RETURNING conversation_id;", (row[1], self.__NP_VALUE,))

		self._conn.commit()

		if self._cur !=None:
			self._cur.close()
			self._cur = None

	def create_message_table(self):
		if self._connection_status == config.CONN_DOWN:
			return

		if self._cur != None:
			self._cur.close()
			self._cur = None

		self._cur = self._conn.cursor()

		self._cur.execute("select exists(select * from information_schema.tables where table_name=%s)", ('message_table',))
		self._conn.commit()
		if self._cur.fetchone()[0] == True:
			if self._cur != None:
				self._cur.close()
				self._cur = None
			return

		if self._cur != None:
			self._cur.close()
			self._cur = None

		self._cur = self._conn.cursor()

	 			self._cur.execute("CREATE TABLE message_table (message_id serial PRIMARY KEY, message text, conversation_id integer, constraint fk_messages_conversations foreign key (conversation_id) REFERENCES conversation_table (conversation_id), classification_id integer, constraint fk_messages_classifications foreign key (classification_id) REFERENCES classification_table (classification_id));")
		self._conn.commit()

		self._cur.execute("INSERT INTO conversation_table(conversation_id, classification_id) VALUES(%s, %s) RETURNING conversation_id;", (row[1], self.__NP_VALUE,))

		self._conn.commit()

		if self._cur != None:
			self._cur.close()
			self._cur = None

	def create_test_conversation_type_table(self):
		if self._connection_status == config.CONN_DOWN:
			return

		self._cur.execute("select exists(select * from information_schema.tables where table_name=%s)", ('test_conversation_type_table',))
		self._conn.commit()
		if self._cur.fetchone()[0] == True:
			return

		self._cur.execute("CREATE TABLE test_conversation_type_table (type_id serial PRIMARY KEY, type varchar(30));")
		self._conn.commit()

	def create_test_table(self):
		if self._connection_status == config.CONN_DOWN:
			return

		self._cur.execute("select exists(select * from information_schema.tables where table_name=%s)", ('test_table',))
		self._conn.commit()
		if self._cur.fetchone()[0] == True:
			return

		self._cur.execute("CREATE TABLE test_table (test_id serial PRIMARY KEY, precision_grade real, recall_grade real);")
		self._conn.commit()

	def create_test_message_table(self):
		if self._connection_status == config.CONN_DOWN:
			return

		self._cur.execute("select exists(select * from information_schema.tables where table_name=%s)", ('test_message_table',))
		self._conn.commit()
		if self._cur.fetchone()[0] == True:
			return

		self._cur.execute("CREATE TABLE test_message_table (test_id integer, constraint fk_tests_tests foreign key (test_id) REFERENCES test_table (test_id), conversation_id integer, constraint fk_tests_conversations foreign key (conversation_id) REFERENCES conversation_table (conversation_id), type_id integer, constraint fk_tests_typess foreign key (type_id) REFERENCES test_conversation_type_table (type_id));")
		self._conn.commit()
