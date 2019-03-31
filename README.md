# Food-o-clock
Search engine for recipes. The website is built using the framewrork 
`django` and a `sqlite3` database.

# Install requirements
To install the requirements needed to deploy the project run:
`pip install -r requirements.txt`

# How to run the code
Synchronize the DB first with the following commands in sequence:

1. `python manage.py migrate`
2. `python manage.py makemigrations foodoclock`
3. `python manage.py migrate foodoclock`

Run server at http://127.0.0.1:8000/ :

`python manage.py runserver`

<!-- # Admin access
The url is http://127.0.0.1:8000/admin/
username: `admin`
password: `master2019` -->

# Create an account
To access the search engine you will need to create an account first.

# Install new apps
`python settings.py install`