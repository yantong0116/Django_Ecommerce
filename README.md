# Django Ecommerce

## Introduce
- Build a Django Ecommerce backend project.
- Write Django REST Framework with RESTful API.
- Use JWT authentication to enter certain URLs that require permissions.
- Send details on your url with requests via Postman.

## Installation / How to run the project on your computer
#### Step1 : 
Go into Ecommerce/ directory and install the dependencies by running : 
```
cd Ecommerce/ 
pip install -r requirements.txt
```

#### Step2 : 
You should still be in the directory Ecommerce/ which contains the manage.py file.

Start the server : ```python manage.py runserver```

#### Step3 : 
Keep the server running on that tab.

#### Step4 : 
Run the curl commands from the API section. 

Go to ˋˋˋhttp://127.0.0.1:8000/User ˋˋˋ to create account.

Then go to ˋˋˋhttp://127.0.0.1:8000/User/signIn ˋˋˋto siginIn system to get the JSON Web Token (JWT) authentication code.

You can use JWT token to enter URLs that require authentication.

#### Step5 : 

You can go to ```http://127.0.0.1:8000/swagger/``` to view all the API URLs.

The admin email is : ```r10525116@ntu.edu.tw``` and the password is ```abc34567```

## Main Files
- Ecommerce/Ecommerce/serializers.py
- Ecommerce/Ecommerce/views.py
- Ecommerce/Ecommerce/models.py

## RESTful API
You can interact with the API either using curl commands in the terminal or the Django Rest Framework interface.

## JWT Authentication
Use JWT authentication to enter certain URLs that require permissions.

## HTTP Status
- **200 OK** : Request Success
- **201 Created** : Create Success
- **400 Bad Request** : Invalid Syntax
- **401 Unauthorized** : Error Account or Password
- **403 Forbidden** : Non Authentication
- **404 Not Found** : Server cannot found resource


