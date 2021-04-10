# ======================================================================
# Main Views Header
# source file name: EG-Butler-Tools/code/src/views_butler_api.py
# Static Header File. 
# GLVH 2021-03-15
# ----------------------------------------------------------------------
# the routes file that will manage the routing of the web app is imported
#from app import routes
@main.route("/")
def home():
    return "<h1>EG Suite - EG Butler API Server Application</h1>"

# GV 2021-03-15 add standard heartbeat view
@main.route("/api/heartbeat_html") 
def api_heartbeat_html(): # GV 20150315 fix
    return f"<h2>EG Butler API Service is UP</h2>{request.remote_user}@{request.remote_addr}"

@main.route('/api/heartbeat', methods=['GET'])
def api_heartbeat():
    logger.debug(f'{this()}: IN')
    response = "{}"
    try:
        kind       = 'heartbeat'
        entities   = []
        name       = current_app.config['NAME']
        authorized = api_check_authorization(request,current_app,logger=logger)
        logger.debug(f'{this()}: kind={kind} entities={entities} name={name} authorized={authorized}')
        if authorized:
            code,message   = API_OK,'Authorized request'
        else:
            code,message   = API_ERROR,'Unauthorized request'
        logger.debug(f'{this()}: authorized={authorized} code={code} message={message}')
        response = get_api_response(
                    code     = code,
                    message  = message,
                    kind     = kind,
                    entities = entities,
                    name     = name
                    )
    except Exception as e:
        logger.error(f'{this()}: {str(e)}')
        
    logger.debug(f'{this()}: OUT: response={response}')
    return str(response)

# ----------------------------------------------------------------------
# API EG Butler Routes
# ----------------------------------------------------------------------
@main.route("/api/eg-butler/request", methods=['GET', 'POST'])
def api_egbutler_request():
    # This convention allows to get request data no matter request 
    # method, and also allows to debug transaction details
    caller = f'{inspect.stack()[1][3]}:{this_function()}:'
    log    = get_log(app)
    if DEBUG: log(f'{caller} IN')
    data,debug,debug_payload = get_request_data(request,app)
    if DEBUG: dump_request(app,request)
    # Will allways return an string
    # If debug is requested, HTML debug info will be returned
    # as HTML payload prefix
    output=egbutler_request(app,data,debug)
    output_debug=''
    if debug: 
        output_debug=f"<h3>PPRINTED</h3><table><tr><td>{pformat(output)}</td></tr></table>"
        output_debug=output_debug.replace('\n','<br>')
        output_debug=output_debug.replace('{','<table>')
        output_debug=output_debug.replace('}','</table>')
    result = f'{debug_payload}{output}{output_debug}'
    if DEBUG: log(f'{caller} {result}') 
    return result

# ----------------------------------------------------------------------
# EG Monitor Endpoints
# ----------------------------------------------------------------------
@main.route("/api/eg-monitor/host", methods=['GET', 'POST'])
def api_egmonitor_host():
    # This convention allows to get request data no matter request 
    # method, and also allows to debug transaction details
    caller = f'{inspect.stack()[1][3]}:{this_function()}:'
    log    = get_log(app)
    if DEBUG: log(f'{caller} IN')
    data,debug,debug_payload = get_request_data(request,app)
    if DEBUG: dump_request(app,request)
    # Will allways return an string
    # If debug is requested, HTML debug info will be returned
    # as HTML payload prefix
    output=egmonitor_host(app,data,debug)
    output_debug=''
    if debug: 
        output_debug=f"<h3>PPRINTED</h3><table><tr><td>{pformat(output)}</td></tr></table>"
        output_debug=output_debug.replace('\n','<br>')
        output_debug=output_debug.replace('{','<table>')
        output_debug=output_debug.replace('}','</table>')
    result = f'{debug_payload}{output}{output_debug}'
    if DEBUG: log(f'{caller} {result}') 
    return result

@main.route("/api/eg-monitor/host-create/<name>", methods=['GET', 'POST'])
def api_egmonitor_host_create(name):
    # This convention allows to get request data no matter request 
    # method, and also allows to debug transaction details
    caller = f'{inspect.stack()[1][3]}:{this_function()}:'
    log    = get_log(app)
    if DEBUG: log(f'{caller} IN')
    data,debug,debug_payload = get_request_data(request,app)
    if DEBUG: dump_request(app,request)
    # Will allways return an string
    # If debug is requested, HTML debug info will be returned
    # as HTML payload prefix
    result = f'{debug_payload}{egmonitor_host_create(name,app,data,debug)}'
    if DEBUG: log(f'{caller} {result}') 
    return result
# ----------------------------------------------------------------------
@main.route("/api/eg-monitor/host-delete/<name>", methods=['GET', 'POST'])
def api_egmonitor_host_delete(name):
    # This convention allows to get request data no matter request 
    # method, and also allows to debug transaction details
    caller = f'{inspect.stack()[1][3]}:{this_function()}:'
    log    = get_log(app)
    if DEBUG: log(f'{caller} IN')
    data,debug,debug_payload = get_request_data(request,app)
    if DEBUG: dump_request(app,request)
    # Will allways return an string
    # If debug is requested, HTML debug info will be returned
    # as HTML payload prefix
    result = f'{debug_payload}{egmonitor_host_delete(name,app,data,debug)}'
    if DEBUG: log(f'{caller} {result}') 
    return result

# ----------------------------------------------------------------------
# EG Collector Endpoints
# ----------------------------------------------------------------------
@main.route("/api/eg-collector/heartbeat", methods=['GET', 'POST'])
def api_egcollector_heartbeat():
    # This convention allows to get request data no matter request 
    # method, and also allows to debug transaction details
    caller = f'{inspect.stack()[1][3]}:{this_function()}:'
    log    = get_log(app)

    if DEBUG: log(f'{caller} IN DEBUG={DEBUG}')
    data,debug,debug_payload = get_request_data(request,app)
    if DEBUG: log(f'{caller} IN debug={debug}')
    if DEBUG: dump_request(app,request)
    # Will allways return an string
    # If debug is requested, HTML debug info will be returned
    # as HTML payload prefix
    result = f'{debug_payload}{egcollector_heartbeat(app,data,debug)}'
    if DEBUG: log(f'{caller} returns: {result}') 
    return result

@main.route("/api/eg-collector/ci", methods=['GET', 'POST'])
def api_collector_ci():
    # This convention allows to get request data no matter request 
    # method, and also allows to debug transaction details
    caller = f'{inspect.stack()[1][3]}:{this_function()}:'
    log    = get_log(app)
    if DEBUG: log(f'{caller} IN')
    data,debug,debug_payload = get_request_data(request,app)
    if DEBUG: dump_request(app,request)
    # Will allways return an string
    # If debug is requested, HTML debug info will be returned
    # as HTML payload prefix
    output=collector_ci(app,data,debug)
    output_debug=''
    if debug: 
        output_debug=f"<h3>PPRINTED</h3><table><tr><td>{pformat(output)}</td></tr></table>"
        output_debug=output_debug.replace('\n','<br>')
        output_debug=output_debug.replace('{','<table>')
        output_debug=output_debug.replace('}','</table>')
    result = f'{debug_payload}{output}{output_debug}'
    if DEBUG: log(f'{this_function()}: returns: {result}') 
    return result

@main.route("/api/collector/update_Cost_Centers", methods=['GET'])
def api_collector_update_Cost_Centers():
    # This convention allows to get request data no matter request 
    # method, and also allows to debug transaction details
    #caller = f'{inspect.stack()[1][3]}:{this_function()}:'
    #log    = get_log(app)
    if DEBUG: log(f'{caller()} IN')
    result   = None
    host     = current_app.config.get('COLLECTOR_HOST')
    port     = current_app.config.get('COLLECTOR_PORT')
    username = current_app.config.get('COLLECTOR_USERNAME')
    password = current_app.config.get('COLLECTOR_PASSWORD')
    protocol = current_app.config.get('COLLECTOR_PROTOCOL')
    endpoint = 'api/get/Cost_Centers'
    #data={}
    arguments=''
        
    headers  = {'Content-Type': 'application/json'}
    url      = f'{protocol}://{host}:{port}/{endpoint}{arguments}'

    print(f'{this()}: user ={username}:{password}')
    print(f'{this()}: url ={url}')

    response = api_request('GET',
                    url,
                    #data=data,
                    headers=headers,
                    username=username,
                    password=password
                    )
    if response is not None:
        data = response.json()
        if response.status_code == 200:
            # Actual process of result here
            if data['status']['code'] == 0:
                rows=[]
                for entity in data['entities']:
                    row=Cost_Centers()
                    for key in entity:
                        setattr(row,key,entity[key])
                    rows.append(row)
                print(f'len(rows)={len(rows)}')
                for row in rows:
                    db.session.merge(row)
                db.session.commit()
                    
                # Prepare API Response
                result = get_api_response(
                    # status arguments
                    state=data['status']['state'],
                    code=data['status']['code'],
                    message=data['status']['message'],
                    execution_context=None,
                    # metadata
                    total_matches=data['metadata']['total_matches'],
                    kind=data['metadata']['kind'],
                    length=data['metadata']['length'],
                    offset=data['metadata']['offset'],
                    )
            else:
                result = get_api_response(
                    # status arguments
                    state=data['status']['state'],
                    code=response[''],
                    message=data['status']['message'],
                    execution_context=None,
            )
        else:
            result = get_api_response(
                # status arguments
                code=response.status_code,
                message=response.reason
                )
    else:
        result = get_api_response(
            # status arguments
            code=1,
            message=f'NO RESPONSE'
            )
    
    return result

# ----------------------------------------------------------------------
# Nutanix Prism Central v3 Endpoints
# ----------------------------------------------------------------------
@main.route("/api/nutanix/heartbeat", methods=['GET', 'POST'])
def api_nutanix_heartbeat():
    # This convention allows to get request data no matter request 
    # method, and also allows to debug transaction details
    caller = f'{inspect.stack()[1][3]}:{this_function()}:'
    log    = get_log(app)

    if DEBUG: log(f'{caller} IN DEBUG={DEBUG}')
    data,debug,debug_payload = get_request_data(request,app)
    if DEBUG: log(f'{caller} IN debug={debug}')
    if DEBUG: dump_request(app,request)
    # Will allways return an string
    # If debug is requested, HTML debug info will be returned
    # as HTML payload prefix
    result = f'{debug_payload}{nutanix_heartbeat(app,data,debug)}'
    if DEBUG: log(f'{caller} returns: {result}') 
    return result

@main.route("/api/nutanix/vmlist", methods=['GET', 'POST'])
def api_nutanix_vmlist():
    # This convention allows to get request data no matter request 
    # method, and also allows to debug transaction details
    caller = f'{inspect.stack()[1][3]}:{this_function()}:'
    log    = get_log(app)
    if DEBUG: log(f'{caller} IN')
    data,debug,debug_payload = get_request_data(request,app)
    if DEBUG: dump_request(app,request)
    # Will allways return an string
    # If debug is requested, HTML debug info will be returned
    # as HTML payload prefix
    result = f'{debug_payload}{nutanix_vmlist(app,data,debug)}'
    if DEBUG: log(f'{caller} returns: {result}') 
    return result

@main.route("/api/nutanix/vm", methods=['GET', 'POST'])
def api_nutanix_vm():
    # This convention allows to get request data no matter request 
    # method, and also allows to debug transaction details
    caller = f'{inspect.stack()[1][3]}:{this_function()}:'
    log    = get_log(app)
    if DEBUG: log(f'{caller} IN')
    data,debug,debug_payload = get_request_data(request,app)
    if DEBUG: dump_request(app,request)
    # Will allways return an string
    # If debug is requested, HTML debug info will be returned
    # as HTML payload prefix
    result = f'{debug_payload}{nutanix_vm(app,data,debug)}'
    if DEBUG: log(f'{caller} returns: {result}') 
    return result

@main.route("/api/nutanix/pcv3/vm-create", methods=['GET', 'POST'])
def api_nutanix_pcv3_vm_create():
    # This convention allows to get request data no matter request 
    # method, and also allows to debug transaction
    data,debug,payload = get_request_data(request,app)
    # Will allways return an string
    # If debug is requested, HTML debug info will be returned
    # as HTML payload prefix
    result = f'{payload}{nutanix_pcv3_vm_create(app,data)}'
    if DEBUG: log(f'{caller} returns: {result}') 
    return result
# ----------------------------------------------------------------------
@main.route("/api/nutanix/pcv3/vm-delete", methods=['GET', 'POST'])
def api_nutanix_pcv3_vm_delete():
    # This convention allows to get request data no matter request 
    # method, and also allows to debug transaction
    data,debug,payload = get_request_data(request,app)
    # Will allways return an string
    # If debug is requested, HTML debug info will be returned
    # as HTML payload prefix
    result = f'{payload}{nutanix_pcv3_vm_create(app,data)}'
    if DEBUG: log(f'{caller} returns: {result}') 
    return result
    
# ----------------------------------------------------------------------        
