# Data Scout backend
This is the backend for the Data Scout UI. It's written in Django and provides the API endpoints required by the UI 
through the *Django REST Framework* (DRF).

## Docker
TODO: Add Docker scripts

## Installation
Before starting the installation, make sure you've installed all the required **prerequisites**:

* Python (>= 3.7)
* Pip or Conda
* (Optional) SQL Database, by default SQLite is used as a database.

Install the required packages. These can be installed either manually, through the Pip requirements file 
(`pip install -r requirements.txt`) or conda (`conda env create -f environment.yml`).

After installing all requirements, you can now setup the server. To do so use the following steps:

1. (Optional): Setup your database connection by editing `data_scout_server/settings.py -> DATABASES`
1. Change the secret key by editing `data_scout_server/settings.py -> SECRET_KEY` 
1. `python manage.py createsuperuser` - Set up an admin account using your preferred username and password
1. `python manage.py runserver` - A server should now start on [port 8000](http://localhost:8000/)

## Usages
TODO: Add overview of all API endpoints

