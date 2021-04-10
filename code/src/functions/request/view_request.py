# ======================================================================
# BUTLER REQUEST ROUTES
# View for General request Edition
# (c) Sertechno 2020
# GLVH @ 2020-11-06
# ======================================================================
import jinja2
from pprint             import pformat
from sqlalchemy         import desc
from emtec.debug        import *
from emtec.butler.forms import frm_request

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
    query = db.session.query(
                requests.Id,
                requests.Status,
                requests.Last_Status_Time,
                nutanix_prism_vm.vm_name,
                Users.username,
                Cost_Centers.CC_Description#,
                ).join(nutanix_prism_vm,
                    nutanix_prism_vm.Request_Id == requests.Id
                ).join(Users,
                    Users.id == requests.User_Id
                ).join(Cost_Centers,
                    Cost_Centers.CC_Id == requests.CC_Id
                )
    # Various filters to conditionaly implement
    # Filter by REQUESTOR, requestor can not see others user's requests
    if current_user.role_id == ROLE_REQUESTOR:
        query = query.filter(requests.User_Id == current_user.id)
    # Select requests with "Status" Flag on, as per request argument
    if Status is not None:
        # See specific bitwise operator use for comparison
        # This is an AND comparison between:
        # request.Status AND Status <> request.Status & Status
        query = query.filter(requests.Status.op("&")(Status))
    if User_Id is not None:
        if User_Id and current_user.role_id != ROLE_REQUESTOR:
            query = query.filter(requests.User_Id == User_Id)
        else:
            query = query.filter(requests.User_Id == current_user.id)
    # Will allways order by time, newer first
    query = query.order_by(desc(requests.Last_Status_Time))
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
    return render_template('select_request.html',rows=rows)
        
@main.route('/forms/Request', methods=['GET', 'POST'])
@login_required
def forms_Request():
    logger.debug(f'{this()}: Enter')
    logger.debug(f'{this()}: logger.handlers = {logger.handlers}')
    
    # Get Id if any
    Id  =  request.args.get('Id',0,type=int)
    # DB Control
    try:    db.session.commit()
    except: db.session.rollback()
    # Setup initial data -----------------------------------------------
    # look for initial data in DB if any
    logger.debug(f'{this()}: load row from DB for Id={Id}')
    row =  requests.query.filter(requests.Id == Id).first()
    if row is None:
        logger.debug(f'{this()}: row no existe inicializa objetos vacios')
        row=requests()
        rox=nutanix_prism_vm()
        session['is_new_row']=True
    else:
        logger.debug(f'{this()}: load rox from DB for row.Id={row.Id}')
        rox =  nutanix_prism_vm.query.filter(nutanix_prism_vm.Request_Id == row.Id).first()
        if rox is None:
            logger.debug(f'{this()}: rox no existe inicializa objeto vacio')
            rox=nutanix_prism_vm()

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
        
    if current_user.role_id in [ROLE_REQUESTOR]:
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
    form = frm_request()
    form.logger  = logger
    form.vmTopCC = session['data']['top_cost_center_id']
    form.vmTopCCCode = session['data']['top_cost_center_code']
    form.vmDebug.data = session['data']['debug']
    
    # ******************************************************************
    
    # Inicializacion de datos debe reemplazarse por las rutinas de
    # poblamiento de opciones principalmente
    # ------------------------------------------------------------------

    # OJO Control con falla de configuracion/archivo mientras default tonto
    
    
    top_cost_center_code = current_app.config['BUTLER_TOP_COST_CENTER']
    top_cost_center_id = db.session.query(Cost_Centers.CC_Id
                            ).filter(
                                Cost_Centers.CC_Code == top_cost_center_code
                            ).scalar()
    #all_cc_list = get_cost_centers(top_cost_center_code)
    all_cc_list = get_cost_centers_fast(top_cost_center_id)
        
    logger.debug(f'{this()}: inicializa listas de opciones ...') 
    
    corporate_list  = get_corporate_list(session['data']['top_cost_center_code'],all_cc_list)
    department_list,gd_map = get_department_list(session['data']['top_cost_center_code'],all_cc_list)
    cc_list         = get_cc_list(session['data']['top_cost_center_code'],all_cc_list)
    type_list       = get_type_list(session['data']['top_cost_center_code'],all_cc_list)
    image_list      = get_image_list()
    cluster_list    = get_cluster_list()
    project_list    = get_project_list()
    category_list   = get_category_list()
    subnet_list     = get_project_subnet_list()
    subnet_options  = get_project_subnet_options()
    user_list       = get_user_list()
    rates_list      = get_db_rates()
    logger.debug(f"{this()}: subnet_list = {subnet_list}")
    logger.debug(f"{this()}: subnet_options = {subnet_options}")

    # Javascript/JQuery scripts array initialization -------------------
    scripts = []
    for template in Script_Templates:
        script = jinja2.Template(template
                        ).render(
                            subnet_options = subnet_options,
                            rates          = rates_list,
                            gd_map         = gd_map
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
    logger.debug(f"{this()}: updating session data ...")
    session['data'].update({'clusters'      : cluster_list})
    session['data'].update({'projects'      : project_list})
    session['data'].update({'categories'    : category_list})
    session['data'].update({'subnets'       : get_subnet_list()})

    session['data'].update({'corporates'    : corporate_list })
    session['data'].update({'departments'   : department_list })
    session['data'].update({'ccs'           : cc_list })
    session['data'].update({'types'         : type_list })
    session['data'].update({'gd_map'        : gd_map })

    session['data'].update({'users'         : user_list})
    session['data'].update({'subnet_options': get_project_subnet_options()})
    session['data'].update({'rates'         : rates_list})
    # Populates vm Data with all captured session data -----------------
    form.vmData.update(session['data'])
    
    logger.debug(f"session['data']=\n{pformat(session['data'])}")

    vmCorporate_choices = []
    vmDepartment_choices = []
    vmCC_choices         = []
    vmType_choices       = []
    vmDiskImage_choices  = [('','')] # An empty option is valid in this context
    vmCluster_choices    = []
    vmProject_choices    = []
    vmCategory_choices   = []
    vmSubnet_choices     = []
    
    for corporate in corporate_list:
        vmCorporate_choices.append(corporate)
    for department in department_list:
        vmDepartment_choices.append(department)
    for cc in cc_list:
        vmCC_choices.append(cc)
    vmType_choices = session['data']['types']
    for image in image_list:
        vmDiskImage_choices.append(
            (image.uuid,
            f'{image.name} ({int(image.vm_disk_size_gib)} GB)')
            )
    # Load Select Fields Choices and codes -----------------------------
    form.vmCorporate.choices   = vmCorporate_choices
    form.vmDepartment.choices   = vmDepartment_choices
    form.vmCC.choices   = vmCC_choices
    form.vmType.choices = vmType_choices
    form.vmCluster.choices = cluster_list
    form.vmProject.choices = project_list
    form.vmCategory.choices = category_list
    form.vmSubnet.choices = subnet_list
    subnet_list_other=[('','')]+subnet_list
    logger.debug(f"{this()}: subnet_list   ={pformat(subnet_list)}")
    logger.debug(f"{this()}: subnet_options={pformat(subnet_options)}")
    logger.debug(f"{this()}: subnet_list_other={pformat(subnet_list_other)}")
    for i in range(3):
        setattr(getattr(form,f'vmNic{i}Vlan'),'choices',subnet_list_other)
        logger.trace(f"{this()}: vmNic{i}Vlan.choices = {getattr(form,f'vmNic{i}Vlan').choices}")
        
    for i in range(12):
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
            emtec_handle_general_exception(e,logger=logger)
        logger.debug(f"{this()}: return from form.validate()")
        if len(form.errors) != 0:
            logger.warning(f"{this()}: form.is_submitted()={form.is_submitted()} form.errors={form.errors}")
            print(f"{this()}: form.is_submitted()={form.is_submitted()} form.errors={form.errors}")
        else:
            logger.debug(f"no errors will evaluate button pushed")
            # --------------------------------------------------------------
            # Basic Requestor's submits
            # --------------------------------------------------------------
            # Guardar ------------------------------------------------------
            if     form.submit_Guardar.data and row.Status < BUTLER_STATUS['REQUESTED']:
                # Get data from context ------------------------------------
                row.Id               = Id     
                row.Type             = 1     # Nutanix VM 
                row.User_Id          = current_user.id 
                rox.Request_Id       = row.Id 
                save_form(form,row,rox)
                # Aqui ajusta valor en BD ----------------------------------
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
                            func.max(requests.Id)
                            ).filter(requests.User_Id == current_user.id
                            ).scalar()
                        Id = rox.Request_Id
                        db.session.add(rox)
                        session['new_row']    = str(row)+str(rox)
                    else:
                        session['is_new_row'] = False
                        session['new_row']    = str(row)+str(rox)
                        db.session.merge(row)
                        db.session.merge(rox)
                    db.session.commit()
                    ## GV db.session.close()
                    if session['is_new_row']==True:
                        logger.audit ( '%s:NEW:%s' % (current_user.username,session['new_row'] ) )
                        notify_request(Id,f'Creada por {current_user.username}',form.vmData)
                        message=Markup(f'<b>Nueva solicitud {Id} creada OK</b>')
                    else:
                        if session['new_row'] != session['prev_row']:
                            logger.audit ( '%s:OLD:%s' % (current_user.username,session['prev_row']) )
                            logger.audit ( '%s:UPD:%s' % (current_user.username,session['new_row'] ) )    
                            notify_request(Id,f"Solicitud {Id} Modificada por '{current_user.username}'",form.vmData)
                            message=Markup(f"<b>Solicitud {Id} Modificada</b>")
                        else:
                            message=Markup(f'<b>Solicitud {Id} no fue modificada</b>')                        
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
                    logger.audit ( '%s:OLD:%s' % (current_user.username,session['prev_row']) )
                    logger.audit ( '%s:UPD:%s' % (current_user.username,session['new_row'] ) )    
                    notify_request(Id,f'Completada por {current_user.username}. En Proceso de aprobación.',form.vmData)
                    message=Markup('<b>Solicitud en Aprobacion</b>')
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
                        row.Comments = f"Solicitud Cancelada/Eliminada por usuario '{current_user.username}'. Estado Final."
                        if current_user.role_id == ROLE_APPROVER:
                            row.Approver_Id = current_user.id
                        session['new_row']    = str(row)+str(rox)
                        db.session.merge(row)
                        db.session.merge(rox)
                    db.session.commit()
                    ## GV db.session.close()
                    logger.audit ( '%s:OLD:%s' % (current_user.username,session['prev_row']) )
                    logger.audit ( '%s:UPD:%s' % (current_user.username,session['new_row'] ) )    
                    notify_request(Id,f'Cancelada por {current_user.username}',form.vmData)
                    message=Markup(f'<b>Solicitud {Id} Cancelada</b>')
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
                # Aqui ajusta valor en BD
                try:
                    session['new_row']   = str(row)+str(rox)
                    # Check for changes in request
                    if session['new_row'] != session['prev_row']:
                        row.Status           = row.Status | REQUEST_REVIEWED
                        row.Last_Status_Time = datetime.now()
                        row.Approver_Id      = current_user.id
                        if row.Comments is None: row.Comments = ''
                        if len(row.Comments): row.Comments += '\n'
                        row.Comments         = row.Comments + f"Solicitud modificada por '{current_user.username}' @ {datetime.now().strftime('%d/%m/%y %H:%M')}. "
                        db.session.merge(row)
                        db.session.merge(rox)
                        db.session.commit()
                        ## GV db.session.close()
                        logger.audit ( '%s:OLD:%s' % (current_user.username,session['prev_row']) )
                        logger.audit ( '%s:UPD:%s' % (current_user.username,session['new_row'] ) )    
                        notify_request(Id,f'Solicitud {Id} Modificada por {current_user.username}',form.vmData)
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
                    db.session.commit()
                    ## GV db.session.close()
                    logger.audit ( '%s:OLD:%s' % (current_user.username,session['prev_row']) )
                    logger.audit ( '%s:UPD:%s' % (current_user.username,session['new_row'] ) )    
                    notify_request(Id,f'Rechazada por {current_user.username}',form.vmData)
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
                # Aqui ajusta valor en BD
                try:
                    row.Status           = REQUEST_APPROVED
                    row.Last_Status_Time = datetime.now()
                    row.Approver_Id      = current_user.id
                    session['new_row']   = str(row)+str(rox)
                    db.session.merge(row)
                    db.session.merge(rox)
                    db.session.commit()
                    ## GV db.session.close()
                    logger.audit ( '%s:OLD:%s' % (current_user.username,session['prev_row']) )
                    logger.audit ( '%s:UPD:%s' % (current_user.username,session['new_row'] ) )    
                    notify_request(Id,f'Aprobada por {current_user.username}',form.vmData)
                    message=Markup('<b>Solicitud {Id} Aprobada</b>')
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
        #print(dir(form))
        logger.debug(f'{this()}: form is not submitted !!!! will load form !!!...')
        load_form(form,row,rox)
        logger.debug(f"{this()}: after load_formvmTopCC={form.vmTopCC} vmCorporate={form.vmCorporate.data} vmDepartment={form.vmDepartment.data} vmCC={form.vmCC.data} vmType={form.vmType.data}")
        logger.debug(f"{this()}: form.vmData['storage']={form.vmData.get('storage',None)}")
        logger.debug(f"{this()}: form.vmData['month']  ={form.vmData.get('month',None)}")
    logger.debug(f'{this()}: loading jinja globals functions ...')
    current_app.jinja_env.globals.update(get_request_status_description=get_request_status_description)
    current_app.jinja_env.globals.update(get_vm_resume=get_vm_resume)
    current_app.jinja_env.globals.update(has_status=has_status)
    current_app.jinja_env.globals.update(get_description=get_description)
    session['prev_row'] = str(row)+str(rox)   
    session['is_new_row'] = False
    logger.trace(f"{this()}: form.vmData['storage']={form.vmData.get('storage',None)}")
    logger.trace(f"{this()}: form.vmData['month']  ={form.vmData.get('month',None)}")
    form.vmData.update(session['data'])
    logger.trace(f"{this()}: form.vmData['storage']={form.vmData.get('storage',None)}")
    logger.trace(f"{this()}: form.vmData['month']  ={form.vmData.get('month',None)}")
    # Fill vmData detail change to debug on new population 
    logger.trace(f'{this()}: form.vmData = {pformat(form.vmData)}')
    logger.trace(f"{this()}: form.vmSubnet={form.vmSubnet}")
    logger.trace(f"{this()}: form.vmNic0Vlan={form.vmNic0Vlan}")
    logger.trace(f"{this()}: form.vmNic1Vlan={form.vmNic1Vlan}")
    logger.trace(f"{this()}: form.vmNic2Vlan={form.vmNic2Vlan}")
    
    logger.debug(f'{this()}: will render form ...')
    # Will display all errors as Flask Flash messages ...
    for key in form.errors:
        for error in form.errors[key]:
            logger.error(f"{this()}: {key}: {error}")
            flash(f"{key}: {error}")
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
    if ID is not None:
        Id = ID
    else:
        Id  =  request.args.get('Id',default=0,type=int)

    row=rox=None
    data={}
    
    image_list          = get_image_list()
    vmDiskImage_choices = [('','')]
    
    for image in image_list:
        vmDiskImage_choices.append(
            (image.uuid,
            f'{image.name} ({int(image.vm_disk_size_gib)} GB)')
            )
    cc_top_id           = get_cost_center(current_app.config['BUTLER_TOP_COST_CENTER']).CC_Id
    data['role']        = current_user.role_id
    data['roles']       = ROLES
    data['status']      = BUTLER_STATUS
    data['debug']       = current_app.config['DEBUG']
    data['clusters']    = get_cluster_list()
    data['projects']    = get_project_list()
    data['categories']  = get_category_list()
    data['subnets']     = get_subnet_list()
    data['users']       = get_user_list()
    data['images']      = get_image_list()
    data['corporates']  = get_corporate_list(cc_top_id)
    data['departments'] = get_department_list(cc_top_id)
    data['ccs']         = get_cc_list(cc_top_id)
    data['types']       = get_type_list(cc_top_id)
    data['month']       = 0
    data['status_description'] = ''
    data['disk_images']        = []
    data['month']              = 0
    data['storage']            = 0
    data['storage_type']       = 0
    
    if Id > 0:
        # GV db.session.close()
        row = db.session.query(
                requests,
                nutanix_prism_vm,
                Users,
                Cost_Centers,
                request_type
                ).join(nutanix_prism_vm,nutanix_prism_vm.Request_Id==requests.Id
                ).join(Users,Users.id==requests.User_Id
                ).join(Cost_Centers,Cost_Centers.CC_Id==requests.CC_Id
                ).join(request_type,request_type.Id==requests.Type
                ).filter(requests.Id == Id
                ).first()
        # GV db.session.close()
        data['status_description'] = get_request_status_description(row[0].Status)
        data['storage_type']       = row[1].disk_type
        # Gets Monthly Rates as per Rates Table
        #rates = get_rates()
        for i in range(12):
            uuid = getattr(row.nutanix_prism_vm,f'disk_{i}_image')
            data['disk_images'].append(get_description('images',uuid,data))
            data['storage'] += getattr(row.nutanix_prism_vm,f'disk_{i}_size')
        data['month'] = get_monthly_rate(row.requests,row.nutanix_prism_vm)
    # will render for screen or body only depending on call
    current_app.jinja_env.globals.update(get_request_status_description=get_request_status_description)
    current_app.jinja_env.globals.update(get_vm_resume=get_vm_resume)
    current_app.jinja_env.globals.update(has_status=has_status)
    current_app.jinja_env.globals.update(get_description=get_description)
    
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
