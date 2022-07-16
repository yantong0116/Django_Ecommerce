# E-commerce

## Introduce
- Develop a Django Ecommerce backend project.
- Write Django REST Framework with RESTful API.
- Use JWT authentication to enter certain URLs that require permissions.
- Test API with Postman.

## Tool
- Python(Django)、SQLite、JWT、Swagger、RestFul API、Postman
- Custom User Form in Django.

## Installation / How to run the project on your computer
### Step1 : 
cd to the directory which contains the manage.py file.

Start the server : ```python manage.py runserver```

Keep the server running on that tab.

### Step2 : 
Run the curl commands from the API section. 

Go to http://127.0.0.1:8000/User  to create account.

Then go to http://127.0.0.1:8000/User/signIn to siginIn system to get the JSON Web Token (JWT) authentication code.

You can use JWT token to enter URLs that require authentication.

### Step3 : 

You can go to http://127.0.0.1:8000/swagger/ to view all the API URLs.

The admin email is : ```r10525116@ntu.edu.tw``` and the password is ```abc34567```

## API
### RESTful API
You can interact with the API either using curl commands in the terminal or the Django Rest Framework interface.

### HTTP Request
#### Order

|Request|URL|
|---|---|
|[GET]|/Order|
|[POST]|/Order|
|[GET]|/Order/{id}|

#### Product

|Request|URL|
|---|---|
|[GET]|/Product|
|[POST]|/Product|
|[GET]|/Product/{id}|
|[PATCH]|/Product/{id}|
|[DELETE]|/Product/{id}|

#### User
|Request|URL|
|---|---|
|[POST]|/User/|
|[GET]|/User/me|
|[PATCH]|/User/me|
|[POST]|/User/signIn|
|[PATCH]|/User/{id}|

## Main .py files
#### Ecommerce/

|File name|description|
|---|---|
|settings.py|project environment setting|
|urls.py|urls|

#### Shop/

|File name|description|
|---|---|
|admin.py|models displayed on the admin board|
|apps.py|record the project app|
|forms.py|custom User form|
|managers.py|custom user manager|
|models.py|create database table|
|serializers.py|setting the fields which have to view on the page, frequently used in views.py|
|urls.py|urls|
|views.py|API response, used in urls.py|

#### image/
Store product images.

## Authentication
### JWT Authentication
Use JWT authentication to enter certain URLs that require permissions.

## HTTP Status
- **200 OK** : Request Success
- **201 Created** : Create Success
- **400 Bad Request** : Invalid Syntax
- **401 Unauthorized** : Error Account or Password
- **403 Forbidden** : Non Authentication
- **404 Not Found** : Server cannot found resource
