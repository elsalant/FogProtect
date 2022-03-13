FROM python:3.8-slim

WORKDIR /app
COPY filter_OPA_JWT.py filter_OPA_JWT.py
COPY curlCommands.py curlCommands.py
COPY requirements.txt requirements.txt
RUN    pip install -r requirements.txt
RUN ["apt-get", "update"]
RUN ["apt-get", "install", "-y", "vim"]
ENTRYPOINT ["python3"]
EXPOSE 5559
ENV PYTHONUNBUFFERED=1
ENV SCHEMA_ORG="organization"
CMD ["filter_OPA_JWT.py"]
