FROM python:3.10.8
RUN mkdir -p /app_blacklist
WORKDIR /app_blacklist
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0
EXPOSE 3003
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD [ "flask", "run","-p","3003"]

##Confguración New Relic
RUN pip install newrelic
ENV NEW_RELIC_APP_NAME="docker_black_list_dt"
ENV NEW_RELIC_LOG=stdout
ENV NEW_RELIC_DISTRIBUTED_TRACING_ENABLED=true
#INGEST_License
ENV NEW_RELIC_LICENSE_KEY=a12275488c86bc62f4956977b12bfcc72c88NRAL
ENV NEW_RELIC_LOG_LEVEL=info
# etc.

ENTRYPOINT ["newrelic-admin", "run-program"]