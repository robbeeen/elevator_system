# Elevator System

**Description** : 

**Requisite** : Make sure you have Python3 and Pip installed in your System

**How to Run (Windows)** :

1. Install requirements.txt to install necessary packages [**pip install -r requirements.txt**]

2.  Runserver on localhost [**python manage.py runserver**]

3. Go to http://127.0.0.1:8000/ on your browser to visit Home

4. Go to http://127.0.0.1:8000/admin on your browser to visit Admin Panel

**Pre-Existing User Credentials** :

1. Superuser -> Username : admin, Password : admin

**How to Remove existing DB & Make new DB** : 

1. Delete the db.sqlite3 file

2. Create new migration [**python manage.py makemigrations**]

3. Run the new migration [**python manage.py migrate**]

4. Create new Superuser [**python manage.py createsuperuser**]

**How To check the functionality** :
1. Make sure you have installed POSTMAN
2. Select the method as per view requirements
3. Enter the url
4. Complete the body and send the request
5. Go to admin section of site and see the values of the object


