import datetime
import logging
import requests
import json
import os
import azure.cosmos.cosmos_client as cosmos_client
import azure.functions as func


def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()     
    
    logging.info("Function triggered successfully")

    #Setting base URL values for api calls to various services 
    qns_base_url= os.environ['QNS_BASE_URL']
    json_generator_url = os.environ['JSON_GENERATOR_URL']
    atlas_url = os.environ['ATLAS_URL']
    logging.info("Setting Base URLs")

    #Fetching the list of Cosmos DB accounts and read-only keys 
    input_string = os.environ['ACCOUNT_LIST']
    acclist= json.loads(input_string) 
    
    #  account_initial_guid for initial assignment of guid for cosmos if enity doesn't e       
    #  database_initial_guid
    
    entity_final = []
    guid_dictionary={}
    account_initial_guid = -400
    
    for account in acclist:
        # Initialize the Cosmos client for a given account 
        logging.info("Entering the account loop ")
        cosmos_client_url = account['ENDPOINT']
        cosmos_read_only_primary_key = account['PRIMARYKEY']

        client = cosmos_client.CosmosClient(url_connection=cosmos_client_url, auth={'masterKey': cosmos_read_only_primary_key}) 
        #offerList =client.ReadOffers(options= None)

        #Retrieving Account QualifiedName and GUID using QNS service
        account_QNS_info = getQualifiedNameAccount(cosmos_client_url, qns_base_url)
        account_qualifiedName= account_QNS_info['qualifiedName']
        if (account_QNS_info['guid'] is not None ) :
            account_guid = account_QNS_info['guid']
        else :
            account_initial_guid -= 1
            account_guid = account_initial_guid
            

        #Update the GUID dictionary
        guid_dictionary[account_qualifiedName] = account_guid

        #Retrieving account name from cosmos endpoint 
        if(cosmos_client_url.find('.document') != -1):
            index = cosmos_client_url.find('.document')
        account_name= cosmos_client_url[8:index]
        logging.info("account  " +account_name)
        account_enity_json ={
        "entity_type_name": "azure_cosmosdb_account",
        "created_by": "psk",
        "guid": guid_dictionary[account_qualifiedName] ,
        "attributes": [
            {
            "attr_name":"qualifiedName" ,
            "attr_value": account_qualifiedName
            
            }, 
            {
            "attr_name":"name" ,
            "attr_value": account_name
            },
            {
            "attr_name":"api_type" ,
            "attr_value": "Table"
            }
        ]
        }
        entity_final.append(account_enity_json)

        # List the databases
        logging.info("Entering the database loop ")
        database_initial_guid = -300
        dblist = client.ReadDatabases( options=None)
        for db in dblist:
            #print(db.values())
            database_link =  db['_self']
            database_name = db['id']
            database_lastModifiedTime= db['_ts'] 
            db_offer = list(client.QueryOffers('SELECT * FROM c WHERE c.resource = \'{0}\''.format(db['_self'])))[0] 
            database_offerContent =db_offer['content']
            database_offerLink=db_offer['_self']

            #Retrieving QualifiedName and GUID using QNS service
            database_QNS_info = getQualifiedNameDatabase(cosmos_client_url, database_name, qns_base_url)
            database_qualifiedName= database_QNS_info['qualifiedName']
            if (database_QNS_info['guid'] is not None ) :
                database_guid = database_QNS_info['guid']
            else :
                database_initial_guid -= 1
                database_guid = database_initial_guid

            logging.info("database  " + database_name)
            #Update the GUID dictionary
            guid_dictionary[database_qualifiedName] = database_guid   

        
            database_entity_json = {
                    "entity_type_name": "azure_cosmosdb_database" ,
                    "created_by": "psk",
                    "guid": guid_dictionary[database_qualifiedName],
                    "attributes": [          
                    {
                        "attr_name":"account" ,
                        "attr_value": {
                            "guid": guid_dictionary[account_qualifiedName] ,
                            "typeName": "azure_cosmosdb_account",
                            "optionalAttributes": {}
                        }
                                
                    }, 
                    {
                        "attr_name":"qualifiedName" ,
                        "attr_value":database_qualifiedName 
                    }, 
                    {
                        "attr_name":"name" ,
                        "attr_value": database_name
                    },
                    {
                        "attr_name":"resourceLink" ,
                        "attr_value": database_link
                    },
                    {
                        "attr_name":"lastModifiedTime" ,
                        "attr_value": database_lastModifiedTime
                    },
                    { 
                        "attr_name":"offer" ,
                        "attr_value":  {"content": database_offerContent,"offerLink":database_offerLink},
                    }

                    ]
            }
            entity_final.append(database_entity_json)
            print("\n ")
            collist = client.ReadContainers(database_link, options=None)
            #entity_final = [] 
            for coll in collist:
                logging.info("Entering the container loop ")
                #print(coll.values())
                collection_link = coll['_self']
                collection_name = coll['id']
                collection_defaultTtl =  checkAndAssignKey(coll, 'defaultTtl') 
                collection_isOn = True
                collection_lastModifiedTime= coll['_ts']      
                #collection = client.ReadContainer(collection_link)
                offer = list(client.QueryOffers('SELECT * FROM c WHERE c.resource = \'{0}\''.format(database_link)))[0] 
                collection_offerContent =offer['content']
                collection_offerLink=offer['_self']
                #entity_type_name=settings['ENTITYNAME']

                # Calling QNS to generate the atribute name 
                collection_qualified_name = getQualifiedNameContainer(cosmos_client_url, database_name, collection_name, qns_base_url)['qualifiedName']
                logging.info("collection  " + collection_name)
                # Creating entity for cosmos container
                
                container_entity_json ={
                    "entity_type_name": "azure_cosmosdb_container" ,
                    "created_by": "psk",
                    "attributes": [

                    {

                        "attr_name":"db" ,
                        "attr_value": {
                            "guid": guid_dictionary[database_qualifiedName],
                            "typeName": "azure_cosmosdb_database",
                            "optionalAttributes": {}
                        },
                        "is_entityref": False             
                    }, 
                    {
                        "attr_name":"qualifiedName" ,
                        "attr_value": collection_qualified_name,
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
                entity_final.append(container_entity_json)

    #Call Json Generator          
    
    payload=entity_final  
    logging.info("Calling Json Generator with input as below: \n")
    logging.info(payload)    
        
    json_generator_response=httpPost(entity_final,json_generator_url, "Json-Generator") 
    if json_generator_response.status_code == 200:           
        # Call Atlas Wrapper service
        json_entity_objects= json_generator_response.json() 
        api_output = httpPost(json_entity_objects,atlas_url, "Atlas-Wrapper")
        logging.info("Json generator status code \t"+ str(json_generator_response.status_code))
        if api_output.status_code ==200:
            logging.info("Entity created successfully!")
            logging.info("Atlas status code 2 \t" + str(api_output.status_code))
        else:
            logging.error("Error in calling Atlas Wrapper with error code:"+ str(api_output.status_code) + " "+api_output.text)
    else:
        logging.error("Error in calling JSON generator  with error code:" + str(json_generator_response.status_code) + " "+ json_generator_response.text)

    if mytimer.past_due:
        logging.info('The timer is past due!')
    

    logging.info('Python timer trigger function ran at %s', utc_timestamp)



def checkAndAssignKey(dict, key):      
    if key in dict.keys(): 
        return dict[key]
    return -1

def httpPost(input_content, url, service):
    try:        
        headers = {'Content-type': 'application/json'}
        #later modify according to the verb - maybe a Case , inputs to include , verb, service
        #response = requests.request( "POST", url, data=json.dumps(input_content), headers=headers)
        response = requests.post(url, data=json.dumps(input_content), headers=headers)  
        return response
    except Exception as e:        
        logging.error("error occured in calling "+ service + e)

def getQualifiedNameContainer(cosmosdb_uri, cosmosdb_database, container_name, qns_url):
    qns_request_obj ={
        "cosmosdb_uri":cosmosdb_uri,
        "cosmosdb_database":cosmosdb_database,
        "container_name":container_name
    }
    headers = {'Content-type': 'application/json'}
    qns_final_url = qns_url + "azure_cosmosdb_container"
    response=requests.post(qns_final_url,data=json.dumps(qns_request_obj),headers=headers)
    if response.status_code==200:
        response_text = json.loads(response.content)
        if response_text['isExists']==False:
          return   {'qualifiedName': response_text["qualifiedName"] , 'guid' : None }  
        elif response_text['isExists']==True:
          return {'qualifiedName': response_text["qualifiedName"] , 'guid' : response_text["guid"] }
    else:
        logging.error("Error in validating Qualified Name for Container with error code:"+ str(response.status_code) + " "+response.text)

def getQualifiedNameAccount(cosmosdb_uri, qns_url):
    qns_request_obj ={
        "cosmosdb_uri":cosmosdb_uri
    }
    headers = {'Content-type': 'application/json'}
    qns_final_url = qns_url + "azure_cosmosdb_account"
    response=requests.post(qns_final_url,data=json.dumps(qns_request_obj),headers=headers)
    if response.status_code==200:
        response_text = json.loads(response.content)
        if response_text['isExists']==False:
          return   {'qualifiedName': response_text["qualifiedName"] , 'guid' : None }  
        elif response_text['isExists']==True:
          return {'qualifiedName': response_text["qualifiedName"] , 'guid' : response_text["guid"] }
    else:
        logging.error("Error in validating Qualified Name for Cosmos DB account  with error code:"+ str(response.status_code) + " "+response.text)

def getQualifiedNameDatabase(cosmosdb_uri, cosmosdb_database, qns_url):
    qns_request_obj ={
        "cosmosdb_uri":cosmosdb_uri,
        "cosmosdb_database":cosmosdb_database
    }
    headers = {'Content-type': 'application/json'}
    qns_final_url = qns_url + "azure_cosmosdb_database"
    response=requests.post(qns_final_url,data=json.dumps(qns_request_obj),headers=headers)
    if response.status_code==200:
        response_text = json.loads(response.content)
        if response_text['isExists']==False:
          return   {'qualifiedName': response_text["qualifiedName"] , 'guid' : None }  
        elif response_text['isExists']==True:
          return {'qualifiedName': response_text["qualifiedName"] , 'guid' : response_text["guid"]} 
    else:
        logging.error("Error in validating Qualified Name for Cosmos DB database with error code:"+ str(response.status_code) + " "+response.text)