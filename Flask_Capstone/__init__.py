"""
The flask application package.
"""

from flask import Flask
app = Flask("Flask_Capstone")
app.config.update(
SESSION_COOKIE_SECURE=True,
SESSION_COOKIE_HTTPONLY=True,
SESSION_COOKIE_SAMESITE="Lax",
)
print(__name__.split(".")[0])

import Flask_Capstone.ad_hoc
import Flask_Capstone.main_module
import Flask_Capstone.views
