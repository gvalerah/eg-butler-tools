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
from emtec.butler.forms     import frm_request,form_log
from emtec.butler.functions import *

# Templates will reside on view_request_template.py
# Functions will reside on view_request_functions.py

# Support functions

# View functions are in view_request_functions.py  
    # ------------------------------------------------------------------

@main.route('/select/Request', methods=['GET', 'POST'])
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

import  pandas
from    pandas.io.json          import json_normalize
from    flask                   import send_file
import tempfile

@main.route('/export/Request', methods=['GET', 'POST'])
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
        
@main.route('/forms/Request', methods=['GET', 'POST'])
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
    # 20210603 GV row =  Requests.query.filter(Requests.Id == Id).first()
    row =  db.session.query(Requests).filter(Requests.Id == Id).first()
    if row is None:
        logger.debug(f'{this()}: row no existe inicializa objetos vacios')
        row=Requests()
        rox=Nutanix_Prism_VM()
        session['is_new_row']=True
        # set defaults
        row.CC_Id         = current_app.config.get('BUTLER_DEFAULT_COST_CENTER')
        rox.vm_drp        = True
        rox.vm_drp_remote = True
        rox.vm_cdrom      = True
    else:
        logger.debug(f'{this()}: load rox from DB for row.Id={row.Id}')
        rox =  db.session.query(Nutanix_Prism_VM).filter(Nutanix_Prism_VM.Request_Id == row.Id).first()
        if rox is None:
            logger.debug(f'{this()}: rox no existe inicializa objeto vacio')
            rox=Nutanix_Prism_VM()
            # set defaults
            rox.vm_drp        = True
            rox.vm_drp_remote = True
            rox.vm_cdrom      = True

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
    cc = get_cost_center(json.loads(session['data']['config']['BUTLER_TOP_COST_CENTER']))
    logger.debug(f"{this()}: session['data']['config']['BUTLER_TOP_COST_CENTER']={session['data']['config']['BUTLER_TOP_COST_CENTER']}")
    logger.debug(f"{this()}: cc={cc}")
    if cc is not None:
        session['data']['top_cost_center_id'] = cc.CC_Id
        session['data']['top_cost_center_code'] = cc.CC_Code
        
    if   current_user.role_id in [ROLE_REQUESTOR]:
        session['data']['rolename'] = 'Requestor'
    elif current_user.role_id in [ROLE_APPROVER]:
        session['data']['rolename'] = 'Approver'
    elif current_user.role_id in [ROLE_VIEWER]:
        session['data']['rolename'] = 'Viewer'
    elif current_user.role_id in [ROLE_AUDITOR]:
        session['data']['rolename'] = 'Auditor'
    else:
        session['data']['rolename'] = 'Other'
        
    # ------------------------------------------------------------------
    # ******************************************************************
    # Instance form
    logger.debug(f'{this()}: instance new form <= frm_request')
    form              = frm_request()
    form.logger       = logger
    form.vmTopCC      = session['data']['top_cost_center_id']
    form.vmTopCCCode  = session['data']['top_cost_center_code']
    form.vmDebug.data = session['data']['debug']
    
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
    
    logger.trace(f"session['data']=\n{pformat(session['data'])}")

    # Javascript/JQuery scripts array initialization -------------------
    scripts = []
    for template in Script_Templates:
        logger.trace(f"rendering template={template} ...")
        script = jinja2.Template(template
                        ).render(
                            subnet_options     = data.get('subnet_options'),
                            rates              = data.get('rates'),
                            gd_map             = data.get('gd_map'),
                            environments_codes = data.get('environments_codes')
                        )
        scripts.append(Markup(script))
    # Updates JS/JQ functions/events file as per actual DATA -----------
    # Alert include temporary process id for concurrency of sessions ---
    jspath = f"{current_app.root_path}/static/js"
    jsfile = f"{jspath}/butler.requests.{current_user.id}.js"
    logger.debug(f"{this()}: ACTUALIZANDO : {jsfile} ...")
    with open(jsfile,'w') as fp:
        fp.write(f"// {jsfile}{datetime.now()}\n")
        fp.write(f"// updated: {datetime.now()}\n")
        for script in scripts:
            fp.write(f"{script}\n")
        fp.write(f"// {jsfile}:EOF\n")
    # ------------------------------------------------------------------

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
    form.vmCluster.choices    = data.get('clusters')
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
            form_log(form,logger.debug)
            
            # Gets sure vmData buffer is complete **********************
            form.vmData.update(Get_data_context(current_app,db,mail,row.Id,current_user))
            # **********************************************************
            # ----------------------------------------------------------
            # Basic Requestor's submits
            # ----------------------------------------------------------
            # Guardar --------------------------------------------------
            if     form.submit_Guardar.data and row.Status < BUTLER_STATUS['REQUESTED']:
                # Get data from context --------------------------------
                row.Id         = Id     
                row.Type       = 1     # Nutanix VM 
                row.User_Id    = current_user.id 
                rox.Request_Id = row.Id 
                save_form(form,row,rox)
                form.vmData.update({'row':row,'rox':rox})
                # Aqui ajusta valor en BD ------------------------------
                try:
                    ## GV db.session.close()
                    if row.Id == 0: 
                        row.Status            = REQUEST_CREATED
                        row.Creation_Time     = datetime.now()
                        row.Last_Status_Time  = row.Creation_Time
                        session['is_new_row'] = True
                        db.session.add(row)
                        db.session.flush()
                        # specific query to get last id, other approach seem
                        # not to work
                        rox.Request_Id = db.session.query(
                            func.max(Requests.Id)
                            ).filter(Requests.User_Id == current_user.id
                            ).scalar()
                        Id = rox.Request_Id
                        db.session.add(rox)
                        session['new_row']    = str(row)+str(rox)
                    else:
                        session['is_new_row'] = False
                        session['new_row']    = str(row)+str(rox)
                        db.session.merge(row)
                        db.session.merge(rox)
                    saved_row=copy.copy(row)
                    saved_rox=copy.copy(rox)
                    db.session.commit()
                    ## GV db.session.close()
                    if session['is_new_row']==True:
                        form.vmData['row']=saved_row
                        form.vmData['rox']=saved_rox
                        logger.audit ( '%s:NEW:%s' % (current_user.username,session['new_row'] ) )
                        try:
                            butler_notify_request(
                                f'Creada por {current_user.username}',
                                data=form.vmData,
                                html_function=butler_output_request
                                )
                            message=Markup(f'<b>Nueva solicitud {Id} creada OK</b>')
                        except Exception as e:
                            message=Markup(f'<b>Nueva solicitud {Id} creacion excepcion: {str(e)}</b>')
                            emtec_handle_general_exception(e,logger=logger)
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
                                form.vmData['rox']=saved_rox
                                logger.audit ( '%s:OLD:%s' % (current_user.username,session['prev_row']) )
                                logger.audit ( '%s:UPD:%s' % (current_user.username,session['new_row'] ) )    
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
                            else:
                                logger.debug(f"change NOT detected, session.prev_row is available")
                                message=Markup(f'<b>Solicitud {Id} no fue modificada</b>')                        
                        else:
                            logger.audit ( '%s:UPD:%s' % (current_user.username,session['new_row'] ) )    
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
                except Exception as e:
                    emtec_handle_general_exception(e,logger=logger)
                    db.session.rollback()
                    ## GV db.session.close()
                    message=Markup(f'ERROR salvando Solicitud : {str(e)}')
                flash(message)
                ## GV db.session.close()
                return redirect(url_for('.select_Request' ))
            # Completado ---------------------------------------------------
            elif   form.submit_Completado.data:
                save_form(form,row,rox)
                form.vmData.update({'row':row,'rox':rox})
                saved_row=copy.copy(row)
                saved_rox=copy.copy(rox)
                # Aqui ajusta valor en BD
                try:
                    if row.Id > 0:
                        row.Status           = REQUEST_REQUESTED
                        row.Last_Status_Time = datetime.now()
                        session['new_row']   = str(row)+str(rox)
                        Id = row.Id    
                        db.session.merge(row)
                        db.session.merge(rox)
                    db.session.commit()
                    ## GV db.session.close()
                    if session.get('prev_row') is not None:
                        logger.audit ( '%s:OLD:%s' % (current_user.username,session['prev_row']) )
                    logger.audit ( '%s:UPD:%s' % (current_user.username,session['new_row'] ) )    
                    form.vmData['row']=saved_row
                    form.vmData['rox']=saved_rox
                    try:
                        butler_notify_request(
                            f'Completada por {current_user.username}. En Proceso de aprobación.',
                            data=form.vmData,
                            html_function=butler_output_request
                            )
                        message=Markup(f'<b>Solicitud {saved_rox.Request_Id} en Aprobacion</b>')
                    except Exception as e:
                        message=Markup(f'<b>Solicitud {saved_rox.Request_Id} en Aprobacion excepcion:{str(e)}</b>')
                        emtec_handle_general_exception(e,logger=logger)
                except Exception as e:
                    emtec_handle_general_exception(e,logger=logger)
                    db.session.rollback()
                    ## GV db.session.close()
                    message=Markup(f'ERROR enviando Solicitud : {str(e)}')
                flash(message)
                ## GV db.session.close()
                return redirect(url_for('.select_Request' ))
            # Eliminar -----------------------------------------------------
            elif   form.submit_Cancelar.data:
                # Aqui ajusta valor en BD
                try:
                    if row.Id > 0:
                        row.Status           = REQUEST_CANCELED
                        row.Last_Status_Time = datetime.now()
                        if row.Comments is None: row.Comments = ''
                        if len(row.Comments): row.Comments += '\n'
                        row.Comments = row.Comments + f"Solicitud Cancelada/Eliminada por usuario '{current_user.username}'. Estado Final."
                        if current_user.role_id == ROLE_APPROVER:
                            row.Approver_Id = current_user.id
                        session['new_row']    = str(row)+str(rox)
                        db.session.merge(row)
                        db.session.merge(rox)
                    db.session.commit()
                    ## GV db.session.close()
                    if session.get('prev_row') is not None:
                        logger.audit ( '%s:OLD:%s' % (current_user.username,session['prev_row']) )
                    logger.audit ( '%s:UPD:%s' % (current_user.username,session['new_row'] ) )    
                    form.vmData.update({'row':row,'rox':rox})
                    try:
                        butler_notify_request(
                            f'Cancelada por {current_user.username}',
                            data=form.vmData,
                            html_function=butler_output_request
                            )
                        message=Markup(f'<b>Solicitud {Id} Cancelada</b>')
                    except Exception as e:
                        message=Markup(f'<b>Solicitud {Id} Cancelacion excepcion: {str(e)}</b>')
                        emtec_handle_general_exception(e,logger=logger)
                except Exception as e:
                    emtec_handle_general_exception(e,logger=logger)
                    db.session.rollback()
                    message=Markup(f'<b>ERROR eliminando Solicitud {Id}: {str(e)}</b>')
                flash(message)
                ## GV db.session.close()
                return redirect(url_for('.select_Request' ))
            # Retorno ------------------------------------------------------
            elif   form.submit_Retorno.data and session['data']['rolename'] == 'Requestor':
                message=Markup(f'<b>Modificaciones a Solicitud {Id} descartadas</b>')
                flash(message)
                ## GV db.session.close()
                return redirect(url_for('.select_Request' ))
            # --------------------------------------------------------------
            # Approver's submits
            # --------------------------------------------------------------
            # Guardar ------------------------------------------------------ 
            elif   form.submit_Guardar.data and row.Status >= BUTLER_STATUS['REQUESTED']:
                ## GV db.session.close()
                # Get Data from form
                # CC Id is a mix of distribution CC + Storage Type
                save_form(form,row,rox)
                form.vmData.update({'row':row,'rox':rox})
                # Aqui ajusta valor en BD
                try:
                    session['new_row']   = str(row)+str(rox)
                    # Check for changes in request
                    if session.get('new_row') is not None:
                        row.Status           = row.Status | REQUEST_REVIEWED
                        row.Last_Status_Time = datetime.now()
                        row.Approver_Id      = current_user.id
                        if row.Comments is None: row.Comments = ''
                        if len(row.Comments): row.Comments += '\n'
                        row.Comments         = row.Comments + f"Solicitud modificada por '{current_user.username}' @ {datetime.now().strftime('%d/%m/%y %H:%M')}. "
                        db.session.merge(row)
                        db.session.merge(rox)
                        saved_row=copy.copy(row)
                        saved_rox=copy.copy(rox)
                        db.session.commit()
                        ## GV db.session.close()
                        if session.get('prev_row') is not None:
                            logger.audit ( '%s:OLD:%s' % (current_user.username,session['prev_row']) )
                        logger.audit ( '%s:UPD:%s' % (current_user.username,session['new_row'] ) )    
                        form.vmData.update({'row':row,'rox':rox})
                        form.vmData['row']=saved_row
                        form.vmData['rox']=saved_rox
                        butler_notify_request(
                            f'Solicitud {Id} Modificada por {current_user.username}',
                            data=form.vmData,
                            html_function=butler_output_request
                            )
                        message=Markup(f"<b>Solicitud {Id} Modificada por '{current_user.username}'</b>")
                    else:
                        message=Markup(f"<b>Solicitud {Id} no Modificada'</b>")
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

# ======================================================================

# **********************************************************************
# NOTA Hay que ajustar esta funcion para trabajar bien con los rates !!!
# **********************************************************************

# 'Magic' argument ID is used to assign ID and mark body_only mode
# for exploit via external functions like 'notity_request'
@main.route('/report/Request', methods=['GET','POST'])
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
# EOF ******************************************************************
