package com.ms.cse.api.service;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.UnsupportedEncodingException;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.ProtocolException;
import java.net.URL;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import com.ms.cse.api.apiApp;
import com.ms.cse.api.conf.Constants;
import com.ms.cse.api.exception.CustomAllException;
import com.ms.cse.api.exception.GlobalExceptionHandler;

import sun.misc.BASE64Encoder;

@Service
public class ApiServiceImpl implements ApiService {
	private static final Logger LOG = LoggerFactory.getLogger(ApiServiceImpl.class);

	
	
	@Override
	public String callApi(String method, String inputJSON, String aPIUrl) throws IOException, CustomAllException  {

		String atlasServerIP = Constants.ATLASSERVERIP;
		String atlasServerPort = Constants.ATLASSERVERPORT;
		String userName = Constants.USERNAME;
		String password = Constants.PASSWORD;

		URL url = null;
		
			url = new URL("http://" + atlasServerIP + ":" + atlasServerPort + "/api/atlas/" + aPIUrl);
		
		HttpURLConnection conn = null;

			conn = (HttpURLConnection) url.openConnection( );
		
		conn.setDoOutput(true);

			conn.setRequestMethod(method);
		
		conn.setRequestProperty("Content-Type", "application/json");

		BASE64Encoder enc = new sun.misc.BASE64Encoder();
		String userpassword = userName + ":" + password;
		String encodedAuthorization = enc.encode(userpassword.getBytes()).replaceAll("(\\r|\\n)", "");;
		conn.setRequestProperty("Authorization", "Basic " + encodedAuthorization);

		String input = inputJSON;

		OutputStream os;
		BufferedReader br = null ;
		
			os = conn.getOutputStream();
			os.write(input.getBytes());
			os.flush();
			System.out.println(conn.getResponseCode());
			 String output = "";
				String result="";
			if (200 <= conn.getResponseCode() && conn.getResponseCode() <= 299) {
			    br = new BufferedReader(new InputStreamReader(conn.getInputStream()));
			   
				System.out.println("Output from Server .... \n");
				
					while ((output = br.readLine()) != null) {
						System.out.println("output String : " +output);
						result+=output;
					}
				System.out.println("In 200 sequence :Result is :"+result);
				conn.disconnect();
				return result;
				// throw new CustomAllException(result);
			} else {
				System.out.println("Inside Else");
				try {
				 br = new BufferedReader(new InputStreamReader(conn.getErrorStream()));
				}
				catch(Exception e)
				{
					 throw new CustomAllException(e.getMessage());
				}
				//String output = null;
				//String result="";
				System.out.println("Inside Else");
				while ((output = br.readLine()) != null) {
					System.out.println("output String : " +output);
					result+=output;
				}
				System.out.println(result);
				System.out.println(result);
			    br = new BufferedReader(new InputStreamReader(conn.getErrorStream()));
			    conn.disconnect();
			    System.out.println("In Custom exception other then 200 sequence :Result is :"+result);
			    //CustomAllException customAllException= new CustomAllException(result);
			   throw new CustomAllException(result);

			}
			
		
		//return result;

	}
	

	
	@Override
	public String callApi(String method, String aPIUrl) throws IOException, CustomAllException {

		String atlasServerIP = Constants.ATLASSERVERIP;
		String atlasServerPort = Constants.ATLASSERVERPORT;
		String userName = Constants.USERNAME;
		String password = Constants.PASSWORD;

		int start = aPIUrl.lastIndexOf("=");
		StringBuilder builder = new StringBuilder();
		builder.append(aPIUrl.substring(0, start));
		builder.append("%3D");
		builder.append(aPIUrl.substring(start + "=".length()));
		System.out.println(((builder.toString().replaceFirst(" ", "%20"))).replace(" ", "+"));

		URL url = new URL("http://" + atlasServerIP + ":" + atlasServerPort + "/api/atlas" + (((builder.toString().replaceFirst(" ", "%20"))).replace(" ", "+")));
		HttpURLConnection conn = (HttpURLConnection) url.openConnection();
		conn.setDoOutput(true);
		conn.setRequestMethod(method);
		conn.setRequestProperty("Content-Type", "application/json");

		BASE64Encoder enc = new sun.misc.BASE64Encoder();
		String userpassword = userName + ":" + password;
		String encodedAuthorization = enc.encode(userpassword.getBytes()).replaceAll("(\\r|\\n)", "");;
		conn.setRequestProperty("Authorization", "Basic " + encodedAuthorization);
		
		BufferedReader br = null ;
		 String output = "";
			String result="";
		if (200 <= conn.getResponseCode() && conn.getResponseCode() <= 299) {
		    br = new BufferedReader(new InputStreamReader(conn.getInputStream()));
		   
			System.out.println("Output from Server .... \n");
			
				while ((output = br.readLine()) != null) {
					System.out.println("output String : " +output);
					result+=output;
				}
			System.out.println("In 200 sequence :Result is :"+result);
			conn.disconnect();
			return result;
			// throw new CustomAllException(result);
		} else {
			System.out.println("Inside Else");
			try {
			 br = new BufferedReader(new InputStreamReader(conn.getErrorStream()));
			}
			catch(Exception e)
			{
				 throw new CustomAllException(e.getMessage());
			}
			//String output = null;
			//String result="";
			System.out.println("Inside Else");
			while ((output = br.readLine()) != null) {
				System.out.println("output String : " +output);
				result+=output;
			}
			System.out.println(result);
			System.out.println(result);
		    br = new BufferedReader(new InputStreamReader(conn.getErrorStream()));
		    conn.disconnect();
		    System.out.println("In Custom exception other then 200 sequence :Result is :"+result);
		    //CustomAllException customAllException= new CustomAllException(result);
		   throw new CustomAllException(result);
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
