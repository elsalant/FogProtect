    package katalog.example

    import data.kubernetes.assets

    filters[output] {
        count(rule)==0
        output = {"name": "No filtering by default!", "action": "Allow"}
    }

    filters[output] {
        count(rule)>0
        output = rule[_]
    }

    blockList[output] {
       count(blocked) == 0
       output = {"name":"Allow all URLs!", "action": "None"}
    }

    blockList[output] {
        count(blocked)>0
        output = blocked[_]
    }

    rule[{"name": "Full priviledges for Manager", "action": "Allow"}] {
        input.request.operation == "READ"
        input.request.role[_] = "Manager"
    }

    rule[{"name": "Redact PII columns if not Manager or HR for personnel data", "action": "RedactColumn", "columns": columns}] {
        not (input.request.role[_] = "Manager")
        not (input.request.role[_] = "HR")
        asset := assets[input.request.asset.namespace][input.request.asset.name]
        asset.spec.assetMetadata.tags[_] = "personnel"
        columns := [c | asset.spec.assetMetadata.componentsMetadata[i].tags[_] = "PII"; c = i]
    }

    blocked[{"name": "Block data-related tagged URLs for HR", "action": "BlockURL"}] {
       input.request.role[_] = "HR"
       asset := assets[input.request.asset.namespace][input.request.asset.name]
       asset.spec.assetMetadata.tags[_] = "data"
    }

    blocked[{"name": "Block order-related tagged URLs for all but Managers", "action": "BlockURL"}] {
       not (input.request.role[_] = "Manager")
       asset := assets[input.request.asset.namespace][input.request.asset.name]
       asset.spec.assetMetadata.tags[_] = "order"
    }

    blocked[{"name": "Block control tagged-URLs for HR", "action": "BlockURL"}] {
       input.request.role[_] = "HR"
       asset := assets[input.request.asset.namespace][input.request.asset.name]
       asset.spec.assetMetadata.tags[_] = "control"
    }

    blocked[{"name": "Block personnel tagged-URLs if not Manager or HR", "action": "BlockURL"}] {
       not (input.request.role[_] = "HR")
       not (input.request.role[_] = "Manager")
       not (input.request.role[_] = "Technician")
       asset := assets[input.request.asset.namespace][input.request.asset.name]
       asset.spec.assetMetadata.tags[_] = "personnel"
    }

    blocked[{"name": "Requested assets does not exist", "action": "BlockURL"}] {
       not assets[input.request.asset.namespace][input.request.asset.name]
    }

    blocked[{"name": "Access for user suspended", "action": "BlockURL"}] {
       input.request.role == "suspended"
    }

