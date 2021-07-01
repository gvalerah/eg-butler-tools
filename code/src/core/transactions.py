# ======================================================================
# EG Suite - EG Butler Core Service Application Transactions
# Purpose: To handle Butler API requests and orchestrate Butler Requests
# Live cycle
# (c) Emtec Group/Sertechno 2020
# GLVH gvalera@emtecgroup.net
# 2021-05-09 GVLH Refactoring to move functions to library and reuse
# 2021-05-18 GLVH adjust fur multiple subnets, and NO IP request
# 2021-05-23 GLVH QA and refactoring
# 2021-06-30 GÑVH QA final testing. Request lists download and other
# ======================================================================

import  os
import  sys
import  time
import  datetime
from    sqlalchemy                  import desc
from    pprint                      import pprint
from    pprint                      import pformat
from    emtec                       import *
from    emtec.butler.db.orm_model   import *
from    emtec.butler.constants      import *
from    emtec.butler.functions      import *
from    emtec.api                   import *
from    emtec.data                  import *
from    emtec.nutanix               import *
from    .                           import db
from    .                           import mail
from    .                           import logger
# Transactions
# Context Variables 
tracebox_log_length=80
# This structure will keep data cache between main loop executions

current={
    'cost_centers':[],
    'rates':[],
    'images':[],
    'projects':[],
    'categories':[],
    'subnets':[],
    'transactions':{}
}

# Transaction support functions

# Get list of remote sites
# nota verificar si requiere algun parametro para la llamada por sitio
# Ojo validar correo de David dice que debe ser hacia un Prism Element 
def get_hosts(app,timeout=None):
    logger = check_logger()
    logger.debug(f'{this()}: IN Get list of Nutanix hosts ...')
    
    hosts = None
    try:
        host      = app.config.get('NUTANIX_HOST')
        port      = app.config.get('NUTANIX_PORT')
        username  = app.config.get('NUTANIX_USERNAME')
        password  = app.config.get('NUTANIX_PASSWORD')
        protocol  = app.config.get('NUTANIX_PROTOCOL')
        # 20210509 GV refactoring to move code to library
        hosts   = prism_central_get_hosts(
                        host,
                        port,
                        username,
                        password,
                        protocol,
                        timeout=timeout,
                        logger=logger
                        )
    except Exception as e:
        tracebox_log(
            f'{this()}: EXCEPTION: {str(e)}',
            logger = logger,
            level  = logging.ERROR
            )
        
    logger.trace(f"{this()}: hosts: {hosts}")
    logger.debug(f'{this()}: OUT')
    return hosts

# Get list of remote sites
# nota verificar si requiere algun parametro para la llamada por sitio
# Ojo validar correo de David dice que debe ser hacia un Prism Element 
def get_remote_sites(app,host=None,timeout=None):
    logger.debug(f'{this()}: IN Get list of Nutanix remote sites ...')
    remote_sites = None
    try:
        if host is None:
            host  = app.config.get('NUTANIX_HOST')
        port      = app.config.get('NUTANIX_PORT')
        username  = app.config.get('NUTANIX_USERNAME')
        password  = app.config.get('NUTANIX_PASSWORD')
        protocol  = app.config.get('NUTANIX_PROTOCOL')
        # 20210509 GV refactoring to move code to library
        remote_sites = prism_central_get_remote_sites(
                            host,
                            port,
                            username,
                            password,
                            protocol,
                            timeout=timeout,
                            logger=logger
                            )
    except Exception as e:
        tracebox_log(
            f'{this()}: {str(e)}',
            logger = logger,
            level  = logging.ERROR,
            length = tracebox_log_length
            )
        
    logger.debug(f"{this()}: OUT remote_sites: {remote_sites}")
    return remote_sites
    
# Create data protection
# nota verificar si requiere algun parametro para la llamada por sitio
# Ojo validar correo de David dice que debe ser hacia un Prism Element 
def create_protection_domain(app,host=None,pdname=None,annotation=None,vmname=None,timeout=None):
    logger.debug(f'{this()}: IN Create Protection Domain: host:{host},pdname:{pdname},vmname:{vmname}')
    
    created = False
    if pdname is None:
        # Default: if pdname is None then pdname = vmname
        if vmname is not None:
            pdname = f"PD-{vmname}"
        else:
            # default will be an hex number based in actual timestamp in usecs
            # this shouldn't happen since vmname need to be available
            pdname = f"PD-{int(datetime.datetime.now().timestamp()*1000000):x}"
    pdname = pdname.replace(" ","_")
    try:
        if host is None:
            host  = app.config.get('NUTANIX_HOST')
        port      = app.config.get('NUTANIX_PORT')
        username  = app.config.get('NUTANIX_USERNAME')
        password  = app.config.get('NUTANIX_PASSWORD')
        protocol  = app.config.get('NUTANIX_PROTOCOL')
        endpoint  = '/PrismGateway/services/rest/v2.0/protection_domains'
        arguments = ''
        if annotation is None:
            annotation = f'Protection domain created by EG Butler at {datetime.datetime.now()}'
        data      = {
            'annotations':[annotation],
            'value':pdname
            }
            
        headers   = {'Content-Type': 'application/json'}
        url       = f'{protocol}://{host}:{port}/{endpoint}{arguments}'

        logger.debug(f'{this()}: user = {username}')
        logger.debug(f'{this()}: url  = {url}')

        response = api_request('POST',
                        url,
                        data     = json.dumps(data),
                        headers  = headers,
                        username = username,
                        password = password,
                        timeout  = timeout,
                        logger   = logger
                        )
        if response is not None:
            data=response.json()
            logger.debug(f'{this()}: data={data}')
            if response.ok:
                if response.status_code == 201:
                    logger.debug(f"protection domain '{pdname}' created {response.status_code} {response.reason}")
                created = True
            else:
                if response.status_code == 422:
                    logger.warning( f"protection domanin '{pdname}' "
                                    f"{response.status_code} "
                                    f"{response.reason} "
                                    f"{data.get('message',None)} "
                                    f"{data.get('error_code',None)}"
                                )
                    created = True
                else:
                    logger.error(   f"protection domanin '{pdname}' "
                                    f"{response.status_code} "
                                    f"{response.reason} "
                                    f"{data.get('message',None)} "
                                    f"{data.get('error_code',None)}"
                                )
                    created = False
        else:
            created = False
    except Exception as e:
        tracebox_log(f'{this()}: {str(e)}',
            logger = logger,
            level  = logging.ERROR,
            length = tracebox_log_length
            )
        
    logger.debug(f"{this()}: OUT protection domain: {pdname} created={created}")
    return pdname if created else None

# Create data protection
# nota verificar si requiere algun parametro para la llamada por sitio
# Ojo validar correo de David dice que debe ser hacia un Prism Element 
def protect_vms(app,vmname,host,pdname,timeout=None):
    logger.info(f'{this()}: IN Protect vms {vmname}')
    
    success = False
    try:
        if host is None:
            host  = app.config.get('NUTANIX_HOST')
        port      = app.config.get('NUTANIX_PORT')
        username  = app.config.get('NUTANIX_USERNAME')
        password  = app.config.get('NUTANIX_PASSWORD')
        protocol  = app.config.get('NUTANIX_PROTOCOL')
        endpoint  = f'/PrismGateway/services/rest/v2.0/protection_domains/{pdname}/protect_vms'
        arguments = ''
        data      = {
            'app_consistent_snapshots'  : False,
            'consistency_group_name'    : vmname, # protection domain, preguntar punto 3 del email de David
            'ignore_dup_or_missing_vms' : True,
            'names'                     : [vmname]
        }
            
        headers   = {'Content-Type': 'application/json'}
        url       = f'{protocol}://{host}:{port}/{endpoint}{arguments}'

        logger.debug(f'{this()}: user = {username}')
        logger.debug(f'{this()}: url  = {url}')

        response = api_request('POST',
                        url,
                        data     = json.dumps(data),
                        headers  = headers,
                        username = username,
                        password = password,
                        timeout  = timeout,
                        logger   = logger
                        )
        if response is not None:
            data=response.json()
            logger.debug(f'{this()}: 233 data={data}')
            if response.ok:
                if response.status_code in [200,201]:
                    success = True
                    logger.info(f"{this()}: {response.status_code} {vmname} is protected now.")
                else:
                    logger.warning(f"{this()}: {response.status_code} {response.reason} {data.get('message',None)} {data.get('error_code',None)}")
                    success = False
            else:
                logger.debug(f"389 data={data}")
                if response.status_code == 422:
                    if data['message'].find('already protected') != -1:
                        logger.warning(f"{this()}: 244 {vmname} is already protected")
                        success = True
                    else:
                        logger.error(f"{this()}: {response.status_code} {response.reason} {data.get('message',None)} {data.get('error_code',None)}")
                        success = False                            
        else:
            logger.error(f"{this()}: invalid/null response")
            success = False                            
                    
    except Exception as e:
        tracebox_log(f'{this()}: {str(e)}',
            logger = logger,
            level  = logging.ERROR,
            length = tracebox_log_length
            )
        
    logger.debug(f"{this()}: OUT success: {success}")
    return success

def create_schedule(
        app,
        host                     = None,
        port                     = None,
        username                 = None,
        password                 = None,
        protocol                 = None,
        pdname                   = None,
        remote_cluster           = None,
        schedule_type            = 'HOURLY',
        user_start_time_in_usecs = None,
        every_nth                = None,
        local_max_snapshots      = 0,
        remote_max_snapshots     = 0,
        timeout                  = None,
    ):
    logger.debug(f'{this()}: IN Create schedule ...')
    logger.debug(f'{this()}: app                      = {app} {protocol}://{username}:{password}@{host}:{port}')
    logger.debug(f'{this()}: pdname                   = {pdname}')
    logger.debug(f'{this()}: remote_cluster           = {remote_cluster}')
    logger.debug(f'{this()}: schedule_type            = {schedule_type}')
    logger.debug(f'{this()}: user_start_time_in_usecs = {user_start_time_in_usecs}')
    logger.debug(f'{this()}: every_nth                = {every_nth}')
    logger.debug(f'{this()}: local_max_snapshots      = {local_max_snapshots}')
    logger.debug(f'{this()}: remote_max_snapshots     = {remote_max_snapshots}')
    logger.debug(f'{this()}: timeout                  = {timeout}')
    
    created = False
    try:
        if host     is None: host     = app.config.get('NUTANIX_HOST')
        if port     is None: port     = app.config.get('NUTANIX_PORT')
        if username is None: username = app.config.get('NUTANIX_USERNAME')
        if password is None: password = app.config.get('NUTANIX_PASSWORD')
        if protocol is None: protocol = app.config.get('NUTANIX_PROTOCOL')
        endpoint  = f'PrismGateway/services/rest/v2.0/protection_domains/{pdname}/schedules'
        arguments = ''
        
        if user_start_time_in_usecs is None:
            user_start_time_in_usecs = datetime.datetime.now().timestamp()*1000000
        
        if every_nth is None:
            if   schedule_type == 'SECONDLY':   every_nth = 300
            elif schedule_type == 'MINUTELY':   every_nth = 30                
            elif schedule_type == 'HOURLY':     every_nth = 6                
            elif schedule_type == 'DAILY':      every_nth = 1                
            elif schedule_type == 'WEEKLY':     every_nth = 1                
            elif schedule_type == 'MONTHLY':    every_nth = 1                

        data      = {
            'pd_name'  : pdname,
            'type'     : schedule_type,
            'user_start_time_in_usecs' : int(user_start_time_in_usecs),
            'app_consistent': False,
            'retention_policy':{}
            }
        
        # retention policy will be fullfilled depending on request
        # if local snapshots requested
        if local_max_snapshots is not None and local_max_snapshots > 0:
            data['retention_policy'].update({'local_max_snapshots':local_max_snapshots})
        if remote_max_snapshots is not None and remote_max_snapshots > 0:
            data['retention_policy'].update({'remote_max_snapshots':{remote_cluster: remote_max_snapshots}})

        if every_nth is not None:
            data.update({'every_nth':every_nth})
            
        headers   = {'Content-Type': 'application/json'}
        url       = f'{protocol}://{host}:{port}/{endpoint}{arguments}'

        logger.debug(f'{this()}: user = {username}')
        logger.debug(f'{this()}: url  = {url}')
        logger.debug(f'{this()}: data = {data}')

        response = api_request('POST',
                        url,
                        data     = json.dumps(data),
                        headers  = headers,
                        username = username,
                        password = password,
                        timeout  = timeout,
                        logger   = logger
                        )
        try:
            with open(f'trace/create_schedule_{pdname}','a') as fp:
                fp.write(f"{this()}: -----------------------\n")
                fp.write(f"{this()}: now     =  {datetime.datetime.now()}\n")
                fp.write(f"{this()}: url     =  {url}\n")
                fp.write(f"{this()}: headers =  {headers}\n")
                fp.write(f"{this()}: data    =\n")
                fp.write(f"{this()}: -----------------------\n")
                fp.write(f"{json.dumps(data)}\n")
                fp.write(f"{this()}: -----------------------\n")
                fp.write(f"{this()}: response = {response}\n")
        except:
            pass
        if response is not None:
            if response.ok:
                data = response.json()
                if response.status_code in [200,201]:
                    created = True
                else:
                    logger.error(f"{this()}: {response.status_code} {response.reason} {data.get('message',None)} {data.get('error_code',None)}")
                    logger.error(f'{this()}: data={data}')
                    created = False
            else:
                logger.error(f"{this()}: response.status_code = {response.status_code}")
                logger.error(f"{this()}: response.reason      = {response.reason}")
                logger.error(f'{this()}: data                 = {data}')
                created = False                
        else:
            logger.error(f"{this()}: No valid response received.")
                
    except Exception as e:
        tracebox_log(f'{this()}: {str(e)}',
            logger = logger,
            level  = logging.ERROR,
            length = tracebox_log_length
            )
        
    logger.trace(f"{this()}: created: {created}")
    logger.debug(f'{this()}: OUT')
    return created

# Atomic transaction for VM DRP creation in one call 
def create_drp(
        app,
        vmname,
        pdname                   = None,
        annotation               = None,
        remote_cluster           = None,
        schedule_type            = 'HOURLY',
        user_start_time_in_usecs = None,
        every_nth                = 1,
        local_max_snapshots      = 4,
        remote_max_snapshots     = 4,
        timeout                  = None
        ):
    ''' Create VM DRP replication in one call
    
    Arguments                | Description
    ---------                | -----------
    app                      | Requires a Flask Application object 
                             | containing proper environment 
                             | configuration (config NUTANIX* keys)
    vmname                   | VM name
    pdname                   | Protection domain name, 
                             | defaults to PD-<vmname>
    annotation               | Protection domain comment
    remote_cluster           | Remote Cluster name
    schedule_type            | Type of snapshot: SECONDLY,MINUTELY,
                             | HOURLY,DAILY,WEEKLY,MONTHLY, 
                             | defaults to "HOURLY"
    user_start_time_in_usecs | Snapshot start timestamp in microseconds
    every_nth                | snapshot interval, defaults to:
                             | 300 for SECONDLY, 30 for MINUTELY,
                             | 6 for HOURLY, 1 for DAILY,WEEKLY,MONTHLY
    local_max_snapshots      | Max local snapshot retention. default 4
    remote_max_snapshots     | Max remote snapshot retention. default 4
    timeout                  | connection/response timeout seconds
    '''
    logger.debug(f"{this()}: IN create DRP ...")
    success = False
    # Get cluster's hosts list
    logger.info(f"{this()}: getting clusters's hosts ...")
    cluster_host_ip = None
    cluster_host_name = None
    cluster_hosts = get_hosts(app)
    ip = None
    if cluster_hosts is not None:
        for host in cluster_hosts:
            cluster_host_name = host['spec'].get('name',None)
            if cluster_host_name is not None:
                cluster_host_ip = host['spec']['resources']['controller_vm']['ip']
                break
    else:
        logger.error(f"{this()}: No hosts found !!!")
        return False,None
    if cluster_host_ip is not None:
        # try to get remote cluster if not defined
        if remote_cluster is None:
            logger.info(f"{this()}: getting remote cluster ...")
            sites = get_remote_sites(app,host=cluster_host_ip)
            if len(sites):
                remote_cluster = sites[0]['name']
        if remote_cluster is not None:
            # Create protection domain -------------------------------------
            logger.info(f"{this()}: remote_cluster: {remote_cluster}")
            logger.info(f"{this()}: creating protection domain for vm '{vmname}' ...")
            # if protection domain is None, then creates one and
            # initializes name, it wil lbe returned later
            if pdname is None:
                pdname = create_protection_domain(
                        app,
                        host       = cluster_host_ip,
                        pdname     = pdname,
                        annotation = annotation,
                        vmname     = vmname,
                        timeout    = timeout
                        )
            # Schedules if valid protection domain
            if pdname is not None:
                # got valid protection domain, will protect vms ------------
                # create schedule
                logger.info(f"{this()}: pdname = '{pdname}' ...")
                logger.info(f"{this()}: protecting vm '{vmname}' in '{remote_cluster}:{pdname}' ...")
                if protect_vms(app,vmname,cluster_host_ip,pdname,timeout=timeout):
                    # VM is protected, then schedule it --------------------
                    logger.info(f"{this()}: creating schedule for '{remote_cluster}:{pdname}' ...")
                    logger.debug(f"{this()}: app = {app}")
                    logger.debug(f"{this()}: host = {host}")
                    logger.debug(f"{this()}: pdname = {pdname}")
                    logger.debug(f"{this()}: remote_cluster = {remote_cluster}")
                    logger.debug(f"{this()}: schedule_type = {schedule_type}")
                    logger.debug(f"{this()}: user_start_time_in_usecs = {user_start_time_in_usecs}")
                    logger.debug(f"{this()}: every_nth = {every_nth}")
                    logger.debug(f"{this()}: local_max_snapshots = {local_max_snapshots}")
                    logger.debug(f"{this()}: remote_max_snapshots = {remote_max_snapshots}")
                    logger.debug(f"{this()}: timeout = {timeout}")
                    logger.debug(f"{this()}: callig create schedule ...")
                    if create_schedule(
                        app,
                        host                     = cluster_host_ip,
                        pdname                   = pdname,
                        remote_cluster           = remote_cluster,
                        schedule_type            = schedule_type,
                        user_start_time_in_usecs = user_start_time_in_usecs,
                        every_nth                = every_nth,
                        local_max_snapshots      = local_max_snapshots,
                        remote_max_snapshots     = remote_max_snapshots,
                        timeout                  = timeout
                        ):
                        logger.info(f'{this()}: protection schedule for VM {vmname} SUCCESS.')
                        success = True
                    else:
                        # no calendarizada
                        logger.warning(f'{this()}: protection schedule for VM {vmname} FAILURE.')
                else:
                    # error no protegida
                    logger.warning(f'{this()}: VM {vmname} protection failure.')
            else:
                # Error nada creado
                logger.warning(f'{this()}: protection domain creation for VM {vmname} FAILURE.')
    else:
        logger.error(f"{this()}: No valid Nutanix host found in cluster.")
    logger.debug(f'{this()}: OUT success = {success} pdname = {pdname}')
    return success,pdname
       
def trace_trx(trx_name,app,row,response=None):
    try:
        if app.config.get("DEBUG"):
            logger.debug(f"{this()}: trx_name   : {trx_name}")
            logger.debug(f"{this()}: app        : {response}")
            logger.debug(f"{this()}: row        : {row}")
            logger.debug(f"{this()}: response   : {response}")
            trace_folder = f"{app.config.get('app_folder','/tmp')}/trace"
            os.makedirs(trace_folder,exist_ok=True)
            ts=strftime('%y%m%d-%H%M%S')
            if hasattr(row,'Id'):
                filename=f"{trace_folder}/{trx_name}_{row.Id}_{ts}.txt"
            elif hasattr(row,'Requests'):
                filename=f"{trace_folder}/{trx_name}_{row.Requests.Id}_{ts}.txt"
            else:
                filename=f"{trace_folder}/{trx_name}_{os.getpid()}_{ts}.txt"
            logger.debug(f'{this()}: IN writing {filename}')
            with open(filename,"w") as fp:
                try:
                    fp.write(f"Transaction: {trx_name}\n")
                    fp.write(f"Date Time  : {datetime.datetime.now()}\n")
                    if hasattr(row,'Id'):                
                        fp.write(f"Request    : {row.Id}\n")
                    elif hasattr(row,'Requests'):
                        fp.write(f"Request    : {row.Requests.Id}\n")
                    fp.write(f"row        : {row}\n")
                    fp.write(f"response   : {response}\n")
                    if response is not None:
                        fp.write(f"r.request  : {response.request}\n")
                        logger.debug(f"r.request  : {response.request}")
                        if response.request is not None:
                            fp.write(f"      url  : {response.request.url}\n")
                            logger.debug(f"      url  : {response.request.url}")
                        if response.ok:
                            fp.write(f"url        : {response.url}\n")
                            fp.write(f"data       : {response.json()}\n")
                            logger.debug(f"url        : {response.url}")
                            logger.debug(f"data       : {response.json()}")
                        else:
                            fp.write(f"url        : {response.url}\n")
                            fp.write(f"reason     : {response.reason}\n")
                            logger.debug(f"url        : {response.url}")
                            logger.debug(f"data       : {response.reason}")
                except Exception as e:
                    emtec_handle_general_exception(e,logger=logger,fp=fp)
    except Exception as e:
        emtec_handle_general_exception(e,logger=logger,fp=sys.stderr)
        
# ----------------------------------------------------------------------
            
# Update Cost Centers from EG Collector --------------------------------
def trx_ucc_update_butler_cost_centers(app):
    logger.debug(f'{this()}: IN Get CCs from EG Collector and update EG Butler')
    result   = get_api_response(    
                code=BUTLER_CORE_TRX_ERROR,
                message=f'NO TRX RESPONSE')
    
    host      = app.config.get('COLLECTOR_HOST')
    port      = app.config.get('COLLECTOR_PORT')
    username  = app.config.get('COLLECTOR_USERNAME')
    password  = app.config.get('COLLECTOR_PASSWORD')
    protocol  = app.config.get('COLLECTOR_PROTOCOL')
    timeout   = app.config.get('COLLECTOR_TIMEOUT',5)
    endpoint  = 'api/get/Cost_Centers'
    arguments =''
    data      = {}
        
    headers   = {'Content-Type': 'application/json'}
    url       = f'{protocol}://{host}:{port}/{endpoint}{arguments}'

    logger.debug(f'{this()}: user = {username}')
    logger.debug(f'{this()}: url  = {url}')

    response = api_request('GET',
                    url,
                    data=data,
                    headers=headers,
                    username=username,
                    password=password,
                    timeout=timeout,
                    logger   = logger
                    )
    logger.trace(f"{this()}: response:             {response}")
    if response is not None:
        logger.debug(f"{this()}: response.status_code: {response.status_code}")
        data = response.json()
        logger.trace(f"{this()}: data: {data}")
        if response.status_code == 200:
            # Actual process of result here
            if data['status']['code'] == 0:
                rows=[]                
                logger.trace(f"{this()}: {pformat(data)}")
                logger.debug(f"{this()}: Got: {len(data['entities'])} Cost Center entities from Collector")
                for entity in data['entities']:
                    row=Cost_Centers()
                    for key in entity:
                        setattr(row,key,entity[key])
                    rows.append(row)
                    logger.trace(f'{this()}: CC:{row.CC_Id}|{row.CC_Code}|{row.CC_Description}')
                logger.debug(f'{this()}: Loaded: {len(rows)} Cost Center rows from Collector')
                # rows contains all Cost Centers from Collector
                # only these codes should remain in butler
                try:
                    keep=[]
                    for row in rows:
                        db.session.merge(row)
                        #eep.append(row.CC_Code)
                        keep.append(row.CC_Id)
                    db.session.commit()
                    db.session.flush()
                    logger.debug(f"{this()}: Got:  {len(rows)} Cost Centers. Merged with Butler")
                    logger.debug(f"{this()}: Keep: {len(rows)} Cost Centers. In Butler")
                    logger.trace(f"{this()}: Keep: {keep}")
                    if len(rows):
                        current['cost_centers']=rows
                        # delete obsolete codes
                        query = db.session.query(Cost_Centers
                            #).filter(Cost_Centers.CC_Code.notin_(keep))
                            ).filter(Cost_Centers.CC_Id.notin_(keep))
                        logger.trace(f'{this()}: query={query}')
                        rows_to_delete=query.all()
                        logger.debug(f'{this()}: Cost Centers to delete = {len(rows_to_delete)}')
                        logger.trace(f'{this()}: rows_to_delete = {rows_to_delete}')
                        for row in rows_to_delete:
                            db.session.delete(row)
                        db.session.commit()
                        db.session.flush()
                except Exception as e:
                    logger.error(f'{this()}: exception = {str(e)}')
                    
                # Prepare API Response
                result = get_api_response(
                    # status arguments
                    state = data['status']['state'],
                    code = data['status']['code'],
                    message = data['status']['message'],
                    execution_context = None,
                    # metadata
                    total_matches = data['metadata']['total_matches'],
                    kind = data['metadata']['kind'],
                    length = data['metadata']['length'],
                    offset = data['metadata']['offset'],
                    )
            else:
                result = get_api_response(
                    # status arguments
                    state = data['status']['state'],
                    code = data['status']['code'],
                    message = data['status']['message'],
                    execution_context = None,
            )
        else:
            result = get_api_response(
                code = response.status_code,
                message = response.reason
                )
    else:
        result = get_api_response(
            code = BUTLER_CORE_TRX_ERROR,
            message = f'NO RESPONSE'
            )
    logger.debug(f'{this()}: OUT')
    tracebox_log(f'{this()}: {str(result)}',
            logger=logger,level=logging.DEBUG,length=tracebox_log_length)
    return result

# Update RAtes from EG Collector ---------------------------------------
def trx_ura_update_butler_rates(app):
    logger.debug(f'{this()}: IN Get Rates from EG Collector and update EG Butler')
    result   = get_api_response(    code=BUTLER_CORE_TRX_ERROR,
                                    message=f'NO TRX RESPONSE')
    
    host     = app.config.get('COLLECTOR_HOST')
    port     = app.config.get('COLLECTOR_PORT')
    username = app.config.get('COLLECTOR_USERNAME')
    password = app.config.get('COLLECTOR_PASSWORD')
    protocol = app.config.get('COLLECTOR_PROTOCOL')
    timeout  = app.config.get('COLLECTOR_TIMEOUT',5)
    endpoint = 'api/get/Rates'
    arguments=''
        
    headers  = {'Content-Type': 'application/json'}
    url      = f'{protocol}://{host}:{port}/{endpoint}{arguments}'

    logger.debug(f'{this()}: user = {username}')
    logger.debug(f'{this()}: url  = {url}')

    response = api_request('GET',
                    url,
                    #data=data,
                    headers=headers,
                    username=username,
                    password=password,
                    timeout=timeout,
                    logger   = logger
                    )
    if response is not None:
        data = response.json()
        if response.status_code == 200:
            # Actual process of result here
            if data['status']['code'] == 0:
                rows=[]
                for entity in data['entities']:
                    row=Rates()
                    for key in entity:
                        setattr(row,key,entity[key])
                    rows.append(row)
                    logger.trace(f'{this()}: Rate: {row.Rat_Id}')
                logger.debug(f'{this()}: Processed: {len(rows)} Rate rows')

                # rows contains all Rates from Collector
                # only these rates should remain in butler
                try:
                    keep=[]
                    for row in rows:
                        db.session.merge(row)
                        keep.append(row.Rat_Id)
                    db.session.commit()
                    db.session.flush()
                    logger.debug(f"{this()}: Got: {len(rows)} Rates.")
                    if len(rows):
                        current['rates']=rows
                        # delete obsolete codes
                        rows_to_delete = db.session.query(Rates
                            ).filter(Rates.Rat_Id.notin_(keep)
                            ).all()
                        logger.debug(f'{this()}: Cost Rates to delete = {len(rows_to_delete)}')
                        for row in rows_to_delete:
                            db.session.delete(row)
                        db.session.commit()
                        db.session.flush()
                except Exception as e:
                    db.session.rollback()
                    tracebox_log(f'{this()}: exception = {str(e)}',
                        logger = logger,
                        level  = logging.ERROR,
                        length = tracebox_log_length
                        )
                    
                # Prepare API Response
                result = get_api_response(
                    # status arguments
                    state = data['status']['state'],
                    code = data['status']['code'],
                    message = data['status']['message'],
                    execution_context = None,
                    # metadata
                    total_matches = data['metadata']['total_matches'],
                    kind = data['metadata']['kind'],
                    length = data['metadata']['length'],
                    offset = data['metadata']['offset'],
                    )
            else:
                result = get_api_response(
                    # status arguments
                    state = data['status']['state'],
                    code = data['status']['code'],
                    message = data['status']['message'],
                    execution_context = None,
            )
        else:
            result = get_api_response(
                code = response.status_code,
                message = response.reason
                )
    else:
        result = get_api_response(
            code = BUTLER_CORE_TRX_ERROR,
            message = f'NO RESPONSE'
            )
    logger.debug(f'{this()}: OUT')
    tracebox_log(f'{this()}: {str(result)}',
            logger=logger,level=logging.DEBUG,length=tracebox_log_length)
    return result

# Update disk IMages from Nutanix (Prism Central + Prism Element(s)) ---
def trx_uim_update_butler_images(app):
    logger.debug(f'{this()}: IN Get Images list from Nutanix ...')
    result   = get_api_response(    code=BUTLER_CORE_TRX_ERROR,
                                    message=f'NO TRX RESPONSE')
    
    host     = app.config.get('NUTANIX_HOST')
    port     = app.config.get('NUTANIX_PORT')
    username = app.config.get('NUTANIX_USERNAME')
    password = app.config.get('NUTANIX_PASSWORD')
    protocol = app.config.get('NUTANIX_PROTOCOL')
    timeout  = app.config.get('NUTANIX_TIMEOUT',5)
    endpoint = 'api/nutanix/v3/clusters/list'
    arguments=''
    
    headers  = {'Content-Type': 'application/json'}
    data     = {'kind': 'cluster'}
    url      = f'{protocol}://{host}:{port}/{endpoint}{arguments}'

    logger.debug(f'{this()}: Get clusters list: user = {username} url  = {url}')

    clusters = api_request('POST',
                    url,
                    data=json.dumps(data),
                    headers=headers,
                    username=username,
                    password=password,
                    timeout=timeout,
                    logger   = logger
                    )        

    if clusters is not None:
        data_clusters = clusters.json()
        if clusters.status_code == 200:
            cluster_ips=[]
            for entity in data_clusters['entities']:
                try:
                    cluster_ips.append(entity['spec']['resources']['network']['external_ip'])
                except:
                    pass
            rows=[]
            
            logger.debug(f"{this()}: Got {len(cluster_ips)} cluster's images ...")
            for cluster_ip in cluster_ips:
                endpoint = 'PrismGateway/services/rest/v2.0/images/'
                data={  'include_vm_disk_sizes':True,
                        'include_vm_disk_paths':True
                        }
                url = f'{protocol}://{cluster_ip}:{port}/{endpoint}{arguments}'
                logger.debug(f'{this()}: url  = {url}')
                response = api_request('GET',
                                url,
                                data=data,
                                headers=headers,
                                username=username,
                                password=password,
                                logger  = logger
                                )        
                if response is not None:
                    if response.status_code == 200:
                        # Actual process of result here
                        new_disk_images = 0
                        for entity in response.json()['entities']:
                            if 'image_type' in entity and entity['image_type'] == 'DISK_IMAGE' and entity['image_state']=='ACTIVE':
                                row=Nutanix_VM_Images()
                                row.imageservice_uuid_diskclone=entity['uuid']
                                row.description=entity['name']
                                row.size_mib=entity['vm_disk_size']/(1024*1024)
                                rows.append(row)
                                new_disk_images += 1
                                logger.trace(f'{this()}: Image: {row.description}')
                        logger.debug(f'{this()}: {new_disk_images} new disk images found in {cluster_ip}')

            # rows contains all VM Images from Nutanix
            # only these image uuids should remain in butler
            try:
                keep=[]
                for row in rows:
                    db.session.merge(row)
                    keep.append(row.imageservice_uuid_diskclone)
                db.session.commit()
                db.session.flush()
                logger.debug(f"{this()}: Got: {len(rows)} Images.")
                if len(rows):
                    current['images']=rows
                    # delete obsolete codes
                    rows_to_delete = db.session.query(Nutanix_VM_Images
                        ).filter(Nutanix_VM_Images.imageservice_uuid_diskclone.notin_(keep)
                        ).all()
                    if len(rows_to_delete):
                        logger.warning(f'{this()}: Images to delete = {len(rows_to_delete)}.')
                    for row in rows_to_delete:
                        logger.warning(f'{this()}: Deleting VM Image {row.description} ...')
                        db.session.delete(row)
                    db.session.commit()
                    db.session.flush()
            except Exception as e:
                db.session.rollback()
                tracebox_log(f'{this()}: exception = {str(e)}',
                    logger = logger,
                    level  = logging.ERROR,
                    length = tracebox_log_length
                    )

            logger.debug(f"{this()}: Got: {len(rows)} Image rows for clusters: {','.join(cluster_ips)}")
            # Prepare API Response
            result = get_api_response(
                # status arguments
                state = 'OK',
                code = 0,
                message = f"{this()}: Got: {len(rows)} Image rows for clusters {','.join(cluster_ips)}",
                execution_context = None,
                # metadata
                total_matches = len(rows),
                kind = 'disk image',
                length = len(rows),
                offset = 0,
                )
        else:
            result = get_api_response(
                # status arguments
                state = 'ERROR',
                code = 1,
                message = f'{this()}: status code = {clusters.status_code} {clusters.reason}. '
                          f'url={url} data={data} headers={headers}',
                execution_context = None,
            )            
    else:
        result = get_api_response(
            # status arguments
            state = 'ERROR',
            code = 1,
            message = f'{this()}: No Clusters found.',
            execution_context = None,
        )
    logger.debug(f'{this()}: OUT')
    tracebox_log(f'{this()}: {str(result)}',
            logger=logger,level=logging.DEBUG,length=tracebox_log_length)
    return result

# Update PRojects from Nutanix Prism Central ---------------------------
def trx_upr_update_butler_projects(app):
    logger.debug(f'{this()}: IN Get Nutanix Projects ...')
    result   = get_api_response(    code=BUTLER_CORE_TRX_ERROR,
                                    message=f'NO TRX RESPONSE')
    
    host     = app.config.get('NUTANIX_HOST')
    port     = app.config.get('NUTANIX_PORT')
    username = app.config.get('NUTANIX_USERNAME')
    password = app.config.get('NUTANIX_PASSWORD')
    protocol = app.config.get('NUTANIX_PROTOCOL')
    timeout  = app.config.get('NUTANIX_TIMEOUT',5)
    endpoint = 'api/nutanix/v3/projects/list'
    arguments=''
    
    headers  = {'Content-Type': 'application/json'}
    data     = {'kind': 'project'}
    url      = f'{protocol}://{host}:{port}/{endpoint}{arguments}'

    logger.debug(f'{this()}: user = {username}')
    logger.debug(f'{this()}: url  = {url}')

    projects = api_request('POST',
                    url,
                    data=json.dumps(data),
                    headers=headers,
                    username=username,
                    password=password,
                    timeout=timeout,
                    logger   = logger
                    )        
    
    if projects is not None:
        data = projects.json()
        rows=[]
        # Actual process of result here
        for entity in projects.json()['entities']:
            try:
                if entity['metadata'].get('project_reference') is not None:
                    if entity['metadata']['project_reference']['name'] != 'DEFAULT':
                        try:
                            row=Projects()
                            row.project_uuid    = entity['metadata']['project_reference']['uuid']
                            row.project_name    = entity['metadata']['project_reference']['name']
                            # This code is intented to capture project's subnets specifications
                            subnets = []
                            try:
                                for subnet in entity['spec']['resources']['subnet_reference_list']:
                                    for s in current['subnets']:
                                        if s.uuid == subnet['uuid']:
                                            subnets.append(f"{s.uuid}:{s.name}")
                            except Exception as e:
                                logger.debug(f"{this()}: Getting Project's Subnets exception: {str(e)}")
                            row.project_subnets = ','.join(subnets)
                            logger.debug(f'{this()}: Project: {row.project_name}')
                            logger.debug(f'{this()}: Project Subnets: {len(subnets)} {row.project_subnets}')
                            rows.append(row)
                        except:
                            pass
                else:
                    logger.warning(f"{this()}: no project_reference available for uuid: {entity['metadata'].get('uuid')}")
            except Exception as e:
                logger.error(f'{this()}: exception: {str(e)}')
                logger.error(f"{this()}: entity['metadata']: {entity['metadata']}")
                                    
        # rows contains all Projects from Nutanix
        # only these projects should remain in butler
        try:
            keep=[]
            for row in rows:
                db.session.merge(row)
                keep.append(row.project_uuid)
                logger.trace(f'{this()}: project={row}')
            db.session.commit()
            db.session.flush()
            logger.debug(f"{this()}: Got: {len(rows)} Projects.")
            if len(rows):
                current['projects']=rows
                # delete obsolete codes
                rows_to_delete = db.session.query(Projects
                    ).filter(Projects.project_uuid.notin_(keep)
                    ).all()
                logger.debug(f'{this()}: Projects to delete = {len(rows_to_delete)}')
                for row in rows_to_delete:
                    db.session.delete(row)
                db.session.commit()
                db.session.flush()
        except Exception as e:
            db.session.rollback()
            tracebox_log(f'{this()}: exception = {str(e)}',
                logger = logger,
                level  = logging.ERROR,
                length = tracebox_log_length
                )
                                                
        # Prepare API Response
        result = get_api_response(
            # status arguments
            state = 'OK',
            code = 0,
            message = f"{this()}: Got: {len(rows)} Projects.",
            execution_context = None,
            # metadata
            total_matches = len(rows),
            kind = 'disk image',
            length = len(rows),
            offset = 0,
            )
    else:
        result = get_api_response(
            # status arguments
            state = 'ERROR',
            code = 1,
            message = f'{this()}: No Projects found.',
            execution_context = None,
        )
    logger.debug(f'{this()}: OUT')
    tracebox_log(f'{this()}: {str(result)}',
            logger=logger,level=logging.DEBUG,length=tracebox_log_length)
    return result

# Update CAtegories from Nutanix Prism Central -------------------------
def trx_uca_update_butler_categories(app):
    logger.debug(f'{this()}: IN Get Nutanix Categories ...')
    result   = get_api_response(    code=BUTLER_CORE_TRX_ERROR,
                                    message=f'NO TRX RESPONSE')
    
    host     = app.config.get('NUTANIX_HOST')
    port     = app.config.get('NUTANIX_PORT')
    username = app.config.get('NUTANIX_USERNAME')
    password = app.config.get('NUTANIX_PASSWORD')
    protocol = app.config.get('NUTANIX_PROTOCOL')
    timeout  = app.config.get('NUTANIX_TIMEOUT',5)
    # 20210528 GV endpoint = 'api/nutanix/v3/categories/list'
    endpoint = 'api/nutanix/v3/categories/Environment/list'
    arguments=''
    
    headers  = {'Content-Type': 'application/json'}
    data     = {'kind': 'category'}
    url      = f'{protocol}://{host}:{port}/{endpoint}{arguments}'

    logger.debug(f'{this()}: user = {username}')
    logger.debug(f'{this()}: url  = {url}')

    categories = api_request('POST',
                    url,
                    data=json.dumps(data),
                    headers=headers,
                    username=username,
                    password=password,
                    timeout=timeout,
                    logger   = logger
                    )        

    if categories is not None:
        data = categories.json()
        rows=[]
        if categories.status_code == 200:
            #if data_clusters['status']['code'] == 0:
            # Actual process of result here
            for entity in categories.json()['entities']:
                # 20210528 GV if not entity['system_defined']:
                if not entity['system_defined']:
                # 20210601 GV if True:
                    try:
                        row=Categories()
                        # 20210528 row.category_name = entity['name']
                        row.category_name = entity['value']
                        row.category_description = entity['description']
                        rows.append(row)
                        logger.debug(f'{this()}: Category: {row.category_name}')
                    except:
                        pass

            # rows contains all Categories from Nutanix
            # only these projects should remain in butler
            try:
                keep=[]
                for row in rows:
                    db.session.merge(row)
                    keep.append(row.category_name)
                db.session.commit()
                db.session.flush()
                logger.debug(f"{this()}: Got: {len(rows)} Categories.")
                if len(rows):
                    current['categories']=rows
                    # delete obsolete codes
                    rows_to_delete = db.session.query(Categories
                        ).filter(Categories.category_name.notin_(keep)
                        ).all()
                    logger.debug(f'{this()}: Categories to delete = {len(rows_to_delete)}')
                    for row in rows_to_delete:
                        db.session.delete(row)
                    db.session.commit()
                    db.session.flush()
            except Exception as e:
                db.session.rollback()
                tracebox_log(f'{this()}: exception = {str(e)}',
                    logger = logger,
                    level  = logging.ERROR,
                    length = tracebox_log_length
                    )

        # Prepare API Response
        result = get_api_response(
            # status arguments
            state = 'OK',
            code = 0,
            message = f"{this()}: Got: {len(rows)} Categories.",
            execution_context = None,
            # metadata
            total_matches = len(rows),
            kind = 'Categories',
            length = len(rows),
            offset = 0,
            )
    else:
        result = get_api_response(
            # status arguments
            state = 'ERROR',
            code = 1,
            message = f'{this()}: No Categories found.',
            execution_context = None,
        )
    logger.debug(f'{this()}: OUT')
    tracebox_log(f'{this()}: {str(result)}',
            logger=logger,level=logging.DEBUG,length=tracebox_log_length)
    return result

# Update SubNets from Nutanix Prism Central Projects -------------------
def trx_usn_update_butler_subnets(app):
    logger.debug(f'{this()}: IN Get Nutanix Subnets ...')
    result   = get_api_response(    code=BUTLER_CORE_TRX_ERROR,
                                    message=f'NO TRX RESPONSE')
    
    host     = app.config.get('NUTANIX_HOST')
    port     = app.config.get('NUTANIX_PORT')
    username = app.config.get('NUTANIX_USERNAME')
    password = app.config.get('NUTANIX_PASSWORD')
    protocol = app.config.get('NUTANIX_PROTOCOL')
    timeout  = app.config.get('NUTANIX_TIMEOUT',5)
    endpoint = 'api/nutanix/v3/subnets/list'
    arguments=''
    
    headers  = {'Content-Type': 'application/json'}
    data     = {'kind': 'subnet'}
    url      = f'{protocol}://{host}:{port}/{endpoint}{arguments}'

    logger.debug(f'{this()}: user = {username}')
    logger.debug(f'{this()}: url  = {url}')

    subnets = api_request('POST',
                    url,
                    data=json.dumps(data),
                    headers=headers,
                    username=username,
                    password=password,
                    timeout=timeout,
                    logger   = logger
                    )        

    if subnets is not None:
        rows=[]
        if subnets.status_code == 200:
            # Actual process of result here
            data = subnets.json()
            logger.debug(f"{this()}: Subnets = {len(data['entities'])}")
            for entity in data['entities']:
                logger.trace(pformat(entity))
                try:
                    row=Subnets()
                    row.uuid         = entity['metadata']['uuid']
                    row.name         = entity['spec']['name']
                    row.vlan_id      = entity['spec']['resources']['vlan_id']
                    row.vswitch_name = entity['spec']['resources']['vswitch_name']
                    row.type         = entity['spec']['resources']['subnet_type']
                    if entity.get('spec').get('resources').get('ip_config') is not None:
                        row.default_gateway_ip = entity['spec']['resources']['ip_config']['default_gateway_ip']
                        row.range              = entity['spec']['resources']['ip_config']['pool_list'][0]['range']
                        row.prefix_length      = entity['spec']['resources']['ip_config']['prefix_length']
                        row.subnet_ip          = entity['spec']['resources']['ip_config']['subnet_ip']
                    else:
                        logger.info(f"{this()}: WARNING Incomplete Subnet '{row.name}' no IP configuration.")
                    row.cluster      = entity['spec']['cluster_reference']['uuid']
                    rows.append(row)
                    logger.debug(f'{this()}: Subnet: {row.name}')
                except Exception as e:
                    logger.error(f'{this()}: Incomplete Subnet {row.name} exception: {str(e)}')

            # rows contains all Subnets from Nutanix
            # only these projects should remain in butler
            try:
                keep=[]
                for row in rows:
                    db.session.merge(row)
                    keep.append(row.uuid)
                db.session.commit()
                db.session.flush()
                logger.debug(f"{this()}: Got: {len(rows)} Complete Subnets.")
                if len(rows):
                    current['subnets']=rows
                    # delete obsolete codes
                    rows_to_delete = db.session.query(Subnets
                        ).filter(Subnets.uuid.notin_(keep)
                        ).all()
                    logger.debug(f'{this()}: Subnets to delete = {len(rows_to_delete)}')
                    for row in rows_to_delete:
                        db.session.delete(row)
                    db.session.commit()
                    db.session.flush()
            except Exception as e:
                db.session.rollback()
                tracebox_log(f'{this()}: exception = {str(e)}',
                    logger = logger,
                    level  = logging.ERROR,
                    length = tracebox_log_length
                    )

        # Prepare API Response
        result = get_api_response(
            # status arguments
            state = 'OK',
            code = 0,
            message = f"{this()}: Got: {len(rows)} Subnets.",
            execution_context = None,
            # metadata
            total_matches = len(rows),
            kind = 'disk image',
            length = len(rows),
            offset = 0,
            )
    else:
        result = get_api_response(
            # status arguments
            state = 'ERROR',
            code = 1,
            message = f'{this()}: No Subnets found.',
            execution_context = None,
        )
    logger.debug(f'{this()}: OUT')
    tracebox_log(f'{this()}: {str(result)}',
            logger=logger,level=logging.DEBUG,length=tracebox_log_length)
    return result

# Request is approved but not VM Creation requested yet ----------------
def trx_001_not_nutanix_pending(app):
    logger.info(f'{this()}: IN Get approved Requests and create VM')
    # query for matching rows for transaction
    # API Version hard coded here need to variabilize it 
    API_Version = '3.1.0'
    trx = TRX_EGB_NO_NTX_PENDING
    try:
        rows = butler_trx_get(transaction=trx,session=db.session,logger=logger)
        # process result here
        if rows is not None and len(rows):
            logger.debug(f'Transaction {BUTLER_TRANSACTIONS[trx]}: {len(rows)} rows found : ')
            for row in rows:
                # Process row here
                # For transaction 001
                # build Nutanix Request
                logger.debug(f'{this()}: processing row = {row}')
                #print(f'{this()}: processing Solicitud = {row}')
                host      = app.config['NUTANIX_HOST']
                port      = app.config['NUTANIX_PORT']
                username  = app.config['NUTANIX_USERNAME']
                password  = app.config['NUTANIX_PASSWORD']
                protocol  = app.config['NUTANIX_PROTOCOL']
                # This is a default VM Project Configuration
                project   = {   
                    'name': app.config.get('NUTANIX_PROJECT','Butler'),
                    'uuid': app.config.get('NUTANIX_PROJECT_UUID',None),
                }
                # Overrides default project UUID from DB record
                if row.Nutanix_Prism_VM.project_uuid is not None:
                    project['uuid'] = row.Nutanix_Prism_VM.project_uuid
                    # project['name'] will be completed later bellow ...

                endpoint  = 'api/nutanix/v3/vms'
                url       = f'{protocol}://{host}:{port}/{endpoint}'
                headers   = {'Content-Type':'application/json'}
                disk_list = []
                nic_list  = []
                # Load Disk List ---------------------------------------
                logger.debug(f'{this()}: procesing disks')
                for i in range(12):
                    size  = getattr(row.Nutanix_Prism_VM,f'disk_{i}_size')
                    if i==0:
                        image = getattr(row.Nutanix_Prism_VM,f'disk_{i}_image')
                    else:
                        image = None
                    disk  = {}
                    if size or (image is not None and len(image)):
                        # If Disk Size is requested --------------------
                        if size:    disk.update({
                                'disk_size_mib':size*1024,
                                'device_properties':{
                                    'device_type':'DISK'
                                },
                            })
                        # If Base Image is provided --------------------
                        if image is not None:   disk.update({
                                'data_source_reference':{
                                    'kind':'image',
                                    'uuid':image
                                }
                            })
                        disk_list.append(disk)
                # CDROM option here ... ********************************
                if row.Nutanix_Prism_VM.vm_cdrom:
                    cdrom = { 
                        "device_properties": {
                            "device_type": "CDROM"
                        }
                    }
                    disk_list.append(cdrom)
                # ******************************************************
                # Try to get proper project UUID -----------------------
                logger.debug(f"{this()}: current['projects']={current['projects']}")
                if project['uuid'] is None:
                    #print(f"project[uuid] is None")
                    if project['name'] is None:
                        if len(current['projects']):
                            project['name'] = current['projects'][0].project_name
                            project['uuid'] = current['projects'][0].project_uuid
                            logger.debug(f"{this()}: Default Project {project['name']} set up as per 1st current project")
                        else:
                            project['name'] = app.config.get('NUTANIX_PROJECT',None)
                            project['uuid'] = app.config.get('NUTANIX_PROJECT_UUID',None)
                            logger.debug(f"{this()}: Default Project {project['name']} set up as per configurarion")
                    else:
                        found = False
                        for p in current['projects']:
                            if p.project_name == project['name']:
                                project['uuid'] = p.project_uuid
                                found = True
                                logger.debug(f"{this()}: Project Name {project['name']} found in current projects ({project['uuid']})")
                                break
                        if not found:
                            project['uuid'] = None
                else:
                    found = False
                    for p in current['projects']:
                        if p.project_uuid == project['uuid']:
                            project['name'] = p.project_name
                            found = True
                            logger.debug(f"{this()}: Project UUID {project['uuid']} found in current projects ({project['name']})")
                            break
                    if not found:
                        project['uuid'] = None
                logger.debug(f'{this()}: project = {project}')
                #print(f"row.Nutanix_Prism_VM.project_uuid={row.Nutanix_Prism_VM.project_uuid}")
                #print(f"**********************************************")
                # Load NIC List ----------------------------------------
                # Depends on Project
                # Check for populated project's UUID
                if row.Nutanix_Prism_VM.project_uuid is None:
                    row.Nutanix_Prism_VM.project_uuid = project['uuid']
                # populates project's available subnets
                if row.Nutanix_Prism_VM.project_uuid is not None and row.Nutanix_Prism_VM.project_uuid != '0':
                    logger.debug(f"{this()}: populates project's available subnets")
                    # subnet depends of actual project
                    # As a default a NIC for each subnet should be
                    # created 
                    # get subnets for project here
                    
                    #subnets = [(None,None),]
                    # load subnets for this project
                    subnets = []
                    for p in current['projects']:
                        if p.project_uuid == row.Nutanix_Prism_VM.project_uuid:
                            for s in p.project_subnets.split(','):
                                subnets.append((s+':').split(':'))
                    nic_list=[]
                    # Will create a NIC for each subnet in project
                    
                    # Will check all required subnets, if any
                    # First consolidates all requested subnets
                    # and filter for unique items in list
                    subnets_list = unique_list([
                        row.Nutanix_Prism_VM.nic_0_vlan,
                        row.Nutanix_Prism_VM.nic_1_vlan,
                        row.Nutanix_Prism_VM.nic_2_vlan,
                        row.Nutanix_Prism_VM.nic_3_vlan
                        ])
                    
                    logger.debug(f"{this()}: project's available subnets = {subnets}")
                    for subnet in subnets_list:
                        logger.debug(f'{this()}: requested subnet = {subnet}')
                        # Will check all subnets in project, if any
                        if subnet is not None and len(str(subnet).strip()):
                            found = False
                            for subnet_uuid,subnet_name,filler in subnets:
                                # if subnet required matches valid subnet
                                # in project
                                if subnet == subnet_uuid:
                                    nic = {
                                        'nic_type': 'NORMAL_NIC',
                                        'is_connected': True,
                                        'subnet_reference': {
                                            'kind': 'subnet',
                                            'name': subnet_name,
                                            'uuid': subnet_uuid
                                        }
                                    }
                                    # Reserved for IP inclusion in request 
                                    #'ip_endpoint_list':[
                                    #    #{'ip_type': 'DHCP'}
                                    #],
                                    nic_list.append(nic)
                                    found = True
                                    break
                            if found:
                                logger.debug(f'{this()}: subnet {subnet_name}:{subnet_uuid} included in VM creation request.')
                            else:
                                logger.error(f'{this()}: subnet {subnet} was not found for project:{row.Nutanix_Prism_VM.project_uuid}')
                        else:
                            pass
                else:
                    logger.warning(f'{this()}: Invalid project uuid:{row.Nutanix_Prism_VM.project_uuid}')
                # load disk list here
                logger.debug(f'{this()}: building VM creation request data ...')
                data     = {
                'spec':{
                    'description': row.Nutanix_Prism_VM.vm_name,
                    'name': row.Nutanix_Prism_VM.vm_name,
                    'resources':{
                        'power_state'         : 'ON',
                        'num_vcpus_per_socket': row.Nutanix_Prism_VM.vcpus_per_socket,
                        'num_sockets'         : row.Nutanix_Prism_VM.num_sockets,
                        'memory_size_mib'     : row.Nutanix_Prism_VM.memory_size_gib*1024,
                        'disk_list'           : disk_list,
                        'nic_list'            : nic_list,
                        },
                    'cluster_reference': {
                        'kind': 'cluster',
                        'uuid': row.Nutanix_Prism_VM.cluster_uuid
                        }
                    },
                'api_version': API_Version,
                'metadata':{
                    'kind'                    : 'vm',
                    'project_reference'       : {
                        'kind': 'project',
                        'name': project['name'],
                        'uuid': project['uuid']
                        },
                    
                    },
                }
                # 20210601 Includes conditional boot configuration
                if app.config.get('BUTLER_BOOT_TYPE') is not None:
                    if row.Nutanix_Prism_VM.vm_cdrom:
                        device_order_list = ['CDROM','DISK','NETWORK']
                    else:
                        device_order_list = ['DISK','NETWORK']
                    boot_config = {
                        'boot_device_order_list':device_order_list,
                        'boot_type':str(app.config.get('BUTLER_BOOT_TYPE')).upper()
                    }
                    data['spec']['resources'].update({'boot_config':boot_config})
                    logger.debug(f"{this()}: boot_config={boot_config}")
                # 20210518 add category upon request
                if row.Nutanix_Prism_VM.category_name is not None:
                    data['metadata'].update({
                        'use_categories_mapping' : True,
                        'categories_mapping' : {
                            # 20210528 GV row.Nutanix_Prism_VM.category_name : [row.Nutanix_Prism_VM.category_name]
                            'Environment' : [row.Nutanix_Prism_VM.category_name]
                            }
                        })

                # ------------------------------------------------------
                # Actual VM Creation Request here
                # get Nutanix Response
                # First check that VM is not existent
                #print         (f'{this()}: search for existing VM ...')
                logger.debug(f'{this()}: search for existing VM ...')
                vm = get_nutanix_vm(app,row.Nutanix_Prism_VM.vm_name)
                if vm is None:
                    #print         (f'{this()}: VM does not exists, creating ...')
                    logger.debug(f'{this()}: VM does not exists, creating ...')
                    logger.debug(f'{this()}: url     =  {url}')
                    logger.debug(f'{this()}: headers =  {headers}')
                    logger.trace(f'{this()}: data    = {data}') # <------- TRACE HERE
                    logger.trace(f'{this()}: json    = {json.dumps(data)}') # <------- TRACE HERE
                    response = api_request(    
                                    'POST',
                                    url,
                                    data=json.dumps(data),
                                    headers=headers,
                                    username=username,
                                    password=password,
                                    logger   = logger
                                )
                    logger.debug(f'{this()}: response = {response}')
                    trace_trx(this(),app,row,response)
                    if response is not None:
                        if response.ok:
                            logger.debug(f'{this()}: response = {response} is OK')
                            data = response.json()
                            logger.debug(f"{this()}: status state = {data['status']['state']} is OK")
                            if data['status']['state'] == 'PENDING':
                                row.Requests.Task_uuid   = data['status']['execution_context']['task_uuid']
                                row.Requests.Task_status = 0
                                row.Requests.uuid        = data['metadata']['uuid']
                                row.Requests.Status = turn_on(row.Requests.Status,NUTANIX_PENDING)
                                row.Requests.Comments = '' if row.Requests.Comments is None else row.Requests.Comments
                                row.Requests.Comments += f"Provisionando @ {strftime('%d/%m/%y %H:%M')}..."
                                row.Nutanix_Prism_VM.vm_uuid = data['metadata']['uuid']
                                db.session.merge(row.Requests)
                                db.session.merge(row.Nutanix_Prism_VM)
                                db.session.commit()
                                db.session.flush()
                                logger.info(f'{this()}: request {row.Requests.Id} updated. provissioning PENDING.')
                            elif data['status'] == 'SUCCEEDED':
                                row.Requests.Task_status = 1
                                row.Requests.Status = turn_on(row.Requests.Status,NUTANIX_COMPLETED)
                                row.Requests.Comments = '' if row.Comments is None else row.Comments
                                row.Requests.Comments += f"Provisionada @ {strftime('%d/%m/%y %H:%M')}."
                                db.session.merge(row.Requests)
                                db.session.commit()
                                db.session.flush()
                                logger.info(f'{this()}: request {row.Requests.Id} updated. Provissioned. SUCCEEDED.')                    
                        else:   
                            logger.error(f'{this()}: response.status_code = {response.status_code}')
                            logger.error(f'{this()}: response.reason      = {response.reason}')
                            logger.error(f'{this()}: response.text        = {response.text}')
                    else:
                        logger.critical(f'{this()}: response = {response} No response from API request {url}')
                else:
                    logger.error(f"{this()}: VM '{row.Nutanix_Prism_VM.vm_name}' ya existe en NUTANIX {host}")
                    row.Requests.Status = turn_on(row.Requests.Status,REQUEST_ERROR)
                    row.Requests.Comments = '' if row.Requests.Comments is None else row.Requests.Comments
                    row.Requests.Comments += f"Error MV ya existe @ {strftime('%d/%m/%y %H:%M')}."
                    db.session.merge(row.Requests)
                    db.session.merge(row.Nutanix_Prism_VM)
                    db.session.commit()
                    db.session.flush()
                    logger.debug(f'{this()}: {row.Requests} updated')
                # ------------------------------------------------------
            result   =  get_api_response(   code=BUTLER_CORE_TRX_OK,
                            message=f'{this()}: trx: {trx} : {len(rows)} Requests processed.'
                            )
        else:
            result   =  get_api_response(   code=BUTLER_CORE_TRX_OK,
                            message=f'{this()}: No rows for trx {trx}'
                            )
        logger.debug(f'{this()}: normal function completion')
    except Exception as e:
        tracebox_log(f'{this()}: exception = {str(e)}',
            logger = logger,
            level  = logging.CRITICAL,
            length = tracebox_log_length
            )
        result   =  get_api_response(   code=BUTLER_CORE_TRX_ERROR,
                        message=f'{this()}: Exception: {str(e)}'
                        )

    logger.debug(f'{this()}: OUT')
    tracebox_log(f'{this()}: {str(result)}',
            logger=logger,level=logging.DEBUG,length=tracebox_log_length)
    return result

# Request is approved but CC is not populated in EG Collector ----------
def trx_002_not_collector_pending(app):
    logger.info(f'{this()}: IN Get Approved, seach in EG Collector and update CC ...')
    # query for matching rows for transaction
    trx = TRX_EGB_NO_EGC_PENDING
    try:
        logger.debug(f"******** ENTER TRX 002 EG COLLECTOR POPULATION *******")
        rows = butler_trx_get(transaction=trx,session=db.session,logger=logger)
        logger.debug(f'Transaction {BUTLER_TRANSACTIONS[trx]}: {len(rows)} rows found.')
        # process result here
        if rows is not None and len(rows):
            logger.debug(f'Transaction {BUTLER_TRANSACTIONS[trx]}: {len(rows)} rows found : ')
            for row in rows:
                # Process row here
                # For transaction 002
                # Update Collector VM with proper CC
                host      = app.config['COLLECTOR_HOST']
                port      = app.config['COLLECTOR_PORT']
                username  = app.config['COLLECTOR_USERNAME']
                password  = app.config['COLLECTOR_PASSWORD']
                protocol  = app.config['COLLECTOR_PROTOCOL']
                # Search for CI Id
                endpoint  = f'api/get/Configuration_Items'
                data      = {'CI_Name':row.Nutanix_Prism_VM.vm_name}
                url       = f'{protocol}://{host}:{port}/{endpoint}'
                headers   = ''
                response = api_request(    
                                'GET',
                                url,
                                data=data,
                                headers=headers,
                                username=username,
                                password=password,
                                logger   = logger
                            )
                if response is not None:
                    CI = response.json()
                    if response.ok and len(CI['entities']):
                        endpoint  = f"api/patch/Configuration_Items/{CI['entities'][0]['CI_Id']}"
                        url       = f'{protocol}://{host}:{port}/{endpoint}'
                        headers   = ''
                        data      = {'CC_Id':row.Requests.CC_Id}
                        # get Nutanix Response
                        logger.debug(f'{this()}: url = {url}')
                        
                        response = api_request(    
                                        'PATCH',
                                        url,
                                        data=data,
                                        headers=headers,
                                        username=username,
                                        password=password,
                                        logger   = logger
                                    )
                        trace_trx(this(),app,row,response)
                        if response is not None:
                            if response.ok:
                                data=response.json()                                
                                if data['status']['state'] == 'OK':
                                    row.Requests.Status    = turn_on(row.Requests.Status,COLLECTOR_COMPLETED)
                                    row.Requests.Comments  = '' if row.Requests.Comments is None else row.Requests.Comments
                                    row.Requests.Comments += f"Tarificada @ {strftime('%d/%m/%y %H:%M')}."
                                    db.session.merge(row.Requests)
                                    db.session.commit()
                                    db.session.flush()
                                    logger.info(f'{this()}: request {row.Requests.Id} updated. EG Collector CC populated.')
                                else:
                                    logger.error(f"{this()}: response status: {data['status']['state']}")
                            else:
                                logger.error(f'{this()}: response.status_code = {response.status_code}')
                                logger.error(f'{this()}: response.reason      = {response.reason}')
                                logger.error(f'{this()}: response.text        = {response.text}')
                        else:
                            logger.error(f'{this()}: response = {response}')
                    else:
                        logger.warning(f"{this()}: CI '{data['CI_Name']}' not found in Collector.")
                        logger.warning(f"{this()}: response = {response}.")
                        logger.warning(f"{this()}: CI = {CI}.")
                else:
                    logger.error(f"{this()}: no response from Collector ({url} {data}).")                    
            result   =  get_api_response(   code=BUTLER_CORE_TRX_OK,
                            message=f'{this()}: trx: {trx} : {len(rows)} CIs updated.'
                            )
        else:
            result   =  get_api_response(   code=BUTLER_CORE_TRX_OK,
                            message=f'{this()}: No rows for trx {trx}'
                            )
        logger.debug(f"******** EXIT TRX 002 EG COLLECTOR POPULATION ********")
    except Exception as e:
        tracebox_log(f'{this()}: exception = {str(e)}',
            logger = logger,
            level  = logging.CRITICAL,
            length = tracebox_log_length
            )
        result   =  get_api_response(   code=BUTLER_CORE_TRX_ERROR,
                        message=f'{this()}: Exception: {str(e)}'
                        )

    logger.debug(f'{this()}: OUT')
    tracebox_log(f'{this()}: {str(result)}',
            logger=logger,level=logging.DEBUG,length=tracebox_log_length)
    return result

# Nutanix VM Creation was requested, checks for completion -------------
def trx_003_nutanix_pending(app):
    logger.info(f'{this()}: IN Search task and sets completion ...')
    # query for matching rows for transaction
    trx = TRX_EGB_NTX_PENDING
    try:
        rows = butler_trx_get(transaction=trx,session=db.session,logger=logger)
        # process result here
        if rows is not None and len(rows):
            logger.info(f'Transaction {BUTLER_TRANSACTIONS[trx]}: {len(rows)} requests found : ')
            for row in rows:
                logger.debug(f"{this()}: Request = {row.Id}")
                # Process row here
                # For transaction 003
                # build Nutanix Request for task status
                host      = app.config['NUTANIX_HOST']
                port      = app.config['NUTANIX_PORT']
                username  = app.config['NUTANIX_USERNAME']
                password  = app.config['NUTANIX_PASSWORD']
                protocol  = app.config['NUTANIX_PROTOCOL']
                endpoint  = f'api/nutanix/v3/tasks/{row.Task_uuid}'
                url       = f'{protocol}://{host}:{port}/{endpoint}'
                headers   = ''
                data     = {}
                # get Nutanix Response
                logger.debug(f'{this()}: url = {url}')
                
                response = api_request(    
                                'GET',
                                url,
                                data=data,
                                headers=headers,
                                username=username,
                                password=password,
                                logger   = logger
                            )
                logger.debug(f'{this()}: response = {response}')
                trace_trx(this(),app,row,response)
                if response is not None:
                    if response.ok:
                        try:
                            data=response.json()
                            logger.warning(f"data status = {data.get('status')}")
                            if data['status'] == 'SUCCEEDED':
                                row.Task_status = 1
                                row.Status = turn_off(row.Status,NUTANIX_PENDING)
                                row.Status = turn_on (row.Status,NUTANIX_COMPLETED)
                                row.Comments = '' if row.Comments is None else row.Comments
                                row.Comments += f"Provisionada @ {strftime('%d/%m/%y %H:%M')}."
                                db.session.merge(row)
                                db.session.commit()
                                db.session.flush()
                                logger.info(f'{this()}: request {row.Id} updated. Provissioned.')
                                # NOTIFY PROVISSION TO SUPPORT FOR ADM COMPLETION
                                if app.config.get('BUTLER_REQUEST_NOTIFICATIONS'):
                                    try:
                                        rox = db.session.query(Nutanix_Prism_VM).filter(Nutanix_Prism_VM.Request_Id == row.Id).one_or_none()
                                        # Collect user and approver emails
                                        User_email = db.session.query(Users.email).filter(Users.id==row.User_Id).one_or_none()
                                        Approver_email = db.session.query(Users.email).filter(Users.id==row.Approver_Id).one_or_none()
                                        if User_email     is None: User_email=(None,)
                                        if Approver_email is None: Approver_email=(None,)
                                        # Setup required data
                                        
                                        data = Get_data_context(app=app,db=db,mail=mail,Id=Id)

                                        data.update({
                                            'top_cost_center_code':app.config.get('BUTLER_TOP_COST_CENTER'),
                                            'requestor_email': User_email[0],
                                            'approver_email': Approver_email[0],
                                            'row'   : row,
                                            'rox'   : rox,
                                            'app'   : app,
                                            'db'    : db,
                                            'mail'  : mail,
                                            'role'  : ROLE_VIEWER,
                                            'roles' : ROLES,
                                            'status': BUTLER_STATUS,
                                        })
                                        logger.debug(f"data.keys()={data.keys()}")        
                                        To = app.config.get('BUTLER_SUPPORT_NOTIFICATION')
                                                                                
                                        butler_notify_request(
                                            subject_detail=f"Maquina Virtual PROVISIONADA",
                                            data=data,
                                            recipients=To.split(','),
                                            html_function=butler_output_request
                                            )
                                    except Exception as e:
                                        emtec_handle_general_exception(e,logger=logger,fp=sys.stderr)
                                else:
                                    logger.info(f"{this()}: request {row.Id} Notification not required.")
                                # --------------------------------------
                            elif data['status'] == 'RUNNING':                            
                                # Catches task working now ...
                                logger.warning(f'{this()}: request {row.Id} still being Provissioned ...')
                            else:
                                logger.error(f"{this()}: response.ok status={data['status']}")
                                row.Status = turn_on(row.Status,NUTANIX_ERROR)
                                row.Status = turn_on(row.Status,REQUEST_ERROR)
                                row.Comments = '' if row.Comments is None else row.Comments
                                try:
                                    row.Comments += f"Error @ {strftime('%d/%m/%y %H:%M')}. {data['error_detail']}."
                                except:
                                    row.Comments += f"Error @ {strftime('%d/%m/%y %H:%M')}."
                                db.session.merge(row)
                                db.session.commit()
                                db.session.flush()
                                logger.error(f'{this()}: request {row.Id} updated. FAILED.')
                                try:
                                    tracebox_log(f"{this()}: Request = {row.Id} {data['error_detail']}",
                                        logger=logger,level=logging.ERROR,length=tracebox_log_length)
                                except Exception as e:
                                    tracebox_log(f"{this()}: status={data['status']} log exception = {str(e)}",
                                        logger = logger,
                                        level  = logging.ERROR,
                                        length = tracebox_log_length
                                        )
                        except Exception as e:
                            logger.error(f'{this()}: response.ok exception = {str(e)}')
                    else:
                        logger.error(f'{this()}: response.status_code = {response.status_code}')
                        logger.error(f'{this()}: response.reason      = {response.reason}')
                        logger.error(f'{this()}: response.text        = {response.text}')
                        logger.error(f"{this()}: response.ok=False status={data['status']}")
                else:
                    logger.error(f'{this()}: response = {response}')
            result   =  get_api_response(   code=BUTLER_CORE_TRX_OK,
                            message=f'{this()}: trx: {trx} : {len(rows)} Tasks processed.'
                            )
        else:
            result   =  get_api_response(   code=BUTLER_CORE_TRX_OK,
                            message=f'{this()}: No rows for trx {trx}'
                            )
    except Exception as e:
        tracebox_log(f'{this()}: exception = {str(e)}',
            logger = logger,
            level  = logging.CRITICAL,
            length = tracebox_log_length
            )
        result   =  get_api_response(   code=BUTLER_CORE_TRX_ERROR,
                        message=f'{this()}: Exception: {str(e)}'
                        )

    tracebox_log(f'{this()}: result={str(result)}',
            logger=logger,
            level=logging.DEBUG,
            length=tracebox_log_length
        )
    logger.debug(f'{this()}: OUT')
    return result

# If VM is Nutanix provisioned and has a valid IP address, then --------
# sets up EG Monitor Host creation
def trx_004_nutanix_completed(app,timeout=None):
    logger.info(f'{this()}: IN Get Created VM and set up Replicas ...')
    # query for matching rows for transaction
    # 20210529 GV trx = TRX_EGB_NTX_OK_NO_IP
    trx = TRX_EGB_NTX_OK
    try:
        rows = butler_trx_get(transaction=trx,session=db.session,logger=logger)
        # process result here
        if rows is not None and len(rows):
            logger.warning(f'Transaction {BUTLER_TRANSACTIONS[trx]}: {len(rows)} rows found : ')
            for row in rows:
                # Process row here
                # For transaction 004
                # Load Nutanix VM  and get IP Address to setup Monitoring
                host      = app.config['NUTANIX_HOST']
                port      = app.config['NUTANIX_PORT']
                username  = app.config['NUTANIX_USERNAME']
                password  = app.config['NUTANIX_PASSWORD']
                protocol  = app.config['NUTANIX_PROTOCOL']
                #'https://10.26.1.247:5665/v1/objects/hosts?filter=match(%22aix-director%22,host.name)'
                #endpoint  = f'v1/objects/hosts?filter=match("{row.uuid}",host.name)'
                endpoint  = f'api/nutanix/v3/vms/{row.Requests.uuid}'
                url       = f'{protocol}://{host}:{port}/{endpoint}'
                headers   = ''
                data     = {}
                # get Nutanix Response
                logger.warning(f'{this()}: url = {url}')
                
                response = api_request(    
                                'GET',
                                url,
                                data=data,
                                headers=headers,
                                username=username,
                                password=password,
                                logger   = logger
                            )
                trace_trx(this(),app,row,response)
                if response is not None:
                    data=response.json()
                    if response.ok:
                        #print(f"ENTER DATA PROTECTION BLOCK")
                        Setup_Monitoring = True
                        # DATA PROTECTION BLOCK STARTS HERE ------------
                        if row.Nutanix_Prism_VM.vm_drp or row.Nutanix_Prism_VM.vm_drp_remote:
                            VM_Protected = True
                            # Oportunity check for DRP Schedule ------------
                            # implementation. requires:
                            # row.Nutanix_Prism_VM.vm_name
                            # Using defaults oportunity for customization
                            # 20210503 Se modifico para implementar doble 
                            # creacion de replicas: Locales y Remotas
                            # **********************************************
                            # Falta probar y validar 
                            # **********************************************
                            # Common arguments
                            pdname                      = None
                            annotation                  = None
                            user_start_time_in_usecs    = None
                            timeout                     = app.config.get('NUTANIX_TIMEOUT',5)
                            remote_cluster              = app.config.get('NUTANIX_REMOTE_CLUSTER',None)
                            # Local replicas 
                            local_schedule_type         = app.config.get('NUTANIX_LOCAL_SCHEDULE_TYPE','DAILY')
                            local_every_nth             = app.config.get('NUTANIX_LOCAL_EVERY_NTH',1)
                            local_max_snapshots         = app.config.get('NUTANIX_LOCAL_LOCAL_MAX_SNAPSHOTS',0)
                            local_remote_max_snapshots  = app.config.get('NUTANIX_LOCAL_REMOTE_MAX_SNAPSHOTS',0)
                            # Remote replicas
                            remote_schedule_type        = app.config.get('NUTANIX_REMOTE_SCHEDULE_TYPE','HOURLY')
                            remote_every_nth            = app.config.get('NUTANIX_REMOTE_EVERY_NTH',1)
                            remote_max_snapshots        = app.config.get('NUTANIX_REMOTE_LOCAL_MAX_SNAPSHOTS',0)
                            remote_remote_max_snapshots = app.config.get('NUTANIX_REMOTE_REMOTE_MAX_SNAPSHOTS',0)
                            # if local replicas are required
                            # a protection domain is created and an schedule
                            # is configured for local replicas
                            # optionaly, remote copies of local replicas can 
                            # be created , note, will be recognized as
                            # remote copies anyway
                            
                            # Populated upon Request Status ************
                            
                            Protection_Complete   = has_status(row.Requests.Status,NUTANIX_PROTECTED)
                            Protection_Uncomplete = not Protection_Complete
                            logger.warning(f"{this()}: Protection_Uncomplete = {Protection_Uncomplete}")
                            #print         (f"{this()}: Protection_Uncomplete = {Protection_Uncomplete}")
                            # Check for Local Security copies
                            try:
                                if row.Nutanix_Prism_VM.vm_drp and Protection_Uncomplete:
                                    logger.info(f"{this()}: Local security copies requested for VM: '{row.Nutanix_Prism_VM.vm_name}'")
                                    success,pdname = create_drp(
                                            app,
                                            vmname                   = row.Nutanix_Prism_VM.vm_name,
                                            pdname                   = pdname,
                                            annotation               = annotation,
                                            remote_cluster           = remote_cluster,
                                            schedule_type            = local_schedule_type,
                                            user_start_time_in_usecs = user_start_time_in_usecs,
                                            every_nth                = local_every_nth,
                                            local_max_snapshots      = local_max_snapshots,
                                            remote_max_snapshots     = local_remote_max_snapshots,
                                            timeout                  = timeout
                                            )
                                    if success:
                                        logger.info(f"{this()}: Local security copies for VM: '{row.Nutanix_Prism_VM.vm_name}' SUCCESS.")
                                    else:
                                        logger.warning(f"{this()}: Local security copies for VM: '{row.Nutanix_Prism_VM.vm_name}' FAILURE")
                                        VM_Protected = False
                            except Exception as e:
                                VM_Protected = False
                                logger.error(f"{this()}: Local security copies for VM: '{row.Nutanix_Prism_VM.vm_name}' exception: {str(e)}")
                                emtec_handle_general_exception(e,logger=logger)
                            # if remote replicas are required
                            # a protection domain is created if does not 
                            # exits and an schedule is configured for remote
                            # replicas
                            # optionaly, local copies of remote replicas can 
                            # be created , note, will be recognized as
                            # local copies anyway
                            
                            # Check for Remote Security copies
                            try:
                                if row.Nutanix_Prism_VM.vm_drp_remote and Protection_Uncomplete:
                                    logger.info(f"{this()}: DRP copies requested for VM: '{row.Nutanix_Prism_VM.vm_name}'")
                                    success,pdname = create_drp(
                                            app,
                                            vmname                   = row.Nutanix_Prism_VM.vm_name,
                                            pdname                   = pdname,
                                            annotation               = annotation,
                                            remote_cluster           = remote_cluster,
                                            schedule_type            = remote_schedule_type,
                                            user_start_time_in_usecs = user_start_time_in_usecs,
                                            every_nth                = remote_every_nth,
                                            local_max_snapshots      = remote_max_snapshots,
                                            remote_max_snapshots     = remote_remote_max_snapshots,
                                            timeout                  = timeout
                                            )
                                    if success:
                                        logger.info(f"{this()}: DRP for VM: '{row.Nutanix_Prism_VM.vm_name}' SUCCESS.")
                                    else:
                                        logger.warning(f"{this()}: DRP for VM: '{row.Nutanix_Prism_VM.vm_name}' FAILURE.")
                                        VM_Protected = False
                            except Exception as e:
                                logger.error(f"{this()}: DRP for VM: '{row.Nutanix_Prism_VM.vm_name}' EXCEPTION: {str(e)}")
                                emtec_handle_general_exception(e,logger=logger)
                                VM_Protected = False
                            if VM_Protected:
                                # actualizar aqui el Flag **************
                                row.Requests.Status = turn_on(row.Requests.Status,NUTANIX_PROTECTED)
                                row.Requests.Comments = '' if row.Requests.Comments is None else row.Requests.Comments
                                row.Requests.Comments += f"Protegida @ {strftime('%d/%m/%y %H:%M')}."
                                db.session.merge(row.Requests)
                                db.session.commit()
                                db.session.flush()
                            else:
                                logger.warning(f"{this()}: VM '{row.Nutanix_Prism_VM.vm_name}' is not protected yet.")
                        # DATA PROTECTION BLOCK ENDS HERE --------------
                    else:
                        logger.error(f'{this()}: response.ok          = {response.ok}')
                        logger.error(f'{this()}: response.status_code = {response.status_code}')
                        logger.error(f'{this()}: response.reason      = {response.reason}')
                        logger.error(f'{this()}: response.text        = {response.text}')
                else:
                    logger.error(f'{this()}: response = {response}')
            result   =  get_api_response(   code=BUTLER_CORE_TRX_OK,
                            message=f'{this()}: trx: {trx} : {len(rows)} Tasks processed.'
                            )
        else:
            result   =  get_api_response(   code=BUTLER_CORE_TRX_OK,
                            message=f'{this()}: No rows for trx {trx}'
                            )
    except Exception as e:
        tracebox_log(f'{this()}: exception = {str(e)}',
            logger = logger,
            level  = logging.CRITICAL,
            length = tracebox_log_length
            )
        result   =  get_api_response(   code=BUTLER_CORE_TRX_ERROR,
                        message=f'{this()}: Exception: {str(e)}'
                        )
        emtec_handle_general_exception(e,logger=logger)

    logger.debug(f'{this()}: OUT')
    tracebox_log(f'{this()}: {str(result)}',
            logger=logger,level=logging.DEBUG,length=tracebox_log_length)
    return result

# If VM is Nutanix provisioned and has a valid IP address, then --------
# sets up EG Monitor Host creation
def trx_005_monitor_pending(app):
    logger.info(f'{this()}: IN Get Created VM and monitor it with EG Monitor ...')
    # query for matching rows for transaction
    # 20210529 GV trx = TRX_EGB_NTX_OK_NO_IP
    trx = TRX_EGB_EGM_PENDING
    try:
        rows = butler_trx_get(transaction=trx,session=db.session,logger=logger)
        # process result here
        if rows is not None and len(rows):
            logger.warning(f'Transaction {BUTLER_TRANSACTIONS[trx]}: {len(rows)} rows found : ')
            for row in rows:
                # Process row here
                # For transaction 004
                # Load Nutanix VM  and get IP Address to setup Monitoring
                host      = app.config['NUTANIX_HOST']
                port      = app.config['NUTANIX_PORT']
                username  = app.config['NUTANIX_USERNAME']
                password  = app.config['NUTANIX_PASSWORD']
                protocol  = app.config['NUTANIX_PROTOCOL']
                #'https://10.26.1.247:5665/v1/objects/hosts?filter=match(%22aix-director%22,host.name)'
                #endpoint  = f'v1/objects/hosts?filter=match("{row.uuid}",host.name)'
                endpoint  = f'api/nutanix/v3/vms/{row.Requests.uuid}'
                url       = f'{protocol}://{host}:{port}/{endpoint}'
                headers   = ''
                data     = {}
                # get Nutanix Response
                logger.warning(f'{this()}: url = {url}')
                
                response = api_request(    
                                'GET',
                                url,
                                data=data,
                                headers=headers,
                                username=username,
                                password=password,
                                logger   = logger
                            )
                trace_trx(this(),app,row,response)
                if response is not None:
                    data=response.json()
                    if response.ok:
                        # EG MONITOR BLOCK STARTS HERE -----------------
                        # Monitoring Setup depends on DP block process, 
                        # if any
                        #if Setup_Monitoring:
                        logger.warning(f"ENTER VM MONITORING BLOCK")
                        # Aqui puede faltar revisar IPs de otras NICS
                        if row.Nutanix_Prism_VM.vm_ip is not None and row.Nutanix_Prism_VM.vm_ip != '':
                            IP = row.Nutanix_Prism_VM.vm_ip
                        elif row.Nutanix_Prism_VM.nic_0_ip is not None and row.Nutanix_Prism_VM.nic_0_ip != '':
                            IP = row.Nutanix_Prism_VM.nic_0_ip
                        elif row.Nutanix_Prism_VM.nic_1_ip is not None and row.Nutanix_Prism_VM.nic_1_ip != '':
                            IP = row.Nutanix_Prism_VM.nic_1_ip
                        elif row.Nutanix_Prism_VM.nic_2_ip is not None and row.Nutanix_Prism_VM.nic_2_ip != '':
                            IP = row.Nutanix_Prism_VM.nic_2_ip
                        else:
                            IP = None
                        logger.warning(f"IP from row = '{IP}'")
                        try:
                            # Check for first valid IP address
                            for nic in data['spec']['resources']['nic_list']:
                                for endpoint in nic['ip_endpoint_list']:
                                    IP = endpoint.get('ip',None)
                                    logger.warning(f"IP from Nutanix = '{IP}'")
                                    if IP not in [None,'']:
                                        break;
                                if IP not in [None,'']:
                                    break;
                        except:
                            IP = None
                        logger.warning(f"IP from row = '{IP}'")
                        # If IP address detected then try to monitor
                        if IP not in [None,'']:
                            # ------------------------------------------
                            # Update VM IP, will setup a temporary
                            # Monitor Pending Status
                            # ------------------------------------------
                            logger.info(f"{this()}: IP '{IP}' for VM '{row.Nutanix_Prism_VM.vm_name}' found ...")
                            row.Requests.Task_status = 1
                            '''
                            if not has_status(row.Requests.Status,MONITOR_PENDING):
                                row.Requests.Status += MONITOR_PENDING
                            '''
                            row.Requests.Status = turn_on(row.Requests.Status,MONITOR_PENDING)
                            db.session.merge(row.Requests)
                            db.session.commit()
                            db.session.flush()
                            logger.warning(f'{this()}: request {row.Requests.Id} updated to MONITOR PENDING ...')                    
                            # Setup EG Monitor Host , left "Monitor Completed"
                            host      = app.config['MONITOR_HOST']
                            port      = app.config['MONITOR_PORT']
                            username  = app.config['MONITOR_USERNAME']
                            password  = app.config['MONITOR_PASSWORD']
                            protocol  = app.config['MONITOR_PROTOCOL']
                            # ------------------------------------------
                            # Nutanix VM UUID will be used as unique 
                            # Identifier for EG Monitor
                            # ------------------------------------------
                            endpoint  = f'v1/objects/hosts/{row.Requests.uuid}'
                            url       = f'{protocol}://{host}:{port}/{endpoint}'
                            headers   = {
                                'Content-Type': 'application/json',
                                'Connection'  : 'close',
                                'Accept'      : 'application/json'
                                }

                            data     = {
                                'attrs':{
                                    'address'       : IP,
                                    'check_command' : 'hostalive',
                                    'display_name'  : row.Nutanix_Prism_VM.vm_name
                                    }
                                }

                            # get Icinga Response ----------------------
                            logger.warning(f'{this()}: url = {url}')
                            logger.warning(f'{this()}: data = {data}')
                            # Will instruct Icinga to create new Host
                            response = api_request(    
                                            'PUT',
                                            url,
                                            data=json.dumps(data),
                                            headers=headers,
                                            username=username,
                                            password=password,
                                            logger   = logger
                                        )
                            # If all goes OK, Then complete status -----
                            if response is not None and response.ok:
                                if response.status_code == 200:
                                    '''
                                    if has_status(row.Requests.Status,MONITOR_PENDING):
                                        row.Requests.Status -= MONITOR_PENDING
                                    row.Requests.Status += MONITOR_COMPLETED
                                    '''
                                    row.Requests.Status = turn_off(MONITOR_PENDING)
                                    row.Requests.Status = turn_on (MONITOR_COMPLETED)
                                    row.Requests.Comments = '' if row.Requests.Comments is None else row.Requests.Comments
                                    row.Requests.Comments += f"Monitoreada @ {strftime('%d/%m/%y %H:%M')}."
                                    db.session.merge(row.Requests)
                                    db.session.commit()
                                    db.session.flush()
                            else:
                                if response is not None:
                                    if response.status_code == 500:
                                        data = response.json()
                                        try:
                                            if data['results'][0]['errors'][0].find('already exists.')>-1:
                                                row.Requests.Status = turn_off(MONITOR_PENDING)
                                                row.Requests.Status = turn_on (MONITOR_COMPLETED)
                                                row.Requests.Comments = '' if row.Requests.Comments is None else row.Requests.Comments
                                                row.Requests.Comments += f"Monitoreada @ {strftime('%d/%m/%y %H:%M')}."
                                                db.session.merge(row.Requests)
                                                db.session.commit()    
                                                db.session.flush()                                            
                                            else:
                                                logger.error(f'{this()}: response = {response}')
                                        except Exception as e:
                                            logger.error(f'{this()}: response = {response} e={str(e)}')                                            
                                    else:
                                        logger.error(f'{this()}: response = {response}')
                                else:
                                    logger.error(f'{this()}: response = {response}')
                        else:
                            logger.warning(f"{this()}: NO IP for VM '{row.Nutanix_Prism_VM.vm_name}' yet ...")
                        logger.warning(f"EXIT VM MONITORING BLOCK")
                        # EG MONITOR BLOCK ENDS HERE -----------------
                    else:
                        logger.error(f'{this()}: response.ok          = {response.ok}')
                        logger.error(f'{this()}: response.status_code = {response.status_code}')
                        logger.error(f'{this()}: response.reason      = {response.reason}')
                        logger.error(f'{this()}: response.text        = {response.text}')
                else:
                    logger.error(f'{this()}: response = {response}')
            result   =  get_api_response(   code=BUTLER_CORE_TRX_OK,
                            message=f'{this()}: trx: {trx} : {len(rows)} Tasks processed.'
                            )
        else:
            result   =  get_api_response(   code=BUTLER_CORE_TRX_OK,
                            message=f'{this()}: No rows for trx {trx}'
                            )
    except Exception as e:
        tracebox_log(f'{this()}: exception = {str(e)}',
            logger = logger,
            level  = logging.CRITICAL,
            length = tracebox_log_length
            )
        result   =  get_api_response(   code=BUTLER_CORE_TRX_ERROR,
                        message=f'{this()}: Exception: {str(e)}'
                        )
        emtec_handle_general_exception(e,logger=logger)

    logger.debug(f'{this()}: OUT')
    tracebox_log(f'{this()}: {str(result)}',
            logger=logger,level=logging.DEBUG,length=tracebox_log_length)
    return result

# In case EG Collector keeps on pending status -------------------------
# OJO OJO OJO NO VEO ACCIONES SOBRE BD DE COLLECTOR
# POBLAMIENTO DE CC !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def trx_006_collector_pending(app):
    logger.info(f'{this()}: IN Search VM in EG Collector and Update CC')
    trx = TRX_EGB_EGC_PENDING
    
    try:
        rows = butler_trx_get(transaction=trx,session=db.session,logger=logger)
        # process result here
        if rows is not None and len(rows):
            logger.debug(f'Transaction {BUTLER_TRANSACTIONS[trx]}: {len(rows)} rows found : ')
            for row in rows:
                # AQUI ES DONDE SE DEBE POBLAR LA TRANSACCION
                # POBLAR CC EN BD COLLECTOR
                # collector.Configuration_Items.CC_Id = xxxx
                # Y marcar como collector completed
                
                CI_Name = row.Nutanix_Prsm_VM.vm_name
                CC_Id   = row.CC_Id
                # Setup EG Collector Host , update "Cost Center"
                host      = app.config['COLLECTOR_HOST']
                port      = app.config['COLLECTOR_PORT']
                username  = app.config['COLLECTOR_USERNAME']
                password  = app.config['COLLECTOR_PASSWORD']
                protocol  = app.config['COLLECTOR_PROTOCOL']
                # ------------------------------------------
                # Nutanix VM UUID will be used as unique 
                # Identifier for EG Monitor
                # ------------------------------------------
                endpoint  = f'api/get/Configuration_Items?CI_Name={CI_Name}'
                url       = f'{protocol}://{host}:{port}/{endpoint}'
                headers   = ''
                # get Icinga Response ----------------------
                logger.debug(f'{this()}: url = {url}')
                # Will instruct Icinga to create new Host
                response = api_request(    
                                'GET',
                                url,
                                headers=headers,
                                username=username,
                                password=password,
                                logger   = logger
                            )
                if response is not None:
                    try:
                        CI_Id   = response.json.entities[0]('CI_Id')
                        endpoint  = f'api/patch/Configuration_Items/{CI_Id}?CC_Id={CC_Id}'
                        url       = f'{protocol}://{host}:{port}/{endpoint}'
                        response = api_request(    
                                        'PATCH',
                                        url,
                                        headers=headers,
                                        username=username,
                                        password=password,
                                        logger   = logger
                                    )
                        trace_trx(this(),app,row,response)
                        if response is not None:
                            if response.ok:
                                try:
                                    data=response.json()
                                    if data['status'] == 'SUCCEEDED':
                                        #row.Status -= COLLECTOR_PENDING
                                        #row.Status += COLLECTOR_COMPLETED
                                        row.Status = turn_off(row.Status,COLLECTOR_PENDING)
                                        row.Status = turn_on (row.Status,COLLECTOR_COMPLETED)
                                        row.Comments = '' if row.Comments is None else row.Comments
                                        row.Comments += f"Tarificada @ {strftime('%d/%m/%y %H:%M')}."
                                        db.session.merge(row)
                                        db.session.commit()
                                        db.session.flush()
                                        logger.info(f'{this()}: request {row.Id} updated. EG Collector CC populated.')                    
                                    else:
                                        logger.error(f"{this()}: status={data['status']}")                                                
                                        try:
                                            tracebox_log(f"{this()}: Request = {row.Id} {data['error_detail']}",
                                                logger=logger,level=logging.ERROR,length=tracebox_log_length)
                                        except Exception as e:
                                            tracebox_log(f"{this()}: status={data['status']} log exception = {str(e)}",
                                                logger = logger,
                                                level  = logging.WARNING,
                                                length = tracebox_log_length
                                                )
                                except Exception as e:
                                    logger.error(f'{this()}: response.ok exception = {str(e)}')
                            else:
                                logger.error(f'{this()}: response.status_code = {response.status_code}')
                                logger.error(f'{this()}: response.reason      = {response.reason}')
                                logger.error(f'{this()}: response.text        = {response.text}')
                        else:
                            logger.error(f'{this()}: response = {response}')
                        
                    except:
                        logger.warning(f"{this()}: CI_Id not found for '{CI_Name}'")
                
            result   =  get_api_response(   code=BUTLER_CORE_TRX_OK,
                            message=f'{this()}: trx: {trx} : {len(rows)} Tasks processed.'
                            )
        else:
            result   =  get_api_response(   code=BUTLER_CORE_TRX_OK,
                            message=f'{this()}: No rows for trx {trx}'
                            )
    except Exception as e:
        tracebox_log(f'{this()}: exception = {str(e)}',
            logger = logger,
            level  = logging.CRITICAL,
            length = tracebox_log_length
            )
        result   =  get_api_response(   code=BUTLER_CORE_TRX_ERROR,
                        message=f'{this()}: Exception: {str(e)}'
                        )

    logger.debug(f'{this()}: OUT')
    tracebox_log(f'{this()}: {str(result)}',
            logger=logger,level=logging.DEBUG,length=tracebox_log_length)
    return result

# Check for all requirements completed ---------------------------------
def trx_007_all_completed(app):
    logger.info(f'{this()}: IN Check for Completion')
    # query for matching rows for transaction
    trx = TRX_EGB_OK
    try:
        rows = butler_trx_get(transaction=trx,session=db.session,logger=logger,current=current)
        # process result here
        if rows is not None and len(rows):
            logger.warning(f'Transaction {BUTLER_TRANSACTIONS[trx]}: {len(rows)} rows found : ')
            for row in rows:
                # Process row here
                # For transaction 007   
                # Check for full completion in order to finalize
                # request life cycle
                # 
                logger.warning(f"row={row}")
                row.Status    = turn_on(row.Status,REQUEST_COMPLETED)
                row.Comments  = '' if row.Comments is None else row.Comments
                row.Comments += f"Completa @ {strftime('%d/%m/%y %H:%M')}. Estado Final."
                db.session.merge(row)
                db.session.commit()
                db.session.flush()
                logger.info(f'{this()}: request {row.Id} updated. Completed.')
                try:
                    trace_trx(this(),app,row)
                except Exception as e:
                    logger.error(f"exception: {str(e)}")
            message=f'{this()}: trx: {trx} : {len(rows)} Requests completed!!!.'
        else:
            message = f'{this()}: No rows for trx {trx}'
        result   =  get_api_response(
                        code=BUTLER_CORE_TRX_OK,
                        message = message
                        )
    except Exception as e:
        tracebox_log(f'{this()}: exception = {str(e)}',
            logger = logger,
            level  = logging.CRITICAL,
            length = tracebox_log_length
            )
        result   =  get_api_response(   code=BUTLER_CORE_TRX_ERROR,
                        message=f'{this()}: Exception: {str(e)}'
                        )

    logger.debug(f'{this()}: OUT')
    tracebox_log(f'{this()}: {str(result)}',
            logger=logger,
            level=logging.DEBUG,
            length=tracebox_log_length
            )
    return result

# ======================================================================
# Main transactions caller
# ======================================================================
#ef execute_transactions(app,db,mail):
def execute_transactions(app,user=None):
    logger.info(f"----------------------------------------------------")
    logger.info(f"{this()}: Start @ {time.strftime('%Y-%m-%d %H:%M:%S')}")
    ''' This block if for testing purposes only '''
    if app.config['DEBUG'] and False:
        try:
            # gets contextual Data for actual request (last one)
            Id=db.session.query(Requests.Id).order_by(Requests.Id.desc()).limit(1).scalar()
            data = Get_data_context(app=app,db=db,mail=mail,Id=Id)
            logger.debug(f"{this()}: data keys            = {data.keys()}")        
            logger.debug(f"{this()}: butler_notify_request= {butler_notify_request}")
            logger.debug(f"{this()}: html_provission      = {html_provission}")
            logger.debug(f"{this()}: requests             = {requests}")
            logger.debug(f"{this()}: Requests             = {Requests}")
            logger.debug(f"{this()}: app                  = {app}")
            logger.debug(f"{this()}: db                   = {db}")
            logger.debug(f"{this()}: mail                 = {mail}")
            
            # Forced user role for testing
            data['role'] = ROLE_REQUESTOR
            
            # gets actual records for selected request
            row = db.session.query(Requests).filter(Requests.Id == Id).one_or_none()
            rox = db.session.query(Nutanix_Prism_VM).filter(Nutanix_Prism_VM.Request_Id == Id).one_or_none()
            
            data.update({
                'top_cost_center_code':app.config.get('BUTLER_TOP_COST_CENTER'),
                'requestor_email': 'User_email',
                'approver_email': 'Approver_email',
                'row':row,
                'rox':rox
            })
            
            logger.debug(f"Id={Id} data={data}")        
            html = html_provission(data=data)
            logger.debug(f"html=\n{html}")
            To = app.config.get('BUTLER_SUPPORT_NOTIFICATION')
            # Setup required data
            # Collect user and approver emails
            User_email = db.session.query(Users.email).filter(Users.id==row.User_Id).one_or_none()
            Approver_email = db.session.query(Users.email).filter(Users.id==row.Approver_Id).one_or_none()
            logger.warning(f"row = {row}")
            logger.warning(f"User_email = {User_email}")
            logger.warning(f"Approver_email = {Approver_email}")
            if User_email     is None: User_email=(None,)
            if Approver_email is None: Approver_email=(None,)
            data.update({
                'top_cost_center_code':app.config.get('BUTLER_TOP_COST_CENTER'),
                'requestor_email': User_email[0],
                'approver_email': Approver_email[0],
            })
            # Format email,must include IP address if any
            # send email
            for html_function in [html_provission,butler_output_request]:
                butler_notify_request(
                    subject_detail=f"Maquina Virtual PROVISIONADA TEST DEBUG",
                    data=data,
                    recipients=To.split(','),
                    html_function=html_function
                )

        except Exception as e:
            emtec_handle_general_exception(e,logger=logger)

    # Trx execution order is important if 'current' data will be used
    # from 'previous' trx
    global tracebox_log_length
    tracebox_log_length = app.config.get('TRACEBOX_LOG_LENGTH',80)
    logger.debug(f'{this()}: tracebox_log_length = {tracebox_log_length}')
    transactions = [
        # First update context values for iteration
        trx_ucc_update_butler_cost_centers,
        trx_ura_update_butler_rates,
        trx_uim_update_butler_images,
        trx_usn_update_butler_subnets,  # Subnets to be consumed by projects
        trx_upr_update_butler_projects,
        trx_uca_update_butler_categories,
        # Then execute Butler transactions
        trx_001_not_nutanix_pending,
        trx_002_not_collector_pending,
        trx_003_nutanix_pending,
        trx_004_nutanix_completed,
        #trx_005_monitor_pending,
        #trx_006_collector_pending,
        trx_007_all_completed
    ]
    logger.info(f"{this()}: BUTLER_CONFIG_FILE = '{app.config.get('BUTLER_CONFIG_FILE')}'.")
    # Oportunity here to hot update config , not mandatory
    #config_ini = ConfigParser(interpolation=ExtendedInterpolation())
    #config_ini.read( app.config.get('BUTLER_CONFIG_FILE') )
    for transaction in transactions:
        TRX_NAME = transaction.__name__.upper()
        active      = app.config.get(TRX_NAME,True)
        # update context transaction active status
        current['transactions'].update({TRX_NAME:active})
        
        if active:
            logger.debug(f"{this()}: Transaction '{transaction.__name__}' is active.")
            try:
                db.session.flush()
            except Exception as e:
                logger.error(f'{this()}: exception: {str(e)}')
                db.session.rollback()
            result = transaction(app)
            try:
                result = json.loads(result)
                if result['status']['code'] != BUTLER_CORE_TRX_OK:
                    logger.error(f"{this()}: Transaction '{transaction.__name__}' Error {result['status']['message']}")
            except Exception as e:
                tracebox_log(f"{this()}: Transaction '{transaction.__name__}' exception = {str(e)}",
                    logger = logger,
                    level  = logging.CRITICAL,
                    length = tracebox_log_length
                    )
        else:
            logger.info(f"{this()}: WARNING Transaction '{transaction.__name__}' is inactive.")
    for key in current:
        logger.info(f"{this()}: {key} = {len(current[key])}")
    logger.info(f"{this()}: Completed @ {time.strftime('%Y-%m-%d %H:%M:%S')}.")
