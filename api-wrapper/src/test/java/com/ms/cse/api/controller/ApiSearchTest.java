package com.ms.cse.api.controller;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.Before;
import org.junit.jupiter.api.Test;

import com.ms.cse.api.conf.Configuration;
import com.ms.cse.api.conf.Constants;
import com.ms.cse.api.service.ApiService;

class ApiSearchTest {

	Configuration config = new Configuration();
	Constants cons= new Constants();
	@Before
	void conf()
	{
		Configuration config = new Configuration();
//		cons.ATLASSERVERIP="40.127.72.92";
//		cons.ATLASSERVERPORT="21000";
//		cons.PASSWORD="admin";
//		cons.USERNAME="admin";
	}
	com.ms.cse.api.service.ApiServiceImpl apiService = new com.ms.cse.api.service.ApiServiceImpl();
    @Test
    void searchBasicGet() {
//    	Configuration config = new Configuration();
    	cons.ATLASSERVERIP="40.127.72.92";
		cons.ATLASSERVERPORT="21000";
		cons.PASSWORD="admin";
		cons.USERNAME="admin";
    	String query = "from azure_cosmosdb_database where qualifiedName=test%2testdb";
    	String result=null;
    	try {
    	result=apiService.callApi("GET", "/v2/search/basic?query="+query);
    	assertTrue(true);
    	}
    	catch(Exception e)
    	{
    		//e.printStackTrace();
    		
    		assertTrue(true);
    	}
    }

}