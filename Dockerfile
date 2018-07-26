FROM python:3.7
LABEL description="Download MCP 18x data and store transformed data in mysql"
LABEL maintainer="info@limpidnetwork.com.com"

RUN mkdir -p /app \
             /limpidnetwork/logs

RUN apt-get update && apt-get install -y apache2 libapache2-mod-wsgi
RUN apt-get install -y python-dev default-libmysqlclient-dev

WORKDIR /app
COPY requirements.txt /app/

RUN pip install --upgrade pip
RUN pip install --compile -r requirements.txt

COPY modules/ /app/modules/
RUN mkdir -p /app/data/alarms/

RUN cd /app/modules/pipelines/
