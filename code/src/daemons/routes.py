from app import app

@app.route("/")
def home():
	return "<h1>EG Suite - EG Mock App</h1>"

@app.route("/contacts")
def contacts():
	return "<h2>My email is example@gmail.com</h2>"

# API Mock Routes
# Nutanix Prism Central Server
# Mock Output will be handled by these endpoints
# 
import json
from .transactions import *

@app.route("/api/v3")
def api_v3_vmlist():
    Data={
        'title':'Nutanix Prism Central API  v3',
        'endpoint':'/api/v3',
        'payload':'EG Mock is alive'
    }
    return json.dumps(Data)

@app.route("/api/v3/vmlist")
def api_v3():
    Data={
        'title':'VM list',
        'endpoint':'/api/v3/vmlist',
        'payload':'Payload is here'
    }
    return json.dumps(Data)

@app.route("/api/v3/trx_001")
def api_v3_trx_001():
    Data={
        'title':'V3 TRX 001',
        'endpoint':'/api/v3/vmlist',
        'payload':'Payload is here'
    }
    return trx_001(Data)
    
@app.route('/query-example')
def query_example():
    language = request.args.get('language') #if key doesn't exist, returns None
    framework = request.args['framework'] #if key doesn't exist, returns a 400, bad request error
    website = request.args.get('website')

    return '''<h1>The language value is: {}</h1>
              <h1>The framework value is: {}</h1>
              <h1>The website value is: {}'''.format(language, framework, website)
