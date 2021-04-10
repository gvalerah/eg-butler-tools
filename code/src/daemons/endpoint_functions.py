# End point functions
# Functions required imports
import  json
import  requests
import  json
import  urllib3
from    pprint import pprint,pformat
from    .support_functions import *

# ----------------------------------------------------------------------
# EG Butler Endpoint Functions
# ----------------------------------------------------------------------
def egbutler_request(app,data,debug=False):
    return json.dumps({"status":f"function {this_function()} not implemented yet."})

def request_create(app,data,debug=False):
    return json.dumps(None)

# ----------------------------------------------------------------------
# EG Monitor Endpoint Functions
# ----------------------------------------------------------------------

"""
#curl -k  
#    -u butler:butler 
#    -H 'Accept: application/json' 
#    -X GET 
#    https://192.168.56.102:5665
#    /v1/objects/host
"""
def egmonitor_host(app,data,debug=False):
    """ Create a new API Host in Icinga2 
    
    Agument | description
    ------- | -----------
    app     | Application object
    data    | Request data received
            | address: Host IP Address (mandatory)
            | os     : OS specification (optional) (Linux,Windows,AIX,...)
    """
    # process data here
    # endpoint has a default hard coded and depends of Icinga2 API version
    # can be overrided in configuration file
    caller = f'{inspect.stack()[1][3]}:{this_function()}:'
    log    = get_log(app)
    payload=None
    debug=True
    try:
        #host = app.egconfig.get('eg-monitor','host')
        #port = app.egconfig.get('eg-monitor','port')
        #user = app.egconfig.get('eg-monitor','username')
        #pasw = app.egconfig.get('eg-monitor','password')
        #cert = app.egconfig.get('eg-monitor','certificate')
        #pkik = app.egconfig.get('eg-monitor','key')
        endpoint=app.egconfig.get('eg-monitor','host_list',fallback='/v1/objects/hosts')
    except Exception as e:
        payload=None
        if debug:
            log(f"{caller} eg-monitor   : {app.egconfig.get('eg-monitor','host')}:{app.egconfig.get('eg-monitor','port')}")
            log(f"{caller} endpoint     : {endpoint}")
            log(f"{caller} data         : {data}")
            log(f'{caller} Request is bad formed: EXCEPTION: {str(e)}')
    try:
        if debug:
            log(f'{caller} call')
            #log(f'    egmonitor: {host}:{port}') 
            #log(f'    user/pass: {user}:{pasw}') 
            log(f'    endpoint : {endpoint}') 
            log(f'    payload  : {payload}')
        # call egmonitor
        # response = call eg-monitor and wait for response
        # Replace 'localhost' with your FQDN and certificate CN
        # for TLS verification
        #request_url = f"https://{host}:{port}{endpoint}"
        headers = {
                'Accept': 'application/json'
                }
        if debug:
            #log(f'{caller} request_url : {request_url}')
            log(f'{caller} headers     : {headers}')
            #log(f'{caller} auth        : {user}:{pasw}')
            #log(f'{caller} certificate : {cert}')
            #log(f'{caller} data        : {data} {type(data)}')
        response = relay_request(
            app,
            data,
            debug=debug,
            service='eg-monitor',
            endpoint=endpoint,
            method='GET'
            )
        dump_response(app,response=response,debug=debug,full=False)
        if response is not None:
            code   = response.status_code
            fulldata = response.json()
            hosts=[]
            for host in response.json()['results']:
                hosts.append({
                    'name':host['name'],
                    'type':host['type'],
                    'active':host['attrs']['active'],
                    'address':host['attrs']['address'],
                    'state':host['attrs']['state'],
                    'state_type':host['attrs']['state_type'],
                    })
            #status = json.dumps(hosts)
            status = hosts
            if debug: log(str(hosts))
        # return egmonitor response here as a JSON array
    except Exception as e:
        log(f"{caller} EG Butler Exception: {str(e)}. EG Monitor Object was not created.")
        code   = 500.0
        status = f"EG Butler Exception: {str(e)}. EG Monitor Object was not created."

    response={ 'results': [ { 'code':code, 'status':status } ] }
    return json.dumps(response)

"""
curl -k  -u butler:butler 
    -H 'Accept: application/json' 
    -X PUT https://monitor:5665/v1/objects/hosts/TEST-API 
    -d '{   "templates": [ "generic-host" ], 
            "attrs": { "address": "10.26.1.247", "check_command": "hostalive", "vars.os" : "Linux" }, 
            "pretty": true 
        }'
{
    "results": [
        {
            "code": 200.0,
            "status": "Object was created"
        }
    ]
}(venv) [gvalera@eg-suite-lab-mock eg-butler]$
"""
def egmonitor_host_create(name,app,data,debug=False):
    """ Create a new API Host in Icinga2 
    
    Agument | description
    ------- | -----------
    app     | Application object
    data    | Request data received
            | address: Host IP Address (mandatory)
            | os     : OS specification (optional) (Linux,Windows,AIX,...)
    """
    # process data here
    # endpoint has a default hard coded and depends of Icinga2 API version
    # can be overrided in configuration file
    try:
        http     = app.egconfig.get('eg-monitor','http',fallback='https')
        host     = app.egconfig.get('eg-monitor','host',fallback=None)
        port     = app.egconfig.get('eg-monitor','port',fallback=None)
        user     = app.egconfig.get('eg-monitor','username',fallback=None)
        pasw     = app.egconfig.get('eg-monitor','password',fallback=None)
        cert     = app.egconfig.get('eg-monitor','certificate',fallback='pki/butler.crt')
        pkik     = app.egconfig.get('eg-monitor','key',fallback='pki/butler.key')
        verify   = app.egconfig.get('eg-monitor','verify',fallback=False)
        endpoint = app.egconfig.get('eg-monitor','host_create',fallback='/v1/objects/hosts')
        # Icinga2 API Payload requirements
        payload={
            'templates':['generic-host'],
            'attrs':{
                'address':data['address'],
                'check_command':'hostalive'
            }
        }
        if 'os'     in data.keys(): payload['attrs'].update({'vars.os':data['os']})
        if 'pretty' in data.keys(): payload.update({'pretty':data['pretty']})
    except Exception as e:
        payload=None
        if debug:
            print(f"egmonitor_host_create: eg-monitor   : {app.egconfig.get('eg-monitor','host')}:{app.egconfig.get('eg-monitor','port')}")
            print(f"egmonitor_host_create: endpoint     : {endpoint}")
            print(f"egmonitor_host_create: data         : {data}")
            print(f'egmonitor_host_create: Request is bad formed: EXCEPTION: {str(e)}')
    if payload is not None:
        try:
            if debug:
                print(f'egmonitor_host_create: call')
                print(f'    egmonitor: {host}:{port}') 
                print(f'    user/pass: {user}:{pasw}') 
                print(f'    endpoint : {endpoint}') 
                print(f'    name     : {name}') 
                print(f'    payload  : {payload}')
            # call egmonitor
            # response = call eg-monitor and wait for response

            # Replace 'localhost' with your FQDN and certificate CN
            # for TLS verification
            request_url = f"{http}://{host}:{port}{endpoint}/{name}"
            headers = {
                    'Accept': 'application/json',
                    #'X-HTTP-Method-Override': 'GET'
                    }
            #data = payload
            data = json.dumps(payload)
            if debug:
                print(f'egmonitor_host_create: request_url: {request_url}')
                print(f'egmonitor_host_create: headers    : {headers}')
                print(f'egmonitor_host_create: auth       : {user}:{pasw}')
                print(f'egmonitor_host_create: verify     : {cert}')
                print(f'egmonitor_host_create: data       : {data} {type(data)}')
            # Host Creation requires a PUT call to REST API
            r = requests.put(
                    request_url,
                    headers= headers,
                    auth   = (user, pasw),
                    data   = data,
                    verify = verify
                    )

            if debug:
                print(f"egmonitor_host_create: After request execution:")
                print(f"egmonitor_host_create: Request URL = {str(r.url)}")
                print(f"egmonitor_host_create: Status code = {str(r.status_code)}")
                print(f"egmonitor_host_create: Text        = {str(r.text)}")
            if r is not None:
                if debug:
                    print(f'r={r}')
                    print(f'r.status_code = {r.status_code}')
                    print(f'r.reason      = {r.reason}')
                    print(f'r.text        = {r.text} {type(r.text)}')
                    print(f'r.json        = {r.text} {type(r.text)}')
                code   = r.status_code
                status = r.json()
            # return egmonitor response here as a JSON array
        except Exception as e:
            code   = 500.0
            status = f"EG Butler Exception: {str(e)}. EG Monitor Object was not created."
            #raise e
    else:
        code   = 500.0
        status = "EG Butler received an Invalid request. EG Monitor Object was not created."

    response={ 'results': [ { 'code':code, 'status':status } ] }
    return json.dumps(response)

"""
curl -k  -u butler:butler 
    -H 'Accept: application/json' 
    -X DELETE https://monitor:5665/v1/objects/hosts/TEST-API?cascade=1&pretty=1
{"results":
    [{  "code":200.0,"errors":[],
        "name":"TEST-API",
        "status":"Object was deleted.",
        "type":"Host"
        }]}

"""
def egmonitor_host_delete(name,app,data,debug=False):
    """ Create a new API Host in Icinga2 
    
    Agument | description
    ------- | -----------
    app     | Application object
    data    | Request data received
            | address: Host IP Address (mandatory)
            | os     : OS specification (optional) (Linux,Windows,AIX,...)
    """
    # process data here
    # endpoint has a default hard coded and depends of Icinga2 API version
    # can be overrided in configuration file

    try:
        http     = app.egconfig.get('eg-monitor','http',fallback='https')
        host     = app.egconfig.get('eg-monitor','host',fallback=None)
        port     = app.egconfig.get('eg-monitor','port',fallback=None)
        user     = app.egconfig.get('eg-monitor','username',fallback=None)
        pasw     = app.egconfig.get('eg-monitor','password',fallback=None)
        cert     = app.egconfig.get('eg-monitor','certificate',fallback='pki/butler.crt')
        pkik     = app.egconfig.get('eg-monitor','key',fallback='pki/butler.key')
        verify   = app.egconfig.get('eg-monitor','verify',fallback=False)
        endpoint = app.egconfig.get('eg-monitor','host_create',fallback=f'/v1/objects/hosts')
        # Icinga2 API Payload requirements
    except Exception as e:
        if debug:
            print(f"egmonitor_host_delete: eg-monitor   : {app.egconfig.get('eg-monitor','host')}:{app.egconfig.get('eg-monitor','port')}")
            print(f"egmonitor_host_delete: endpoint     : {endpoint}")
            print(f"egmonitor_host_delete: data         : {data}")
            print(f'egmonitor_host_delete: Request is bad formed: EXCEPTION: {str(e)}')
    try:
        if debug:
            print(f'egmonitor_host_delete: call')
            print(f'    egmonitor: {host}:{port}') 
            print(f'    user/pass: {user}:{pasw}') 
            print(f'    endpoint : {endpoint}') 
        # call egmonitor
        # response = call eg-monitor and wait for response

        # Replace 'localhost' with your FQDN and certificate CN
        # for TLS verification
        request_url = f"{http}://{host}:{port}{endpoint}/{name}?cascade=1&pretty=1"
        headers = {
                'Accept': 'application/json',
                #'X-HTTP-Method-Override': 'GET'
                }
        if debug:
            print(f"egmonitor_host_delete: Previous request execution:")
            print(f'egmonitor_host_delete: request_url: {request_url}')
            print(f'egmonitor_host_delete: headers    : {headers}')
            print(f'egmonitor_host_delete: auth       : {user}:{pasw}')
            print(f'egmonitor_host_delete: verify     : {verify}')
            print(f'egmonitor_host_delete: cert       : {cert}')
            print(f'egmonitor_host_delete: key        : {pkik}')
        # Host deletion requires a DELETE call to REST API
        # including cascade
        r = requests.delete(
                request_url,
                headers= headers,
                auth   = (user, pasw),
                verify = verify
                )

        if debug:
            print(f"egmonitor_host_delete: After request execution:")
            print(f"egmonitor_host_delete: Request URL = {str(r.url)}")
            print(f"egmonitor_host_delete: Status code = {str(r.status_code)}")
            print(f"egmonitor_host_delete: Text        = {str(r.text)}")
        if r is not None:
            if debug:
                print(f'r={r}')
                print(f'r.status_code = {r.status_code}')
                print(f'r.reason      = {r.reason}')
                print(f'r.text        = {r.text} {type(r.text)}')
                print(f'r.json        = {r.text} {type(r.text)}')
            code   = r.status_code
            status = r.json()
        # return egmonitor response here as a JSON array
    except Exception as e:
        code   = 500.0
        status = f"EG Butler Exception: {str(e)}. EG Monitor Object was not deleted."
        #raise e


    response={ 'results': [ { 'code':code, 'status':status } ] }
    return json.dumps(response)

# ----------------------------------------------------------------------
# Nutanix Prism Central Endpoint Functions
# ----------------------------------------------------------------------

def nutanix_heartbeat(app,data=None,debug=False):
    """ Creates a new VM via Nutanix Prism Central
    
    Argument | Description
    -------- | -----------
    app      | Application object
    data     | Request data received
             | xxx    : VM required specifications are required here
             | xxx    : .........
    """
    # process data here
    # contact nutanix
    caller = f'{inspect.stack()[1][3]}:{this_function()}:'
    log    = get_log(app)
    log(f'{caller} will call relay_request with:')
    log(f'{caller} app      = {app}')
    log(f'{caller} data     = {data}')
    log(f'{caller} debug    = {debug}')
    log(f'{caller} service  = nutanix')
    log(f'{caller} endpoint = /api/v3')
    log(f'{caller} method   = GET')
    response = relay_request(
        app,
        data,
        debug=debug,
        service='nutanix',
        endpoint='/api/v3',
        method='GET'
        )
    log(f'{caller} response = {response} type:{type(response)}')
    if response is not None:
        log(f'{caller} response.status_code   = {response.status_code}')
        log(f'{caller} response.json()   = {response.json()}')
    try:
        response={'code':response.status_code,'status':response.json()}
    except Exception as e:
        log(f'{caller} response: {response}')
        log(f'{caller} Exception: {str(e)}')
        response=None
    return json.dumps(response)

def nutanix_vmlist(app,data=None,debug=False):
    """ Creates a new VM via Nutanix Prism Central
    
    Argument | Description
    -------- | -----------
    app      | Application object
    data     | Request data received
             | xxx    : VM required specifications are required here
             | xxx    : .........
    """
    # process data here
    arguments=data
    # contact nutanix
    r = relay_request(
        app,
        data,
        debug=False,
        service='nutanix',
        endpoint='/api/v3/vmlist',
        method='GET',
        )
    try:
        response={'code':r.status_code,'status':r.json()}
    except:
        response=None
    return json.dumps(response)

def nutanix_vm(app,data=None,debug=False):
    """ Creates a new VM via Nutanix Prism Central
    
    Argument | Description
    -------- | -----------
    app      | Application object
    data     | Request data received
             | xxx    : VM required specifications are required here
             | xxx    : .........
    """
    # process data here
    arguments=data
    # contact nutanix
    r = relay_request(
        app,
        data,
        debug=debug,
        service='nutanix',
        endpoint='/api/v3/vm',
        method='GET',
        )

    try:
        response={'code':r.status_code,'status':r.json()}
    except:
        response=None
    return json.dumps(response)

def nutanix_vm_create(app,data):
    """ Creates a new VM via Nutanix Prism Central
    
    Argument | Description
    -------- | -----------
    app      | Application object
    data     | Request data received
             | xxx    : VM required specifications are required here
             | xxx    : .........
    """
    # process data here
    arguments=data
    # contact nutanix
    response={'data':data,'config':{}}
    for section in app.egconfig.sections():
        response['config'].update({section:{}})
        for option in app.egconfig.options(section):
            response['config'][section].update({option:app.egconfig.get(section,option)})
    # return egmonitor response here as a JSON array
    return json.dumps(response)

def nutanix_vm_delete(app,data):
    # process data here
    arguments=data
    # contact nutanix
    response={'data':data,'config':{}}
    for section in app.egconfig.sections():
        response['config'].update({section:{}})
        for option in app.egconfig.options(section):
            response['config'][section].update({option:app.egconfig.get(section,option)})
    # return egmonitor response here as a JSON array
    return json.dumps(response)

# ----------------------------------------------------------------------
# EG Collector Endpoint Functions
# ----------------------------------------------------------------------

def egcollector_heartbeat(app,data=None,debug=False):
    """ Creates a new VM via Nutanix Prism Central
    
    Argument | Description
    -------- | -----------
    app      | Application object
    data     | Request data received
             | xxx    : VM required specifications are required here
             | xxx    : .........
    """
    # process data here
    # contact nutanix
    caller   = f'{inspect.stack()[1][3]}:{this_function()}:'
    log      = get_log(app)
    service  = 'eg-collector'
    endpoint = '/'
    method   = 'GET'
    if debug:
        log(f'{caller} will call relay_request with:')
        log(f'{caller} app      = {app}')
        log(f'{caller} data     = {data}')
        log(f'{caller} debug    = {debug}')
        log(f'{caller} service  = {service}')
        log(f'{caller} endpoint = {endpoint}')
        log(f'{caller} method   = {method}')
    response = relay_request(
        app,
        data,
        debug=debug,
        service=service,
        endpoint=endpoint,
        method=method
        )
    log(f'{caller} response             = {response} type:{type(response)}')
    if response is not None:
        # Do whatevr is required with response
        try:
            log(f'{caller} response.status_code = {response.status_code}')
            log(f'{caller} response.reason      = {response.reason}')
        except Exception as e:
            log(f'{caller} response: {response}')
            log(f'{caller} Exception: {str(e)}')
    return json.dumps({'code':response.status_code,'status':response.reason})

def collector_get_cc(app,data=None,debug=False):
    """ Get CC(s) as  per filter """

def collector_ci(app,data=None,debug=False):
    """ Get CI(s) as  per filter """
    # process data here
    arguments=data
    # contact collector
    response={'data':data,'config':{'status':f"Unimplemented function '{this_function()}'. Callback data returned."}}
    #for section in app.egconfig.sections():
    #    response['config'].update({section:{}})
    #    for option in app.egconfig.options(section):
    #        response['config'][section].update({option:app.egconfig.get(section,option)})
    # return egmonitor response here as a JSON array
    return json.dumps(response)

def collector_ci_update(app,data=None,debug=False):
    """ Update CC Code for specific CI """
    # process data here
    arguments=data
    # contact nutanix
    response={'data':data,'config':{}}
    for section in app.egconfig.sections():
        response['config'].update({section:{}})
        for option in app.egconfig.options(section):
            response['config'][section].update({option:app.egconfig.get(section,option)})
    # return egmonitor response here as a JSON array
    return json.dumps(response)

"""
@app.route("/api/v3/vmlist")
def api_v3():
    Data={
        'title':'VM list',
        'endpoint':'/api/v3/vmlist',
        'payload':'Payload is here'
    }
    return json.dumps(Data)
# ----------------------------------------------------------------------
@app.route("/api/v3/trx_001")
def api_v3_trx_001():
    Data={
        'title':'V3 TRX 001',
        'endpoint':'/api/v3/vmlist',
        'payload':'Payload is here'
    }
    return trx_001(Data)
# ----------------------------------------------------------------------
"""
"""
@app.route('/query-example', methods=['GET', 'POST'])
def query_example():
    debug=False
    if request.method == 'GET':
        data=json.dumps(dict(request.args))
        if 'DEBUG' in dict(request.args).keys():
            debug=True
    elif request.method == 'POST':
        data=request.json
        #print(f"data={data} type={type(data)}")
        if 'DEBUG' in data.keys():
            debug=True
    else:
        return "ERROR: Invalid request method"
    # Will allways return an string
    # If debug is requested, HTML debug info will be returned   
    if debug:
        return f'{get_request(app,request,data)}{data}'
    else:
        return json.dumps(data)
"""
