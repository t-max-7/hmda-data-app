"""
This script runs the Flask_Capstone application using a development server.
"""

from os import environ
from Flask_Capstone import app

if __name__ == '__main__':
    HOST = "0.0.0.0"
    try:
        PORT = int(environ.get('PORT', '5000'))
    except ValueError:
        PORT = 5000
    app.run(HOST, PORT)
