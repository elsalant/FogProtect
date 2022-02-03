# API Reference

Packages:

- [katalog.m4d.ibm.com/v1alpha1](#katalog.m4d.ibm.com/v1alpha1)




# katalog.m4d.ibm.com/v1alpha1

Resource Types:

- [Asset](#asset)

- [Credentials](#credentials)




## Asset

<sup><sup>[↑ Jump to parent](#katalog.m4d.ibm.com/v1alpha1 )</sup></sup>









<table>
    <thead>
        <tr>
            <th>Name</th>
            <th>Type</th>
            <th>Description</th>
            <th>Required</th>
        </tr>
    </thead>
    <tbody><tr>
      <td><b>apiVersion</b></td>
      <td>string</td>
      <td>katalog.m4d.ibm.com/v1alpha1</td>
      <td>true</td>
      </tr>
      <tr>
      <td><b>kind</b></td>
      <td>string</td>
      <td>Asset</td>
      <td>true</td>
      </tr>
      <tr>
      <td><b><a href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.20/#objectmeta-v1-meta">metadata</a></b></td>
      <td>object</td>
      <td>Refer to the Kubernetes API documentation for the fields of the `metadata` field.</td>
      <td>true</td>
      </tr><tr>
        <td><b><a href="#assetspec">spec</a></b></td>
        <td>object</td>
        <td></td>
        <td>false</td>
      </tr></tbody>
</table>

### Asset.spec

<sup><sup>[↑ Jump to parent](#asset)</sup></sup>



<table>
    <thead>
        <tr>
            <th>Name</th>
            <th>Type</th>
            <th>Description</th>
            <th>Required</th>
        </tr>
    </thead>
    <tbody><tr>
        <td><b><a href="#assetspecconnection">connection</a></b></td>
        <td>object</td>
        <td>Connection information</td>
        <td>true</td>
      </tr><tr>
        <td><b><a href="#assetspecschemaindex">schema</a></b></td>
        <td>[]object</td>
        <td>Schema information for rectangular data assets (can be partial)</td>
        <td>false</td>
      </tr><tr>
        <td><b><a href="#assetspecsecretref">secretRef</a></b></td>
        <td>object</td>
        <td>Reference to a Secret resource holding credentials for this asset</td>
        <td>false</td>
      </tr><tr>
        <td><b>tags</b></td>
        <td>[]string</td>
        <td>Tags associated with the asset</td>
        <td>false</td>
      </tr></tbody>
</table>

### Asset.spec.connection

<sup><sup>[↑ Jump to parent](#assetspec)</sup></sup>

Connection information

<table>
    <thead>
        <tr>
            <th>Name</th>
            <th>Type</th>
            <th>Description</th>
            <th>Required</th>
        </tr>
    </thead>
    <tbody><tr>
        <td><b>custom</b></td>
        <td>object</td>
        <td>Arbitrary JSON for custom connections</td>
        <td>false</td>
      </tr><tr>
        <td><b><a href="#assetspecconnections3">s3</a></b></td>
        <td>object</td>
        <td>Connection information for S3 compatible object store</td>
        <td>false</td>
      </tr></tbody>
</table>

### Asset.spec.connection.s3

<sup><sup>[↑ Jump to parent](#assetspecconnection)</sup></sup>

Connection information for S3 compatible object store

<table>
    <thead>
        <tr>
            <th>Name</th>
            <th>Type</th>
            <th>Description</th>
            <th>Required</th>
        </tr>
    </thead>
    <tbody><tr>
        <td><b>bucket</b></td>
        <td>string</td>
        <td></td>
        <td>true</td>
      </tr><tr>
        <td><b>endpoint</b></td>
        <td>string</td>
        <td></td>
        <td>true</td>
      </tr><tr>
        <td><b>format</b></td>
        <td>string</td>
        <td></td>
        <td>true</td>
      </tr><tr>
        <td><b>path</b></td>
        <td>string</td>
        <td></td>
        <td>true</td>
      </tr><tr>
        <td><b>region</b></td>
        <td>string</td>
        <td></td>
        <td>false</td>
      </tr></tbody>
</table>

### Asset.spec.schema[index]

<sup><sup>[↑ Jump to parent](#assetspec)</sup></sup>



<table>
    <thead>
        <tr>
            <th>Name</th>
            <th>Type</th>
            <th>Description</th>
            <th>Required</th>
        </tr>
    </thead>
    <tbody><tr>
        <td><b>name</b></td>
        <td>string</td>
        <td>Column name</td>
        <td>true</td>
      </tr><tr>
        <td><b>tags</b></td>
        <td>[]string</td>
        <td>Tags associated with the column</td>
        <td>false</td>
      </tr><tr>
        <td><b>type</b></td>
        <td>string</td>
        <td>Column type</td>
        <td>false</td>
      </tr></tbody>
</table>

### Asset.spec.secretRef

<sup><sup>[↑ Jump to parent](#assetspec)</sup></sup>

Reference to a Secret resource holding credentials for this asset

<table>
    <thead>
        <tr>
            <th>Name</th>
            <th>Type</th>
            <th>Description</th>
            <th>Required</th>
        </tr>
    </thead>
    <tbody><tr>
        <td><b>name</b></td>
        <td>string</td>
        <td>Name of the Secret resource (must exist in the same namespace)</td>
        <td>false</td>
      </tr></tbody>
</table>

## Credentials

<sup><sup>[↑ Jump to parent](#katalog.m4d.ibm.com/v1alpha1 )</sup></sup>







Credentials for an asset (can include arbitrary fields)

<table>
    <thead>
        <tr>
            <th>Name</th>
            <th>Type</th>
            <th>Description</th>
            <th>Required</th>
        </tr>
    </thead>
    <tbody><tr>
      <td><b>apiVersion</b></td>
      <td>string</td>
      <td>katalog.m4d.ibm.com/v1alpha1</td>
      <td>true</td>
      </tr>
      <tr>
      <td><b>kind</b></td>
      <td>string</td>
      <td>Credentials</td>
      <td>true</td>
      </tr>
      <tr>
      <td><b><a href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.20/#objectmeta-v1-meta">metadata</a></b></td>
      <td>object</td>
      <td>Refer to the Kubernetes API documentation for the fields of the `metadata` field.</td>
      <td>true</td>
      </tr><tr>
        <td><b><a href="#credentialsspec">spec</a></b></td>
        <td>object</td>
        <td></td>
        <td>false</td>
      </tr></tbody>
</table>

### Credentials.spec

<sup><sup>[↑ Jump to parent](#credentials)</sup></sup>



<table>
    <thead>
        <tr>
            <th>Name</th>
            <th>Type</th>
            <th>Description</th>
            <th>Required</th>
        </tr>
    </thead>
    <tbody><tr>
        <td><b>apiKey</b></td>
        <td>string</td>
        <td>API key used in various IAM enabled services</td>
        <td>false</td>
      </tr><tr>
        <td><b><a href="#credentialsspecawskeys">awsKeys</a></b></td>
        <td>object</td>
        <td>Access and secret keys used in AWS and compatible systems</td>
        <td>false</td>
      </tr><tr>
        <td><b><a href="#credentialsspecbasic">basic</a></b></td>
        <td>object</td>
        <td>Password based authentication used in basic access authentication</td>
        <td>false</td>
      </tr><tr>
        <td><b>custom</b></td>
        <td>object</td>
        <td>Arbitrary JSON for custom connections</td>
        <td>false</td>
      </tr></tbody>
</table>

### Credentials.spec.awsKeys

<sup><sup>[↑ Jump to parent](#credentialsspec)</sup></sup>

Access and secret keys used in AWS and compatible systems

<table>
    <thead>
        <tr>
            <th>Name</th>
            <th>Type</th>
            <th>Description</th>
            <th>Required</th>
        </tr>
    </thead>
    <tbody><tr>
        <td><b>accessKey</b></td>
        <td>string</td>
        <td>The access key is also known as AccessKeyId</td>
        <td>true</td>
      </tr><tr>
        <td><b>secretKey</b></td>
        <td>string</td>
        <td>The secret key is also known as SecretAccessKey</td>
        <td>true</td>
      </tr></tbody>
</table>

### Credentials.spec.basic

<sup><sup>[↑ Jump to parent](#credentialsspec)</sup></sup>

Password based authentication used in basic access authentication

<table>
    <thead>
        <tr>
            <th>Name</th>
            <th>Type</th>
            <th>Description</th>
            <th>Required</th>
        </tr>
    </thead>
    <tbody><tr>
        <td><b>password</b></td>
        <td>string</td>
        <td></td>
        <td>true</td>
      </tr><tr>
        <td><b>username</b></td>
        <td>string</td>
        <td></td>
        <td>false</td>
      </tr></tbody>
</table>
