from flask import Flask
from dotenv import load_dotenv

# Loading from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = 'OurSecretKey'

from freelancehq import routes