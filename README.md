# Food-o-clock
Search engine for recipes.

# Install requirements
`pip install -r requirements.txt`

# How to run the code
Synchronize the DB first:

`python manage.py migrate`
`python manage.py makemigrations foodoclock`
`python manage.py migrate foodoclock`

Run server at http://127.0.0.1:8000/ :

`python manage.py runserver`

# Admin access
The url is http://127.0.0.1:8000/admin/
username: `admin`
password: `master2019`
