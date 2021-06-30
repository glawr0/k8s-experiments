
from flask import Flask

app = Flask(__name__)

@app.route('/')
def default_route():
	return "Hello, World!"

