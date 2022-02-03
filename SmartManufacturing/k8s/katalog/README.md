# Katalog

Katalog is a policy-enabled data catalog powered by Kubernetes and [Open Policy Agent](https://www.openpolicyagent.org/) (OPA).

Katalog provides a Kubernetes interface for creating entries of:

1. **Data assets** using the [`Asset`](docs/README.md#asset) Custom Resource Definition (CRD).
1. **Credentials** of a data asset using Kubernetes `Secret` wrapping the [`Credentials`](docs/README.md#credentials) CRD.
1. **Data policies** using Kubernetes `Configmap` resources that hold Rego policies.

## Install

Install Katalog to `katalog-system` namespace of your Kubernetes cluster:

```bash
kubectl apply -f manifests/install.yaml
kubectl apply -f manifests/opa.yaml
```

Install the `katalog` CLI by copying [`bin/katalog`](bin/katalog) to a directory in your system's PATH (optional). For example:
```bash
sudo cp bin/katalog /usr/local/bin
```

## Usage

See the [example](example/README.md) for sample usage. 


### Managing policies

Data policies are stored in Kubernetes `Configmap` resources that contain a Rego policy in the `data` section. These `Configmap` resources for policies must be created in the `katalog-system` namespace and include a label `openpolicyagent.org/policy=rego`.


To apply a policy from a Rego file named `policy.rego`:

```bash
katalog policy policy.rego | kubectl apply -n katalog-system -f -
``` 

### Managing credenditals

Credenditals are stored in Kubernetes `Secret` resources that contain [`Credentials`](docs/README.md#credentials) in the `data` section. These `Secret` resources should be applied in the same namespace as `Asset` resources that refer to them.


To apply a secret from a `Credentials` YAML file named `credentials.yaml`:

```bash
katalog secret credentials.yaml | kubectl apply -f -
```

### Managing assets

Assets are stored in [`Asset`](docs/README.md#asset) resources. An `Asset` CRD includes a reference to a credentials `Secret`, connection information, and other metadata such as columns and associated security tags.

To apply an asset from a `Asset` YAML file named `asset.yaml`:

```bash
kubectl apply -f asset.yaml
```

## Security 

[`manifests/opa.yaml`](manifests/opa.yaml) installs an instance of OPA for development and evaluation and lacks any [security](https://www.openpolicyagent.org/docs/latest/security/) measures. You can modify it manually if needed.

## Help

For any question create an issue with a title in the form of `Katalog: <title content>`.
