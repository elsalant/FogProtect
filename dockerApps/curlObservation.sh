curl -k --location --request POST 'https://127.0.01:443/fhir-server/api/v4/Observation' \
--header 'Content-Type: application/json' \
--header 'KMStoken: {'\''tokenType'\'': '\''keycloak'\'', '\''AccessOrIDToken'\'': '\''eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJXNWtWZ3RibEVDNlJQSy1feUZabnNmdUY1NVpodE0zX1p2WWFjUzM4NS1vIn0.eyJqdGkiOiJhNmM0OWYyZC1iZjE5LTQxNWQtYWY0My0zNmJlNzIyNmM4ZGMiLCJleHAiOjE1ODY4NzA2MzQsIm5iZiI6MCwiaWF0IjoxNTg2ODY5OTE0LCJpc3MiOiJodHRwOi8vbG9jYWxob3N0OjgwODAvYXV0aC9yZWFsbXMvZGVtbyIsImF1ZCI6ImFjY291bnQiLCJzdWIiOiJjN2Q4NDcxMi04NzIwLTQ2ZmYtODYyZi02MTUyNjI2OTBkYjUiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJmYS1jb25zb2xlIiwiYXV0aF90aW1lIjowLCJzZXNzaW9uX3N0YXRlIjoiYzU1Y2EwMzgtMmE5Zi00YWUxLThhYjgtY2Q3NDgyOThmNWQzIiwiYWNyIjoiMSIsImFsbG93ZWQtb3JpZ2lucyI6WyJodHRwOi8vbG9jYWxob3N0OjgwODAiXSwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIm15Um9sZSIsIm9mZmxpbmVfYWNjZXNzIiwidW1hX2F1dGhvcml6YXRpb24iLCJ1c2VyIl19LCJyZXNvdXJjZV9hY2Nlc3MiOnsiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJwcm9maWxlIG15c2NvcGUgZW1haWwiLCJncm91cHMyIjpbIi9Eb2N0b3JzIl0sImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwibmFtZSI6ImEgYiIsImdyb3VwcyI6WyIvRG9jdG9ycyJdLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJ0ZXN0IiwiZ2l2ZW5fbmFtZSI6ImEiLCJmYW1pbHlfbmFtZSI6ImIiLCJlbWFpbCI6ImVsY2VuZzJAeWFob28uY29tIn0.DpPepk-u0natqOlKz2r_9aKnG75yaXqB59tPpnRPN9CSD97cs_g1KYulYKauNZp1_yFT-Q0HU6RrFXIIGyBZUcNezev5nM2T8FJybHUvRqZQUPgtIC474TFjxOPw8Qj14gBPqtd57dsEo5q0vGgwR4pplyyuMOW5oCqTQajItDX4dG6TB6lNcU-Ryc8uPRT8yPdiN_yWEt7gjdSSoiACF_-C71ieigaSf9cH0AjOBYVz2QBcRHuNriYc3v1R_JpnxyI14RAMlFetuaClyxn89pi65iE4UobjULEkKgcPtNkIg0CpS_FceWFnc00VpCfE5aXPNsndxAum2Zi2DXHuow'\'', '\''AuthToken'\'': '\''s.JvKotVPg3HlQ1ZpchK6xerB'\''}' \
--header 'Authorization: Basic ZmhpcnVzZXI6ZmhpcnVzZXI=' \
--data-raw '{
  "resourceType": "Observation",
  "id": "009",
  "extension": [
  	{
  		"url": "http://protego.eu/mealPortion",
  		"valueString": "breakfast: spam and eggs"
  	}
  ],
  "valueQuantity": {
  	"value": 459,
  	"unit": "gram"
  },

  "status": "final",
    "code": {
    "coding": [
      {
        "system": "http://loinc.org",
        "code": "9279-1",
        "display": "ProTego demo"
      }
    ],
    "text": "ProTego example"
  }
}'
