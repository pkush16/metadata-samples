package com.ms.cse.api.controller;


import java.io.IOException;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import org.slf4j.Logger;

import org.slf4j.LoggerFactory;

import com.ms.cse.api.exception.CustomAllException;
import com.ms.cse.api.exception.GlobalExceptionHandler;
import com.ms.cse.api.exception.ResourceNotFoundException;
import com.ms.cse.api.service.ApiService;

import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import io.swagger.annotations.ApiParam;


@Api(value="Atlas Rest API wrapper", description="Operations of entity api on underline Atlas")

@RestController
public class ApiEntity {

	private static final Logger LOG = LoggerFactory.getLogger(ApiEntity.class);
	@Autowired
	ApiService apiService;

	

	@ApiOperation(value = "Add new entity in atlas")
	@PostMapping("/api/entity")
	public String entityPost(@ApiParam(value = "{\r\n" + 
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
			"}", required = true)@RequestBody String input) throws IOException, Exception  {
		try {
			return apiService.callApi("POST", input, "v2/entity");
		} catch (CustomAllException e) {
			e.printStackTrace();
			 throw new CustomAllException(e.getLocalizedMessage());
			// TODO Auto-generated catch block
			//e.printStackTrace();
			//return e.getMessage();
			//return e.
		}
		
	}
	
	
	@GetMapping("/api/entity/bulk")
	public String entityBulkGet(@RequestBody String input) {
		try {
			return apiService.callApi("GET", input, "v2/entity/bulk");
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			return e.getMessage();
		}
		
	}
	
	@DeleteMapping("/api/entity/bulk")
	public String entityBulkDelete(@RequestBody String ipJSON) {
		try {
			return apiService.callApi("DELETE", ipJSON, "v2/entity/bulk");
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			return e.getMessage();
		}
		
	}
	
	@PostMapping("/api/entity/bulk")
	public String entityBulkPost(@RequestBody String ipJSON) {
		try {
			return apiService.callApi("POST", ipJSON, "v2/entity/bulk");
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			return e.getMessage();
		}
		
	}
	
	
	
}