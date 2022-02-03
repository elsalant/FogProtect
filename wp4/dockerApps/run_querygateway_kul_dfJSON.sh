docker run --entrypoint python -v$HOME/fhir/gateway-docker-KUL:/root/fhir/gateway -e VAULT_TOKEN -e VAULT_URI="http://127.0.0.1:5000/KUL/KMS"  -e PYTHONPATH="/usr/spark-2.3.0/python/:/usr/spark-2.3.0/python/lib/py4j-0.8.2.1-src.zip" --network="host" querygateway-kul /usr/spark-2.3.0/jars/queryGateway_ProTego_dfJSON.py