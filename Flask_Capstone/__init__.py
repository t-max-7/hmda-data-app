"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
)
print(__name__)

import Flask_Capstone.ad_hoc
import Flask_Capstone.plot_module
import Flask_Capstone.secure_views
