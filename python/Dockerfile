FROM bde2020/spark-python-template:3.1.1-hadoop3.2
WORKDIR /app
COPY filterModule.py filterModule.py
COPY curlCommands.py curlCommands.py
COPY requirements.txt requirements.txt
RUN    pip install -r requirements.txt
ENTRYPOINT ["python3"]
EXPOSE 5559
ENV PYTHONUNBUFFERED=1
ENV SCHEMA_ORG="organization"
ENV USE_SPARK="true"
#CMD ["filter_OPA_JWT.py"]
CMD ["filterModule.py"]
