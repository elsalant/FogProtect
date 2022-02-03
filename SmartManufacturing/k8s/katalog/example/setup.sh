set -e 

setup_minio() {
    helm repo add minio https://helm.min.io
    helm install --wait minio minio/minio
}

upload_csv() {
    ACCESS_KEY=$(kubectl get secret minio -o jsonpath="{.data.accesskey}" | base64 --decode) 
    SECRET_KEY=$(kubectl get secret minio -o jsonpath="{.data.secretkey}" | base64 --decode)
    cat << EOF | kubectl apply -f -
apiVersion: batch/v1
kind: Job
metadata:
  name: csv-uploader
spec:
  template:
    spec:
      containers:
      - name: mc
        image: minio/mc
        command: ["bash"]
        args:
        - -c
        - >-
            mc alias set minio-local http://minio:9000 "${ACCESS_KEY}" "${SECRET_KEY}" --api s3v4 &&
            mc mb minio-local/demo &&
            (curl -s https://raw.githubusercontent.com/IBM/the-mesh-for-data/master/samples/kubeflow/data.csv | mc pipe minio-local/demo/data.csv) &&
            echo "Completed"
      restartPolicy: Never
  backoffLimit: 4
EOF
    echo "To access the minio UI use the following command:"
    echo "> kubectl port-forward svc/minio 9000"
    echo "then browse to localhost:9000 and login with Access Key: ${ACCESS_KEY} and Secret Key: ${SECRET_KEY}"
}

cleanup() {
    kubectl delete job csv-uploader
    helm uninstall minio
}

case "$1" in
cleanup)
    cleanup
    ;;
*)
    setup_minio
    upload_csv
    ;;
esac
