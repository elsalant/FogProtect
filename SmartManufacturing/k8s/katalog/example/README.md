# Example

Before running this example [Install Katalog](../README.md#install) to a Kubernetes cluster of your choice (e.g., [Kind](https://kind.sigs.k8s.io/)).

## Run the sample

### Upload `data.csv` to object storage

```bash
./setup.sh 
```

### Add credentials for `data.csv` to the catalog 

```bash
katalog secret credentials.yaml | kubectl apply -f -
```

Or directly with `kubectl`:
```bash
kubectl apply --dry-run=client -f credentials.yaml # validates credentials.yaml
kubectl create secret generic data-csv-creds --from-file=main=credentials.yaml
```

### Add `data.csv` to the catalog 

```bash
kubectl apply -f asset.yaml
```

### Add a policy 

```bash
katalog policy policy.rego | kubectl apply -f -
```

Or directly with `kubectl` using `policy.yaml`:
```bash
kubectl apply -f policy.yaml -n katalog-system
```

### Port forward OPA

```bash
kubectl port-forward deployment/opa 8181
```

### Send an OPA query

```bash
curl localhost:8181/v1/data/katalog/example/verdict -d @input.json -H 'Content-Type: application/json'
```

The expected output is
```json
{"result":[{"action":"RedactColumn","columns":["nameOrig"],"name":"Redact PII columns for CBA"}]}
```

## Cleanup

```bash
./setup.sh cleanup
kubectl delete -f asset.yaml,policy.yaml
```

