# ======================================================================
# BUTLER REQUEST ROUTES
# View for General request Edition
# (c) Sertechno 2020
# GLVH @ 2020-11-06
# ======================================================================
import jinja2
import copy
from pprint                 import pformat
from sqlalchemy             import desc
from emtec.debug            import *
from emtec.data             import *
from emtec.butler.forms     import frm_migration_01,form_log
from emtec.butler.functions import *

# Templates will reside on view_request_template.py
# Functions will reside on view_request_functions.py

# Support functions

import urllib3
def nutanix_get_vm_list(host=None,port=9440,username=None,password=None,protocol='https',version=2,verify=False):
    urllib3.disable_warnings()
    response = None
    try:
        if version == 2:
            method   = 'GET'
            endpoint = '/api/nutanix/v2.0/vms/'
            headers  = {'Accept': 'application/json'}
            url      = f"{protocol}://{host}:{port}/{endpoint}"
            response = requests.get(url,auth=(username,password),headers=headers,verify=verify)
        elif version == 3:
            method   = 'POST'
            endpoint = '/api/nutanix/v3/vms/list'
            headers  = {'Accept':'application/json','Content-Type': 'application/json'}
            data     = {'kind':'vm'}
            url      = f"{protocol}://{host}:{port}/{endpoint}"
            response = requests.get(url,auth=(username,password),headers=headers,data=data,verify=verify)
    except Exception as e:
        print(f"nutanix_get_vm_list: Exception = {str(e)}")
    return response


# View functions are in view_request_functions.py  
    # ------------------------------------------------------------------

"""@main.route('/select/Request', methods=['GET', 'POST'])
@login_required
def select_Request():
    logger.debug(f'{this()}: Enter')    
    data={}
    # Pagination/Filter required  field
    page    = request.args.get('page'   ,1           ,type=int)
    field   = request.args.get('field'  ,None        ,type=str)
    value   = request.args.get('value'  ,None        ,type=str)
    # Spacific Filter fields
    Status  = request.args.get('Status' ,default=None,type=int)
    User_Id = request.args.get('User_Id',default=None,type=int)
    # Define basical query, joining Requests with related tables
    # Basic Query will get a JOIN of related tables
    logger.debug(f'{this()}: page    = {page}')    
    logger.debug(f'{this()}: field   = {field}')    
    logger.debug(f'{this()}: value   = {value}')    
    logger.debug(f'{this()}: Status  = {Status}')    
    logger.debug(f'{this()}: User_id = {User_Id}')    
    # Setup query for required fields only, no need to load all table
    # fields
    # 20210603 cambiado de modelo flask a ORM requests -> Requests
    
    # DB Control -------------------------------------------------------
    try:    
        db.session.flush()
        db.session.commit()
    except Exception as e:
        logger.error(f"{this()}: DB Control Exception: {str(e)}. rolling back ...")
        try:
            db.session.rollback()
            logger.error(f"{this()}: Rolled back.")
        except Exception as e:
            logger.error(f"{this()}: While rolling back Exception{str(e)}.")
    # DB Control -------------------------------------------------------

    query = db.session.query(
                Requests.Id,
                Requests.Status,
                Requests.Last_Status_Time,
                nutanix_prism_vm.vm_name,
                Users.username,
                Cost_Centers.CC_Description
                ).join(nutanix_prism_vm,
                    nutanix_prism_vm.Request_Id == Requests.Id
                ).join(Users,
                    Users.id == Requests.User_Id
                ).join(Cost_Centers,
                    Cost_Centers.CC_Id == Requests.CC_Id
                )
    # Various filters to conditionaly implement
    # Filter by REQUESTOR, requestor can not see others user's requests
    if current_user.role_id == ROLE_REQUESTOR:
        query = query.filter(Requests.User_Id == current_user.id)
    
    fltr=''
    # Select requests with "Status" Flag on, as per request argument
    if Status is not None:
        # See specific bitwise operator use for comparison
        # This is an AND comparison between:
        # request.Status AND Status <> request.Status & Status
        query = query.filter(Requests.Status.op("&")(Status))
        fltr=f'Status={Status}'
    if User_Id is not None:
        if User_Id and current_user.role_id != ROLE_REQUESTOR:
            query = query.filter(Requests.User_Id == User_Id)
            fltr=fltr+f'&User_Id={User_Id}'
        else:
            query = query.filter(Requests.User_Id == current_user.id)
            fltr=fltr+f'&User_Id={current_user.id}'
    # Will allways order by time, newer first
    query = query.order_by(desc(Requests.Last_Status_Time))
    logger.debug(f'{this()}: query   = {query}')    
    
    # Actually query DB and get all requests upon filter
    
    # getting paginated rows for query
    rows =  query.paginate(  
                page, 
                per_page  = current_app.config['LINES_PER_PAGE'], 
                error_out = False
            )
    # Setting pagination variables ...
    if field is not None:
       next_url = url_for('.select_Request', field=field, value=value, page=rows.next_num) if rows.has_next else None
       prev_url = url_for('.select_Request', field=field, value=value, page=rows.prev_num) if rows.has_prev else None
    else:
       next_url = url_for('.select_Request', page=rows.next_num) if rows.has_next else None
       prev_url = url_for('.select_Request', page=rows.prev_num) if rows.has_prev else None
    # Actual rendering ...
    
    # Option to return json list 
    if request.headers.get('Content-Type') is not None or request.args.get('JSON',None,type=str) is not None:
        # NOTE: needs review for JSONnifiyng output when needed (API Interface?)
        if "JSON" in request.headers.get('Content-Type') or request.args.get('JSON',None,type=str) is not None:
            return json.dumps(serialize_object(rows.__dict__))
    
    # Setup exploit functions for Jinja template 
    current_app.jinja_env.globals.update(get_request_status_description=get_request_status_description)
    current_app.jinja_env.globals.update(get_vm_resume=get_vm_resume)
    current_app.jinja_env.globals.update(has_status=has_status)
    current_app.jinja_env.globals.update(get_description=get_description)
    logger.debug(f'{this()}: will render select_request.html rows={type(rows)}')    
    return render_template('select_request.html',rows=rows,fltr=fltr)
"""
import  pandas
from    pandas.io.json          import json_normalize
from    flask                   import send_file
import tempfile

"""@main.route('/export/Request', methods=['GET', 'POST'])
@login_required
def export_Request():
    logger.debug(f'{this()}: Enter')    
    data={}
    # Pagination/Filter required  field
    page    = request.args.get('page'   ,1           ,type=int)
    field   = request.args.get('field'  ,None        ,type=str)
    value   = request.args.get('value'  ,None        ,type=str)
    # Spacific Filter fields
    Status  = request.args.get('Status' ,default=None,type=int)
    User_Id = request.args.get('User_Id',default=None,type=int)
    # Define basical query, joining Requests with related tables
    # Basic Query will get a JOIN of related tables
    logger.debug(f'{this()}: page    = {page}')    
    logger.debug(f'{this()}: field   = {field}')    
    logger.debug(f'{this()}: value   = {value}')    
    logger.debug(f'{this()}: Status  = {Status}')    
    logger.debug(f'{this()}: User_id = {User_Id}')    
    # Setup query for required fields only, no need to load all table
    # fields
    # 20210603 cambiado de modelo flask a ORM requests -> Requests
    
    # DB Control -------------------------------------------------------
    try:    
        db.session.flush()
        db.session.commit()
    except Exception as e:
        logger.error(f"{this()}: DB Control Exception: {str(e)}. rolling back ...")
        try:
            db.session.rollback()
            logger.error(f"{this()}: Rolled back.")
        except Exception as e:
            logger.error(f"{this()}: While rolling back Exception{str(e)}.")
    # DB Control -------------------------------------------------------

    query = db.session.query(
                Requests.Id,
                Requests.Status,
                Requests.Last_Status_Time,
                nutanix_prism_vm.vm_name,
                Users.username,
                Cost_Centers.CC_Description
                ).join(nutanix_prism_vm,
                    nutanix_prism_vm.Request_Id == Requests.Id
                ).join(Users,
                    Users.id == Requests.User_Id
                ).join(Cost_Centers,
                    Cost_Centers.CC_Id == Requests.CC_Id
                )
    # Various filters to conditionaly implement
    # Filter by REQUESTOR, requestor can not see others user's requests
    if current_user.role_id == ROLE_REQUESTOR:
        query = query.filter(Requests.User_Id == current_user.id)
    # Select requests with "Status" Flag on, as per request argument
    if Status is not None:
        # See specific bitwise operator use for comparison
        # This is an AND comparison between:
        # request.Status AND Status <> request.Status & Status
        query = query.filter(Requests.Status.op("&")(Status))
    if User_Id is not None:
        if User_Id and current_user.role_id != ROLE_REQUESTOR:
            query = query.filter(Requests.User_Id == User_Id)
        else:
            query = query.filter(Requests.User_Id == current_user.id)
    # Will allways order by time, newer first
    query = query.order_by(desc(Requests.Last_Status_Time))
    logger.debug(f'{this()}: query   = {query}')    
    
    # Actually query DB and get all requests upon filter
    
    # getting all rows for query
    rows =  query.all()
    # Actual rendering ...

    #def export_to_xls(output_file,rows,Customer,From,To,Status,Currency):

    temp_name   = next(tempfile._get_candidate_names())
    output_file = f"{temp_name}.xlsx"
    
    d = {'detail':[]}
    
    for row in rows:
        d['detail'].append(
            {   
                'Id':row.Id,
                'Estado':', '.join(get_request_status_description(row.Status)),
                'Ultima modificacion':row.Last_Status_Time,
                'Nombre de MV':row.vm_name,
                'Usuario':row.username,
                'Centro de Costo':row.CC_Description            
            }
        )

    #f1 = json_normalize(d, 'detail').assign(**d['header'])        
    df1 = json_normalize(d, 'detail')       
    xlsx_file="%s/%s"%(current_app.root_path,url_for('static',filename='tmp/%s'%(output_file)))
    df1.to_excel(xlsx_file,'Sheet 1')
    return send_file(xlsx_file,as_attachment=True,attachment_filename=output_file)
"""

"""@main.route('/forms/Request', methods=['GET', 'POST'])
@login_required
def forms_Request():
    logger.debug(f"{this()}: Enter")
    logger.debug(f"{this()}: logger.handlers       = {logger.handlers}")
    logger.debug(f"{this()}: session               = {session}")
    logger.debug(f"{this()}: session dir           = {dir(session)}")
    logger.debug(f"{this()}: session keys          = {session.keys()}")
    logger.debug(f"{this()}: session.prev_row      = {session.get('prev_row')}")
    if session.get('data') is not None:
        logger.debug(f"{this()}: session.data.prev_row = {session.get('data').get('prev_row')}")
    logger.debug(f"{this()}: request               = {request}")
    logger.debug(f"{this()}: request dir           = {dir(request)}")
    
    # DB Control -------------------------------------------------------
    try:    
        db.session.flush()
        db.session.commit()
    except Exception as e:
        logger.error(f"{this()}: DB Control Exception: {str(e)}. rolling back ...")
        try:
            db.session.rollback()
            logger.error(f"{this()}: Rolled back.")
        except Exception as e:
            logger.error(f"{this()}: While rolling back Exception{str(e)}.")
    # DB Control -------------------------------------------------------
    # Get Id if any
    Id  =  request.args.get('Id',0,type=int)
    
    # Setup initial data -----------------------------------------------
    # look for initial data in DB if any
    logger.debug(f'{this()}: load row from DB for Id={Id}')
    # GV 20210603 GV row =  Requests.query.filter(Requests.Id == Id).first()
    row =  db.session.query(Migration_Groups).filter(Migration_Groups.MG_Id == Id).first()
    if row is None:
        logger.debug(f'{this()}: row no existe inicializa objetos vacios')
        row=Migration_Groups()
        session['is_new_row']=True
        # set defaults
    else:

    # Setup some session context data
    
    # Asures Current App Configuration is captured as dict
    d={}
    for key in current_app.config.keys():
        d.update({key:current_app.config.get(key)})
    session['data']={
        'user'  : current_user.username,
        'userid': current_user.id,
        'role'  : current_user.role_id,
        'roles' : ROLES,
        'status': BUTLER_STATUS,
        'debug' : current_app.config.get('DEBUG',False),
        'extra' : current_app.config.get('BUTLER_EXTRA',False),
        'config': serialize_object(d),
        'top_cost_center_id': 0,
        'top_cost_center_code': '',
    }
        
    if   current_user.role_id in [ROLE_REQUESTOR]:
        session['data']['rolename'] = 'Requestor'
    elif current_user.role_id in [ROLE_APPROVER]:
        session['data']['rolename'] = 'Approver'
    elif current_user.role_id in [ROLE_VIEWER]:
        session['data']['rolename'] = 'Viewer'
    elif current_user.role_id in [ROLE_AUDITOR]:
        session['data']['rolename'] = 'Auditor'
    elif current_user.role_id in [ROLE_OPERATOR]:
        session['data']['rolename'] = 'Operator'
    else:
        session['data']['rolename'] = 'Other'
        
    # ------------------------------------------------------------------
    # ******************************************************************
    # Instance form
    logger.debug(f'{this()}: instance new form <= frm_request')
    form              = frm_request_01()
    
    # ******************************************************************
    
    # Inicializacion de datos debe reemplazarse por las rutinas de
    # poblamiento de opciones principalmente
    # ------------------------------------------------------------------

    # OJO Control con falla de configuracion/archivo mientras default tonto
    
    # ******************************************************************
    # ******************************************************************
    
    # ******************************************************************
    # Aqui está cargado todo el contexto
    data = Get_data_context(current_app,db,mail,row.Id,current_user)

    # ******************************************************************
    # ******************************************************************

    # Populates vm Data with all captured session data -----------------

    form.vmData.update(data)
    


    vmCorporate_choices  = []
    vmDepartment_choices = []
    vmCC_choices         = []
    vmType_choices       = []
    vmDiskImage_choices  = [('','')] # An empty option is valid in this context
    vmCluster_choices    = []
    vmProject_choices    = []
    vmCategory_choices   = []
    vmSubnet_choices     = []    
    
    for corporate in data.get('corporates'):
        vmCorporate_choices.append(corporate)
    for department in data.get('departments'):
        vmDepartment_choices.append(department)
    for cc in data.get('ccs'):
        vmCC_choices.append(cc)
    vmType_choices = data.get('types')

    for uuid,description,size in data.get('images'):
        vmDiskImage_choices.append((uuid,f'{description} ({size} GB)'))
    # Load Select Fields Choices and codes -----------------------------
    form.vmCorporate.choices  = vmCorporate_choices
    form.vmDepartment.choices = vmDepartment_choices
    form.vmCC.choices         = vmCC_choices
    form.vmType.choices       = vmType_choices
    # load uuid and name only
    form.vmCluster.choices = []
    for cluster in data.get('clusters'):
        form.vmCluster.choices.append((cluster[0],cluster[1]))
    form.vmProject.choices    = data.get('projects')
    form.vmCategory.choices   = data.get('categories')
    
    subnet_options = []
    for project,subnets in data.get('subnet_options'):
        if project == form.vmProject.data:
            subnet_options = [('','')] + subnets
            break
    
    logger.debug(pformat(subnet_options))

    form.vmVlan0Name.choices  = subnet_options
    form.vmVlan1Name.choices  = subnet_options
    form.vmVlan2Name.choices  = subnet_options
    form.vmVlan3Name.choices  = subnet_options


    for i in range(1):
        getattr(form,f'vmDisk{i}Image').choices = vmDiskImage_choices
    # ------------------------------------------------------------------

    logger.debug(f"{this()}: form.is_submitted() = {form.is_submitted()}")
    logger.debug(f"{this()}: form.errors         = {form.errors}")
    # Will check if all validated
    if form.is_submitted() and len(form.errors)==0:
        logger.debug(f"{this()}: will call form.validate()")
        try:
            form.validate()
        except Exception as e:
            logger.error(f"form.validate exception: {str(e)}")
            logger.error(f"form.errors: {form.errors}")
            emtec_handle_general_exception(e,logger=logger)
        logger.debug(f"{this()}: return from form.validate() errors={len(form.errors)}")
        if len(form.errors) != 0:
            logger.debug(f"{this()}: form.is_submitted() = {form.is_submitted()} form.errors = {form.errors}")
        else:
            logger.debug(f"no errors will evaluate button pushed")
            #form_log(form,logger.debug)
            
            # Gets sure vmData buffer is complete **********************
            form.vmData.update(Get_data_context(current_app,db,mail,row.Id,current_user))
            # **********************************************************
            # ----------------------------------------------------------
            # Basic Requestor's submits
            # ----------------------------------------------------------
            # Guardar --------------------------------------------------
            if     form.submit_Guardar.data and row.Status:
                # Get data from context --------------------------------
                row.MG_Id         = Id     
                save_form(form,row,rox)
                form.vmData.update({'row':row,'rox':rox})
                # Aqui ajusta valor en BD ------------------------------
                try:
                    ## GV db.session.close()
                    if row.Id == 0: 
                        session['is_new_row'] = True
                        db.session.add(row)
                        db.session.flush()
                        # specific query to get last id, other approach seem
                        # not to work
                        session['new_row']    = str(row)
                    else:
                        session['is_new_row'] = False
                        session['new_row']    = str(row)
                        db.session.merge(row)
                    saved_row=copy.copy(row)
                    db.session.commit()
                    ## GV db.session.close()
                    if session['is_new_row']==True:
                        form.vmData['row']=saved_row
                        logger.audit ( '%s:NEW:%s' % (current_user.username,session['new_row'] ) )
                    else:
                        # Check this code, cookie must transport premodification state
                        # so we can save audit data conditionaly
                        logger.debug(f"session.get('prev_row')={session.get('prev_row')}")
                        logger.debug(f"form.vmData.get('prev_row')={form.vmData.get('prev_row')}")
                        session['prev_row']=form.vmData.get('prev_row')
                        if session.get('prev_row') is not None:
                            logger.debug(f"session.prev_row is available")
                            if session['new_row'] != session['prev_row']:
                                logger.debug(f"change detected, session.prev_row is available")
                                form.vmData['row']=saved_row
                                logger.audit ( '%s:OLD:%s' % (current_user.username,session['prev_row']) )
                                logger.audit ( '%s:UPD:%s' % (current_user.username,session['new_row'] ) )    
                                '''
                                try:
                                    butler_notify_request(
                                        f"Solicitud {Id} Modificada por '{current_user.username}'",
                                        data=form.vmData,
                                        html_function=butler_output_request
                                        )
                                    message=Markup(f"<b>Solicitud {Id} Modificada</b>")
                                except Exception as e:
                                    message=Markup(f"<b>Solicitud {Id} Modificion excepcion: {str(e)}</b>")
                                    emtec_handle_general_exeption(e,logger=logger)
                                '''
                            else:
                                logger.debug(f"change NOT detected, session.prev_row is available")
                                message=Markup(f'<b>Grupo de Migración {Id} no fue modificado</b>')                        
                        else:
                            logger.audit ( '%s:UPD:%s' % (current_user.username,session['new_row'] ) )    
                            '''
                            try:
                                butler_notify_request(
                                    f"Solicitud {Id} Modificada por '{current_user.username}'",
                                    data=form.vmData,
                                    html_function=butler_output_request
                                    )
                                message=Markup(f"<b>Solicitud {Id} Modificada</b>")                            
                            except Exception as e:
                                message=Markup(f"<b>Solicitud {Id} Modificion excepcion: {str(e)}</b>")
                                emtec_handle_general_exception(e,logger=logger)                            
                            '''
                except Exception as e:
                    emtec_handle_general_exception(e,logger=logger)
                    db.session.rollback()
                    # GV db.session.close()
                    message=Markup(f'ERROR salvando Solicitud : {str(e)}')
                flash(message)
                # GV db.session.close()
                return redirect(url_for('.select_Request' ))
            # Eliminar -----------------------------------------------------
            elif   form.submit_Cancelar.data:
                # Aqui ajusta valor en BD
            # Retorno ------------------------------------------------------
            elif   form.submit_Retorno.data and session['data']['rolename'] == 'Requestor':
                message=Markup(f'<b>Modificaciones a Grupo de Migración {Id} descartadas</b>')
                flash(message)
                ## GV db.session.close()
                return redirect(url_for('.select_Request' ))
            # --------------------------------------------------------------
            # Approver's submits
            # --------------------------------------------------------------
            # Guardar ------------------------------------------------------ 
            elif   form.submit_Guardar.data:
                ## GV db.session.close()
                # Get Data from form
                # CC Id is a mix of distribution CC + Storage Type
                save_form(form,row,rox)
                #orm.vmData.update({'row':row,'rox':rox})
                form.vmData.update({'row':row})
                # Aqui ajusta valor en BD
                try:
                    session['new_row']   = str(row)
                    # Check for changes in request
                    if session.get('new_row') is not None:
                        #row.Status           = row.Status | REQUEST_REVIEWED
                        #row.Last_Status_Time = datetime.now()
                        #row.Approver_Id      = current_user.id
                        #if row.Comments is None: row.Comments = ''
                        #if len(row.Comments): row.Comments += '\n'
                        #row.Comments         = row.Comments + f"Solicitud modificada por '{current_user.username}' @ {datetime.now().strftime('%d/%m/%y %H:%M')}. "
                        db.session.merge(row)
                        #db.session.merge(rox)
                        saved_row=copy.copy(row)
                        #saved_rox=copy.copy(rox)
                        db.session.commit()
                        ## GV db.session.close()
                        if session.get('prev_row') is not None:
                            logger.audit ( '%s:OLD:%s' % (current_user.username,session['prev_row']) )
                        logger.audit ( '%s:UPD:%s' % (current_user.username,session['new_row'] ) )    
                        #orm.vmData.update({'row':row,'rox':rox})
                        form.vmData.update({'row':row})
                        form.vmData['row']=saved_row
                        form.vmData['rox']=saved_rox
                        butler_notify_request(
                            f'Solicitud {Id} Modificada por {current_user.username}',
                            data=form.vmData,
                            html_function=butler_output_request
                            )
                        message=Markup(f"<b>Grupo de Migración {Id} Modificado por '{current_user.username}'</b>")
                    else:
                        message=Markup(f"<b>grupo de Migración {Id} no Modificado'</b>")
                except Exception as e:
                    emtec_handle_general_exception(e,logger=logger)
                    db.session.rollback()
                    ## GV db.session.close()
                    message=Markup(f'<b>ERROR modificando Solicitud {Id}: {str(e)}</b>')
                ## GV db.session.close()
                flash(message)
                return redirect(url_for('.report_Request', Id = Id ))
            # Rechazar -----------------------------------------------------
            elif   form.submit_Rechazar.data:
                # Aqui ajusta valor en BD
                try:
                    row.Status           = REQUEST_REJECTED
                    row.Last_Status_Time = datetime.now()
                    row.Approver_Id      = current_user.id
                    session['new_row']   = str(row)+str(rox)
                    db.session.merge(row)
                    db.session.merge(rox)
                    saved_row=copy.copy(row)
                    saved_rox=copy.copy(rox)
                    db.session.commit()
                    ## GV db.session.close()
                    if session.get('prev_row') is not None:
                        logger.audit ( '%s:OLD:%s' % (current_user.username,session['prev_row']) )
                    logger.audit ( '%s:UPD:%s' % (current_user.username,session['new_row'] ) )    
                    form.vmData.update({'row':saved_row,'rox':saved_rox})
                    butler_notify_request(
                        f'Rechazada por {current_user.username}',
                        data=form.vmData,
                        html_function=butler_output_request
                        )
                    message=Markup('<b>Solicitud Rechazada</b>')
                except Exception as e:
                    emtec_handle_general_exception(e,logger=logger)
                    db.session.rollback()
                    ## GV db.session.close()
                    message=Markup(f'ERROR rechazando Solicitud : {str(e)}')
                ## GV db.session.close()
                flash(message)
                return redirect(url_for('.select_Request' ))
            # Aprobar ------------------------------------------------------
            elif   form.submit_Aprobar.data:
                save_form(form,row,rox)
                # Aqui ajusta valor en BD
                try:
                    row.Status           = REQUEST_APPROVED
                    row.Last_Status_Time = datetime.now()
                    row.Approver_Id      = current_user.id
                    session['new_row']   = str(row)+str(rox)
                    db.session.merge(row)
                    db.session.merge(rox)
                    saved_row=copy.copy(row)
                    saved_rox=copy.copy(rox)
                    db.session.commit()
                    ## GV db.session.close()
                    if session.get('prev_row') is not None:
                        logger.audit ( '%s:OLD:%s' % (current_user.username,session['prev_row']) )
                    logger.audit ( '%s:UPD:%s' % (current_user.username,session['new_row'] ) )    
                    form.vmData.update({'row':saved_row,'rox':saved_rox})
                    butler_notify_request(
                        f'Aprobada por {current_user.username}',
                        data=form.vmData,
                        html_function=butler_output_request
                        )
                    message=Markup(f'<b>Solicitud {Id} Aprobada</b>')
                except Exception as e:
                    emtec_handle_general_exception(e,logger=logger)
                    db.session.rollback()
                    ## GV db.session.close()
                    message=Markup(f'ERROR aprobando Solicitud {Id}: {str(e)}')
                ## GV db.session.close()
                flash(message)
                return redirect(url_for('.select_Request' ))
            # Other roles non action submits
            # Retorno ------------------------------------------------------
            elif   form.submit_Retorno.data:
                message=Markup(f'<b>Retorno sin acción ...</b>')
                flash(message)
                return redirect(url_for('.select_Request'))
            # Accion inesperada ERROR
            else:
                flash('<b>Form validado pero no sometido ???. Llamar al administrador del sistema</b>')
            return redirect(url_for('.select_Request'))

    logger.debug(f"{this()}: form is_submitted() = {form.is_submitted()}")
    logger.debug(f"{this()}: form errors         = {form.errors}")
    
    if form.is_submitted():
        logger.debug(f'{this()}: form is submitted !!!! wont load form !!!...')
        calculate_form(form,row,rox)
    else:
        # load actual data into form fields prior rendering
        logger.debug(f'{this()}: form is not submitted !!!! will load form !!!...')
        load_form(form,row,rox)
        form.vmData.update({'row':row,'rox':rox})
        logger.debug(f"{this()}: after load_form vmTopCC = {form.vmTopCC} vmCorporate = {form.vmCorporate.data} vmDepartment = {form.vmDepartment.data} vmCC={form.vmCC.data} vmType = {form.vmType.data}")
        logger.debug(f"{this()}: form.vmData['storage'] = {form.vmData.get('storage',None)}")
        logger.debug(f"{this()}: form.vmData['month']   = {form.vmData.get('month',None)}")

    logger.debug(f'{this()}: loading jinja globals functions ...')
    current_app.jinja_env.globals.update(get_request_status_description=get_request_status_description)
    current_app.jinja_env.globals.update(get_vm_resume=get_vm_resume)
    current_app.jinja_env.globals.update(has_status=has_status)
    current_app.jinja_env.globals.update(get_description=get_description)
    current_app.jinja_env.globals.update(object_to_html_table=object_to_html_table)
    session['prev_row'] = str(row)+str(rox)   
    session['is_new_row'] = False
    session['data']['prev_row'] = session['prev_row']
    session['data']['is_new_row'] = session['is_new_row']
    
    logger.debug(f"{this()}: session.prev_row       = {session.get('prev_row',None)}")
    logger.debug(f"{this()}: session.is_new_row     = {session.get('is_new_row',None)}")
    logger.trace(f"{this()}: form.vmData['storage'] = {form.vmData.get('storage',None)}")
    logger.trace(f"{this()}: form.vmData['month']   = {form.vmData.get('month',None)}")

    form.vmData.update(session.get('data'))

    logger.trace(f"{this()}: form.vmData['storage'] = {form.vmData.get('storage',None)}")
    logger.trace(f"{this()}: form.vmData['month']   = {form.vmData.get('month',None)}")
    # Fill vmData detail change to debug on new population 
    logger.trace(f'{this()}: form.vmData            = {pformat(form.vmData)}')
    
    logger.debug(f"{this()}: will render form with template 'request.html'...")
    # Will display all errors as Flask Flash messages ...
    for key in form.errors:
        for error in form.errors[key]:
            logger.error(f"{this()}: {key}: {error}")
            flash(f"{key}: {error}")

    form.vmData.update({'row':row,'rox':rox})
    # Patch lists for proper render
    if form.vmVlan0Name.choices is None: form.vmVlan0Name.choices=[]
    if form.vmVlan1Name.choices is None: form.vmVlan1Name.choices=[]
    if form.vmVlan2Name.choices is None: form.vmVlan2Name.choices=[]
    if form.vmVlan3Name.choices is None: form.vmVlan3Name.choices=[]
    logger.debug(f'PRE RENDER')
    logger.debug(f"form.vmCorporate.data    = {form.vmCorporate.data}")
    logger.debug(f"form.vmCorporate.choices = {pformat(form.vmCorporate.choices)}")
    logger.debug(f"form.vmDepartment.data   = {form.vmDepartment.data}")
    logger.debug(f"form.vmDepartment.choices= {pformat(form.vmDepartment.choices)}")
    logger.debug(f"form.vmCC.data           = {form.vmCC.data}")
    logger.debug(f"form.vmCC.choices        = {pformat(form.vmCC.choices)}")
    logger.debug(f"form.vmType.data         = {form.vmType.data}")
    logger.debug(f"form.vmType.choices      = {pformat(form.vmType.choices)}")
    logger.debug(f"form.vmDisk0Image.data   = {form.vmDisk0Image.data}")
    logger.debug(f"form.vmDisk0Image.choices= {pformat(form.vmDisk0Image.choices)}")
    logger.debug(f"form.vmCluster.data      = {form.vmCluster.data}")
    logger.debug(f"form.vmCluster.choices   = {pformat(form.vmCluster.choices)}")
    logger.debug(f"form.vmVlan0Name.data    = {form.vmVlan0Name.data}")
    logger.debug(f"form.vmVlan0Name.choices = {pformat(form.vmVlan0Name.choices)}")
    logger.debug(f"form.vmVlan1Name.data    = {form.vmVlan1Name.data}")
    logger.debug(f"form.vmVlan1Name.choices = {pformat(form.vmVlan1Name.choices)}")
    logger.debug(f"form.vmVlan2Name.data    = {form.vmVlan2Name.data}")
    logger.debug(f"form.vmVlan2Name.choices = {pformat(form.vmVlan2Name.choices)}")
    logger.debug(f"form.vmVlan3Name.data    = {form.vmVlan3Name.data}")
    logger.debug(f"form.vmVlan3Name.choices = {pformat(form.vmVlan3Name.choices)}")
    
    return render_template(
            'request.html',
            form = form,
            row = row,
            rox = rox,
            )
"""


@main.route('/forms/Migration/popup1', methods=['GET', 'POST'])
@login_required
def form_Migration_popup1():
    print(f"Will render template migration_popup1.html")
    return render_template('migration_popup1.html')

@main.route('/forms/Migration/popup2', methods=['GET', 'POST'])
@login_required
def form_Migration_popup2():
    mgId=request.args.get('mgId',None)
    print(f"Will render template migration_popup2.html with mgId={mgId}")
    return render_template('migration_popup2.html',mgId=mgId)

#@main.route('/forms/Migration/create_group', methods=['GET', 'POST'])
#@login_required
#ef forms_Migration_create_group():
def forms_Migration_create_group(form):
    logger.debug(f"{this()}: IN new name = {form.mgNewName.data}")
    #roupid   = request.form.get('groupid',0)
    #roupname = request.form.get('groupname',None)
    groupid   = form.mgId
    groupname = form.mgNewName.data
    logger.debug(f"{this()}: groupid={groupid} groupname={groupname}")
    # Aqui debe crear el grupo de migracion si no existe y 
    # llamar a forms/Migration con el nuevo Id
    mgs = db.session.query(Migration_Groups
            ).filter(Migration_Groups.Name == groupname
        ).all()
    #orm.mgNewName=groupname
    if mgs is None or len(mgs)==0:
        # GV its a new group then create one
        # creo nuevo grupo en BD y cargo ultimo id
        newmg = Migration_Groups(
                    Name=groupname
                    )
        logger.debug(f"{this()}: newmg={newmg}")
        db.session.add(newmg)
        db.session.commit()
        db.session.flush()
        db.session.refresh(newmg)
        logger.debug(f"{this()}: newmg={newmg}")
        logger.info(f"Creo grupo '{groupname}' ...")
        flash(f"Creo grupo '{groupname}' ...")
        form.mgNewId.data=newmg.MG_Id
    else:
        #lash(f"Grupo '{groupname}' ya existe","warning")
        logger.warning(f"Grupo '{groupname}' ya existe")
        logger.warning(f"Grupo '{mgs}' ya existe")
        for mg in mgs:
            if mg.Name == groupname:
                form.mgNewId.data=mg.MG_Id
                break
        logger.warning(f"Grupo '{groupname}' ya existe con id={form.mgNewId.data}")
        flash(f"Grupo '{groupname}' ya existe con id={form.mgNewId.data}")
    
    groupid   = form.mgNewId.data
    logger.debug(f"{this()}: OUT returns Group Id={groupid}")
    return groupid
    #return redirect(url_for('.forms_Migration',Id=groupid))

@main.route('/forms/Migration/add_vm_to_group', methods=['GET', 'POST'])
@login_required
def forms_Migration_add_vm_to_group():
    mgId = request.form.get('mgId',None)
    vmId = request.form.get('vmId',None)
    # Aqui debe crear el registro de vm asociado al grupo 
    # llamar a forms/Migration con el mismo mgId
    print(f"{this()}: Enter. mgId = {mgId} vmId={vmId}")
    return f"{this()}: Enter. mgId = {mgId} vmId={vmId}"

@main.route('/forms/Migration', methods=['GET', 'POST'])
@login_required
def forms_Migration():
    logger.debug(f"{this()}: Enter")
    logger.debug(f"{this()}: request = {request}")
    
    # DB Control -------------------------------------------------------
    try:    
        db.session.flush()
        db.session.commit()
    except Exception as e:
        logger.error(f"{this()}: DB Control Exception: {str(e)}. rolling back ...")
        try:
            db.session.rollback()
            logger.error(f"{this()}: Rolled back.")
        except Exception as e:
            logger.error(f"{this()}: While rolling back Exception{str(e)}.")
    # DB Control -------------------------------------------------------
    # Get Id if any
    Id  =  request.args.get('Id',0,type=int)
    
    # Setup initial data -----------------------------------------------
    # look for initial data in DB if any
    logger.debug(f'{this()}: load row from DB for Id={Id}')
    # GV 20210603 GV row =  Requests.query.filter(Requests.Id == Id).first()
    logger.debug(f"{this()}: Id = {Id}")
    if Id>0:
        logger.debug(f"getting specific group for Id={Id}")
        row =  db.session.query(Migration_Groups).filter(Migration_Groups.MG_Id == Id).first()
    else:
        logger.debug(f"{this()}: getting first group")
        row =  db.session.query(Migration_Groups).first()        
    logger.debug(f"{this()}: row = {row}")
    rox =  None
    if row is None:
        logger.debug(f'{this()}: row no existe inicializa objetos vacios')
        row=Migration_Groups()
        session['is_new_row']=True
        # GV set defaults
    else:
        # GV row ya está cargado
        pass
    if row is not None:
        logger.debug(f"{this()}: getting rows from Id={Id}")
        rox = db.session.query(Migration_Groups_VM).filter(Migration_Groups_VM.MG_Id == row.MG_Id).all()
    else:
        rox = None
    logger.debug(f"{this()}: row id  = {row.MG_Id}")
    logger.debug(f"{this()}: len rox = {len(rox)}")
        
    
    # GV Setup some session context data
    form = frm_migration_01()
    form.mgVms = []
    if row is not None:
        form.mgId=row.MG_Id
    for r in rox:
        form.mgVms.append(r)
    
    migration_group_list = get_migration_group_list()
    migration_group_options = [('','')]
    for mgid,name,origin,destiny in migration_group_list:
        migration_group_options.append((mgid,name))
    
    cluster_list = get_cluster_list()
    cluster_options = [('','')]
    for uuid,name,ip in cluster_list:
        cluster_options.append((uuid,name))
    
    
    form.mgName.choices    = migration_group_options
    form.mgOrigin.choices  = cluster_options
    form.mgDestiny.choices = cluster_options
    
    form.mgName.data    = row.MG_Id 
    form.mgOrigin.data  = row.Origin 
    form.mgDestiny.data = row.Destiny
        
    vm_list = {}
    for cluster_name in current_app.config.get('NUTANIX_CLUSTERS'):
        cluster  = current_app.config.get('NUTANIX_CLUSTERS').get(cluster_name)
        uuid     = cluster.get('uuid')
        vm_list.update({uuid:{'name':cluster_name,'vms':{}}})
        vm_list[uuid]['vms'] = {}
        try:
            response = nutanix_get_vm_list(
                host     = cluster.get('host'),
                username = cluster.get('username'),
                password = cluster.get('password')
                )
            if response.ok:
                for vm in response.json().get('entities'):
                    vm_list[uuid]['vms'].update({
                        vm.get('name'):{
                            'uuid'       :vm.get('uuid'),
                            'power_state':vm.get('power_state'),
                            }
                    })
            else:
                logger.error(f"{this()}: Invalid response {response}")
        except Exception as e:
            emtec_handle_general_exception(e,logger=logger)
            
    form.mgData = {
        'migration_group_list': migration_group_list,
        'cluster_list': cluster_list,
        'vm_list': vm_list,
    }
    
    form.mgOriginVms.choices = []
    logger.debug(f"{this()}: row.Origin={row.Origin} None? {row.Origin is None} type? {type(row.Origin)}")
    if row.Origin is not None and row.Origin != 'None':
        OriginVms = vm_list.get(row.Origin).get('vms')
        #print(f"OriginVms={OriginVms}")
        for vm in OriginVms:
            form.mgOriginVms.choices.append(
                (
                    OriginVms.get(vm).get('uuid'),
                    vm
                )
            )

    logger.debug(f"{this()}: len migration groups = {len(migration_group_list)}")
    logger.debug(f"{this()}: len clusters         = {len(cluster_list)}")
    logger.debug(f"{this()}: len vm_list          = {len(vm_list)}")
    logger.debug(f"{this()}: len origin vms       = {len(form.mgOriginVms.choices)}")
    
    # GV ***************************************************************

    logger.debug(f"{this()}: form.is_submitted() = {form.is_submitted()}")
    logger.debug(f"{this()}: form.errors         = {form.errors}")
    # Will check if all validated
    if form.is_submitted() and len(form.errors)==0:
        logger.debug(f"submit_Crear.data    = {form.submit_Crear.data}")
        logger.debug(f"submit_Agregar.data  = {form.submit_Agregar.data}")
        logger.debug(f"submit_Clonar.data   = {form.submit_Clonar.data}")
        logger.debug(f"submit_Salvar.data   = {form.submit_Salvar.data}")
        logger.debug(f"submit_Eliminar.data = {form.submit_Eliminar.data}")
        logger.debug(f"submit_Cancelar.data = {form.submit_Cancelar.data}")
        logger.debug(f"submit_Validar.data  = {form.submit_Validar.data}")
        logger.debug(f"submit_Migrar.data   = {form.submit_Migrar.data}")
        #ogger.debug(f"form dir             = {dir(form)}")
        logger.debug(f"form data            = {form.data}")
        logger.debug(f"form.mgNewName       = {form.mgNewName.data}")
        logger.debug(f"form.mgNewId         = {form.mgNewId.data}")
        if form.submit_Crear.data or form.submit_Agregar.data:
            if form.submit_Crear.data:
                logger.debug(f"{this()}: Create code here. then redirect")
                flash(f"Create code here. then redirect")
                groupid = forms_Migration_create_group(form)
                logger.debug(f"{this()}: groupid = {groupid}")
                logger.debug(f"{this()}: form.mgNewId.data = {form.mgNewId.data}")
                return redirect(url_for('.forms_Migration',Id=form.mgNewId.data))
            elif form.submit_Agregar.data:
                #lash(f"Add VM here. then redirect","warning")
                logger.debug(f"{this()}: Add VM here. then redirect")
                flash(f"{this()}: Add VM here. then redirect")
                return redirect(url_for('.forms_Migration',Id=form.mgId))
        else:
            logger.debug(f"{this()}: will call form.validate()")
            try:
                form.validate()
            except Exception as e:
                logger.error(f"form.validate exception: {str(e)}")
                logger.error(f"form.errors: {form.errors}")
                emtec_handle_general_exception(e,logger=logger)
            logger.debug(f"{this()}: return from form.validate() errors={len(form.errors)}")
            if len(form.errors) != 0:
                logger.debug(f"{this()}: form.is_submitted() = {form.is_submitted()} form.errors = {form.errors}")
            else:
                logger.debug(f"no errors will evaluate button pushed")
                
                # Gets sure vmData buffer is complete **********************
                #form.vmData.update(Get_data_context(current_app,db,mail,row.Id,current_user))
                # **********************************************************
                # ------------------------------------------------------
                # Basic Requestor's submits
                # ------------------------------------------------------
                # Clonar -----------------------------------------------
                if form.submit_Clonar.data:
                    alert(f"Clonar")
                # Salvar -----------------------------------------------
                elif form.submit_Salvar.data:
                    alert(f"Salvar")
                # Eliminar ---------------------------------------------
                elif form.submit_Eliminar.data:
                    alert(f"Eliminar")
                # Eliminar ---------------------------------------------
                elif form.submit_Cancelar.data:
                    alert(f"Cancelar")
                # Eliminar ---------------------------------------------
                elif form.submit_Validar.data:
                    alert(f"Validar")
                # Eliminar ---------------------------------------------
                elif form.submit_Migrar.data:
                    alert(f"Migrar")
                # ------------------------------------------------------
    else:
        logger.debug(f"form is not submitted")


    # GV ***************************************************************
    logger.debug(f"Will render template: migration.html")
    return render_template('migration.html',
            form = form
            )
            
# ======================================================================

# **********************************************************************
# NOTA Hay que ajustar esta funcion para trabajar bien con los rates !!!
# **********************************************************************

# 'Magic' argument ID is used to assign ID and mark body_only mode
# for exploit via external functions like 'notity_request'
"""@main.route('/report/Request', methods=['GET','POST'])
@login_required
def report_Request(ID=None):
    logger.debug(f'{this()}: Enter')
    # DB Control -------------------------------------------------------
    try:    
        db.session.flush()
        db.session.commit()
    except Exception as e:
        logger.error(f"{this()}: DB Control Exception: {str(e)}. rolling back ...")
        try:
            db.session.rollback()
            logger.error(f"{this()}: Rolled back.")
        except Exception as e:
            logger.error(f"{this()}: While rolling back Exception{str(e)}.")
    # DB Control -------------------------------------------------------
    if ID is not None:
        Id = ID
    else:
        Id  =  request.args.get('Id',default=0,type=int)


    row=rox=None
    data={}
    logger.debug(f'{this()}: inicializa listas de opciones ...') 
    
    data = Get_data_context(current_app,db,mail,Id,current_user)
    
    if Id > 0:
        # GV db.session.close()
        row = db.session.query(
                Requests,
                Nutanix_Prism_VM,
                Users,
                Cost_Centers,
                Request_Type
                ).join(Nutanix_Prism_VM,Nutanix_Prism_VM.Request_Id==Requests.Id
                ).join(Users,Users.id==Requests.User_Id
                ).join(Cost_Centers,Cost_Centers.CC_Id==Requests.CC_Id
                ).join(Request_Type,Request_Type.Id==Requests.Type
                ).filter(Requests.Id == Id
                ).first()
        # GV db.session.close()
        data['status_description'] = get_request_status_description(row.Requests.Status)
        data['storage_type']       = row.Nutanix_Prism_VM.disk_type
        for i in range(12):
            if i == 0:
                uuid = getattr(row.Nutanix_Prism_VM,f'disk_{i}_image')
                data['disk_images'].append(get_description('images',uuid,data))
            data['storage'] += getattr(row.Nutanix_Prism_VM,f'disk_{i}_size')
        data['month'] = get_monthly_rate(row.Requests,row.Nutanix_Prism_VM)
    # will render for screen or body only depending on call
    current_app.jinja_env.globals.update(get_request_status_description=get_request_status_description)
    current_app.jinja_env.globals.update(get_vm_resume=get_vm_resume)
    current_app.jinja_env.globals.update(has_status=has_status)
    current_app.jinja_env.globals.update(get_description=get_description)
    current_app.jinja_env.globals.update(object_to_html_table=object_to_html_table)
    if ID is None:
        return render_template(
                'report_request.html',
                data = data,
                row  = row,
        )
    else:
        return render_template(
                'report_request.html',
                data      = data,
                row       = row,
                body_only = True
        )
"""
# EOF ******************************************************************
