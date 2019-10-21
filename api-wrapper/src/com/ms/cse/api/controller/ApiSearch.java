package com.ms.cse.api.controller;


import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import org.slf4j.Logger;

import org.slf4j.LoggerFactory;

import com.ms.cse.api.service.ApiService;

@RestController
public class ApiSearch {

	private static final Logger LOG = LoggerFactory.getLogger(ApiSearch.class);
	@Autowired
	ApiService apiService;
	
	

/*	@GetMapping("/api/search")
	public String searchBasicGet(@RequestBody String queryString) {
		try {
			return apiService.callApi("GET", queryString, "/v2/search/basic");
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			return e.getMessage();
		}
		
	}
	
*/
	@GetMapping("/api/search")
	public String searchBasicGet(@RequestParam String query) {
		try {
			System.out.println(query);
			System.out.println(encodeValue(query));
			return apiService.callApi("GET", "/v2/search/basic?query="+query);
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			return e.getMessage();
		}
		
	}
	
	private  String encodeValue(String value) {
        try {
            return URLEncoder.encode(value, StandardCharsets.UTF_8.toString());
        } catch (UnsupportedEncodingException ex) {
            throw new RuntimeException(ex.getCause());
        }
    }
	
}