# Cryptocurrency Tracker

## Description
 App allows for simulation of purchasing cryptocurrency while tracking changes in value based on deposits and withdrawals. Data is obtained from CoinGecko public API and is stored in personal PostgreSQL database. Web app uses Django framework with Python utilities. 

## How to use
 The code requires Python 3 which can be downloaded from https://www.python.org/downloads/ and PostgreSQL which can be downloaded at https://www.postgresql.org/download/. /crypto_util/crypto.py contains all functionality for the web page. /cryptoApp/ contains all files for the Django front end. The PostgreSQL database info and user info should be placed into /crypto_util/crypto.py in the connectDB function starting at line 8. The server can be started using command prompt by navigating to your /cryptoApp/ directory using "cd **your directory here** and inputting "python manage.py runserver". The web page can be accessed from your localhost/crypto/.
 
 ## Dependencies
 The bot requires the following Python libraries: requests, psycopg2, decimal, re.
