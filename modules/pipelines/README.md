## Data Pipelines

### This module has a code to fetch data from MCP REST API's and store data in MySQL in raw format.

### Ingesting Data from MCP REST API in postgres


### Login into docker (mcp-api-automation_processor):
`sudo docker exec -it mcp-api-automation_processor_1 /bin/bash`


### Data download commands.
```
python modules/pipelines/main.py --data-type device_types --lab-password <lab-password> --dest-db-type postgres
python modules/pipelines/main.py --data-type active_alarms --lab-password <lab-password> --dest-db-type postgres
python modules/pipelines/main.py --data-type equipment --lab-password <lab-password> --dest-db-type postgres
python modules/pipelines/main.py --data-type HeatDissipationReport --lab-password <lab-password> --dest-db-type postgres
python modules/pipelines/main.py --data-type policyTypes --lab-password <lab-password> --dest-db-type postgres
python modules/pipelines/main.py --data-type policy --lab-password <lab-password> --dest-db-type postgres
python modules/pipelines/main.py --data-type policyDefaults --lab-password <lab-password> --dest-db-type postgres
python modules/pipelines/main.py --data-type networkConstructs --lab-password <lab-password> --dest-db-type postgres
python modules/pipelines/main.py --data-type tpes --lab-password <lab-password> --dest-db-type postgres
python modules/pipelines/main.py --data-type fres --lab-password <lab-password> --dest-db-type postgres
python modules/pipelines/main.py --data-type managementSessions --lab-password <lab-password> --dest-db-type postgres
```

### NOTE: 
	1. <lab-password> will be available once MCP lab is scheduled.
	2. All supported data-type are defined in config.PATH_MAP


### How to connect Postgres

`psql -h 127.0.0.1 -U limpid -d mcp -p 54321 -W
<POSTGRES_PASSWORD>`

### How to connect MySQL

`mysql -h 127.0.0.1 -u limpid -p<MYSQL_PASSWORD> -P 33061`

### NOTE: <POSTGRES_PASSWORD> or <MYSQL_PASSWORD> are same as specified in `docker-compose.yml`