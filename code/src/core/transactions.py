# ======================================================================
# EG Suite - EG Butler Core Service Application Transactions
# Purpose: To handle Butler API requests and orchestrate Butler Requests
# Live cycle
# (c) Emtec Group/Sertechno 2020
# GLVH gvalera@emtecgroup.net
# ======================================================================

import  time
from    pprint                      import pprint
from    pprint                      import pformat
from    emtec                       import *
from    emtec.butler.db.orm_model   import *
from    emtec.butler.constants      import *
from    emtec.api                   import *
#rom    emtec.nutanix               import *
from    .                           import db
from    .                           import logger
import datetime
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
}

# Transaction support functions

"""
# Search VM in Nutanix
def get_nutanix_vm(app,vm_name,timeout=None):
    logger.debug(f'{this()}: IN')
    
    vm        = None
    try:
        host      = app.config.get('NUTANIX_HOST')
        port      = app.config.get('NUTANIX_PORT')
        username  = app.config.get('NUTANIX_USERNAME')
        password  = app.config.get('NUTANIX_PASSWORD')
        protocol  = app.config.get('NUTANIX_PROTOCOL')
        timeout   = app.config.get('NUTANIX_API_TIMEOUT',None)
        endpoint  = 'api/nutanix/v3/vms/list'
        arguments = ''
        data      = {'kind':'vm','filter':f'vm_name=={vm_name}'}
            
        headers   = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
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
            if response.ok:
                data=response.json()
                if data['metadata']['total_matches'] == 1:
                    vm = data['entities'][0]
    except Exception as e:
        tracebox_log(f'{this()}: {str(e)}',
            logger = logger,
            level  = logging.ERROR,
            length = tracebox_log_length
            )
        
    logger.trace(f"{this()}: vm: {vm}")
    logger.debug(f'{this()}: OUT')
    return vm
"""

# Get list of remote sites
# nota verificar si requiere algun parametro para la llamada por sitio
# Ojo validar correo de David dice que debe ser hacia un Prism Element 
def get_hosts(app,timeout=None):
    logger.debug(f'{this()}: IN')
    
    hosts = None
    try:
        host      = app.config.get('NUTANIX_HOST')
        port      = app.config.get('NUTANIX_PORT')
        username  = app.config.get('NUTANIX_USERNAME')
        password  = app.config.get('NUTANIX_PASSWORD')
        protocol  = app.config.get('NUTANIX_PROTOCOL')
        endpoint  = '/api/nutanix/v3/hosts/list'
        arguments = ''
        data      = {'kind':'host'}
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
            if response.ok:
                data=response.json()
                logger.debug(f'{this()}: data={data}')
                hosts = []
                for entity in data['entities']:
                    hosts.append(entity)
    except Exception as e:
        tracebox_log(
            f'{this()}: {str(e)}',
            logger = logger,
            level  = logging.ERROR,
            length = tracebox_log_length
            )
        
    logger.trace(f"{this()}: hosts: {hosts}")
    logger.debug(f'{this()}: OUT')
    return hosts

""" MOVIDO A LIBRERIA EMTEC.NUTANIX PARA PORTABILIDAD
    DESPUES DE PROBADO MOVER OTRAS FUNCIONES PORTABLES
# Get list of local and remote snapshots
# nota verificar si requiere algun parametro para la llamada por sitio
# Ojo validar correo de David dice que debe ser hacia un Prism Element 
def get_snapshots(app,host=None,port=None,username=None,password=None,protocol=None,timeout=None):
    ''' looks for snapshots and return a list will all meaningfull '''
    logger.debug(f'{this()}: IN')
    
    snapshots = None
    try:
        if host     is None:    host  = app.config.get('NUTANIX_HOST')
        if port     is None:    port      = app.config.get('NUTANIX_PORT')
        if username is None:    username  = app.config.get('NUTANIX_USERNAME')
        if password is None:    password  = app.config.get('NUTANIX_PASSWORD')
        if protocol is None:    protocol  = app.config.get('NUTANIX_PROTOCOL')
        endpoint  = '/PrismGateway/services/rest/v2.0/protection_domains/dr_snapshots'
        arguments = '/?fulldetails=true'
        data      = None
        headers   = {'Content-Type': 'application/json'}
        url       = f'{protocol}://{host}:{port}/{endpoint}{arguments}'

        logger.debug(f'{this()}: user = {username}')
        logger.debug(f'{this()}: url  = {url}')

        response = api_request('GET',
                        url,
                        data     = data,
                        headers  = headers,
                        username = username,
                        password = password,
                        timeout  = timeout,
                        logger   = logger
                        )
        if response is not None:
            if response.ok:
                data=response.json()
                snapshots = []
                for entity in data['entities']:
                    exclusive_usage_in_bytes = entity.get('exclusive_usage_in_bytes',0)
                    if exclusive_usage_in_bytes>0:
                        for vm in entity['vms']:
                            if vm['vm_name'] == entity['consistency_groups'][0]:
                                snapshots.append({
                                'vm_name':vm['vm_name'],
                                'vm_id':vm['vm_id'],
                                'size_in_bytes':entity.get('size_in_bytes',0),
                                'exclusive_usage_in_bytes':entity.get('exclusive_usage_in_bytes',0),
                                'state':entity.get('state',None),
                                })
                                break
    except Exception as e:
        tracebox_log(
            f'{this()}: {str(e)}',
            logger = logger,
            level  = logging.ERROR,
            length = tracebox_log_length
            )
        
    logger.debug(f"{this()}: OUT snapshots: {snapshots}")
    return snapshots

def get_snapshots_dict(snapshots):
    ''' Process snapshots list from get_snapshots and builds a dict '''
    snaps={}
    for snapshot in snapshots:
        size_bytes = snapshot['size_in_bytes']
        usage_bytes = snapshot['exclusive_usage_in_bytes']
        # construye diccionario
        if snapshot['vm_name'] not in snaps:
            snaps.update({
                snapshot['vm_name']:{
                    **snapshot,
                    'size_in_gigabytes': 0,
                    'exclusive_usage_in_gigabytes': 0,
                    'ci_id': None,
                }
            })
        else:
            snaps[snapshot['vm_name']]['size_in_bytes']            += size_bytes  
            snaps[snapshot['vm_name']]['exclusive_usage_in_bytes'] += usage_bytes  
        snaps[snapshot['vm_name']]['size_in_gigabytes']            += size_bytes/(1024*1024*1024)
        snaps[snapshot['vm_name']]['exclusive_usage_in_gigabytes'] += usage_bytes/(1024*1024*1024)
        # --------------------------
    return snaps
"""    
# Get list of remote sites
# nota verificar si requiere algun parametro para la llamada por sitio
# Ojo validar correo de David dice que debe ser hacia un Prism Element 
def get_remote_sites(app,host=None,timeout=None):
    logger.debug(f'{this()}: IN')
    
    remote_sites = None
    try:
        if host is None:
            host  = app.config.get('NUTANIX_HOST')
        port      = app.config.get('NUTANIX_PORT')
        username  = app.config.get('NUTANIX_USERNAME')
        password  = app.config.get('NUTANIX_PASSWORD')
        protocol  = app.config.get('NUTANIX_PROTOCOL')
        endpoint  = '/PrismGateway/services/rest/v2.0/remote_sites/'
        arguments =''
        data      = None
        headers   = {'Content-Type': 'application/json'}
        url       = f'{protocol}://{host}:{port}/{endpoint}{arguments}'

        logger.debug(f'{this()}: user = {username}')
        logger.debug(f'{this()}: url  = {url}')

        response = api_request('GET',
                        url,
                        data     = data,
                        headers  = headers,
                        username = username,
                        password = password,
                        timeout  = timeout,
                        logger   = logger
                        )
        if response is not None:
            if response.ok:
                data=response.json()
                #logger.warning(f'{this()}: data={data}')
                #pprint(data)
                remote_sites = []
                for entity in data['entities']:
                    remote_sites.append({
                        'name':entity.get('name',None),
                        'uuid':entity.get('uuid',None),
                        'remote_ip_ports':entity.get('remote_ip_ports',None),
                    })
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
    logger.debug(f'{this()}: IN h:{host},n:{pdname},vm:{vmname}')
    
    created = False
    if pdname is None:
        # Default: if pdname is None then pdname = vmname
        if vmname is not None:
            pdname = vmname
        else:
            # default will be an hex number based in actual timestamp in usecs
            # this shouldn't happen sin vmname need to be available
            pdname = f"{int(datetime.datetime.now().timestamp()*1000000):x}"
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
            annotation = f'Created by EG Butler at {datetime.datetime.now()}'
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
                    logger.warning(f"protection domanin '{pdname}' {response.status_code} {response.reason} {data.get('message',None)} {data.get('error_code',None)}")
                    created = True
                else:
                    logger.error(f"protection domanin '{pdname}' {response.status_code} {response.reason} {data.get('message',None)} {data.get('error_code',None)}")
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
def protect_vms(app,vmname,host,protection_domain,timeout=None):
    logger.debug(f'{this()}: IN')
    
    success = False
    try:
        if host is None:
            host  = app.config.get('NUTANIX_HOST')
        port      = app.config.get('NUTANIX_PORT')
        username  = app.config.get('NUTANIX_USERNAME')
        password  = app.config.get('NUTANIX_PASSWORD')
        protocol  = app.config.get('NUTANIX_PROTOCOL')
        endpoint  = f'/PrismGateway/services/rest/v2.0/protection_domains/{protection_domain}/protect_vms'
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
            logger.debug(f'{this()}: 296 data={data}')
            if response.ok:
                if response.status_code in [200,201]:
                    success = True
                else:
                    logger.warning(f"{this()}: {response.status_code} {response.reason} {data.get('message',None)} {data.get('error_code',None)}")
                    success = False
            else:
                logger.debug(f"305 data={data}")
                if response.status_code == 422:
                    if data['message'].find('already protected') != -1:
                        logger.warning(f"{this()}: 422 {vmname} is already protected")
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
        host,
        protection_domain,
        remote_cluster,
        schedule_type            = 'HOURLY',
        user_start_time_in_usecs = None,
        every_nth                = None,
        local_max_snapshots      = 4,
        remote_max_snapshots     = 4,
        timeout                  = None,
    ):
    logger.debug(f'{this()}: IN')
    
    created = False
    try:
        if host is None:
            host  = app.config.get('NUTANIX_HOST')
        port      = app.config.get('NUTANIX_PORT')
        username  = app.config.get('NUTANIX_USERNAME')
        password  = app.config.get('NUTANIX_PASSWORD')
        protocol  = app.config.get('NUTANIX_PROTOCOL')
        endpoint  = f'/PrismGateway/services/rest/v2.0/protection_domains/{protection_domain}/schedules'
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
            'pd_name'  : protection_domain,
            'type'     : schedule_type,
            'user_start_time_in_usecs' : user_start_time_in_usecs,
            'app_consistent': True,
            'retention_policy':{
                'local_max_snapshots':4,
                'remote_max_snapshots':{
                    remote_cluster: remote_max_snapshots
                }
            }
        }
        if every_nth is not None:
            data.update({'every_nth':every_nth})
            
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
            if response.ok:
                data = response.json()
                if response.status_code in [200,201]:
                    created = True
                else:
                    logger.error(f"{this()}: {response.status_code} {response.reason} {data.get('message',None)} {data.get('error_code',None)}")
                    logger.error(f'{this()}: data={data}')
                    created = False
            else:
                logger.error(f"{this()}: {response.status_code} {response.reason} {data.get('message',None)} {data.get('error_code',None)}")
                logger.error(f'{this()}: data={data}')
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
        every_nth                = None,
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
    logger.debug(f"{this()}: IN")
    success = False
    # Get cluster's hosts list
    logger.debug(f"getting clusters's hosts ...")
    cluster_hosts = get_hosts(app)
    ip = None
    if cluster_hosts is not None:
        for host in cluster_hosts:
            if host['spec'].get('name',None) is not None:
                cluster_host_ip = host['spec']['resources']['controller_vm']['ip']
                break
    else:
        logger.error(f"No hosts found !!!")
        return False
    if cluster_host_ip is not None:
        # try to get remote cluster if not defined
        if remote_cluster is None:
            logger.info(f"getting remote cluster ...")
            sites = get_remote_sites(app,host=cluster_host_ip)
            if len(sites):
                remote_cluster = sites[0]['name']
        if remote_cluster is not None:
            # Create protection domain -------------------------------------
            logger.info(f"remote_cluster: {remote_cluster}")
            logger.info(f"creating protection domain for vm '{vmname}' ...")
            protection_domain = create_protection_domain(
                    app,
                    host       = cluster_host_ip,
                    pdname     = pdname,
                    annotation = annotation,
                    vmname     = vmname,
                    timeout    = timeout
                    )
            if protection_domain is not None:
                # got valid protection domain, will protect vms ------------
                logger.info(f"protection_domain = '{protection_domain}' ...")
                logger.info(f"protecting vm '{vmname}' in '{remote_cluster}:{protection_domain}' ...")
                if protect_vms(app,vmname,cluster_host_ip,protection_domain,timeout=timeout):
                    # VM is protected, then schedule it --------------------
                    logger.info(f"creating schedule for '{remote_cluster}:{protection_domain}' ...")
                    if create_schedule(app,
                        cluster_host_ip,
                        protection_domain,
                        remote_cluster           = remote_cluster,
                        schedule_type            = 'HOURLY',
                        user_start_time_in_usecs = None,
                        every_nth                = None,
                        local_max_snapshots      = 4,
                        remote_max_snapshots     = 4,
                        timeout                  = timeout
                        ):
                        logger.debug(f'protection schedule for VM {vmname} success.')
                        success = True
                    else:
                        # no calendarizada
                        logger.warning(f'protection schedule for VM {vmname} failure.')
                else:
                    # error no protegida
                    logger.warning(f'VM {vmname} protection failure.')
            else:
                # Error nada creado
                logger.warning(f'protection domain creation for VM {vmname} failure.')
    else:
        logger.error(f"No valid Nutanix host found in cluster.")
    logger.debug(f'{this()}: OUT success = {success}')
    return success
            
# Update Cost Centers from EG Collector --------------------------------
def trx_ucc_update_butler_cost_centers(app):
    logger.debug(f'{this()}: IN')
    result   = get_api_response(    
                code=BUTLER_CORE_TRX_ERROR,
                message=f'NO TRX RESPONSE')
    
    host      = app.config.get('COLLECTOR_HOST')
    port      = app.config.get('COLLECTOR_PORT')
    username  = app.config.get('COLLECTOR_USERNAME')
    password  = app.config.get('COLLECTOR_PASSWORD')
    protocol  = app.config.get('COLLECTOR_PROTOCOL')
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
                    logger=logger
                    )
    logger.trace(f"{this()}: response:             {response}")
    if response is not None:
        logger.trace(f"{this()}: response.status_code: {response.status_code}")
        data = response.json()
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
                    code = response[''],
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

# Update Rates from EG Collector ---------------------------------------
def trx_ura_update_butler_rates(app):
    logger.debug(f'{this()}: IN')
    result   = get_api_response(    code=BUTLER_CORE_TRX_ERROR,
                                    message=f'NO TRX RESPONSE')
    
    host     = app.config.get('COLLECTOR_HOST')
    port     = app.config.get('COLLECTOR_PORT')
    username = app.config.get('COLLECTOR_USERNAME')
    password = app.config.get('COLLECTOR_PASSWORD')
    protocol = app.config.get('COLLECTOR_PROTOCOL')
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
                    password=password
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
                    code = response[''],
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

# Update Disk Images from Nutanix (Prism Central + Prism Element(s)) ---
def trx_uim_update_butler_images(app):
    logger.debug(f'{this()}: IN')
    result   = get_api_response(    code=BUTLER_CORE_TRX_ERROR,
                                    message=f'NO TRX RESPONSE')
    
    host     = app.config.get('NUTANIX_HOST')
    port     = app.config.get('NUTANIX_PORT')
    username = app.config.get('NUTANIX_USERNAME')
    password = app.config.get('NUTANIX_PASSWORD')
    protocol = app.config.get('NUTANIX_PROTOCOL')
    endpoint = 'api/nutanix/v3/clusters/list'
    arguments=''
    
    headers  = {'Content-Type': 'application/json'}
    data     = {'kind': 'cluster'}
    url      = f'{protocol}://{host}:{port}/{endpoint}{arguments}'

    logger.debug(f'{this()}: Look for clusters')
    logger.debug(f'{this()}: user = {username}')
    logger.debug(f'{this()}: url  = {url}')

    clusters = api_request('POST',
                    url,
                    data=data,
                    headers=headers,
                    username=username,
                    password=password
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
        
        logger.debug(f'{this()}: Got {len(cluster_ips)} clusters')
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
                            password=password
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
                            #row.comments=entity['uuid']
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
            logger.debug(f"{this()}: Got: {len(rows)} Images.")
            if len(rows):
                current['images']=rows
                # delete obsolete codes
                rows_to_delete = db.session.query(Nutanix_VM_Images
                    ).filter(Nutanix_VM_Images.imageservice_uuid_diskclone.notin_(keep)
                    ).all()
                logger.debug(f'{this()}: Images to delete = {len(rows_to_delete)}')
                for row in rows_to_delete:
                    db.session.delete(row)
                db.session.commit()
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
            message = f'{this}: No Clusters found.',
            execution_context = None,
        )
    logger.debug(f'{this()}: OUT')
    tracebox_log(f'{this()}: {str(result)}',
            logger=logger,level=logging.DEBUG,length=tracebox_log_length)
    return result

# Update Projects from Nutanix Prism Central ---------------------------
def trx_upr_update_butler_projects(app):
    logger.debug(f'{this()}: IN')
    result   = get_api_response(    code=BUTLER_CORE_TRX_ERROR,
                                    message=f'NO TRX RESPONSE')
    
    host     = app.config.get('NUTANIX_HOST')
    port     = app.config.get('NUTANIX_PORT')
    username = app.config.get('NUTANIX_USERNAME')
    password = app.config.get('NUTANIX_PASSWORD')
    protocol = app.config.get('NUTANIX_PROTOCOL')
    endpoint = 'api/nutanix/v3/projects/list'
    arguments=''
    
    headers  = {'Content-Type': 'application/json'}
    data     = {'kind': 'project'}
    url      = f'{protocol}://{host}:{port}/{endpoint}{arguments}'

    logger.debug(f'{this()}: user = {username}')
    logger.debug(f'{this()}: url  = {url}')

    projects = api_request('POST',
                    url,
                    data=data,
                    headers=headers,
                    username=username,
                    password=password
                    )        

    if projects is not None:
        data = projects.json()
        rows=[]
        # Actual process of result here
        for entity in projects.json()['entities']:
            try:
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
            except Exception as e:
                logger.debug(f'{this()}: exception: {str(e)}')
                                    
        # rows contains all Projects from Nutanix
        # only these projects should remain in butler
        try:
            keep=[]
            for row in rows:
                db.session.merge(row)
                keep.append(row.project_uuid)
                logger.trace(f'{this()}: project={row}')
            db.session.commit()
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
            message = f'{this}: No Projects found.',
            execution_context = None,
        )
    logger.debug(f'{this()}: OUT')
    tracebox_log(f'{this()}: {str(result)}',
            logger=logger,level=logging.DEBUG,length=tracebox_log_length)
    return result

# Update Categories from Nutanix Prism Central -------------------------
def trx_uca_update_butler_categories(app):
    logger.debug(f'{this()}: IN')
    result   = get_api_response(    code=BUTLER_CORE_TRX_ERROR,
                                    message=f'NO TRX RESPONSE')
    
    host     = app.config.get('NUTANIX_HOST')
    port     = app.config.get('NUTANIX_PORT')
    username = app.config.get('NUTANIX_USERNAME')
    password = app.config.get('NUTANIX_PASSWORD')
    protocol = app.config.get('NUTANIX_PROTOCOL')
    endpoint = 'api/nutanix/v3/categories/list'
    arguments=''
    
    headers  = {'Content-Type': 'application/json'}
    data     = {'kind': 'category'}
    url      = f'{protocol}://{host}:{port}/{endpoint}{arguments}'

    logger.debug(f'{this()}: user = {username}')
    logger.debug(f'{this()}: url  = {url}')

    categories = api_request('POST',
                    url,
                    data=data,
                    headers=headers,
                    username=username,
                    password=password
                    )        

    if categories is not None:
        data = categories.json()
        if categories.status_code == 200:
            #if data_clusters['status']['code'] == 0:
            rows=[]
            # Actual process of result here
            for entity in categories.json()['entities']:
                if not entity['system_defined']:
                    try:
                        row=Categories()
                        row.category_name = entity['name']
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
            kind = 'disk image',
            length = len(rows),
            offset = 0,
            )
    else:
        result = get_api_response(
            # status arguments
            state = 'ERROR',
            code = 1,
            message = f'{this}: No Categories found.',
            execution_context = None,
        )
    logger.debug(f'{this()}: OUT')
    tracebox_log(f'{this()}: {str(result)}',
            logger=logger,level=logging.DEBUG,length=tracebox_log_length)
    return result

# update Subnets from Nutanix Prism Central Projects -------------------
def trx_usn_update_butler_subnets(app):
    logger.debug(f'{this()}: IN')
    result   = get_api_response(    code=BUTLER_CORE_TRX_ERROR,
                                    message=f'NO TRX RESPONSE')
    
    host     = app.config.get('NUTANIX_HOST')
    port     = app.config.get('NUTANIX_PORT')
    username = app.config.get('NUTANIX_USERNAME')
    password = app.config.get('NUTANIX_PASSWORD')
    protocol = app.config.get('NUTANIX_PROTOCOL')
    endpoint = 'api/nutanix/v3/subnets/list'
    arguments=''
    
    headers  = {'Content-Type': 'application/json'}
    data     = {'kind': 'subnet'}
    url      = f'{protocol}://{host}:{port}/{endpoint}{arguments}'

    logger.debug(f'{this()}: user = {username}')
    logger.debug(f'{this()}: url  = {url}')

    subnets = api_request('POST',
                    url,
                    data=data,
                    headers=headers,
                    username=username,
                    password=password
                    )        

    if subnets is not None:
        if subnets.status_code == 200:
            rows=[]
            # Actual process of result here
            data = subnets.json()
            logger.debug(f"{this()}: Subnets = {len(data['entities'])}")
            for entity in data['entities']:
                logger.trace(pformat(entity))
                try:
                    row=Subnets()
                    row.uuid               = entity['metadata']['uuid']
                    row.name               = entity['spec']['name']
                    row.vlan_id            = entity['spec']['resources']['vlan_id']
                    row.vswitch_name       = entity['spec']['resources']['vswitch_name']
                    row.type               = entity['spec']['resources']['subnet_type']
                    row.default_gateway_ip = entity['spec']['resources']['ip_config']['default_gateway_ip']
                    row.range              = entity['spec']['resources']['ip_config']['pool_list'][0]['range']
                    row.prefix_length      = entity['spec']['resources']['ip_config']['prefix_length']
                    row.subnet_ip          = entity['spec']['resources']['ip_config']['subnet_ip']
                    row.cluster            = entity['spec']['cluster_reference']['uuid']
                    rows.append(row)
                    logger.debug(f'{this()}: Subnet: {row.name}')
                except Exception as e:
                    logger.warning(f'{this()}: Uncomplete Subnet {row.name} exception{str(e)}')

            # rows contains all Subnets from Nutanix
            # only these projects should remain in butler
            try:
                keep=[]
                for row in rows:
                    db.session.merge(row)
                    keep.append(row.uuid)
                db.session.commit()
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
            message = f'{this}: No Subnets found.',
            execution_context = None,
        )
    logger.debug(f'{this()}: OUT')
    tracebox_log(f'{this()}: {str(result)}',
            logger=logger,level=logging.DEBUG,length=tracebox_log_length)
    return result

# Request is approved but not VM Creation requested yet ----------------
def trx_001_not_nutanix_pending(app):
    logger.debug(f'{this()}: IN')
    # query for matching rows for transaction
    trx=1
    try:
        rows = butler_trx_get(transaction=trx,session=db.session,logger=logger)
        # process result here
        if rows is not None and len(rows):
            logger.debug(f'Transaction {BUTLER_TRANSACTIONS[trx]}: {len(rows)} rows found : ')
            for row in rows:
                # Process row here
                # For transaction 001
                # build Nutanix Request
                logger.trace(f'{this()}: row={row}')
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
                endpoint  = 'api/nutanix/v3/vms'
                url       = f'{protocol}://{host}:{port}/{endpoint}'
                headers   = ''
                disk_list = []
                nic_list  = []
                # Load Disk List ---------------------------------------
                for i in range(12):
                    size  = getattr(row.Nutanix_Prism_VM,f'disk_{i}_size')
                    image = getattr(row.Nutanix_Prism_VM,f'disk_{i}_image')
                    disk  = {}
                    if size or len(image):
                        # If Disk Size is requested --------------------
                        if size:    disk.update({
                                'disk_size_mib':size*1024,
                                'device_properties':{
                                    'device_type':'DISK'
                                },
                            })
                        # If Base Image is provided --------------------
                        if image:   disk.update({
                                'data_source_reference':{
                                    'kind':'image',
                                    'uuid':image
                                }
                            })
                        disk_list.append(disk)
                # Try to get proper project UUID -----------------------
                if project['uuid'] is None:
                    if project['name'] is None:
                        if len(current['projects']):
                            project['name'] = current['projects'][0].project_name
                            project['uuid'] = current['projects'][0].project_uuid
                            logger.warning(f"{this()}: Default Project {project['name']} set up as per 1st current project")
                        else:
                            project['name'] = app.config.get('NUTANIX_PROJECT',None)
                            project['uuid'] = app.config.get('NUTANIX_PROJECT_UUID',None)
                            logger.warning(f"{this()}: Default Project {project['name']} set up as per configurarion")
                    else:
                        found = False
                        for p in current['projects']:
                            if p.project_name == project['name']:
                                project['uuid'] = p.project_uuid
                                found = True
                                logger.warning(f"{this()}: Project Name {project['name']} found in current projects ({project['uuid']})")
                                break
                        if not found:
                            project['uuid'] = None
                else:
                    for p in current['projects']:
                        found = False
                        if p.project_uuid == project['uuid']:
                            project['name'] = p.project_name
                            found = True
                            logger.warning(f"{this()}: Project UUID {project['uuid']} found in current projects ({project['name']})")
                            break
                    if not found:
                        project['uuid'] = None
                logger.trace(f'{this()}: project={project}')
                # Load NIC List ----------------------------------------
                # Depends on Project
                row.Nutanix_Prism_VM.project_uuid = project['uuid']
                if row.Nutanix_Prism_VM.project_uuid is not None and row.Nutanix_Prism_VM.project_uuid != '0':
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
                    for subnet in subnets:
                        nic_list.append(
                            {
                                'nic_type':'NORMAL_NIC',
                                'is_connected': True,
                                'ip_endpoint_list':[
                                    {'ip_type': 'DHCP'}
                                ],
                                'subnet_reference':{
                                    'kind':'subnet',
                                    'name': subnet[1],
                                    'uuid': subnet[0]
                                }
                            }
                        )
                else:
                    logger.warning(f'{this()}: Invalid project uuid:{row.Nutanix_Prism_VM.project_uuid}')
                # load disk list here
                data     = {
                'spec':{
                    'description': row.Nutanix_Prism_VM.vm_name,
                    'name': row.Nutanix_Prism_VM.vm_name,
                    'resources':{
                        'power_state': 'ON',
                        'num_vcpus_per_socket': row.Nutanix_Prism_VM.vcpus_per_socket,
                        'num_sockets':row.Nutanix_Prism_VM.num_sockets,
                        'memory_size_mib':row.Nutanix_Prism_VM.memory_size_gib*1024,
                        'disk_list': disk_list,
                        'nic_list': nic_list,
                        }
                    },
                'metadata':{
                    'kind':'vm',
                    'project_reference':{
                        'kind': 'project',
                        'name': project['name'],
                        'uuid': project['uuid']
                        }
                    },
                    #'categories':['prd']
                }
                # ------------------------------------------------------
                # Actual VM Creation Request here
                # get Nutanix Response
                # First check that VM is not existent
                vm = get_nutanix_vm(app,row.Nutanix_Prism_VM.vm_name)
                if vm is None:
                    logger.debug(f'{this()}: url =  {url}')
                    logger.trace(f'{this()}: data = {data}')
                    response = api_request(    
                                    'POST',
                                    url,
                                    data=data,
                                    headers=headers,
                                    username=username,
                                    password=password
                                )
                    if response is not None:
                        if response.ok:
                            data = response.json()
                            if data['status']['state'] == 'PENDING':
                                row.Requests.Task_uuid   = data['status']['execution_context']['task_uuid']
                                row.Requests.Task_status = 0
                                row.Requests.uuid        = data['metadata']['uuid']
                                row.Requests.Status = REQUEST_APPROVED + NUTANIX_PENDING
                                row.Requests.Comments = '' if row.Requests.Comments is None else row.Requests.Comments
                                row.Requests.Comments += f"Provisionando @ {strftime('%d/%m/%y %H:%S')}."
                                row.Nutanix_Prism_VM.vm_uuid = data['metadata']['uuid']
                                db.session.merge(row.Requests)
                                db.session.merge(row.Nutanix_Prism_VM)
                                db.session.commit()
                                logger.debug(f'{this()}: {row.Requests} updated')
                        else:
                            logger.error(f'{this()}: response.status_code = {response.status_code}')
                            logger.error(f'{this()}: response.reason      = {response.reason}')
                            logger.error(f'{this()}: response.text        = {response.text}')
                    else:
                        logger.critical(f'{this()}: response = {response}')
                else:
                    logger.warning(f"{this()}: VM '{row.Nutanix_Prism_VM.vm_name}' ya existe en NUTANIX {host}")
                    row.Requests.Status = REQUEST_ERROR
                    row.Requests.Comments = '' if row.Requests.Comments is None else row.Requests.Comments
                    row.Requests.Comments += f"Error @ {strftime('%d/%m/%y %H:%S')}"
                    db.session.merge(row.Requests)
                    db.session.merge(row.Nutanix_Prism_VM)
                    db.session.commit()
                    logger.debug(f'{this()}: {row.Requests} updated')
                # ------------------------------------------------------
            result   =  get_api_response(   code=BUTLER_CORE_TRX_OK,
                            message=f'{this()}: trx: {trx} : {len(rows)} Requests processed.'
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

# Request is approved but CC is not populated in EG Collector ----------
def trx_002_not_collector_pending(app):
    logger.debug(f'{this()}: IN')
    # query for matching rows for transaction
    trx=2
    try:
        rows = butler_trx_get(transaction=trx,session=db.session,logger=logger)
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
                                password=password
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
                                        password=password
                                    )
                        if response is not None:
                            if response.ok:
                                data=response.json()
                                if data['status'] == 'OK':
                                    row.Status += COLLECTOR_COMPLETED
                                    row.Comments = '' if row.Comments is None else row.Comments
                                    row.Comments += f"Tarificada @ {strftime('%d/%m/%y %H:%S')}."
                                    db.session.merge(row)
                                    db.session.commit()
                                    logger.debug(f'{this()}: {row} updated')
                            else:
                                logger.error(f'{this()}: response.status_code = {response.status_code}')
                                logger.error(f'{this()}: response.reason      = {response.reason}')
                                logger.error(f'{this()}: response.text        = {response.text}')
                        else:
                            logger.error(f'{this()}: response = {response}')
                    else:
                            logger.warning(f"{this()}: CI '{data['CI_Name']}' not found in Collector.")
                else:
                            logger.error(f"{this()}: no response from Collector ({url} {data}).")                    
            result   =  get_api_response(   code=BUTLER_CORE_TRX_OK,
                            message=f'{this()}: trx: {trx} : {len(rows)} CIs updated.'
                            )
        else:
            result   =  get_api_response(   code=BUTLER_CORE_TRX_ERROR,
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

# Nutanix VM Creation was requested, checks for completion -------------
def trx_003_nutanix_pending(app):
    logger.debug(f'{this()}: IN')
    # query for matching rows for transaction
    trx=3
    try:
        rows = butler_trx_get(transaction=trx,session=db.session,logger=logger)
        # process result here
        if rows is not None and len(rows):
            logger.debug(f'Transaction {BUTLER_TRANSACTIONS[trx]}: {len(rows)} rows found : ')
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
                                password=password
                            )
                logger.debug(f'{this()}: response = {response}')
                if response is not None:
                    if response.ok:
                        try:
                            data=response.json()
                            if data['status'] == 'SUCCEEDED':
                                row.Task_status = 1
                                row.Status -= NUTANIX_PENDING
                                row.Status += NUTANIX_COMPLETED
                                row.Comments = '' if row.Comments is None else row.Comments
                                row.Comments += f"Provisionada @ {strftime('%d/%m/%y %H:%S')}."
                                db.session.merge(row)
                                db.session.commit()
                                logger.debug(f'{this()}: {row} updated')                    
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
            result   =  get_api_response(   code=BUTLER_CORE_TRX_OK,
                            message=f'{this()}: trx: {trx} : {len(rows)} Tasks processed.'
                            )
        else:
            result   =  get_api_response(   code=BUTLER_CORE_TRX_ERROR,
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
    logger.debug(f'{this()}: IN')
    # query for matching rows for transaction
    trx=4
    try:
        rows = butler_trx_get(transaction=trx,session=db.session,logger=logger)
        # process result here
        if rows is not None and len(rows):
            logger.debug(f'Transaction {BUTLER_TRANSACTIONS[trx]}: {len(rows)} rows found : ')
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
                endpoint  = f'api(nutanix/v3/vms/{row.Requests.uuid}'
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
                                password=password
                            )
                if response is not None:
                    data=response.json()
                    if response.ok:
                        # Oportunity check for DRP Schedule
                        # implementation. requires:
                        # row.Nutanix_Prism_VM.vm_name
                        # Using defaults oportunity for customization
                        pdname                   = None
                        annotation               = None
                        remote_cluster           = app.config.get('NUTANIX_REMOTE_CLUSTER',None)
                        schedule_type            = app.config.get('NUTANIX_SCHEDULE_TYPE','HOURLY')
                        user_start_time_in_usecs = None
                        every_nth                = app.config.get('NUTANIX_EVERY_NTH',None),
                        local_max_snapshots      = app.config.get('NUTANIX_LOCAL_MAX_SNAPSHOTS',4)
                        remote_max_snapshots     = app.config.get('NUTANIX_REMOTE_MAX_SNAPSHOTS',4)
                        timeout                  = app.config.get('NUTANIX_TIMEOUT',None)
                        
                        if row.Nutanix_Prism_VM.vm_drp:
                            logger.debug(f"{this()}: DRP requested fo for VM: '{row.Nutanix_Prism_VM.vm_name}'")
                            if create_drp(
                                    app,
                                    vmname                   = row.Nutanix_Prism_VM.vm_name,
                                    pdname                   = pdname,
                                    annotation               = annotation,
                                    remote_cluster           = remote_cluster,
                                    schedule_type            = schedule_type,
                                    user_start_time_in_usecs = user_start_time_in_usecs,
                                    every_nth                = every_nth,
                                    local_max_snapshots      = local_max_snapshots,
                                    remote_max_snapshots     = remote_max_snapshots,
                                    timeout                  = timeout
                                    ):
                                logger.info(f"{this()}: DRP for VM: '{row.Nutanix_Prism_VM.vm_name}' Success !!!")
                            else:
                                logger.warning(f"{this()}: DRP for VM: '{row.Nutanix_Prism_VM.vm_name}' Failure !!!")
                        
                        # ----------------------------------------------
                        try:
                            # Check for first valid IP address
                            ip = data['spec']['resources']['nic_list']['0']['ip_endpoint_list'][0]
                        except:
                            ip = None
                        if ip is not None:
                            # ------------------------------------------
                            # Update VM IP, will setup a temporary
                            # Monitor Pending Status
                            # ------------------------------------------
                            row.Task_status = 1
                            row.Requests.Status += MONITOR_PENDING
                            db.session.merge(row.Requests)
                            db.session.commit()
                            logger.debug(f'{this()}: {row} updated')                    
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
                            endpoint  = f'v1/objects/hosts/{row.uuid}'
                            url       = f'{protocol}://{host}:{port}/{endpoint}'
                            headers   = ''
                            data     = {
                                'attrs':{
                                    'address':row.Nutanix_Prism_VM.vm_ip,
                                    'display_name':row.Nutanix_Prism_VM.vm_name,
                                    'check_command':'hostalive'
                                }
                            }
                            # get Icinga Response ----------------------
                            logger.debug(f'{this()}: url = {url}')
                            # Will instruct Icinga to create new Host
                            response = api_request(    
                                            'PUT',
                                            url,
                                            data=data,
                                            headers=headers,
                                            username=username,
                                            password=password
                                        )
                            # If all goes OK, Then complete status -----
                            if response is not None and response.ok:
                                if response.status_code == 200:
                                    row.Requests.Status -= MONITOR_PENDING
                                    row.Requests.Status += MONITOR_COMPLETED
                                    row.Requests.Comments = '' if row.Requests.Comments is None else row.Requests.Comments
                                    row.Requests.Comments += f"Monitoreada @ {strftime('%d/%m/%y %H:%S')}"
                                    db.session.merge(row.Requests)
                                    db.session.commit()
                            else:
                                logger.error(f'{this()}: response = {response}')
                    else:
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

    logger.debug(f'{this()}: OUT')
    tracebox_log(f'{this()}: {str(result)}',
            logger=logger,level=logging.DEBUG,length=tracebox_log_length)
    return result

# In case TRX 004 was only partially success, it will complete EG Monitor
# status here
def trx_005_monitor_pending(app):
    logger.debug(f'{this()}: IN')
    # query for matching rows for transaction
    trx=5
    try:
        rows = butler_trx_get(transaction=trx,session=db.session,logger=logger)
        # process result here
        if rows is not None and len(rows):
            logger.debug(f'Transaction {BUTLER_TRANSACTIONS[trx]}: {len(rows)} rows found : ')
            for row in rows:
                # Process row here
                # For transaction 005
                # Try to create EG Monitor Host
 
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
                endpoint  = f'v1/objects/hosts/{row.uuid}'
                url       = f'{protocol}://{host}:{port}/{endpoint}'
                headers   = ''
                data     = {
                    'attrs':{
                        'address':row.Nutanix_Prism_VM.vm_ip,
                        'display_name':row.Nutanix_Prism_VM.vm_name,
                        'check_command':'hostalive'
                    }
                }
                # get Icinga Response ----------------------
                logger.debug(f'{this()}: url = {url}')
                # Will instruct Icinga to create new Host
                response = api_request(    
                                'PUT',
                                url,
                                data=data,
                                headers=headers,
                                username=username,
                                password=password
                            )
                # If all goes OK, Then complete status -----------------
                if response is not None and response.ok:
                    if response.status_code == 200:
                        row.Requests.Status -= MONITOR_PENDING
                        row.Requests.Status += MONITOR_COMPLETED
                        row.Requests.Comments = '' if row.Requests.Comments is None else row.Requests.Comments
                        row.Requests.Comments += f"Monitoreada @ {strftime('%d/%m/%y %H:%S')}"
                        db.session.merge(row.Requests)
                        db.session.commit()
                else:
                    logger.error(f'{this()}: response.status_code = {response.status_code}')
                    logger.error(f'{this()}: response.reason      = {response.reason}')
                    logger.error(f'{this()}: response.text        = {response.text}')
            result   =  get_api_response(   code=BUTLER_CORE_TRX_OK,
                            message=f'{this()}: trx: {trx} : {len(rows)} Requests processed.'
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
        #logger.critical(f'{this()}: response = {response}')
        result   =  get_api_response(   code=BUTLER_CORE_TRX_ERROR,
                        message=f'{this()}: Exception: {str(e)}'
                        )

    logger.debug(f'{this()}: OUT')
    tracebox_log(f'{this()}: {str(result)}',
            logger=logger,level=logging.DEBUG,length=tracebox_log_length)
    return result

# In case EG Collector keeps on pending status -------------------------
def trx_006_collector_pending(app):
    logger.debug(f'{this()}: IN')
    result   = get_api_response(    code=BUTLER_CORE_TRX_OK,
                                    message=f'NO TRX RESPONSE')
    logger.debug(f'{this()}: OUT')
    tracebox_log(f'{this()}: {str(result)}',
            logger=logger,level=logging.DEBUG,length=tracebox_log_length)
    return result

# Check for all requirements completed ---------------------------------
def trx_007_all_completed(app):
    logger.debug(f'{this()}: IN')
    # query for matching rows for transaction
    trx=7
    try:
        rows = butler_trx_get(transaction=trx,session=db.session,logger=logger)
        # process result here
        if rows is not None and len(rows):
            logger.debug(f'Transaction {BUTLER_TRANSACTIONS[trx]}: {len(rows)} rows found : ')
            for row in rows:
                # Process row here
                # For transaction 007
                # Check for full completion in order to finalize
                # request life cycle
                row.Status += REQUEST_COMPLETED
                row.Comments = '' if row.Comments is None else row.Comments
                row.Comments += f"Completa @ {strftime('%d/%m/%y %H:%S')}. Estado Final."
                db.session.merge(row)
                db.session.commit()
                logger.debug(f'{this()}: {row} updated')
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
        #logger.critical(f'{this()}: response = {response}')
        result   =  get_api_response(   code=BUTLER_CORE_TRX_ERROR,
                        message=f'{this()}: Exception: {str(e)}'
                        )

    logger.debug(f'{this()}: OUT')
    tracebox_log(f'{this()}: {str(result)}',
            logger=logger,level=logging.DEBUG,length=tracebox_log_length)
    return result

# ======================================================================
# Main transactions caller
# ======================================================================
def execute_transactions(app):
    logger.info(f"{this()}: Start @ {time.strftime('%Y-%m-%d %H:%M:%S')}")
    # Trx execution order is important if 'current' data will be used
    # from 'previous' trx
    global tracebox_log_length
    tracebox_log_length = app.config.get('TRACEBOX_LOG_LENGTH',80)
    print(f'{this()}: tracebox_log_length = {tracebox_log_length}')
    transactions = [
        trx_ucc_update_butler_cost_centers,
        trx_ura_update_butler_rates,
        trx_uim_update_butler_images,
        trx_usn_update_butler_subnets,  # Subnets to be consumed by projects
        trx_upr_update_butler_projects,
        trx_uca_update_butler_categories,
        trx_001_not_nutanix_pending,
        trx_002_not_collector_pending,
        trx_003_nutanix_pending,
        trx_004_nutanix_completed,
        trx_005_monitor_pending,
        trx_006_collector_pending,
        trx_007_all_completed
    ]
    for transaction in transactions:
        active      = app.config.get(transaction.__name__.upper(),True)
        if active:
            print(f"{this()}: Transaction '{transaction.__name__}' is active.")
            try:
                db.session.close()
            except Exception as e:
                logger.error(f'{this()}: exception: {str(e)}')
                db.session.rollback()
            result = transaction(app)
            try:
                result = json.loads(result)
                if result['status']['code'] != BUTLER_CORE_TRX_OK:
                    logger.error(f"{this()}: Transaction '{transaction.__name__}' Error {result['status']['message']}")
            except Exception as e:
                print(f"{this()}: Transaction '{transaction.__name__}' exception = {str(e)}")
                tracebox_log(f"{this()}: Transaction '{transaction.__name__}' exception = {str(e)}",
                    logger = logger,
                    level  = logging.CRITICAL,
                    length = tracebox_log_length
                    )
        else:
            print(f"{this()}: WARNING Transaction '{transaction.__name__}' is inactive.")
    for key in current:
        logger.info(f"{this()}: {key} = {len(current[key])}")
    logger.info(f"{this()}: Completed @ {time.strftime('%Y-%m-%d %H:%M:%S')}.")
