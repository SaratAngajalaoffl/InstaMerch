# InstaMerch

# This is part of SOAD project.

## AGENDA:

  1. Make a web application for designing and selling Merch.

  2. Also provide users with an API so that they can integrate our services into their applications

## Setting up the development environment

  * Install `pipenv` by using the command `pip install pipenv`.
  
  * Run `pipenv install` in the project directory to install all the dependencies.
  
  * Run `pipenv shell` to activate the environment.

  * Create a stripe account

  * Install `stripe cli`,instructions can be found [here](https://stripe.com/docs/stripe-cli)
  
  * After installation open your and run `stripe login`
  
  * Follow the login steps,after logging in run `stripe listen --forward-to localhost:8000/api/webhook/`

  * Open `.env.example`,add the values and rename the file to `.env`.
  
  * Change directory into the InstaMerch folder.
  
  * Create Superuser using `python manage.py createsuperuser`.
  
## Running the application
 
  * Navigate to where the manage.py file is in your terminal

  * run `python manage.py runserver`
