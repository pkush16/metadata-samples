package com.ms.cse.api.controller;


import java.io.IOException;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import com.ms.cse.api.service.ApiService;

@RestController
public class ApiTypeDefs {

	
	private static final Logger LOG = LoggerFactory.getLogger(ApiTypeDefs.class);
	
	
	@Autowired
	ApiService apiService;
	

	
	
	@GetMapping("/api/typedefs")
	public String typedefsGet(@RequestBody String ipJSON) {
		try {
			return apiService.callApi("GET", ipJSON, "v2/types/typedefs");
		} catch (Exception e) {
			// TODO Auto-generated catch block
			System.out.println("In Exception "+e.fillInStackTrace());
			e.printStackTrace();
			return e.getMessage();
		}
		
	}
	
	@DeleteMapping("/api/typedefs")
	public String typedefsDelete(@RequestBody String ipJSON) {
		try {
			return apiService.callApi("DELETE", ipJSON, "v2/types/typedefs");
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			System.out.println("In Exception "+e.fillInStackTrace());
			return e.getMessage();
		}
		
	}
	
	@PostMapping("/api/typedefs")
	public String typedefsPost(@RequestBody String ipJSON) {
		try {
			return apiService.callApi("POST", ipJSON, "v2/types/typedefs");
			
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			System.out.println("In Exception "+e.fillInStackTrace());
			return e.getMessage();
		}
		
	}
	
	@PutMapping("/api/typedefs")
	public String typedefsPut(@RequestBody String ipJSON) {
		try {
			return apiService.callApi("PUT", ipJSON, "v2/types/typedefs");
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			return e.getMessage();
		}
		
	}
	
	
	
	
}