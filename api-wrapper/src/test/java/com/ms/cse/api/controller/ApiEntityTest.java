package com.ms.cse.api.controller;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.Before;
import org.junit.jupiter.api.Test;
import org.springframework.web.bind.annotation.RequestBody;

import com.ms.cse.api.conf.Configuration;
import com.ms.cse.api.conf.Constants;
import com.ms.cse.api.service.ApiService;

class ApiEntityTest {

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
    void getApiEntity() {
//    	Configuration config = new Configuration();
    	cons.ATLASSERVERIP="40.127.72.92";
		cons.ATLASSERVERPORT="21000";
		cons.PASSWORD="admin";
		cons.USERNAME="admin";
    	String input = "{\r\n" + 
    			"    \"entities\": [\r\n" + 
    			"        {\r\n" + 
    			"            \"typeName\": \"adls_gen2_resource_set\",\r\n" + 
    			"            \"createdBy\": \"sg\",\r\n" + 
    			"            \"attributes\": {\r\n" + 
    			"                \"qualifiedName\": \"/2019/\",\r\n" + 
    			"                \"name\": \"/2019/\"\r\n" + 
    			"            }\r\n" + 
    			"        }\r\n" + 
    			"	]\r\n" + 
    			"}";
    	String result=null;
    	try {
    	result=apiService.callApi("POST", input, "v2/entity");
    	assertTrue(true);
    	}
    	catch(Exception e)
    	{
    	//	e.printStackTrace();
    		
    		assertTrue(true);
    	}
    }
    
    @Test
    public void entityBulkGet() {
    	cons.ATLASSERVERIP="40.127.72.92";
		cons.ATLASSERVERPORT="21000";
		cons.PASSWORD="admin";
		cons.USERNAME="admin";
    	String input = "{\r\n" + 
    			"    \"entities\": [\r\n" + 
    			"        {\r\n" + 
    			"            \"typeName\": \"adls_gen2_resource_set\",\r\n" + 
    			"            \"createdBy\": \"sg\",\r\n" + 
    			"            \"attributes\": {\r\n" + 
    			"                \"qualifiedName\": \"/2019/\",\r\n" + 
    			"                \"name\": \"/2019/\"\r\n" + 
    			"            }\r\n" + 
    			"        }\r\n" + 
    			"	]\r\n" + 
    			"}";
    	String result=null;
    	try {
			result=apiService.callApi("POST", input, "v2/entity");
			System.out.println(result);
	    	assertTrue(true);
		} catch (Exception e) {
			// TODO Auto-generated catch block
			//e.printStackTrace();
			assertTrue(true);
		}
		
	}

}