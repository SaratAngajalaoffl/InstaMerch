# InstaMerch

# This is part of SOAD project.

## AGENDA:

  1. Make a web application for designing and selling Merch.

  2. Also provide users with an API so that they can integrate our services into their applications

## Setting up the development environment

  * Install `pipenv` by using the command `pip install pipenv`.

  * Open `.env.example`,add the values and rename the file to `.env`.

  * Create a stripe account

  * Install `stripe cli`,instructions can be found [here](https://stripe.com/docs/stripe-cli)
  
  * After installation open your and run `stripe login`
  
  * Follow the login steps,after logging in run `stripe listen --forward-to localhost:8000/api/webhook/`
  
  * copy the webhook secret and paste it in settings.py file replacing the comment for webhook secret.
  
  * Copy your test public and secret keys from the stripe dashboard and paste them in the respective comment areas in settings.py,you can also use them from your system variables for added security.
  
## Running the application
 
  * Navigate to where the manage.py file is in your terminal

  * run `python manage.py runserver`
