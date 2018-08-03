from config import *
import csv
import MySQLdb
import time

def write_data_to_file(data_list, data_type):
	"""convert nested json to flat csv based 
	on the column mapping defined in configuration
	"""
	start_time = time.time()
	data_file = "data/%s_%s.csv"%(data_type, str(start_time))
	with open(data_file, "w") as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=COLUMN_MAP[data_type].keys())
		writer.writeheader()
		for data in data_list:
			row_dict = {}
			for key,val in COLUMN_MAP[data_type].items():
				d = data
				for i, elem in enumerate(val):
					d = d[elem]
				row_dict.update({key: d})
			writer.writerow(row_dict)
	return data_file


def get_drop_table_stmt(data_type):
	return 'drop table if exists %s'%(data_type)

def get_create_table_stmt(data_type):
	"""Dynamically build create table statement
	"""
	col_list = map(lambda a:'%s VARCHAR(1024)'%a,COLUMN_MAP[data_type].keys())
	create_stmt = 'create table %s(%s)'%(data_type, ",".join(col_list))
	return create_stmt

def recreate_table(data_type, host, username, password, db, port=3306):
	"""Execute drop and create table ddl
	"""
	db = MySQLdb.connect(host=host, user=username, password=password, database=db, port=port)
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

def load_data_in_db(data_type, data_file, host, username, password, db, port=3306, ignore_top_lines=1):
	"""
	"""
	db = MySQLdb.connect(host=host, user=username, password=password, database=db, port=port)
	cursor = db.cursor()
	try:
		with open(data_file) as f:
			for data in f.readlines()[ignore_top_lines:]:
				try:
					col_list = map(lambda a:'%s'%a,COLUMN_MAP[data_type].keys())
					insert_stmt = "INSERT INTO %s (%s) values "%(data_type, ",".join(col_list))
					insert_stmt +=  str(tuple(data.split(",")))
					cursor.execute(insert_stmt)
				except ValueError as e:
					print("ValueError while processing %s"%data)
				except IndexError as e:
					print("IndexError while processing %s"%data)
	except Exception as e:
		raise
	finally:
		pass
		db.commit()
		db.close()