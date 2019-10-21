package com.ms.cse.api.exception;


import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;
@ResponseStatus(value = HttpStatus.NOT_FOUND)
public class CustomAllException extends Exception{
 private static final long serialVersionUID = 1L;
 public CustomAllException(String message){
     super(message);
    }
public CustomAllException(CustomAllException e) {
	// TODO Auto-generated constructor stub
	super(e);
}
}