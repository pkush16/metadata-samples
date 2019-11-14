# CosmosScanner 

The `CosmosScanner` is a TimerTrigger python function in Azure which scans the CosmosDB account every 2 minutes to fetch relevant metadata and create/update enitites in the Apache Atlas using various micrososervices like Qualified Name Service, JSON Genertaor and AtlasAPIWrapper.

## How it works

The TimerTrigger Azure functions runs at a scheduled interval(for testing it is set to every 2 minutes) and using CosmosDB SDK for python fetches the metadata about given CosmosDB accounts, its database(s) and collection(s). The metadata about the azure resources maps to the attributes defined in the Atlas typedefs.<br/>
It then calls **QNS** which generates a unique qualified name, an attribute that is mandatory to create entities(of type Referenceable) in Atlas.<br/>
Once we have all the required metadata, **JSON generator** is called to generate json compatible with Atlas APIs.<br/> 
Finally the AtlasAPIWrapper is called to make the relevant Atlas API call.<br/>

Dockerfile - uses the base image for python functions in Azure. It will build a containerized Azure Function on Linux which can be deployed as Azure Container Image and deployed in ASE(App Service Environment)/ AKS.etc 


