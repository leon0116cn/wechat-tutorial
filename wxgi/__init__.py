from flask import Flask
from wxgi import settings


app = app = Flask(__name__)
app.config.from_object(settings)

from wxgi import view