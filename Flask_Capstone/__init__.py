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

import hmda_data_app.ad_hoc
import hmda_data_app.plot_module
import hmda_data_app.secure_views
