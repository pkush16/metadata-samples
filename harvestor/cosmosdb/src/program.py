import json 
import logging
import requests
import azure.cosmos.cosmos_client as cosmos_client

def checkAndAssignKey(dict, key): 
      
    if key in dict.keys(): 
        return dict[key]
    return -1

def httpPost(input_content, url):
    try:        
        headers = {'Content-type': 'application/json'}
        #later modify according to the verb - maybe a Case , inputs to include , verb, service
        #response = requests.request( "POST", url, data=json.dumps(input_content), headers=headers)
        response = requests.post(url, data=json.dumps(input_content), headers=headers)  
        return response
    except Exception as e:        
        logging.error("error occured in calling" + e)


def getQualifiedName(cosmosdb_uri, cosmosdb_database, container_name, qns_url):
    qns_request_obj ={
        "cosmosdb_uri":cosmosdb_uri,
        "cosmosdb_database":cosmosdb_database,
        "container_name":container_name
    }
    headers = {'Content-type': 'application/json'}
    response=requests.post(qns_url,data=json.dumps(qns_request_obj),headers=headers)
    if response.status_code==200:
        response_text = json.loads(response.content)
        return  response_text["qualifiedName"]
        

with open('settings.json') as config_file:
    settings = json.load(config_file)

cosmos_client_url= settings['ENDPOINT']
cosmos_primary_key= settings['PRIMARYKEY']

# Initialize the Cosmos client
client = cosmos_client.CosmosClient(url_connection=cosmos_client_url, auth={'masterKey': cosmos_primary_key}) 
#entity_final = []  

# List the databases
dblist = client.ReadDatabases( options=None)
for db in dblist:
    #print(db.values())
    database_link =  db['_self']
    database_name = db['id']
    print("\n ")
    collist = client.ReadContainers(database_link, options=None)
    entity_final = []   
    for coll in collist:
        #print(coll.values())
        collection_link = coll['_self']
        collection_name = coll['id']
        collection_defaultTtl =  checkAndAssignKey(coll, 'defaultTtl') 
        collection_isOn = True
        collection_lastModifiedTime= coll['_ts']      
        #print(collection_link)
        collection = client.ReadContainer(collection_link)
        # container_props = collection.read()
        # print("\n Container properties")
        # print(json.dumps(collection['defaultTtl']))
        offer = list(client.QueryOffers('SELECT * FROM c WHERE c.resource = \'{0}\''.format(collection['_self'])))[0] 
        collection_offerContent =offer['content']
        collection_offerLink=offer['_self']
        entity_type_name=settings['ENTITYNAME']

        # Calling QNS to generate the atribute name 
        qns_base_url = "https://metadata-services.azurewebsites.net/api/metadata-qualifiedname-service?code=DCJoZnzNKZ4teDSPicw5578a9xhPTKXbcqqDuOzi9XIWtbtzcCxZbw==&typeName="
        type_name = entity_type_name
        qns_url= qns_base_url+ type_name
        qns_type_get_response=  requests.request("GET", qns_url, headers={'Content-type': 'application/json'})
        qns_input= qns_type_get_response.text
        qns_json = json.loads(qns_input)
        qualified_name = getQualifiedName(cosmos_client_url, database_name, collection_name, qns_url)
        
        # Creating entity
        ### TODO- make this

        entity_json ={
            "entity_type_name": entity_type_name ,
            "created_by": "psk",
            "attributes": [{
		        "attr_name":"qualifiedName" ,
		        "attr_value": qualified_name,
		        "is_entityref": False
            }, 
            {
		        "attr_name": "name",
		        "attr_value": collection_name,
		        "is_entityref": False
            },
            {
            "attr_name": "resourceLink",
		    "attr_value": collection_link,
		    "is_entityref": False
            },
            {
            "attr_name": "lastModifiedTime",
		    "attr_value": collection_lastModifiedTime,
		    "is_entityref": False
            },
            {
            "attr_name": "offer",
		    "attr_value": {"content": collection_offerContent,"offerLink":collection_offerLink},
		    "is_entityref": False
            },
            {
            "attr_name": "timeToLive",
		    "attr_value": {"isOn": collection_isOn  ,"defaultValue" :collection_defaultTtl},
		    "is_entityref": False
            }
            ]   
        }       
        entity_final.append(entity_json)


        #Call Json Generator from function 
        
        #payload= json.dumps(entity_final)
        payload=entity_final
        #print(entity_final)
        json_generator_url="https://atlas-json-creator.azurewebsites.net/api/atlas_entities_create"
        #atlas_url="https://atlasapiwrapper.azurewebsites.net/api/entity/bulk"
        atlas_url = "http://admin:admin@52.189.237.74:21000/api/atlas/v2/entity/bulk"
        json_generator_response=httpPost(entity_final,json_generator_url) 
        if json_generator_response.status_code == 200:
            #json_entity_objects=json.loads(json_generator_response.content)
            json_entity_objects= json_generator_response.json()
            print(json.dumps(json_entity_objects))
            # Call Atlas Wrapper service
            api_output = httpPost(json_entity_objects,atlas_url)
            print(api_output)
            print("Json generator status code 2 \t")
            print(json_generator_response.status_code)
            if api_output.status_code ==200:
                logging.info("Entity created successfully!")
                print("Atlas status code 2 \t")
                print(api_output.status_code)
            else:
                logging.error("Error in calling Atlas access layer with error code:"+ str(api_output.status_code) + 
                " "+api_output.text)
        else:
            logging.error("Error in calling JSON generator layer with error code:" + str(json_generator_response.status_code) + 
                " "+ json_generator_response.text)

    #print (entity_final)    
        