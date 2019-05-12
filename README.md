# Feature Request App

This is a feature request app. It allows IWS staff to view, create, update and delete feature requests. This project fulfills the
requirements listed on [PROJECT](https://github.com/edkahara/britecore-implementation-test/blob/master/PROJECT.md).

## How it works

* Users can create feature requests by clicking on the NEW FEATURE REQUEST BUTTON.

* Users can update feature requests by clicking on the Edit button.

* Users can delete feature requests by clicking on the Delete button.

* Users can view the descriptions of their feature requests by clicking on the View button.

* Users can view all feature requests for each client sorted by priority on separate tables.

* Feature requests for each client cannot share priorities. When a created or updated request's priority is similar to that of an existing
request for a client, all of that client's priorities are re-ordered. This is done by incrementing each feature request that has a priority
greater than on equal to the new or updated request's priority by one.

## How To Run The Application Locally

### Create two PostgreSQL databases

  Create two PostgreSQL databases, one for the app and one for testing.

### Clone this repository

  `git clone https://github.com/edkahara/britecore-implementation-test.git`

### Change directories into your repository

  `cd britecore-implementation-test`

### Switch to the project branch

  `git checkout project`

### Create a virtual environment

  `python3 -m venv env` or `py -3 -m venv env` for Windows.

### Set the environment variables

  On the root folder, create a .env file or an env.bat file for Windows and set your environment variables using env.example as a template. Then run:

  `source .env` or `env.bat` for Windows.

### Install the packages needed

  `pip install -r requirements.txt`

### Make migrations

  `python manage.py db init`

  `python manage.py db migrate`

  `python manage.py db upgrade`

### Test the application

  `nosetests tests/tests.py --with-coverage --cover-package=web` or `nosetests --with-coverage --cover-package=web` for Windows.

### Run the application

  `flask run`

  Navigate to <http://localhost:5000> in your web browser to view the application.

## Tech Stack

* Ubuntu 18.04
* Python 3.6.7
* PostgreSQL 11
* Flask
* SQLAlchemy
* jQuery
* Materialize CSS

# Author

Edward Njoroge