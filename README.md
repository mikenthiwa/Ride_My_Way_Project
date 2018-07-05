[![Coverage Status](https://coveralls.io/repos/github/mikenthiwa/Ride_My_Way_Project/badge.svg?branch=apiv3)](https://coveralls.io/github/mikenthiwa/Ride_My_Way_Project?branch=apiv3)
[![Build Status](https://travis-ci.org/mikenthiwa/Ride_My_Way_Project.svg?branch=apiv3)](https://travis-ci.org/mikenthiwa/Ride_My_Way_Project)
[![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Ride-My-Way

Ride-my App(apiv3) is a carpooling api that provides drivers with the ability to create ride offers and passengers  to join available ride offers.

***
![Home Image](https://raw.github.com/mikenthiwa/Ride-My-Way/apiv1/img.png)

## Getting Started
```
Go to https://github.com/mikenthiwa/Ride-My-Way.git 
Download or clone the repository to your local machine. 
Open the project using your ide
```

***

## Prerequisites

* Python 3 and above.
* Virtual environment.
* Flask
* flask-restplus
* Postman
* Browser e.g Chrome, firefox, safari
* Postgres

***

## Installing

#### Creating virtual environment

On the root directory folder, open cmd.
````
* Run the command: virtualenv venv
* Activating virtual environment : cd venv\Scripts: activate 
````

***
### Application requirements

The requirements.txt files will contain all the requirements needed 
for the application. <br>
To install the requirements :
````
pip install -r requirements.txt 
````

***
Ensure you are located within the root directory and your virtual env. is activated <br/>
Some of the third party modules that will be installed are: 
* flask - Python module used for building web application.
* flask-restplus - flask extension used for developing API.
* Coverage - Python module used in testing, for assessing the quantity of test covered.
* Pytest - Python module for running test.

***

### Postman
Sign up and login to access features. <br>
Endpoint available for this api are shown in the table below:
````

|Requests     |   EndPoint                           | Functionality                         | Fields
|:-----------:|:-------------------------------------:---------------------------------------:------------
   GET        |  /api/v3/rides                       | Get all Rides                         | 
   GET        |  /api/v3/rides/{rideId}              | Get a specific ride                   | id required(int)                     
   DELETE     |  /api/v3/driver/rideId               | Delete ride                           | id required (int)
   POST       |  /api/v3/driver/rides                | Add a ride                            | e.g {"route": "Nairobi-Thika", "driver": "Reg Nduku", "time": 8:00}                                                                                               
   PATCH      |  /api/v3/rides/{rideId}/Request      | Request to join a ride                | e.g {"username": "james", "pick_point": "syokimau", "time": 8:00 }
   PATCH      |  /api/v3/driver/rides/rideId/Accept  | Accept the request passengers request |  
   PUT        |  /api/v3/driver/rides/rideId         | Modify ride details                   |
                                                                                             | if changing route e.g {"route": "Naivasha - Nakuru"}
                                                                                                    "       driver   {"driver": "Kevin Auri"}
                                                                                                    "        time    {"time": "12:00"}
                                                                                                                     
   POST       |  /api/v3/register                    | Register users                        | e.g register as a passanger {"username": "test_user", "email":test_user@gmail.com, "password": "12345"}
                                                                                               e.g register as driver {"username": "test_user", "email":test_user@gmail.com, "password": "12345", "driver": true}
                                                                                               
   POST       |  /api/v3/login                       | Login user                            | e.g {"email: "test_user@gmail.com", "password": "1234"}
   PUT        |  /api/v3/auth/user/email             | Reset password                        | e.g  /api/v3/auth/user/email 
   PUT        |  /api/v3/auth/user/email             | Reset username                        | e.g  /api/v3/auth/user/email 
   GET        |  /api/v3/admin/users                 | Get all users                         |
   PATCH      |  /api/v3/admin/users/<int:user_id>   | Promote users                         | email required
   
  
````

Environment variable
```
export settings:
export SECRET_KEY=!@#$%^&*
export database=dbname=RideMyWaydb

```

Run application on postman
```
http://127.0.0.1:5000 
```

````
***


***

## Running test
````
coverage run -m unittest
pytest
````
***

## Built using

* python 3.6.5
* Flask
* flask-restplus

***



## Heroku

https://ridemywayapiv1.herokuapp.com/api/v3/documentation
***

## Versioning
Most recent version: version 3

***

## Authors
Michael Mutua 

***

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration and encouragement
* etc

***
    
 
