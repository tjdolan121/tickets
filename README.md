# Tickets

![Tickets](static/img/SS_Tickets.png?raw=true "Tickets")

#### CONTEXT: Along with "NMC" and "GABC", this app was designed as a "concept app" to streamline various processes in the DoD. This app deals with streamlining customer IT support in deployed locations, where such applications might not be available.

#### It was my first starter project, and it is based off of Vitor Freita's incredibly comprehensive "A Complete Beginner's Guide to Django".

#### This tutorial introduced me to Django, and can be found [here](https://simpleisbetterthancomplex.com).

###### Contributions are always welcome!  Whether you are new to Django or web development in general (like me) or you're more experienced, you are more than welcome to contribute!

STEP 1: Clone the project (in the terminal): ```git clone git@github.com:tjdolan121/tickets.git```

STEP 2: Create a new virtual environment: ```virtualenv env```

STEP 3: Activate the virtual environment: ```source env/bin/activate```

STEP 4: Navigate to the project directory (should contain "manage.py" file) and install requirements: ```pip install -r requirements.txt```

STEP 5: Obtain a SECRET_KEY: https://www.miniwebtool.com/django-secret-key-generator/

STEP 5: Create a .env file in the project directory

STEP 6: Add a secret key environment variable (in .env): ```SECRET_KEY=(paste key here)```

STEP 7: Run migrations (while in project directory): ```python manage.py migrate```

STEP 8: Create a superuser account: ```python manage.py createsuperuser```

STEP 9: Run server: ```python manage.py runserver```

STEP 10: Navigate to http://127.0.0.1:8000/admin in browser, log in with your super user account, and create some data.

#### Commits to master are set to auto-deploy to the staging app, found here: https://pure-retreat-74022.herokuapp.com

### Feel free to message me if you have any questions!