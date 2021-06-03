"""
This script runs the hmda data application using a development server.
"""

from os import environ
from hmda_data_app import app

if __name__ == '__main__':
    HOST = "0.0.0.0"
    try:
        PORT = int(environ.get('PORT', '5000'))
    except ValueError:
        PORT = 5000
    app.run(HOST, PORT)
