Rule Based Chatbot
===================

This repository contains the code for chatbot. I have developed this chatbot using template based approach.

## Dependencies

In oreder to run this you need forllowing libraries.

* flask
* flask_cors
* json
* os
* flask_pymongo
* pytz
* datetime
* uuid

## Installation

* OS, json, datetime and uuid are default python libraries


* Install Flask libraries using following commands:
```bash
 $ sudo pip install Flask==0.12.2
 $ sudo pip Flask-Cors==3.0.2
 $ sudo Flask-PyMongo==0.5.1
```
* Installlation of pytz library
```bash
 $ sudo pip install pytz==2017.2
```


* Install MongoDB NoSQL db by following this step.
```bash
 $ sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 0C49F3730359A14518585931BC711F9BA15703C6
 $ echo "deb [ arch=amd64,arm64 ] http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.4.list
 $ sudo apt-get update
 $ sudo apt-get install -y mongodb-org
 $ sudo service mongod start

```
 ## usage
1. First run `flaskengin.py` 

2. Go to the URL: 

3. `http://0.0.0.0:5002/` where you can see Hello from chatbot Flask! 

4. You can see the chatbot JSON response by using this URL: 
```http://0.0.0.0:5002/welcomemsg_chat```

5. After that you can hit the following urls
  ```
  http://0.0.0.0:5002/hi_chat?msg=Hi
  http://0.0.0.0:5002/asking_borowers_full_name?msg=<your name> 
  http://0.0.0.0:5002/asking_borowers_email_id?msg=<Your email address>
  ```
 