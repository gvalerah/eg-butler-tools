# ======================================================================
# Main Views Header
# source file name: views_py_header.py
# Static Header File. 
# GLVH 2020-10-11
# ----------------------------------------------------------------------
from time           import strftime
from datetime       import datetime     
from pprint         import pformat                    
from pprint         import pprint                    
from sqlalchemy     import exc
from sqlalchemy     import func
from flask          import render_template
from flask          import session
from flask          import redirect
from flask          import url_for
from flask          import current_app
from flask          import flash
from flask          import request
from flask          import Markup
from flask_login    import login_required
from flask_login    import current_user
#rom ..email        import send_email

from .              import main

from ..             import db
#from ..             import mail
from ..             import logger

from ..decorators   import admin_required, permission_required

from emtec                       import *
from emtec.common.functions      import *
#from emtec.butler.db.flask_models       import User
from emtec.butler.db.flask_models       import User
from emtec.butler.db.flask_models       import Permission
# 20200224 GV from emtec.butler.db.orm_model          import Interface
from emtec.butler.db.flask_models       import *
from emtec.butler.db.orm_model          import *
from emtec.butler.constants             import *

from markdown import markdown
from markdown import markdownFromFile

# the routes file that will manage the routing of the web app is imported
#from app import routes
@main.route("/")
def home():
    return "<h1>EG Suite - EG Butler API Server Application</h1>"

@main.route("/api/heartbeat_html")
def api_heartbeat_html():
    return f"<h2>EG Butler API Service is UP</h2>{request.remote_user}@{request.remote_addr}"

@main.route('/api/heartbeat', methods=['GET'])
def api_heartbeat():
    logger.debug(f'{this()}: IN')
    kind='heartbeat'
    entities=[]
    name=current_app.config['NAME']
    authorized = api_check_authorization(request,current_app)
    if authorized:
        code    = API_OK
        message = 'Authorized request'
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(
            code=code,
            message=message,
            kind=kind,
            entities=entities,
            name=name)


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

"""
     'entities': [{'CC_Code': 'DEFAULT-CC-CODE',
               'CC_Description': 'DEFAULT_CC_DESCRIPTION',
               'CC_Id': 1,
               'CC_Parent_Code': 'DEFAULT-CC-CODE',
               'CC_Reference': None,
               'CC_Reg_Exp': None,
               'Cur_Code': 'USD'},
"""



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
# view_categories.py_gen_views_api.html.auto

# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2020-11-23 19:59:58.399244
# ======================================================================
# gen_views_api.html:AG 2020-11-23 19:59:58.399259
# table_name: Categories
# class_name: categories
# is shardened: False
# Table 'Categories' keys = category_name
# Errors: None
# PK field found 'category_name' db.String(45)
# Categories id field is 'Categories.category_name' of type ''

@main.route('/api/get/Categories'     , methods=['GET'])
@main.route('/api/get/Categories/<id>', methods=['GET'])
def api_get_Categories(id=None):
    code       = API_OK
    message    = 'OK'
    rows       = None
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            id_counter = 0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values=[id]
            # Codigo para un solo campo de id
            # chequear si marcado explicitamente
            query = db.session.query(Categories)
            if id is not None:
                query = query.filter(Categories.category_name == id_values[id_counter])
                rows = query.one_or_none()
            else:
                if request.args is not None and len(request.args):
                    if 'category_name' in request.args:
                        query = query.filter(Categories.category_name == request.args.get('category_name'))
                    if 'category_description' in request.args:
                        query = query.filter(Categories.category_description == request.args.get('category_description'))
                rows = query.all()
            if rows is not None:
                if type(rows) == list:
                    for i in range(len(rows)):
                        rows[i] = json.loads(rows[i].get_json())
                else:
                    rows = [json.loads(rows.get_json())]
            else:
                rows = []
            if len(rows) == 0:
                code = API_NO_DATA
                state = get_api_state(API_NO_DATA)
                
                if id is None:
                    message = f"No 'Categories' records found"
                else:
                    message = f"No 'Categories.category_name' = {id} record found"
                
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Categories',entities=rows,name=current_app.config['NAME'])

@main.route('/api/post/Categories', methods=['POST'])
def api_post_Categories():
    code    = API_OK
    message = 'OK'
    row     = None
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            row = Categories()
            # Populates row from json, if ID=int:autoincrement then None
            row.category_name = request.json.get('category_name',None)
            row.category_description = request.json.get('category_description',None)
            # ----------------------------------------------------------
            db.session.add(row)
            db.session.flush()
            db.session.commit()
            db.session.refresh(row)
            db.session.close()
            message = f"Created 'Categories' category_name = {row.category_name}"
            row     = json.loads(row.get_json())
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
            row     = None
    else:
        code    = API_ERROR
        message = 'Unauthorized request'            
    return get_api_response(code=code,message=message,kind='Categories',entities=[row],name=current_app.config['NAME'])

@main.route('/api/put/Categories/<id>', methods=['PUT'])
def api_put_Categories(id):
    code    = API_OK
    message = 'OK'
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            id_counter=0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values = [id]
            row   = Categories()
            query = db.session.query(Categories)
            
            # First loop mandatory for row population ----------------------
            query = query.filter(Categories.category_name == id_values[id_counter])
            id_counter += 1
            # --------------------------------------------------------------
            row = query.one_or_none()
            # If row exists then continue:
            if row is not None:
                # Second loop seek for updated fields ----------------------
                if 'category_description' in request.json.keys():
                    row.category_description = request.json.get('category_description')
                # ----------------------------------------------------------
                db.session.merge(row)
                db.session.flush()
                db.session.commit()
                db.session.refresh(row)
                db.session.close()
                message = f"Modified 'Categories' category_name = {id}"
                row     = json.loads(row.get_json())
            else:
                code    = API_NOT_FOUND
                message = f"Not found Categories with category_name = {id}"
                row     = None
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Categories',entities=[row],name=current_app.config['NAME'])

@main.route('/api/patch/Categories/<id>', methods=['PATCH'])
def api_patch_Categories(id):
    code    = API_OK
    message = 'OK'
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            id_counter=0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values = [id]
            row   = Categories()
            query = db.session.query(Categories)
            
            # First loop mandatory for row population ----------------------
            query = query.filter(Categories.category_name == id_values[id_counter])
            id_counter += 1
            # --------------------------------------------------------------
            row = query.one_or_none()
            # If row exists then continue:
            if row is not None:
                # Second loop seek for updated fields ----------------------
                if 'category_description' in request.json.keys():
                    row.category_description = request.json.get('category_description')
                # ----------------------------------------------------------
                db.session.merge(row)
                db.session.flush()
                db.session.commit()
                db.session.refresh(row)
                db.session.close()
                message = f"Modified 'Categories' category_name = {id}"
                row     = json.loads(row.get_json())
            else:
                code    = API_NOT_FOUND
                message = f"Not found Categories with category_name = {id}"
                row     = None
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Categories',entities=[row],name=current_app.config['NAME'])

@main.route('/api/delete/Categories/<id>', methods=['DELETE'])
def api_delete_Categories(id):
    code    = API_OK
    message = 'OK'
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            id_counter=0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values = [id]
            row   = Categories()
            query = db.session.query(Categories)
            
            # First loop mandatory for row population ----------------------
            # detected primary key field: c.field
            query       = query.filter(Categories.category_name == id_values[id_counter])
            id_counter +=1
            # --------------------------------------------------------------
            row = query.one_or_none()

            if row is not None:
                db.session.delete(row)
                db.session.flush()
                db.session.commit()
                db.session.close()
                message = f"Deleted 'Categories' category_name = {id}"
                row     = json.loads(row.get_json())
            else:
                code    = API_NOT_FOUND
                message = f"Not found 'Categories' with category_name = {id}"
                row     = None        
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Categories',entities=[],name=current_app.config['NAME'])

# ======================================================================# view_clusters.py_gen_views_api.html.auto

# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2020-11-23 19:59:58.575594
# ======================================================================
# gen_views_api.html:AG 2020-11-23 19:59:58.575617
# table_name: Clusters
# class_name: clusters
# is shardened: False
# Table 'Clusters' keys = cluster_uuid
# Errors: None
# PK field found 'cluster_uuid' db.String(45)
# Clusters id field is 'Clusters.cluster_uuid' of type ''

@main.route('/api/get/Clusters'     , methods=['GET'])
@main.route('/api/get/Clusters/<id>', methods=['GET'])
def api_get_Clusters(id=None):
    code       = API_OK
    message    = 'OK'
    rows       = None
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            id_counter = 0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values=[id]
            # Codigo para un solo campo de id
            # chequear si marcado explicitamente
            query = db.session.query(Clusters)
            if id is not None:
                query = query.filter(Clusters.cluster_uuid == id_values[id_counter])
                rows = query.one_or_none()
            else:
                if request.args is not None and len(request.args):
                    if 'cluster_uuid' in request.args:
                        query = query.filter(Clusters.cluster_uuid == request.args.get('cluster_uuid'))
                    if 'cluster_name' in request.args:
                        query = query.filter(Clusters.cluster_name == request.args.get('cluster_name'))
                    if 'cluster_username' in request.args:
                        query = query.filter(Clusters.cluster_username == request.args.get('cluster_username'))
                    if 'cluster_password' in request.args:
                        query = query.filter(Clusters.cluster_password == request.args.get('cluster_password'))
                    if 'cluster_ip' in request.args:
                        query = query.filter(Clusters.cluster_ip == request.args.get('cluster_ip'))
                rows = query.all()
            if rows is not None:
                if type(rows) == list:
                    for i in range(len(rows)):
                        rows[i] = json.loads(rows[i].get_json())
                else:
                    rows = [json.loads(rows.get_json())]
            else:
                rows = []
            if len(rows) == 0:
                code = API_NO_DATA
                state = get_api_state(API_NO_DATA)
                
                if id is None:
                    message = f"No 'Clusters' records found"
                else:
                    message = f"No 'Clusters.cluster_uuid' = {id} record found"
                
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Clusters',entities=rows,name=current_app.config['NAME'])

@main.route('/api/post/Clusters', methods=['POST'])
def api_post_Clusters():
    code    = API_OK
    message = 'OK'
    row     = None
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            row = Clusters()
            # Populates row from json, if ID=int:autoincrement then None
            row.cluster_uuid = request.json.get('cluster_uuid',None)
            row.cluster_name = request.json.get('cluster_name',None)
            row.cluster_username = request.json.get('cluster_username',None)
            row.cluster_password = request.json.get('cluster_password',None)
            row.cluster_ip = request.json.get('cluster_ip',None)
            # ----------------------------------------------------------
            db.session.add(row)
            db.session.flush()
            db.session.commit()
            db.session.refresh(row)
            db.session.close()
            message = f"Created 'Clusters' cluster_uuid = {row.cluster_uuid}"
            row     = json.loads(row.get_json())
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
            row     = None
    else:
        code    = API_ERROR
        message = 'Unauthorized request'            
    return get_api_response(code=code,message=message,kind='Clusters',entities=[row],name=current_app.config['NAME'])

@main.route('/api/put/Clusters/<id>', methods=['PUT'])
def api_put_Clusters(id):
    code    = API_OK
    message = 'OK'
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            id_counter=0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values = [id]
            row   = Clusters()
            query = db.session.query(Clusters)
            
            # First loop mandatory for row population ----------------------
            query = query.filter(Clusters.cluster_uuid == id_values[id_counter])
            id_counter += 1
            # --------------------------------------------------------------
            row = query.one_or_none()
            # If row exists then continue:
            if row is not None:
                # Second loop seek for updated fields ----------------------
                if 'cluster_name' in request.json.keys():
                    row.cluster_name = request.json.get('cluster_name')
                if 'cluster_username' in request.json.keys():
                    row.cluster_username = request.json.get('cluster_username')
                if 'cluster_password' in request.json.keys():
                    row.cluster_password = request.json.get('cluster_password')
                if 'cluster_ip' in request.json.keys():
                    row.cluster_ip = request.json.get('cluster_ip')
                # ----------------------------------------------------------
                db.session.merge(row)
                db.session.flush()
                db.session.commit()
                db.session.refresh(row)
                db.session.close()
                message = f"Modified 'Clusters' cluster_uuid = {id}"
                row     = json.loads(row.get_json())
            else:
                code    = API_NOT_FOUND
                message = f"Not found Clusters with cluster_uuid = {id}"
                row     = None
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Clusters',entities=[row],name=current_app.config['NAME'])

@main.route('/api/patch/Clusters/<id>', methods=['PATCH'])
def api_patch_Clusters(id):
    code    = API_OK
    message = 'OK'
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            id_counter=0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values = [id]
            row   = Clusters()
            query = db.session.query(Clusters)
            
            # First loop mandatory for row population ----------------------
            query = query.filter(Clusters.cluster_uuid == id_values[id_counter])
            id_counter += 1
            # --------------------------------------------------------------
            row = query.one_or_none()
            # If row exists then continue:
            if row is not None:
                # Second loop seek for updated fields ----------------------
                if 'cluster_name' in request.json.keys():
                    row.cluster_name = request.json.get('cluster_name')
                if 'cluster_username' in request.json.keys():
                    row.cluster_username = request.json.get('cluster_username')
                if 'cluster_password' in request.json.keys():
                    row.cluster_password = request.json.get('cluster_password')
                if 'cluster_ip' in request.json.keys():
                    row.cluster_ip = request.json.get('cluster_ip')
                # ----------------------------------------------------------
                db.session.merge(row)
                db.session.flush()
                db.session.commit()
                db.session.refresh(row)
                db.session.close()
                message = f"Modified 'Clusters' cluster_uuid = {id}"
                row     = json.loads(row.get_json())
            else:
                code    = API_NOT_FOUND
                message = f"Not found Clusters with cluster_uuid = {id}"
                row     = None
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Clusters',entities=[row],name=current_app.config['NAME'])

@main.route('/api/delete/Clusters/<id>', methods=['DELETE'])
def api_delete_Clusters(id):
    code    = API_OK
    message = 'OK'
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            id_counter=0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values = [id]
            row   = Clusters()
            query = db.session.query(Clusters)
            
            # First loop mandatory for row population ----------------------
            # detected primary key field: c.field
            query       = query.filter(Clusters.cluster_uuid == id_values[id_counter])
            id_counter +=1
            # --------------------------------------------------------------
            row = query.one_or_none()

            if row is not None:
                db.session.delete(row)
                db.session.flush()
                db.session.commit()
                db.session.close()
                message = f"Deleted 'Clusters' cluster_uuid = {id}"
                row     = json.loads(row.get_json())
            else:
                code    = API_NOT_FOUND
                message = f"Not found 'Clusters' with cluster_uuid = {id}"
                row     = None        
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Clusters',entities=[],name=current_app.config['NAME'])

# ======================================================================# view_cost_centers.py_gen_views_api.html.auto

# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2020-11-23 19:59:58.754884
# ======================================================================
# gen_views_api.html:AG 2020-11-23 19:59:58.754900
# table_name: Cost_Centers
# class_name: cost_centers
# is shardened: True
# Table 'Cost_Centers' keys = CC_Id
# Errors: None
# PK field found 'CC_Id' db.Integer
# Cost_Centers id field is 'Cost_Centers.CC_Id' of type 'int:'

@main.route('/api/get/Cost_Centers'     , methods=['GET'])
@main.route('/api/get/Cost_Centers/<int:id>', methods=['GET'])
def api_get_Cost_Centers(id=None):
    code       = API_OK
    message    = 'OK'
    rows       = None
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            id_counter = 0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values=[id]
            # Codigo para un solo campo de id
            # chequear si marcado explicitamente
            query = db.session.query(Cost_Centers)
            if id is not None:
                query = query.filter(Cost_Centers.CC_Id == id_values[id_counter])
                rows = query.one_or_none()
            else:
                if request.args is not None and len(request.args):
                    if 'CC_Id' in request.args:
                        query = query.filter(Cost_Centers.CC_Id == request.args.get('CC_Id'))
                    if 'CC_Code' in request.args:
                        query = query.filter(Cost_Centers.CC_Code == request.args.get('CC_Code'))
                    if 'CC_Description' in request.args:
                        query = query.filter(Cost_Centers.CC_Description == request.args.get('CC_Description'))
                    if 'Cur_Code' in request.args:
                        query = query.filter(Cost_Centers.Cur_Code == request.args.get('Cur_Code'))
                    if 'CC_Parent_Code' in request.args:
                        query = query.filter(Cost_Centers.CC_Parent_Code == request.args.get('CC_Parent_Code'))
                    if 'CC_Reg_Exp' in request.args:
                        query = query.filter(Cost_Centers.CC_Reg_Exp == request.args.get('CC_Reg_Exp'))
                    if 'CC_Reference' in request.args:
                        query = query.filter(Cost_Centers.CC_Reference == request.args.get('CC_Reference'))
                rows = query.all()
            if rows is not None:
                if type(rows) == list:
                    for i in range(len(rows)):
                        rows[i] = json.loads(rows[i].get_json())
                else:
                    rows = [json.loads(rows.get_json())]
            else:
                rows = []
            if len(rows) == 0:
                code = API_NO_DATA
                state = get_api_state(API_NO_DATA)
                
                if id is None:
                    message = f"No 'Cost_Centers' records found"
                else:
                    message = f"No 'Cost_Centers.CC_Id' = {id} record found"
                
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Cost_Centers',entities=rows,name=current_app.config['NAME'])

@main.route('/api/post/Cost_Centers', methods=['POST'])
def api_post_Cost_Centers():
    code    = API_OK
    message = 'OK'
    row     = None
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            row = Cost_Centers()
            # Populates row from json, if ID=int:autoincrement then None
            row.CC_Id = request.json.get('CC_Id',0)
            row.CC_Code = request.json.get('CC_Code',None)
            row.CC_Description = request.json.get('CC_Description',None)
            row.Cur_Code = request.json.get('Cur_Code',None)
            row.CC_Parent_Code = request.json.get('CC_Parent_Code',1)
            row.CC_Reg_Exp = request.json.get('CC_Reg_Exp',None)
            row.CC_Reference = request.json.get('CC_Reference',None)
            # ----------------------------------------------------------
            db.session.add(row)
            db.session.flush()
            db.session.commit()
            db.session.refresh(row)
            db.session.close()
            message = f"Created 'Cost_Centers' CC_Id = {row.CC_Id}"
            row     = json.loads(row.get_json())
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
            row     = None
    else:
        code    = API_ERROR
        message = 'Unauthorized request'            
    return get_api_response(code=code,message=message,kind='Cost_Centers',entities=[row],name=current_app.config['NAME'])

@main.route('/api/put/Cost_Centers/<int:id>', methods=['PUT'])
def api_put_Cost_Centers(id):
    code    = API_OK
    message = 'OK'
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            id_counter=0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values = [id]
            row   = Cost_Centers()
            query = db.session.query(Cost_Centers)
            
            # First loop mandatory for row population ----------------------
            query = query.filter(Cost_Centers.CC_Id == id_values[id_counter])
            id_counter += 1
            # --------------------------------------------------------------
            row = query.one_or_none()
            # If row exists then continue:
            if row is not None:
                # Second loop seek for updated fields ----------------------
                if 'CC_Code' in request.json.keys():
                    row.CC_Code = request.json.get('CC_Code')
                if 'CC_Description' in request.json.keys():
                    row.CC_Description = request.json.get('CC_Description')
                if 'Cur_Code' in request.json.keys():
                    row.Cur_Code = request.json.get('Cur_Code')
                if 'CC_Parent_Code' in request.json.keys():
                    row.CC_Parent_Code = request.json.get('CC_Parent_Code')
                if 'CC_Reg_Exp' in request.json.keys():
                    row.CC_Reg_Exp = request.json.get('CC_Reg_Exp')
                if 'CC_Reference' in request.json.keys():
                    row.CC_Reference = request.json.get('CC_Reference')
                # ----------------------------------------------------------
                db.session.merge(row)
                db.session.flush()
                db.session.commit()
                db.session.refresh(row)
                db.session.close()
                message = f"Modified 'Cost_Centers' CC_Id = {id}"
                row     = json.loads(row.get_json())
            else:
                code    = API_NOT_FOUND
                message = f"Not found Cost_Centers with CC_Id = {id}"
                row     = None
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Cost_Centers',entities=[row],name=current_app.config['NAME'])

@main.route('/api/patch/Cost_Centers/<int:id>', methods=['PATCH'])
def api_patch_Cost_Centers(id):
    code    = API_OK
    message = 'OK'
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            id_counter=0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values = [id]
            row   = Cost_Centers()
            query = db.session.query(Cost_Centers)
            
            # First loop mandatory for row population ----------------------
            query = query.filter(Cost_Centers.CC_Id == id_values[id_counter])
            id_counter += 1
            # --------------------------------------------------------------
            row = query.one_or_none()
            # If row exists then continue:
            if row is not None:
                # Second loop seek for updated fields ----------------------
                if 'CC_Code' in request.json.keys():
                    row.CC_Code = request.json.get('CC_Code')
                if 'CC_Description' in request.json.keys():
                    row.CC_Description = request.json.get('CC_Description')
                if 'Cur_Code' in request.json.keys():
                    row.Cur_Code = request.json.get('Cur_Code')
                if 'CC_Parent_Code' in request.json.keys():
                    row.CC_Parent_Code = request.json.get('CC_Parent_Code')
                if 'CC_Reg_Exp' in request.json.keys():
                    row.CC_Reg_Exp = request.json.get('CC_Reg_Exp')
                if 'CC_Reference' in request.json.keys():
                    row.CC_Reference = request.json.get('CC_Reference')
                # ----------------------------------------------------------
                db.session.merge(row)
                db.session.flush()
                db.session.commit()
                db.session.refresh(row)
                db.session.close()
                message = f"Modified 'Cost_Centers' CC_Id = {id}"
                row     = json.loads(row.get_json())
            else:
                code    = API_NOT_FOUND
                message = f"Not found Cost_Centers with CC_Id = {id}"
                row     = None
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Cost_Centers',entities=[row],name=current_app.config['NAME'])

@main.route('/api/delete/Cost_Centers/<int:id>', methods=['DELETE'])
def api_delete_Cost_Centers(id):
    code    = API_OK
    message = 'OK'
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            id_counter=0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values = [id]
            row   = Cost_Centers()
            query = db.session.query(Cost_Centers)
            
            # First loop mandatory for row population ----------------------
            # detected primary key field: c.field
            query       = query.filter(Cost_Centers.CC_Id == id_values[id_counter])
            id_counter +=1
            # --------------------------------------------------------------
            row = query.one_or_none()

            if row is not None:
                db.session.delete(row)
                db.session.flush()
                db.session.commit()
                db.session.close()
                message = f"Deleted 'Cost_Centers' CC_Id = {id}"
                row     = json.loads(row.get_json())
            else:
                code    = API_NOT_FOUND
                message = f"Not found 'Cost_Centers' with CC_Id = {id}"
                row     = None        
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Cost_Centers',entities=[],name=current_app.config['NAME'])

# ======================================================================# view_disk_images.py_gen_views_api.html.auto

# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2020-11-23 19:59:58.942917
# ======================================================================
# gen_views_api.html:AG 2020-11-23 19:59:58.942946
# table_name: Disk_Images
# class_name: disk_images
# is shardened: False
# Table 'Disk_Images' keys = uuid
# Errors: None
# PK field found 'uuid' db.String(45)
# Disk_Images id field is 'Disk_Images.uuid' of type ''

@main.route('/api/get/Disk_Images'     , methods=['GET'])
@main.route('/api/get/Disk_Images/<id>', methods=['GET'])
def api_get_Disk_Images(id=None):
    code       = API_OK
    message    = 'OK'
    rows       = None
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            id_counter = 0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values=[id]
            # Codigo para un solo campo de id
            # chequear si marcado explicitamente
            query = db.session.query(Disk_Images)
            if id is not None:
                query = query.filter(Disk_Images.uuid == id_values[id_counter])
                rows = query.one_or_none()
            else:
                if request.args is not None and len(request.args):
                    if 'uuid' in request.args:
                        query = query.filter(Disk_Images.uuid == request.args.get('uuid'))
                    if 'name' in request.args:
                        query = query.filter(Disk_Images.name == request.args.get('name'))
                    if 'annotation' in request.args:
                        query = query.filter(Disk_Images.annotation == request.args.get('annotation'))
                    if 'image_type' in request.args:
                        query = query.filter(Disk_Images.image_type == request.args.get('image_type'))
                    if 'image_state' in request.args:
                        query = query.filter(Disk_Images.image_state == request.args.get('image_state'))
                    if 'vm_disk_size' in request.args:
                        query = query.filter(Disk_Images.vm_disk_size == request.args.get('vm_disk_size'))
                    if 'vm_disk_size_mib' in request.args:
                        query = query.filter(Disk_Images.vm_disk_size_mib == request.args.get('vm_disk_size_mib'))
                    if 'vm_disk_size_gib' in request.args:
                        query = query.filter(Disk_Images.vm_disk_size_gib == request.args.get('vm_disk_size_gib'))
                    if 'cluster' in request.args:
                        query = query.filter(Disk_Images.cluster == request.args.get('cluster'))
                rows = query.all()
            if rows is not None:
                if type(rows) == list:
                    for i in range(len(rows)):
                        rows[i] = json.loads(rows[i].get_json())
                else:
                    rows = [json.loads(rows.get_json())]
            else:
                rows = []
            if len(rows) == 0:
                code = API_NO_DATA
                state = get_api_state(API_NO_DATA)
                
                if id is None:
                    message = f"No 'Disk_Images' records found"
                else:
                    message = f"No 'Disk_Images.uuid' = {id} record found"
                
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Disk_Images',entities=rows,name=current_app.config['NAME'])

@main.route('/api/post/Disk_Images', methods=['POST'])
def api_post_Disk_Images():
    code    = API_OK
    message = 'OK'
    row     = None
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            row = Disk_Images()
            # Populates row from json, if ID=int:autoincrement then None
            row.uuid = request.json.get('uuid',None)
            row.name = request.json.get('name',None)
            row.annotation = request.json.get('annotation',None)
            row.image_type = request.json.get('image_type',None)
            row.image_state = request.json.get('image_state',None)
            row.vm_disk_size = request.json.get('vm_disk_size',0)
            row.vm_disk_size_mib = request.json.get('vm_disk_size_mib',0)
            row.vm_disk_size_gib = request.json.get('vm_disk_size_gib',0)
            row.cluster = request.json.get('cluster',None)
            # ----------------------------------------------------------
            db.session.add(row)
            db.session.flush()
            db.session.commit()
            db.session.refresh(row)
            db.session.close()
            message = f"Created 'Disk_Images' uuid = {row.uuid}"
            row     = json.loads(row.get_json())
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
            row     = None
    else:
        code    = API_ERROR
        message = 'Unauthorized request'            
    return get_api_response(code=code,message=message,kind='Disk_Images',entities=[row],name=current_app.config['NAME'])

@main.route('/api/put/Disk_Images/<id>', methods=['PUT'])
def api_put_Disk_Images(id):
    code    = API_OK
    message = 'OK'
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            id_counter=0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values = [id]
            row   = Disk_Images()
            query = db.session.query(Disk_Images)
            
            # First loop mandatory for row population ----------------------
            query = query.filter(Disk_Images.uuid == id_values[id_counter])
            id_counter += 1
            # --------------------------------------------------------------
            row = query.one_or_none()
            # If row exists then continue:
            if row is not None:
                # Second loop seek for updated fields ----------------------
                if 'name' in request.json.keys():
                    row.name = request.json.get('name')
                if 'annotation' in request.json.keys():
                    row.annotation = request.json.get('annotation')
                if 'image_type' in request.json.keys():
                    row.image_type = request.json.get('image_type')
                if 'image_state' in request.json.keys():
                    row.image_state = request.json.get('image_state')
                if 'vm_disk_size' in request.json.keys():
                    row.vm_disk_size = request.json.get('vm_disk_size')
                if 'vm_disk_size_mib' in request.json.keys():
                    row.vm_disk_size_mib = request.json.get('vm_disk_size_mib')
                if 'vm_disk_size_gib' in request.json.keys():
                    row.vm_disk_size_gib = request.json.get('vm_disk_size_gib')
                if 'cluster' in request.json.keys():
                    row.cluster = request.json.get('cluster')
                # ----------------------------------------------------------
                db.session.merge(row)
                db.session.flush()
                db.session.commit()
                db.session.refresh(row)
                db.session.close()
                message = f"Modified 'Disk_Images' uuid = {id}"
                row     = json.loads(row.get_json())
            else:
                code    = API_NOT_FOUND
                message = f"Not found Disk_Images with uuid = {id}"
                row     = None
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Disk_Images',entities=[row],name=current_app.config['NAME'])

@main.route('/api/patch/Disk_Images/<id>', methods=['PATCH'])
def api_patch_Disk_Images(id):
    code    = API_OK
    message = 'OK'
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            id_counter=0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values = [id]
            row   = Disk_Images()
            query = db.session.query(Disk_Images)
            
            # First loop mandatory for row population ----------------------
            query = query.filter(Disk_Images.uuid == id_values[id_counter])
            id_counter += 1
            # --------------------------------------------------------------
            row = query.one_or_none()
            # If row exists then continue:
            if row is not None:
                # Second loop seek for updated fields ----------------------
                if 'name' in request.json.keys():
                    row.name = request.json.get('name')
                if 'annotation' in request.json.keys():
                    row.annotation = request.json.get('annotation')
                if 'image_type' in request.json.keys():
                    row.image_type = request.json.get('image_type')
                if 'image_state' in request.json.keys():
                    row.image_state = request.json.get('image_state')
                if 'vm_disk_size' in request.json.keys():
                    row.vm_disk_size = request.json.get('vm_disk_size')
                if 'vm_disk_size_mib' in request.json.keys():
                    row.vm_disk_size_mib = request.json.get('vm_disk_size_mib')
                if 'vm_disk_size_gib' in request.json.keys():
                    row.vm_disk_size_gib = request.json.get('vm_disk_size_gib')
                if 'cluster' in request.json.keys():
                    row.cluster = request.json.get('cluster')
                # ----------------------------------------------------------
                db.session.merge(row)
                db.session.flush()
                db.session.commit()
                db.session.refresh(row)
                db.session.close()
                message = f"Modified 'Disk_Images' uuid = {id}"
                row     = json.loads(row.get_json())
            else:
                code    = API_NOT_FOUND
                message = f"Not found Disk_Images with uuid = {id}"
                row     = None
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Disk_Images',entities=[row],name=current_app.config['NAME'])

@main.route('/api/delete/Disk_Images/<id>', methods=['DELETE'])
def api_delete_Disk_Images(id):
    code    = API_OK
    message = 'OK'
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            id_counter=0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values = [id]
            row   = Disk_Images()
            query = db.session.query(Disk_Images)
            
            # First loop mandatory for row population ----------------------
            # detected primary key field: c.field
            query       = query.filter(Disk_Images.uuid == id_values[id_counter])
            id_counter +=1
            # --------------------------------------------------------------
            row = query.one_or_none()

            if row is not None:
                db.session.delete(row)
                db.session.flush()
                db.session.commit()
                db.session.close()
                message = f"Deleted 'Disk_Images' uuid = {id}"
                row     = json.loads(row.get_json())
            else:
                code    = API_NOT_FOUND
                message = f"Not found 'Disk_Images' with uuid = {id}"
                row     = None        
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Disk_Images',entities=[],name=current_app.config['NAME'])

# ======================================================================# view_domains.py_gen_views_api.html.auto

# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2020-11-23 19:59:59.098486
# ======================================================================
# gen_views_api.html:AG 2020-11-23 19:59:59.098501
# table_name: Domains
# class_name: domains
# is shardened: False
# Table 'Domains' keys = Domain_Id
# Errors: None
# PK field found 'Domain_Id' db.Integer
# Domains id field is 'Domains.Domain_Id' of type 'int:'

@main.route('/api/get/Domains'     , methods=['GET'])
@main.route('/api/get/Domains/<int:id>', methods=['GET'])
def api_get_Domains(id=None):
    code       = API_OK
    message    = 'OK'
    rows       = None
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            id_counter = 0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values=[id]
            # Codigo para un solo campo de id
            # chequear si marcado explicitamente
            query = db.session.query(Domains)
            if id is not None:
                query = query.filter(Domains.Domain_Id == id_values[id_counter])
                rows = query.one_or_none()
            else:
                if request.args is not None and len(request.args):
                    if 'Domain_Id' in request.args:
                        query = query.filter(Domains.Domain_Id == request.args.get('Domain_Id'))
                    if 'Name' in request.args:
                        query = query.filter(Domains.Name == request.args.get('Name'))
                    if 'Comments' in request.args:
                        query = query.filter(Domains.Comments == request.args.get('Comments'))
                rows = query.all()
            if rows is not None:
                if type(rows) == list:
                    for i in range(len(rows)):
                        rows[i] = json.loads(rows[i].get_json())
                else:
                    rows = [json.loads(rows.get_json())]
            else:
                rows = []
            if len(rows) == 0:
                code = API_NO_DATA
                state = get_api_state(API_NO_DATA)
                
                if id is None:
                    message = f"No 'Domains' records found"
                else:
                    message = f"No 'Domains.Domain_Id' = {id} record found"
                
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Domains',entities=rows,name=current_app.config['NAME'])

@main.route('/api/post/Domains', methods=['POST'])
def api_post_Domains():
    code    = API_OK
    message = 'OK'
    row     = None
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            row = Domains()
            # Populates row from json, if ID=int:autoincrement then None
            row.Domain_Id = request.json.get('Domain_Id',None)
            row.Name = request.json.get('Name',None)
            row.Comments = request.json.get('Comments',None)
            # ----------------------------------------------------------
            db.session.add(row)
            db.session.flush()
            db.session.commit()
            db.session.refresh(row)
            db.session.close()
            message = f"Created 'Domains' Domain_Id = {row.Domain_Id}"
            row     = json.loads(row.get_json())
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
            row     = None
    else:
        code    = API_ERROR
        message = 'Unauthorized request'            
    return get_api_response(code=code,message=message,kind='Domains',entities=[row],name=current_app.config['NAME'])

@main.route('/api/put/Domains/<int:id>', methods=['PUT'])
def api_put_Domains(id):
    code    = API_OK
    message = 'OK'
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            id_counter=0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values = [id]
            row   = Domains()
            query = db.session.query(Domains)
            
            # First loop mandatory for row population ----------------------
            query = query.filter(Domains.Domain_Id == id_values[id_counter])
            id_counter += 1
            # --------------------------------------------------------------
            row = query.one_or_none()
            # If row exists then continue:
            if row is not None:
                # Second loop seek for updated fields ----------------------
                if 'Name' in request.json.keys():
                    row.Name = request.json.get('Name')
                if 'Comments' in request.json.keys():
                    row.Comments = request.json.get('Comments')
                # ----------------------------------------------------------
                db.session.merge(row)
                db.session.flush()
                db.session.commit()
                db.session.refresh(row)
                db.session.close()
                message = f"Modified 'Domains' Domain_Id = {id}"
                row     = json.loads(row.get_json())
            else:
                code    = API_NOT_FOUND
                message = f"Not found Domains with Domain_Id = {id}"
                row     = None
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Domains',entities=[row],name=current_app.config['NAME'])

@main.route('/api/patch/Domains/<int:id>', methods=['PATCH'])
def api_patch_Domains(id):
    code    = API_OK
    message = 'OK'
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            id_counter=0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values = [id]
            row   = Domains()
            query = db.session.query(Domains)
            
            # First loop mandatory for row population ----------------------
            query = query.filter(Domains.Domain_Id == id_values[id_counter])
            id_counter += 1
            # --------------------------------------------------------------
            row = query.one_or_none()
            # If row exists then continue:
            if row is not None:
                # Second loop seek for updated fields ----------------------
                if 'Name' in request.json.keys():
                    row.Name = request.json.get('Name')
                if 'Comments' in request.json.keys():
                    row.Comments = request.json.get('Comments')
                # ----------------------------------------------------------
                db.session.merge(row)
                db.session.flush()
                db.session.commit()
                db.session.refresh(row)
                db.session.close()
                message = f"Modified 'Domains' Domain_Id = {id}"
                row     = json.loads(row.get_json())
            else:
                code    = API_NOT_FOUND
                message = f"Not found Domains with Domain_Id = {id}"
                row     = None
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Domains',entities=[row],name=current_app.config['NAME'])

@main.route('/api/delete/Domains/<int:id>', methods=['DELETE'])
def api_delete_Domains(id):
    code    = API_OK
    message = 'OK'
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            id_counter=0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values = [id]
            row   = Domains()
            query = db.session.query(Domains)
            
            # First loop mandatory for row population ----------------------
            # detected primary key field: c.field
            query       = query.filter(Domains.Domain_Id == id_values[id_counter])
            id_counter +=1
            # --------------------------------------------------------------
            row = query.one_or_none()

            if row is not None:
                db.session.delete(row)
                db.session.flush()
                db.session.commit()
                db.session.close()
                message = f"Deleted 'Domains' Domain_Id = {id}"
                row     = json.loads(row.get_json())
            else:
                code    = API_NOT_FOUND
                message = f"Not found 'Domains' with Domain_Id = {id}"
                row     = None        
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Domains',entities=[],name=current_app.config['NAME'])

# ======================================================================# view_interface.py_gen_views_api.html.auto

# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2020-11-23 19:59:59.279691
# ======================================================================
# gen_views_api.html:AG 2020-11-23 19:59:59.279713
# table_name: Interface
# class_name: interface
# is shardened: False
# Table 'Interface' keys = Id
# Errors: None
# ID field found 'Id' auto_increment db.Integer
# Interface id field is 'Interface.Id' of type 'int:'

@main.route('/api/get/Interface'     , methods=['GET'])
@main.route('/api/get/Interface/<int:id>', methods=['GET'])
def api_get_Interface(id=None):
    code       = API_OK
    message    = 'OK'
    rows       = None
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            id_counter = 0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values=[id]
            # Codigo para un solo campo de id
            # chequear si marcado explicitamente
            query = db.session.query(Interface)
            if id is not None:
                query = query.filter(Interface.Id == id_values[id_counter])
                rows = query.one_or_none()
            else:
                if request.args is not None and len(request.args):
                    if 'Id' in request.args:
                        query = query.filter(Interface.Id == request.args.get('Id'))
                    if 'User_Id' in request.args:
                        query = query.filter(Interface.User_Id == request.args.get('User_Id'))
                    if 'Table_name' in request.args:
                        query = query.filter(Interface.Table_name == request.args.get('Table_name'))
                    if 'Option_Type' in request.args:
                        query = query.filter(Interface.Option_Type == request.args.get('Option_Type'))
                    if 'Argument_1' in request.args:
                        query = query.filter(Interface.Argument_1 == request.args.get('Argument_1'))
                    if 'Argument_2' in request.args:
                        query = query.filter(Interface.Argument_2 == request.args.get('Argument_2'))
                    if 'Argument_3' in request.args:
                        query = query.filter(Interface.Argument_3 == request.args.get('Argument_3'))
                    if 'Is_Active' in request.args:
                        query = query.filter(Interface.Is_Active == request.args.get('Is_Active'))
                rows = query.all()
            if rows is not None:
                if type(rows) == list:
                    for i in range(len(rows)):
                        rows[i] = json.loads(rows[i].get_json())
                else:
                    rows = [json.loads(rows.get_json())]
            else:
                rows = []
            if len(rows) == 0:
                code = API_NO_DATA
                state = get_api_state(API_NO_DATA)
                
                if id is None:
                    message = f"No 'Interface' records found"
                else:
                    message = f"No 'Interface.Id' = {id} record found"
                
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Interface',entities=rows,name=current_app.config['NAME'])

@main.route('/api/post/Interface', methods=['POST'])
def api_post_Interface():
    code    = API_OK
    message = 'OK'
    row     = None
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            row = Interface()
            # Populates row from json, if ID=int:autoincrement then None
            row.Id = None
            row.User_Id = request.json.get('User_Id',None)
            row.Table_name = request.json.get('Table_name',None)
            row.Option_Type = request.json.get('Option_Type',None)
            row.Argument_1 = request.json.get('Argument_1',None)
            row.Argument_2 = request.json.get('Argument_2',None)
            row.Argument_3 = request.json.get('Argument_3',None)
            row.Is_Active = request.json.get('Is_Active',None)
            # ----------------------------------------------------------
            db.session.add(row)
            db.session.flush()
            db.session.commit()
            db.session.refresh(row)
            db.session.close()
            message = f"Created 'Interface' Id = {row.Id}"
            row     = json.loads(row.get_json())
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
            row     = None
    else:
        code    = API_ERROR
        message = 'Unauthorized request'            
    return get_api_response(code=code,message=message,kind='Interface',entities=[row],name=current_app.config['NAME'])

@main.route('/api/put/Interface/<int:id>', methods=['PUT'])
def api_put_Interface(id):
    code    = API_OK
    message = 'OK'
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            id_counter=0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values = [id]
            row   = Interface()
            query = db.session.query(Interface)
            
            # First loop mandatory for row population ----------------------
            query = query.filter(Interface.Id == id_values[id_counter])
            id_counter += 1
            # --------------------------------------------------------------
            row = query.one_or_none()
            # If row exists then continue:
            if row is not None:
                # Second loop seek for updated fields ----------------------
                if 'User_Id' in request.json.keys():
                    row.User_Id = request.json.get('User_Id')
                if 'Table_name' in request.json.keys():
                    row.Table_name = request.json.get('Table_name')
                if 'Option_Type' in request.json.keys():
                    row.Option_Type = request.json.get('Option_Type')
                if 'Argument_1' in request.json.keys():
                    row.Argument_1 = request.json.get('Argument_1')
                if 'Argument_2' in request.json.keys():
                    row.Argument_2 = request.json.get('Argument_2')
                if 'Argument_3' in request.json.keys():
                    row.Argument_3 = request.json.get('Argument_3')
                if 'Is_Active' in request.json.keys():
                    row.Is_Active = request.json.get('Is_Active')
                # ----------------------------------------------------------
                db.session.merge(row)
                db.session.flush()
                db.session.commit()
                db.session.refresh(row)
                db.session.close()
                message = f"Modified 'Interface' Id = {id}"
                row     = json.loads(row.get_json())
            else:
                code    = API_NOT_FOUND
                message = f"Not found Interface with Id = {id}"
                row     = None
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Interface',entities=[row],name=current_app.config['NAME'])

@main.route('/api/patch/Interface/<int:id>', methods=['PATCH'])
def api_patch_Interface(id):
    code    = API_OK
    message = 'OK'
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            id_counter=0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values = [id]
            row   = Interface()
            query = db.session.query(Interface)
            
            # First loop mandatory for row population ----------------------
            query = query.filter(Interface.Id == id_values[id_counter])
            id_counter += 1
            # --------------------------------------------------------------
            row = query.one_or_none()
            # If row exists then continue:
            if row is not None:
                # Second loop seek for updated fields ----------------------
                if 'User_Id' in request.json.keys():
                    row.User_Id = request.json.get('User_Id')
                if 'Table_name' in request.json.keys():
                    row.Table_name = request.json.get('Table_name')
                if 'Option_Type' in request.json.keys():
                    row.Option_Type = request.json.get('Option_Type')
                if 'Argument_1' in request.json.keys():
                    row.Argument_1 = request.json.get('Argument_1')
                if 'Argument_2' in request.json.keys():
                    row.Argument_2 = request.json.get('Argument_2')
                if 'Argument_3' in request.json.keys():
                    row.Argument_3 = request.json.get('Argument_3')
                if 'Is_Active' in request.json.keys():
                    row.Is_Active = request.json.get('Is_Active')
                # ----------------------------------------------------------
                db.session.merge(row)
                db.session.flush()
                db.session.commit()
                db.session.refresh(row)
                db.session.close()
                message = f"Modified 'Interface' Id = {id}"
                row     = json.loads(row.get_json())
            else:
                code    = API_NOT_FOUND
                message = f"Not found Interface with Id = {id}"
                row     = None
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Interface',entities=[row],name=current_app.config['NAME'])

@main.route('/api/delete/Interface/<int:id>', methods=['DELETE'])
def api_delete_Interface(id):
    code    = API_OK
    message = 'OK'
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            id_counter=0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values = [id]
            row   = Interface()
            query = db.session.query(Interface)
            
            # First loop mandatory for row population ----------------------
            query = query.filter(Interface.Id == id)
            # --------------------------------------------------------------
            row = query.one_or_none()

            if row is not None:
                db.session.delete(row)
                db.session.flush()
                db.session.commit()
                db.session.close()
                message = f"Deleted 'Interface' Id = {id}"
                row     = json.loads(row.get_json())
            else:
                code    = API_NOT_FOUND
                message = f"Not found 'Interface' with Id = {id}"
                row     = None        
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Interface',entities=[],name=current_app.config['NAME'])

# ======================================================================# view_nutanix_prism_vm.py_gen_views_api.html.auto

# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2020-11-23 19:59:59.527827
# ======================================================================
# gen_views_api.html:AG 2020-11-23 19:59:59.527842
# table_name: Nutanix_Prism_VM
# class_name: nutanix_prism_vm
# is shardened: False
# Table 'Nutanix_Prism_VM' keys = Request_Id
# Errors: None
# PK field found 'Request_Id' db.Integer
# Nutanix_Prism_VM id field is 'Nutanix_Prism_VM.Request_Id' of type 'int:'

@main.route('/api/get/Nutanix_Prism_VM'     , methods=['GET'])
@main.route('/api/get/Nutanix_Prism_VM/<int:id>', methods=['GET'])
def api_get_Nutanix_Prism_VM(id=None):
    code       = API_OK
    message    = 'OK'
    rows       = None
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            id_counter = 0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values=[id]
            # Codigo para un solo campo de id
            # chequear si marcado explicitamente
            query = db.session.query(Nutanix_Prism_VM)
            if id is not None:
                query = query.filter(Nutanix_Prism_VM.Request_Id == id_values[id_counter])
                rows = query.one_or_none()
            else:
                if request.args is not None and len(request.args):
                    if 'Request_Id' in request.args:
                        query = query.filter(Nutanix_Prism_VM.Request_Id == request.args.get('Request_Id'))
                    if 'project_uuid' in request.args:
                        query = query.filter(Nutanix_Prism_VM.project_uuid == request.args.get('project_uuid'))
                    if 'category_name' in request.args:
                        query = query.filter(Nutanix_Prism_VM.category_name == request.args.get('category_name'))
                    if 'cluster_uuid' in request.args:
                        query = query.filter(Nutanix_Prism_VM.cluster_uuid == request.args.get('cluster_uuid'))
                    if 'vm_name' in request.args:
                        query = query.filter(Nutanix_Prism_VM.vm_name == request.args.get('vm_name'))
                    if 'power_state' in request.args:
                        query = query.filter(Nutanix_Prism_VM.power_state == request.args.get('power_state'))
                    if 'vcpus_per_socket' in request.args:
                        query = query.filter(Nutanix_Prism_VM.vcpus_per_socket == request.args.get('vcpus_per_socket'))
                    if 'num_sockets' in request.args:
                        query = query.filter(Nutanix_Prism_VM.num_sockets == request.args.get('num_sockets'))
                    if 'memory_size_mib' in request.args:
                        query = query.filter(Nutanix_Prism_VM.memory_size_mib == request.args.get('memory_size_mib'))
                    if 'memory_size_gib' in request.args:
                        query = query.filter(Nutanix_Prism_VM.memory_size_gib == request.args.get('memory_size_gib'))
                    if 'Comments' in request.args:
                        query = query.filter(Nutanix_Prism_VM.Comments == request.args.get('Comments'))
                    if 'vm_ip' in request.args:
                        query = query.filter(Nutanix_Prism_VM.vm_ip == request.args.get('vm_ip'))
                    if 'subnet_uuid' in request.args:
                        query = query.filter(Nutanix_Prism_VM.subnet_uuid == request.args.get('subnet_uuid'))
                    if 'vm_username' in request.args:
                        query = query.filter(Nutanix_Prism_VM.vm_username == request.args.get('vm_username'))
                    if 'vm_password' in request.args:
                        query = query.filter(Nutanix_Prism_VM.vm_password == request.args.get('vm_password'))
                    if 'backup_set_1' in request.args:
                        query = query.filter(Nutanix_Prism_VM.backup_set_1 == request.args.get('backup_set_1'))
                    if 'backup_set_2' in request.args:
                        query = query.filter(Nutanix_Prism_VM.backup_set_2 == request.args.get('backup_set_2'))
                    if 'backup_set_3' in request.args:
                        query = query.filter(Nutanix_Prism_VM.backup_set_3 == request.args.get('backup_set_3'))
                    if 'disk_type' in request.args:
                        query = query.filter(Nutanix_Prism_VM.disk_type == request.args.get('disk_type'))
                    if 'disk_0_image' in request.args:
                        query = query.filter(Nutanix_Prism_VM.disk_0_image == request.args.get('disk_0_image'))
                    if 'disk_0_size' in request.args:
                        query = query.filter(Nutanix_Prism_VM.disk_0_size == request.args.get('disk_0_size'))
                    if 'disk_1_image' in request.args:
                        query = query.filter(Nutanix_Prism_VM.disk_1_image == request.args.get('disk_1_image'))
                    if 'disk_1_size' in request.args:
                        query = query.filter(Nutanix_Prism_VM.disk_1_size == request.args.get('disk_1_size'))
                    if 'disk_2_image' in request.args:
                        query = query.filter(Nutanix_Prism_VM.disk_2_image == request.args.get('disk_2_image'))
                    if 'disk_2_size' in request.args:
                        query = query.filter(Nutanix_Prism_VM.disk_2_size == request.args.get('disk_2_size'))
                    if 'disk_3_image' in request.args:
                        query = query.filter(Nutanix_Prism_VM.disk_3_image == request.args.get('disk_3_image'))
                    if 'disk_3_size' in request.args:
                        query = query.filter(Nutanix_Prism_VM.disk_3_size == request.args.get('disk_3_size'))
                    if 'disk_4_image' in request.args:
                        query = query.filter(Nutanix_Prism_VM.disk_4_image == request.args.get('disk_4_image'))
                    if 'disk_4_size' in request.args:
                        query = query.filter(Nutanix_Prism_VM.disk_4_size == request.args.get('disk_4_size'))
                    if 'disk_5_image' in request.args:
                        query = query.filter(Nutanix_Prism_VM.disk_5_image == request.args.get('disk_5_image'))
                    if 'disk_5_size' in request.args:
                        query = query.filter(Nutanix_Prism_VM.disk_5_size == request.args.get('disk_5_size'))
                    if 'disk_6_image' in request.args:
                        query = query.filter(Nutanix_Prism_VM.disk_6_image == request.args.get('disk_6_image'))
                    if 'disk_6_size' in request.args:
                        query = query.filter(Nutanix_Prism_VM.disk_6_size == request.args.get('disk_6_size'))
                    if 'disk_7_image' in request.args:
                        query = query.filter(Nutanix_Prism_VM.disk_7_image == request.args.get('disk_7_image'))
                    if 'disk_7_size' in request.args:
                        query = query.filter(Nutanix_Prism_VM.disk_7_size == request.args.get('disk_7_size'))
                    if 'disk_8_image' in request.args:
                        query = query.filter(Nutanix_Prism_VM.disk_8_image == request.args.get('disk_8_image'))
                    if 'disk_8_size' in request.args:
                        query = query.filter(Nutanix_Prism_VM.disk_8_size == request.args.get('disk_8_size'))
                    if 'disk_9_image' in request.args:
                        query = query.filter(Nutanix_Prism_VM.disk_9_image == request.args.get('disk_9_image'))
                    if 'disk_9_size' in request.args:
                        query = query.filter(Nutanix_Prism_VM.disk_9_size == request.args.get('disk_9_size'))
                    if 'disk_10_image' in request.args:
                        query = query.filter(Nutanix_Prism_VM.disk_10_image == request.args.get('disk_10_image'))
                    if 'disk_10_size' in request.args:
                        query = query.filter(Nutanix_Prism_VM.disk_10_size == request.args.get('disk_10_size'))
                    if 'disk_11_image' in request.args:
                        query = query.filter(Nutanix_Prism_VM.disk_11_image == request.args.get('disk_11_image'))
                    if 'disk_11_size' in request.args:
                        query = query.filter(Nutanix_Prism_VM.disk_11_size == request.args.get('disk_11_size'))
                rows = query.all()
            if rows is not None:
                if type(rows) == list:
                    for i in range(len(rows)):
                        rows[i] = json.loads(rows[i].get_json())
                else:
                    rows = [json.loads(rows.get_json())]
            else:
                rows = []
            if len(rows) == 0:
                code = API_NO_DATA
                state = get_api_state(API_NO_DATA)
                
                if id is None:
                    message = f"No 'Nutanix_Prism_VM' records found"
                else:
                    message = f"No 'Nutanix_Prism_VM.Request_Id' = {id} record found"
                
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Nutanix_Prism_VM',entities=rows,name=current_app.config['NAME'])

@main.route('/api/post/Nutanix_Prism_VM', methods=['POST'])
def api_post_Nutanix_Prism_VM():
    code    = API_OK
    message = 'OK'
    row     = None
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            row = Nutanix_Prism_VM()
            # Populates row from json, if ID=int:autoincrement then None
            row.Request_Id = request.json.get('Request_Id',None)
            row.project_uuid = request.json.get('project_uuid',None)
            row.category_name = request.json.get('category_name',None)
            row.cluster_uuid = request.json.get('cluster_uuid',None)
            row.vm_name = request.json.get('vm_name',None)
            row.power_state = request.json.get('power_state',1)
            row.vcpus_per_socket = request.json.get('vcpus_per_socket',1)
            row.num_sockets = request.json.get('num_sockets',1)
            row.memory_size_mib = request.json.get('memory_size_mib',0)
            row.memory_size_gib = request.json.get('memory_size_gib',0)
            row.Comments = request.json.get('Comments',None)
            row.vm_ip = request.json.get('vm_ip',None)
            row.subnet_uuid = request.json.get('subnet_uuid',None)
            row.vm_username = request.json.get('vm_username',None)
            row.vm_password = request.json.get('vm_password',None)
            row.backup_set_1 = request.json.get('backup_set_1',None)
            row.backup_set_2 = request.json.get('backup_set_2',None)
            row.backup_set_3 = request.json.get('backup_set_3',None)
            row.disk_type = request.json.get('disk_type',0)
            row.disk_0_image = request.json.get('disk_0_image',None)
            row.disk_0_size = request.json.get('disk_0_size',0)
            row.disk_1_image = request.json.get('disk_1_image',None)
            row.disk_1_size = request.json.get('disk_1_size',0)
            row.disk_2_image = request.json.get('disk_2_image',None)
            row.disk_2_size = request.json.get('disk_2_size',0)
            row.disk_3_image = request.json.get('disk_3_image',None)
            row.disk_3_size = request.json.get('disk_3_size',0)
            row.disk_4_image = request.json.get('disk_4_image',None)
            row.disk_4_size = request.json.get('disk_4_size',0)
            row.disk_5_image = request.json.get('disk_5_image',None)
            row.disk_5_size = request.json.get('disk_5_size',0)
            row.disk_6_image = request.json.get('disk_6_image',None)
            row.disk_6_size = request.json.get('disk_6_size',0)
            row.disk_7_image = request.json.get('disk_7_image',None)
            row.disk_7_size = request.json.get('disk_7_size',0)
            row.disk_8_image = request.json.get('disk_8_image',None)
            row.disk_8_size = request.json.get('disk_8_size',0)
            row.disk_9_image = request.json.get('disk_9_image',None)
            row.disk_9_size = request.json.get('disk_9_size',0)
            row.disk_10_image = request.json.get('disk_10_image',None)
            row.disk_10_size = request.json.get('disk_10_size',0)
            row.disk_11_image = request.json.get('disk_11_image',None)
            row.disk_11_size = request.json.get('disk_11_size',0)
            # ----------------------------------------------------------
            db.session.add(row)
            db.session.flush()
            db.session.commit()
            db.session.refresh(row)
            db.session.close()
            message = f"Created 'Nutanix_Prism_VM' Request_Id = {row.Request_Id}"
            row     = json.loads(row.get_json())
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
            row     = None
    else:
        code    = API_ERROR
        message = 'Unauthorized request'            
    return get_api_response(code=code,message=message,kind='Nutanix_Prism_VM',entities=[row],name=current_app.config['NAME'])

@main.route('/api/put/Nutanix_Prism_VM/<int:id>', methods=['PUT'])
def api_put_Nutanix_Prism_VM(id):
    code    = API_OK
    message = 'OK'
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            id_counter=0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values = [id]
            row   = Nutanix_Prism_VM()
            query = db.session.query(Nutanix_Prism_VM)
            
            # First loop mandatory for row population ----------------------
            query = query.filter(Nutanix_Prism_VM.Request_Id == id_values[id_counter])
            id_counter += 1
            # --------------------------------------------------------------
            row = query.one_or_none()
            # If row exists then continue:
            if row is not None:
                # Second loop seek for updated fields ----------------------
                if 'project_uuid' in request.json.keys():
                    row.project_uuid = request.json.get('project_uuid')
                if 'category_name' in request.json.keys():
                    row.category_name = request.json.get('category_name')
                if 'cluster_uuid' in request.json.keys():
                    row.cluster_uuid = request.json.get('cluster_uuid')
                if 'vm_name' in request.json.keys():
                    row.vm_name = request.json.get('vm_name')
                if 'power_state' in request.json.keys():
                    row.power_state = request.json.get('power_state')
                if 'vcpus_per_socket' in request.json.keys():
                    row.vcpus_per_socket = request.json.get('vcpus_per_socket')
                if 'num_sockets' in request.json.keys():
                    row.num_sockets = request.json.get('num_sockets')
                if 'memory_size_mib' in request.json.keys():
                    row.memory_size_mib = request.json.get('memory_size_mib')
                if 'memory_size_gib' in request.json.keys():
                    row.memory_size_gib = request.json.get('memory_size_gib')
                if 'Comments' in request.json.keys():
                    row.Comments = request.json.get('Comments')
                if 'vm_ip' in request.json.keys():
                    row.vm_ip = request.json.get('vm_ip')
                if 'subnet_uuid' in request.json.keys():
                    row.subnet_uuid = request.json.get('subnet_uuid')
                if 'vm_username' in request.json.keys():
                    row.vm_username = request.json.get('vm_username')
                if 'vm_password' in request.json.keys():
                    row.vm_password = request.json.get('vm_password')
                if 'backup_set_1' in request.json.keys():
                    row.backup_set_1 = request.json.get('backup_set_1')
                if 'backup_set_2' in request.json.keys():
                    row.backup_set_2 = request.json.get('backup_set_2')
                if 'backup_set_3' in request.json.keys():
                    row.backup_set_3 = request.json.get('backup_set_3')
                if 'disk_type' in request.json.keys():
                    row.disk_type = request.json.get('disk_type')
                if 'disk_0_image' in request.json.keys():
                    row.disk_0_image = request.json.get('disk_0_image')
                if 'disk_0_size' in request.json.keys():
                    row.disk_0_size = request.json.get('disk_0_size')
                if 'disk_1_image' in request.json.keys():
                    row.disk_1_image = request.json.get('disk_1_image')
                if 'disk_1_size' in request.json.keys():
                    row.disk_1_size = request.json.get('disk_1_size')
                if 'disk_2_image' in request.json.keys():
                    row.disk_2_image = request.json.get('disk_2_image')
                if 'disk_2_size' in request.json.keys():
                    row.disk_2_size = request.json.get('disk_2_size')
                if 'disk_3_image' in request.json.keys():
                    row.disk_3_image = request.json.get('disk_3_image')
                if 'disk_3_size' in request.json.keys():
                    row.disk_3_size = request.json.get('disk_3_size')
                if 'disk_4_image' in request.json.keys():
                    row.disk_4_image = request.json.get('disk_4_image')
                if 'disk_4_size' in request.json.keys():
                    row.disk_4_size = request.json.get('disk_4_size')
                if 'disk_5_image' in request.json.keys():
                    row.disk_5_image = request.json.get('disk_5_image')
                if 'disk_5_size' in request.json.keys():
                    row.disk_5_size = request.json.get('disk_5_size')
                if 'disk_6_image' in request.json.keys():
                    row.disk_6_image = request.json.get('disk_6_image')
                if 'disk_6_size' in request.json.keys():
                    row.disk_6_size = request.json.get('disk_6_size')
                if 'disk_7_image' in request.json.keys():
                    row.disk_7_image = request.json.get('disk_7_image')
                if 'disk_7_size' in request.json.keys():
                    row.disk_7_size = request.json.get('disk_7_size')
                if 'disk_8_image' in request.json.keys():
                    row.disk_8_image = request.json.get('disk_8_image')
                if 'disk_8_size' in request.json.keys():
                    row.disk_8_size = request.json.get('disk_8_size')
                if 'disk_9_image' in request.json.keys():
                    row.disk_9_image = request.json.get('disk_9_image')
                if 'disk_9_size' in request.json.keys():
                    row.disk_9_size = request.json.get('disk_9_size')
                if 'disk_10_image' in request.json.keys():
                    row.disk_10_image = request.json.get('disk_10_image')
                if 'disk_10_size' in request.json.keys():
                    row.disk_10_size = request.json.get('disk_10_size')
                if 'disk_11_image' in request.json.keys():
                    row.disk_11_image = request.json.get('disk_11_image')
                if 'disk_11_size' in request.json.keys():
                    row.disk_11_size = request.json.get('disk_11_size')
                # ----------------------------------------------------------
                db.session.merge(row)
                db.session.flush()
                db.session.commit()
                db.session.refresh(row)
                db.session.close()
                message = f"Modified 'Nutanix_Prism_VM' Request_Id = {id}"
                row     = json.loads(row.get_json())
            else:
                code    = API_NOT_FOUND
                message = f"Not found Nutanix_Prism_VM with Request_Id = {id}"
                row     = None
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Nutanix_Prism_VM',entities=[row],name=current_app.config['NAME'])

@main.route('/api/patch/Nutanix_Prism_VM/<int:id>', methods=['PATCH'])
def api_patch_Nutanix_Prism_VM(id):
    code    = API_OK
    message = 'OK'
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            id_counter=0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values = [id]
            row   = Nutanix_Prism_VM()
            query = db.session.query(Nutanix_Prism_VM)
            
            # First loop mandatory for row population ----------------------
            query = query.filter(Nutanix_Prism_VM.Request_Id == id_values[id_counter])
            id_counter += 1
            # --------------------------------------------------------------
            row = query.one_or_none()
            # If row exists then continue:
            if row is not None:
                # Second loop seek for updated fields ----------------------
                if 'project_uuid' in request.json.keys():
                    row.project_uuid = request.json.get('project_uuid')
                if 'category_name' in request.json.keys():
                    row.category_name = request.json.get('category_name')
                if 'cluster_uuid' in request.json.keys():
                    row.cluster_uuid = request.json.get('cluster_uuid')
                if 'vm_name' in request.json.keys():
                    row.vm_name = request.json.get('vm_name')
                if 'power_state' in request.json.keys():
                    row.power_state = request.json.get('power_state')
                if 'vcpus_per_socket' in request.json.keys():
                    row.vcpus_per_socket = request.json.get('vcpus_per_socket')
                if 'num_sockets' in request.json.keys():
                    row.num_sockets = request.json.get('num_sockets')
                if 'memory_size_mib' in request.json.keys():
                    row.memory_size_mib = request.json.get('memory_size_mib')
                if 'memory_size_gib' in request.json.keys():
                    row.memory_size_gib = request.json.get('memory_size_gib')
                if 'Comments' in request.json.keys():
                    row.Comments = request.json.get('Comments')
                if 'vm_ip' in request.json.keys():
                    row.vm_ip = request.json.get('vm_ip')
                if 'subnet_uuid' in request.json.keys():
                    row.subnet_uuid = request.json.get('subnet_uuid')
                if 'vm_username' in request.json.keys():
                    row.vm_username = request.json.get('vm_username')
                if 'vm_password' in request.json.keys():
                    row.vm_password = request.json.get('vm_password')
                if 'backup_set_1' in request.json.keys():
                    row.backup_set_1 = request.json.get('backup_set_1')
                if 'backup_set_2' in request.json.keys():
                    row.backup_set_2 = request.json.get('backup_set_2')
                if 'backup_set_3' in request.json.keys():
                    row.backup_set_3 = request.json.get('backup_set_3')
                if 'disk_type' in request.json.keys():
                    row.disk_type = request.json.get('disk_type')
                if 'disk_0_image' in request.json.keys():
                    row.disk_0_image = request.json.get('disk_0_image')
                if 'disk_0_size' in request.json.keys():
                    row.disk_0_size = request.json.get('disk_0_size')
                if 'disk_1_image' in request.json.keys():
                    row.disk_1_image = request.json.get('disk_1_image')
                if 'disk_1_size' in request.json.keys():
                    row.disk_1_size = request.json.get('disk_1_size')
                if 'disk_2_image' in request.json.keys():
                    row.disk_2_image = request.json.get('disk_2_image')
                if 'disk_2_size' in request.json.keys():
                    row.disk_2_size = request.json.get('disk_2_size')
                if 'disk_3_image' in request.json.keys():
                    row.disk_3_image = request.json.get('disk_3_image')
                if 'disk_3_size' in request.json.keys():
                    row.disk_3_size = request.json.get('disk_3_size')
                if 'disk_4_image' in request.json.keys():
                    row.disk_4_image = request.json.get('disk_4_image')
                if 'disk_4_size' in request.json.keys():
                    row.disk_4_size = request.json.get('disk_4_size')
                if 'disk_5_image' in request.json.keys():
                    row.disk_5_image = request.json.get('disk_5_image')
                if 'disk_5_size' in request.json.keys():
                    row.disk_5_size = request.json.get('disk_5_size')
                if 'disk_6_image' in request.json.keys():
                    row.disk_6_image = request.json.get('disk_6_image')
                if 'disk_6_size' in request.json.keys():
                    row.disk_6_size = request.json.get('disk_6_size')
                if 'disk_7_image' in request.json.keys():
                    row.disk_7_image = request.json.get('disk_7_image')
                if 'disk_7_size' in request.json.keys():
                    row.disk_7_size = request.json.get('disk_7_size')
                if 'disk_8_image' in request.json.keys():
                    row.disk_8_image = request.json.get('disk_8_image')
                if 'disk_8_size' in request.json.keys():
                    row.disk_8_size = request.json.get('disk_8_size')
                if 'disk_9_image' in request.json.keys():
                    row.disk_9_image = request.json.get('disk_9_image')
                if 'disk_9_size' in request.json.keys():
                    row.disk_9_size = request.json.get('disk_9_size')
                if 'disk_10_image' in request.json.keys():
                    row.disk_10_image = request.json.get('disk_10_image')
                if 'disk_10_size' in request.json.keys():
                    row.disk_10_size = request.json.get('disk_10_size')
                if 'disk_11_image' in request.json.keys():
                    row.disk_11_image = request.json.get('disk_11_image')
                if 'disk_11_size' in request.json.keys():
                    row.disk_11_size = request.json.get('disk_11_size')
                # ----------------------------------------------------------
                db.session.merge(row)
                db.session.flush()
                db.session.commit()
                db.session.refresh(row)
                db.session.close()
                message = f"Modified 'Nutanix_Prism_VM' Request_Id = {id}"
                row     = json.loads(row.get_json())
            else:
                code    = API_NOT_FOUND
                message = f"Not found Nutanix_Prism_VM with Request_Id = {id}"
                row     = None
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Nutanix_Prism_VM',entities=[row],name=current_app.config['NAME'])

@main.route('/api/delete/Nutanix_Prism_VM/<int:id>', methods=['DELETE'])
def api_delete_Nutanix_Prism_VM(id):
    code    = API_OK
    message = 'OK'
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            id_counter=0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values = [id]
            row   = Nutanix_Prism_VM()
            query = db.session.query(Nutanix_Prism_VM)
            
            # First loop mandatory for row population ----------------------
            # detected primary key field: c.field
            query       = query.filter(Nutanix_Prism_VM.Request_Id == id_values[id_counter])
            id_counter +=1
            # --------------------------------------------------------------
            row = query.one_or_none()

            if row is not None:
                db.session.delete(row)
                db.session.flush()
                db.session.commit()
                db.session.close()
                message = f"Deleted 'Nutanix_Prism_VM' Request_Id = {id}"
                row     = json.loads(row.get_json())
            else:
                code    = API_NOT_FOUND
                message = f"Not found 'Nutanix_Prism_VM' with Request_Id = {id}"
                row     = None        
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Nutanix_Prism_VM',entities=[],name=current_app.config['NAME'])

# ======================================================================# view_nutanix_vm_images.py_gen_views_api.html.auto

# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2020-11-23 19:59:59.715794
# ======================================================================
# gen_views_api.html:AG 2020-11-23 19:59:59.715808
# table_name: Nutanix_VM_Images
# class_name: nutanix_vm_images
# is shardened: False
# Table 'Nutanix_VM_Images' keys = imageservice_uuid_diskclone
# Errors: None
# PK field found 'imageservice_uuid_diskclone' db.String(45)
# Nutanix_VM_Images id field is 'Nutanix_VM_Images.imageservice_uuid_diskclone' of type ''

@main.route('/api/get/Nutanix_VM_Images'     , methods=['GET'])
@main.route('/api/get/Nutanix_VM_Images/<id>', methods=['GET'])
def api_get_Nutanix_VM_Images(id=None):
    code       = API_OK
    message    = 'OK'
    rows       = None
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            id_counter = 0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values=[id]
            # Codigo para un solo campo de id
            # chequear si marcado explicitamente
            query = db.session.query(Nutanix_VM_Images)
            if id is not None:
                query = query.filter(Nutanix_VM_Images.imageservice_uuid_diskclone == id_values[id_counter])
                rows = query.one_or_none()
            else:
                if request.args is not None and len(request.args):
                    if 'imageservice_uuid_diskclone' in request.args:
                        query = query.filter(Nutanix_VM_Images.imageservice_uuid_diskclone == request.args.get('imageservice_uuid_diskclone'))
                    if 'description' in request.args:
                        query = query.filter(Nutanix_VM_Images.description == request.args.get('description'))
                    if 'size_mib' in request.args:
                        query = query.filter(Nutanix_VM_Images.size_mib == request.args.get('size_mib'))
                    if 'comments' in request.args:
                        query = query.filter(Nutanix_VM_Images.comments == request.args.get('comments'))
                rows = query.all()
            if rows is not None:
                if type(rows) == list:
                    for i in range(len(rows)):
                        rows[i] = json.loads(rows[i].get_json())
                else:
                    rows = [json.loads(rows.get_json())]
            else:
                rows = []
            if len(rows) == 0:
                code = API_NO_DATA
                state = get_api_state(API_NO_DATA)
                
                if id is None:
                    message = f"No 'Nutanix_VM_Images' records found"
                else:
                    message = f"No 'Nutanix_VM_Images.imageservice_uuid_diskclone' = {id} record found"
                
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Nutanix_VM_Images',entities=rows,name=current_app.config['NAME'])

@main.route('/api/post/Nutanix_VM_Images', methods=['POST'])
def api_post_Nutanix_VM_Images():
    code    = API_OK
    message = 'OK'
    row     = None
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            row = Nutanix_VM_Images()
            # Populates row from json, if ID=int:autoincrement then None
            row.imageservice_uuid_diskclone = request.json.get('imageservice_uuid_diskclone',None)
            row.description = request.json.get('description',None)
            row.size_mib = request.json.get('size_mib',None)
            row.comments = request.json.get('comments',None)
            # ----------------------------------------------------------
            db.session.add(row)
            db.session.flush()
            db.session.commit()
            db.session.refresh(row)
            db.session.close()
            message = f"Created 'Nutanix_VM_Images' imageservice_uuid_diskclone = {row.imageservice_uuid_diskclone}"
            row     = json.loads(row.get_json())
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
            row     = None
    else:
        code    = API_ERROR
        message = 'Unauthorized request'            
    return get_api_response(code=code,message=message,kind='Nutanix_VM_Images',entities=[row],name=current_app.config['NAME'])

@main.route('/api/put/Nutanix_VM_Images/<id>', methods=['PUT'])
def api_put_Nutanix_VM_Images(id):
    code    = API_OK
    message = 'OK'
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            id_counter=0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values = [id]
            row   = Nutanix_VM_Images()
            query = db.session.query(Nutanix_VM_Images)
            
            # First loop mandatory for row population ----------------------
            query = query.filter(Nutanix_VM_Images.imageservice_uuid_diskclone == id_values[id_counter])
            id_counter += 1
            # --------------------------------------------------------------
            row = query.one_or_none()
            # If row exists then continue:
            if row is not None:
                # Second loop seek for updated fields ----------------------
                if 'description' in request.json.keys():
                    row.description = request.json.get('description')
                if 'size_mib' in request.json.keys():
                    row.size_mib = request.json.get('size_mib')
                if 'comments' in request.json.keys():
                    row.comments = request.json.get('comments')
                # ----------------------------------------------------------
                db.session.merge(row)
                db.session.flush()
                db.session.commit()
                db.session.refresh(row)
                db.session.close()
                message = f"Modified 'Nutanix_VM_Images' imageservice_uuid_diskclone = {id}"
                row     = json.loads(row.get_json())
            else:
                code    = API_NOT_FOUND
                message = f"Not found Nutanix_VM_Images with imageservice_uuid_diskclone = {id}"
                row     = None
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Nutanix_VM_Images',entities=[row],name=current_app.config['NAME'])

@main.route('/api/patch/Nutanix_VM_Images/<id>', methods=['PATCH'])
def api_patch_Nutanix_VM_Images(id):
    code    = API_OK
    message = 'OK'
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            id_counter=0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values = [id]
            row   = Nutanix_VM_Images()
            query = db.session.query(Nutanix_VM_Images)
            
            # First loop mandatory for row population ----------------------
            query = query.filter(Nutanix_VM_Images.imageservice_uuid_diskclone == id_values[id_counter])
            id_counter += 1
            # --------------------------------------------------------------
            row = query.one_or_none()
            # If row exists then continue:
            if row is not None:
                # Second loop seek for updated fields ----------------------
                if 'description' in request.json.keys():
                    row.description = request.json.get('description')
                if 'size_mib' in request.json.keys():
                    row.size_mib = request.json.get('size_mib')
                if 'comments' in request.json.keys():
                    row.comments = request.json.get('comments')
                # ----------------------------------------------------------
                db.session.merge(row)
                db.session.flush()
                db.session.commit()
                db.session.refresh(row)
                db.session.close()
                message = f"Modified 'Nutanix_VM_Images' imageservice_uuid_diskclone = {id}"
                row     = json.loads(row.get_json())
            else:
                code    = API_NOT_FOUND
                message = f"Not found Nutanix_VM_Images with imageservice_uuid_diskclone = {id}"
                row     = None
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Nutanix_VM_Images',entities=[row],name=current_app.config['NAME'])

@main.route('/api/delete/Nutanix_VM_Images/<id>', methods=['DELETE'])
def api_delete_Nutanix_VM_Images(id):
    code    = API_OK
    message = 'OK'
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            id_counter=0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values = [id]
            row   = Nutanix_VM_Images()
            query = db.session.query(Nutanix_VM_Images)
            
            # First loop mandatory for row population ----------------------
            # detected primary key field: c.field
            query       = query.filter(Nutanix_VM_Images.imageservice_uuid_diskclone == id_values[id_counter])
            id_counter +=1
            # --------------------------------------------------------------
            row = query.one_or_none()

            if row is not None:
                db.session.delete(row)
                db.session.flush()
                db.session.commit()
                db.session.close()
                message = f"Deleted 'Nutanix_VM_Images' imageservice_uuid_diskclone = {id}"
                row     = json.loads(row.get_json())
            else:
                code    = API_NOT_FOUND
                message = f"Not found 'Nutanix_VM_Images' with imageservice_uuid_diskclone = {id}"
                row     = None        
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Nutanix_VM_Images',entities=[],name=current_app.config['NAME'])

# ======================================================================# view_projects.py_gen_views_api.html.auto

# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2020-11-23 19:59:59.873022
# ======================================================================
# gen_views_api.html:AG 2020-11-23 19:59:59.873037
# table_name: Projects
# class_name: projects
# is shardened: False
# Table 'Projects' keys = project_uuid
# Errors: None
# PK field found 'project_uuid' db.String(45)
# Projects id field is 'Projects.project_uuid' of type ''

@main.route('/api/get/Projects'     , methods=['GET'])
@main.route('/api/get/Projects/<id>', methods=['GET'])
def api_get_Projects(id=None):
    code       = API_OK
    message    = 'OK'
    rows       = None
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            id_counter = 0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values=[id]
            # Codigo para un solo campo de id
            # chequear si marcado explicitamente
            query = db.session.query(Projects)
            if id is not None:
                query = query.filter(Projects.project_uuid == id_values[id_counter])
                rows = query.one_or_none()
            else:
                if request.args is not None and len(request.args):
                    if 'project_uuid' in request.args:
                        query = query.filter(Projects.project_uuid == request.args.get('project_uuid'))
                    if 'project_name' in request.args:
                        query = query.filter(Projects.project_name == request.args.get('project_name'))
                rows = query.all()
            if rows is not None:
                if type(rows) == list:
                    for i in range(len(rows)):
                        rows[i] = json.loads(rows[i].get_json())
                else:
                    rows = [json.loads(rows.get_json())]
            else:
                rows = []
            if len(rows) == 0:
                code = API_NO_DATA
                state = get_api_state(API_NO_DATA)
                
                if id is None:
                    message = f"No 'Projects' records found"
                else:
                    message = f"No 'Projects.project_uuid' = {id} record found"
                
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Projects',entities=rows,name=current_app.config['NAME'])

@main.route('/api/post/Projects', methods=['POST'])
def api_post_Projects():
    code    = API_OK
    message = 'OK'
    row     = None
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            row = Projects()
            # Populates row from json, if ID=int:autoincrement then None
            row.project_uuid = request.json.get('project_uuid',None)
            row.project_name = request.json.get('project_name',None)
            # ----------------------------------------------------------
            db.session.add(row)
            db.session.flush()
            db.session.commit()
            db.session.refresh(row)
            db.session.close()
            message = f"Created 'Projects' project_uuid = {row.project_uuid}"
            row     = json.loads(row.get_json())
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
            row     = None
    else:
        code    = API_ERROR
        message = 'Unauthorized request'            
    return get_api_response(code=code,message=message,kind='Projects',entities=[row],name=current_app.config['NAME'])

@main.route('/api/put/Projects/<id>', methods=['PUT'])
def api_put_Projects(id):
    code    = API_OK
    message = 'OK'
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            id_counter=0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values = [id]
            row   = Projects()
            query = db.session.query(Projects)
            
            # First loop mandatory for row population ----------------------
            query = query.filter(Projects.project_uuid == id_values[id_counter])
            id_counter += 1
            # --------------------------------------------------------------
            row = query.one_or_none()
            # If row exists then continue:
            if row is not None:
                # Second loop seek for updated fields ----------------------
                if 'project_name' in request.json.keys():
                    row.project_name = request.json.get('project_name')
                # ----------------------------------------------------------
                db.session.merge(row)
                db.session.flush()
                db.session.commit()
                db.session.refresh(row)
                db.session.close()
                message = f"Modified 'Projects' project_uuid = {id}"
                row     = json.loads(row.get_json())
            else:
                code    = API_NOT_FOUND
                message = f"Not found Projects with project_uuid = {id}"
                row     = None
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Projects',entities=[row],name=current_app.config['NAME'])

@main.route('/api/patch/Projects/<id>', methods=['PATCH'])
def api_patch_Projects(id):
    code    = API_OK
    message = 'OK'
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            id_counter=0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values = [id]
            row   = Projects()
            query = db.session.query(Projects)
            
            # First loop mandatory for row population ----------------------
            query = query.filter(Projects.project_uuid == id_values[id_counter])
            id_counter += 1
            # --------------------------------------------------------------
            row = query.one_or_none()
            # If row exists then continue:
            if row is not None:
                # Second loop seek for updated fields ----------------------
                if 'project_name' in request.json.keys():
                    row.project_name = request.json.get('project_name')
                # ----------------------------------------------------------
                db.session.merge(row)
                db.session.flush()
                db.session.commit()
                db.session.refresh(row)
                db.session.close()
                message = f"Modified 'Projects' project_uuid = {id}"
                row     = json.loads(row.get_json())
            else:
                code    = API_NOT_FOUND
                message = f"Not found Projects with project_uuid = {id}"
                row     = None
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Projects',entities=[row],name=current_app.config['NAME'])

@main.route('/api/delete/Projects/<id>', methods=['DELETE'])
def api_delete_Projects(id):
    code    = API_OK
    message = 'OK'
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            id_counter=0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values = [id]
            row   = Projects()
            query = db.session.query(Projects)
            
            # First loop mandatory for row population ----------------------
            # detected primary key field: c.field
            query       = query.filter(Projects.project_uuid == id_values[id_counter])
            id_counter +=1
            # --------------------------------------------------------------
            row = query.one_or_none()

            if row is not None:
                db.session.delete(row)
                db.session.flush()
                db.session.commit()
                db.session.close()
                message = f"Deleted 'Projects' project_uuid = {id}"
                row     = json.loads(row.get_json())
            else:
                code    = API_NOT_FOUND
                message = f"Not found 'Projects' with project_uuid = {id}"
                row     = None        
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Projects',entities=[],name=current_app.config['NAME'])

# ======================================================================# view_rates.py_gen_views_api.html.auto

# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2020-11-23 20:00:00.063194
# ======================================================================
# gen_views_api.html:AG 2020-11-23 20:00:00.063210
# table_name: Rates
# class_name: rates
# is shardened: True
# Table 'Rates' keys = Rat_Id
# Errors: None
# ID field found 'Rat_Id' auto_increment db.Integer
# Rates id field is 'Rates.Rat_Id' of type 'int:'

@main.route('/api/get/Rates'     , methods=['GET'])
@main.route('/api/get/Rates/<int:id>', methods=['GET'])
def api_get_Rates(id=None):
    code       = API_OK
    message    = 'OK'
    rows       = None
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            id_counter = 0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values=[id]
            # Codigo para un solo campo de id
            # chequear si marcado explicitamente
            query = db.session.query(Rates)
            if id is not None:
                query = query.filter(Rates.Rat_Id == id_values[id_counter])
                rows = query.one_or_none()
            else:
                if request.args is not None and len(request.args):
                    if 'Rat_Id' in request.args:
                        query = query.filter(Rates.Rat_Id == request.args.get('Rat_Id'))
                    if 'Typ_Code' in request.args:
                        query = query.filter(Rates.Typ_Code == request.args.get('Typ_Code'))
                    if 'Cus_Id' in request.args:
                        query = query.filter(Rates.Cus_Id == request.args.get('Cus_Id'))
                    if 'Pla_Id' in request.args:
                        query = query.filter(Rates.Pla_Id == request.args.get('Pla_Id'))
                    if 'CC_Id' in request.args:
                        query = query.filter(Rates.CC_Id == request.args.get('CC_Id'))
                    if 'CI_Id' in request.args:
                        query = query.filter(Rates.CI_Id == request.args.get('CI_Id'))
                    if 'Rat_Price' in request.args:
                        query = query.filter(Rates.Rat_Price == request.args.get('Rat_Price'))
                    if 'Cur_Code' in request.args:
                        query = query.filter(Rates.Cur_Code == request.args.get('Cur_Code'))
                    if 'MU_Code' in request.args:
                        query = query.filter(Rates.MU_Code == request.args.get('MU_Code'))
                    if 'Rat_Period' in request.args:
                        query = query.filter(Rates.Rat_Period == request.args.get('Rat_Period'))
                    if 'Rat_Type' in request.args:
                        query = query.filter(Rates.Rat_Type == request.args.get('Rat_Type'))
                rows = query.all()
            if rows is not None:
                if type(rows) == list:
                    for i in range(len(rows)):
                        rows[i] = json.loads(rows[i].get_json())
                else:
                    rows = [json.loads(rows.get_json())]
            else:
                rows = []
            if len(rows) == 0:
                code = API_NO_DATA
                state = get_api_state(API_NO_DATA)
                
                if id is None:
                    message = f"No 'Rates' records found"
                else:
                    message = f"No 'Rates.Rat_Id' = {id} record found"
                
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Rates',entities=rows,name=current_app.config['NAME'])

@main.route('/api/post/Rates', methods=['POST'])
def api_post_Rates():
    code    = API_OK
    message = 'OK'
    row     = None
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            row = Rates()
            # Populates row from json, if ID=int:autoincrement then None
            row.Rat_Id = None
            row.Typ_Code = request.json.get('Typ_Code',None)
            row.Cus_Id = request.json.get('Cus_Id',None)
            row.Pla_Id = request.json.get('Pla_Id',None)
            row.CC_Id = request.json.get('CC_Id',None)
            row.CI_Id = request.json.get('CI_Id',None)
            row.Rat_Price = request.json.get('Rat_Price',None)
            row.Cur_Code = request.json.get('Cur_Code',None)
            row.MU_Code = request.json.get('MU_Code',None)
            row.Rat_Period = request.json.get('Rat_Period',None)
            row.Rat_Type = request.json.get('Rat_Type',None)
            # ----------------------------------------------------------
            db.session.add(row)
            db.session.flush()
            db.session.commit()
            db.session.refresh(row)
            db.session.close()
            message = f"Created 'Rates' Rat_Id = {row.Rat_Id}"
            row     = json.loads(row.get_json())
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
            row     = None
    else:
        code    = API_ERROR
        message = 'Unauthorized request'            
    return get_api_response(code=code,message=message,kind='Rates',entities=[row],name=current_app.config['NAME'])

@main.route('/api/put/Rates/<int:id>', methods=['PUT'])
def api_put_Rates(id):
    code    = API_OK
    message = 'OK'
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            id_counter=0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values = [id]
            row   = Rates()
            query = db.session.query(Rates)
            
            # First loop mandatory for row population ----------------------
            query = query.filter(Rates.Rat_Id == id_values[id_counter])
            id_counter += 1
            # --------------------------------------------------------------
            row = query.one_or_none()
            # If row exists then continue:
            if row is not None:
                # Second loop seek for updated fields ----------------------
                if 'Typ_Code' in request.json.keys():
                    row.Typ_Code = request.json.get('Typ_Code')
                if 'Cus_Id' in request.json.keys():
                    row.Cus_Id = request.json.get('Cus_Id')
                if 'Pla_Id' in request.json.keys():
                    row.Pla_Id = request.json.get('Pla_Id')
                if 'CC_Id' in request.json.keys():
                    row.CC_Id = request.json.get('CC_Id')
                if 'CI_Id' in request.json.keys():
                    row.CI_Id = request.json.get('CI_Id')
                if 'Rat_Price' in request.json.keys():
                    row.Rat_Price = request.json.get('Rat_Price')
                if 'Cur_Code' in request.json.keys():
                    row.Cur_Code = request.json.get('Cur_Code')
                if 'MU_Code' in request.json.keys():
                    row.MU_Code = request.json.get('MU_Code')
                if 'Rat_Period' in request.json.keys():
                    row.Rat_Period = request.json.get('Rat_Period')
                if 'Rat_Type' in request.json.keys():
                    row.Rat_Type = request.json.get('Rat_Type')
                # ----------------------------------------------------------
                db.session.merge(row)
                db.session.flush()
                db.session.commit()
                db.session.refresh(row)
                db.session.close()
                message = f"Modified 'Rates' Rat_Id = {id}"
                row     = json.loads(row.get_json())
            else:
                code    = API_NOT_FOUND
                message = f"Not found Rates with Rat_Id = {id}"
                row     = None
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Rates',entities=[row],name=current_app.config['NAME'])

@main.route('/api/patch/Rates/<int:id>', methods=['PATCH'])
def api_patch_Rates(id):
    code    = API_OK
    message = 'OK'
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            id_counter=0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values = [id]
            row   = Rates()
            query = db.session.query(Rates)
            
            # First loop mandatory for row population ----------------------
            query = query.filter(Rates.Rat_Id == id_values[id_counter])
            id_counter += 1
            # --------------------------------------------------------------
            row = query.one_or_none()
            # If row exists then continue:
            if row is not None:
                # Second loop seek for updated fields ----------------------
                if 'Typ_Code' in request.json.keys():
                    row.Typ_Code = request.json.get('Typ_Code')
                if 'Cus_Id' in request.json.keys():
                    row.Cus_Id = request.json.get('Cus_Id')
                if 'Pla_Id' in request.json.keys():
                    row.Pla_Id = request.json.get('Pla_Id')
                if 'CC_Id' in request.json.keys():
                    row.CC_Id = request.json.get('CC_Id')
                if 'CI_Id' in request.json.keys():
                    row.CI_Id = request.json.get('CI_Id')
                if 'Rat_Price' in request.json.keys():
                    row.Rat_Price = request.json.get('Rat_Price')
                if 'Cur_Code' in request.json.keys():
                    row.Cur_Code = request.json.get('Cur_Code')
                if 'MU_Code' in request.json.keys():
                    row.MU_Code = request.json.get('MU_Code')
                if 'Rat_Period' in request.json.keys():
                    row.Rat_Period = request.json.get('Rat_Period')
                if 'Rat_Type' in request.json.keys():
                    row.Rat_Type = request.json.get('Rat_Type')
                # ----------------------------------------------------------
                db.session.merge(row)
                db.session.flush()
                db.session.commit()
                db.session.refresh(row)
                db.session.close()
                message = f"Modified 'Rates' Rat_Id = {id}"
                row     = json.loads(row.get_json())
            else:
                code    = API_NOT_FOUND
                message = f"Not found Rates with Rat_Id = {id}"
                row     = None
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Rates',entities=[row],name=current_app.config['NAME'])

@main.route('/api/delete/Rates/<int:id>', methods=['DELETE'])
def api_delete_Rates(id):
    code    = API_OK
    message = 'OK'
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            id_counter=0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values = [id]
            row   = Rates()
            query = db.session.query(Rates)
            
            # First loop mandatory for row population ----------------------
            query = query.filter(Rates.Rat_Id == id)
            # --------------------------------------------------------------
            row = query.one_or_none()

            if row is not None:
                db.session.delete(row)
                db.session.flush()
                db.session.commit()
                db.session.close()
                message = f"Deleted 'Rates' Rat_Id = {id}"
                row     = json.loads(row.get_json())
            else:
                code    = API_NOT_FOUND
                message = f"Not found 'Rates' with Rat_Id = {id}"
                row     = None        
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Rates',entities=[],name=current_app.config['NAME'])

# ======================================================================# view_requests.py_gen_views_api.html.auto

# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2020-11-23 20:00:00.414724
# ======================================================================
# gen_views_api.html:AG 2020-11-23 20:00:00.414741
# table_name: Requests
# class_name: requests
# is shardened: False
# Table 'Requests' keys = Id
# Errors: None
# ID field found 'Id' auto_increment db.Integer
# Requests id field is 'Requests.Id' of type 'int:'

@main.route('/api/get/Requests'     , methods=['GET'])
@main.route('/api/get/Requests/<int:id>', methods=['GET'])
def api_get_Requests(id=None):
    code       = API_OK
    message    = 'OK'
    rows       = None
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            id_counter = 0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values=[id]
            # Codigo para un solo campo de id
            # chequear si marcado explicitamente
            query = db.session.query(Requests)
            if id is not None:
                query = query.filter(Requests.Id == id_values[id_counter])
                rows = query.one_or_none()
            else:
                if request.args is not None and len(request.args):
                    if 'Id' in request.args:
                        query = query.filter(Requests.Id == request.args.get('Id'))
                    if 'Type' in request.args:
                        query = query.filter(Requests.Type == request.args.get('Type'))
                    if 'User_Id' in request.args:
                        query = query.filter(Requests.User_Id == request.args.get('User_Id'))
                    if 'Approver_Id' in request.args:
                        query = query.filter(Requests.Approver_Id == request.args.get('Approver_Id'))
                    if 'Status' in request.args:
                        query = query.filter(Requests.Status == request.args.get('Status'))
                    if 'Creation_Time' in request.args:
                        query = query.filter(Requests.Creation_Time == request.args.get('Creation_Time'))
                    if 'Last_Status_Time' in request.args:
                        query = query.filter(Requests.Last_Status_Time == request.args.get('Last_Status_Time'))
                    if 'Comments' in request.args:
                        query = query.filter(Requests.Comments == request.args.get('Comments'))
                    if 'Task_uuid' in request.args:
                        query = query.filter(Requests.Task_uuid == request.args.get('Task_uuid'))
                    if 'Task_status' in request.args:
                        query = query.filter(Requests.Task_status == request.args.get('Task_status'))
                    if 'CC_Id' in request.args:
                        query = query.filter(Requests.CC_Id == request.args.get('CC_Id'))
                rows = query.all()
            if rows is not None:
                if type(rows) == list:
                    for i in range(len(rows)):
                        rows[i] = json.loads(rows[i].get_json())
                else:
                    rows = [json.loads(rows.get_json())]
            else:
                rows = []
            if len(rows) == 0:
                code = API_NO_DATA
                state = get_api_state(API_NO_DATA)
                
                if id is None:
                    message = f"No 'Requests' records found"
                else:
                    message = f"No 'Requests.Id' = {id} record found"
                
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Requests',entities=rows,name=current_app.config['NAME'])

@main.route('/api/post/Requests', methods=['POST'])
def api_post_Requests():
    code    = API_OK
    message = 'OK'
    row     = None
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            row = Requests()
            # Populates row from json, if ID=int:autoincrement then None
            row.Id = None
            row.Type = request.json.get('Type',1)
            row.User_Id = request.json.get('User_Id',None)
            row.Approver_Id = request.json.get('Approver_Id',None)
            row.Status = request.json.get('Status',0)
            row.Creation_Time = request.json.get('Creation_Time',None)
            row.Last_Status_Time = request.json.get('Last_Status_Time',None)
            row.Comments = request.json.get('Comments',None)
            row.Task_uuid = request.json.get('Task_uuid',None)
            row.Task_status = request.json.get('Task_status',None)
            row.CC_Id = request.json.get('CC_Id',None)
            # ----------------------------------------------------------
            db.session.add(row)
            db.session.flush()
            db.session.commit()
            db.session.refresh(row)
            db.session.close()
            message = f"Created 'Requests' Id = {row.Id}"
            row     = json.loads(row.get_json())
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
            row     = None
    else:
        code    = API_ERROR
        message = 'Unauthorized request'            
    return get_api_response(code=code,message=message,kind='Requests',entities=[row],name=current_app.config['NAME'])

@main.route('/api/put/Requests/<int:id>', methods=['PUT'])
def api_put_Requests(id):
    code    = API_OK
    message = 'OK'
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            id_counter=0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values = [id]
            row   = Requests()
            query = db.session.query(Requests)
            
            # First loop mandatory for row population ----------------------
            query = query.filter(Requests.Id == id_values[id_counter])
            id_counter += 1
            # --------------------------------------------------------------
            row = query.one_or_none()
            # If row exists then continue:
            if row is not None:
                # Second loop seek for updated fields ----------------------
                if 'Type' in request.json.keys():
                    row.Type = request.json.get('Type')
                if 'User_Id' in request.json.keys():
                    row.User_Id = request.json.get('User_Id')
                if 'Approver_Id' in request.json.keys():
                    row.Approver_Id = request.json.get('Approver_Id')
                if 'Status' in request.json.keys():
                    row.Status = request.json.get('Status')
                if 'Creation_Time' in request.json.keys():
                    row.Creation_Time = request.json.get('Creation_Time')
                if 'Last_Status_Time' in request.json.keys():
                    row.Last_Status_Time = request.json.get('Last_Status_Time')
                if 'Comments' in request.json.keys():
                    row.Comments = request.json.get('Comments')
                if 'Task_uuid' in request.json.keys():
                    row.Task_uuid = request.json.get('Task_uuid')
                if 'Task_status' in request.json.keys():
                    row.Task_status = request.json.get('Task_status')
                if 'CC_Id' in request.json.keys():
                    row.CC_Id = request.json.get('CC_Id')
                # ----------------------------------------------------------
                db.session.merge(row)
                db.session.flush()
                db.session.commit()
                db.session.refresh(row)
                db.session.close()
                message = f"Modified 'Requests' Id = {id}"
                row     = json.loads(row.get_json())
            else:
                code    = API_NOT_FOUND
                message = f"Not found Requests with Id = {id}"
                row     = None
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Requests',entities=[row],name=current_app.config['NAME'])

@main.route('/api/patch/Requests/<int:id>', methods=['PATCH'])
def api_patch_Requests(id):
    code    = API_OK
    message = 'OK'
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            id_counter=0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values = [id]
            row   = Requests()
            query = db.session.query(Requests)
            
            # First loop mandatory for row population ----------------------
            query = query.filter(Requests.Id == id_values[id_counter])
            id_counter += 1
            # --------------------------------------------------------------
            row = query.one_or_none()
            # If row exists then continue:
            if row is not None:
                # Second loop seek for updated fields ----------------------
                if 'Type' in request.json.keys():
                    row.Type = request.json.get('Type')
                if 'User_Id' in request.json.keys():
                    row.User_Id = request.json.get('User_Id')
                if 'Approver_Id' in request.json.keys():
                    row.Approver_Id = request.json.get('Approver_Id')
                if 'Status' in request.json.keys():
                    row.Status = request.json.get('Status')
                if 'Creation_Time' in request.json.keys():
                    row.Creation_Time = request.json.get('Creation_Time')
                if 'Last_Status_Time' in request.json.keys():
                    row.Last_Status_Time = request.json.get('Last_Status_Time')
                if 'Comments' in request.json.keys():
                    row.Comments = request.json.get('Comments')
                if 'Task_uuid' in request.json.keys():
                    row.Task_uuid = request.json.get('Task_uuid')
                if 'Task_status' in request.json.keys():
                    row.Task_status = request.json.get('Task_status')
                if 'CC_Id' in request.json.keys():
                    row.CC_Id = request.json.get('CC_Id')
                # ----------------------------------------------------------
                db.session.merge(row)
                db.session.flush()
                db.session.commit()
                db.session.refresh(row)
                db.session.close()
                message = f"Modified 'Requests' Id = {id}"
                row     = json.loads(row.get_json())
            else:
                code    = API_NOT_FOUND
                message = f"Not found Requests with Id = {id}"
                row     = None
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Requests',entities=[row],name=current_app.config['NAME'])

@main.route('/api/delete/Requests/<int:id>', methods=['DELETE'])
def api_delete_Requests(id):
    code    = API_OK
    message = 'OK'
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            id_counter=0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values = [id]
            row   = Requests()
            query = db.session.query(Requests)
            
            # First loop mandatory for row population ----------------------
            query = query.filter(Requests.Id == id)
            # --------------------------------------------------------------
            row = query.one_or_none()

            if row is not None:
                db.session.delete(row)
                db.session.flush()
                db.session.commit()
                db.session.close()
                message = f"Deleted 'Requests' Id = {id}"
                row     = json.loads(row.get_json())
            else:
                code    = API_NOT_FOUND
                message = f"Not found 'Requests' with Id = {id}"
                row     = None        
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Requests',entities=[],name=current_app.config['NAME'])

# ======================================================================# view_request_type.py_gen_views_api.html.auto

# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2020-11-23 20:00:00.237940
# ======================================================================
# gen_views_api.html:AG 2020-11-23 20:00:00.237955
# table_name: Request_Type
# class_name: request_type
# is shardened: False
# Table 'Request_Type' keys = Id
# Errors: None
# PK field found 'Id' db.Integer
# Request_Type id field is 'Request_Type.Id' of type 'int:'

@main.route('/api/get/Request_Type'     , methods=['GET'])
@main.route('/api/get/Request_Type/<int:id>', methods=['GET'])
def api_get_Request_Type(id=None):
    code       = API_OK
    message    = 'OK'
    rows       = None
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            id_counter = 0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values=[id]
            # Codigo para un solo campo de id
            # chequear si marcado explicitamente
            query = db.session.query(Request_Type)
            if id is not None:
                query = query.filter(Request_Type.Id == id_values[id_counter])
                rows = query.one_or_none()
            else:
                if request.args is not None and len(request.args):
                    if 'Id' in request.args:
                        query = query.filter(Request_Type.Id == request.args.get('Id'))
                    if 'Description' in request.args:
                        query = query.filter(Request_Type.Description == request.args.get('Description'))
                    if 'Table_Name' in request.args:
                        query = query.filter(Request_Type.Table_Name == request.args.get('Table_Name'))
                rows = query.all()
            if rows is not None:
                if type(rows) == list:
                    for i in range(len(rows)):
                        rows[i] = json.loads(rows[i].get_json())
                else:
                    rows = [json.loads(rows.get_json())]
            else:
                rows = []
            if len(rows) == 0:
                code = API_NO_DATA
                state = get_api_state(API_NO_DATA)
                
                if id is None:
                    message = f"No 'Request_Type' records found"
                else:
                    message = f"No 'Request_Type.Id' = {id} record found"
                
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Request_Type',entities=rows,name=current_app.config['NAME'])

@main.route('/api/post/Request_Type', methods=['POST'])
def api_post_Request_Type():
    code    = API_OK
    message = 'OK'
    row     = None
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            row = Request_Type()
            # Populates row from json, if ID=int:autoincrement then None
            row.Id = request.json.get('Id',None)
            row.Description = request.json.get('Description',None)
            row.Table_Name = request.json.get('Table_Name',None)
            # ----------------------------------------------------------
            db.session.add(row)
            db.session.flush()
            db.session.commit()
            db.session.refresh(row)
            db.session.close()
            message = f"Created 'Request_Type' Id = {row.Id}"
            row     = json.loads(row.get_json())
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
            row     = None
    else:
        code    = API_ERROR
        message = 'Unauthorized request'            
    return get_api_response(code=code,message=message,kind='Request_Type',entities=[row],name=current_app.config['NAME'])

@main.route('/api/put/Request_Type/<int:id>', methods=['PUT'])
def api_put_Request_Type(id):
    code    = API_OK
    message = 'OK'
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            id_counter=0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values = [id]
            row   = Request_Type()
            query = db.session.query(Request_Type)
            
            # First loop mandatory for row population ----------------------
            query = query.filter(Request_Type.Id == id_values[id_counter])
            id_counter += 1
            # --------------------------------------------------------------
            row = query.one_or_none()
            # If row exists then continue:
            if row is not None:
                # Second loop seek for updated fields ----------------------
                if 'Description' in request.json.keys():
                    row.Description = request.json.get('Description')
                if 'Table_Name' in request.json.keys():
                    row.Table_Name = request.json.get('Table_Name')
                # ----------------------------------------------------------
                db.session.merge(row)
                db.session.flush()
                db.session.commit()
                db.session.refresh(row)
                db.session.close()
                message = f"Modified 'Request_Type' Id = {id}"
                row     = json.loads(row.get_json())
            else:
                code    = API_NOT_FOUND
                message = f"Not found Request_Type with Id = {id}"
                row     = None
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Request_Type',entities=[row],name=current_app.config['NAME'])

@main.route('/api/patch/Request_Type/<int:id>', methods=['PATCH'])
def api_patch_Request_Type(id):
    code    = API_OK
    message = 'OK'
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            id_counter=0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values = [id]
            row   = Request_Type()
            query = db.session.query(Request_Type)
            
            # First loop mandatory for row population ----------------------
            query = query.filter(Request_Type.Id == id_values[id_counter])
            id_counter += 1
            # --------------------------------------------------------------
            row = query.one_or_none()
            # If row exists then continue:
            if row is not None:
                # Second loop seek for updated fields ----------------------
                if 'Description' in request.json.keys():
                    row.Description = request.json.get('Description')
                if 'Table_Name' in request.json.keys():
                    row.Table_Name = request.json.get('Table_Name')
                # ----------------------------------------------------------
                db.session.merge(row)
                db.session.flush()
                db.session.commit()
                db.session.refresh(row)
                db.session.close()
                message = f"Modified 'Request_Type' Id = {id}"
                row     = json.loads(row.get_json())
            else:
                code    = API_NOT_FOUND
                message = f"Not found Request_Type with Id = {id}"
                row     = None
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Request_Type',entities=[row],name=current_app.config['NAME'])

@main.route('/api/delete/Request_Type/<int:id>', methods=['DELETE'])
def api_delete_Request_Type(id):
    code    = API_OK
    message = 'OK'
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            id_counter=0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values = [id]
            row   = Request_Type()
            query = db.session.query(Request_Type)
            
            # First loop mandatory for row population ----------------------
            # detected primary key field: c.field
            query       = query.filter(Request_Type.Id == id_values[id_counter])
            id_counter +=1
            # --------------------------------------------------------------
            row = query.one_or_none()

            if row is not None:
                db.session.delete(row)
                db.session.flush()
                db.session.commit()
                db.session.close()
                message = f"Deleted 'Request_Type' Id = {id}"
                row     = json.loads(row.get_json())
            else:
                code    = API_NOT_FOUND
                message = f"Not found 'Request_Type' with Id = {id}"
                row     = None        
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Request_Type',entities=[],name=current_app.config['NAME'])

# ======================================================================# view_roles.py_gen_views_api.html.auto

# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2020-11-23 20:00:00.571665
# ======================================================================
# gen_views_api.html:AG 2020-11-23 20:00:00.571683
# table_name: Roles
# class_name: Role
# is shardened: False
# Table 'Roles' keys = id
# Errors: None
# PK field found 'id' db.Integer
# Roles id field is 'Roles.id' of type 'int:'

@main.route('/api/get/Roles'     , methods=['GET'])
@main.route('/api/get/Roles/<int:id>', methods=['GET'])
def api_get_Roles(id=None):
    code       = API_OK
    message    = 'OK'
    rows       = None
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            id_counter = 0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values=[id]
            # Codigo para un solo campo de id
            # chequear si marcado explicitamente
            query = db.session.query(Roles)
            if id is not None:
                query = query.filter(Roles.id == id_values[id_counter])
                rows = query.one_or_none()
            else:
                if request.args is not None and len(request.args):
                    if 'id' in request.args:
                        query = query.filter(Roles.id == request.args.get('id'))
                    if 'name' in request.args:
                        query = query.filter(Roles.name == request.args.get('name'))
                    if 'default' in request.args:
                        query = query.filter(Roles.default == request.args.get('default'))
                    if 'permissions' in request.args:
                        query = query.filter(Roles.permissions == request.args.get('permissions'))
                rows = query.all()
            if rows is not None:
                if type(rows) == list:
                    for i in range(len(rows)):
                        rows[i] = json.loads(rows[i].get_json())
                else:
                    rows = [json.loads(rows.get_json())]
            else:
                rows = []
            if len(rows) == 0:
                code = API_NO_DATA
                state = get_api_state(API_NO_DATA)
                
                if id is None:
                    message = f"No 'Roles' records found"
                else:
                    message = f"No 'Roles.id' = {id} record found"
                
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Roles',entities=rows,name=current_app.config['NAME'])

@main.route('/api/post/Roles', methods=['POST'])
def api_post_Roles():
    code    = API_OK
    message = 'OK'
    row     = None
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            row = Roles()
            # Populates row from json, if ID=int:autoincrement then None
            row.id = request.json.get('id',None)
            row.name = request.json.get('name',None)
            row.default = request.json.get('default',None)
            row.permissions = request.json.get('permissions',None)
            # ----------------------------------------------------------
            db.session.add(row)
            db.session.flush()
            db.session.commit()
            db.session.refresh(row)
            db.session.close()
            message = f"Created 'Roles' id = {row.id}"
            row     = json.loads(row.get_json())
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
            row     = None
    else:
        code    = API_ERROR
        message = 'Unauthorized request'            
    return get_api_response(code=code,message=message,kind='Roles',entities=[row],name=current_app.config['NAME'])

@main.route('/api/put/Roles/<int:id>', methods=['PUT'])
def api_put_Roles(id):
    code    = API_OK
    message = 'OK'
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            id_counter=0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values = [id]
            row   = Roles()
            query = db.session.query(Roles)
            
            # First loop mandatory for row population ----------------------
            query = query.filter(Roles.id == id_values[id_counter])
            id_counter += 1
            # --------------------------------------------------------------
            row = query.one_or_none()
            # If row exists then continue:
            if row is not None:
                # Second loop seek for updated fields ----------------------
                if 'name' in request.json.keys():
                    row.name = request.json.get('name')
                if 'default' in request.json.keys():
                    row.default = request.json.get('default')
                if 'permissions' in request.json.keys():
                    row.permissions = request.json.get('permissions')
                # ----------------------------------------------------------
                db.session.merge(row)
                db.session.flush()
                db.session.commit()
                db.session.refresh(row)
                db.session.close()
                message = f"Modified 'Roles' id = {id}"
                row     = json.loads(row.get_json())
            else:
                code    = API_NOT_FOUND
                message = f"Not found Roles with id = {id}"
                row     = None
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Roles',entities=[row],name=current_app.config['NAME'])

@main.route('/api/patch/Roles/<int:id>', methods=['PATCH'])
def api_patch_Roles(id):
    code    = API_OK
    message = 'OK'
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            id_counter=0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values = [id]
            row   = Roles()
            query = db.session.query(Roles)
            
            # First loop mandatory for row population ----------------------
            query = query.filter(Roles.id == id_values[id_counter])
            id_counter += 1
            # --------------------------------------------------------------
            row = query.one_or_none()
            # If row exists then continue:
            if row is not None:
                # Second loop seek for updated fields ----------------------
                if 'name' in request.json.keys():
                    row.name = request.json.get('name')
                if 'default' in request.json.keys():
                    row.default = request.json.get('default')
                if 'permissions' in request.json.keys():
                    row.permissions = request.json.get('permissions')
                # ----------------------------------------------------------
                db.session.merge(row)
                db.session.flush()
                db.session.commit()
                db.session.refresh(row)
                db.session.close()
                message = f"Modified 'Roles' id = {id}"
                row     = json.loads(row.get_json())
            else:
                code    = API_NOT_FOUND
                message = f"Not found Roles with id = {id}"
                row     = None
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Roles',entities=[row],name=current_app.config['NAME'])

@main.route('/api/delete/Roles/<int:id>', methods=['DELETE'])
def api_delete_Roles(id):
    code    = API_OK
    message = 'OK'
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            id_counter=0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values = [id]
            row   = Roles()
            query = db.session.query(Roles)
            
            # First loop mandatory for row population ----------------------
            # detected primary key field: c.field
            query       = query.filter(Roles.id == id_values[id_counter])
            id_counter +=1
            # --------------------------------------------------------------
            row = query.one_or_none()

            if row is not None:
                db.session.delete(row)
                db.session.flush()
                db.session.commit()
                db.session.close()
                message = f"Deleted 'Roles' id = {id}"
                row     = json.loads(row.get_json())
            else:
                code    = API_NOT_FOUND
                message = f"Not found 'Roles' with id = {id}"
                row     = None        
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Roles',entities=[],name=current_app.config['NAME'])

# ======================================================================# view_subnets.py_gen_views_api.html.auto

# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2020-11-23 20:00:00.757932
# ======================================================================
# gen_views_api.html:AG 2020-11-23 20:00:00.757961
# table_name: Subnets
# class_name: subnets
# is shardened: False
# Table 'Subnets' keys = uuid
# Errors: None
# PK field found 'uuid' db.String(45)
# Subnets id field is 'Subnets.uuid' of type ''

@main.route('/api/get/Subnets'     , methods=['GET'])
@main.route('/api/get/Subnets/<id>', methods=['GET'])
def api_get_Subnets(id=None):
    code       = API_OK
    message    = 'OK'
    rows       = None
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            id_counter = 0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values=[id]
            # Codigo para un solo campo de id
            # chequear si marcado explicitamente
            query = db.session.query(Subnets)
            if id is not None:
                query = query.filter(Subnets.uuid == id_values[id_counter])
                rows = query.one_or_none()
            else:
                if request.args is not None and len(request.args):
                    if 'uuid' in request.args:
                        query = query.filter(Subnets.uuid == request.args.get('uuid'))
                    if 'name' in request.args:
                        query = query.filter(Subnets.name == request.args.get('name'))
                    if 'vlan_id' in request.args:
                        query = query.filter(Subnets.vlan_id == request.args.get('vlan_id'))
                    if 'vswitch_name' in request.args:
                        query = query.filter(Subnets.vswitch_name == request.args.get('vswitch_name'))
                    if 'type' in request.args:
                        query = query.filter(Subnets.type == request.args.get('type'))
                    if 'default_gateway_ip' in request.args:
                        query = query.filter(Subnets.default_gateway_ip == request.args.get('default_gateway_ip'))
                    if 'range' in request.args:
                        query = query.filter(Subnets.range == request.args.get('range'))
                    if 'prefix_length' in request.args:
                        query = query.filter(Subnets.prefix_length == request.args.get('prefix_length'))
                    if 'subnet_ip' in request.args:
                        query = query.filter(Subnets.subnet_ip == request.args.get('subnet_ip'))
                    if 'cluster' in request.args:
                        query = query.filter(Subnets.cluster == request.args.get('cluster'))
                rows = query.all()
            if rows is not None:
                if type(rows) == list:
                    for i in range(len(rows)):
                        rows[i] = json.loads(rows[i].get_json())
                else:
                    rows = [json.loads(rows.get_json())]
            else:
                rows = []
            if len(rows) == 0:
                code = API_NO_DATA
                state = get_api_state(API_NO_DATA)
                
                if id is None:
                    message = f"No 'Subnets' records found"
                else:
                    message = f"No 'Subnets.uuid' = {id} record found"
                
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Subnets',entities=rows,name=current_app.config['NAME'])

@main.route('/api/post/Subnets', methods=['POST'])
def api_post_Subnets():
    code    = API_OK
    message = 'OK'
    row     = None
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            row = Subnets()
            # Populates row from json, if ID=int:autoincrement then None
            row.uuid = request.json.get('uuid',None)
            row.name = request.json.get('name',None)
            row.vlan_id = request.json.get('vlan_id',None)
            row.vswitch_name = request.json.get('vswitch_name',None)
            row.type = request.json.get('type',None)
            row.default_gateway_ip = request.json.get('default_gateway_ip',None)
            row.range = request.json.get('range',None)
            row.prefix_length = request.json.get('prefix_length',None)
            row.subnet_ip = request.json.get('subnet_ip',None)
            row.cluster = request.json.get('cluster',None)
            # ----------------------------------------------------------
            db.session.add(row)
            db.session.flush()
            db.session.commit()
            db.session.refresh(row)
            db.session.close()
            message = f"Created 'Subnets' uuid = {row.uuid}"
            row     = json.loads(row.get_json())
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
            row     = None
    else:
        code    = API_ERROR
        message = 'Unauthorized request'            
    return get_api_response(code=code,message=message,kind='Subnets',entities=[row],name=current_app.config['NAME'])

@main.route('/api/put/Subnets/<id>', methods=['PUT'])
def api_put_Subnets(id):
    code    = API_OK
    message = 'OK'
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            id_counter=0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values = [id]
            row   = Subnets()
            query = db.session.query(Subnets)
            
            # First loop mandatory for row population ----------------------
            query = query.filter(Subnets.uuid == id_values[id_counter])
            id_counter += 1
            # --------------------------------------------------------------
            row = query.one_or_none()
            # If row exists then continue:
            if row is not None:
                # Second loop seek for updated fields ----------------------
                if 'name' in request.json.keys():
                    row.name = request.json.get('name')
                if 'vlan_id' in request.json.keys():
                    row.vlan_id = request.json.get('vlan_id')
                if 'vswitch_name' in request.json.keys():
                    row.vswitch_name = request.json.get('vswitch_name')
                if 'type' in request.json.keys():
                    row.type = request.json.get('type')
                if 'default_gateway_ip' in request.json.keys():
                    row.default_gateway_ip = request.json.get('default_gateway_ip')
                if 'range' in request.json.keys():
                    row.range = request.json.get('range')
                if 'prefix_length' in request.json.keys():
                    row.prefix_length = request.json.get('prefix_length')
                if 'subnet_ip' in request.json.keys():
                    row.subnet_ip = request.json.get('subnet_ip')
                if 'cluster' in request.json.keys():
                    row.cluster = request.json.get('cluster')
                # ----------------------------------------------------------
                db.session.merge(row)
                db.session.flush()
                db.session.commit()
                db.session.refresh(row)
                db.session.close()
                message = f"Modified 'Subnets' uuid = {id}"
                row     = json.loads(row.get_json())
            else:
                code    = API_NOT_FOUND
                message = f"Not found Subnets with uuid = {id}"
                row     = None
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Subnets',entities=[row],name=current_app.config['NAME'])

@main.route('/api/patch/Subnets/<id>', methods=['PATCH'])
def api_patch_Subnets(id):
    code    = API_OK
    message = 'OK'
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            id_counter=0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values = [id]
            row   = Subnets()
            query = db.session.query(Subnets)
            
            # First loop mandatory for row population ----------------------
            query = query.filter(Subnets.uuid == id_values[id_counter])
            id_counter += 1
            # --------------------------------------------------------------
            row = query.one_or_none()
            # If row exists then continue:
            if row is not None:
                # Second loop seek for updated fields ----------------------
                if 'name' in request.json.keys():
                    row.name = request.json.get('name')
                if 'vlan_id' in request.json.keys():
                    row.vlan_id = request.json.get('vlan_id')
                if 'vswitch_name' in request.json.keys():
                    row.vswitch_name = request.json.get('vswitch_name')
                if 'type' in request.json.keys():
                    row.type = request.json.get('type')
                if 'default_gateway_ip' in request.json.keys():
                    row.default_gateway_ip = request.json.get('default_gateway_ip')
                if 'range' in request.json.keys():
                    row.range = request.json.get('range')
                if 'prefix_length' in request.json.keys():
                    row.prefix_length = request.json.get('prefix_length')
                if 'subnet_ip' in request.json.keys():
                    row.subnet_ip = request.json.get('subnet_ip')
                if 'cluster' in request.json.keys():
                    row.cluster = request.json.get('cluster')
                # ----------------------------------------------------------
                db.session.merge(row)
                db.session.flush()
                db.session.commit()
                db.session.refresh(row)
                db.session.close()
                message = f"Modified 'Subnets' uuid = {id}"
                row     = json.loads(row.get_json())
            else:
                code    = API_NOT_FOUND
                message = f"Not found Subnets with uuid = {id}"
                row     = None
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Subnets',entities=[row],name=current_app.config['NAME'])

@main.route('/api/delete/Subnets/<id>', methods=['DELETE'])
def api_delete_Subnets(id):
    code    = API_OK
    message = 'OK'
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            id_counter=0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values = [id]
            row   = Subnets()
            query = db.session.query(Subnets)
            
            # First loop mandatory for row population ----------------------
            # detected primary key field: c.field
            query       = query.filter(Subnets.uuid == id_values[id_counter])
            id_counter +=1
            # --------------------------------------------------------------
            row = query.one_or_none()

            if row is not None:
                db.session.delete(row)
                db.session.flush()
                db.session.commit()
                db.session.close()
                message = f"Deleted 'Subnets' uuid = {id}"
                row     = json.loads(row.get_json())
            else:
                code    = API_NOT_FOUND
                message = f"Not found 'Subnets' with uuid = {id}"
                row     = None        
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Subnets',entities=[],name=current_app.config['NAME'])

# ======================================================================# view_users.py_gen_views_api.html.auto

# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2020-11-23 20:00:00.937177
# ======================================================================
# gen_views_api.html:AG 2020-11-23 20:00:00.937192
# table_name: Users
# class_name: User
# is shardened: False
# Table 'Users' keys = id
# Errors: None
# ID field found 'id' auto_increment db.Integer
# Users id field is 'Users.id' of type 'int:'

@main.route('/api/get/Users'     , methods=['GET'])
@main.route('/api/get/Users/<int:id>', methods=['GET'])
def api_get_Users(id=None):
    code       = API_OK
    message    = 'OK'
    rows       = None
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            id_counter = 0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values=[id]
            # Codigo para un solo campo de id
            # chequear si marcado explicitamente
            query = db.session.query(Users)
            if id is not None:
                query = query.filter(Users.id == id_values[id_counter])
                rows = query.one_or_none()
            else:
                if request.args is not None and len(request.args):
                    if 'id' in request.args:
                        query = query.filter(Users.id == request.args.get('id'))
                    if 'username' in request.args:
                        query = query.filter(Users.username == request.args.get('username'))
                    if 'role_id' in request.args:
                        query = query.filter(Users.role_id == request.args.get('role_id'))
                    if 'email' in request.args:
                        query = query.filter(Users.email == request.args.get('email'))
                    if 'password_hash' in request.args:
                        query = query.filter(Users.password_hash == request.args.get('password_hash'))
                    if 'confirmed' in request.args:
                        query = query.filter(Users.confirmed == request.args.get('confirmed'))
                    if 'CC_Id' in request.args:
                        query = query.filter(Users.CC_Id == request.args.get('CC_Id'))
                rows = query.all()
            if rows is not None:
                if type(rows) == list:
                    for i in range(len(rows)):
                        rows[i] = json.loads(rows[i].get_json())
                else:
                    rows = [json.loads(rows.get_json())]
            else:
                rows = []
            if len(rows) == 0:
                code = API_NO_DATA
                state = get_api_state(API_NO_DATA)
                
                if id is None:
                    message = f"No 'Users' records found"
                else:
                    message = f"No 'Users.id' = {id} record found"
                
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Users',entities=rows,name=current_app.config['NAME'])

@main.route('/api/post/Users', methods=['POST'])
def api_post_Users():
    code    = API_OK
    message = 'OK'
    row     = None
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            row = Users()
            # Populates row from json, if ID=int:autoincrement then None
            row.id = None
            row.username = request.json.get('username',None)
            row.role_id = request.json.get('role_id',None)
            row.email = request.json.get('email',None)
            row.password_hash = request.json.get('password_hash',None)
            row.confirmed = request.json.get('confirmed',0)
            row.CC_Id = request.json.get('CC_Id',1)
            # ----------------------------------------------------------
            db.session.add(row)
            db.session.flush()
            db.session.commit()
            db.session.refresh(row)
            db.session.close()
            message = f"Created 'Users' id = {row.id}"
            row     = json.loads(row.get_json())
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
            row     = None
    else:
        code    = API_ERROR
        message = 'Unauthorized request'            
    return get_api_response(code=code,message=message,kind='Users',entities=[row],name=current_app.config['NAME'])

@main.route('/api/put/Users/<int:id>', methods=['PUT'])
def api_put_Users(id):
    code    = API_OK
    message = 'OK'
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            id_counter=0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values = [id]
            row   = Users()
            query = db.session.query(Users)
            
            # First loop mandatory for row population ----------------------
            query = query.filter(Users.id == id_values[id_counter])
            id_counter += 1
            # --------------------------------------------------------------
            row = query.one_or_none()
            # If row exists then continue:
            if row is not None:
                # Second loop seek for updated fields ----------------------
                if 'username' in request.json.keys():
                    row.username = request.json.get('username')
                if 'role_id' in request.json.keys():
                    row.role_id = request.json.get('role_id')
                if 'email' in request.json.keys():
                    row.email = request.json.get('email')
                if 'password_hash' in request.json.keys():
                    row.password_hash = request.json.get('password_hash')
                if 'confirmed' in request.json.keys():
                    row.confirmed = request.json.get('confirmed')
                if 'CC_Id' in request.json.keys():
                    row.CC_Id = request.json.get('CC_Id')
                # ----------------------------------------------------------
                db.session.merge(row)
                db.session.flush()
                db.session.commit()
                db.session.refresh(row)
                db.session.close()
                message = f"Modified 'Users' id = {id}"
                row     = json.loads(row.get_json())
            else:
                code    = API_NOT_FOUND
                message = f"Not found Users with id = {id}"
                row     = None
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Users',entities=[row],name=current_app.config['NAME'])

@main.route('/api/patch/Users/<int:id>', methods=['PATCH'])
def api_patch_Users(id):
    code    = API_OK
    message = 'OK'
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            id_counter=0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values = [id]
            row   = Users()
            query = db.session.query(Users)
            
            # First loop mandatory for row population ----------------------
            query = query.filter(Users.id == id_values[id_counter])
            id_counter += 1
            # --------------------------------------------------------------
            row = query.one_or_none()
            # If row exists then continue:
            if row is not None:
                # Second loop seek for updated fields ----------------------
                if 'username' in request.json.keys():
                    row.username = request.json.get('username')
                if 'role_id' in request.json.keys():
                    row.role_id = request.json.get('role_id')
                if 'email' in request.json.keys():
                    row.email = request.json.get('email')
                if 'password_hash' in request.json.keys():
                    row.password_hash = request.json.get('password_hash')
                if 'confirmed' in request.json.keys():
                    row.confirmed = request.json.get('confirmed')
                if 'CC_Id' in request.json.keys():
                    row.CC_Id = request.json.get('CC_Id')
                # ----------------------------------------------------------
                db.session.merge(row)
                db.session.flush()
                db.session.commit()
                db.session.refresh(row)
                db.session.close()
                message = f"Modified 'Users' id = {id}"
                row     = json.loads(row.get_json())
            else:
                code    = API_NOT_FOUND
                message = f"Not found Users with id = {id}"
                row     = None
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Users',entities=[row],name=current_app.config['NAME'])

@main.route('/api/delete/Users/<int:id>', methods=['DELETE'])
def api_delete_Users(id):
    code    = API_OK
    message = 'OK'
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            id_counter=0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values = [id]
            row   = Users()
            query = db.session.query(Users)
            
            # First loop mandatory for row population ----------------------
            query = query.filter(Users.id == id)
            # --------------------------------------------------------------
            row = query.one_or_none()

            if row is not None:
                db.session.delete(row)
                db.session.flush()
                db.session.commit()
                db.session.close()
                message = f"Deleted 'Users' id = {id}"
                row     = json.loads(row.get_json())
            else:
                code    = API_NOT_FOUND
                message = f"Not found 'Users' with id = {id}"
                row     = None        
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Users',entities=[],name=current_app.config['NAME'])

# ======================================================================
