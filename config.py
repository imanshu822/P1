import os
from dotenv import load_dotenv
 
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config():
    '''
    Set config variables for the flask app
    Using Environment variables where available.
    Otherwise create the config variable if not done already
    '''

    FLASK_APP = 'finalproject'
    FLASK_ENV = 'development'
    SECRET_KEY = 'secret'
    # Replace these with your ElephantSQL connection details
    ELEPHANTSQL_USER = 'xdyoyyen'
    ELEPHANTSQL_PASSWORD = 'YWUh2Qz_05ZyzKtTLefPUhxF6e5hzQdi'
    ELEPHANTSQL_HOST = 'suleiman.db.elephantsql.com'
    ELEPHANTSQL_PORT = '5432'
    ELEPHANTSQL_DATABASE = 'xdyoyyen'

    # Constructing the ElephantSQL connection string
    SQLALCHEMY_DATABASE_URI = f"postgresql://{ELEPHANTSQL_USER}:{ELEPHANTSQL_PASSWORD}@{ELEPHANTSQL_HOST}:{ELEPHANTSQL_PORT}/{ELEPHANTSQL_DATABASE}"

    SQLALCHEMY_TRACK_NOTIFICATIONS = False
    
