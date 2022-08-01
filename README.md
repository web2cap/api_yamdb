## Project System of reviews and ratings for products

### Project details:

The **YaMDb** project is designed to collect feedback on products.
Products can be: *"Books"*, *"Movies"*, *"Music"*.

### Project composition:

The project includes:

1. A system for storing and processing information on products, reviews and users.
2. A system for remote access to information, implemented using the REST architecture.

### Project features:

1. The project allows you to store information:
    * about users
    * about products
    * about product reviews and their comments
2. The project allows you to specify additional information about products:
    * genre (fantasy, thriller, etc.)
    * category (movie, book, music, etc.)
3. The project allows you to work with users:
    * register user
    * get information about your user
    * receive authentication parameters for working via the API protocol
4. The project allows you to specify the user's access role:
    * user
    * moderator
    * administrator
5. The project allows you to add reviews to products:
    * the review is given a score (from 1 to 10)
    * products have an automatically calculated rating on
based on ratings in reviews

### Project API features:

1. Users
    * adding a user
    * get authentication parameters
    * user management (delete, change, view)
2. Categories
    * adding categories
    * category management (delete, view)
3. Genres
    * adding genres
    * genre management (delete, view)
4. Products
    * addition product
    * product management (delete, change, view)
5. Product reviews
    * adding reviews
    * reviews management (delete, change, view)
6. Comments on reviews
    * adding comments
    * comment management (delete, change, view)

### Technical requirements of the project

```
python3.7.9
django 2.2.16
djangorestframework 3.12.4
djangorestframework-simplejwt 5.1.0
django-filter 21.1
```

### How to start the project:

Clone the repository and change into it on the command line:

```
git clone https://github.com/web2cap/api_yamdb.git
```

```
cd api_yamdb
```

Create and activate virtual environment:

```
python3 -m venv venv
```

```
source venv/bin/activate
```

```
python3 -m pip install --upgrade pip
```

Install dependencies from requirements.txt file:

```
pip install -r requirements.txt
```

Run migrations:

```
python3 manage.py migrate
```

You can load test data into the database:

```
python3 manage.py loaddata
```

Run project:

```
python3 manage.py runserver
```

### API description

A description of the project methods API is available at: http://127.0.0.1:8000/redoc/

### Author:

The development team of the 32 Yandex.Practicum categories:
* Pavel Koshelev (Teamlead)
* Kirillov Evgeny
* Sudoplatova Marina


### About the development process:

The project was developed in a team, using the agile methodology. We used Trello as a task tracker. I was a team leader, responsible for the development process, team morale, developed the authorization section and the Users application. All project developers conducted code reviews.