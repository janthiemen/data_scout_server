Data Scout server
======================================

The server, in combination with the frontend, can be used to create data preparation pipelines in an easy-to-use visual WYSIWYG editor.
This guide explains how to setup the server. If you're looking for a usage guide, you can find that `here <usage.html>`__. 

Installation
------------
There are two ways to setup the server, through the provided Docker image, or by setting it up manually.

Docker
++++++
The easiest and quickest way to install the server is through the provided docker environment. TODO

Manual setup
++++++++++++
Alternatively you can setup the server manually. To do so, follow the steps outlined in this section.

Prerequisites
#############
Before you get started it's important to have all prerequisites available:

- Python 3.5 or higher (using Anaconda or a virtual env is recommended)
- NodeJS (including NPM)
- SQL database (MySQL is recommended)
- Cloned both the data scout frontend and data scout backend packages

Backend
#######
The backend of the data scout server is build in Django. Its main role is to provide the API endpoints that are used by the frontend.

1. Install the requirements::

    pip install -r requirements.txt

2. Setup the SQL connection in the ``data_scout_server/settings.py`` file, according to the instructions `here <https://docs.djangoproject.com/en/3.2/ref/settings/#databases>`_

3. Run the required migrations to setup the database::

    python manage.py migrate

4. Create a Django super user following the instructions `here <https://docs.djangoproject.com/en/3.2/ref/django-admin/#createsuperuser>`_

5. Run the server in development mode::

    python manage.py runserver

Your backend should now be ready to use.

Frontend
########
To actually use the backend you'll need to get the frontend up-and-running as well. The frontend is a React app that requires NodeJS to build and run.

1. Install the required packages::

    npm install

2. Run the frontend::

    npm start

The frontend should now be running and it should be able to connect to your backend. You can login using the Django super user credentials. If you'd like you can create more user accounts from the settings page in the frontend.

.. warning::
    These steps outline how to run the server in development mode. This is **not** supposed to be used in a production environment.  


