# Schedule

System for scheduling the pickup of an order

[![codecov](https://codecov.io/gh/Derhks/Pickup-You/branch/main/graph/badge.svg?token=QvK8AQvUKE)](https://codecov.io/gh/Derhks/Pickup-You)

## Table of Content

* [Development Environment Configuration](#development-environment-configuration-ubuntu-2004)
  * [Prerequisites](#prerequisites)
  * [Downloading the app](#downloading-the-app)
  * [Create a virtual environment with Pyenv](#create-a-virtual-environment-with-pyenv)
  * [Setup SQLite](#setup-sqlite)
  * [Create superuser](#create-superuser)
  * [Run server](#run-server)
* [Run development version with docker](#run-development-version-with-docker)
* [Endpoints](#endpoints)
  * [Interactive API docs](#interactive-api-docs)
  * [Postman](#postman)
* [Built With](#built-with)
* [Authors](#authors)

________________________________________________________________________________
## Development Environment Configuration (Ubuntu 20.04)

### Prerequisites

The following programs must be installed:
- Git version 2.25.1
- Pyenv version 2.3.4

Verify that you have `Git` and `Pyenv` installed on your computer, run the 
following commands:

```bash
git --version
```

```bash
pyenv --version
```

If you do not see the `Git` or `Pyenv` version, you must install it.

### Downloading the app

```bash
git clone https://github.com/Derhks/Pickup-You.git
```

Enter the project folder

```bash
cd Pickup-You/
```

### Create a virtual environment with Pyenv

Install the version of `Python` to be used by the virtual environment:

```bash
pyenv install -v 3.9.13
```

Create the `pickupyou` virtual environment

```bash
pyenv virtualenv 3.9.13 pickupyou
```

Now, let's activate the created virtual environment

```bash
pyenv activate pickupyou
```

To deactivate an active environment, use:

```bash
pyenv deactivate
```

### Install project dependencies

With the virtual environment activated we are going to install the dependencies 
used in the project

```bash
pip3 install --upgrade pip && pip3 install -r requirements.txt
```

We must export the environment variables we need in our project. Create the 
.env file by executing the following command:

```bash
mv pickupyou/.example pickupyou/.env
```

Fill in the environment variables with their corresponding value. Finally, 
execute the following command:

```bash
export $(cat pickupyou/.env | grep -v ^# | xargs)
```

### Setup SQLite

We must create the tables that will be used by the applications in the project, 
to do so, execute the following commands:

```bash
python3 manage.py makemigrations
```

Now we create the tables of all the models that need one in the database, 
execute the command:

```bash
python3 manage.py migrate
```

### Create superuser

If you need to create a user who can log in to the administrative site, run 
the following command:

```bash
python3 manage.py createsuperuser
```

You must fill in the Username, Email address and Password fields to create the 
user. Start the server and enter the `/admin/` endpoint and verify that you can 
access the administrative site with the user you created.


### Run server

The application has its unit tests, run one of the following commands before 
running the server:

```bash
python3 manage.py test
```

Note: if running the above command fails some tests, remove the environment 
variable by executing the command 

```bash
unset URL_DRIVERS_LOCATIONS
```

And run the command again.

Let's verify that the project works, run the following command:

```bash
python3 manage.py runserver 8000
```

With the above command the server will operate on port 8000.

Validate from the command terminal that the server is working correctly. 
Execute the following command from another terminal:

```bash
curl -H 'Accept: application/json; indent=4' -u `user`:`password` http://127.0.0.1:8000/
```

________________________________________________________________________________
## Run development version with docker

Before proceeding, validate that you have Docker installed. Run the following 
command:

```bash
sudo docker run hello-world
```

Run the following command to initialize the project using docker:

Note: The project needs environment variables that are declared in the 
`.env` file, complete all variables that do not have any value assigned, 
this is necessary for the command below to work.

```bash
docker-compose up --remove-orphans
```

At this point the application is running on port 8080 on your Docker host. Go 
to `http://localhost:8080/swagger/` in a web browser.

You can stop the containers and also delete everything that was 
created at initialization by executing the following command:

```bash
docker-compose down --rmi all && sudo rm -rf data/
```

________________________________________________________________________________
## Endpoints

### Interactive API docs

Now go to `http://127.0.0.1:8000/swagger/`.

You will see the automatic interactive API documentation 
(provided by Swagger UI)

### Postman

`GET /coordinates/`

API endpoint to view all coordinates.

```bash
curl --location --request GET 'http://127.0.0.1:8000/coordinates/' \
--header 'accept: application/json' \
--header 'Authorization: Basic Auth'
```

`POST /coordinates/`

API endpoint to create coordinates.

```bash
curl --location --request POST 'http://127.0.0.1:8000/coordinates/' \
--header 'accept: application/json' \
--header 'Content-Type: application/json' \
--header 'Authorization: Basic Auth' \
--data-raw '{
  "latitude": "string",
  "longitude": "string"
}'
```

`GET /drivers/`

API endpoint to view all drivers.

```bash
curl --location --request GET 'http://127.0.0.1:8000/drivers/' \
--header 'accept: application/json' \
--header 'Authorization: Basic Auth'
```

`POST /drivers/`

API endpoint that allows you to create a driver.

```bash
curl --location --request POST 'http://127.0.0.1:8000/drivers/' \
--header 'accept: application/json' \
--header 'Content-Type: application/json' \
--header 'Authorization: Basic Auth' \
--data-raw '{
  "first_name": "string",
  "last_name": "string"
}'
```

`GET /drivers/{id}/orders/{day}/`

API endpoint that allows to view the orders assigned to the driver on the 
specified day.

```bash
curl --location --request GET 'http://127.0.0.1:8000/drivers/2/orders/2022-10-19/'
```

`GET /nearest-driver/`

API endpoint that allows you to see the nearest driver.

```bash
curl --location --request GET 'http://127.0.0.1:8000/nearest-driver/?latitude=1&longitude=7&day=2021-12-10&hour=00:00:00'
```

`GET /orders/`

API endpoint to view all orders

```bash
curl --location --request GET 'http://127.0.0.1:8000/orders/' \
--header 'accept: application/json' \
--header 'Authorization: Basic Auth'
```

`GET /orders/{day}`

API endpoint that allows you to view the orders assigned on the specified day.

```bash
curl --location --request GET 'http://127.0.0.1:8000/orders/2022-10-19'
```

`POST /orders/`

API endpoint that allows you to create an order.

```bash
curl --location --request POST 'http://127.0.0.1:8000/orders/' \
--header 'Content-Type: application/json' \
--header 'accept: application/json' \
--header 'Authorization: Basic Auth' \
--data-raw '{
  "title": "string",
  "day": "YYYY-MM-DD",
  "start_time": "string",
  "driver": "string",
  "pickup_point": "string",
  "destination_point": "string"
}'
```

________________________________________________________________________________
## Built With

- [Python](https://www.python.org/) - Programming language
- [Django](https://www.djangoproject.com) - Web framework
- [SQLite](https://www.sqlite.org/index.html) - Database

________________________________________________________________________________
## Authors
- **Juli??n Sandoval [derhks](https://www.linkedin.com/in/sandoval-julian/)**
