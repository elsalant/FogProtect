#
# (C) Copyright IBM Corp. 2019
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from flask import Flask
from flask import request

FLASK_PORT_NUM = 9005
app = Flask(__name__)

@app.route('/')
@app.route('/<path:queryString>')
def getAll(queryString=None):
    jdf = """[{
		"code_coding[0]_code": "9279-1",
		"code_coding[0]_display": "ProTego demo",
		"code_coding[0]_system": "http://loinc.org",
		"code_text": "ProTego example",
		"extension[0]_url": "http://protego.eu/mealPortion",
		"extension[0]_valueString": "breakfast: [spam and eggs]",
		"id": "009",
		"resourceType": "Observation",
		"status": "final",
		"valueQuantity_unit": "gram",
		"valueQuantity_value": 459.1
	},
	{
		"code_coding[0]_code": "9279-1",
		"code_coding[0]_display": "ProTego demo",
		"code_coding[0]_system": "http://loinc.org",
		"code_text": "ProTego example",
		"extension[0]_url": "http://protego.eu/mealPortion",
		"extension[0]_valueString": "breakfast: [spam and eggs]",
		"id": "009",
		"resourceType": "Observation",
		"status": "final",
		"valueQuantity_unit": "gram",
		"valueQuantity_value": 459.1
	},
	{
		"code_coding[0]_code": "9279-1",
		"code_coding[0]_display": "ProTego demo",
		"code_coding[0]_system": "http://loinc.org",
		"code_text": "ProTego example",
		"extension[0]_url": "http://protego.eu/mealPortion",
		"extension[0]_valueString": "breakfast: [spam and eggs]",
		"id": "009",
		"resourceType": "Observation",
		"status": "final",
		"valueQuantity_unit": "gram",
		"valueQuantity_value": 459.1
	},
	{
		"code_coding[0]_code": "9279-1",
		"code_coding[0]_display": "ProTego demo",
		"code_coding[0]_system": "http://loinc.org",
		"code_text": "ProTego example",
		"extension[0]_url": "http://protego.eu/mealPortion",
		"extension[0]_valueString": "breakfast: [spam and eggs]",
		"id": "009",
		"resourceType": "Observation",
		"status": "final",
		"valueQuantity_unit": "gram",
		"valueQuantity_value": 459.1
	 }
    ]"""
    print("queryGateway_ProTegoHack: about to return" + jdf)
    return jdf, 200

app.run(port=FLASK_PORT_NUM, host='0.0.0.0')
