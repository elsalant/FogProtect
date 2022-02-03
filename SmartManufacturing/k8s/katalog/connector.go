package main

import (
	"context"
	"encoding/base64"
	"encoding/json"
	"fmt"
	"log"
	"net"
	"strings"

	corev1 "k8s.io/api/core/v1"

	connectors "github.com/ibm/the-mesh-for-data/pkg/connectors/protobuf"
	"github.com/pkg/errors"
	"google.golang.org/grpc"
	v1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/apis/meta/v1/unstructured"
	"k8s.io/apimachinery/pkg/runtime/schema"

	kclient "sigs.k8s.io/controller-runtime/pkg/client"
	kconfig "sigs.k8s.io/controller-runtime/pkg/client/config"
)

type dataCatalogService struct {
	client kclient.Client
}

func (s *dataCatalogService) GetDatasetInfo(ctx context.Context, req *connectors.CatalogDatasetRequest) (*connectors.CatalogDatasetInfo, error) {

	identifier := strings.SplitN(req.DatasetId, "/", 2)
	if len(identifier) != 2 {
		return nil, errors.New(fmt.Sprintf("Invalid dataset ID: %s. Expected <namespace>/<name>", req.DatasetId))
	}
	namespace := identifier[0]
	name := identifier[1]

	object := createUnstructured("katalog.m4d.ibm.com", "v1alpha1", "Asset", name, namespace)
	objectKey, err := kclient.ObjectKeyFromObject(object)
	if err != nil {
		return nil, err
	}
	err = s.client.Get(ctx, objectKey, object)
	if err != nil {
		return nil, err
	}

	return &connectors.CatalogDatasetInfo{
		DatasetId: req.DatasetId,
		Details: &connectors.DatasetDetails{
			Name:       req.DatasetId,
			DataOwner:  "",
			DataFormat: "",
			Geo:        "",
			DataStore: &connectors.DataStore{
				Type: connectors.DataStore_S3, // TODO
				Name: "",
				S3: &connectors.S3DataStore{
					Endpoint:  "",
					Bucket:    "",
					ObjectKey: "",
					Region:    "",
				},
				Db2:   nil,
				Kafka: nil,
			},
			Metadata: &connectors.DatasetMetadata{
				DatasetTags:          object.UnstructuredContent()["spec"].(map[string]interface{})["tags"].([]string),
				DatasetNamedMetadata: nil,
				ComponentsMetadata: map[string]*connectors.DataComponentMetadata{
					"columnName": {
						ComponentType: "column",
						Tags:          []string{},
					},
				},
			},
		},
	}, nil
}

type dataCredentialsService struct {
	client kclient.Client
}

func (s *dataCredentialsService) GetCredentialsInfo(ctx context.Context, req *connectors.DatasetCredentialsRequest) (*connectors.DatasetCredentials, error) {
	namespace, name := parseDatasetId(req.DatasetId)
	secret := &corev1.Secret{
		ObjectMeta: v1.ObjectMeta{
			Namespace: namespace,
			Name:      name,
		},
	}
	objectKey, err := kclient.ObjectKeyFromObject(secret)
	if err != nil {
		return nil, err
	}

	err = s.client.Get(ctx, objectKey, secret)
	if err != nil {
		return nil, err
	}

	data, err := base64.StdEncoding.DecodeString(string(secret.Data["main"]))
	if err != nil {
		return nil, errors.Wrap(err, "Failed to decode secret")
	}
	var credentials map[string]interface{}
	err = json.Unmarshal(data, &credentials)
	if err != nil {
		return nil, errors.Wrap(err, "Failed to parse secret as JSON")
	}

	// TODO get from credentials
	return &connectors.DatasetCredentials{
		DatasetId: req.DatasetId,
		Creds: &connectors.Credentials{
			AccessKey: "",
			SecretKey: "",
			Username:  "",
			Password:  "",
			ApiKey:    "",
		},
	}, nil
}

// type policyManagerService struct {
// 	client     kclient.Client
// 	httpClient *http.Client
// }

// func (s *policyManagerService) GetPoliciesDecisions(ctx context.Context, req *connectors.ApplicationContext) (*connectors.PoliciesDecisions, error) {

// 	runtimeContext := req.GetAppInfo()

// 	var datasetDecitions []*connectors.DatasetDecision

// 	for _, datasetContext := range req.Datasets {
// 		datasetId := datasetContext.GetDataset().GetDatasetId()
// 		namespace, name := parseDatasetId(datasetId)

// 		operation := datasetContext.GetOperation()
// 		if operation.Type != connectors.AccessOperation_READ {
// 			return nil, errors.New("Only READ operations are currently supported")
// 		}

// 		requestBody, err := json.Marshal(map[string]interface{}{
// 			"input": map[string]interface{}{
// 				"request": map[string]interface{}{
// 					"operation": "READ",
// 					"purpose":   runtimeContext.Purpose,
// 					"asset": map[string]interface{}{
// 						"namespace": namespace,
// 						"name":      name,
// 					},
// 				},
// 			},
// 		})
// 		if err != nil {
// 			return nil, errors.Wrap(err, "Failed to marshal request")
// 		}

// 		response, err := s.httpClient.Post("http://localhost:8181/v1/data/katalog/example/verdict", "application/json", bytes.NewBuffer(requestBody))
// 		if err != nil {
// 			return nil, errors.Wrap(err, "Error sending request to OPA")
// 		}
// 		defer response.Body.Close()

// 		if response.StatusCode != 200 {
// 			return nil, errors.Wrapf(err, "Received response from OPA with status code %d", response.StatusCode)
// 		}

// 		data, err := ioutil.ReadAll(response.Body)
// 		if err != nil {
// 			return nil, errors.Wrap(err, "Error reading response from OPA")
// 		}

// 		var operationDecitions []*connectors.OperationDecision

// 		// TODO: iterate
// 		operationDecition := &connectors.OperationDecision{
// 			Operation:          operation,
// 			EnforcementActions: []*connectors.EnforcementAction{},
// 		}
// 		operationDecitions = append(operationDecitions, operationDecition)

// 		datasetDecition := &connectors.DatasetDecision{
// 			Dataset:   datasetContext.Dataset,
// 			Decisions: []*connectors.OperationDecision{},
// 		}
// 		datasetDecitions = append(datasetDecitions, datasetDecition)
// 	}

// 	return &connectors.PoliciesDecisions{
// 		DatasetDecisions: datasetDecitions,
// 	}, nil
// }

// TODO: reuse from m4d once this is moved to /pkg
func createUnstructured(group, version, kind, name, namespace string) *unstructured.Unstructured {
	result := &unstructured.Unstructured{}
	result.SetGroupVersionKind(schema.GroupVersionKind{
		Group:   group,
		Version: version,
		Kind:    kind,
	})
	result.SetName(name)
	result.SetNamespace(namespace)
	return result
}

func parseDatasetId(datasetId string) (namespace string, name string) {
	identifier := strings.SplitN(datasetId, "/", 2)
	namespace = identifier[0]
	name = identifier[1]
	return
}

func main() {

	client, err := kclient.New(kconfig.GetConfigOrDie(), kclient.Options{})
	if err != nil {
		log.Fatalf("failed to create client")
	}

	listener, err := net.Listen("tcp", ":8080")
	if err != nil {
		log.Fatalf("Error creating a listerning socket: %v", err)
	}

	server := grpc.NewServer()

	// httpClient := &http.Client{}

	connectors.RegisterDataCatalogServiceServer(server, &dataCatalogService{client})
	connectors.RegisterDataCredentialServiceServer(server, &dataCredentialsService{client})
	// connectors.RegisterPolicyManagerServiceServer(server, &policyManagerService{client, httpClient})

	if err := server.Serve(listener); err != nil {
		log.Fatalf("Error starting server: %v", err)
	}
}
