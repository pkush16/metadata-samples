package com.ms.cse.api.conf;



public final class Configuration {

	public Configuration(){

		Constants.ATLASSERVERIP=System.getenv("AtlasServerIP");

		Constants.ATLASSERVERPORT=System.getenv("AtlasServerPort");

		Constants.USERNAME=System.getenv("AtlasUserName");

		Constants.PASSWORD=System.getenv("AtlasPassword");


	}
}
