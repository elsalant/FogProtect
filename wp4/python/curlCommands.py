import json
import requests
import curlify
import base64
import re
import urllib.parse

def handleQuery(queryGatewayURL, queryString, passedHeaders, method, values, args):
  #  print("querystring = " + queryString)
    queryStringsLessBlanks = re.sub(' +', ' ', queryString)

    curlString = queryGatewayURL + urllib.parse.unquote_plus(queryStringsLessBlanks)
 #   curlString = queryGatewayURL + str(base64.b64encode(queryStringsLessBlanks.encode('utf-8')))
    if 'Host' in passedHeaders:  # avoid issues with istio gateways
      passedHeaders= dict(passedHeaders)
      passedHeaders.pop('Host')
    print("curlCommands: curlString = ", curlString)
    try:
      if (method == 'POST'):
        r = requests.post(curlString, headers=passedHeaders, data=values, params=args)
      else:
        r = requests.get(curlString, headers = passedHeaders, data=values, params=args)
    except Exception as e:
      print("Exception in handleQuery, curlString = " + curlString + ", method = " + method  + " passedHeaders = " + str(passedHeaders)  + " values = " + str(values))
      print(e.message, e.args)

    print("curl request = " + curlify.to_curl(r.request))
 #   if r.status_code != 200:
 #       return None
    if (r.status_code == 404):
      print("handleQuery: empty return!")
      return(None)
    else:
      try:
        returnList = r.json()  # decodes the response in json
      except:
        print('curlCommands: curl return is not in JSON format! Returing as binary')
        returnList = r.content
#    if re.response is None:
#        print("---> error on empty returnList in curlCommands.py")
#    else:
 #       print('[%s]' % ', '.join(map(str, returnList)))

    return (returnList, r.headers)

def decodeQuery(queryString):
    return(urllib.parse.unquote_plus(queryString))
 #   return base64.b64decode(queryString[2:-1]).decode('utf-8')
