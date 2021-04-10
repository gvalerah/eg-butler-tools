#  we import the class.
from flask import Flask
from flask import request

# create an instance, the variable __name__ passed to the Flask class 
# is a predefined variable Python, 
# which is set on the name of the module in which it is used.
app = Flask(__name__)

# the routes file that will manage the routing of the web app is imported
from app import routes
