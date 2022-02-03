    package katalog.example

    import data.kubernetes.assets

    filters[output] {
        count(rule)==0
        output = {"name": "Allow by default", "action": "Allow"}
    }

    filters[output] {
        count(rule)>0
        output = rule[_]
    }

    test2 {
       input.role == "engineer"
    }

    test2 {
       input.role == "worker"
       data.operation == input.operation
    }

    test[{"name":"Bond, James"}] {
       input.operation = "READ"
       roles = data.role[_]
       roles.name = "moose"
    }

    blockList[output] {
       count(blocked) == 0
       output = {"name":"Allow all URLs", "action": "None"}
    }

    blockList[output] {
        count(blocked)>0
        output = blocked[_]
    }

    rule[{"name": "Full priviledges for boss", "action": "Allow"}] {
        data.operation == "READ"
        data.role == "boss"
    }

    rule[{"name": "Redact PII columns for workers", "action": "RedactColumn", "columns": columns}] {
        asset := assets[data.asset.namespace][data.asset.name]
        data.role == "worker"
        columns := [c | asset.spec.assetMetadata.componentsMetadata[i].tags[_] == "PII"; c = i]
    }

    rule[{"name": "Block sensitive columns for workers", "action": "BlockColumn", "columns": columns}] {
        asset := assets[data.asset.namespace][data.asset.name]
        data.role == "worker"
        columns := [c | asset.spec.assetMetadata.componentsMetadata[i].tags[_] == "sensitive"; c = i]
    }

    rule[{"name": "Block videos not created by owning organization", "action": "FilterPred", "token" : "organization", "filterPredicate" : "WHERE organization = **T1**", "replaceMe": "**T1**"}]  {
        data.asset.name == "videos"
    }
  
    blocked[{"name": "Block employee_related tagged URLs for workers", "action": "BlockURL"}] {
       data.role == "worker"
       asset := assets[data.asset.namespace][data.asset.name]
       asset.spec.assetMetadata.tags[_] == "employee_related"
    }

    blocked[{"name": "Block control tagged URLs for except for workers", "action": "BlockURL"}] {
       data.role != "worker"
       asset := assets[data.asset.namespace][data.asset.name]
       asset.spec.assetMetadata.tags[_] == "control"
    }

    blocked[{"name": "Requested assets does not exist", "action": "BlockURL"}] {
       not assets[data.asset.namespace][data.asset.name]
    }

    blocked[{"name": "Access for user suspended", "action": "BlockURL"}] {
       data.role = "suspended"
    }
