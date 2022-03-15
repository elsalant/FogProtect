DOCKER_FILE ?= Dockerfile
DOCKER_CONTEXT ?= .
DOCKER_TAGNAME ?= v1
DOCKER_HOSTNAME ?= ghcr.io
DOCKER_NAMESPACE ?= elsalant
DOCKER_IMG_NAME ?= filtermodule-spark
APP_IMG ?= ${DOCKER_HOSTNAME}/${DOCKER_NAMESPACE}/${DOCKER_IMG_NAME}:${DOCKER_TAGNAME}

.PHONY: docker-build
docker-build:
	docker build $(DOCKER_CONTEXT) -t ${APP_IMG} -f $(DOCKER_FILE)
#        kind load docker-image ${APP_IMG} --name fogprotect

.PHONY: docker-push
docker-push:
	docker push ${APP_IMG}

helm-install:
	helm uninstall filterid
	helm install filterid ../k8s/filteridchart_opa

