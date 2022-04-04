from flask import Flask, request, Response
from curlCommands import handleQuery
import urllib.parse as urlparse

import json
import re
import os
import requests
import jwt
import sys
import logging

from kafka import KafkaProducer
from datetime import datetime

# Use Spark by default unless disabled in Dockerfile env
USE_SPARK = False if os.getenv("USE_SPARK").lower() in ('false', '0', 'f') else True
if USE_SPARK:
    from pyspark.sql import SQLContext
    from pyspark.sql import SparkSession

app = Flask(__name__)

REDIRECT_SERVICE = os.getenv("QUERYGW_URI") if os.getenv("QUERYGW_URI") else "localhost:9005"
REDIRECT_PORT = 9005

ACCESS_DENIED_CODE = 403
ERROR_CODE = 406
VALID_RETURN = 200

queryGatewayURL = "http://" + REDIRECT_SERVICE + "/"
FIXED_SCHEMA_USER = 'realm_access.user'
FIXED_SCHEMA_ROLE = 'realm_access.roles'
FIXED_SCHEMA_ORG = 'organization'

logger = logging.getLogger(__name__)

logger.info(f"queryGatewayURL: {queryGatewayURL}")

FLASK_PORT_NUM = 5559  # this application
OPA_SERVER = os.getenv("OPA_SERVER") if os.getenv("OPA_SERVER") else 'localhost'

OPA_PORT = os.getenv("OPA_SERVICE_PORT") if os.getenv("OPA_SERVICE_PORT") else 8181
OPA_FILTER_URL = os.getenv("OPA_URL") if os.getenv("OPA_URL") else '/v1/data/katalog/example/filters'
OPA_BLOCK_URL = os.getenv("OPA_URL") if os.getenv("OPA_URL") else '/v1/data/katalog/example/blockList'
ASSET_NAMESPACE = os.getenv("ASSET_NAMESPACE") if os.getenv("ASSET_NAMESPACE") else 'default'
# DATASET_NAME = os.getenv("DATASET_NAME") if os.getenv("DATASET_NAME") else 'data-csv'
OPA_HEADER = {"Content-Type": "application/json"}

TESTING = False
kafkaDisabled = False
kafkaAwaitingFirstConnect = True

KAFKA_SERVER = os.getenv("FOGPROTECT_KAFKA_SERVER") if os.getenv("FOGPROTECT_KAFKA_SERVER") else "127.0.0.1:9092"
KAFKA_DENY_TOPIC = os.getenv("KAFKA_DENY_TOPIC") if os.getenv("KAFKA_DENY_TOPIC") else "blocked-access"
KAFKA_ALLOW_TOPIC = os.getenv("KAFKA_ALLOW_TOPIC") if os.getenv("KAFKA_ALLOW_TOPIC") else "granted-access"

def connectKafka():
    global kafkaAwaitingFirstConnect
    global kafkaDisabled
    global producer
# Set up Kafka connection
    if kafkaDisabled == False and kafkaAwaitingFirstConnect:
        try:
            producer = KafkaProducer(
                bootstrap_servers=[KAFKA_SERVER],
                max_block_ms = 5000,
            )  # , value_serializer=lambda x:json.dumps(x).encode('utf-8'))
        except Exception as e:
            logger.warning(f"Connection to Kafka failed.  Is the server on {KAFKA_SERVER} running?")
            logger.warning(f"{e}")
            kafkaDisabled = True
        kafkaAwaitingFirstConnect = False

def composeAndExecuteCurl(role, queryURL, passedURL):
    # The assumption is that the if there are query parameters (queryString), then this is prefixed by a "?"

    parsedURL = urlparse.urlparse(passedURL)
    asset = parsedURL[1]+parsedURL[2]
    # If we have passed parameters, asset will end in a '/' which needs to be stripped off
    if (asset[-1] == '/'):
        asset = asset[:-1]
    logger.info(f"asset = : {asset}")
    assetName = asset.replace('/', '.').replace('_','-')
 ## TBD - role is being put into the header as a string - it should go in as a list for Rego.  What we are doing
 ## now requires the Rego to do a substring search, rather than search in a list

    opa_query_body = '{ \"input\": { \
\"request\": { \
\"operation\": \"READ\", \
\"role\": \"' + str(role) + '\", \
\"asset\": { \
\"namespace\": \"' + ASSET_NAMESPACE + '\", \
\"name\": \"' + assetName + '\" \
}  \
}  \
}  \
}'

    urlString = 'http://' + OPA_SERVER + ":" + str(OPA_PORT) + queryURL
    logger.info(f"urlString = {urlString}, assetName = {assetName}, opa_query_body = {opa_query_body}")

    r = requests.post(urlString, data=opa_query_body, headers=OPA_HEADER)

    if (r is None):  # should never happen
        raise Exception("No values returned from OPA! for " + urlString + " data " + opa_query_body)
    try:
        returnString = r.json()
    except Exception as e:
        logger.error(f"r.json fails - {urlString}, data = {opa_query_body}")
        raise Exception("No values returned from OPA! for " + urlString + " data " + opa_query_body)
    logger.info(f"returnString = {returnString}")
    return (returnString)

# @app.route('/query/<queryString>')
# def query(queryString):
# Catch anything
@app.route('/<path:queryString>',methods=['GET', 'POST', 'PUT'])
def getAll(queryString=None):
    logger.info(f"getAll: queryString = {queryString}, request.url = {request.url}")
# Support JWT token for OAuth 2.1
    noJWT = True
    headers = request.headers
    headersList = dict(request.headers.to_wsgi_list())
    payloadEncrypted = request.headers.get('Authorization')
    if (payloadEncrypted != None):
        noJWT = False
        userKey = os.getenv("SCHEMA_USER") if os.getenv("SCHEMA_USER") else FIXED_SCHEMA_USER
        roleKey = os.getenv("SCHEMA_ROLE") if os.getenv("SCHEMA_ROLE") else FIXED_SCHEMA_ROLE
        try:
            user = str(decryptJWT(payloadEncrypted, userKey))
        except:
            user = 'No user defined'
        role = str(decryptJWT(payloadEncrypted, roleKey))
        organizationKey = os.getenv("SCHEMA_ORG") if os.getenv("SCHEMA_ORG") else FIXED_SCHEMA_ORG
        organization = str(decryptJWT(payloadEncrypted, organizationKey))
    if (noJWT):
        role = request.headers.get('role')   # testing only
        try:
            user = request.headers.get('user')
        except:
            user = 'No user defined'
    if (role == None):
        role = 'ERROR NO ROLE!'
    logger.info(f"role = {role}")
    if (not TESTING):
    # Determine if the requester has access to this URL.  If the requested endpoint shows up in blockDict, then return 500
        blockDict = composeAndExecuteCurl(role, OPA_BLOCK_URL, queryString)
        timeOut = datetime.timestamp(datetime.now())

        for resultDict in blockDict['result']:
            actionOnURL = resultDict['action']
            jString = "{\"user\": " + user + \
                      "\"role\": " + role + \
                      ", \"org\": " + organization + \
                      ", \"URL\": \"" + str(request.url) + "\""  + \
                      ", \"Reason\": \"" + str(resultDict['name']) + "\"" + \
                      ", \"Timestamp\" : " + "\"" + str(timeOut) + "\"}"
            jStringFormatted = jString.replace("'", "\"")
            if actionOnURL == "BlockURL":
                logToKafka(jStringFormatted, KAFKA_DENY_TOPIC)
                return ("Access denied!", ACCESS_DENIED_CODE)
            else:
                logToKafka(jStringFormatted, KAFKA_ALLOW_TOPIC)

    # Get the filter constraints from OPA
        filterDict = composeAndExecuteCurl(role, OPA_FILTER_URL, queryString)   # queryString not needed here
        logger.info(f"filterDict = {filterDict}")
        logger.info(f"queryGatewayURL = {queryGatewayURL}, request.method = {request.method}")
    # Go out to the actual destination webserver
    try:
        if request.form:
            ans, returnHeaders = handleQuery(queryGatewayURL, queryString, headersList, request.method, request.form, request.args)
        else:
            ans, returnHeaders = handleQuery(queryGatewayURL, queryString, headersList, request.method, request.data,
                                             request.args)
    except:
        return ("No results returned", VALID_RETURN)

    filteredLine = ''
 # The input can actually be a list, a string (JSON), or interpreted by Python to be a dict
    processing = True
    listIndex = 0
    while processing:
        processing = False
        if (type(ans) is str):
            try:
                jsonDict = json.loads(ans)
            except:
                logger.info(f"Non-JSON string received! ans = {ans}")
                return('Non-JSON string received!',ERROR_CODE)
        elif (type(ans) is dict):
                jsonDict = ans
        elif (type(ans) is bytes):
            logger.info(f"Binary bytes received!")
            return ans, VALID_RETURN
        elif (type(ans) is list):
            if (type(ans[listIndex]) is not dict):
                logger.warning(f"WARNING: list of {str(type(ans[listIndex]))} - not filtering")
                r = cleanReturn(str(ans).replace('\'', '\"' ), returnHeaders)
                return r
            jsonDict = ans[listIndex]
            listIndex += 1
            if listIndex < len(ans):
                processing = True
        else:
            logger.warning(f"WARNING: Too complicated - not filtering")
            r = cleanReturn(str(ans), returnHeaders)
            return(r)
        for resultDict in filterDict['result']:
            action = resultDict['action']
            # Handle the filtering here
            if (action == 'Deny'):
                return ('{"action":"Deny","name":"Deny by default"}', ACCESS_DENIED_CODE)
            if (action == 'Allow'):
                r = cleanReturn(json.dumps(ans), returnHeaders)
                return r, VALID_RETURN
            # Note: can have both "RedactColumn" and "BlockColumn" actions in line
            if (action == 'RedactColumn' or action == 'BlockColumn'):
                columns = resultDict['columns']
                for keySearch in columns:
                    recurse(jsonDict, keySearch.split('.'), action)
            if (action == 'FilterPred'):
                filterPred = resultDict['filterPredicate']
                queryKey = resultDict['token']
                replaceSymbol = resultDict['replaceMe']
                queryPred = decryptJWT(payloadEncrypted, queryKey)
 # Replace token from policy with actual value from JWT
                filterPred = filterPred.replace(replaceSymbol, queryPred)
                logger.info(f"filterPred = {filterPred}, queryKey = {queryKey}, queryPred = {queryPred}")
                jsonRet = sqlSetup(ans, filterPred, queryPred)
                logger.info(f"jsonRet = {jsonRet}")
                r = cleanReturn(json.dumps(jsonRet), returnHeaders)
                return r, VALID_RETURN

        filteredLine += json.dumps(jsonDict)
        logger.info(f"filteredLine = {filteredLine}")
    r = cleanReturn(filteredLine, returnHeaders)
    return r, VALID_RETURN

def cleanHeader(r):
  if 'Content-Length' in r.headers:  # content-length will be recalculated anyway
    r.headers.pop('Content-Length')
  if 'Access-Control-Allow-Origin' in r.headers:  # required by SmartMedia use case for some reason...
    r.headers.pop('Access-Control-Allow-Origin')
  return (r)

def cleanReturn(responseLine, passedHeaders):
    r = Response(response=responseLine, status=VALID_RETURN)
    r = cleanHeader(r)
    if 'Content-Type' in passedHeaders:
      r.headers['Content-Type'] = passedHeaders['Content-Type']
    return r

def decryptJWT(encryptedToken, flatKey):
# String with "Bearer <token>".  Strip out "Bearer"...
    prefix = 'Bearer'
    assert encryptedToken.startswith(prefix), '\"Bearer\" not found in token' + encryptedToken
    strippedToken = encryptedToken[len(prefix):].strip()
    decodedJWT = jwt.api_jwt.decode(strippedToken, options={"verify_signature": False})
    logger.info(f"decodedJWT = {decodedJWT}")
# We might have an nested key in JWT (dict within dict).  In that case, flatKey will express the hierarchy and so we
# will interatively chunk through it.
    decodedKey = None
    while type(decodedJWT) is dict:
        for s in flatKey.split('.'):
            if s in decodedJWT:
                decodedJWT = decodedJWT[s]
                decodedKey = decodedJWT
            else:
                logger.warning(f"{s} not found in decodedKey!")
                return decodedKey
    return decodedKey

def recurse(jDict, keySearch, action):
    try:
        i = keySearch.pop(0)
    except:
        logger.error(f"Error on keySearch.pop, keySearch = {str(keySearch)}")
        return(jDict)
    while i in jDict:
        last = jDict[i]
        if not keySearch:
            if action == 'RedactColumn':
                jDict[i] = 'XXX'
            else:
                del jDict[i]
            return(jDict)
        else:
            recurse(jDict[i], keySearch, action)
            return(jDict)

if USE_SPARK:
    def sqlSetup(ans, filterPred,keyValue):
        spark = SparkSession.builder.appName("filter_OPA_spark").config("spark.jars.ivy", "/tmp/.ivy").master("local[*]").getOrCreate()
        sc = spark.sparkContext
        sqlContext = SQLContext(sc)
        print("sqlSetup - type(ans) = " + str(type(ans)))
        if (type(ans) is list):
            df = spark.read.json(sc.parallelize(ans))
        else:
            if (type(ans) is dict):
                # hack for use case
                if 'videos' in ans:
                    cleanDict = ans['videos']
                    SMART_MEDIA_HACK = True
                    df = spark.createDataFrame(cleanDict)
                else:
                    df = spark.createDataFrame(ans)
     #           df = spark.createDataFrame(ans)
        df.show()
        df.createOrReplaceTempView("results")
        sqlStatement = "select * from results " + filterPred
        # Replace in sqlStatement the actual value of organization with values from JWT token
        sqlDF = spark.sql(sqlStatement)
        jsonReturn = sqlDF.toJSON().collect()
        # jsonReturn is a list of json strings.  Need to convert to a list of json
        jsonCleaned = [json.loads(i) for i in jsonReturn]
        if SMART_MEDIA_HACK:
            SMART_MEDIA_HACK = False
            jsonCleaned = {'videos' : jsonCleaned}   # put things back the way they were...
        return jsonCleaned

def logToKafka(jString, kafka_topic):
    global kafkaDisabled

    if kafkaAwaitingFirstConnect == True:
        connectKafka()
    if (kafkaDisabled):
        return
    jSONoutBytes = str.encode(jString)
    try:
        logging.info(f"Writing to Kafka queue {kafka_topic}: {jString}")
        producer.send(kafka_topic, value=jSONoutBytes)  # to the SIEM
    except Exception as e:
        logger.warning(f"Write to Kafka failed.  Is the server on {KAFKA_SERVER} running?")
        logger.warning(f"{e}")
        kafkaDisabled = True

app.run(port=FLASK_PORT_NUM, host='0.0.0.0')
