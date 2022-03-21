# ======================================================================
# BUTLER MIGRATION ROUTES
# View for Protection Domains/VMs Migration Edition
# (c) Emtec/Sertechno 2022
# GLVH @ 2022-01-19
# ======================================================================
import os
import sys
import jinja2
import copy
from pprint                 import pformat
from sqlalchemy             import desc
from emtec                  import *
from emtec.debug            import *
from emtec.data             import *
from emtec.butler.forms     import frm_migration_01,form_log
from emtec.butler.functions import *
from emtec.feedback         import *
from wtforms                import BooleanField
from wtforms                import IntegerField
from flask                  import Flask
from flask                  import g
from emtec.nutanix          import *
import  pandas
from    pandas.io.json          import json_normalize
from    flask                   import send_file
import  tempfile

import urllib3
urllib3.disable_warnings()

# Templates will reside on view_request_template.py
# Functions will reside on view_request_functions.py

def format_timestamp(timestamp,format="%Y-%m-%d %H:%M:%S"):
    ''' Fortmat a timestamp as and returns a formated string '''
    if timestamp is None:
        return ""
    return datetime.fromtimestamp(timestamp).strftime(format)

# GV Support functions
def nutanix_get_vm_list(host=None,port=9440,username=None,password=None,protocol='https',version=2,verify=False,timeout=10,logger=None):
    response = None
    try:
        if version == 2:            
            endpoint = '/api/nutanix/v2.0/vms/'
            url      = f"{protocol}://{host}:{port}/{endpoint}"
            response = api_request(
                method         = 'GET',
                url            = url,
                headers        = {'Accept': 'application/json'},
                data           = None,
                timeout        = 10,
                authentication = None,
                username       = username,
                password       = password,
                verify         = verify,
                logger         = logger
                )
            #response = requests.get(url,auth=(username,password),headers=headers,verify=verify,timeout=timeout)
        elif version == 3:
            '''
            method   = 'POST'
            endpoint = '/api/nutanix/v3/vms/list'
            headers  = {'Accept':'application/json','Content-Type': 'application/json'}
            data     = {'kind':'vm'}
            url      = f"{protocol}://{host}:{port}/{endpoint}"
            response = requests.get(url,auth=(username,password),headers=headers,data=data,verify=verify,timeout=timeout)
            '''
            protocol = 'https'
            endpoint = '/api/nutanix/v3/vms/list'
            url      = f"{protocol}://{cluster.get('host')}:{cluster.get('port')}/{endpoint}"
            response = api_request(
                method         = 'POST',
                url            = url,
                headers        = {'Accept':'application/json','Content-Type': 'application/json'},
                data           = {'kind':'vm'},
                timeout        = 10,
                authentication = None,
                username       = cluster.get('username'),
                password       = cluster.get('password'),
                verify         = False,
                logger         = logger
                )
            
            
            
    except Exception as e:
        emtec_handle_general_exception(e,logger=logger)
    return response

def get_vm_project(form,vm_uuid):
    project = None
    cluster = form.mgData.get('clusters_uuid').get('prism_central')
    logger.debug(f"{this()}: cluster: {cluster}")
    protocol = 'https'
    endpoint = f'api/nutanix/v3/vms/{vm_uuid}'
    url      = f"{protocol}://{cluster.get('host')}:{cluster.get('port')}/{endpoint}"
    response = api_request(
        method         = 'GET',
        url            = url,
        headers        = {'Content-Type': 'application/json'},
        data           = None,
        timeout        = 10,
        authentication = None,
        username       = cluster.get('username'),
        password       = cluster.get('password'),
        verify         = False,
        logger         = logger
        )
    logger.debug(f"{this()}: response: {response}")
    if response is not None:
        if response.ok:
            if response.status_code == 200:
                data = response.json()
                if 'metadata' in data:
                    project = data['metadata'].get('project_reference')
                else:
                    logger.error(f"{this()}: no 'metadata' in response: {response}")                    
            else:
                logger.warning(f"{this()}: response status = {response}")
        else:
            logger.warning(f"{this()}: response not OK = {response}")            
    else:
        logger.warning(f"{this()}: response = {response}")
        
    return project

def get_projects_list(form):
    projects_list = {}
    cluster = form.mgData.get('clusters_uuid').get('prism_central')
    logger.debug(f"{this()}: cluster: {cluster}")
    protocol = 'https'
    endpoint = f'api/nutanix/v3/projects/list'
    url      = f"{protocol}://{cluster.get('host')}:{cluster.get('port')}/{endpoint}"
    response = api_request(
        method         = 'POST',
        url            = url,
        headers        = {'Accept': 'application/json','Content-Type': 'application/json'},
        data           = json.dumps({
                            'kind':'project'
                            }),
        timeout        = 10,
        authentication = None,
        username       = cluster.get('username'),
        password       = cluster.get('password'),
        verify         = False,
        logger         = logger
        )
        
    logger.debug(f"{this()}: response: {response}")
    if response is not None:
        if response.ok:
            if response.status_code == 200:
                data = response.json()
                entities = data.get('entities')
                logger.debug(f"{this()}: {len(entities)} projects found in {cluster.get('host')}")
                for entity in entities:
                    projects_list.update({
                        entity.get('status').get('name'):{
                            'status': entity.get('status').get('status'),
                            'uuid'  : entity.get('metadata').get('uuid'),
                            }
                    })
            else:
                logger.warning(f"{this()}: response status = {response}")
        else:
            logger.warning(f"{this()}: response not OK = {response}")            
            logger.warning(f"{this()}: response url    = {response.url}")            
            logger.warning(f"{this()}: response not OK = {response.text}")            
            logger.warning(f"{this()}: response not OK = {dir(response)}")            
            logger.warning(f"{this()}: response request = {response.request}")            
            logger.warning(f"{this()}: response request = {dir(response.request)}")            
            logger.warning(f"{this()}: response request body= {response.request.body}")            
    else:
        logger.warning(f"{this()}: response = {response}")
        
    return projects_list

# GV Group Oriented functions
def forms_Migration_create_group(form):
    groupid=0
    try:
        logger.debug(f"{this()}: IN new name = {form.mgNewName.data}")
        logger.debug(f"{this()}: form.data = {form.data}")
        logger.debug(f"{this()}: type(form.data) = {type(form.data)}")
        if form.mgNewName.data is not None and len(form.mgNewName.data):
            groupid   = form.mgId
            groupname = form.mgNewName.data
            Origin    = form.data.get('mgOrigin')
            Destiny   = form.data.get('mgDestiny')
            Customer  = form.data.get('mgCustomer')
            Platform  = form.data.get('mgPlatform')
            if Origin   is None: Origin = ''
            if Destiny  is None: Destiny = ''
            if Customer is None: Customer = 0
            if Platform is None: Platform = 0
            logger.debug(f"{this()}: groupid={groupid} groupname={groupname}")
            logger.debug(f"{this()}: Origin   = {Origin}")
            logger.debug(f"{this()}: Destiny  = {Destiny}")
            logger.debug(f"{this()}: Customer = {Customer}")
            logger.debug(f"{this()}: Platform = {Platform}")
            # Aqui debe crear el grupo de migracion si no existe y 
            # llamar a forms/Migration con el nuevo Id
            mgs = db.session.query(Migration_Groups
                    ).filter(Migration_Groups.Name == groupname
                ).all()
            if mgs is None or len(mgs)==0:
                # GV its a new group then create one
                # creo nuevo grupo en BD y cargo ultimo id
                try:
                    newmg = Migration_Groups(
                                Name=groupname,
                                Origin  =Origin,
                                Destiny =Destiny,
                                Customer=Customer,
                                Platform=Platform
                                )
                    logger.debug(f"{this()}: 785 groupname={groupname} add newmg={newmg}")
                    db.session.add(newmg)
                    logger.debug(f"{this()}: groupname={groupname} commit {newmg}")
                    try:
                        db.session.commit()
                        logger.warning(f"{this()}: 790 get mg record to get id of {groupname}...")
                        mg = db.session.query(Migration_Groups
                                                ).filter(Migration_Groups.Name==groupname
                                                ).one_or_none()
                        form.mgNewId.data   = mg.MG_Id
                        form.mgNewName.data = mg.Name                        
                    except Exception as e:
                        emtec_handle_general_exception(e,logger=logger)
                        form.mgNewId.data = None
                        db.session.rollback()
                        db.session.flush()
                        flash(f"{this()}: {gettext('exception')}: {str(e)}","error")  
                    logger.debug(f"{this()}: form.mgNewId.data =  {form.mgNewId.data}")                                    
                except Exception as e:
                    emtec_handle_general_exception(e,logger=logger)
                    flash(f"{this()}: {gettext('exception')}: {str(e)}","error")
                    db.session.rollback()
                    db.session.flush()
            else:
                # GV This groupname already exists
                logger.warning(f"""{this()}: {gettext("Group '%s' already exists")}"""%groupname)
                logger.warning(f"""{this()}: {gettext("Group '%s' already exists")}"""%mgs)
                for mg in mgs:
                    if mg.Name == groupname:
                        form.mgNewId.data=mg.MG_Id
                        break
                logger.warning(f"""{this()}: {gettext("Group '%s' already exists with id = %s")}"""%(groupname,form.mgNewId.data))
                flash(gettext("Group '%s' already exists with id = %s")%(groupname,form.mgNewId.data))
            groupid   = form.mgNewId.data
            logger.debug(f"{this()}: OUT returns Group Id = {groupid}")
        else:
            flash(gettext("Invalid group '%s'")%(form.mgNewName.data),"error")        
            groupid   = form.mgId
    except Exception as e:
        flash(f"{this()}: {gettext('exception')}: {str(e)}","error")
        emtec_handle_general_exception(e,logger=logger)
        db.session.rollback()
        db.session.flush()
    return groupid

def forms_Migration_add_vm_to_group(form,vmId):
    vmName = None
    # Aqui debe crear el registro de vm asociado al grupo 
    # llamar a forms/Migration con el mismo form.mgId
    try:
        try:
            for cluster_uuid in form.mgData.get('vm_list'):
                logger.debug(f"cluster_uuid={cluster_uuid}")
                vms = form.mgData.get('vm_list').get(cluster_uuid).get('vms')
                for vm_name in vms:
                    logger.debug(f"vm_name={vm_name}")
                    if vms.get(vm_name).get('uuid') == vmId:
                        vmName = vm_name
                logger.info(f"vmName={vmName}")
        except Exception as e:
            emtec_handle_general_exception(e,logger=logger)
            vmName = None
        vm = Migration_Groups_VM(MG_Id=form.mgId,vm_uuid=vmId,vm_name=vmName,vm_migrate=True)
        db.session.merge(vm)
        db.session.commit()
        db.session.flush()
        flash(gettext("'%s' added to migration group '%s'")%(
                vmName,
                dict(form.mgName.choices).get(form.mgName.data)
                ),"info")
    except Exception as e:
        emtec_handle_general_exception(e,logger=logger)
    
    logger.info(f"{this()}: return vmName = {vmName}")
    return vmName

def forms_Migration_save_group(form):
    logger.info(f"{this()}: IN")
    logger.debug  (f"{this()}: IN {form.data}")
    try:
        if current_user.confirmed:
            mg = Migration_Groups(
                    MG_Id    = form.mgId,
                    Name     = dict(form.mgName.choices).get(form.mgName.data),
                    Origin   = form.mgOrigin.data,
                    Destiny  = form.mgDestiny.data,
                    Customer = form.mgCustomer,
                    Platform = form.mgPlatform
                    )
            counter = 0
            for vm in form.mgVms:
                try:
                    logger.info(f"{this()}: merging vm: {vm.vm_uuid} {vm.vm_name:30} {vm.vm_migrate}")
                    db.session.merge(vm)
                except Exception as e:
                    emtec_handle_general_exception(e,logger=logger)
                counter+=1
            logger.info(f"{this()}: merging mg: {mg.MG_Id} {mg.Name}")
            db.session.merge(mg)
            db.session.commit()
            db.session.flush()
            flash(gettext("MG saved: (%s) '%s'"%(form.mgId,dict(form.mgName.choices).get(form.mgName.data))),"info")
        else:
            flash(gettext("MG save request by non privileged user: %s")%(current_user.username))
            logger.error(gettext("MG save request by non privileged user: %s")%(current_user.username))
    except Exception as e:
        emtec_handle_general_exception(e,logger=logger)    
        flash(f"{this()}: {gettext('exception')}: {str(e)}","error")
    logger.info(f"{this()}: return Migration Group Id = {form.mgId} {form.mgName.data}")
    return form.mgId

def forms_Migration_clone_group(form):
    original_groupid   = form.mgId
    original_groupname = dict(form.mgName.choices).get(int(form.mgName.data))
    try:
        # GV Asigna nombre de clon
        form.mgNewName = form.mgCloneName
        logger.info(f"{this()}: mgNewName={form.mgNewName.data} mgCloneName={form.mgCloneName.data}")
        new_groupid = forms_Migration_create_group(form)
        logger.info(f"{this()}: new groupid = {new_groupid}")
        try:
            # Cloning VMs, get all former MG VMs
            logger.info(f"{this()}: creating vms from group {original_groupid} to cloned group {new_groupid} ...")
            vms = db.session.query(Migration_Groups_VM
                                ).filter(Migration_Groups_VM.MG_Id==original_groupid
                                ).all()
            # repeat records with new MG Id
            if len(vms):
                logger.info(f"{this()}: original vms count is {len(vms)}")
            try:
                for vm in vms:
                    newvm=Migration_Groups_VM(
                        MG_Id             = new_groupid,
                        vm_uuid           = vm.vm_uuid,
                        vm_name           = vm.vm_name,
                        vm_state          = vm.vm_state,
                        vm_has_pd         = vm.vm_has_pd,
                        vm_pd_name        = vm.vm_pd_name,
                        vm_pd_active      = vm.vm_pd_active,
                        vm_pd_replicating = vm.vm_pd_replicating,
                        vm_migrate        = vm.vm_migrate
                    )
                    logger.debug(f"{this()}: new vm = {newvm}")
                    db.session.merge(newvm)
                db.session.commit()
                logger.info(f"{this()}: MG {original_groupname} successfully cloned as {form.mgNewName.data}")
                flash(gettext("'%s' successfully cloned as '%s'")%(original_groupname,form.mgNewName.data),"info")
            except Exception as e:
                emtec_handle_general_exception(e,logger=logger)
                form.mgNewId.data = None
                db.session.rollback()
                db.session.flush()                        
                flash(gettext("'%s' could not be cloned as '%s'")%(original_groupname,form.mgNewName.data),"error")
        except Exception as e:
            emtec_handle_general_exception(e,logger=logger)
            form.mgNewId.data = None
            db.session.rollback()
            db.session.flush()
            flash(gettext("'%s' could not be cloned")%(original_groupname),"error")
    except Exception as e:
        emtec_handle_general_exception(e,logger=logger)
        flash(gettext("'%s' could not be cloned")%(original_groupname),"error")
    return form.mgNewId.data

def forms_Migration_edit_group(form):
    original_groupid   = form.mgId
    original_groupname = dict(form.mgName.choices).get(form.mgName.data)
    try:
        # GV Nuevo nombre desde modal
        logger.info(f"{this()}: mgEditName={form.mgEditName.data}")
        try:
            # Editing MG Name
            mg = db.session.query(Migration_Groups
                                ).filter(Migration_Groups.MG_Id==original_groupid
                                ).one_or_none()
            if mg:
                # repeat records with new MG Id
                logger.warning(f"{this()}: mg={mg}")
                original_groupname = mg.Name
                
                mg.Name = form.mgEditName.data
                logger.warning(f"{this()}: mg={mg}")
                try:
                    db.session.merge(mg)
                    db.session.commit()
                    logger.info(f"{this()}: MG '{original_groupid}' '{original_groupname}' renamed to '{mg.Name}'")
                    flash(gettext("'%s' renamed to '%s'")%(original_groupname,mg.Name),"info")
                except Exception as e:
                    db.session.rollback()
                    db.session.flush()
                    emtec_handle_general_exception(e,logger=logger)
                    flash(gettext("'%s' could not be renamed to '%s'")%(original_groupname,mg.Name),"error")
            else:
                logger.error(f"{this()}: MG '{original_groupid}' cuold not be renamed to '{mg.Name}'","info")
                flash(gettext("'%s' could not be renamed to '%s'")%(original_groupname,mg.Name),"error")
        except Exception as e:
            emtec_handle_general_exception(e,logger=logger)
            form.mgNewId.data = None
            db.session.rollback()
            db.session.flush()
            flash(gettext("'%s' could not be edited")%(original_groupname),"error")
    except Exception as e:
        emtec_handle_general_exception(e,logger=logger)
        flash(gettext("'%s' could not be edited")%(original_groupname),"error")
    return form.mgId

def forms_Migration_delete_group(form):
    mgId=form.mgId
    
    try:
        vms = db.session.query(Migration_Groups_VM
                    ).filter(Migration_Groups_VM.MG_Id==mgId
                    ).delete()
        logger.warning(f"{this()}: deleted vms = {vms}")
        mg = db.session.query(Migration_Groups
                ).filter(Migration_Groups.MG_Id==mgId
                ).delete()
        logger.warning(f"{this()}: deleted mg = {mg}")
        db.session.commit()
        db.session.flush()
        flash(gettext("MG deleted: (%s) '%s'")%(mgId,dict(form.mgName.choices).get(int(form.mgName.data))),"info")
        mgId = 0
    except Exception as e:
        db.session.rollback()
        emtec_handle_general_exception(e,logger=logger)    
        flash(f"{this()}: {gettext('exception')}: {str(e)}","error")
    if mgId is None:
        mgId = 0
    return mgId

def poll_tasks(form,cluster,version=2):
    logger.debug(f"{this()}: IN cluster = {cluster.get('name')} {len(form.mgData['tasks'])} tasks")
    try:
        for t in range(len(form.mgData['tasks'])):
            task = form.mgData['tasks'][t]
            logger.debug(f"{this()}: INFO task: {task}")
            if not task.get('completed'):
                protocol = 'https'
                if version == 2:
                    endpoint = f"PrismGateway/services/rest/v2.0/tasks/{task.get('uuid')}"
                elif version == 3:
                    endpoint = f"api/nutanix/v3/tasks/{task.get('uuid')}"
                url      = f"{protocol}://{cluster.get('host')}:{cluster.get('port')}/{endpoint}"
                logger.debug(f"{this()}: INFO url: {url}")
                response = api_request(
                    method         = 'GET',
                    url            = url,
                    headers        = {'Accept':'application/json'},
                    data           = None,
                    timeout        = 10,
                    authentication = None,
                    username       = cluster.get('username'),
                    password       = cluster.get('password'),
                    verify         = False,
                    logger         = logger
                    )
                    
                logger.debug(f"{this()}: INFO response: {response}")
                if response is not None:
                    if response.ok:
                        data = response.json()
                        logger.debug(f"{this()}: data: {data}")
                        if response.status_code == 200:
                            form.mgData['tasks'][t].update(data)
                            if version == 2:
                                if task.get('progress_status').upper() in ['SUCCEDED','FAILED']:
                                    form.mgData['tasks'][t]['completed'] = True
                                logger.debug(f"{this()}: task: {task.get('uuid')} {task.get('percentage_complete')}% '{task.get('progress_status')}' completed={form.mgData['tasks'][t]['completed']}")
                            elif version == 3:
                                if task.get('progress_message').upper() in ['SUCCEDED','FAILED']:
                                    form.mgData['tasks'][t]['completed'] = True
                                logger.debug(f"{this()}: task: {task.get('uuid')} {task.get('percentage_complete')}% '{task.get('progress_message')}' {task.get('status')} completed={form.mgData['tasks'][t]['completed']}")
                        else:
                            logger.warning(f"{this()}: task: {uuid} status = {response.status_code}")
                    else:
                        logger.error(f"{this()}: task: {uuid} ok     = {response.ok}")
                        logger.error(f"{this()}: task: {uuid} reason = {response.reason}")
                        logger.error(f"{this()}: task: {uuid} test   = {response.text}")
                else:
                    logger.error(f"{this()}: invalid response {response}")
            else:
                logger.debug(f"{this()}: task: {task.get('uuid')} {task.get('percentage_complete')}% {task.get('progress_status')} completed={task['completed']}")

    except Exception as e:
        emtec_handle_general_exception(e,logger=logger)                
    logger.debug(f"{this()}: OUT")

'''def forms_Migration_update_vms_slow(form):
    logger.debug(f"{this()}: IN")
    vm_protection  = {}
    found_clusters = 0
    found_pds      = 0
    found_vms      = 0
    found_rls      = 0
    # Build updated VM Protection Data
    logger.debug(f"{this()}: ***** Build updated VM Protection Data")
    for cluster_uuid in form.mgData.get('clusters_uuid'):
        cluster = form.mgData.get('clusters_uuid').get(cluster_uuid)
        if cluster.get('name') != "Prism Central":
            found_clusters += 1
            vm_protection.update({cluster_uuid:{}})
            logger.debug(f"{this()}: cluster: {cluster}")
            protocol = 'https'
            endpoint = 'api/nutanix/v2.0/protection_domains/'
            url      = f"{protocol}://{cluster.get('host')}:{cluster.get('port')}/{endpoint}"
            response = api_request(
                method         = 'GET',
                url            = url,
                headers        = {'Accept':'application/json'},
                data           = None,
                timeout        = 10,
                authentication = None,
                username       = cluster.get('username'),
                password       = cluster.get('password'),
                verify         = False,
                logger         = logger
                )
                
            logger.debug(f"{this()}: response: {response}")
            if response is not None:
                if response.ok:
                    data = response.json()
                    if response.status_code == 200:
                        logger.debug(f"{this()}: data.entities = {len(data['entities'])}")
                        for pd in data['entities']:
                            found_pds += 1
                            logger.debug(f"{this()}: pd name={pd.get('name')} active={pd.get('active')} vms ={len(pd.get('vms'))} replication links ={len(pd.get('replication_links'))}")
                            remote_site_name = None
                            last_replication = None
                            last_datetime    = None
                            for rl in pd.get('replication_links'):
                                found_rls += 1
                                remote_site_name = rl.get('remote_site_name')
                                last_replication = rl.get('last_replication_start_time_in_usecs')
                                last_datetime    = datetime.fromtimestamp(last_replication/1000000)
                                logger.debug(f"{this()}:   rl = {remote_site_name} {last_replication} {last_datetime}")
                            for vm in pd.get('vms'):
                                found_vms += 1
                                logger.debug(f"{this()}:   vm = {vm.get('vm_id')} {vm.get('vm_name')}")
                                # this structure is intented to ease future search
                                if rl.get('last_replication_start_time_in_usecs'):
                                    last_replication = rl.get('last_replication_start_time_in_usecs')
                                    last_datetime    = datetime.fromtimestamp(last_replication/1000000)
                                else:
                                    last_replication = None
                                    last_datetime    = None
                                
                                vm_protection[cluster_uuid].update({
                                    vm.get('vm_id'): {
                                        'vm_name'          : vm.get('vm_name'),
                                        'cluster_uuid'     : cluster_uuid,
                                        'cluster_name'     : cluster.get('name'),
                                        'pd_name'          : pd.get('name'),
                                        'pd_active'        : pd.get('active'),
                                        'pd_schedules'     : len(pd.get('cron_schedules',[])),
                                        'vms'              : len(pd.get('vms')),
                                        'replication_links': len(pd.get('replication_links')),
                                        'remote_site_name' : rl.get('remote_site_name'),
                                        'last_replication' : last_replication,
                                        'last_datetime'    : last_datetime,
                                    }
                                })
                    else:
                        logger.warning(f"{this()}: response status : {response}")                                            
                else:
                    logger.warning(f"{this()}: response not OK : {response}")                    
            else:
                logger.error(f"{this()}: Invalid response : {response}")                    
                
            logger.debug(f"{this()}: found vms     : {found_vms}")
        else:
            logger.debug(f"{this()}: Prism Central is ignored for PD search")
             
    logger.debug(f"{this()}: ***** found clusters: {found_clusters} pds: {found_pds} rls: {found_rls} vms: {found_vms}")
    # GV Updating data for Migration Group VMs
    logger.debug(f"{this()}: ***** Updating data for Migration Group {form.mgId}, {len(form.mgVms)} VMs")
    for vm in form.mgVms:
        # GV Get Protection domain details for VM
        for cluster_uuid in form.mgData.get('clusters_uuid'):
            cluster = form.mgData.get('clusters_uuid').get(cluster_uuid)
            if cluster.get('name') != "Prism Central":
                logger.debug(f"{this()}: search for vm : {vm.vm_name} {vm.MG_Id}:{vm.vm_uuid} in cluster {cluster_uuid}")
                detail = vm_protection.get(cluster_uuid).get(vm.vm_uuid,None)
                if detail:
                    break
        logger.debug(f"{this()}:   detail for {vm.vm_uuid} = {detail}")
        project = get_vm_project(form,vm.vm_uuid)
        if project:
            project_name = project.get('name')
        else:
            project_name = None
        if detail:
            pd_replicating = True if detail.get('remote_site_name') is not None else False
            logger.debug(f"{this()}: PD updates : vm_cluster_id       {detail.get('cluster_uuid')}")
            logger.debug(f"{this()}:              vm_has_pd           {True}")
            logger.debug(f"{this()}:              vm_pd_name          {detail.get('pd_name')}")
            logger.debug(f"{this()}:              vm_pd_is_active     {detail.get('pd_active')}")
            logger.debug(f"{this()}:              vm_pd_replicating   {pd_replicating}")
            logger.debug(f"{this()}:              vm_pd_schedules     {detail.get('pd_schedules')}")
            logger.debug(f"{this()}:              vm_last_replication {detail.get('last_datetime')}")
            logger.debug(f"{this()}:              vm_project          {project_name}")
            cluster = form.mgData.get('clusters_uuid').get(cluster_uuid)
            logger.debug(f"{this()}:               : CLUSTER             {cluster}")
            
            protocol = 'https'
            endpoint = f'PrismGateway/services/rest/v2.0/vms/{vm.vm_uuid}'
            url      = f"{protocol}://{cluster.get('host')}:{cluster.get('port')}/{endpoint}"
            response = api_request(
                method         = 'GET',
                url            = url,
                headers        = {'Accept':'application/json'},
                data           = None,
                timeout        = 10,
                authentication = None,
                username       = cluster.get('username'),
                password       = cluster.get('password'),
                verify         = False,
                logger         = logger
                )

            logger.debug(f"{this()}: response: {response}")
            if response is not None and response.ok:
                data = response.json()
                power_state = data.get('power_state')
                if str(power_state).upper() in ['ON','TRUE','SI','VERDADERO','T','V','S','1']:
                    vm.vm_state = True
                else:
                    vm.vm_state = False
                logger.debug(f"{this()}:              power_state = {vm.vm_state}")
            else:
                logger.warning(f"{this()}:            Couldn't get power_state for vm {vm.vm_name} {vm.MG_Id}:{vm.vm_uuid}")
            vm.vm_cluster_uuid     = detail.get('cluster_uuid')
            vm.vm_has_pd           = True
            vm.vm_pd_name          = detail.get('pd_name')
            vm.vm_pd_active        = detail.get('pd_active')
            vm.vm_pd_schedules     = detail.get('pd_schedules')
            vm.vm_pd_replicating   = pd_replicating
            vm.vm_last_replication = detail.get('last_datetime')
            vm.vm_project          = project_name
        else:
            logger.error(f"{this()}: no PD details for vm: {vm.vm_name} {vm.MG_Id}:{vm.vm_uuid}")
        # GV vm.vm_migrate is loaded from calling form
        # GV Actual VM update here ....
        try:
            logger.debug(f"{this()}: updating DB VM: {vm.vm_name} {vm.MG_Id}:{vm.vm_uuid} pwr:{vm.vm_state}")
            db.session.merge(vm)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            emtec_handle_general_exception(e,logger=logger)
    
    logger.debug(f"{this()}: OUT")
    return 
'''

def forms_Migration_update_vms(form):
    logger.debug(f"{this()}: IN")
    vm_protection  = {}
    found_clusters = 0
    found_pds      = 0
    found_vms      = 0
    found_rls      = 0
    # Build updated VM Protection Data
    logger.debug(f"{this()}: ***** Build updated VM Protection Data")
    formVms = []
    for vm in form.mgVms:
        formVms.append(vm.vm_uuid)
    for cluster_uuid in form.mgData.get('clusters_uuid'):
        cluster = form.mgData.get('clusters_uuid').get(cluster_uuid)
        if cluster.get('name') != "Prism Central":
            found_clusters += 1
            vm_protection.update({cluster_uuid:{}})
            logger.debug(f"{this()}: cluster: {cluster}")
            protocol = 'https'
            data = {'include_deleted':False}
            endpoint = 'api/nutanix/v2.0/protection_domains/'
            url      = f"{protocol}://{cluster.get('host')}:{cluster.get('port')}/{endpoint}"
            response = api_request(
                method         = 'GET',
                url            = url,
                headers        = {'Accept':'application/json'},
                data           = data,
                timeout        = 10,
                authentication = None,
                username       = cluster.get('username'),
                password       = cluster.get('password'),
                verify         = False,
                logger         = logger
                )
                
            logger.debug(f"{this()}: response: {response}")
            if response is not None:
                if response.ok:
                    data = response.json()
                    if response.status_code == 200:
                        logger.info(f"{this()}: protection domains found = {len(data['entities'])} in cluster {cluster.get('name')}")
                        for pd in data['entities']:
                            # Initialize temporary list for faster searches 
                            pd_vms               = pd.get('vms',[])
                            pd_replication_links = pd.get('replication_links',[])
                            # check if VM within PD's vms list
                            if (len(pd.get('vms'))):
                                logger.debug(f"{this()}: will look for {'|'.join(formVms)} in {len(pd.get('vms'))} vms")
                                
                                for vm_uuid in formVms:
                                    # GV 20220221 for i in range(len(pd.get('vms'))):
                                    for i in range(len(pd_vms)):
                                        if pd_vms[i]['vm_id'] == vm_uuid:
                                            logger.info(f"{this()}: found vm '{vm_uuid}' in pd '{pd.get('name')}'")
                                            found_pds += 1
                                            logger.debug(f"{this()}: pd name={pd.get('name')} active={pd.get('active')} vms ={len(pd.get('vms'))} replication links ={len(pd.get('replication_links'))}")
                                            remote_site_name = None
                                            last_replication = None
                                            last_datetime    = None
                                            # GV 20220221 for rl in pd.get('replication_links'):
                                            for rl in pd_replication_links:
                                                found_rls += 1
                                                remote_site_name = rl.get('remote_site_name')
                                                last_replication = rl.get('last_replication_start_time_in_usecs')
                                                last_datetime    = datetime.fromtimestamp(last_replication/1000000)
                                                logger.debug(f"{this()}:   rl = {remote_site_name} {last_replication} {last_datetime}")
                                            # GV 20220221 for vm in pd.get('vms'):
                                            for vm in pd_vms:
                                                found_vms += 1
                                                logger.debug(f"{this()}:   vm = {vm.get('vm_id')} {vm.get('vm_name')}")
                                                # this structure is intented to ease future search
                                                '''
                                                try:
                                                    if rl.get('last_replication_start_time_in_usecs'):
                                                        last_replication = rl.get('last_replication_start_time_in_usecs')
                                                        last_datetime    = datetime.fromtimestamp(last_replication/1000000)
                                                    else:
                                                        last_replication = None
                                                        last_datetime    = None
                                                except Exception as e:
                                                    logger.warning(f"exception: {str(e)}")
                                                    last_replication = None
                                                    last_datetime    = None
                                                '''
                                                vm_protection[cluster_uuid].update({
                                                    vm.get('vm_id'): {
                                                        'vm_name'          : vm.get('vm_name'),
                                                        'cluster_uuid'     : cluster_uuid,
                                                        'cluster_name'     : cluster.get('name'),
                                                        'pd_name'          : pd.get('name'),
                                                        'pd_active'        : pd.get('active'),
                                                        'pd_schedules'     : len(pd.get('cron_schedules',[])),
                                                        # GV 20220221 'vms'              : len(pd.get('vms',[])),
                                                        # GV 20220221 'replication_links': len(pd.get('replication_links'.[])),
                                                        'vms'              : len(pd_vms),
                                                        'replication_links': len(pd_replication_links),
                                                        'remote_site_name' : remote_site_name,
                                                        'last_replication' : last_replication,
                                                        'last_datetime'    : last_datetime,
                                                    }
                                                })
                                        else:
                                            pass            
                            else:
                                # discards any PD wit empty vms list
                                pass
                    else:
                        logger.warning(f"{this()}: response status : {response}")                                            
                else:
                    logger.warning(f"{this()}: response not OK : {response}")                    
            else:
                logger.error(f"{this()}: Invalid response : {response}")                    
                
            logger.debug(f"{this()}: found vms     : {found_vms}")
        else:
            logger.debug(f"{this()}: Prism Central is ignored for PD search")
             
    logger.info(f"{this()}: ***** found clusters: {found_clusters} pds: {found_pds} rls: {found_rls} vms: {found_vms}")
    # GV Updating data for Migration Group VMs
    logger.debug(f"{this()}: ***** Updating data for Migration Group {form.mgId}, {len(form.mgVms)} VMs")
    for vm in form.mgVms:
        detail = None
        project_name = None
        # GV Get Protection domain details for VM
        for cluster_uuid in form.mgData.get('clusters_uuid'):
            cluster = form.mgData.get('clusters_uuid').get(cluster_uuid)
            if cluster.get('name') != "Prism Central":
                logger.debug(f"{this()}: search for vm : {vm.vm_name} {vm.MG_Id}:{vm.vm_uuid} in cluster {cluster_uuid}")
                detail = vm_protection.get(cluster_uuid).get(vm.vm_uuid,None)
                if detail:
                    break
        logger.debug(f"{this()}:   detail for {vm.vm_uuid} = {detail}")
        project = get_vm_project(form,vm.vm_uuid)
        if project:
            project_name = project.get('name')
        if detail:
            pd_replicating = True if detail.get('remote_site_name') is not None else False
            logger.debug(f"{this()}: PD updates : vm_cluster_id       {detail.get('cluster_uuid')}")
            logger.debug(f"{this()}:              vm_has_pd           {True}")
            logger.debug(f"{this()}:              vm_pd_name          {detail.get('pd_name')}")
            logger.debug(f"{this()}:              vm_pd_is_active     {detail.get('pd_active')}")
            logger.debug(f"{this()}:              vm_pd_replicating   {pd_replicating}")
            logger.debug(f"{this()}:              vm_pd_schedules     {detail.get('pd_schedules')}")
            logger.debug(f"{this()}:              vm_last_replication {detail.get('last_datetime')}")
            logger.debug(f"{this()}:              vm_project          {project_name}")
            cluster = form.mgData.get('clusters_uuid').get(cluster_uuid)
            logger.debug(f"{this()}:               : CLUSTER             {cluster}")
            
            protocol = 'https'
            endpoint = f'PrismGateway/services/rest/v2.0/vms/{vm.vm_uuid}'
            url      = f"{protocol}://{cluster.get('host')}:{cluster.get('port')}/{endpoint}"
            response = api_request(
                method         = 'GET',
                url            = url,
                headers        = {'Accept':'application/json'},
                data           = None,
                timeout        = 10,
                authentication = None,
                username       = cluster.get('username'),
                password       = cluster.get('password'),
                verify         = False,
                logger         = logger
                )

            logger.debug(f"{this()}: response: {response}")
            if response is not None and response.ok:
                data = response.json()
                power_state = data.get('power_state')
                if str(power_state).upper() in ['ON','TRUE','SI','VERDADERO','T','V','S','1']:
                    vm.vm_state = True
                else:
                    vm.vm_state = False
                logger.debug(f"{this()}:              power_state = {vm.vm_state}")
            else:
                logger.warning(f"{this()}:            Couldn't get power_state for vm {vm.vm_name} {vm.MG_Id}:{vm.vm_uuid}")
            vm.vm_cluster_uuid     = detail.get('cluster_uuid')
            vm.vm_has_pd           = True
            vm.vm_pd_name          = detail.get('pd_name')
            vm.vm_pd_active        = detail.get('pd_active')
            vm.vm_pd_schedules     = detail.get('pd_schedules')
            vm.vm_pd_replicating   = pd_replicating
            vm.vm_last_replication = detail.get('last_datetime')
            vm.vm_project          = project_name
        else:
            logger.error(f"{this()}: no PD details for vm: {vm.vm_name} {vm.MG_Id}:{vm.vm_uuid}")
        # GV vm.vm_migrate is loaded from calling form
        # GV Actual VM update here ....
        try:
            logger.debug(f"{this()}: updating DB VM: {vm.vm_name} {vm.MG_Id}:{vm.vm_uuid} pwr:{vm.vm_state}")
            db.session.merge(vm)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            emtec_handle_general_exception(e,logger=logger)
    
    logger.debug(f"{this()}: OUT")
    return 

def forms_Migration_Validate(form):
    logger.info(f"{this()}: IN")
    infos    = []
    errors   = []
    warnings = []
    # Check Origin Cluster
    Origin    = gettext('unknown').capitalize()
    Destiny   = gettext('unknown').capitalize()
    if form.mgOrigin.data is None:
        errors.append(gettext('invalid origin cluster').capitalize())
    else:
        pass # check for valid cluster
        Origin = dict(form.mgOrigin.choices).get(form.mgOrigin.data)
    # Check Destiny Cluster
    if form.mgDestiny.data is None:
        errors.append(gettext('invalid Origin Cluster').capitalize())
    else:
        Destiny = dict(form.mgDestiny.choices).get(form.mgDestiny.data)
        # check for valid cluster
        if form.mgDestiny.data == form.mgOrigin.data:
            errors.append(gettext('destiny cluster should be different than origin cluster').capitalize())
    # VM Checks
    if form.mgVms:
        for vm in form.mgVms:
            if vm.vm_migrate:
                # Check for Origin cluster integrity
                if vm.vm_cluster_uuid != form.mgOrigin.data:
                    errors.append(gettext("vm '%s' is not active in cluster '%s'").capitalize()%(vm.vm_name,Origin))
                # Check for Power off
                if vm.vm_state:
                    errors.append(gettext("vm '%s' is powered on").capitalize()%(vm.vm_name))
                # Check for PD availabiliity
                if not vm.vm_has_pd:
                    errors.append(gettext("vm '%s' hasn't protection domain").capitalize()%(vm.vm_name))
                else:
                    if not vm.vm_pd_active:
                        errors.append(gettext("vm '%s' protection domain '%s' is not active").capitalize()%(vm.vm_name,vm_pd_name))
                    else:
                        pass
                # Check for Replication
                if not vm.vm_pd_replicating:
                    errors.append(gettext("pd '%s' is not replicating").capitalize()%(vm.vm_name))
                else:
                    if vm.vm_last_replication is None:
                        errors.append(gettext("vm '%s' hasn't remote replica").capitalize()%(vm.vm_name))
                    else:
                        elapsed = (datetime.now() - vm.vm_last_replication).seconds
                        if elapsed > 3600:
                            logger.warning(f"Migration of '{vm.vm_name}' may take more than usual since last replication was on {vm.vm_last_replication} ({elapsed:,.0f} seconds ago)")
                            warnings.append(gettext("Migration of '%s' may take more than usual since last replication was on %s (%s hours ago)"
                                ).capitalize()%(vm.vm_name,vm.vm_last_replication.strftime('%Y-%m-%d %H:%M:%S'),f"{elapsed/3600:,.1f}"))
                        else:
                            pass
                # Check for category
                project = get_vm_project(form,vm.vm_uuid)
                if project is None:
                    warnings.append(gettext("vm '%s' invalid project: '%s'")%(vm.vm_name,project))
                    logger.warning(f"{this()}: vm '{vm.vm_name}' invalid project: '{project}' {type(project)}")
                else:
                    logger.debug(f"{this()}: project={project}")
                    logger.debug(f"{this()}: current_app.config.get('NUTANIX_PROJECTS') = {current_app.config.get('NUTANIX_PROJECTS')}")
                    project_name = project.get('name').lower()
                    logger.debug(f"{this()}: project_name = {project_name}")
                    if project_name:
                        if current_app.config.get("NUTANIX_PROJECTS").get(project_name):
                            destiny_project = current_app.config.get("NUTANIX_PROJECTS").get(project_name).get(Destiny)
                            logger.info(f"{this()}: '{vm.vm_name}' project: '{project_name}' would be migrated to {Destiny}:{destiny_project}")
                        else:
                            logger.warning(f"{this()}: project_name '{project_name}' not in NUTANIX_PROJECTS.")                        
                    else:
                        logger.warning(f"{this()}: '{vm.vm_name}' project: '{project_name}' wouldn't be migrated.")                        
            else:
                infos.append(gettext("'%s' not selected for migration")%(vm.vm_name))
                logger.info(f"{this()}: '{vm.vm_name}' not selected for migration")
    else:
        errors.append(gettext('no virtual machines asociated to migration group').capitalize())
        logger.error(f"{this()}: No virtual machines asociated to migration group")
    if len(infos):
        Infos = ""
        for info in infos:
            logger.info(info)
            Infos += f"<li>{info}</li>"
        flash(Markup(f"<ul>{Infos}</ul>"),"info")
    if len(warnings):
        Warnings = ""
        for warning in warnings:
            logger.warning(warning)
            Warnings += f"<li>{warning}</li>"
        flash(Markup(f"<ul>{Warnings}</ul>"),"warning")
    if len(errors):
        Errors = ""
        for error in errors:
            logger.error(error)
            Errors += f"<li>{error}</li>"
        flash(Markup(f"<ul>{Errors}</ul><br>"),"error")
    
    if len(warnings):
        flash(gettext("Detected %s warning(s). Migration can continue at your discretion")%(len(warnings)),"warning")
        form.mgData['can_migrate'] = True
    if len(errors):
        flash(gettext("Detected %s error(s). Migration can not continue. Please fix it/them and try again")%(len(errors)),"error")
        form.mgData['can_migrate'] = False
    
    logger.info(f"{this()}: OUT (Id:{form.mgId},err:{len(errors)},war:{len(warnings)})")
    return form.mgId,errors,warnings

def forms_Migration_migrate_vm(form,vm):
    logger.debug(f"{this()}: IN")
    task = None
    try:
        Origin  = dict(form.mgOrigin.choices).get(form.mgOrigin.data)
        Destiny = dict(form.mgDestiny.choices).get(form.mgDestiny.data)
        logger.info(f"{this()}: Migrating {Origin}:{vm.vm_name}")
        logger.info(f"{this()}: Origin  : {form.mgOrigin.data} {Origin}")
        logger.info(f"{this()}: Destiny : {form.mgDestiny.data} {Destiny}")
        cluster = form.mgData.get('clusters_uuid').get(form.mgOrigin.data)
        prism_central = form.mgData.get('clusters_uuid').get('prism_central')
        poll_tasks(form,prism_central,3)
        if vm.vm_has_pd and vm.vm_pd_name is not None:
            protocol = 'https'
            endpoint = f'PrismGateway/services/rest/v2.0/protection_domains/{vm.vm_pd_name}/migrate'
            url      = f"{protocol}://{cluster.get('host')}:{cluster.get('port')}/{endpoint}"
            logger.debug(f"{this()}: url: {url}")
            response = None
            # Forzado a no ejecutarse por ahora
            if not current_app.config.get('BUTLER_TEST_ONLY_MODE'):
                protocol = 'https'
                url      = f"{protocol}://{cluster.get('host')}:{cluster.get('port')}/{endpoint}"
                response = api_request(
                    method         = 'POST',
                    url            = url,
                    headers        = {'Content-Type': 'application/json'},
                    data           = json.dumps({'value':Destiny}),
                    timeout        = 10,
                    authentication = None,
                    username       = cluster.get('username'),
                    password       = cluster.get('password'),
                    verify         = False,
                    logger         = logger
                    )
                
                logger.debug(f"{this()}: response: {response}")
                if response is not None:
                    data = response.json()
                    logger.debug(f"{this()}: response data: {data}")
                    if response.ok:
                        if response.status_code in  [200,201]:
                            task_uuid = f"task_for_{vm.vm_name}"
                            task = {
                                'uuid': task_uuid,
                                'vm'  : vm,
                            }
                        else:
                            logger.warning(f"{this()}: response status = {response}")
                    else:
                        logger.error(f"{this()}: response not ok  = {response}")
                        logger.error(f"{this()}: response.reason  = {response.reason}")
                        logger.error(f"{this()}: response.text  = {response.text}")
                else:
                    logger.error(f"{this()}: response invalid = {response}")
            else:
                logger.info(f"{this()}: WARNING BUTLER_TEST_ONLY_MODE no actual execution. fake task loaded.")
                task_uuid = f"fake_task_for_{vm.vm_name}"
                task = {
                    'uuid': task_uuid,
                    'vm'  : vm,
                }
        else:
            logger.error(f"{this()}: '{vm.vm_name}' does not have a valid protection domain")
    except Exception as e:
        emtec_handle_general_exception(e,logger=logger)
    logger.debug(f"{this()}: OUT task = {task}")
    return task

def forms_Migration_create_schedules(form,pd_name):
    # All migration validations upon Destiny Cluster
    destiny_cluster = form.mgData.get('clusters_uuid').get(form.mgDestiny.data)
    origin_cluster  = form.mgData.get('clusters_uuid').get(form.mgOrigin.data)
    logger.info(f"{this()}: {pd_name}@{destiny_cluster.get('name')} -> {origin_cluster.get('name')}")
    remote_created = True
    local_created  = True
    if current_app.config.get('NUTANIX_MIGRATION_CREATE_REMOTE_SCHEDULES'):
        logger.info(f"{this()}: Remote CRON schedules creation requested in {destiny_cluster.get('name')}")
        schedule_type       = current_app.config.get('NUTANIX_REMOTE_SCHEDULE_TYPE')
        schedule_every_nth  = current_app.config.get('NUTANIX_REMOTE_EVERY_NTH')
        schedule_local_max  = current_app.config.get('NUTANIX_REMOTE_LOCAL_MAX_SNAPSHOTS')
        schedule_remote_max = current_app.config.get('NUTANIX_REMOTE_REMOTE_MAX_SNAPSHOTS')
        # Actual 'REMOTE' schedules creation here
        logger.info(f"{this()}: type: {schedule_type} every nth: {schedule_every_nth} local snps: {schedule_local_max} remote snps: {schedule_remote_max}")
        logger.info(f"{this()}: creating cron in cluster {destiny_cluster.get('name')} remote {origin_cluster.get('name')}")
        if not current_app.config.get('BUTLER_TEST_ONLY_MODE'):
            remote_created = create_pd_schedule(
                    current_app,
                    host                     = destiny_cluster.get('host'),
                    port                     = destiny_cluster.get('port'),
                    username                 = destiny_cluster.get('username'),
                    password                 = destiny_cluster.get('password'),
                    protocol                 = 'https',
                    pdname                   = pd_name,
                    remote_cluster           = origin_cluster.get('name'),
                    schedule_type            = schedule_type,
                    every_nth                = schedule_every_nth,
                    local_max_snapshots      = schedule_local_max,
                    remote_max_snapshots     = schedule_remote_max,
                )
        else:
            logger.info(f"{this()}: WARNING BUTLER TEST ONLY MODE will not create REMOTE schedule on {destiny_cluster.get('name')}")
        if remote_created:
            logger.info(f"{this()}: Remote CRON Schedule created")
        else:
            logger.info(f"{this()}: Remote CRON Schedule not created")
    else:
        logger.info(f"{this()}: Remote CRON schedules creation not requested in {destiny_cluster.get('name')}")
    if current_app.config.get('NUTANIX_MIGRATION_CREATE_LOCAL_SCHEDULES'):
        logger.info(f"{this()}: Local CRON schedules creation requested in {destiny_cluster.get('name')}")
        schedule_type       = current_app.config.get('NUTANIX_LOCAL_SCHEDULE_TYPE')
        schedule_every_nth  = current_app.config.get('NUTANIX_LOCAL_EVERY_NTH')
        schedule_local_max  = current_app.config.get('NUTANIX_LOCAL_LOCAL_MAX_SNAPSHOTS')
        schedule_remote_max = current_app.config.get('NUTANIX_LOCAL_REMOTE_MAX_SNAPSHOTS')
        # Actual 'LOCAL' schedules creation here
        logger.info(f"{this()}: type: {schedule_type} every nth: {schedule_every_nth} local snps: {schedule_local_max} remote snps: {schedule_remote_max}")
        logger.info(f"{this()}: creating cron in cluster {destiny_cluster.get('name')} remote {origin_cluster.get('name')}")
        if not current_app.config.get('BUTLER_TEST_ONLY_MODE'):
            local_created = create_pd_schedule(
                    current_app,
                    host                     = destiny_cluster.get('host'),
                    port                     = destiny_cluster.get('port'),
                    username                 = destiny_cluster.get('username'),
                    password                 = destiny_cluster.get('password'),
                    protocol                 = 'https',
                    pdname                   = pd_name,
                    remote_cluster           = origin_cluster.get('name'),
                    schedule_type            = schedule_type,
                    every_nth                = schedule_every_nth,
                    local_max_snapshots      = schedule_local_max,
                    remote_max_snapshots     = schedule_remote_max,
                )
        else:
            logger.info(f"{this()}: WARNING BUTLER TEST ONLY MODE wont create LOCAL schedule on {destiny_cluster.get('name')}")
        if local_created:
            logger.info(f"{this()}: Local CRON Schedule created")
        else:
            logger.info(f"{this()}: Local CRON Schedule not created")
    else:
        logger.info(f"{this()}: Local CRON schedules creation not requested in {destiny_cluster.get('name')}")
    created = remote_created and local_created
    logger.info(f"{this()}: remote={remote_created} and local={local_created} returns {created}")
    return created

def forms_Migration_validate_remote_vm(form,vm,count):
    logger.info(f"{this()}: IN feedback count = {count}")
    vmMigrationComplete = True
    vmMigrationWarnings = []
    count += 1
    form.mgData['ipc']['last_shown'] = send_feedback(form,count,gettext("Validating VM: '%s'")%(vm.vm_name))
    vm_ok   = False
    pr_ok   = False
    pd_ok   = False
    pdvm_ok = False
    cs_ok   = False
    try:
        Origin  = dict(form.mgOrigin.choices).get(form.mgOrigin.data)
        Destiny = dict(form.mgDestiny.choices).get(form.mgDestiny.data)
        logger.info (f"{this()}: Validating {vm.vm_name}@{Destiny}'")
        logger.debug(f"{this()}: Origin  : {form.mgOrigin.data} {Origin}")
        logger.debug(f"{this()}: Destiny : {form.mgDestiny.data} {Destiny}")
        # All migration validations upon Destiny Cluster
        cluster         = form.mgData.get('clusters_uuid').get(form.mgDestiny.data)
        remote_cluster  = form.mgData.get('clusters_uuid').get(form.mgOrigin.data)
        prism_central   = form.mgData.get('clusters_uuid').get('prism_central')
        protocol = 'https'
        endpoint = f"PrismGateway/services/rest/v2.0/vms/{vm.vm_uuid}?include_vm_disk_config=false&include_vm_nic_config=false"
        url      = f"{protocol}://{cluster.get('host')}:{cluster.get('port')}/{endpoint}"
        response = api_request(
            method         = 'GET',
            url            = url,
            headers        = {'Content-Type': 'application/json'},
            data           = None,
            timeout        = 10,
            authentication = None,
            username       = cluster.get('username'),
            password       = cluster.get('password'),
            verify         = False,
            logger         = logger
            )

        logger.debug(f"{this()}: response: {response}")
        if response is not None:
            data = response.json()
            if response.ok:
                if response.status_code == 200:
                    if data.get('name') == vm.vm_name and data.get('uuid') == vm.vm_uuid:
                        logger.info(f"{this()}: VM Validation: vm name/uuid success !!!")
                        # Prism Central project Update -----------------
                        logger.info(f"{this()}: VM Validation: will procded to update project")
                        # get VM data from Prism Central
                        
                        vm_ok=True
                        endpoint = f"api/nutanix/v3/vms/{vm.vm_uuid}"
                        url      = f"{protocol}://{prism_central.get('host')}:{prism_central.get('port')}/{endpoint}"
                        response = api_request(
                            method         = 'GET',
                            url            = url,
                            headers        = {'Content-Type': 'application/json'},
                            data           = None,
                            timeout        = 10,
                            authentication = None,
                            username       = cluster.get('username'),
                            password       = cluster.get('password'),
                            verify         = False,
                            logger         = logger
                            )

                        logger.debug(f"{this()}: response: {response}")
                        if response is not None:
                            vm_data = response.json()
                            logger.debug(f"{this()}: GOT VM DATA FROM PC WILL PROCEED TO UPDATE PROJECT")
                            logger.debug(f"{this()}: nutanix projects  : {current_app.config.get('NUTANIX_PROJECTS')}")
                            logger.debug(f"{this()}: old vm.vm_project : {vm.vm_project} to {Destiny}")
                            name    = current_app.config.get('NUTANIX_PROJECTS').get(vm.vm_project.lower()).get(Destiny)
                            if name:
                                if form.mgData.get('projects_list').get(name):
                                    uuid = form.mgData.get('projects_list').get(name).get('uuid')
                                else:
                                    uuid = None
                            else:
                                name = None
                                uuid = None
                            logger.debug(f"{this()}: new project uuid  : {uuid}")
                            logger.debug(f"{this()}: vm_data           : {vm_data}")
                            if name and uuid:
                                logger.info(f"{this()}: Project update {vm.vm_project}@{Origin} --> {name}@{Destiny} {uuid}")
                                # update project fields only all other remain untouched
                                vm_data['metadata']['project_reference']['name']=name
                                vm_data['metadata']['project_reference']['uuid']=uuid
                                data     = json.dumps({
                                              "spec"    : vm_data.get('spec'),
                                              "metadata": vm_data.get('metadata'),
                                            })

                                logger.debug(f"{this()}: request data: {data}")
                                response = api_request(
                                    method         = 'PUT',
                                    url            = url,
                                    headers  = {'Content-Type': 'application/json','Accept': 'application/json'},
                                    data           = data,
                                    timeout        = 10,
                                    authentication = None,
                                    username       = cluster.get('username'),
                                    password       = cluster.get('password'),
                                    verify         = False,
                                    logger         = logger
                                    )
                                
                                logger.debug(f"{this()}: response: {response}")
                                if response is not None:
                                    data = response.json()
                                    logger.debug(f"{this()}: response data = {data}")
                                    if response.ok:
                                        if response.status_code in [200,201,202]:
                                            logger.info(f"{this()}: VM Validation: project update task sent OK ({data.get('status').get('execution_context').get('task_uuid')})")
                                            form.mgData['tasks'].append({
                                                'uuid'      : data.get('status').get('execution_context').get('task_uuid'),
                                                'completed' : False
                                            })
                                            pr_ok=True
                                            # Check tasks in prism central
                                            poll_tasks(form,prism_central,3)
                                        else:
                                            logger.warning(f"{this()}: VM Validation: project PUT response status = {response}")
                                            logger.warning(f"{this()}: VM Validation: project PUT response status = {dir(response)}")
                                    else:
                                        logger.warning(f"{this()}: VM Validation: project PUT response not ok={response}")
                                        logger.warning(f"{this()}: VM Validation: project PUT response status: {response.status_code} state: {data.get('state')} errors: {data.get('message_list')}")
                                        vmMigrationWarnings.append(gettext("update project warning: response: %s %s %s %s").capitalize()%(
                                            response,
                                            response.status_code,
                                            data.get('code'),
                                            data.get('message')
                                            )
                                        )
                                else:
                                    logger.warning(f"{this()}: VM Validation: response={response}")
                                    vmMigrationWarnings.append(gettext("update project warning: response: %s").capitalize()%(
                                            response
                                            )
                                    )
                            else:
                                logger.warning(f"{this()}: Couldn't update project: {name}:{uuid}")
                                vmMigrationComplete=False
                        else:
                            logger.warning(f"{this()}: VM Validation: not found in Prism central !!!")
                            vmMigrationComplete=False
                    else:
                        logger.error(f"{this()}: VM Validation: vm name/uuid error")
                        vmMigrationComplete=False
                else:
                    logger.warning(f"{this()}: VM Validation: response status = {response}")
                    logger.warning(f"{this()}: VM Validation: response status = {dir(response)}")
            else:
                if response.status_code == 500:
                    if data.get('error_code').get('code') == 1202:
                        logger.info(f"{this()}: {vm.vm_name}@{Destiny} does not exist")
                    else:
                        logger.warning(f"{this()}: VM Validation: response not ok={response}")
                        logger.warning(f"{this()}: VM Validation: response status: {response.status_code} error: {data.get('error_code').get('code')} {data.get('message')}")
                else:
                    logger.warning(f"{this()}: VM Validation: response not ok={response}")
                    logger.warning(f"{this()}: VM Validation: response status: {response.status_code} error: {data.get('error_code').get('code')} {data.get('message')}")
                vmMigrationComplete=False
        else:
            logger.warning(f"{this()}: VM Validation: response={response}")
            vmMigrationComplete=False
        count += 1
        form.mgData['ipc']['last_shown'] = send_feedback(form,count,gettext("Validating PD: '%s'")%(vm.vm_pd_name))

        # GV Validate PD active in Destiny
        logger.info(f"{this()}: Validating PD {vm.vm_pd_name}@{Destiny}")
        protocol = 'https'
        endpoint = f"/PrismGateway/services/rest/v2.0/protection_domains/{vm.vm_pd_name}"
        url      = f"{protocol}://{cluster.get('host')}:{cluster.get('port')}/{endpoint}"
        response = api_request(
            method         = 'GET',
            url            = url,
            headers        = {'Accept': 'application/json'},
            data           = None,
            timeout        = 10,
            authentication = None,
            username       = cluster.get('username'),
            password       = cluster.get('password'),
            verify         = False,
            logger         = logger
            )

        logger.debug(f"{this()}: response: {response}")
        # look for name = vm.vm_pd_name, in vms[] look for vm_name=vm.vm_name (o vm.vm_pd_name), active = true
        # validate schedule in destiny
        # look for cron_schedules if missing will try to create them
        if response is not None:
            if response.ok:
                data = response.json()
                if response.status_code == 200:
                    if data.get('name') == vm.vm_pd_name:                    
                        logger.info(f"{this()}: PD Validation: pd name/uuid success !!!")
                        pd_ok=True
                        # GV Will check for PD active in Destiny cluster
                        if data.get('active'):
                            logger.info(f"{this()}: PD Validation: pd {vm.vm_name}@{Destiny} is active")
                        else:
                            logger.info(f"{this()}: PD Validation: {vm.vm_name}@{Destiny} is not active")
                            vmMigrationComplete=False

                        # Will check for VM in PD'd vms list 
                        vfound = False
                        
                        logger.debug(f"{this()}: data.get('vms')= {type(data.get('vms'))} {data.get('vms')}")
                        
                        for v in data.get('vms'):
                            logger.debug(f"{this()}: looking for vm '{v.get('vm_name')}' {v.get('vm_id')} in pd '{vm.vm_pd_name}'")
                            if v.get('vm_name') == vm.vm_name and v.get('vm_id')==vm.vm_uuid:
                                vfound = True
                                break
                        if vfound:
                            logger.info(f"{this()}: PD Validation: vm name/uuid found in PD's vms list !!!")
                            pdvm_ok=True
                        else:
                            logger.error(f"{this()}: PD Validation: vm name/uuid error: VM '{vm.vm_name}' not found in PD '{vm.vm_pd_name}'")
                            vmMigrationComplete=False                            
                            
                        # Will check for any CRON Schedules in Destiny cluster
                        if data.get('cron_schedules'):
                            if len(data.get('cron_schedules')):
                                logger.info(f"{this()}: PD Validation: PD schedule list has {len(data.get('cron_schedules'))} schedules")
                                cs_ok=True
                            else:
                                logger.warning(f"{this()}: PD Validation: PD schedule list is empty. Will create schedules if required.")
                                created = forms_Migration_create_schedules(form,vm.vm_pd_name)
                                cs_ok=created
                                logger.info(f"{this()}: required schedules created = {created}")
                                vmMigrationComplete = vmMigrationComplete and created
                        else:
                            logger.info(f"{this()}: PD Validation: PD schedule list not found. Will create schedules if required.")
                            created = forms_Migration_create_schedules(form,vm.vm_pd_name)
                            cs_ok=created
                            logger.info(f"{this()}: required schedules created = {created}")
                            vmMigrationComplete = vmMigrationComplete and created
                    else:
                        logger.warning(f"{this()}: PD Validation: PD name does not match. failure.")
                        vmMigrationComplete=False
                else:
                    logger.warning(f"{this()}: PD Validation: response status = {response}")
                    vmMigrationComplete=False
            else:
                logger.warning(f"{this()}: PD Validation: response not ok={response}")
                logger.warning(f"{this()}: PD Validation: response status: {response.status_code} error: {data.get('error_code').get('code')} {data.get('message')}")
                vmMigrationComplete=False                
        else:
            logger.warning(f"{this()}: PD Validation: response={response}")
            vmMigrationComplete=False

    except Exception as e:
        emtec_handle_general_exception(e,logger=logger)    
    logger.info(f"{this()}: vm:{vm_ok} pr:{pr_ok} pd:{pd_ok} pdvm:{pdvm_ok} cs:{cs_ok} complete:{vm_ok and pr_ok and pd_ok and pdvm_ok and cs_ok}")
    logger.info(f"{this()}: OUT {vm.vm_name} migration complete? {vmMigrationComplete}")
    count+=1
    status = " (vm:%s pr:%s pd:%s pdvm:%s cs:%s)"%(
            'OK' if vm_ok   else '?',
            'OK' if pr_ok   else '?',
            'OK' if pd_ok   else '?',
            'OK' if pdvm_ok else '?',
            'OK' if cs_ok   else '?'
            )
    logger.info(f"{this()}: OUT status ={status}")
    form.mgData['ipc']['last_shown'] = send_feedback(form,count,gettext("Migration validation of '%s' complete")%(vm.vm_name)+status)
    return vmMigrationComplete
    
def forms_Migration_Migrate(form):
    logger.info(f"{this()}: IN")
    form.MgId,errors,warnings = forms_Migration_Validate(form)
    
    tasks = []
    
    if len(errors) == 0 or current_app.config.get('BUTLER_TEST_ONLY_MODE'):
        if len(errors):
            flash(gettext("will execute with %s errors. DEVELOPMENT MODE ONLY").capitalize()%(
                len(errors)),"error")
        if len(warnings):
            flash(gettext("will execute with %s warnings.").capitalize()%(
                len(warnings)),"warning")            
            logger.warning(f"{this()}: Validation reports {len(warnings)} warnings")
        #GV flash(gettext('Migration execution starts'),"message")
        logger.info(f"{this()}: Starts Migration execution ...")
        for vm in form.mgVms:
            if vm.vm_migrate:
                task = forms_Migration_migrate_vm(form,vm)
                if task is not None:
                    tasks.append(task)
            else:
                logger.info(f"{this()}: '{vm.vm_name}' excluded from migration")
    else:
        logger.error  (f"{this()}: Validation reports {len(errors)} errors")
        logger.warning(f"{this()}: Validation reports {len(warnings)} warnings")
        logger.warning(f"{this()}: Migration execution can not proceed")
        flash(gettext("Migration execution can not proceed due to validation errors"),"error")
        
    logger.info(f"{this()}: tasks = {len(tasks)}")
    logger.info(f"{this()}: OUT form.mgId = {form.mgId}")
    return form.mgId,tasks

def forms_Migration_populate_lists(form):
    logger.debug(f"{this()}: IN")
    cluster_options = []
    clusters_uuid   = {}
    vm_list         = {}
    vms_uuid        = {}
    try:
        logger.info(f"{this()}: Getting Prism Central from Nutanix. Upon Butler Configuration: {current_app.config.get('NUTANIX_HOST')}")
        clusters_uuid.update({
            'prism_central':{
                'name'    : 'Prism Central',
                'host'    : current_app.config.get('NUTANIX_HOST'),
                'port'    : current_app.config.get('NUTANIX_PORT'),
                'username': current_app.config.get('NUTANIX_USERNAME'),
                'password': current_app.config.get('NUTANIX_PASSWORD'),
                }
            })
        logger.info(f"{this()}: Getting clusters from Nutanix. Upon Butler Configuration: {','.join( list(current_app.config.get('NUTANIX_CLUSTERS').keys())) }")
        for cluster_name in current_app.config.get('NUTANIX_CLUSTERS'):
            logger.debug(f"{this()}: cluster_name={cluster_name}")
            cluster          = current_app.config.get('NUTANIX_CLUSTERS').get(cluster_name)
            cluster_uuid     = cluster.get('uuid')
            cluster_options.append(
                (cluster_uuid,cluster_name)
            )
            clusters_uuid.update({
                cluster_uuid:{
                    'name'    :cluster_name,
                    'host'    :cluster.get('host'),
                    'port'    :cluster.get('port'),
                    'username':cluster.get('username'),
                    'password':cluster.get('password'),
                    }
                })
            vm_list.update({cluster_uuid:{'name':cluster_name,'vms':{}}})
            vm_list[cluster_uuid]['vms'] = {}
            try:
                logger.debug(f"{this()}: Getting VM list from {cluster_name} @ {cluster.get('host')}")
                response = nutanix_get_vm_list(
                    host     = cluster.get('host'),
                    username = cluster.get('username'),
                    password = cluster.get('password'),
                    logger   = logger
                    )
                if response and response.ok:
                    for vm in response.json().get('entities'):
                        vm_list[cluster_uuid]['vms'].update({
                            vm.get('name'):{
                                'uuid'       :vm.get('uuid'),
                                'power_state':vm.get('power_state'),
                                }
                        })
                    logger.debug(f"{this()}: len vm_list[{cluster_uuid}]['vms'] = {len(vm_list[cluster_uuid]['vms'])}")
                else:
                    logger.error(f"{this()}: Invalid response {response} no vms found in {cluster_name} @ {cluster.get('host')}")
                    flash(gettext("Invalid response '%s' no vms found in %s @ %s"%(
                        response,cluster_name,cluster.get('host'))),"error")
                    return None
            except Exception as e:
                emtec_handle_general_exception(e,logger=logger)
                flash(f"{this()}: {gettext('exception')}: {str(e)}","error")
                return None
        logger.debug(f"{this()}: clusters_uuid = {clusters_uuid}")
    except Exception as e:
            emtec_handle_general_exception(e,logger=logger)
            flash(f"{this()}: {gettext('exception')}: {str(e)}","error")
            return None
    logger.debug(f"{this()}: OUT")
    return  {
                'cluster_options':cluster_options,
                'clusters_uuid'  :clusters_uuid,
                'vm_list'        :vm_list,
                'vms_uuid'       :vms_uuid
            }

def send_feedback(form,count,message):
    form.mgData['ipc'].update({'value':count,'message':message})
    last_shown = display_advance(**form.mgData['ipc'])
    time.sleep(1.5) # gv This is required to be sure all feedback is captured by interface
    return last_shown

def forms_Migration_Feedback(form,tasks):
    if current_app.config.get('BUTLER_TEST_ONLY_MODE'):
        timeout   = 20       # SHOULD BE CONFIGURABLE OR CALCULATED UPON NUMBER OF TASKS
        step      = 5
    else:
        timeout   = current_app.config.get('NUTANIX_MIGRATION_TIMEOUT')
        step      = current_app.config.get('NUTANIX_MIGRATION_VALIDATION_STEP')
    completed = False
    message = gettext("process timeout=%.0f seconds, idle step=%.0f seconds, max iterations=%.0f"
                        ).capitalize()%(timeout,step,timeout/step)
    logger.info(f"{this()}: {message}")
    # Feedback Initialize    
    num_subtasks = 4 # This is the number of validation sub-steps

    form.mgData['ipc'].update({
        'value'      : 0,
        'maximum'    : len(tasks)*num_subtasks+num_subtasks+5,
        'last_shown' : 0,
        'step'       : 0.01,
        'start'      : datetime.now(),
        'logger'     : logger,
        'message'    : message,
        'fmt'        : 'json',
        })
    # GV Send first message with initialization data
    logger.debug(f"{this()}: form.mgData['ipc']={form.mgData['ipc']}")
    form.mgData['ipc']['last_shown'] = send_feedback(form,1,message)
    count = 0
    validation_iteration = 0
    while not completed and timeout>0:
        validation_iteration += 1
        completed_text = gettext('yes').capitalize if completed else gettext('no').capitalize()
        message = gettext("validation iteration %s starts. %s idle seconds to go, waiting %s seconds, %s validation tasks to go").capitalize()%(
            validation_iteration,
            timeout,
            step,
            len(tasks)
        )
        logger.info(f"{this()}: {message}")
        # GV reesets fedback counter to 1
        count = 2
        form.mgData['ipc']['last_shown'] = send_feedback(form,count,message)
        time.sleep(step)
        timeout -= step
        # GV completad means all VMs completed, any false will uncomplete loop
        completed = True
        task_counter = 0
        for task in tasks:
            # feedback counter reset to: 0=2, 1=6, 2=10, ...
            count = task_counter * num_subtasks + 3
            logger.info(f"{this()}: Validation task = '{task.get('uuid')}'")
            if task:
                vm = task.get('vm')
                if vm:
                    if forms_Migration_validate_remote_vm(form,vm,count):
                        message = gettext("%s@%s validated OK")%(vm.vm_name,dict(form.mgDestiny.choices).get(form.mgDestiny.data))
                        logger.info(f"{this()}: {message}")
                    else:
                        message = gettext("%s@%s migration not successful yet")%(vm.vm_name,dict(form.mgDestiny.choices).get(form.mgDestiny.data))
                        logger.info(f"{this()}: {message}")
                        completed = False
                else:
                    message = gettext("invalid vm: '%s'").capitalize()%(vm)
                    logger.error(f"{this()}: {message}")
                    completed = False
            else:
                message = gettext("invalid task: %s").capitalize()%(task)
                logger.info(f"{this()}: {message}")
                completed = False
            # GV feedback counter reset to 0=7, 1=11
            count = task_counter * num_subtasks + 3 + num_subtasks
            form.mgData['ipc']['last_shown'] = send_feedback(form,count,message)
            task_counter += 1
        
        prism_central = form.mgData.get('clusters_uuid').get('prism_central')
        logger.info(f"{this()}: iteration  final 'poll_tasks({prism_central.get('name')})' call ...")

        poll_tasks(form,prism_central,3)
        
        completed_text = gettext('yes') if completed else gettext('no')
        logger.info(f"{this()}: completed = {completed}")
        message = "%s %s, %s = '%s'"%(
                gettext('validation iteration').capitalize(),
                validation_iteration,
                gettext('completed'),
                completed_text.capitalize()
                )
        #message = gettext('validation iteration').capitalize()  %s, {gettext('completed')} = '%s'"%(validation_iteration,completed_text)
        form.mgData['ipc']['last_shown'] = send_feedback(form,form.mgData['ipc']['maximum']-1,message)
        if completed:
            break            
    # Ver aqui si se puede poner un Modal que espere y muestre avance?????
    # logger.info(f"{this()}: redirecting to '.forms_Migration' with Id = {form.mgId}")
    # logger.info(f"{this()}: **************************")
    logger.info(f"{this()}: returns completed = {completed}")
    message = gettext("final migration status completed = %s").capitalize()%(completed_text)
    form.mgData['ipc']['last_shown'] = send_feedback(form,form.mgData['ipc']['maximum'],message)
    return completed #,feedback

# GV Feedback buffer/cache area
FEEDBACK = {}

# GV ROUTES
@main.route('/read-progress',methods=['GET'])
def read_progress():
    ''' Reads progress data from cache file in file system 
        and returns it as a JSON string
    '''
    global FEEDBACK
    ipc_mode          = request.args.get('ipc_mode'    , None)
    ipc_id            = request.args.get('ipc_id'      , None)
    logger.trace(f"{this()}: IPC mode:{ipc_mode} id:{ipc_id} FEEDBACK = {FEEDBACK}")  

    temp_dir = tempfile.gettempdir()   
    error = False 
    if   ipc_mode == 'filesystem':
        progress_filename = f"{temp_dir}/{ipc_id}"  
    elif ipc_mode == 'fifo':
        progress_fifo     = f"{temp_dir}/{ipc_id}"  
    elif ipc_mode == 'queue':
        progress_queue    = FEEDBACK.get(ipc_id,None)
        if progress_queue is not None:
            logger.trace(f"{this()}: IPC mode:{ipc_mode} id:{ipc_id} queue:{progress_queue} size={progress_queue.qsize()} FEEDBACK = {FEEDBACK}")  
        else:
            logger.error(f"{this()}: IPC mode:{ipc_mode} id:{ipc_id} queue:{progress_queue} size=None FEEDBACK = {FEEDBACK} url={request.url}")              
            error = True
    else:
        logger.error(f"{this()}: IPC invalid mode:{ipc_mode} id:{ipc_id} FEEDBACK = {FEEDBACK}")  
        error = True
    data={}
    if not error:
        if   ipc_mode == 'filesystem':
            try:
                logger.trace(f"{this()}: will read file: '{progress_filename}' ...")
                with open(progress_filename,'r') as fp:
                    read_bytes = fp.read(1024*1024)
                    logger.trace(f"{this()}: read bytes = {len(read_bytes)} bytes")
                    data = json.loads(read_bytes.encode())
            except FileNotFoundError:
                logger.trace(f"{this()}: File '{progress_filename}' does not exist.")
            except Exception as e:
                emtec_handle_general_exception(e,logger=logger)
                data={}
            finally:
                # GV anyway remove temporary file
                try:
                    if os.path.exists(progress_filename):
                        os.remove(progress_filename)
                except:
                    pass
        elif ipc_mode == 'fifo':
            try:
                logger.warning(f"{this()}: will read fifo: '{progress_fifo}' ...")
                ffh = os.open(progress_fifo,os.O_RDONLY|os.O_NONBLOCK)
                if ffh:
                    read_bytes = os.read(ffh,1024*1024)
                    logger.warning(f"{this()}: read bytes = {len(read_bytes)} bytes")
                    if len(read_bytes) == 0:
                        data={} # GV data will be empty 
                    else:
                        lines=read_bytes.encode().split('\n')
                        logger.warning(f"{this()}: lines = {len(lines)}")
                        for line in lines:
                            data = json.loads(line) # GV data will have last line read only
                    os.close(ffh)
                    logger.warning(f"{this()}: fifo fh {ffh} closed.")
            except Exception as e:
                emtec_handle_general_exception(e,logger=logger)
                data={}        
        elif ipc_mode == 'queue':
            if progress_queue:
                logger.trace(f"{this()}: will read queue: '{ipc_id}' ... {progress_queue} qsize={progress_queue.qsize()}")
                try:
                    #data = progress_queue.get(block=False,timeout=1)
                    data = progress_queue.get(block=False)
                    progress_queue.task_done()
                except Empty:
                    logger.trace(f"{this()}: empty queue {ipc_id}.")
                    data={}
                except Exception as e:
                    emtec_handle_general_exception(e,logger=logger)
                    data={}
            else:
                logger.warning(f"{this()}: Invalid queue {progress_queue} FEEDBACK = {FEEDBACK}")
                data={}
    if len(data):
        logger.trace(f"{this()}: read from: {ipc_mode}:{ipc_id} => {type(data)} data:{data}")  
    return json.dumps(data)
        
@main.route('/clean-progress',methods=['GET'])
def clean_progress():
    ''' Deletes/cleans up progress data from server
    '''
    global FEEDBACK
    status = f"{this()}: UNKNOWN"
    
    ipc_mode          = request.args.get('ipc_mode'    , None)
    ipc_id            = request.args.get('ipc_id'      , None)

    temp_dir = tempfile.gettempdir()
    
    if   ipc_mode == 'filesystem':
        progress_filename = f"{temp_dir}/{ipc_id}.log"  
        trace_filename    = f"{temp_dir}/{ipc_id}.trace"  
    elif ipc_mode == 'fifo':
        progress_fifo     = f"{temp_dir}/{ipc_id}"  
    elif ipc_mode == 'queue':
        progress_queue    = FEEDBACK.get(ipc_id)
    else:
        logger.error(f"{this()}: IPC invalid mode:{ipc_mode} id:{ipc_id} FEEDBACK = {FEEDBACK}")  

    logger.debug(f"{this()}: IPC mode:{ipc_mode} id:{ipc_id} FEEDBACK = {FEEDBACK}")  

    if ipc_mode == 'filesystem':
        status = ''
        if os.path.exists(progress_filename):
            try:
                os.remove(progress_filename)
                status = f"file: '{progress_filename}' removed OK. "
            except Exception as e:
                status = f"exception: {str(e)}. "
                emtec_handle_general_exception(e,logger=logger)
        else:
            status = f"'{progress_filename}' did not exist. "
            emtec_handle_general_exception(e,logger=logger)
        if os.path.exists(trace_filename):
            try:
                os.remove(trace_filename)
                status = status + f"file: '{trace_filename}' removed OK."
            except Exception as e:
                status = status + f"exception: {str(e)}."
                emtec_handle_general_exception(e,logger=logger)
        else:
            status = status + f"file: '{trace_filename}' did not exist."
    if ipc_mode == 'fifo':
        try:
            os.remove(progress_fifo)
            status = f"{this()}: named pipe fifo'{progress_fifo}' removed OK"
        except Exception as e:
            status = f"{this()}: exception: {str(e)}"
            emtec_handle_general_exception(e,logger=logger)
    if ipc_mode == 'queue':
        try:
            while not progress_queue.empty():
                item = progress_queue.get(block=False)
            FEEDBACK.pop(ipc_id,None)
            status = f"{this()}: OK queue '{ipc_id}' is empty and deleted now"
        except queue.exc.Empty:
            status = f"{this()}: OK queue is empty"
        except Exception as e:
            status = f"{this()}: ERROR exception: {str(e)}"
            emtec_handle_general_exception(e,logger=logger)
    logger.info(f"{this()}: status = {status}")
    data = { 'status' : status }
    return json.dumps(data)

@main.route('/forms/Migration/delete_vm_from_group', methods=['GET', 'POST'])
@login_required
def forms_Migration_delete_vm_from_group(form=None):
    mgId   = request.values.get('mgId',None)
    vmId   = request.values.get('vmId',None)
    # Aqui debe eliminar el registro de vm asociado al grupo 
    # llamar a forms/Migration con el mismo mgId
    try:
        vm = db.session.query(Migration_Groups_VM
            ).filter(   
                Migration_Groups_VM.MG_Id==mgId,
                Migration_Groups_VM.vm_uuid==vmId
                ).one_or_none()
        logger.debug(f"{this()}: vm to delete = {vm}")
        if vm is not None:
            vmName=vm.vm_name
            db.session.delete(vm)
            db.session.commit()
            db.session.flush()
        flash(gettext("'%s' deleted from migration group '%s'")%(vmName,mgId),"info")
    except Exception as e:
        emtec_handle_general_exception(e,logger=logger)    
        flash(f"{this()}: {gettext('exception')}: {str(e)}","error")
    return redirect(url_for('.forms_Migration',Id=mgId))

@main.route('/forms/Migration/report_migration_feedback', methods=['GET', 'POST'])
@login_required
def forms_Migration_report_migration_feedback():
    logger.info (f"{this()}: IN {request.method} Migration Group Id = {request.values.get('Id')} User = {current_user}")
    ipc_id = request.values.get('ipc_id')
    if ipc_id:
        try:
            logger.debug(f'{this()}: got Id={ipc_id} from request.form {request}')        
            temp_dir = tempfile.gettempdir()
            try:
                trace_filename = f"{temp_dir}/{ipc_id}.trace"
                with open(trace_filename,"r") as fp:
                    resume = json.loads(fp.read())
            except Exception as e:
                emtec_handle_general_exception(e,logger=logger)
                resume = {}
            data = {
            'resume':resume,
            'lines' :[]
            }
            log_filename = f"{temp_dir}/{ipc_id}.log"
            logger.debug(f"{this()}:data = {type(data)} {data}")
            if os.path.exists(trace_filename):
                logger.debug(f"{this()}: file {trace_filename} exists")
                with open(log_filename,"r") as fp:
                    lines = fp.readlines()
                if len(lines):
                    for line in lines:
                        log,feedback = line.split('|')
                        data['lines'].append({
                            'log':log,
                            'feedback':json.loads(feedback)
                            })
            logger.debug(f"{this()}: data = {type(data)} {len(data)} rows")
            logger.info(f"{this()}: will render migration_report.html ...")
            current_app.jinja_env.filters['format_timestamp'] = format_timestamp
            return render_template('migration_report.html',
                    data = data
                    )
        except Exception as e:
            emtec_handle_general_exception(e,logger=logger)
            flash(f"{this()}: {gettext('exception')}: {str(e)}","error")
            return redirect("/")
    else:
        flash(gettext('invalid migration report id = %s').capitalize()%ipc_id,'error')
        return redirect("/")

@main.route('/forms/Migration', methods=['GET', 'POST'])
@login_required
def forms_Migration():
    ''' GV current_user must me 'confirmed' in order to have update privileges '''
    tracebox_log(f"{this()}: IN {request.method} Migration Group Id = {request.values.get('Id')} User = {current_user} confirmed = {current_user.confirmed}",
            logger = logger,
            level  = logging.INFO,
            length = TRACEBOX_LOG_LENGTH
            )

    logger.debug (f"{this()}: ***** -----------------------------------")
    logger.debug (f"{this()}: request          = {request}")
    logger.debug (f"{this()}: request.args     = {request.args}")
    logger.debug (f"{this()}: request.form     = {request.form}")
    logger.debug (f"{this()}: Nutanix Projects = {current_app.config.get('NUTANIX_PROJECTS')}")
    logger.debug (f"{this()}: Test Only Mode   = {current_app.config.get('BUTLER_TEST_ONLY_MODE')}")
        
    # DB Control -------------------------------------------------------
    logger.debug(f"{this()}: Reseting DB state ...")
    try:    
        db.session.flush()
        db.session.commit()
    except Exception as e:
        emtec_handle_general_exception(e,logger=logger)
        try:
            db.session.rollback()
            logger.error(f"{this()}: Rolled back.")
        except Exception as e:
            emtec_handle_general_exception(e,logger=logger)
    # DB Control -------------------------------------------------------
    # Get Id if any, dont care if GET (query string) or POST (post data) Method
    Id = request.form.get('mgMigrationGroups',0,type=int)
    logger.debug(f'{this()}: got Id={Id} from request.form {request}')        
    if not Id:
        Id = request.values.get('Id',0,type=int)
    logger.debug(f'{this()}: got Id={Id} from request.values {request}')        
    # Setup initial data -----------------------------------------------
    # look for initial data in DB if any
    row =  None
    rox =  None
    logger.debug(f'{this()}: load Migration Group row from DB for Id = {Id}')
    if Id>0:
        row =  db.session.query(Migration_Groups).filter(Migration_Groups.MG_Id == Id).first()
    else:
        logger.info(f"{this()}: No specific Id. Getting first group")
        row =  db.session.query(Migration_Groups).first()        
    logger.debug(f'{this()}: load Migration Group prow from DB for Id = {Id}')
    if row is None:
        logger.debug(f'{this()}: Migration Group row does not exist. Initialize empty objects.')
        row=Migration_Groups()
        #session['is_new_row']=True
        # GV set defaults
    if row is not None:
        logger.debug(f"{this()}: Getting VM rows for Migration Group = ({row.MG_Id}) {row.Name}")
        rox = db.session.query(Migration_Groups_VM
                ).filter(Migration_Groups_VM.MG_Id == row.MG_Id
                ).all()
    else:
        rox = None
    logger.debug(f"{this()}: Migration_Group table row id  = {row.MG_Id}")
    logger.debug(f"{this()}: Migration_Group_VM rows len   = {len(rox)}")
    
    logger.debug(f"{this()}: Preparing form instantiation ...")
    logger.debug(f"{this()}: Setting up VMs & checkboxes for 'migration' option")

    mgVmCheckBoxes=[]
    mgVms=[]
    for r in rox:
        #orm.mgVms.append(r)
        mgVms.append(r)
        name = f'cbx_1_{r.vm_uuid}'
        mgVmCheckBoxes.append({'name':name})
    
    # FORM BORNS HERE ##################################################
    
    logger.debug(f"{this()}: Creating form object ...")
    form       = frm_migration_01(mgMigration=mgVmCheckBoxes)
    logger.debug(f"{this()}: form = {form} ...")
    # Basic form Initialization
    if row is not None:
        form.mgId           = row.MG_Id 
        form.mgOrigin.data  = row.Origin 
        form.mgDestiny.data = row.Destiny
    else:
        form.mgId           = 0 
        form.mgOrigin.data  = None 
        form.mgDestiny.data = None
        
    form.mgVms          = mgVms
    
    # FORM BORNS HERE ##################################################

    logger.debug(f"{this()}: Getting migration groups list")
    migration_group_list = get_migration_group_list()
    logger.debug(f"{this()}: {len(migration_group_list)} migration groups list found.")
    
    migration_group_options = []
    for mgid,name,origin,destiny in migration_group_list:
        migration_group_options.append((mgid,name))

    if len(migration_group_options):
        migration_group_options = unique_list(migration_group_options)
        migration_group_options.sort(key=lambda tup: tup[1])
        form.mgName.choices = migration_group_options
        if not form.mgName.data:
            if form.mgId is not None:
                form.mgName.data = form.mgId
            else:
                form.mgName.data = form.mgName.choices[0][0]
    else:
        form.mgName.choices = []
        form.mgName.data    = 0

    logger.debug(f"{this()}: form.mgName.choices = {form.mgName.choices}")
    logger.debug(f"{this()}: form.mgName.data    = {form.mgName.data}")
    logger.debug(f"{this()}: form.mgId           = {form.mgId}")
            
    # GV POST/GET request method depending  initializations ------------
    if request.method == 'POST':
        logger.debug(f"{this()}: POST request initializations ...")
        # GV -----------------------------------------------------------
        logger.debug(f"{this()}: Trying to populate 'migrate' flags ...")
        logger.debug(f"{this()}: form.mgVms len   = {len(form.mgVms)} ...")

        logger.debug(f"{this()}: form.mgMigration.data = {len(form.mgMigration.data)} {form.mgMigration.data} ...")
        for vmcounter in range(len(form.mgVms)):
            if str(request.form.get(f"mgMigration-{vmcounter}")) == 'on':
                mgVms[vmcounter].vm_migrate = True
            else:
                mgVms[vmcounter].vm_migrate = False
            logger.debug(f"{this()}: vm {vmcounter} {mgVms[vmcounter].vm_uuid} {mgVms[vmcounter].vm_name:30} migrate={mgVms[vmcounter].vm_migrate}")
            vmcounter += 1
            form.mgId = request.form.get('mgMigrationGroups')
        form.mgNewName.data   = request.form.get('mgNewName')
        form.mgEditName.data  = request.form.get('mgEditName')
        form.mgCloneName.data = request.form.get('mgCloneName')
        if request.form.get('mgName'):
            form.mgName.data = int(request.form.get('mgName'))
            form.mgId        = int(request.form.get('mgName'))
        if request.form.get('mgOrigin'):
            form.mgOrigin.data = request.form.get('mgOrigin')
        if request.form.get('mgDestiny'):
            form.mgDestiny.data = request.form.get('mgDestiny')
        # GV -----------------------------------------------------------
    elif request.method == 'GET':
        logger.debug(f"{this()}: GET request initializations ...")
        form.mgData.update({'can_migrate':request.values.get('can_migrate')})
        if form.mgData.get('can_migrate'):
            if form.mgData['can_migrate'].upper() in ['TRUE']:
                form.mgData['can_migrate'] = True
            else:
                form.mgData['can_migrate'] = False
        else:
            form.mgData['can_migrate'] = False
            
        form.mgName.data = form.mgId
    # GV ---------------------------------------------------------------    
    
    logger.debug(f"{this()}: form.mgName.choices = {form.mgName.choices}")
    logger.debug(f"{this()}: form.mgName.data    = {form.mgName.data} {dict(form.mgName.choices).get(form.mgName.data)}")
    logger.debug(f"{this()}: form.mgId           = {form.mgId}")
        
    if form.mgName.data is None:
        logger.warning(f"{this()}: form.mgName.data correction ...")
        form.mgName.data = form.mgId

    logger.debug(f"{this()}: form.mgName.choices = {form.mgName.choices}")
    logger.debug(f"{this()}: form.mgName.data    = {form.mgName.data}  {dict(form.mgName.choices).get(form.mgName.data)}")
    logger.debug(f"{this()}: form.mgId           = {form.mgId}")
    logger.debug(f"{this()}: form.mgName         = {dict(form.mgName.choices).get(form.mgName.data)}")
        
    lists = forms_Migration_populate_lists(form)
    
    if lists is None:
        return redirect('/')
    
    cluster_options = lists.get('cluster_options')
    clusters_uuid   = lists.get('clusters_uuid')
    vm_list         = lists.get('vm_list')
    vms_uuid        = lists.get('vms_uuid')
    
    form.mgName.choices    = migration_group_options
    form.mgOrigin.choices  = cluster_options
    form.mgDestiny.choices = cluster_options
    
    if not form.mgName.data:
        form.mgName.data = form.mgId

    # GV Building reverse uuid hashed map ------------------------------
    for cluster_uuid in vm_list:
        logger.debug(f"{this()}: cluster_uuid={cluster_uuid} vm_list[cluster_uuid].get('vms')={len(vm_list[cluster_uuid].get('vms'))}")
        for vmname in vm_list[cluster_uuid].get('vms'):
            vm = vm_list[cluster_uuid].get('vms').get(vmname)
            vms_uuid.update(
                {
                    vm.get('uuid'):{
                        'name':vm.get('name'),
                        'cluster':cluster_uuid,
                        'power_state':vm.get('power_state'),
                        }
                }
            )
    # GV ---------------------------------------------------------------
    
    form.mgData.update({
        'migration_group_list': migration_group_list,
        'vm_list'      : vm_list,
        'clusters_uuid': clusters_uuid,
        'vms_uuid'     : vms_uuid,    
        'tasks'        : [],    
        })
    # GV get_projects_list requires form.mgData populated at this stage
    form.mgData.update({
        'projects_list': get_projects_list(form),
        })
    
    logger.debug(f"{this()}: form.mgData['projects_list']={form.mgData.get('projects_list')}")
    
    # GV Will consider all VMs from all cluster as choice options
    # GV since VMs may migrate among clusters
    logger.debug(f"{this()}: Getting list of VMs for all Clusters")
    form.mgAllVms.choices = []
    form.mgAllVms.data    = None
    
    AllVms={}
    for cluster_uuid in vm_list.keys():
        AllVms.update(vm_list.get(cluster_uuid).get('vms'))
    for vm in AllVms:
        form.mgAllVms.choices.append((AllVms.get(vm).get('uuid'),vm))

    logger.info(f"{this()}: Total {len(form.mgAllVms.choices)} VMs found in all Clusters ...")
    
    form.mgAllVms.choices = unique_list(form.mgAllVms.choices)
    form.mgAllVms.choices.sort(key=lambda tup: tup[1])
        
    if len(form.mgAllVms.choices):
        form.mgAllVms.data = form.mgAllVms.choices[0][0]
    else:
        flash(gettext('No virtual machines available for selection'),"error")
    
    logger.debug(f"{this()}: len migration groups = {len(migration_group_list)}")
    logger.debug(f"{this()}: len clusters         = {len(clusters_uuid)}")
    logger.debug(f"{this()}: len vm_list          = {len(vm_list)}")
    for uuid in vm_list:
        logger.debug(f"{this()}: {uuid} : {vm_list[uuid]['name']} = {len(vm_list[uuid]['vms'])} vms")
    logger.debug(f"{this()}: len origin vms       = {len(form.mgAllVms.choices)}")
    # GV ***************************************************************

    logger.debug(f"{this()}: form.is_submitted() = {form.is_submitted()}")
    logger.debug(f"{this()}: form.errors         = {form.errors}")
    # Will check if all validated
    if form.is_submitted() and len(form.errors)==0:
        logger.info (f"{this()}: form submited and no errors (not validated yet)")
        logger.debug(f"{this()}: form data = {form.data}")
        # GV Functions that do not require validation    
        if form.submit_Choose.data or form.submit_Create.data or form.submit_Add.data or form.submit_Clone.data or form.submit_Edit.data or form.submit_Delete.data:
            if   form.submit_Choose.data:
                logger.info(f"{this()}: Option Choose MG {form.mgName.data} {dict(form.mgName.choices).get(form.mgName.data)}")
                return redirect(url_for('.forms_Migration',Id=form.mgName.data))
            elif form.submit_Create.data:
                logger.info(f"{this()}: Option Create new MG")
                groupid = forms_Migration_create_group(form)
                logger.debug(f"{this()}: form.mgNewId.data = {form.mgNewId.data} redirecting ...")
                return redirect(url_for('.forms_Migration',Id=form.mgNewId.data))
            elif form.submit_Add.data:
                for vmId in request.form.getlist('vmId'):
                    logger.info(f"{this()}: Option Add VM {vmId} to MG {form.mgId}")
                    vmName = forms_Migration_add_vm_to_group(form,vmId)
                return redirect(url_for('.forms_Migration',Id=form.mgId))
            elif form.submit_Clone.data:
                logger.info(f"{this()}: Option Clone MG {form.mgId}")
                form.mgNewId.data = forms_Migration_clone_group(form)
                return redirect(url_for('.forms_Migration',Id=form.mgNewId.data))
            elif form.submit_Edit.data:
                logger.info(f"{this()}: Option Edit MG {form.mgId} Name")
                form.mgNewId.data = forms_Migration_edit_group(form)                
                return redirect(url_for('.forms_Migration',Id=form.mgNewId.data))
            elif form.submit_Delete.data:
                logger.info(f"{this()}: Option Delete MG {form.mgId}")
                form.mgId = forms_Migration_delete_group(form)
                return redirect(url_for('.forms_Migration',Id=0))
        else:
            # GV Functions that do require validation    
            logger.info(f"{this()}: validating ...")
            try:
                form.validate()
            except Exception as e:
                logger.error(f"{this()}: form.validate exception: {str(e)}")
                logger.error(f"{this()}: form.errors: {form.errors}")
                emtec_handle_general_exception(e,logger=logger)
            logger.debug(f"{this()}: returned from form.validate() errors={len(form.errors)} {form.errors}")
            if len(form.errors) > 0:
                logger.error(f"{this()}: form.is_submitted() = {form.is_submitted()} form.errors = {form.errors}")
                logger.error(f"{this()}: form.data           = {form.data}")
            else:
                logger.debug(f"{this()}: no errors will evaluate button pushed")
                
                # Gets sure vmData buffer is complete ******************
                #form.vmData.update(Get_data_context(current_app,db,mail,row.Id,current_user))
                # ******************************************************
                # ------------------------------------------------------
                # Basic Requestor's submits
                # ------------------------------------------------------
                if   form.submit_Save.data:
                    logger.info(f"{this()}: Save button selected.")
                    form.mgId = forms_Migration_save_group(form)
                    logger.info(f"{this()}: redirecting to '.forms_Migration' with Id = {form.mgId}")
                    return redirect(url_for('.forms_Migration',Id=form.mgId))
                elif form.submit_Switch.data:
                    logger.info(f"{this()}: Switch button selected.")
                    temp = row.Origin
                    row.Origin  = row.Destiny
                    row.Destiny = temp
                    try:
                        db.session.merge(row)
                        db.session.commit()
                    except Exception as e:
                        db.session.rollback()
                        emtec_handle_general_exception(e,logger=logger)
                    logger.info(f"{this()}: redirecting to '.forms_Migration' with Id = {form.mgId}")
                    return redirect(url_for('.forms_Migration',Id=form.mgId))
                elif form.submit_Validate.data:
                    logger.info(f"{this()}: Validate button selected.")
                    form.mgId,errors,warnings = forms_Migration_Validate(form)
                    form.mgData.update({'can_migrate':True})
                    if len(errors):
                        form.mgData.update({'can_migrate':False})
                    else:
                        if len(warnings):
                            pass
                        else:
                            flash(gettext("Validation OK. Migration can proceed"),"message")
                    logger.info(f"{this()}: redirecting to '.forms_Migration' with Id = {form.mgId}")
                    return redirect(url_for('.forms_Migration',Id=form.mgId,can_migrate=form.mgData.get('can_migrate')))
                elif form.submit_Migrate.data:
                    logger.info(f"{this()}: Migrate button selected.")
                    form.mgId,tasks = forms_Migration_Migrate(form)
                    if form.mgId and len(tasks):
                        logger.info(f"{this()}: form.mgId={form.mgId} tasks={len(tasks)}")
                        #flash(gettext('migration validation feedback follows'),'message')
                        form.mgData.update({
                            'ipc':{
                                'ipc_mode':'filesystem',
                                'ipc_id'  :datetime.timestamp(datetime.now()),
                                'fmt'     :'json',
                                'verbose' :1,
                                'trace'   :True,
                                'FEEDBACK':FEEDBACK,
                                }
                            })
                        logger.debug(f"{this()}: form.mgData.get('ipc').get('trace') = {form.mgData.get('ipc').get('trace')}")
                        if form.mgData.get('ipc').get('trace'):
                            temp_dir = tempfile.gettempdir()
                            trace_filemame = f"{temp_dir}/{form.mgData.get('ipc').get('ipc_id')}.trace"
                            logger.debug(f"{this()}: creating {trace_filemame}")
                            mgVms = []
                            for vm in form.mgVms:
                                if vm.vm_migrate:
                                    mgVms.append({
                                        'uuid':vm.vm_uuid,
                                        'name':vm.vm_name,
                                    })
                                else:
                                    pass
                            with open(trace_filemame,"w") as fp:
                                resume = {
                                    'mgId':form.mgId,
                                    'mgName':dict(form.mgName.choices).get(form.mgName.data),
                                    'mgOrigin':dict(form.mgOrigin.choices).get(form.mgOrigin.data),
                                    'mgDestiny':dict(form.mgDestiny.choices).get(form.mgDestiny.data),
                                    'mgVms':mgVms,
                                    'ipc':form.mgData.get('ipc')
                                }
                                written = fp.write(json.dumps(resume))
                                logger.debug(f"{this()}: written {written} bytes to {trace_filemame}")
                            
                        logger.debug(f"{this()}: form IPC mode={form.mgData.get('ipc').get('ipc_mode')} id = {form.mgData.get('ipc').get('ipc_id')} fmt={form.mgData.get('ipc').get('fmt')}")
                        newpid = os.fork()
                        if newpid == 0:
                            logger.info(f"{this()}: Child pid = {os.getpid()} unique = {form.mgData.get('ipc').get('ipc_id')}")
                            logger.info(f"{this()}: Remote Migration validation starts")
                            completed = forms_Migration_Feedback(form,tasks)
                            if completed:
                                tracebox_log(f"{this()}: Migration completed successfully",
                                    logger = logger,
                                    level  = logging.INFO,
                                    length = TRACEBOX_LOG_LENGTH
                                    )

                            else:
                                logger.warning(f"{this()}: Migration not completed")
                            # GV Flask requires a non None return, in this case
                            # GV Child will only process and generate feedback
                            # GV for parent render below
                            return ''
                        else:                            
                            tracebox_log(f"{this()}: Parent forked into process newpid = {newpid} unique = {form.mgData.get('ipc').get('ipc_id')}",
                                logger = logger,
                                level  = logging.INFO,
                                length = TRACEBOX_LOG_LENGTH
                                )
                            logger.info(f"{this()}: Will render template 'migration_feedback.html' for ({form.mgId}):'{dict(form.mgName.choices).get(form.mgName.data)}'")
                            return render_template('migration_feedback.html',
                                    form = form
                                    )
                    else:
                        flash(gettext("Invalid Migration response: mg Id=%s migration tasks=%s")%(form.mgId,len(tasks)),"error")    
                        logger.info(f"{this()}: redirecting to '.forms_Migration' with Id = {form.mgId}")
                        return redirect(url_for('.forms_Migration',Id=form.mgId))
                # ------------------------------------------------------
    else:
        logger.info(f"{this()}: form is not submitted")

    # GV ***************************************************************
    logger.info(f"{this()}: updating Vms ...")
    forms_Migration_update_vms(form)
    # GV ***************************************************************
    logger.debug(f"{this()}: form.data =")
    for key in form.data:
        logger.debug(f"{this()}:   {key:15s} = {str(type(form.data.get(key))):20s} {form.data.get(key)}")
        
    logger.info(f"{this()}: Will render template 'migration.html' for ({form.mgId}):'{dict(form.mgName.choices).get(form.mgName.data)}'")
    # Setup exploit functions for Jinja template 
    current_app.jinja_env.globals.update(now=datetime.now)
    return render_template('migration.html',
            form = form
            )
            
# EOF ******************************************************************
