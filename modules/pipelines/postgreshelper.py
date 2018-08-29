from config import *
import json
import psycopg2
import time

def write_data_to_file(data_list, data_type):
	"""convert nested json to flat csv based 
	on the column mapping defined in configuration
	"""
	start_time = time.time()
	data_file = "data/%s_%s.jsonl"%(data_type, str(start_time))
	with open(data_file, "w") as jsonfile:
		for data in data_list:
			jsonfile.write(json.dumps(data))
			jsonfile.write("\n")
	return data_file

def get_drop_table_stmt(data_type):
	return 'drop table if exists %s'%(data_type)


def get_create_table_stmt(data_type):
	"""Dynamically build create table statement
	"""
	create_stmt = 'create table %s(info json)'%(data_type)
	return create_stmt

def recreate_table(data_type, host, username, password, db, port=5432):
	"""Execute drop and create table ddl
	"""
	db = psycopg2.connect("dbname=%s user=%s host=%s password=%s port=%s"%(db, username, host, password, port))
	cursor = db.cursor()
	try:
		drop_stmt = get_drop_table_stmt(data_type)
		create_stmt = get_create_table_stmt(data_type)
		cursor.execute(drop_stmt)
		cursor.execute(create_stmt)
	except Exception as e:
		raise
	finally:
		db.commit()
		db.close()

def load_data_in_db(data_type, data_file, host, username, password, 
			db, port=5432, ignore_top_lines=0):
	"""
	"""
	db = psycopg2.connect("dbname=%s user=%s host=%s password=%s port=%s"%(db, username, host, password, port))
	cursor = db.cursor()
	try:
		with open(data_file) as f:
			for json_line in f.readlines()[ignore_top_lines:]:
				try:
					insert_stmt = "INSERT INTO %s (info) values ('%s')"%(data_type, json_line.replace("'", ''))
					cursor.execute(insert_stmt)
				except ValueError as e:
					print("ValueError while processing %s"%json_line)
				except IndexError as e:
					print("IndexError while processing %s"%json_line)
	except Exception as e:
		raise
	finally:
		pass
		db.commit()
		db.close()
