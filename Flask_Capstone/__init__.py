"""
The flask application package.
"""

from flask import Flask
app = Flask("Flask_Capstone")
print(__name__.split(".")[0])

import Flask_Capstone.ad_hoc
import Flask_Capstone.main_module
import Flask_Capstone.views
