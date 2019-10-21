package com.ms.cse.api;


import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import com.ms.cse.api.conf.Configuration;
import com.ms.cse.api.conf.Constants;
import com.ms.cse.api.controller.ApiTypeDefs;
@SpringBootApplication
public class apiApp {
	private static final Logger LOG = LoggerFactory.getLogger(apiApp.class);
	

	public static void main(String[] args) {
		Configuration config = new Configuration();
		System.out.println("Reenu App Started");
		System.out.println(Constants.ATLASSERVERIP);
		
		SpringApplication.run(apiApp.class, args);
	}
}