## How to start stand-alone container to authenticate and download data from BP MCP 18x

```
docker build -t limpid-data-pipeline . && \
docker run -it --rm -e DEBUG=TRUE -e ENV=STG -e USERNAME=dev -e PASSWORD=XXXXX -e LABID=XXX -p8081:80 \
limpid-data-pipeline bash
```

### Note: In order to get the password a lab needs to be scheduled in `my.ciena.com/CienaPortal`

## How to bash in a container

### MySQL

`docker exec -it mcp-pipelines_db_1 /bin/bash`
