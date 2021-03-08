# AWS-Topology-Mapper
  
  This readme will describe setting up the environment for now.
  
## Prerequisites
**npm** (node package manager) is the dependency/package manager you get out of the box when you install Node.js. I installed the react app with the latest version of Node. Node.js allows for javascript code to be executed outside of a browser.
**python 3.8.5** 

## Commands to execute
* To set up and run the Django server:
	`pip install virtualenv` to install the virtual environment creator(probably already have it with your python installation).
	`python3 -m venv env` to create a virtual environment on your machine (all of you should have Windows 10 from my memory).
	`\env\Scripts\activate.bat\` to activate your virtual environment.
	`echo 'env' > .gitignore` so that you don't commit your virtual environment.
	`pip install -r requirements.txt` to install all dependencies required for the django server.
	`cd src/serversidesrc` to navigate to the correct directory.
	`python manage.py runserver` to run the server as it is.
	The server will be running at **localhost:8000/wel**.
	
* To run the ReactJS App:
	`cd src` to navigate to the *src* directory.
	`npm start` will start the React server on **localhost:3000**.


