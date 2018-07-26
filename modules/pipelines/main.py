from alarms import get_active_alarms
from authenticate import authorize_with_MCP
from datetime import datetime
import csv
import MySQLdb
import os
import time

USERNAME = os.environ.get('USERNAME', 'dev')
PASSWORD = os.environ.get('PASSWORD', 'cec068525')
LABID = os.environ.get('LABID', '254')

HOST = "developer.ciena.com/lab/api/%s"%(LABID)
WS_HOST = "developer.ciena.com/lab-notification/mcp/%s"%(LABID)

MYSQL_HOST = os.environ.get('MYSQL_HOST', "mcp_db")
MYSQL_USERNAME = os.environ.get('MYSQL_USERNAME', "root")
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', "limpid@123")
MYSQL_DB = "mcp"

def recreate_alarms_table():
	with open('modules/db/alarms.ddl') as ddl:
		sql_stmts = ddl.read()
		db = MySQLdb.connect(MYSQL_HOST, MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_DB)
		cursor = db.cursor()
		try:
			drop_stmt = sql_stmts.split(';')[0]
			create_stmt = sql_stmts.split(';')[1]
			cursor.execute(drop_stmt)
			cursor.execute(create_stmt)
		except Exception as e:
			raise
		finally:
			db.commit()
			db.close()

def laod_data_in_db(data_file, tablename):
	db = MySQLdb.connect(MYSQL_HOST, MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_DB)
	cursor = db.cursor()
	try:
		with open(data_file) as f:
			for data in f.readlines():
				try:
					first_raise_time = int(data.split(",")[10])/1000
					last_raise_time = int(data.split(",")[11])/1000
					insert_stmt = """INSERT INTO %s
					(id, type, attributes_id, attributes_node_id,
					attributes_node_type,attributes_resource,
					attributes_native_condition_type,attributes_condition_severity,
					attributes_manual_clearable, attributes_additional_text,
					attributes_first_raise_time, attributes_last_raise_time,
					attributes_number_of_occurrences,attributes_acknowledge_state,
					attributes_device_name, attributes_ip_address,
					attributes_mac_address)
					values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')
					"""%(tablename, data.split(",")[0], data.split(",")[1], 
						data.split(",")[2], data.split(",")[3],
						data.split(",")[4], data.split(",")[5],
						data.split(",")[6], data.split(",")[7],
						data.split(",")[8], data.split(",")[9].replace("'", " "),
						datetime.fromtimestamp(first_raise_time).strftime('%Y-%m-%d %H:%M:%S'),
						datetime.fromtimestamp(last_raise_time).strftime('%Y-%m-%d %H:%M:%S'),
						data.split(",")[12], data.split(",")[13],
						data.split(",")[14], data.split(",")[15],
						data.split(",")[16])
					cursor.execute(insert_stmt)
				except ValueError as e:
					print("ValueError while processing %s"%data)
				except IndexError as e:
					print("IndexError while processing %s"%data)
	except Exception as e:
		raise
	finally:
		db.commit()
		db.close()


def get_alarms():
	token = authorize_with_MCP(HOST, USERNAME, PASSWORD)
	return get_active_alarms(HOST, token)


def write_alarms_to_file(alarms):
	start_time = time.time()
	alarm_file = "data/alarms/%s.csv"%(str(start_time))
	
	with open(alarm_file, "w") as csvfile:
		fieldnames = ['id', 'type', 'attributes_id', 
					  'attributes_node_id', 'attributes_node_type',
					  'attributes_resource', 'attributes_native_condition_type', 
					  'attributes_condition_severity',
					  'attributes_manual_clearable', 'attributes_additional_text', 
					  'attributes_first_raise_time',
					  'attributes_last_raise_time', 'attributes_number_of_occurrences', 
					  'attributes_acknowledge_state',
					  'attributes_device_name', 'attributes_ip_address', 
					  'attributes_mac_address']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
		for alarm in alarms:
			writer.writerow({'id': str(alarm['id']), 
					'type': alarm['type'],
					'attributes_id': alarm['attributes']['id'],
					'attributes_node_id': alarm['attributes']['node-id'],
					'attributes_node_type': alarm['attributes']['node-type'],
					'attributes_resource': alarm['attributes']['resource'],
					'attributes_native_condition_type': alarm['attributes']['native-condition-type'],
					'attributes_condition_severity': alarm['attributes']['condition-severity'],
					'attributes_manual_clearable': alarm['attributes']['manual-clearable'],
					'attributes_additional_text': alarm['attributes']['additional-text'],
					'attributes_first_raise_time': alarm['attributes']['first-raise-time'],
					'attributes_last_raise_time': alarm['attributes']['last-raise-time'],
					'attributes_number_of_occurrences': alarm['attributes']['number-of-occurrences'],
					'attributes_acknowledge_state': alarm['attributes']['acknowledge-state'],
					'attributes_device_name': alarm['attributes']['device-name'],
					'attributes_ip_address': alarm['attributes']['ip-address'],
					'attributes_ip_address': alarm['attributes']['mac-address'],
					})
		return alarm_file

def main():
	alarms = get_alarms()
	alarm_file = write_alarms_to_file(alarms)
	recreate_alarms_table()
	#alarm_file = '/app/modules/pipelines/data/alarms.csv'
	laod_data_in_db(alarm_file, "alarms")


if __name__ == '__main__':
	main()
