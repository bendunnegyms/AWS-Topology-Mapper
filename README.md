# AWS-Topology-Mapper
  
(SWENG 2021 Group 38)

## Prerequisites
**npm** (node package manager) is the dependency/package manager you get out of the box when you install Node.js. I installed the react app with the latest version of Node. Node.js allows for javascript code to be executed outside of a browser.
**python 3.8.5** 

## Command Sequence
* To set up and run the Django server:
	`pip install virtualenv` to install the virtual environment creator(probably already have it with your python installation).  \
	`python3 -m venv env` to create a virtual environment on your machine (all of you should have Windows 10 from my memory).  \
	`\env\Scripts\activate.bat\` to activate your virtual environment.  \
	`source env/bin/activate` on Linux. \
	`echo 'env' > .gitignore` so that you don't commit your virtual environment.  \
	`pip install -r requirements.txt` to install all dependencies required for the django server.  \
	`cd src/serversidesrc` to navigate to the correct directory.  \
	`python3 manage.py runserver` to run the server as it is.  \
	The server will be running at **localhost:8000/**.  

## General Functionality
* User Interface:
	The charts are created using Echarts, HTTP GET requests are sent to /graph_data/ to retrieve the json data. \
	The graphs take a while to load due to the amount of links that are needed to be rendered. \
	Pressing enter after making an input will cause the graph to render with those parameters. \
	Page needs to be refreshed to clear the graph due to a javascript bug we didn't have time to fix. \

* Server-side:
	All scripts are contained in /src/serversidesrc/core/apisrc/. \
	All scripts labelled `describe_xxx_xxx.py` contain functions that make API requests, and return the data as a string. \
	All scripts labelled `xxx_to_frontend.py` contain functions that format the data returned by the `describe_xxx_xxx.py` scripts into json blocks in the format:
	```json
	{
		"InstanceId":  "i-123456789",
		"Name": "instance_name",
		"PrivateIpAddress": "1.2.3.4",
		"OutboundAccess": [
			{
				"Destination": "0.0.0.0/0",
				"Protocol": "-1",
				"Ports": "-1"
			}
		],
		"InboundAccess": [
			{
				"Source": "i-987654321",
				"Protocol": "TCP",
				"Port": 80
			},
			{
				"Source": "i-987654321",
				"Protocol": "TCP",
				"Port": 443
			},
			{
				"Source": "sg-123456789",
				"Protocol": "UDP",
				"Port": 123
			}
		]
	}
	``` \
	A single script `compile_data.py` will create a json file in the format needed for Echarts network graphs using the above formats. \
	The file `views.py` contains definitions for REST API endpoints which, when called, call the above functions. \
	Migrations and sqlite database are depreciated, so are the models contained in `models.py`. \
