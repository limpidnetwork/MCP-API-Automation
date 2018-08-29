## How to start stand-alone container to authenticate and download data from BP MCP 18x

```
docker-compose build
docker-compose up -d
```

### Note: Lab credentials can be specified in `docker-compose.yml`, docker makes it available as an environment variables.
### A lab needs to be scheduled in `my.ciena.com/CienaPortal` to get an active credentials.


## Deployment

### Windows

```
Install python 3.7 - 
Clone this repository
pip install -r requirements.txt

Either set the following environment variables:
 - LAB_USERNAME (default=dev)
 - LAB_PASSWORD
 - LAB_ID

 - POSTGRES_HOST
 - POSTGRES_USERNAME
 - POSTGRES_PASSWORD
 - POSTGRES_DB (default=mcp)

Or these can also be passed as a parameter to python program. See (modules/pipelines/README.md)

```