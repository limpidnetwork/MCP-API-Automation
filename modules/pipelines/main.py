from config import *
from downloader import get_data
from authenticate import authorize_with_MCP
from datetime import datetime

import argparse
import csv
import MySQLdb
import os
import time

USERNAME = os.environ.get('USERNAME', 'dev')
PASSWORD = os.environ.get('PASSWORD', 'cec068525')
LABID = os.environ.get('LABID', '254')

DEFAULT_HOST = os.environ.get("HOST","developer.ciena.com/lab/api/")
WS_HOST = "developer.ciena.com/lab-notification/mcp/%s"%(LABID)

MYSQL_HOST = os.environ.get('MYSQL_HOST', "mcp_db")
MYSQL_USERNAME = os.environ.get('MYSQL_USERNAME', "root")
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', "limpid@123")
MYSQL_DB = "mcp"

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


def get_environment_data(key, user_arg, default=None):
	"""args passed by user overrides the environment variable
	"""
	if user_arg:
		return user_arg
	return os.environ.get(key, default)

def get_path(data_type):
	try:
		return PATH_MAP[data_type]
	except KeyError:
		print('data_type=%s is not supported. Supported types are=%s'%(data_type, str(list(PATH_MAP.keys()))))
		raise

def main():
	parser = argparse.ArgumentParser(description='Ingest Blue Planet data using REST API.\
		Lab Username, Password and Id can also be set as an environment variables.')

	parser.add_argument('--lab-host', '-lh',
                    help='Cienna Emulation Cloud, Lab Host')
	parser.add_argument('--lab-username', '-lu',
                    help='Cienna Emulation Cloud, Lab Username')
	parser.add_argument('--lab-password', '-lp',
                    help='Cienna Emulation Cloud, Lab Password')
	parser.add_argument('--lab-id', '-lid',
                    help='Cienna Emulation Cloud, Lab Id')


	parser.add_argument('--data-type', '-dt',
                    help='Type of data (alarms, user, device, connections) to pull from MCP',
                    required=True)

	parser.add_argument('--recreate-table', '-r',
                    help='To recreate table in database.',
                    required=False,
                    default=True)

	parser.add_argument('--mysql-host', '-mh',
                    help='MySQL host to store data')
	parser.add_argument('--mysql-username', '-mu',
                    help='MySQL username')
	parser.add_argument('--mysql-password', '-mp',
                    help='MySQL Password')
	parser.add_argument('--mysql-db', '-db',
                    help='MySQL DB')
	parser.add_argument('--mysql-port', '-p',
                    help='MySQL Port',
                    default=3306)


	args = parser.parse_args()

	host = get_environment_data("HOST", args.lab_host, DEFAULT_HOST)
	username = get_environment_data("USERNAME", args.lab_username, default="dev")
	password = get_environment_data("PASSWORD", args.lab_password)
	lab_id = get_environment_data("LABID", args.lab_id, default=254)


	host = "%s/%s"%(host, lab_id)

	# End-to-End data pipelines
	# 1. Authentication:
	token = authorize_with_MCP(host, username, password)

	# 2. Get Data:
	data = get_data(host, get_path(args.data_type), token)

	# 3. convert json to flat csv
	data_file = write_data_to_file(data, args.data_type)


	mysql_host = get_environment_data("MYSQL_HOST", args.mysql_host, default='mcp_db')
	mysql_username = get_environment_data("MYSQL_USERNAME", args.mysql_username, default="dev")
	mysql_password = get_environment_data("MYSQL_PASSWORD", args.mysql_password)
	mysql_db = get_environment_data("MYSQL_DB", args.mysql_db, default=MYSQL_DB)
	mysql_port = get_environment_data("PORT", args.mysql_port, default=3306)

	# 4. Recreate table in database
	if args.recreate_table:
		recreate_table(args.data_type, mysql_host, mysql_username, mysql_password, mysql_db, mysql_port)

	load_data_in_db(args.data_type, data_file, mysql_host, mysql_username, mysql_password, mysql_db, mysql_port)


if __name__ == '__main__':
	main()
