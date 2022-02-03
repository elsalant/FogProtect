
from flask import Flask, request, Response
from curlCommands import handleQuery
import urllib.parse as urlparse

import json
import re
import os
import requests
import jwt
import sys

app = Flask(__name__)

REDIRECT_SERVICE = os.getenv("QUERYGW_URI") if os.getenv("QUERYGW_URI") else "localhost:9005"
REDIRECT_PORT = 9005

ACCESS_DENIED_CODE = 403
ERROR_CODE = 406
VALID_RETURN = 200

# queryGatewayURL = "http://" + REDIRECT_SERVICE + ":" + str(REDIRECT_PORT) + "/query/"
# queryGatewayURL = "http://" + REDIRECT_SERVICE + ":" + str(REDIRECT_PORT) + "/"
queryGatewayURL = "http://" + REDIRECT_SERVICE + "/"
FIXED_SCHEMA_ROLE = 'realm_access.roles'
FIXED_SCHEMA_ORG = 'realm_access.organization'

print("queryGatewayURL = " + queryGatewayURL)

FLASK_PORT_NUM = 5559  # this application
OPA_SERVER = os.getenv("OPA_SERVER") if os.getenv("OPA_SERVER") else 'localhost'

OPA_PORT = os.getenv("OPA_SERVICE_PORT") if os.getenv("OPA_SERVICE_PORT") else 8181
OPA_FILTER_URL = os.getenv("OPA_URL") if os.getenv("OPA_URL") else '/v1/data/katalog/example/filters'
OPA_BLOCK_URL = os.getenv("OPA_URL") if os.getenv("OPA_URL") else '/v1/data/katalog/example/blockList'
ASSET_NAMESPACE = os.getenv("ASSET_NAMESPACE") if os.getenv("ASSET_NAMESPACE") else 'default'
# DATASET_NAME = os.getenv("DATASET_NAME") if os.getenv("DATASET_NAME") else 'data-csv'
OPA_HEADER = {"Content-Type": "application/json"}

TESTING = False



def composeAndExecuteCurl(role, queryURL, passedURL):
    # The assumption is that the if there are query parameters (queryString), then this is prefixed by a "?"

    parsedURL = urlparse.urlparse(passedURL)
#    asset = parsedURL.path[1:]
    asset = parsedURL[1]+parsedURL[2]
    # If we have passed parameters, asset will end in a '/' which needs to be stripped off
    if (asset[-1] == '/'):
        asset = asset[:-1]
    print("asset = " + asset)
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
    print('urlString = ' + urlString + " assetName = " + assetName + " opa_query_body " + opa_query_body)

    r = requests.post(urlString, data=opa_query_body, headers=OPA_HEADER)

    if (r is None):  # should never happen
        raise Exception("No values returned from OPA! for " + urlString + " data " + opa_query_body)
    try:
        returnString = r.json()
    except Exception as e:
        print("r.json fails - " + urlString + " data " + opa_query_body)
        raise Exception("No values returned from OPA! for " + urlString + " data " + opa_query_body)

    print('returnString = ' + str(returnString))

    return (returnString)

# @app.route('/query/<queryString>')
# def query(queryString):
# Catch anything
@app.route('/<path:queryString>',methods=['GET', 'POST', 'PUT'])
def getAll(queryString=None):
    print("queryString = " + queryString)
    print('request.url = ' + request.url)
# Support JWT token for OAuth 2.1
    noJWT = True
    payloadEncrypted = request.headers.get('Authorization')
    organization = None
    role = None
    if (payloadEncrypted != None):
        noJWT = False
        roleKey = os.getenv("SCHEMA_ROLE") if os.getenv("SCHEMA_ROLE") else FIXED_SCHEMA_ROLE
        organizationKey = os.getenv("SCHEMA_ORG") if os.getenv("SCHEMA_ORG") else FIXED_SCHEMA_ORG
        try:
            role = decryptJWT(payloadEncrypted, roleKey)
        except:
            print("Error: no role in JWT!")
            role = 'ERROR NO ROLE!'
        organization = decryptJWT(payloadEncrypted, organizationKey)
    if (noJWT):
        role = request.headers.get('role')   # testing only
    if (role == None):
        role = 'ERROR NO ROLE!'
    if (organization == None):
        organization = 'NO ORGANIZATION'
    print('role = ', role, " organization = ", organization)
    if (not TESTING):
    # Determine if the requester has access to this URL.  If the requested endpoint shows up in blockDict, then return 500
        blockDict = composeAndExecuteCurl(role, OPA_BLOCK_URL, queryString)
        for resultDict in blockDict['result']:
            blockURL = resultDict['action']
            if blockURL == "BlockURL":
                return ("Access denied!", ACCESS_DENIED_CODE)

    # Get the filter constraints from OPA
        filterDict = composeAndExecuteCurl(role, OPA_FILTER_URL, queryString)   # queryString not needed here
        print('filterDict = ' + str(filterDict))

    # Go out to the actual destination webserver
    print("queryGatewayURL= ", queryGatewayURL, "request.method = " + request.method)
    ans, returnHeaders = handleQuery(queryGatewayURL, queryString, request.headers, request.method, request.form, request.args)
    if (ans is None):
        return ("No results returned", VALID_RETURN)

    filteredLine = ''
 # The input can actually be a list, a string (JSON), or interpreted by Python to be a dict
    processing = True
    listIndex = 0
    while processing:
        processing = False
        if (type(ans) is str):
            if (returnHeaders['Content-Type'] == 'video/mp4'):  # this check might not be necessary - type should return as bytes in this case
                print("binary data found")
                return ans, VALID_RETURN
            try:
                jsonDict = json.loads(ans)
            except:
               print("Non-JSON string received! ans = " + ans)
               return('Non-JSON string received!',ERROR_CODE)
        elif (type(ans) is dict):
                jsonDict = ans
        elif (type(ans) is bytes):
            print("Binary bytes received!")
            return ans, VALID_RETURN
        elif (type(ans) is list):
            if (type(ans[listIndex]) is not dict):
                print("--> WARNING: list of " + str(type(ans[listIndex])) + " - not filtering")
                return(str(ans).replace('\'', '\"' ), VALID_RETURN)
            jsonDict = ans[listIndex]
            listIndex += 1
            if listIndex < len(ans):
                processing = True
        else:
            print("WARNING: Too complicated - not filtering")
            return (json.dumps(ans), VALID_RETURN)
  #  for line in ans:
        for resultDict in filterDict['result']:
            action = resultDict['action']
            # Handle the filtering here
            if (action == 'Deny'):
                return ('{"action":"Deny","name":"Deny by default"}', ACCESS_DENIED_CODE)
            if (action == 'Allow'):
                return (json.dumps(ans), VALID_RETURN)
            # Note: can have both "RedactColumn" and "BlockColumn" actions in line
            if (action == 'RedactColumn' or action == 'BlockColumn'):
                columns = resultDict['columns']
                for keySearch in columns:
                    recurse(jsonDict, keySearch.split('.'), action)
            if (action == 'Filter'):
                filterPred = resultDict['filterPredicate']

        filteredLine += json.dumps(jsonDict)
        print("filteredLine", filteredLine)
    return (filteredLine, VALID_RETURN)

def decryptJWT(encryptedToken, flatKey):
# String with "Bearer <token>".  Strip out "Bearer"...
    prefix = 'Bearer'
    assert encryptedToken.startswith(prefix), '\"Bearer\" not found in token' + encryptedToken
    strippedToken = encryptedToken[len(prefix):].strip()
    decodedJWT = jwt.api_jwt.decode(strippedToken, options={"verify_signature": False})
    print('decodedJWT = ', decodedJWT)
 #   flatKey = os.getenv("SCHEMA_ROLE") if os.getenv("SCHEMA_ROLE") else FIXED_SCHEMA_ROLE
# We might have an nested key in JWT (dict within dict).  In that case, flatKey will express the hierarchy and so we
# will interatively chunk through it.
    decodedKey = None
    while type(decodedJWT) is dict:
        for s in flatKey.split('.'):
            if s in decodedJWT:
                decodedJWT = decodedJWT[s]
                decodedKey = decodedJWT
            else:
                print("warning: " + s + " not found in decodedKey!")
                return decodedKey
    return decodedKey

def recurse(jDict, keySearch, action):
    try:
        i = keySearch.pop(0)
    except:
        print("Error on keySearch.pop, keySearch = " + str(keySearch))
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

app.run(port=FLASK_PORT_NUM, host='0.0.0.0')
