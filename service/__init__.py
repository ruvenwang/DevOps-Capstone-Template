import os
import logging
from flask import Flask
from flask_cors import CORS
from flask_talisman import Talisman

# Initialize Flask Application
app = Flask(__name__)

# Initialize Cross-Origin Resource Sharing (CORS)
CORS(app)

# Initialize Talisman for secure HTTP headers
talisman = Talisman(app)

# Import routes and models after app initialization to prevent circular dependencies
from service import routes, models
from service.common import error_handlers

# Set up logging level
app.logger.setLevel(logging.INFO)
app.logger.info("Service initialized with security headers and CORS configurations.")
