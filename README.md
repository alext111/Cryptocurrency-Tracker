# Cryptocurrency Tracker

## Description
 App allows for simulation of purchasing cryptocurrency while tracking changes in value based on deposits and withdrawals. Data is obtained from CoinGecko public API and is stored in personal PostgreSQL database. Web app uses Django framework with Python utilities. 

## How to use
 The code requires Python 3 which can be downloaded from https://www.python.org/downloads/ and PostgreSQL which can be downloaded at https://www.postgresql.org/download/. \crypto_util\crypto.py contains all functionality for the web page. /cryptoApp/ contains all files for the Django front end. The PostgreSQL database info and user info should be placed into \crypto_util\crypto.py in the connectDB function starting at line 8. The server can be started using command prompt by navigating to your \cryptoApp\ directory using "cd *your directory here* and inputting "python manage.py runserver". The web page can be accessed from your localhost/crypto/. Cryptocurrency IDs for deposits and withdrawals can be found at https://www.coingecko.com/en/api.
 
## Dependencies
 The app requires the following Python libraries: requests, psycopg2, decimal, re.

## Example
![cryptotable](https://user-images.githubusercontent.com/49249379/122615949-6dee5480-d057-11eb-9567-1a0b3f910d83.PNG)
