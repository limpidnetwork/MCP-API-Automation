## Data Pipelines

### This module has a code to fetch data from MCP REST API's and store data in MySQL in raw format.

### How to start data download commands.
	1. Login in the docker `sudo docker exec -it mcp-api-automation_processor_1 /bin/bash`

### MySQL

`docker exec -it mcp-pipelines_db_1 /bin/bash`

### Data Processing

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