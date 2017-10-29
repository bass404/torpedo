import os

basedir = os.path.abspath(os.path.dirname(__file__))

WTF_CSRF_ENABLED = True
SECRET_KEY = 'QvGs0b2xuJJq4J1z'

# Details for mongodb
MONGODB_DB = 'torpedo'
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017

SECURITY_REGISTERABLE = True

SECURITY_PASSWORD_HASH = "bcrypt"
SECURITY_PASSWORD_SALT = "$~zmT+tQ;5Q>U6uE"
