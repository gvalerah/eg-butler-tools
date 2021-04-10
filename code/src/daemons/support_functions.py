# -------------------------------------------------------------------- #
# Support Functions
# These should be agnostic functions, meaning does not import any 
# other application variables or modules
# -------------------------------------------------------------------- #
"""
def nivel1():
    nivel2()
    
def nivel2():
    nivel3()
    
def nivel3():
    level=0
    for name in inspect.stack()[1]:
        print('nivel3',level,name)
        level+=1
"""
import  os
import  json
import  configparser
from    jinja2          import Template
import  urllib3
import  requests
from    app.templates   import *

import inspect
def this_function():
    return inspect.stack()[1][3]

def get_log(app):
    # defines app wide logger functions
    if app.logger is None:
        log = print
    else:
        log = app.logger.debug
    return log

# Intented for debug tasks
def debug(app=None,data=None):
    """ Debug function, returns IN data and overall app configuration
    
        Returns a JSON string with data and egconfig
    """
    # process data here
    arguments=data
    # contact egmonitor
    response={'data':data,'config':{}}
    for section in app.egconfig.sections():
        response['config'].update({section:{}})
        for option in app.egconfig.options(section):
            response['config'][section].update({option:app.egconfig.get(section,option)})
    # return egmonitor response here as a JSON array
    return json.dumps(response)

def get_request_debug(app,request,data):
    """ Return an HTML view of current request for debug purposes """
    return Template(request_debug).render(app=app,request=request,data=json.dumps(data))    

def read_config(filename=None):
    """ Read Configuration file and returns valid config object """
    caller = f'{inspect.stack()[1][3]}:{this_function()}:'
    config = configparser.ConfigParser()
    # Setup logger function 
    log = print
    if filename is None:
        filename = f"{os.getenv('HOME')}/eg-butler.ini"
    log(f'{caller} filename = {filename}')
    if os.path.exists(filename) and os.path.isfile(filename):
        config.read(filename)
        log(f'{caller} config   = {config}')
        return config
    else:
        log()
        return None

def relay_request(
    app,
    data,
    service  = None,
    username = None,
    password = None,
    protocol = None,
    host     = None,
    port     = None,
    cert     = None,
    pkik     = None,
    verify   = False,
    endpoint = None,
    method   = 'GET',
    warnings = False,
    debug    = False,
    full     = False
    ):
    """ Relays an API Request to a remote server 
    
    Agument | description
    -------  | -----------
    app      | Application object
    data     | Request data received to populate remote request
    service  | Service section present in configuration file, most 
             | request arguments can be specied in config. or be
             | overrided
    http     | Transport protocol: Overrides config
    host     | Service Host: Overrides config
    port     | Service Port: Overrides config
    username | User name: Overrides config
    password | User password: Overrides config
    cert     | PKI Certificate file: Overrides config
    pkik     | PKI Key file: Overrides config
    verify   | Verification Flag: Turns ON/OFF TLS verification
    endpoint | Actual endpoint to be required
    method   | Request type (GET,POST,PUT,PATCH,DELETE)
    warnings | Warnings flag, default is False
    debug    | Development debug flag. default is False
    
    Returns a response object
    """
    # Argument homologation, if required populates form config
    user   = username
    pasw   = password
    http   = protocol
    # get caller function name
    caller = f'{inspect.stack()[1][3]}:{this_function()}:'
    # Setup logger function 
    log = get_log(app)
    if debug:
        log(f'{caller} app={app}')
        log(f'{caller} data={data}')
        log(f'{caller} service={service}')
        log(f'{caller} protocol={protocol}')
        log(f'{caller} host={host}')
        log(f'{caller} port={port}')
        log(f'{caller} username={username}')
        log(f'{caller} password={password}')
        log(f'{caller} cert={cert}')
        log(f'{caller} pkik={pkik}')
        log(f'{caller} verify={verify}')
        log(f'{caller} endpoint={endpoint}')
        log(f'{caller} method={method}')
        log(f'{caller} warnings={warnings}')
        log(f'{caller} debug={debug}')
        log(f'{caller} full={full}')
    try:
        if service is not None:
            # If service specified service defaults populates 'empty' arguments
            if http is None:     http = app.egconfig.get(service,'http',         fallback='http')
            if host is None:     host = app.egconfig.get(service,'host',         fallback=None)
            if port is None:     port = app.egconfig.get(service,'port',         fallback=None)
            if user is None:     user = app.egconfig.get(service,'username',     fallback=None)
            if pasw is None:     pasw = app.egconfig.get(service,'password',     fallback=None)
            if cert is None:     cert = app.egconfig.get(service,'certificate',  fallback=None)
            if pkik is None:     pkik = app.egconfig.get(service,'key',          fallback=None)
            if not warnings: warnings = app.egconfig.get(service,'warnings',     fallback=False)
            if not debug:       debug = app.egconfig.get(service,'debug',        fallback=False)
    except Exception as e:
        log(f'{caller}:relay_request: EXCEPTION: {str(e)}')
        data=None
    try:
        if debug:
            log(f"{caller} will call '{service}' using:")
            log(f'    service    : {service} {host}:{port}') 
            log(f'    protocol   : {http}') 
            log(f'    method     : {method}') 
            log(f'    user/pass  : {user}:{pasw}') 
            log(f'    certificate: {cert}') 
            log(f'    pki key    : {pkik}') 
            log(f'    endpoint   : {endpoint}') 
            log(f'    data       : {data}')
        # call egmonitor
        # response = call eg-monitor and wait for response
        # Replace 'localhost' with your FQDN and certificate CN
        # for TLS verification
        request_url = f"{http}://{host}:{port}{endpoint}"
        headers = {
                'Accept': 'application/json'
                }
        if debug:
            log(f'{caller} request_url : {request_url}')
            log(f'{caller} method      : {method}')
            log(f'{caller} headers     : {headers}')
            log(f'{caller} auth        : {user}:{pasw}')
            log(f'{caller} certificate : {cert}')
            log(f'{caller} key         : {pkik}')
            log(f'{caller} data        : {data} {type(data)}')
        if not warnings:
            urllib3.disable_warnings()
        if   method == 'GET':
            response = requests.get(
                        request_url,
                        headers= headers,
                        auth   = (user, pasw),
                        data   = data,
                        verify = verify,
                        cert   = (cert,pkik)
                        )
        elif method == 'POST':
            response = requests.post(
                        request_url,
                        headers= headers,
                        auth   = (user, pasw),
                        data   = data,
                        verify = verify,
                        cert   = (cert,pkik)
                        )
        elif method == 'PUT':
            response = requests.put(
                        request_url,
                        headers= headers,
                        auth   = (user, pasw),
                        data   = data,
                        verify = verify,
                        cert   = (cert,pkik)
                        )
        elif method == 'PATCH':
            response = requests.patch(
                        request_url,
                        headers= headers,
                        auth   = (user, pasw),
                        data   = data,
                        verify = verify,
                        cert   = (cert,pkik)
                        )
        elif method == 'DELETE':
            response = requests.put(
                    request_url,
                    headers= headers,
                    auth   = (user, pasw),
                    data   = data,
                    verify = verify,
                    cert   = (cert,pkik)
                    )
        else:
            response = None
        if debug: log(f'{caller} Dump response {response} debug={debug} full={full}')
        dump_response(app=app,response=response,debug=debug,full=full)
        if debug: log(f'{caller} After Dump response {response}')

    except Exception as e:
        msg = f"{caller} EG Butler Exception: {str(e)}. Relayed request failed."
        if app.logger is not None:
            app.logger.error(msg)
        else:
            log(msg)
        response = None
    
    if debug: log(f'{caller} will return response={response}')    
    return response

def dump_request(app=None,request=None):
    caller = f'{inspect.stack()[1][3]}:{this_function()}:'
    log = get_log(app)
    try:
        # Setup logger function 
        log(f'{caller} DUMP REQUEST ----------------------->')
        log(f'{caller} app     = {app}')
        log(f'{caller} request = {request}')
        if request is not None:
            log(f'{caller} request.method    = {request.method}')
            log(f'{caller} request.args      = {request.args}{type(request.args)}')
            log(f'{caller} request.form      = {request.form}{type(request.form)}')
            log(f'{caller} request.data      = {request.form}{type(request.data)}')
            log(f'{caller} request.json      = {request.form}{type(request.json)}')
            log(f'{caller} request.get_json()= {request.get_json()}{type(request.get_json())}')
        log(f'{caller}: <----------------------- DUMP REQUEST')
    except Exception as e:
        log(f'{caller} EXCEPTION: {str(e)}')

def dump_response(app=None,response=None,debug=False,full=False):
    caller = f'{inspect.stack()[1][3]}:{this_function()}:'
    log = get_log(app)
    try:
        if debug:
            log(f"{caller} DUMP RESPONSE ---------------------->")
            log(f"{caller} After request execution:")
            log(f"{caller} Request URL : {str(response.url)}")
            log(f"{caller} Status code : {str(response.status_code)}")
            if response is not None:
                if debug:
                    log(f'{caller} response r           = {response}')
                    log(f'{caller} response.status_code = {response.status_code}')
                    log(f'{caller} response.reason      = {response.reason}')
                    if full:
                        log(f'{caller} response.text        = {type(response.text)} ({len(response.text)}) {response.text}')
                        try: log(f'{caller} response.json()      = {type(response.json())} ({len(response.json())}) {len(response.json())}')
                        except: pass
                    else:
                        if len(response.text)>40:
                            sample = f'{response.text[:40]} ...'
                        else:
                            sample = f'{response.text}'
                        log(f'{caller} response.text        = {type(response.text)} ({len(response.text)}) [{sample}]')
                        try: log(f'{caller} response.json()      = {type(response.json())} ({len(response.json())})')
                        except: pass
            log(f"{caller} <---------------------- DUMP RESPONSE")
    except Exception as e:
        print(f'Exception: {str(e)}')
        raise e
        
def get_request_data(request=None,app=None,debug=False):
    """ Gets request data for GET or POST methods
        if DEBUG Field within data the debug flag is turned ON and 
        debug payload is returned
    """
    caller = f'{inspect.stack()[1][3]}:{this_function()}:'
    _debug  = False
    data    = None
    payload = ''
    # Setup logger function 
    log = get_log(app)

    try:
        if request is not None:
            if debug:
                log(f'{caller} request.method    = {request.method}')
                log(f'{caller} request.args      = {request.args}{type(request.args)}')
                log(f'{caller} request.form      = {request.form}{type(request.form)}')
                log(f'{caller} request.get_json  = {request.get_json}')
                log(f'{caller} request.get_json()= {request.get_json()}{type(request.get_json())}')
                log(f'{caller} request.data      = {request.data}{type(request.data)} length={len(request.data)}')
                if len(request.data):
                    log(f'{caller} dict(request.data)      = {json.loads(request.data)}{type(json.loads(request.data))}')
                if request.get_json() is not None:
                    log(f'{caller} dict(request.get_json())= {dict(request.get_json())}')
            if   request.method == 'GET':
                data=json.dumps(dict(request.args))
                if data is not None and 'DEBUG' in dict(request.args).keys():
                    _debug=True
            elif request.method == 'POST':
                data={}
                if len(request.data):
                    # request.data is loaded with JSON data
                    data=json.loads(request.data)
                else:       
                    item=0             
                    for form_item in request.form:
                        if debug: log(f'{caller} form_item={form_item}{type(form_item)}')
                        item+=1
                        if len(form_item):
                            try:
                                data.update(json.loads(form_item))
                            except Exception as e:
                                log(f'{caller} ----------------------')
                                log(f'{caller} WARNING: EXCEPTION: {str(e)}')
                                log(f'{caller} len request.form={len(request.form)}')
                                log(f'{caller}     form.item[{item}]={form_item}')
                                log(f'{caller} len form.item[{item}]={len(form_item)}')
                                log(f'{caller} typ form.item[{item}]={type(form_item)}')
                                log(f'{caller}------------------------')
                if debug:
                    log()
                    log(f'{caller} ***********************************')
                    log(f'{caller} ***********************************')
                    log(f'{caller} data={data}{type(data)}')
                    log(f'{caller} ***********************************')
                    log(f'{caller} ***********************************')
                    log()
                if data is not None and 'DEBUG' in data.keys():
                    _debug=True
            # Code for next methods need to be tested
            elif request.method == 'PUT':
                if request.get_json() is not None:
                    data=json.dumps(dict(request.get_json()))
                    if data is not None and 'DEBUG' in dict(request.get_json).keys():
                        _debug=True
            elif request.method == 'PATCH':
                if data is not None and 'DEBUG' in dict(request.get_json).keys():
                    _debug=True
            elif request.method == 'DELETE':
                data=json.dumps(dict(request.get_json()))
            else:
                data=None
    except Exception as e:
        log(f'{caller} EXCEPTION: str({e})')
        log(f"{caller} -----------------------------------------------")
        log(f"{caller} VARIABLES DUMP")
        log(f'{caller} app     = {app}')
        log(f'{caller} debug   = {debug}')
        log(f'{caller} request = {request}')
        dump_request(app,request)
        log("-------------------------------------------------------")
        raise e

    if _debug:
        payload = f'{get_request_debug(app,request,data)}{data}\n'
    return data,_debug,payload

"""
https://pythonise.com/series/learning-flask/flask-http-methods
"""

