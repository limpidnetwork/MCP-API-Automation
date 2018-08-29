from config import *
from downloader import get_data
from authenticate import authorize_with_MCP

import argparse
import json
import os

USERNAME = os.environ.get('LAB_USERNAME', 'dev')
PASSWORD = os.environ.get('LAB_PASSWORD', 'cec068525')
LABID = os.environ.get('LABID', '254')

DEFAULT_HOST = os.environ.get("HOST","developer.ciena.com/lab/api/")
WS_HOST = "developer.ciena.com/lab-notification/mcp/%s"%(LABID)


def get_environment_data(key, user_arg, default=None):
	"""args passed by user overrides the environment variable
	"""
	if user_arg:
		return user_arg
	return os.environ.get(key, default)

def get_path(data_type, params={}):
	try:
		print( PATH_MAP[data_type][0].format(**params))
		return PATH_MAP[data_type][0].format(**params)
	except KeyError:
		print('data_type=%s is not supported. Supported types are=%s'%(data_type, str(list(PATH_MAP.keys()))))
		raise

def get_data_key(data_type):
	try:
		return PATH_MAP[data_type][1]
	except KeyError:
		print('data_type=%s is not supported. Supported types are=%s'%(data_type, str(list(PATH_MAP.keys()))))
		raise

def valid_dict(params):
	return json.loads(params)


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
                    required=True,
                    choices=PATH_MAP.keys())

	parser.add_argument('--recreate-table', '-r',
                    help='To recreate table in database.',
                    required=False,
                    default=True)

	parser.add_argument('--dest-db-type',
                    help='Destination database type (MySQL or Postgres',
                    default='Postgres')


	parser.add_argument('--postgres-host', '-ph',
                    help='Postgres host to store data')
	parser.add_argument('--postgres-username', '-pu',
                    help='Postgres username')
	parser.add_argument('--postgres-password',
                    help='Postgres Password')
	parser.add_argument('--postgres-db', '-pdb',
                    help='Postgres DB')
	parser.add_argument('--postgres-port',
                    help='Postgres Port',
                    default=5432)


	parser.add_argument('--params',
                    default='{}',
                    type=valid_dict,
                    help='URL parameters for MCP APIs.\
						Accepts valid dictionary as a string.\
						e.g. \'{"params":"1", "type":"mcp"}\'')

	args = parser.parse_args()

	host = get_environment_data("HOST", args.lab_host, DEFAULT_HOST)
	username = get_environment_data("LAB_USERNAME", args.lab_username, default="dev")
	password = get_environment_data("LAB_PASSWORD", args.lab_password)
	lab_id = get_environment_data("LABID", args.lab_id, default=254)

	host = "%s/%s"%(host, lab_id)

	# End-to-End data pipelines
	# 1. Authentication:
	token = authorize_with_MCP(host, username, password)

	# 2. Get Data:
	data = get_data(host, get_path(args.data_type, params=args.params), token,
		key=get_data_key(args.data_type))


	if args.dest_db_type.lower() == 'postgres':
		import postgreshelper
		# 3. convert json to jsonl
		data_file = postgreshelper.write_data_to_file(data, args.data_type)

		postgres_host = get_environment_data("POSTGRES_HOST", args.postgres_host, default='mcp_db_pg')
		postgres_username = get_environment_data("POSTGRES_USERNAME", args.postgres_username, default="limpid")
		postgres_password = get_environment_data("POSTGRES_PASSWORD", args.postgres_password)
		postgres_db = get_environment_data("POSTGRES_DB", args.postgres_db, default=POSTGRES_DB)
		postgres_port = get_environment_data("POSTGRES_PORT", args.postgres_port, default=5432)

		# 4. Recreate table in database
		if args.recreate_table:
			postgreshelper.recreate_table(args.data_type, postgres_host, postgres_username,
				postgres_password, postgres_db, postgres_port)

		postgreshelper.load_data_in_db(args.data_type, data_file, postgres_host,
			postgres_username, postgres_password, postgres_db, postgres_port)
	else:
		print("%s is not supported currently. Supported databases are MySQL and Postgres" % args.dest_db_type)
		raise


if __name__ == '__main__':
	main()
