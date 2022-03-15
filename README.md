Emulation of a use case where a POST command is sent to a REST end point to return data.
 
POST commands coming in to the system will include a "role" token which has been authenticated upstream of this code.

Example: curl -H "role: worker" -k  'http://127.0.0.1:80/query/select%20*%20from%20observation'

1. Run the module executable:
in helm directory:
> helm install filtermodule filtermodule_chart

Restricting data occurs in two ways:
1. Restricting access to URL endpoints based on role.  For example, a URL that returns video data will be accessed controlled.
This is handled by routing rules which get created in conjunction with the Policy Manager.  See k8s/vs1FilterBlock.yaml for an example.
2. Redact data returned from the data source based on Policy Manager rules.  This is handled by the REST data module. (See python/filter_id_OPA.py)

To set up:

1. Open up ports on the ingress gateway:
   kubectl apply -f gateway.yaml
2. Apply virtualservice rule-base routing:  (TBD - automatically deployed by blueprint)
   kubectl apply -f vsRedirect.yaml  
3. Define Asset CRD and then Apply OPA policies (in katalog-system namespace)  (TBD - automatically deployed by blueprint)
   kubectl apply -f katalog.m4d.ibm.com_assets.yaml
   kubectl apply -f policy.yaml -n katalog-system  
4. Apply OPA assets  (TBD - automatically deployed by blueprint)
   kubectl apply -f asset.yaml
5. Apply application code (backend data server)
   kubectl apply -f rest_m4dapp.yaml  (should deploy chart for querygateway component)
6. Apply REST data module (TBD - automatically deployed by blueprint on m4d app invocation)
   (helm package and then install filteridchart_opa)
7. Expose OPA deployment as a service:
   kubectl expose deployment/opa -n katalog-system

Example queries to the the application querygateway and responses:

1. PII information gets redacted
% curl -H "role: worker" -k  'http://127.0.0.1:80/query/select%20*%20from%20observation'
"{'id':'XXX', 'Fname': 'Peter', 'Lname':'XXX', 'Age': '22'}{'id':'XXX', 'Fname': 'Clark', 'Lname':'XXX', 'Age': '41'}"
2. "boss" role can see all information
curl -H "role: boss" -k  'http://127.0.0.1:80/query/select%20*%20from%20observation'
[{"id": "007", "Fname": "Peter", "Lname": "Parker", "Age": "22"}, {"id": "123", "Fname": "Clark", "Lname": "Kent", "Age": "41"}]
3. Role blocked from accessing endpoint
curl -H "role: badguy" -k  'http://127.0.0.1:80/query/select%20*%20from%20observation'
{"action":"Deny","name":"Denied by default"}
4. All information blocked for a give role
curl -H "role: moose" -k  'http://127.0.0.1:80/query/select%20*%20from%20observation'
{"action":"Deny","name":"Denied by default"}


### Developers  
To build the (Spark-enabled) Docker image and push to the repo:  
from the python directory:
- make docker-build
- make docker-push

To build a non-Spark enabled version:
In the python directory:
1. In the Makefile, change the DOCKER_IMG_NAME from filtermodule-spark to filtermodule
2. In the Dockerfile, change ENV USE_SPARK="true" to "false"

To package and push a chart:  
from the charts directory:  
- export HELM_EXPERIMENTAL_OCI=1
- helm package filteridchart_opa -d /tmp
- helm push /tmp/filteridchart_opa-0.1.0.tgz oci://ghcr.io/elsalant
