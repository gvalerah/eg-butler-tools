# GV ===================================================================
# GV Main Views Header
# GV source file name: views_py_header.py
# GV Static Header File. 
# GV GLVH 2020-10-11
# GV -------------------------------------------------------------------
from datetime       import datetime
from time           import strftime
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
from flask_babel    import gettext
from flask_babel    import lazy_gettext

from .              import main

from ..             import db
from ..             import mail
from ..             import logger
from ..             import babel

from emtec.debug    import *

# add to you main app code
@babel.localeselector
def get_locale():
    try:
        if current_app.config.CURRENT_LANGUAGE is not None:
            language =  current_app.config.CURRENT_LANGUAGE
        else:
            language =  request.accept_languages.best_match(
                            current_app.config.LANGUAGES.keys()
                        )
    except Exception as e:
        print(f"get_locale: exception: {str(e)}")
        language = 'en'
    return language

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

""" GV Application decorators for routes """
""" GV Decorators specify main routes to be handled by Butler Solution """

""" GV Include JINJA 2 global functions/filters
"""



@main.route('/', methods=['GET', 'POST'])
def index():
    logger.debug(f"@main.route('/', methods=['GET', 'POST'])")
    try: logger.debug(f'current_user={current_user}')
    except Exception as e: logger.debug(f'exception={str(e)}')
    # GV Espera a capitulo 3 para mejorar procedimiento de respuesta, hard coding mucho aqui
    
    # GV Aqui debo setear el ambiente de variables de periodo ----------
    try:
        Period = get_period_data(current_user.id,db.engine,Interface)
    except:
        Period = get_period_data()
    logger.debug(f"Period={Period}")    
    # GV ---------------------------------------------------------------
    # GV Setup all data to render in template
    data =  {   "name":current_app.name,
                "app_name":current_app.name,
                "date_time":strftime('%Y-%m-%d %H:%M:%S'),
                "user_agent":request.headers.get('User-Agent'),
                "db":db,
                "logger":logger,
                "VERSION_MAYOR":VERSION_MAYOR,
                "VERSION_MINOR":VERSION_MINOR,
                "VERSION_PATCH":VERSION_PATCH,
            }
    logger.debug(f"data={data}")    
    butlerdata={
                "BUTLER_PERIOD":Period,
    }
    logger.debug(f"butlerdata={butlerdata}")    
    logger.debug(f"return render_template('butler.html',data=data,butlerdata=butlerdata)")
    return render_template('butler.html',data=data,butlerdata=butlerdata)

@main.route('/language/<string:langcode>', methods=['GET', 'POST'])
def language(langcode):
    current_app.config.CURRENT_LANGUAGE = langcode
    return redirect('/')

@main.route('/under_construction', methods=['GET','POST'])
def under_construction():   
    return render_template('under_construction.html')

@main.route('/demo', methods=['GET','POST'])
def demo():   
    return render_template('demo.html')

@main.route('/struct', methods=['GET', 'POST'])
def struct():
    return render_template('struct.html')

@main.route('/test_index', methods=['GET', 'POST'])
def test_index():
    try:
        # Espera a capitulo 3 para mejorar procedimiento de respuesta, hard coding mucho aqui

        if logger is not None:
            logger.debug("index() IN")
        else:
            print("*** WARNING *** Route: test_index: logger is undefined. !!! No logging functions possible. !!!")

        data =  {   "name":current_app.name,
                    #"app_name":C.app_name,
                    "date_time":strftime('%Y-%m-%d %H:%M:%S'),
                    "user_agent":request.headers.get('User-Agent'),
                    "current_time":datetime.utcnow(),
                    "db":db,
                    "logger":logger,
                    #"C":C,
                    #"C.db":C.db,
                    #"C.logger":C.logger,
                    "current_app":current_app,
                    "current_app_dir":dir(current_app),
                    "current_app_app_context":current_app.app_context(),
                    "current_app_app_context DIR":dir(current_app.app_context()),
                    }
        name = None
        password = None
        form = None
        #form = NameForm()

        return render_template('test.html',data=data, name=name,password=password, form=form)
    except Exception as e:
        emtec_handle_general_exception(e,logger)

""" GV        
from markdown import markdown
from markdown import markdownFromFile
from markdown.extensions import tables
from markdown.extensions import toc
"""
@main.route('/butler_faq', methods=['GET','POST'])
def butler_faq():  
    """
    if logger is not None: 
        logger.debug(f"markdown = {markdown}")
        logger.debug(f"markdownFromFile = {markdownFromFile}")
        logger.debug(f"tables = {tables}")
    main_page_md   = f'{current_app.template_folder}/butler_main.md'
    main_page_html = f'{current_app.template_folder}/butler_main.html'
    markdownFromFile(
        input=main_page_md,
        output=main_page_html,
        encoding='utf8',
        extensions=[
            'markdown.extensions.tables',
            'markdown.extensions.toc',
            ]
        )
    """
    return render_template('butler_faq.html')

@main.route('/butler_about', methods=['GET','POST'])
def butler_about():   
    return render_template('butler_about.html')

# ----------------------------------------------------------------------


# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2022-03-23 18:29:41
# =============================================================================
# gen_models_code.py:445 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/includes/models_py_imports.py
from emtec.butler.db.flask_models import categories
from emtec.butler.forms import frm_categories,frm_categories_delete
from emtec.butler.db.flask_models import clusters
from emtec.butler.forms import frm_clusters,frm_clusters_delete
from emtec.butler.db.flask_models import cost_centers
from emtec.butler.forms import frm_cost_centers,frm_cost_centers_delete
from emtec.butler.db.flask_models import disk_images
from emtec.butler.forms import frm_disk_images,frm_disk_images_delete
from emtec.butler.db.flask_models import domains
from emtec.butler.forms import frm_domains,frm_domains_delete
from emtec.butler.db.flask_models import interface
from emtec.butler.forms import frm_interface,frm_interface_delete
from emtec.butler.db.flask_models import migration_groups
from emtec.butler.forms import frm_migration_groups,frm_migration_groups_delete
from emtec.butler.db.flask_models import migration_groups_vm
from emtec.butler.forms import frm_migration_groups_vm,frm_migration_groups_vm_delete
from emtec.butler.db.flask_models import nutanix_prism_vm
from emtec.butler.forms import frm_nutanix_prism_vm,frm_nutanix_prism_vm_delete
from emtec.butler.db.flask_models import nutanix_vm_images
from emtec.butler.forms import frm_nutanix_vm_images,frm_nutanix_vm_images_delete
from emtec.butler.db.flask_models import projects
from emtec.butler.forms import frm_projects,frm_projects_delete
from emtec.butler.db.flask_models import rates
from emtec.butler.forms import frm_rates,frm_rates_delete
from emtec.butler.db.flask_models import request_type
from emtec.butler.forms import frm_request_type,frm_request_type_delete
from emtec.butler.db.flask_models import requests
from emtec.butler.forms import frm_requests,frm_requests_delete
from emtec.butler.db.flask_models import Role
from emtec.butler.forms import frm_Role,frm_Role_delete
from emtec.butler.db.flask_models import subnets
from emtec.butler.forms import frm_subnets,frm_subnets_delete
from emtec.butler.db.flask_models import User
from emtec.butler.forms import frm_User,frm_User_delete

# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2022-03-23 18:29:41
# =============================================================================
# gen_views.py:32 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/views/view_categories.py
# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2022-03-23 18:29:42.501330
# ======================================================================        
# gen_views_form.html:AG 2022-03-23 18:29:42.501352
@main.route('/forms/Categories', methods=['GET', 'POST'])
@login_required

def forms_Categories():
    """ Form handling function for table Categories """
    logger.debug('forms_Categories(): Enter')
    
    # Shardening Code goes her if needed
    collectordata={}
    collectordata.update({"COLLECTOR_PERIOD":get_period_data(current_user.id,db.engine,Interface)})
    collectordata.update({"CONFIG":current_app.config})
    suffix = collectordata['COLLECTOR_PERIOD']['active']
    table_name='Categories'
    class_name='categories'
    template_name='Categories'
    sharding=False
    category_name  =  request.args.get('category_name',0,type=int)
    
    # Ensures DB Data is commited prior main query
    try:
        db.session.commit()
    except:
        db.session.rollback()
    row =  categories.query.filter(categories.category_name == category_name).first()
    if row is None:
        row=categories()
        session['is_new_row']=True
    session['data'] =  {  'category_name':row.category_name, 'category_description':row.category_description }
    
    form = frm_categories()
    
    # Actual Form activation here
    if form.validate_on_submit():
        # Code for SAVE option -----------------------------------------
        if form.submit_Save.data and current_user.role_id > 1:
            row.category_name = form.category_name.data
            row.category_description = form.category_description.data
            try:
               session['new_row']=str(row)
               db.session.flush()
               db.session.add(row)
               db.session.commit()
               db.session.flush()
               if session['is_new_row']==True:
                   logger.audit ( '%s:NEW:%s' % (current_user.username,session['new_row'] ) )
                   flash('New Categories created OK')
               else:
                   logger.audit ( '%s:OLD:%s' % (current_user.username,session['prev_row']) )
                   logger.audit ( '%s:UPD:%s' % (current_user.username,session['new_row'] ) )    
                   message=Markup('<b>Categories category_name saved OK</b>')
                   flash(message)
               db.session.flush()
            except Exception as e:
               db.session.rollback()
               db.session.flush()
               message=Markup('ERROR saving Categories record : %s'%(e))
               flash(message)
            return redirect(url_for('.select_Categories_query'))
        # --------------------------------------------------------------
        # Code for NEW option
        # GV 20190109 f.write(        "        elif   form.submit_New.data:\n")
        elif   form.submit_New.data and current_user.role_id>1:
            #print('New Data Here ...')
            session['is_new_row']=True
            db.session.flush()
            row=categories()
    
            return redirect(url_for('.forms_Categories'))    
    
        # Code for CANCEL option 
        elif   form.submit_Cancel.data:
            #print('Cancel Data Here ... does nothing')
            message=Markup('Categories Record modifications discarded ...')
            flash(message)
        # Code for ANY OTHER option should never get here
        else:
            #print('form validated but not submited ???')
            message=Markup("<b>Categories data modifications not allowed for user '%s'. Please contact EG Suite's Administrator ...</b>"%(current_user.username))    
            flash(message)
    
            return redirect(url_for('.forms_'))    
    
    
    form.category_name.data = row.category_name
    form.category_description.data = row.category_description
    session['prev_row'] = str(row)
    session['is_new_row'] = False
    logger.debug('forms_Categories(): Exit')
    # Generates pagination data here
    P=[]
    # Tab Relations = [{'name': 'nutanix_prism_vm', 'class': 'nutanix_prism_vm', 'backref': 'categories', 'caption': 'NUTANIX_PRISM_VM', 'table': 'Nutanix_Prism_VM'}]
    
    from flask_sqlalchemy import Pagination
    # [{'name': 'nutanix_prism_vm', 'class': 'nutanix_prism_vm', 'backref': 'categories', 'caption': 'NUTANIX_PRISM_VM', 'table': 'Nutanix_Prism_VM'}]
    try:
        if hasattr(row, 'nutanix_prism_vm'):
            P.append(({'name': 'nutanix_prism_vm', 'class': 'nutanix_prism_vm', 'backref': 'categories', 'caption': 'NUTANIX_PRISM_VM', 'table': 'Nutanix_Prism_VM'},row.nutanix_prism_vm.paginate()))
    except Exception as e:
        print(f'Exception: {str(e)}')
    
    
    # Generation of pagination data completed
    collectordata={}
    collectordata.update({"COLLECTOR_PERIOD":get_period_data(current_user.id,db.engine,Interface)})
    return render_template('categories.html', form=form, row=row, P=P,collectordata=collectordata)    
# ======================================================================



# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2022-03-23 18:29:42.509400
# ======================================================================        
# gen_views_delete.html:AG 2022-03-23 18:29:42.509415
@main.route('/forms/Categories_delete', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DELETE)
@admin_required
def forms_Categories_delete():
    """ Delete record handling function for table Categories """
    logger.debug('forms_Categories_delete(): Enter')
    category_name  =  request.args.get('category_name',0,type=int)
    row =  categories.query.filter(categories.category_name == category_name).first()

    if row is None:
        row=categories()
    session['data'] =  {  'category_name':row.category_name, 'category_description':row.category_description }
                       
    form = frm_categories_delete()

    # Tab['has_fks'] False
    
            
    # Actual Form activation here
    if form.validate_on_submit():
    
    # Code for SAVE option
        if  form.submit_Delete.data:
            print('Delete Data Here...')

    
    #f.write(        "            print('Delete Data Here...')
            try:
                session['deleted_row']=str(row)
                db.session.flush()
                db.session.delete(row)
                db.session.commit()
                db.session.flush()
                logger.audit ( '%s:DEL:%s' % (current_user.username,session['deleted_row']) )
                flash('Categories category_name deleted OK')
            except exc.IntegrityError as e:
                db.session.rollback()    
                flash('INTEGRITY ERROR: Are you sure there are no dependant records in other tables?')
                return redirect(url_for('.forms_Categories_delete',category_name=session['data']['category_name']))    
    
            return redirect(url_for('.select_Categories_query'))    
    # Code for CANCEL option 
        elif   form.submit_Cancel.data:
            print('Cancel Data Here ... does nothing')
            flash('Record modifications discarded ...')
            return redirect(url_for('.select_Categories_query'))    
    # Code for ANY OTHER option should never get here
        else:
            print('form validated but not submited ???')
            return redirect(url_for('.select_Categories_query'))    
    
    logger.debug('forms_Categories_delete(): Exit')
    collectordata={}
    collectordata.update({"COLLECTOR_PERIOD":get_period_data(current_user.id,db.engine,Interface)})
    return render_template('categories_delete.html', form=form, data=session.get('data'),row=row,collectordata=collectordata)
#===============================================================================

# table_name: Categories
# class_name: categories
# is shardened: False
# current_app: 
# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2022-03-23 18:29:42.525818
# ======================================================================

# gen_views_select_query.html:AG 2022-03-23 18:29:42.525832        
@main.route('/select/Categories_Query', methods=['GET','POST'])
@login_required
@admin_required
def select_Categories_query():
    """ Select rows handling function for table 'Categories' """
    logger.debug('select_Categories_query(): Enter')
    #chk_c000001(filename=os.path.join(current_app.root_path, '.c000001'),request=request,db=db,logger=logger)
    # Shardening Code goes her if needed
    collectordata={}
    collectordata.update({"COLLECTOR_PERIOD":get_period_data(current_user.id,db.engine,Interface)})
    collectordata.update({"CONFIG":current_app.config})
    suffix = collectordata['COLLECTOR_PERIOD']['active']
    table_name='Categories'
    class_name='categories'
    template_name='Categories'
    sharding=False


    logger.debug("-----------------------------------------------------------")
    logger.debug("%s: template_name            = %s",__name__,template_name)

    logger.debug("-----------------------------------------------------------")    
        
    # Get parameters from URL call
    ia       =  request.args.get('ia',     None,type=str)
    if ia is not None:
        ia=ia.split(',')
        if ia[0]=='ORDER':
            #set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name='categories',Option_Type=OPTION_ORDER_BY,Argument_1=ia[1],Argument_2=ia[2])
            set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name=class_name,Option_Type=OPTION_ORDER_BY,Argument_1=ia[1],Argument_2=ia[2])
        elif ia[0]=='GROUP':
            #set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name='categories',Option_Type=OPTION_GROUP_BY,Argument_1=ia[1])
            set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name=class_name,Option_Type=OPTION_GROUP_BY,Argument_1=ia[1])
        elif ia[0]=='LIMIT':
            #set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name='categories',Option_Type=OPTION_LIMIT,Argument_1=ia[1])
            set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name=class_name,Option_Type=OPTION_LIMIT,Argument_1=ia[1])

    iad      =  request.args.get('iad',     None,type=int)
    if iad is not None: delete_query_option(engine=db.engine,Interface=Interface,Id=iad) 
    
    field    =  request.args.get('field',   None,type=str)
    value    =  request.args.get('value',   None,type=str)
    
    # Populates a list of foreign keys used for advanced filtering
    # ------------------------------------------------------------------
    foreign_keys={}
    
    # ------------------------------------------------------------------
    
    if field is not None:
        reset_query_options(    engine=db.engine,Interface=Interface,
                                User_Id=current_user.id,
                                #Table_name='categories'
                                Table_name=class_name
                                )

        
        if field in foreign_keys.keys():
            Class,referenced_classname,referenced_Field,referenced_Value,column_Header=foreign_keys[field]
            foreign_field='%s.%s:%s'%(referenced_classname,referenced_Value,column_Header)
            foreign_record=Class.query.get(value)
            foreign_description="'%s'"%getattr(foreign_record,referenced_Value)
        set_query_option(   engine=db.engine,Interface=Interface,
                        User_Id=current_user.id,
                        Table_name=class_name,
                        Option_Type=OPTION_FILTER,
                        Argument_1=foreign_field,
                        Argument_2='==',
                        Argument_3=foreign_description
                        )
    page     =  request.args.get('page',    1   ,type=int)
    addx     =  request.args.get('add.x',   None,type=int)
    addy     =  request.args.get('add.y',   None,type=int)
    exportx  =  request.args.get('export.x',None,type=int)
    exporty  =  request.args.get('export.y',None,type=int)
    filterx  =  request.args.get('filter.x',None,type=int)
    filtery  =  request.args.get('filter.y',None,type=int)
    # Select excluyent view mode
    if   addx    is not None: mode = 'add'
    elif exportx is not None: mode = 'export'
    elif filterx is not None: mode = 'filter'
    else:                     mode = 'select'
    category_name =  request.args.get('category_name',None,type=str)
    category_description =  request.args.get('category_description',None,type=str)
    
    # Build default query all fields from table
    

    if category_name is not None and len(category_name)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='category_name:category_name',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%category_name
                )
    
    
    if category_description is not None and len(category_description)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='category_description:category_description',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%category_description
                )
    
    
    
    statement_query,options=get_query_options(engine=db.engine,Interface=Interface,Table_name=class_name,User_Id=current_user.id)
    tracebox_log(statement_query,logger,length=80)
    query=eval(statement_query)
    filtered_query = query    
    if mode == 'filter':
        query=filtered_query
    elif mode == 'export':
        query=filtered_query
        fh,output_file = tempfile.mkstemp(suffix='', prefix='%s_'%table_name, dir=None, text=False)
        dict = {'header':{},'detail':[]}
        count = 0
        rows = query.all()
        for row in rows:
            dict['detail'].append({})
            for column in ['category_name', 'category_description']:
                dict['detail'][count].update( { column:str(row.__getattribute__(column))})
                
            count += 1
        dict['header'].update({'count':count})
        jsonarray      = json.dumps(dict)
        data           = json.loads(jsonarray)  
        dataframe      = json_normalize(data, 'detail').assign(**data['header'])
        fh,output_file = tempfile.mkstemp(suffix='', prefix='%_'%table_name, dir='/tmp', text=False)
        xlsx_file      = '%s/%s'%(current_app.root_path,url_for('static',filename='%s.xls'%(output_file)))
        dataframe.to_excel(xlsx_file,sheet_name=table_name,columns=['category_name', 'category_description'])
        return send_file(xlsx_file,as_attachment=True,attachment_filename=output_file.replace('/','_')+'.xls')
    elif mode == 'add':
        return redirect(url_for('.forms_%s'%table_name))
    elif mode == 'select':
        pass
        # if some filter is required
        if field is not None:
            if field == 'category_name':
                if value is not None:
                    query = query.filter_by(category_name=value)
            if field == 'category_description':
                if value is not None:
                    query = query.filter_by(category_description=value)
            
    # Actual request from DB follows
    tracebox_log(query,logger,length=80)
    # getting paginated rows for query
    rows = query.paginate(page, per_page=current_app.config['LINES_PER_PAGE'], error_out=False)
    # Setting pagination variables ...
    if field is not None:
       next_url = url_for('.select_%s_query'%template_name, field=field, value=value, page=rows.next_num) if rows.has_next else None
       prev_url = url_for('.select_%s_query'%template_name, field=field, value=value, page=rows.prev_num) if rows.has_prev else None
    else:
       next_url = url_for('.select_%s_query'%template_name, page=rows.next_num) if rows.has_next else None
       prev_url = url_for('.select_%s_query'%template_name, page=rows.prev_num) if rows.has_prev else None
    # Actual rendering ...
    if request.headers.get('Content-Type') is not None or request.args.get('JSON',None,type=str) is not None:
        # NOTE: needs review for JSONnifiyng output when needed (API Interface?)
        if "JSON" in request.headers.get('Content-Type') or request.args.get('JSON',None,type=str) is not None:
            logger.debug('select_%s_query(): will render: JSON rows'%template_name)
            logger.debug('select_%s_query(): Exit'%template_name)
            return json.dumps(serialize_object(rows.__dict__))
    logger.debug('select_%s_query(): will render: %s_All.html'%(template_name,table_name.lower()))
    logger.debug('select_%s_query(): Exit'%template_name)
    return render_template('%s_select_All.html'%template_name.lower(),rows=rows,options=options,collectordata=collectordata)
#===============================================================================
   
# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2022-03-23 18:29:42.556227
# ======================================================================
# gen_views_api.html:AG 2022-03-23 18:29:42.556242
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
        #response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        #response.headers['Pragma']        = 'no-cache'
        try:
            id_counter = 0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values=[id]
            # Codigo para un solo campo de id
            # chequear si marcado explicitamente
            db.session.flush()
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
            db.session.flush()
            db.session.refresh(row)
            db.session.flush()
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
                db.session.flush()
                db.session.refresh(row)
                db.session.flush()
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
                db.session.rollback()
                if request.values is not None and len(request.values):
                    if 'category_description' in request.values:
                        row.category_description = request.values.get('category_description')
                # ----------------------------------------------------------
                db.session.merge(row)
                db.session.flush()
                db.session.commit()
                db.session.flush()
                db.session.refresh(row)
                db.session.flush()
                message = f"Modified 'Categories' category_name = {id}"
                try:
                    row     = json.loads(row.get_json())
                except:
                    row     = None
            else:
                code    = API_NOT_FOUND
                message = f"Not found Categories with category_name = {id}"
                row     = None
                db.session.rollback()
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
            row     = None
            db.session.rollback()
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
                db.session.flush()
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

# ======================================================================# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2022-03-23 18:29:41
# =============================================================================
# gen_views.py:32 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/views/view_clusters.py
# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2022-03-23 18:29:42.662023
# ======================================================================        
# gen_views_form.html:AG 2022-03-23 18:29:42.662040
@main.route('/forms/Clusters', methods=['GET', 'POST'])
@login_required

def forms_Clusters():
    """ Form handling function for table Clusters """
    logger.debug('forms_Clusters(): Enter')
    
    # Shardening Code goes her if needed
    collectordata={}
    collectordata.update({"COLLECTOR_PERIOD":get_period_data(current_user.id,db.engine,Interface)})
    collectordata.update({"CONFIG":current_app.config})
    suffix = collectordata['COLLECTOR_PERIOD']['active']
    table_name='Clusters'
    class_name='clusters'
    template_name='Clusters'
    sharding=False
    cluster_uuid  =  request.args.get('cluster_uuid',0,type=int)
    
    # Ensures DB Data is commited prior main query
    try:
        db.session.commit()
    except:
        db.session.rollback()
    row =  clusters.query.filter(clusters.cluster_uuid == cluster_uuid).first()
    if row is None:
        row=clusters()
        session['is_new_row']=True
    session['data'] =  {  'cluster_uuid':row.cluster_uuid, 'cluster_name':row.cluster_name, 'cluster_username':row.cluster_username, 'cluster_password':row.cluster_password, 'cluster_ip':row.cluster_ip }
    
    form = frm_clusters()
    
    # Actual Form activation here
    if form.validate_on_submit():
        # Code for SAVE option -----------------------------------------
        if form.submit_Save.data and current_user.role_id > 1:
            row.cluster_uuid = form.cluster_uuid.data
            row.cluster_name = form.cluster_name.data
            row.cluster_username = form.cluster_username.data
            row.cluster_password = form.cluster_password.data
            row.cluster_ip = form.cluster_ip.data
            try:
               session['new_row']=str(row)
               db.session.flush()
               db.session.add(row)
               db.session.commit()
               db.session.flush()
               if session['is_new_row']==True:
                   logger.audit ( '%s:NEW:%s' % (current_user.username,session['new_row'] ) )
                   flash('New Clusters created OK')
               else:
                   logger.audit ( '%s:OLD:%s' % (current_user.username,session['prev_row']) )
                   logger.audit ( '%s:UPD:%s' % (current_user.username,session['new_row'] ) )    
                   message=Markup('<b>Clusters cluster_uuid saved OK</b>')
                   flash(message)
               db.session.flush()
            except Exception as e:
               db.session.rollback()
               db.session.flush()
               message=Markup('ERROR saving Clusters record : %s'%(e))
               flash(message)
            return redirect(url_for('.select_Clusters_query'))
        # --------------------------------------------------------------
        # Code for NEW option
        # GV 20190109 f.write(        "        elif   form.submit_New.data:\n")
        elif   form.submit_New.data and current_user.role_id>1:
            #print('New Data Here ...')
            session['is_new_row']=True
            db.session.flush()
            row=clusters()
    
            return redirect(url_for('.forms_Clusters'))    
    
        # Code for CANCEL option 
        elif   form.submit_Cancel.data:
            #print('Cancel Data Here ... does nothing')
            message=Markup('Clusters Record modifications discarded ...')
            flash(message)
        # Code for ANY OTHER option should never get here
        else:
            #print('form validated but not submited ???')
            message=Markup("<b>Clusters data modifications not allowed for user '%s'. Please contact EG Suite's Administrator ...</b>"%(current_user.username))    
            flash(message)
    
            return redirect(url_for('.forms_'))    
    
    
    form.cluster_uuid.data = row.cluster_uuid
    form.cluster_name.data = row.cluster_name
    form.cluster_username.data = row.cluster_username
    form.cluster_password.data = row.cluster_password
    form.cluster_ip.data = row.cluster_ip
    session['prev_row'] = str(row)
    session['is_new_row'] = False
    logger.debug('forms_Clusters(): Exit')
    # Generates pagination data here
    P=[]
    # Tab Relations = [{'name': 'nutanix_prism_vm', 'class': 'nutanix_prism_vm', 'backref': 'clusters', 'caption': 'NUTANIX_PRISM_VM', 'table': 'Nutanix_Prism_VM'}]
    
    from flask_sqlalchemy import Pagination
    # [{'name': 'nutanix_prism_vm', 'class': 'nutanix_prism_vm', 'backref': 'clusters', 'caption': 'NUTANIX_PRISM_VM', 'table': 'Nutanix_Prism_VM'}]
    try:
        if hasattr(row, 'nutanix_prism_vm'):
            P.append(({'name': 'nutanix_prism_vm', 'class': 'nutanix_prism_vm', 'backref': 'clusters', 'caption': 'NUTANIX_PRISM_VM', 'table': 'Nutanix_Prism_VM'},row.nutanix_prism_vm.paginate()))
    except Exception as e:
        print(f'Exception: {str(e)}')
    
    
    # Generation of pagination data completed
    collectordata={}
    collectordata.update({"COLLECTOR_PERIOD":get_period_data(current_user.id,db.engine,Interface)})
    return render_template('clusters.html', form=form, row=row, P=P,collectordata=collectordata)    
# ======================================================================



# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2022-03-23 18:29:42.671926
# ======================================================================        
# gen_views_delete.html:AG 2022-03-23 18:29:42.671943
@main.route('/forms/Clusters_delete', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DELETE)
@admin_required
def forms_Clusters_delete():
    """ Delete record handling function for table Clusters """
    logger.debug('forms_Clusters_delete(): Enter')
    cluster_uuid  =  request.args.get('cluster_uuid',0,type=int)
    row =  clusters.query.filter(clusters.cluster_uuid == cluster_uuid).first()

    if row is None:
        row=clusters()
    session['data'] =  {  'cluster_uuid':row.cluster_uuid, 'cluster_name':row.cluster_name, 'cluster_username':row.cluster_username, 'cluster_password':row.cluster_password, 'cluster_ip':row.cluster_ip }
                       
    form = frm_clusters_delete()

    # Tab['has_fks'] False
    
            
    # Actual Form activation here
    if form.validate_on_submit():
    
    # Code for SAVE option
        if  form.submit_Delete.data:
            print('Delete Data Here...')

    
    #f.write(        "            print('Delete Data Here...')
            try:
                session['deleted_row']=str(row)
                db.session.flush()
                db.session.delete(row)
                db.session.commit()
                db.session.flush()
                logger.audit ( '%s:DEL:%s' % (current_user.username,session['deleted_row']) )
                flash('Clusters cluster_uuid deleted OK')
            except exc.IntegrityError as e:
                db.session.rollback()    
                flash('INTEGRITY ERROR: Are you sure there are no dependant records in other tables?')
                return redirect(url_for('.forms_Clusters_delete',cluster_uuid=session['data']['cluster_uuid']))    
    
            return redirect(url_for('.select_Clusters_query'))    
    # Code for CANCEL option 
        elif   form.submit_Cancel.data:
            print('Cancel Data Here ... does nothing')
            flash('Record modifications discarded ...')
            return redirect(url_for('.select_Clusters_query'))    
    # Code for ANY OTHER option should never get here
        else:
            print('form validated but not submited ???')
            return redirect(url_for('.select_Clusters_query'))    
    
    logger.debug('forms_Clusters_delete(): Exit')
    collectordata={}
    collectordata.update({"COLLECTOR_PERIOD":get_period_data(current_user.id,db.engine,Interface)})
    return render_template('clusters_delete.html', form=form, data=session.get('data'),row=row,collectordata=collectordata)
#===============================================================================

# table_name: Clusters
# class_name: clusters
# is shardened: False
# current_app: 
# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2022-03-23 18:29:42.691501
# ======================================================================

# gen_views_select_query.html:AG 2022-03-23 18:29:42.691517        
@main.route('/select/Clusters_Query', methods=['GET','POST'])
@login_required
@admin_required
def select_Clusters_query():
    """ Select rows handling function for table 'Clusters' """
    logger.debug('select_Clusters_query(): Enter')
    #chk_c000001(filename=os.path.join(current_app.root_path, '.c000001'),request=request,db=db,logger=logger)
    # Shardening Code goes her if needed
    collectordata={}
    collectordata.update({"COLLECTOR_PERIOD":get_period_data(current_user.id,db.engine,Interface)})
    collectordata.update({"CONFIG":current_app.config})
    suffix = collectordata['COLLECTOR_PERIOD']['active']
    table_name='Clusters'
    class_name='clusters'
    template_name='Clusters'
    sharding=False


    logger.debug("-----------------------------------------------------------")
    logger.debug("%s: template_name            = %s",__name__,template_name)

    logger.debug("-----------------------------------------------------------")    
        
    # Get parameters from URL call
    ia       =  request.args.get('ia',     None,type=str)
    if ia is not None:
        ia=ia.split(',')
        if ia[0]=='ORDER':
            #set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name='clusters',Option_Type=OPTION_ORDER_BY,Argument_1=ia[1],Argument_2=ia[2])
            set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name=class_name,Option_Type=OPTION_ORDER_BY,Argument_1=ia[1],Argument_2=ia[2])
        elif ia[0]=='GROUP':
            #set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name='clusters',Option_Type=OPTION_GROUP_BY,Argument_1=ia[1])
            set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name=class_name,Option_Type=OPTION_GROUP_BY,Argument_1=ia[1])
        elif ia[0]=='LIMIT':
            #set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name='clusters',Option_Type=OPTION_LIMIT,Argument_1=ia[1])
            set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name=class_name,Option_Type=OPTION_LIMIT,Argument_1=ia[1])

    iad      =  request.args.get('iad',     None,type=int)
    if iad is not None: delete_query_option(engine=db.engine,Interface=Interface,Id=iad) 
    
    field    =  request.args.get('field',   None,type=str)
    value    =  request.args.get('value',   None,type=str)
    
    # Populates a list of foreign keys used for advanced filtering
    # ------------------------------------------------------------------
    foreign_keys={}
    
    # ------------------------------------------------------------------
    
    if field is not None:
        reset_query_options(    engine=db.engine,Interface=Interface,
                                User_Id=current_user.id,
                                #Table_name='clusters'
                                Table_name=class_name
                                )

        
        if field in foreign_keys.keys():
            Class,referenced_classname,referenced_Field,referenced_Value,column_Header=foreign_keys[field]
            foreign_field='%s.%s:%s'%(referenced_classname,referenced_Value,column_Header)
            foreign_record=Class.query.get(value)
            foreign_description="'%s'"%getattr(foreign_record,referenced_Value)
        set_query_option(   engine=db.engine,Interface=Interface,
                        User_Id=current_user.id,
                        Table_name=class_name,
                        Option_Type=OPTION_FILTER,
                        Argument_1=foreign_field,
                        Argument_2='==',
                        Argument_3=foreign_description
                        )
    page     =  request.args.get('page',    1   ,type=int)
    addx     =  request.args.get('add.x',   None,type=int)
    addy     =  request.args.get('add.y',   None,type=int)
    exportx  =  request.args.get('export.x',None,type=int)
    exporty  =  request.args.get('export.y',None,type=int)
    filterx  =  request.args.get('filter.x',None,type=int)
    filtery  =  request.args.get('filter.y',None,type=int)
    # Select excluyent view mode
    if   addx    is not None: mode = 'add'
    elif exportx is not None: mode = 'export'
    elif filterx is not None: mode = 'filter'
    else:                     mode = 'select'
    cluster_uuid =  request.args.get('cluster_uuid',None,type=str)
    cluster_name =  request.args.get('cluster_name',None,type=str)
    cluster_username =  request.args.get('cluster_username',None,type=str)
    cluster_password =  request.args.get('cluster_password',None,type=str)
    cluster_ip =  request.args.get('cluster_ip',None,type=str)
    
    # Build default query all fields from table
    

    if cluster_uuid is not None and len(cluster_uuid)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='cluster_uuid:cluster_uuid',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%cluster_uuid
                )
    
    
    if cluster_name is not None and len(cluster_name)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='cluster_name:cluster_name',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%cluster_name
                )
    
    
    if cluster_username is not None and len(cluster_username)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='cluster_username:cluster_username',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%cluster_username
                )
    
    
    if cluster_password is not None and len(cluster_password)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='cluster_password:cluster_password',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%cluster_password
                )
    
    
    if cluster_ip is not None and len(cluster_ip)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='cluster_ip:cluster_ip',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%cluster_ip
                )
    
    
    
    statement_query,options=get_query_options(engine=db.engine,Interface=Interface,Table_name=class_name,User_Id=current_user.id)
    tracebox_log(statement_query,logger,length=80)
    query=eval(statement_query)
    filtered_query = query    
    if mode == 'filter':
        query=filtered_query
    elif mode == 'export':
        query=filtered_query
        fh,output_file = tempfile.mkstemp(suffix='', prefix='%s_'%table_name, dir=None, text=False)
        dict = {'header':{},'detail':[]}
        count = 0
        rows = query.all()
        for row in rows:
            dict['detail'].append({})
            for column in ['cluster_uuid', 'cluster_name', 'cluster_username', 'cluster_password', 'cluster_ip']:
                dict['detail'][count].update( { column:str(row.__getattribute__(column))})
                
            count += 1
        dict['header'].update({'count':count})
        jsonarray      = json.dumps(dict)
        data           = json.loads(jsonarray)  
        dataframe      = json_normalize(data, 'detail').assign(**data['header'])
        fh,output_file = tempfile.mkstemp(suffix='', prefix='%_'%table_name, dir='/tmp', text=False)
        xlsx_file      = '%s/%s'%(current_app.root_path,url_for('static',filename='%s.xls'%(output_file)))
        dataframe.to_excel(xlsx_file,sheet_name=table_name,columns=['cluster_uuid', 'cluster_name', 'cluster_username', 'cluster_password', 'cluster_ip'])
        return send_file(xlsx_file,as_attachment=True,attachment_filename=output_file.replace('/','_')+'.xls')
    elif mode == 'add':
        return redirect(url_for('.forms_%s'%table_name))
    elif mode == 'select':
        pass
        # if some filter is required
        if field is not None:
            if field == 'cluster_uuid':
                if value is not None:
                    query = query.filter_by(cluster_uuid=value)
            if field == 'cluster_name':
                if value is not None:
                    query = query.filter_by(cluster_name=value)
            if field == 'cluster_username':
                if value is not None:
                    query = query.filter_by(cluster_username=value)
            if field == 'cluster_password':
                if value is not None:
                    query = query.filter_by(cluster_password=value)
            if field == 'cluster_ip':
                if value is not None:
                    query = query.filter_by(cluster_ip=value)
            
    # Actual request from DB follows
    tracebox_log(query,logger,length=80)
    # getting paginated rows for query
    rows = query.paginate(page, per_page=current_app.config['LINES_PER_PAGE'], error_out=False)
    # Setting pagination variables ...
    if field is not None:
       next_url = url_for('.select_%s_query'%template_name, field=field, value=value, page=rows.next_num) if rows.has_next else None
       prev_url = url_for('.select_%s_query'%template_name, field=field, value=value, page=rows.prev_num) if rows.has_prev else None
    else:
       next_url = url_for('.select_%s_query'%template_name, page=rows.next_num) if rows.has_next else None
       prev_url = url_for('.select_%s_query'%template_name, page=rows.prev_num) if rows.has_prev else None
    # Actual rendering ...
    if request.headers.get('Content-Type') is not None or request.args.get('JSON',None,type=str) is not None:
        # NOTE: needs review for JSONnifiyng output when needed (API Interface?)
        if "JSON" in request.headers.get('Content-Type') or request.args.get('JSON',None,type=str) is not None:
            logger.debug('select_%s_query(): will render: JSON rows'%template_name)
            logger.debug('select_%s_query(): Exit'%template_name)
            return json.dumps(serialize_object(rows.__dict__))
    logger.debug('select_%s_query(): will render: %s_All.html'%(template_name,table_name.lower()))
    logger.debug('select_%s_query(): Exit'%template_name)
    return render_template('%s_select_All.html'%template_name.lower(),rows=rows,options=options,collectordata=collectordata)
#===============================================================================
   
# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2022-03-23 18:29:42.722207
# ======================================================================
# gen_views_api.html:AG 2022-03-23 18:29:42.722223
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
        #response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        #response.headers['Pragma']        = 'no-cache'
        try:
            id_counter = 0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values=[id]
            # Codigo para un solo campo de id
            # chequear si marcado explicitamente
            db.session.flush()
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
            db.session.flush()
            db.session.refresh(row)
            db.session.flush()
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
                db.session.flush()
                db.session.refresh(row)
                db.session.flush()
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
                db.session.rollback()
                if request.values is not None and len(request.values):
                    if 'cluster_name' in request.values:
                        row.cluster_name = request.values.get('cluster_name')
                    if 'cluster_username' in request.values:
                        row.cluster_username = request.values.get('cluster_username')
                    if 'cluster_password' in request.values:
                        row.cluster_password = request.values.get('cluster_password')
                    if 'cluster_ip' in request.values:
                        row.cluster_ip = request.values.get('cluster_ip')
                # ----------------------------------------------------------
                db.session.merge(row)
                db.session.flush()
                db.session.commit()
                db.session.flush()
                db.session.refresh(row)
                db.session.flush()
                message = f"Modified 'Clusters' cluster_uuid = {id}"
                try:
                    row     = json.loads(row.get_json())
                except:
                    row     = None
            else:
                code    = API_NOT_FOUND
                message = f"Not found Clusters with cluster_uuid = {id}"
                row     = None
                db.session.rollback()
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
            row     = None
            db.session.rollback()
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
                db.session.flush()
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

# ======================================================================# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2022-03-23 18:29:41
# =============================================================================
# gen_views.py:32 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/views/view_cost_centers.py

# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2022-03-23 18:29:42.836415
# ======================================================================        
# gen_views_delete.html:AG 2022-03-23 18:29:42.836430
@main.route('/forms/Cost_Centers_delete', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DELETE)
@admin_required
def forms_Cost_Centers_delete():
    """ Delete record handling function for table Cost_Centers """
    logger.debug('forms_Cost_Centers_delete(): Enter')
    CC_Id  =  request.args.get('CC_Id',0,type=int)
    row =  cost_centers.query.filter(cost_centers.CC_Id == CC_Id).first()

    if row is None:
        row=cost_centers()
    session['data'] =  {  'CC_Id':row.CC_Id, 'CC_Code':row.CC_Code, 'CC_Description':row.CC_Description, 'Cur_Code':row.Cur_Code, 'CC_Parent_Code':row.CC_Parent_Code, 'CC_Reg_Exp':row.CC_Reg_Exp, 'CC_Reference':row.CC_Reference }
                       
    form = frm_cost_centers_delete()

    # Tab['has_fks'] False
    
            
    # Actual Form activation here
    if form.validate_on_submit():
    
    # Code for SAVE option
        if  form.submit_Delete.data:
            print('Delete Data Here...')

    
    #f.write(        "            print('Delete Data Here...')
            try:
                session['deleted_row']=str(row)
                db.session.flush()
                db.session.delete(row)
                db.session.commit()
                db.session.flush()
                logger.audit ( '%s:DEL:%s' % (current_user.username,session['deleted_row']) )
                flash('Cost_centers CC_Id deleted OK')
            except exc.IntegrityError as e:
                db.session.rollback()    
                flash('INTEGRITY ERROR: Are you sure there are no dependant records in other tables?')
                return redirect(url_for('.forms_Cost_Centers_delete',CC_Id=session['data']['CC_Id']))    
    
            return redirect(url_for('.select_Cost_Centers_query'))    
    # Code for CANCEL option 
        elif   form.submit_Cancel.data:
            print('Cancel Data Here ... does nothing')
            flash('Record modifications discarded ...')
            return redirect(url_for('.select_Cost_Centers_query'))    
    # Code for ANY OTHER option should never get here
        else:
            print('form validated but not submited ???')
            return redirect(url_for('.select_Cost_Centers_query'))    
    
    logger.debug('forms_Cost_Centers_delete(): Exit')
    collectordata={}
    collectordata.update({"COLLECTOR_PERIOD":get_period_data(current_user.id,db.engine,Interface)})
    return render_template('cost_centers_delete.html', form=form, data=session.get('data'),row=row,collectordata=collectordata)
#===============================================================================

# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2022-03-23 18:29:42.885979
# ======================================================================
# gen_views_api.html:AG 2022-03-23 18:29:42.885994
# table_name: Cost_Centers
# class_name: cost_centers
# is shardened: True
# Table 'Cost_Centers' keys = CC_Id
# Errors: None
# ID field found 'CC_Id' auto_increment db.Integer
# Cost_Centers id field is 'Cost_Centers.CC_Id' of type 'int:'

@main.route('/api/get/Cost_Centers'     , methods=['GET'])
@main.route('/api/get/Cost_Centers/<int:id>', methods=['GET'])
def api_get_Cost_Centers(id=None):
    code       = API_OK
    message    = 'OK'
    rows       = None
    authorized = api_check_authorization(request,current_app)
    if authorized:
        #response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        #response.headers['Pragma']        = 'no-cache'
        try:
            id_counter = 0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values=[id]
            # Codigo para un solo campo de id
            # chequear si marcado explicitamente
            db.session.flush()
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
            row.CC_Id = None
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
            db.session.flush()
            db.session.refresh(row)
            db.session.flush()
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
                db.session.flush()
                db.session.refresh(row)
                db.session.flush()
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
                db.session.rollback()
                if request.values is not None and len(request.values):
                    if 'CC_Code' in request.values:
                        row.CC_Code = request.values.get('CC_Code')
                    if 'CC_Description' in request.values:
                        row.CC_Description = request.values.get('CC_Description')
                    if 'Cur_Code' in request.values:
                        row.Cur_Code = request.values.get('Cur_Code')
                    if 'CC_Parent_Code' in request.values:
                        row.CC_Parent_Code = request.values.get('CC_Parent_Code')
                    if 'CC_Reg_Exp' in request.values:
                        row.CC_Reg_Exp = request.values.get('CC_Reg_Exp')
                    if 'CC_Reference' in request.values:
                        row.CC_Reference = request.values.get('CC_Reference')
                # ----------------------------------------------------------
                db.session.merge(row)
                db.session.flush()
                db.session.commit()
                db.session.flush()
                db.session.refresh(row)
                db.session.flush()
                message = f"Modified 'Cost_Centers' CC_Id = {id}"
                try:
                    row     = json.loads(row.get_json())
                except:
                    row     = None
            else:
                code    = API_NOT_FOUND
                message = f"Not found Cost_Centers with CC_Id = {id}"
                row     = None
                db.session.rollback()
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
            row     = None
            db.session.rollback()
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
            query = query.filter(Cost_Centers.CC_Id == id)
            # --------------------------------------------------------------
            row = query.one_or_none()

            if row is not None:
                db.session.delete(row)
                db.session.flush()
                db.session.commit()
                db.session.flush()
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

# ======================================================================# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2022-03-23 18:29:41
# =============================================================================
# gen_views.py:32 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/views/view_disk_images.py
# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2022-03-23 18:29:42.990995
# ======================================================================        
# gen_views_form.html:AG 2022-03-23 18:29:42.991011
@main.route('/forms/Disk_Images', methods=['GET', 'POST'])
@login_required

def forms_Disk_Images():
    """ Form handling function for table Disk_Images """
    logger.debug('forms_Disk_Images(): Enter')
    
    # Shardening Code goes her if needed
    collectordata={}
    collectordata.update({"COLLECTOR_PERIOD":get_period_data(current_user.id,db.engine,Interface)})
    collectordata.update({"CONFIG":current_app.config})
    suffix = collectordata['COLLECTOR_PERIOD']['active']
    table_name='Disk_Images'
    class_name='disk_images'
    template_name='Disk_Images'
    sharding=False
    uuid  =  request.args.get('uuid',0,type=int)
    
    # Ensures DB Data is commited prior main query
    try:
        db.session.commit()
    except:
        db.session.rollback()
    row =  disk_images.query.filter(disk_images.uuid == uuid).first()
    if row is None:
        row=disk_images()
        session['is_new_row']=True
    session['data'] =  {  'uuid':row.uuid, 'name':row.name, 'annotation':row.annotation, 'image_type':row.image_type, 'image_state':row.image_state, 'vm_disk_size':row.vm_disk_size, 'vm_disk_size_mib':row.vm_disk_size_mib, 'vm_disk_size_gib':row.vm_disk_size_gib, 'cluster':row.cluster }
    
    form = frm_disk_images()
    
    # Actual Form activation here
    if form.validate_on_submit():
        # Code for SAVE option -----------------------------------------
        if form.submit_Save.data and current_user.role_id > 1:
            row.uuid = form.uuid.data
            row.name = form.name.data
            row.annotation = form.annotation.data
            row.image_type = form.image_type.data
            row.image_state = form.image_state.data
            row.vm_disk_size = form.vm_disk_size.data
            row.vm_disk_size_mib = form.vm_disk_size_mib.data
            row.vm_disk_size_gib = form.vm_disk_size_gib.data
            row.cluster = form.cluster.data
            try:
               session['new_row']=str(row)
               db.session.flush()
               db.session.add(row)
               db.session.commit()
               db.session.flush()
               if session['is_new_row']==True:
                   logger.audit ( '%s:NEW:%s' % (current_user.username,session['new_row'] ) )
                   flash('New Disk_images created OK')
               else:
                   logger.audit ( '%s:OLD:%s' % (current_user.username,session['prev_row']) )
                   logger.audit ( '%s:UPD:%s' % (current_user.username,session['new_row'] ) )    
                   message=Markup('<b>Disk_images uuid saved OK</b>')
                   flash(message)
               db.session.flush()
            except Exception as e:
               db.session.rollback()
               db.session.flush()
               message=Markup('ERROR saving Disk_images record : %s'%(e))
               flash(message)
            return redirect(url_for('.select_Disk_Images_query'))
        # --------------------------------------------------------------
        # Code for NEW option
        # GV 20190109 f.write(        "        elif   form.submit_New.data:\n")
        elif   form.submit_New.data and current_user.role_id>1:
            #print('New Data Here ...')
            session['is_new_row']=True
            db.session.flush()
            row=disk_images()
    
            return redirect(url_for('.forms_Disk_Images'))    
    
        # Code for CANCEL option 
        elif   form.submit_Cancel.data:
            #print('Cancel Data Here ... does nothing')
            message=Markup('Disk_images Record modifications discarded ...')
            flash(message)
        # Code for ANY OTHER option should never get here
        else:
            #print('form validated but not submited ???')
            message=Markup("<b>Disk_images data modifications not allowed for user '%s'. Please contact EG Suite's Administrator ...</b>"%(current_user.username))    
            flash(message)
    
            return redirect(url_for('.forms_'))    
    
    
    form.uuid.data = row.uuid
    form.name.data = row.name
    form.annotation.data = row.annotation
    form.image_type.data = row.image_type
    form.image_state.data = row.image_state
    form.vm_disk_size.data = row.vm_disk_size
    form.vm_disk_size_mib.data = row.vm_disk_size_mib
    form.vm_disk_size_gib.data = row.vm_disk_size_gib
    form.cluster.data = row.cluster
    session['prev_row'] = str(row)
    session['is_new_row'] = False
    logger.debug('forms_Disk_Images(): Exit')
    # Generates pagination data here
    P=[]
    # Tab Relations = []
    
    # Generation of pagination data completed
    collectordata={}
    collectordata.update({"COLLECTOR_PERIOD":get_period_data(current_user.id,db.engine,Interface)})
    return render_template('disk_images.html', form=form, row=row, P=P,collectordata=collectordata)    
# ======================================================================



# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2022-03-23 18:29:43.000656
# ======================================================================        
# gen_views_delete.html:AG 2022-03-23 18:29:43.000672
@main.route('/forms/Disk_Images_delete', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DELETE)
@admin_required
def forms_Disk_Images_delete():
    """ Delete record handling function for table Disk_Images """
    logger.debug('forms_Disk_Images_delete(): Enter')
    uuid  =  request.args.get('uuid',0,type=int)
    row =  disk_images.query.filter(disk_images.uuid == uuid).first()

    if row is None:
        row=disk_images()
    session['data'] =  {  'uuid':row.uuid, 'name':row.name, 'annotation':row.annotation, 'image_type':row.image_type, 'image_state':row.image_state, 'vm_disk_size':row.vm_disk_size, 'vm_disk_size_mib':row.vm_disk_size_mib, 'vm_disk_size_gib':row.vm_disk_size_gib, 'cluster':row.cluster }
                       
    form = frm_disk_images_delete()

    # Tab['has_fks'] False
    
            
    # Actual Form activation here
    if form.validate_on_submit():
    
    # Code for SAVE option
        if  form.submit_Delete.data:
            print('Delete Data Here...')

    
    #f.write(        "            print('Delete Data Here...')
            try:
                session['deleted_row']=str(row)
                db.session.flush()
                db.session.delete(row)
                db.session.commit()
                db.session.flush()
                logger.audit ( '%s:DEL:%s' % (current_user.username,session['deleted_row']) )
                flash('Disk_images uuid deleted OK')
            except exc.IntegrityError as e:
                db.session.rollback()    
                flash('INTEGRITY ERROR: Are you sure there are no dependant records in other tables?')
                return redirect(url_for('.forms_Disk_Images_delete',uuid=session['data']['uuid']))    
    
            return redirect(url_for('.select_Disk_Images_query'))    
    # Code for CANCEL option 
        elif   form.submit_Cancel.data:
            print('Cancel Data Here ... does nothing')
            flash('Record modifications discarded ...')
            return redirect(url_for('.select_Disk_Images_query'))    
    # Code for ANY OTHER option should never get here
        else:
            print('form validated but not submited ???')
            return redirect(url_for('.select_Disk_Images_query'))    
    
    logger.debug('forms_Disk_Images_delete(): Exit')
    collectordata={}
    collectordata.update({"COLLECTOR_PERIOD":get_period_data(current_user.id,db.engine,Interface)})
    return render_template('disk_images_delete.html', form=form, data=session.get('data'),row=row,collectordata=collectordata)
#===============================================================================

# table_name: Disk_Images
# class_name: disk_images
# is shardened: False
# current_app: 
# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2022-03-23 18:29:43.020888
# ======================================================================

# gen_views_select_query.html:AG 2022-03-23 18:29:43.020904        
@main.route('/select/Disk_Images_Query', methods=['GET','POST'])
@login_required
@admin_required
def select_Disk_Images_query():
    """ Select rows handling function for table 'Disk_Images' """
    logger.debug('select_Disk_Images_query(): Enter')
    #chk_c000001(filename=os.path.join(current_app.root_path, '.c000001'),request=request,db=db,logger=logger)
    # Shardening Code goes her if needed
    collectordata={}
    collectordata.update({"COLLECTOR_PERIOD":get_period_data(current_user.id,db.engine,Interface)})
    collectordata.update({"CONFIG":current_app.config})
    suffix = collectordata['COLLECTOR_PERIOD']['active']
    table_name='Disk_Images'
    class_name='disk_images'
    template_name='Disk_Images'
    sharding=False


    logger.debug("-----------------------------------------------------------")
    logger.debug("%s: template_name            = %s",__name__,template_name)

    logger.debug("-----------------------------------------------------------")    
        
    # Get parameters from URL call
    ia       =  request.args.get('ia',     None,type=str)
    if ia is not None:
        ia=ia.split(',')
        if ia[0]=='ORDER':
            #set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name='disk_images',Option_Type=OPTION_ORDER_BY,Argument_1=ia[1],Argument_2=ia[2])
            set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name=class_name,Option_Type=OPTION_ORDER_BY,Argument_1=ia[1],Argument_2=ia[2])
        elif ia[0]=='GROUP':
            #set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name='disk_images',Option_Type=OPTION_GROUP_BY,Argument_1=ia[1])
            set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name=class_name,Option_Type=OPTION_GROUP_BY,Argument_1=ia[1])
        elif ia[0]=='LIMIT':
            #set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name='disk_images',Option_Type=OPTION_LIMIT,Argument_1=ia[1])
            set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name=class_name,Option_Type=OPTION_LIMIT,Argument_1=ia[1])

    iad      =  request.args.get('iad',     None,type=int)
    if iad is not None: delete_query_option(engine=db.engine,Interface=Interface,Id=iad) 
    
    field    =  request.args.get('field',   None,type=str)
    value    =  request.args.get('value',   None,type=str)
    
    # Populates a list of foreign keys used for advanced filtering
    # ------------------------------------------------------------------
    foreign_keys={}
    
    # ------------------------------------------------------------------
    
    if field is not None:
        reset_query_options(    engine=db.engine,Interface=Interface,
                                User_Id=current_user.id,
                                #Table_name='disk_images'
                                Table_name=class_name
                                )

        
        if field in foreign_keys.keys():
            Class,referenced_classname,referenced_Field,referenced_Value,column_Header=foreign_keys[field]
            foreign_field='%s.%s:%s'%(referenced_classname,referenced_Value,column_Header)
            foreign_record=Class.query.get(value)
            foreign_description="'%s'"%getattr(foreign_record,referenced_Value)
        set_query_option(   engine=db.engine,Interface=Interface,
                        User_Id=current_user.id,
                        Table_name=class_name,
                        Option_Type=OPTION_FILTER,
                        Argument_1=foreign_field,
                        Argument_2='==',
                        Argument_3=foreign_description
                        )
    page     =  request.args.get('page',    1   ,type=int)
    addx     =  request.args.get('add.x',   None,type=int)
    addy     =  request.args.get('add.y',   None,type=int)
    exportx  =  request.args.get('export.x',None,type=int)
    exporty  =  request.args.get('export.y',None,type=int)
    filterx  =  request.args.get('filter.x',None,type=int)
    filtery  =  request.args.get('filter.y',None,type=int)
    # Select excluyent view mode
    if   addx    is not None: mode = 'add'
    elif exportx is not None: mode = 'export'
    elif filterx is not None: mode = 'filter'
    else:                     mode = 'select'
    uuid =  request.args.get('uuid',None,type=str)
    name =  request.args.get('name',None,type=str)
    annotation =  request.args.get('annotation',None,type=str)
    image_type =  request.args.get('image_type',None,type=str)
    image_state =  request.args.get('image_state',None,type=str)
    vm_disk_size =  request.args.get('vm_disk_size',None,type=str)
    vm_disk_size_mib =  request.args.get('vm_disk_size_mib',None,type=str)
    vm_disk_size_gib =  request.args.get('vm_disk_size_gib',None,type=str)
    cluster =  request.args.get('cluster',None,type=str)
    
    # Build default query all fields from table
    

    if uuid is not None and len(uuid)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='uuid:uuid',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%uuid
                )
    
    
    if name is not None and len(name)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='name:name',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%name
                )
    
    
    if annotation is not None and len(annotation)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='annotation:annotation',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%annotation
                )
    
    
    if image_type is not None and len(image_type)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='image_type:image_type',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%image_type
                )
    
    
    if image_state is not None and len(image_state)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='image_state:image_state',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%image_state
                )
    
    
    if vm_disk_size is not None and len(vm_disk_size)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='vm_disk_size:vm_disk_size',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%vm_disk_size
                )
    
    
    if vm_disk_size_mib is not None and len(vm_disk_size_mib)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='vm_disk_size_mib:vm_disk_size_mib',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%vm_disk_size_mib
                )
    
    
    if vm_disk_size_gib is not None and len(vm_disk_size_gib)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='vm_disk_size_gib:vm_disk_size_gib',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%vm_disk_size_gib
                )
    
    
    if cluster is not None and len(cluster)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='cluster:cluster',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%cluster
                )
    
    
    
    statement_query,options=get_query_options(engine=db.engine,Interface=Interface,Table_name=class_name,User_Id=current_user.id)
    tracebox_log(statement_query,logger,length=80)
    query=eval(statement_query)
    filtered_query = query    
    if mode == 'filter':
        query=filtered_query
    elif mode == 'export':
        query=filtered_query
        fh,output_file = tempfile.mkstemp(suffix='', prefix='%s_'%table_name, dir=None, text=False)
        dict = {'header':{},'detail':[]}
        count = 0
        rows = query.all()
        for row in rows:
            dict['detail'].append({})
            for column in ['uuid', 'name', 'annotation', 'image_type', 'image_state', 'vm_disk_size', 'vm_disk_size_mib', 'vm_disk_size_gib', 'cluster']:
                dict['detail'][count].update( { column:str(row.__getattribute__(column))})
                
            count += 1
        dict['header'].update({'count':count})
        jsonarray      = json.dumps(dict)
        data           = json.loads(jsonarray)  
        dataframe      = json_normalize(data, 'detail').assign(**data['header'])
        fh,output_file = tempfile.mkstemp(suffix='', prefix='%_'%table_name, dir='/tmp', text=False)
        xlsx_file      = '%s/%s'%(current_app.root_path,url_for('static',filename='%s.xls'%(output_file)))
        dataframe.to_excel(xlsx_file,sheet_name=table_name,columns=['uuid', 'name', 'annotation', 'image_type', 'image_state', 'vm_disk_size', 'vm_disk_size_mib', 'vm_disk_size_gib', 'cluster'])
        return send_file(xlsx_file,as_attachment=True,attachment_filename=output_file.replace('/','_')+'.xls')
    elif mode == 'add':
        return redirect(url_for('.forms_%s'%table_name))
    elif mode == 'select':
        pass
        # if some filter is required
        if field is not None:
            if field == 'uuid':
                if value is not None:
                    query = query.filter_by(uuid=value)
            if field == 'name':
                if value is not None:
                    query = query.filter_by(name=value)
            if field == 'annotation':
                if value is not None:
                    query = query.filter_by(annotation=value)
            if field == 'image_type':
                if value is not None:
                    query = query.filter_by(image_type=value)
            if field == 'image_state':
                if value is not None:
                    query = query.filter_by(image_state=value)
            if field == 'vm_disk_size':
                if value is not None:
                    query = query.filter_by(vm_disk_size=value)
            if field == 'vm_disk_size_mib':
                if value is not None:
                    query = query.filter_by(vm_disk_size_mib=value)
            if field == 'vm_disk_size_gib':
                if value is not None:
                    query = query.filter_by(vm_disk_size_gib=value)
            if field == 'cluster':
                if value is not None:
                    query = query.filter_by(cluster=value)
            
    # Actual request from DB follows
    tracebox_log(query,logger,length=80)
    # getting paginated rows for query
    rows = query.paginate(page, per_page=current_app.config['LINES_PER_PAGE'], error_out=False)
    # Setting pagination variables ...
    if field is not None:
       next_url = url_for('.select_%s_query'%template_name, field=field, value=value, page=rows.next_num) if rows.has_next else None
       prev_url = url_for('.select_%s_query'%template_name, field=field, value=value, page=rows.prev_num) if rows.has_prev else None
    else:
       next_url = url_for('.select_%s_query'%template_name, page=rows.next_num) if rows.has_next else None
       prev_url = url_for('.select_%s_query'%template_name, page=rows.prev_num) if rows.has_prev else None
    # Actual rendering ...
    if request.headers.get('Content-Type') is not None or request.args.get('JSON',None,type=str) is not None:
        # NOTE: needs review for JSONnifiyng output when needed (API Interface?)
        if "JSON" in request.headers.get('Content-Type') or request.args.get('JSON',None,type=str) is not None:
            logger.debug('select_%s_query(): will render: JSON rows'%template_name)
            logger.debug('select_%s_query(): Exit'%template_name)
            return json.dumps(serialize_object(rows.__dict__))
    logger.debug('select_%s_query(): will render: %s_All.html'%(template_name,table_name.lower()))
    logger.debug('select_%s_query(): Exit'%template_name)
    return render_template('%s_select_All.html'%template_name.lower(),rows=rows,options=options,collectordata=collectordata)
#===============================================================================
   
# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2022-03-23 18:29:43.055981
# ======================================================================
# gen_views_api.html:AG 2022-03-23 18:29:43.056004
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
        #response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        #response.headers['Pragma']        = 'no-cache'
        try:
            id_counter = 0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values=[id]
            # Codigo para un solo campo de id
            # chequear si marcado explicitamente
            db.session.flush()
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
            db.session.flush()
            db.session.refresh(row)
            db.session.flush()
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
                db.session.flush()
                db.session.refresh(row)
                db.session.flush()
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
                db.session.rollback()
                if request.values is not None and len(request.values):
                    if 'name' in request.values:
                        row.name = request.values.get('name')
                    if 'annotation' in request.values:
                        row.annotation = request.values.get('annotation')
                    if 'image_type' in request.values:
                        row.image_type = request.values.get('image_type')
                    if 'image_state' in request.values:
                        row.image_state = request.values.get('image_state')
                    if 'vm_disk_size' in request.values:
                        row.vm_disk_size = request.values.get('vm_disk_size')
                    if 'vm_disk_size_mib' in request.values:
                        row.vm_disk_size_mib = request.values.get('vm_disk_size_mib')
                    if 'vm_disk_size_gib' in request.values:
                        row.vm_disk_size_gib = request.values.get('vm_disk_size_gib')
                    if 'cluster' in request.values:
                        row.cluster = request.values.get('cluster')
                # ----------------------------------------------------------
                db.session.merge(row)
                db.session.flush()
                db.session.commit()
                db.session.flush()
                db.session.refresh(row)
                db.session.flush()
                message = f"Modified 'Disk_Images' uuid = {id}"
                try:
                    row     = json.loads(row.get_json())
                except:
                    row     = None
            else:
                code    = API_NOT_FOUND
                message = f"Not found Disk_Images with uuid = {id}"
                row     = None
                db.session.rollback()
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
            row     = None
            db.session.rollback()
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
                db.session.flush()
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

# ======================================================================# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2022-03-23 18:29:41
# =============================================================================
# gen_views.py:32 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/views/view_domains.py
# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2022-03-23 18:29:43.162769
# ======================================================================        
# gen_views_form.html:AG 2022-03-23 18:29:43.162845
@main.route('/forms/Domains', methods=['GET', 'POST'])
@login_required

def forms_Domains():
    """ Form handling function for table Domains """
    logger.debug('forms_Domains(): Enter')
    
    # Shardening Code goes her if needed
    collectordata={}
    collectordata.update({"COLLECTOR_PERIOD":get_period_data(current_user.id,db.engine,Interface)})
    collectordata.update({"CONFIG":current_app.config})
    suffix = collectordata['COLLECTOR_PERIOD']['active']
    table_name='Domains'
    class_name='domains'
    template_name='Domains'
    sharding=False
    Domain_Id  =  request.args.get('Domain_Id',0,type=int)
    
    # Ensures DB Data is commited prior main query
    try:
        db.session.commit()
    except:
        db.session.rollback()
    row =  domains.query.filter(domains.Domain_Id == Domain_Id).first()
    if row is None:
        row=domains()
        session['is_new_row']=True
    session['data'] =  {  'Domain_Id':row.Domain_Id, 'Name':row.Name, 'Comments':row.Comments }
    
    form = frm_domains()
    
    # Actual Form activation here
    if form.validate_on_submit():
        # Code for SAVE option -----------------------------------------
        if form.submit_Save.data and current_user.role_id > 1:
            row.Domain_Id = form.Domain_Id.data
            row.Name = form.Name.data
            row.Comments = form.Comments.data
            try:
               session['new_row']=str(row)
               db.session.flush()
               db.session.add(row)
               db.session.commit()
               db.session.flush()
               if session['is_new_row']==True:
                   logger.audit ( '%s:NEW:%s' % (current_user.username,session['new_row'] ) )
                   flash('New Domains created OK')
               else:
                   logger.audit ( '%s:OLD:%s' % (current_user.username,session['prev_row']) )
                   logger.audit ( '%s:UPD:%s' % (current_user.username,session['new_row'] ) )    
                   message=Markup('<b>Domains Domain_Id saved OK</b>')
                   flash(message)
               db.session.flush()
            except Exception as e:
               db.session.rollback()
               db.session.flush()
               message=Markup('ERROR saving Domains record : %s'%(e))
               flash(message)
            return redirect(url_for('.select_Domains_query'))
        # --------------------------------------------------------------
        # Code for NEW option
        # GV 20190109 f.write(        "        elif   form.submit_New.data:\n")
        elif   form.submit_New.data and current_user.role_id>1:
            #print('New Data Here ...')
            session['is_new_row']=True
            db.session.flush()
            row=domains()
    
            return redirect(url_for('.forms_Domains'))    
    
        # Code for CANCEL option 
        elif   form.submit_Cancel.data:
            #print('Cancel Data Here ... does nothing')
            message=Markup('Domains Record modifications discarded ...')
            flash(message)
        # Code for ANY OTHER option should never get here
        else:
            #print('form validated but not submited ???')
            message=Markup("<b>Domains data modifications not allowed for user '%s'. Please contact EG Suite's Administrator ...</b>"%(current_user.username))    
            flash(message)
    
            return redirect(url_for('.forms_'))    
    
    
    form.Domain_Id.data = row.Domain_Id
    form.Name.data = row.Name
    form.Comments.data = row.Comments
    session['prev_row'] = str(row)
    session['is_new_row'] = False
    logger.debug('forms_Domains(): Exit')
    # Generates pagination data here
    P=[]
    # Tab Relations = []
    
    # Generation of pagination data completed
    collectordata={}
    collectordata.update({"COLLECTOR_PERIOD":get_period_data(current_user.id,db.engine,Interface)})
    return render_template('domains.html', form=form, row=row, P=P,collectordata=collectordata)    
# ======================================================================



# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2022-03-23 18:29:43.173412
# ======================================================================        
# gen_views_delete.html:AG 2022-03-23 18:29:43.173432
@main.route('/forms/Domains_delete', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DELETE)
@admin_required
def forms_Domains_delete():
    """ Delete record handling function for table Domains """
    logger.debug('forms_Domains_delete(): Enter')
    Domain_Id  =  request.args.get('Domain_Id',0,type=int)
    row =  domains.query.filter(domains.Domain_Id == Domain_Id).first()

    if row is None:
        row=domains()
    session['data'] =  {  'Domain_Id':row.Domain_Id, 'Name':row.Name, 'Comments':row.Comments }
                       
    form = frm_domains_delete()

    # Tab['has_fks'] False
    
            
    # Actual Form activation here
    if form.validate_on_submit():
    
    # Code for SAVE option
        if  form.submit_Delete.data:
            print('Delete Data Here...')

    
    #f.write(        "            print('Delete Data Here...')
            try:
                session['deleted_row']=str(row)
                db.session.flush()
                db.session.delete(row)
                db.session.commit()
                db.session.flush()
                logger.audit ( '%s:DEL:%s' % (current_user.username,session['deleted_row']) )
                flash('Domains Domain_Id deleted OK')
            except exc.IntegrityError as e:
                db.session.rollback()    
                flash('INTEGRITY ERROR: Are you sure there are no dependant records in other tables?')
                return redirect(url_for('.forms_Domains_delete',Domain_Id=session['data']['Domain_Id']))    
    
            return redirect(url_for('.select_Domains_query'))    
    # Code for CANCEL option 
        elif   form.submit_Cancel.data:
            print('Cancel Data Here ... does nothing')
            flash('Record modifications discarded ...')
            return redirect(url_for('.select_Domains_query'))    
    # Code for ANY OTHER option should never get here
        else:
            print('form validated but not submited ???')
            return redirect(url_for('.select_Domains_query'))    
    
    logger.debug('forms_Domains_delete(): Exit')
    collectordata={}
    collectordata.update({"COLLECTOR_PERIOD":get_period_data(current_user.id,db.engine,Interface)})
    return render_template('domains_delete.html', form=form, data=session.get('data'),row=row,collectordata=collectordata)
#===============================================================================

# table_name: Domains
# class_name: domains
# is shardened: False
# current_app: 
# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2022-03-23 18:29:43.194788
# ======================================================================

# gen_views_select_query.html:AG 2022-03-23 18:29:43.194805        
@main.route('/select/Domains_Query', methods=['GET','POST'])
@login_required
@admin_required
def select_Domains_query():
    """ Select rows handling function for table 'Domains' """
    logger.debug('select_Domains_query(): Enter')
    #chk_c000001(filename=os.path.join(current_app.root_path, '.c000001'),request=request,db=db,logger=logger)
    # Shardening Code goes her if needed
    collectordata={}
    collectordata.update({"COLLECTOR_PERIOD":get_period_data(current_user.id,db.engine,Interface)})
    collectordata.update({"CONFIG":current_app.config})
    suffix = collectordata['COLLECTOR_PERIOD']['active']
    table_name='Domains'
    class_name='domains'
    template_name='Domains'
    sharding=False


    logger.debug("-----------------------------------------------------------")
    logger.debug("%s: template_name            = %s",__name__,template_name)

    logger.debug("-----------------------------------------------------------")    
        
    # Get parameters from URL call
    ia       =  request.args.get('ia',     None,type=str)
    if ia is not None:
        ia=ia.split(',')
        if ia[0]=='ORDER':
            #set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name='domains',Option_Type=OPTION_ORDER_BY,Argument_1=ia[1],Argument_2=ia[2])
            set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name=class_name,Option_Type=OPTION_ORDER_BY,Argument_1=ia[1],Argument_2=ia[2])
        elif ia[0]=='GROUP':
            #set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name='domains',Option_Type=OPTION_GROUP_BY,Argument_1=ia[1])
            set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name=class_name,Option_Type=OPTION_GROUP_BY,Argument_1=ia[1])
        elif ia[0]=='LIMIT':
            #set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name='domains',Option_Type=OPTION_LIMIT,Argument_1=ia[1])
            set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name=class_name,Option_Type=OPTION_LIMIT,Argument_1=ia[1])

    iad      =  request.args.get('iad',     None,type=int)
    if iad is not None: delete_query_option(engine=db.engine,Interface=Interface,Id=iad) 
    
    field    =  request.args.get('field',   None,type=str)
    value    =  request.args.get('value',   None,type=str)
    
    # Populates a list of foreign keys used for advanced filtering
    # ------------------------------------------------------------------
    foreign_keys={}
    
    # ------------------------------------------------------------------
    
    if field is not None:
        reset_query_options(    engine=db.engine,Interface=Interface,
                                User_Id=current_user.id,
                                #Table_name='domains'
                                Table_name=class_name
                                )

        
        if field in foreign_keys.keys():
            Class,referenced_classname,referenced_Field,referenced_Value,column_Header=foreign_keys[field]
            foreign_field='%s.%s:%s'%(referenced_classname,referenced_Value,column_Header)
            foreign_record=Class.query.get(value)
            foreign_description="'%s'"%getattr(foreign_record,referenced_Value)
        set_query_option(   engine=db.engine,Interface=Interface,
                        User_Id=current_user.id,
                        Table_name=class_name,
                        Option_Type=OPTION_FILTER,
                        Argument_1=foreign_field,
                        Argument_2='==',
                        Argument_3=foreign_description
                        )
    page     =  request.args.get('page',    1   ,type=int)
    addx     =  request.args.get('add.x',   None,type=int)
    addy     =  request.args.get('add.y',   None,type=int)
    exportx  =  request.args.get('export.x',None,type=int)
    exporty  =  request.args.get('export.y',None,type=int)
    filterx  =  request.args.get('filter.x',None,type=int)
    filtery  =  request.args.get('filter.y',None,type=int)
    # Select excluyent view mode
    if   addx    is not None: mode = 'add'
    elif exportx is not None: mode = 'export'
    elif filterx is not None: mode = 'filter'
    else:                     mode = 'select'
    Domain_Id =  request.args.get('Domain_Id',None,type=str)
    Name =  request.args.get('Name',None,type=str)
    Comments =  request.args.get('Comments',None,type=str)
    
    # Build default query all fields from table
    

    if Domain_Id is not None and len(Domain_Id)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='Domain_Id:Domain_Id',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%Domain_Id
                )
    
    
    if Name is not None and len(Name)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='Name:Name',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%Name
                )
    
    
    if Comments is not None and len(Comments)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='Comments:Comments',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%Comments
                )
    
    
    
    statement_query,options=get_query_options(engine=db.engine,Interface=Interface,Table_name=class_name,User_Id=current_user.id)
    tracebox_log(statement_query,logger,length=80)
    query=eval(statement_query)
    filtered_query = query    
    if mode == 'filter':
        query=filtered_query
    elif mode == 'export':
        query=filtered_query
        fh,output_file = tempfile.mkstemp(suffix='', prefix='%s_'%table_name, dir=None, text=False)
        dict = {'header':{},'detail':[]}
        count = 0
        rows = query.all()
        for row in rows:
            dict['detail'].append({})
            for column in ['Domain_Id', 'Name', 'Comments']:
                dict['detail'][count].update( { column:str(row.__getattribute__(column))})
                
            count += 1
        dict['header'].update({'count':count})
        jsonarray      = json.dumps(dict)
        data           = json.loads(jsonarray)  
        dataframe      = json_normalize(data, 'detail').assign(**data['header'])
        fh,output_file = tempfile.mkstemp(suffix='', prefix='%_'%table_name, dir='/tmp', text=False)
        xlsx_file      = '%s/%s'%(current_app.root_path,url_for('static',filename='%s.xls'%(output_file)))
        dataframe.to_excel(xlsx_file,sheet_name=table_name,columns=['Domain_Id', 'Name', 'Comments'])
        return send_file(xlsx_file,as_attachment=True,attachment_filename=output_file.replace('/','_')+'.xls')
    elif mode == 'add':
        return redirect(url_for('.forms_%s'%table_name))
    elif mode == 'select':
        pass
        # if some filter is required
        if field is not None:
            if field == 'Domain_Id':
                if value is not None:
                    query = query.filter_by(Domain_Id=value)
            if field == 'Name':
                if value is not None:
                    query = query.filter_by(Name=value)
            if field == 'Comments':
                if value is not None:
                    query = query.filter_by(Comments=value)
            
    # Actual request from DB follows
    tracebox_log(query,logger,length=80)
    # getting paginated rows for query
    rows = query.paginate(page, per_page=current_app.config['LINES_PER_PAGE'], error_out=False)
    # Setting pagination variables ...
    if field is not None:
       next_url = url_for('.select_%s_query'%template_name, field=field, value=value, page=rows.next_num) if rows.has_next else None
       prev_url = url_for('.select_%s_query'%template_name, field=field, value=value, page=rows.prev_num) if rows.has_prev else None
    else:
       next_url = url_for('.select_%s_query'%template_name, page=rows.next_num) if rows.has_next else None
       prev_url = url_for('.select_%s_query'%template_name, page=rows.prev_num) if rows.has_prev else None
    # Actual rendering ...
    if request.headers.get('Content-Type') is not None or request.args.get('JSON',None,type=str) is not None:
        # NOTE: needs review for JSONnifiyng output when needed (API Interface?)
        if "JSON" in request.headers.get('Content-Type') or request.args.get('JSON',None,type=str) is not None:
            logger.debug('select_%s_query(): will render: JSON rows'%template_name)
            logger.debug('select_%s_query(): Exit'%template_name)
            return json.dumps(serialize_object(rows.__dict__))
    logger.debug('select_%s_query(): will render: %s_All.html'%(template_name,table_name.lower()))
    logger.debug('select_%s_query(): Exit'%template_name)
    return render_template('%s_select_All.html'%template_name.lower(),rows=rows,options=options,collectordata=collectordata)
#===============================================================================
   
# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2022-03-23 18:29:43.230790
# ======================================================================
# gen_views_api.html:AG 2022-03-23 18:29:43.230808
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
        #response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        #response.headers['Pragma']        = 'no-cache'
        try:
            id_counter = 0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values=[id]
            # Codigo para un solo campo de id
            # chequear si marcado explicitamente
            db.session.flush()
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
            db.session.flush()
            db.session.refresh(row)
            db.session.flush()
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
                db.session.flush()
                db.session.refresh(row)
                db.session.flush()
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
                db.session.rollback()
                if request.values is not None and len(request.values):
                    if 'Name' in request.values:
                        row.Name = request.values.get('Name')
                    if 'Comments' in request.values:
                        row.Comments = request.values.get('Comments')
                # ----------------------------------------------------------
                db.session.merge(row)
                db.session.flush()
                db.session.commit()
                db.session.flush()
                db.session.refresh(row)
                db.session.flush()
                message = f"Modified 'Domains' Domain_Id = {id}"
                try:
                    row     = json.loads(row.get_json())
                except:
                    row     = None
            else:
                code    = API_NOT_FOUND
                message = f"Not found Domains with Domain_Id = {id}"
                row     = None
                db.session.rollback()
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
            row     = None
            db.session.rollback()
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
                db.session.flush()
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

# ======================================================================# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2022-03-23 18:29:41
# =============================================================================
# gen_views.py:32 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/views/view_interface.py
# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2022-03-23 18:29:43.394152
# ======================================================================        
# gen_views_form.html:AG 2022-03-23 18:29:43.394171
@main.route('/forms/Interface', methods=['GET', 'POST'])
@login_required

def forms_Interface():
    """ Form handling function for table Interface """
    logger.debug('forms_Interface(): Enter')
    
    # Shardening Code goes her if needed
    collectordata={}
    collectordata.update({"COLLECTOR_PERIOD":get_period_data(current_user.id,db.engine,Interface)})
    collectordata.update({"CONFIG":current_app.config})
    suffix = collectordata['COLLECTOR_PERIOD']['active']
    table_name='Interface'
    class_name='interface'
    template_name='Interface'
    sharding=False
    Id  =  request.args.get('Id',0,type=int)
    
    # Ensures DB Data is commited prior main query
    try:
        db.session.commit()
    except:
        db.session.rollback()
    row =  interface.query.filter(interface.Id == Id).first()
    if row is None:
        row=interface()
        session['is_new_row']=True
    session['data'] =  {  'Id':row.Id, 'User_Id':row.User_Id, 'Table_name':row.Table_name, 'Option_Type':row.Option_Type, 'Argument_1':row.Argument_1, 'Argument_2':row.Argument_2, 'Argument_3':row.Argument_3, 'Is_Active':row.Is_Active }
    
    form = frm_interface()
    
    # Actual Form activation here
    if form.validate_on_submit():
        # Code for SAVE option -----------------------------------------
        if form.submit_Save.data and current_user.role_id > 1:
            
            row.User_Id = form.User_Id.data
            row.Table_name = form.Table_name.data
            row.Option_Type = form.Option_Type.data
            row.Argument_1 = form.Argument_1.data
            row.Argument_2 = form.Argument_2.data
            row.Argument_3 = form.Argument_3.data
            row.Is_Active = form.Is_Active.data
            try:
               session['new_row']=str(row)
               db.session.flush()
               db.session.add(row)
               db.session.commit()
               db.session.flush()
               if session['is_new_row']==True:
                   logger.audit ( '%s:NEW:%s' % (current_user.username,session['new_row'] ) )
                   flash('New Interface created OK')
               else:
                   logger.audit ( '%s:OLD:%s' % (current_user.username,session['prev_row']) )
                   logger.audit ( '%s:UPD:%s' % (current_user.username,session['new_row'] ) )    
                   message=Markup('<b>Interface Id saved OK</b>')
                   flash(message)
               db.session.flush()
            except Exception as e:
               db.session.rollback()
               db.session.flush()
               message=Markup('ERROR saving Interface record : %s'%(e))
               flash(message)
            return redirect(url_for('.select_Interface_query'))
        # --------------------------------------------------------------
        # Code for NEW option
        # GV 20190109 f.write(        "        elif   form.submit_New.data:\n")
        elif   form.submit_New.data and current_user.role_id>1:
            #print('New Data Here ...')
            session['is_new_row']=True
            db.session.flush()
            row=interface()
    
            return redirect(url_for('.forms_Interface',Id=row.Id))
    
        # Code for CANCEL option 
        elif   form.submit_Cancel.data:
            #print('Cancel Data Here ... does nothing')
            message=Markup('Interface Record modifications discarded ...')
            flash(message)
        # Code for ANY OTHER option should never get here
        else:
            #print('form validated but not submited ???')
            message=Markup("<b>Interface data modifications not allowed for user '%s'. Please contact EG Suite's Administrator ...</b>"%(current_user.username))    
            flash(message)
    
            return redirect(url_for('.forms_Interface',Id=row.Id))
    
    
    form.User_Id.data = row.User_Id
    form.Table_name.data = row.Table_name
    form.Option_Type.data = row.Option_Type
    form.Argument_1.data = row.Argument_1
    form.Argument_2.data = row.Argument_2
    form.Argument_3.data = row.Argument_3
    form.Is_Active.data = row.Is_Active
    session['prev_row'] = str(row)
    session['is_new_row'] = False
    logger.debug('forms_Interface(): Exit')
    # Generates pagination data here
    P=[]
    # Tab Relations = []
    
    # Generation of pagination data completed
    collectordata={}
    collectordata.update({"COLLECTOR_PERIOD":get_period_data(current_user.id,db.engine,Interface)})
    return render_template('interface.html', form=form, row=row, P=P,collectordata=collectordata)    
# ======================================================================



# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2022-03-23 18:29:43.406750
# ======================================================================        
# gen_views_delete.html:AG 2022-03-23 18:29:43.406769
@main.route('/forms/Interface_delete', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DELETE)
@admin_required
def forms_Interface_delete():
    """ Delete record handling function for table Interface """
    logger.debug('forms_Interface_delete(): Enter')
    Id  =  request.args.get('Id',0,type=int)
    row =  interface.query.filter(interface.Id == Id).first()

    if row is None:
        row=interface()
    session['data'] =  {  'Id':row.Id, 'User_Id':row.User_Id, 'Table_name':row.Table_name, 'Option_Type':row.Option_Type, 'Argument_1':row.Argument_1, 'Argument_2':row.Argument_2, 'Argument_3':row.Argument_3, 'Is_Active':row.Is_Active }
                       
    form = frm_interface_delete()

    # Tab['has_fks'] False
    
            
    # Actual Form activation here
    if form.validate_on_submit():
    
    # Code for SAVE option
        if  form.submit_Delete.data:
            print('Delete Data Here...')

    
    #f.write(        "            print('Delete Data Here...')
            try:
                session['deleted_row']=str(row)
                db.session.flush()
                db.session.delete(row)
                db.session.commit()
                db.session.flush()
                logger.audit ( '%s:DEL:%s' % (current_user.username,session['deleted_row']) )
                flash('Interface Id deleted OK')
            except exc.IntegrityError as e:
                db.session.rollback()    
                flash('INTEGRITY ERROR: Are you sure there are no dependant records in other tables?')
                return redirect(url_for('.forms_Interface_delete',Id=session['data']['Id']))    
    
            return redirect(url_for('.select_Interface_query'))    
    # Code for CANCEL option 
        elif   form.submit_Cancel.data:
            print('Cancel Data Here ... does nothing')
            flash('Record modifications discarded ...')
            return redirect(url_for('.select_Interface_query'))    
    # Code for ANY OTHER option should never get here
        else:
            print('form validated but not submited ???')
            return redirect(url_for('.select_Interface_query'))    
    
    logger.debug('forms_Interface_delete(): Exit')
    collectordata={}
    collectordata.update({"COLLECTOR_PERIOD":get_period_data(current_user.id,db.engine,Interface)})
    return render_template('interface_delete.html', form=form, data=session.get('data'),row=row,collectordata=collectordata)
#===============================================================================

# table_name: Interface
# class_name: interface
# is shardened: False
# current_app: 
# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2022-03-23 18:29:43.433655
# ======================================================================

# gen_views_select_query.html:AG 2022-03-23 18:29:43.433674        
@main.route('/select/Interface_Query', methods=['GET','POST'])
@login_required
@admin_required
def select_Interface_query():
    """ Select rows handling function for table 'Interface' """
    logger.debug('select_Interface_query(): Enter')
    #chk_c000001(filename=os.path.join(current_app.root_path, '.c000001'),request=request,db=db,logger=logger)
    # Shardening Code goes her if needed
    collectordata={}
    collectordata.update({"COLLECTOR_PERIOD":get_period_data(current_user.id,db.engine,Interface)})
    collectordata.update({"CONFIG":current_app.config})
    suffix = collectordata['COLLECTOR_PERIOD']['active']
    table_name='Interface'
    class_name='interface'
    template_name='Interface'
    sharding=False


    logger.debug("-----------------------------------------------------------")
    logger.debug("%s: template_name            = %s",__name__,template_name)

    logger.debug("-----------------------------------------------------------")    
        
    # Get parameters from URL call
    ia       =  request.args.get('ia',     None,type=str)
    if ia is not None:
        ia=ia.split(',')
        if ia[0]=='ORDER':
            #set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name='interface',Option_Type=OPTION_ORDER_BY,Argument_1=ia[1],Argument_2=ia[2])
            set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name=class_name,Option_Type=OPTION_ORDER_BY,Argument_1=ia[1],Argument_2=ia[2])
        elif ia[0]=='GROUP':
            #set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name='interface',Option_Type=OPTION_GROUP_BY,Argument_1=ia[1])
            set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name=class_name,Option_Type=OPTION_GROUP_BY,Argument_1=ia[1])
        elif ia[0]=='LIMIT':
            #set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name='interface',Option_Type=OPTION_LIMIT,Argument_1=ia[1])
            set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name=class_name,Option_Type=OPTION_LIMIT,Argument_1=ia[1])

    iad      =  request.args.get('iad',     None,type=int)
    if iad is not None: delete_query_option(engine=db.engine,Interface=Interface,Id=iad) 
    
    field    =  request.args.get('field',   None,type=str)
    value    =  request.args.get('value',   None,type=str)
    
    # Populates a list of foreign keys used for advanced filtering
    # ------------------------------------------------------------------
    foreign_keys={}
    
    # ------------------------------------------------------------------
    
    if field is not None:
        reset_query_options(    engine=db.engine,Interface=Interface,
                                User_Id=current_user.id,
                                #Table_name='interface'
                                Table_name=class_name
                                )

        
        if field in foreign_keys.keys():
            Class,referenced_classname,referenced_Field,referenced_Value,column_Header=foreign_keys[field]
            foreign_field='%s.%s:%s'%(referenced_classname,referenced_Value,column_Header)
            foreign_record=Class.query.get(value)
            foreign_description="'%s'"%getattr(foreign_record,referenced_Value)
        set_query_option(   engine=db.engine,Interface=Interface,
                        User_Id=current_user.id,
                        Table_name=class_name,
                        Option_Type=OPTION_FILTER,
                        Argument_1=foreign_field,
                        Argument_2='==',
                        Argument_3=foreign_description
                        )
    page     =  request.args.get('page',    1   ,type=int)
    addx     =  request.args.get('add.x',   None,type=int)
    addy     =  request.args.get('add.y',   None,type=int)
    exportx  =  request.args.get('export.x',None,type=int)
    exporty  =  request.args.get('export.y',None,type=int)
    filterx  =  request.args.get('filter.x',None,type=int)
    filtery  =  request.args.get('filter.y',None,type=int)
    # Select excluyent view mode
    if   addx    is not None: mode = 'add'
    elif exportx is not None: mode = 'export'
    elif filterx is not None: mode = 'filter'
    else:                     mode = 'select'
    Id =  request.args.get('Id',None,type=str)
    User_Id =  request.args.get('User_Id',None,type=str)
    Table_name =  request.args.get('Table_name',None,type=str)
    Option_Type =  request.args.get('Option_Type',None,type=str)
    Argument_1 =  request.args.get('Argument_1',None,type=str)
    Argument_2 =  request.args.get('Argument_2',None,type=str)
    Argument_3 =  request.args.get('Argument_3',None,type=str)
    Is_Active =  request.args.get('Is_Active',None,type=str)
    
    # Build default query all fields from table
    

    if Id is not None and len(Id)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='Id:Id',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%Id
                )
    
    
    if User_Id is not None and len(User_Id)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='User_Id:User_Id',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%User_Id
                )
    
    
    if Table_name is not None and len(Table_name)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='Table_name:Table_name',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%Table_name
                )
    
    
    if Option_Type is not None and len(Option_Type)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='Option_Type:Option_Type',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%Option_Type
                )
    
    
    if Argument_1 is not None and len(Argument_1)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='Argument_1:Argument_1',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%Argument_1
                )
    
    
    if Argument_2 is not None and len(Argument_2)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='Argument_2:Argument_2',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%Argument_2
                )
    
    
    if Argument_3 is not None and len(Argument_3)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='Argument_3:Argument_3',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%Argument_3
                )
    
    
    if Is_Active is not None and len(Is_Active)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='Is_Active:Is_Active',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%Is_Active
                )
    
    
    
    statement_query,options=get_query_options(engine=db.engine,Interface=Interface,Table_name=class_name,User_Id=current_user.id)
    tracebox_log(statement_query,logger,length=80)
    query=eval(statement_query)
    filtered_query = query    
    if mode == 'filter':
        query=filtered_query
    elif mode == 'export':
        query=filtered_query
        fh,output_file = tempfile.mkstemp(suffix='', prefix='%s_'%table_name, dir=None, text=False)
        dict = {'header':{},'detail':[]}
        count = 0
        rows = query.all()
        for row in rows:
            dict['detail'].append({})
            for column in ['Id', 'User_Id', 'Table_name', 'Option_Type', 'Argument_1', 'Argument_2', 'Argument_3', 'Is_Active']:
                dict['detail'][count].update( { column:str(row.__getattribute__(column))})
                
            count += 1
        dict['header'].update({'count':count})
        jsonarray      = json.dumps(dict)
        data           = json.loads(jsonarray)  
        dataframe      = json_normalize(data, 'detail').assign(**data['header'])
        fh,output_file = tempfile.mkstemp(suffix='', prefix='%_'%table_name, dir='/tmp', text=False)
        xlsx_file      = '%s/%s'%(current_app.root_path,url_for('static',filename='%s.xls'%(output_file)))
        dataframe.to_excel(xlsx_file,sheet_name=table_name,columns=['Id', 'User_Id', 'Table_name', 'Option_Type', 'Argument_1', 'Argument_2', 'Argument_3', 'Is_Active'])
        return send_file(xlsx_file,as_attachment=True,attachment_filename=output_file.replace('/','_')+'.xls')
    elif mode == 'add':
        return redirect(url_for('.forms_%s'%table_name))
    elif mode == 'select':
        pass
        # if some filter is required
        if field is not None:
            if field == 'Id':
                if value is not None:
                    query = query.filter_by(Id=value)
            if field == 'User_Id':
                if value is not None:
                    query = query.filter_by(User_Id=value)
            if field == 'Table_name':
                if value is not None:
                    query = query.filter_by(Table_name=value)
            if field == 'Option_Type':
                if value is not None:
                    query = query.filter_by(Option_Type=value)
            if field == 'Argument_1':
                if value is not None:
                    query = query.filter_by(Argument_1=value)
            if field == 'Argument_2':
                if value is not None:
                    query = query.filter_by(Argument_2=value)
            if field == 'Argument_3':
                if value is not None:
                    query = query.filter_by(Argument_3=value)
            if field == 'Is_Active':
                if value is not None:
                    query = query.filter_by(Is_Active=value)
            
    # Actual request from DB follows
    tracebox_log(query,logger,length=80)
    # getting paginated rows for query
    rows = query.paginate(page, per_page=current_app.config['LINES_PER_PAGE'], error_out=False)
    # Setting pagination variables ...
    if field is not None:
       next_url = url_for('.select_%s_query'%template_name, field=field, value=value, page=rows.next_num) if rows.has_next else None
       prev_url = url_for('.select_%s_query'%template_name, field=field, value=value, page=rows.prev_num) if rows.has_prev else None
    else:
       next_url = url_for('.select_%s_query'%template_name, page=rows.next_num) if rows.has_next else None
       prev_url = url_for('.select_%s_query'%template_name, page=rows.prev_num) if rows.has_prev else None
    # Actual rendering ...
    if request.headers.get('Content-Type') is not None or request.args.get('JSON',None,type=str) is not None:
        # NOTE: needs review for JSONnifiyng output when needed (API Interface?)
        if "JSON" in request.headers.get('Content-Type') or request.args.get('JSON',None,type=str) is not None:
            logger.debug('select_%s_query(): will render: JSON rows'%template_name)
            logger.debug('select_%s_query(): Exit'%template_name)
            return json.dumps(serialize_object(rows.__dict__))
    logger.debug('select_%s_query(): will render: %s_All.html'%(template_name,table_name.lower()))
    logger.debug('select_%s_query(): Exit'%template_name)
    return render_template('%s_select_All.html'%template_name.lower(),rows=rows,options=options,collectordata=collectordata)
#===============================================================================
   
# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2022-03-23 18:29:43.495344
# ======================================================================
# gen_views_api.html:AG 2022-03-23 18:29:43.495364
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
        #response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        #response.headers['Pragma']        = 'no-cache'
        try:
            id_counter = 0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values=[id]
            # Codigo para un solo campo de id
            # chequear si marcado explicitamente
            db.session.flush()
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
            db.session.flush()
            db.session.refresh(row)
            db.session.flush()
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
                db.session.flush()
                db.session.refresh(row)
                db.session.flush()
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
                db.session.rollback()
                if request.values is not None and len(request.values):
                    if 'User_Id' in request.values:
                        row.User_Id = request.values.get('User_Id')
                    if 'Table_name' in request.values:
                        row.Table_name = request.values.get('Table_name')
                    if 'Option_Type' in request.values:
                        row.Option_Type = request.values.get('Option_Type')
                    if 'Argument_1' in request.values:
                        row.Argument_1 = request.values.get('Argument_1')
                    if 'Argument_2' in request.values:
                        row.Argument_2 = request.values.get('Argument_2')
                    if 'Argument_3' in request.values:
                        row.Argument_3 = request.values.get('Argument_3')
                    if 'Is_Active' in request.values:
                        row.Is_Active = request.values.get('Is_Active')
                # ----------------------------------------------------------
                db.session.merge(row)
                db.session.flush()
                db.session.commit()
                db.session.flush()
                db.session.refresh(row)
                db.session.flush()
                message = f"Modified 'Interface' Id = {id}"
                try:
                    row     = json.loads(row.get_json())
                except:
                    row     = None
            else:
                code    = API_NOT_FOUND
                message = f"Not found Interface with Id = {id}"
                row     = None
                db.session.rollback()
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
            row     = None
            db.session.rollback()
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
                db.session.flush()
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

# ======================================================================# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2022-03-23 18:29:41
# =============================================================================
# gen_views.py:32 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/views/view_migration_groups.py

# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2022-03-23 18:29:43.636561
# ======================================================================        
# gen_views_delete.html:AG 2022-03-23 18:29:43.636578
@main.route('/forms/Migration_Groups_delete', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DELETE)
@admin_required
def forms_Migration_Groups_delete():
    """ Delete record handling function for table Migration_Groups """
    logger.debug('forms_Migration_Groups_delete(): Enter')
    MG_Id  =  request.args.get('MG_Id',0,type=int)
    row =  migration_groups.query.filter(migration_groups.MG_Id == MG_Id).first()

    if row is None:
        row=migration_groups()
    session['data'] =  {  'MG_Id':row.MG_Id, 'Name':row.Name, 'Origin':row.Origin, 'Destiny':row.Destiny, 'Customer':row.Customer, 'Platform':row.Platform }
                       
    form = frm_migration_groups_delete()

    # Tab['has_fks'] False
    
            
    # Actual Form activation here
    if form.validate_on_submit():
    
    # Code for SAVE option
        if  form.submit_Delete.data:
            print('Delete Data Here...')

    
    #f.write(        "            print('Delete Data Here...')
            try:
                session['deleted_row']=str(row)
                db.session.flush()
                db.session.delete(row)
                db.session.commit()
                db.session.flush()
                logger.audit ( '%s:DEL:%s' % (current_user.username,session['deleted_row']) )
                flash('Migration_groups MG_Id deleted OK')
            except exc.IntegrityError as e:
                db.session.rollback()    
                flash('INTEGRITY ERROR: Are you sure there are no dependant records in other tables?')
                return redirect(url_for('.forms_Migration_Groups_delete',MG_Id=session['data']['MG_Id']))    
    
            return redirect(url_for('.select_Migration_Groups_query'))    
    # Code for CANCEL option 
        elif   form.submit_Cancel.data:
            print('Cancel Data Here ... does nothing')
            flash('Record modifications discarded ...')
            return redirect(url_for('.select_Migration_Groups_query'))    
    # Code for ANY OTHER option should never get here
        else:
            print('form validated but not submited ???')
            return redirect(url_for('.select_Migration_Groups_query'))    
    
    logger.debug('forms_Migration_Groups_delete(): Exit')
    collectordata={}
    collectordata.update({"COLLECTOR_PERIOD":get_period_data(current_user.id,db.engine,Interface)})
    return render_template('migration_groups_delete.html', form=form, data=session.get('data'),row=row,collectordata=collectordata)
#===============================================================================

# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2022-03-23 18:29:43.697125
# ======================================================================
# gen_views_api.html:AG 2022-03-23 18:29:43.697158
# table_name: Migration_Groups
# class_name: migration_groups
# is shardened: True
# Table 'Migration_Groups' keys = MG_Id
# Errors: None
# ID field found 'MG_Id' auto_increment db.Integer
# Migration_Groups id field is 'Migration_Groups.MG_Id' of type 'int:'

@main.route('/api/get/Migration_Groups'     , methods=['GET'])
@main.route('/api/get/Migration_Groups/<int:id>', methods=['GET'])
def api_get_Migration_Groups(id=None):
    code       = API_OK
    message    = 'OK'
    rows       = None
    authorized = api_check_authorization(request,current_app)
    if authorized:
        #response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        #response.headers['Pragma']        = 'no-cache'
        try:
            id_counter = 0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values=[id]
            # Codigo para un solo campo de id
            # chequear si marcado explicitamente
            db.session.flush()
            query = db.session.query(Migration_Groups)
            if id is not None:
                query = query.filter(Migration_Groups.MG_Id == id_values[id_counter])
                rows = query.one_or_none()
            else:
                if request.args is not None and len(request.args):
                    if 'MG_Id' in request.args:
                        query = query.filter(Migration_Groups.MG_Id == request.args.get('MG_Id'))
                    if 'Name' in request.args:
                        query = query.filter(Migration_Groups.Name == request.args.get('Name'))
                    if 'Origin' in request.args:
                        query = query.filter(Migration_Groups.Origin == request.args.get('Origin'))
                    if 'Destiny' in request.args:
                        query = query.filter(Migration_Groups.Destiny == request.args.get('Destiny'))
                    if 'Customer' in request.args:
                        query = query.filter(Migration_Groups.Customer == request.args.get('Customer'))
                    if 'Platform' in request.args:
                        query = query.filter(Migration_Groups.Platform == request.args.get('Platform'))
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
                    message = f"No 'Migration_Groups' records found"
                else:
                    message = f"No 'Migration_Groups.MG_Id' = {id} record found"
                
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Migration_Groups',entities=rows,name=current_app.config['NAME'])

@main.route('/api/post/Migration_Groups', methods=['POST'])
def api_post_Migration_Groups():
    code    = API_OK
    message = 'OK'
    row     = None
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            row = Migration_Groups()
            # Populates row from json, if ID=int:autoincrement then None
            row.MG_Id = None
            row.Name = request.json.get('Name',None)
            row.Origin = request.json.get('Origin',None)
            row.Destiny = request.json.get('Destiny',None)
            row.Customer = request.json.get('Customer',None)
            row.Platform = request.json.get('Platform',None)
            # ----------------------------------------------------------
            db.session.add(row)
            db.session.flush()
            db.session.commit()
            db.session.flush()
            db.session.refresh(row)
            db.session.flush()
            message = f"Created 'Migration_Groups' MG_Id = {row.MG_Id}"
            row     = json.loads(row.get_json())
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
            row     = None
    else:
        code    = API_ERROR
        message = 'Unauthorized request'            
    return get_api_response(code=code,message=message,kind='Migration_Groups',entities=[row],name=current_app.config['NAME'])

@main.route('/api/put/Migration_Groups/<int:id>', methods=['PUT'])
def api_put_Migration_Groups(id):
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
            row   = Migration_Groups()
            query = db.session.query(Migration_Groups)
            
            # First loop mandatory for row population ----------------------
            query = query.filter(Migration_Groups.MG_Id == id_values[id_counter])
            id_counter += 1
            # --------------------------------------------------------------
            row = query.one_or_none()
            # If row exists then continue:
            if row is not None:
                # Second loop seek for updated fields ----------------------
                if 'Name' in request.json.keys():
                    row.Name = request.json.get('Name')
                if 'Origin' in request.json.keys():
                    row.Origin = request.json.get('Origin')
                if 'Destiny' in request.json.keys():
                    row.Destiny = request.json.get('Destiny')
                if 'Customer' in request.json.keys():
                    row.Customer = request.json.get('Customer')
                if 'Platform' in request.json.keys():
                    row.Platform = request.json.get('Platform')
                # ----------------------------------------------------------
                db.session.merge(row)
                db.session.flush()
                db.session.commit()
                db.session.flush()
                db.session.refresh(row)
                db.session.flush()
                message = f"Modified 'Migration_Groups' MG_Id = {id}"
                row     = json.loads(row.get_json())
            else:
                code    = API_NOT_FOUND
                message = f"Not found Migration_Groups with MG_Id = {id}"
                row     = None
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Migration_Groups',entities=[row],name=current_app.config['NAME'])

@main.route('/api/patch/Migration_Groups/<int:id>', methods=['PATCH'])
def api_patch_Migration_Groups(id):
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
            row   = Migration_Groups()
            query = db.session.query(Migration_Groups)
            
            # First loop mandatory for row population ----------------------
            query = query.filter(Migration_Groups.MG_Id == id_values[id_counter])
            id_counter += 1
            # --------------------------------------------------------------
            row = query.one_or_none()
            # If row exists then continue:
            if row is not None:
                # Second loop seek for updated fields ----------------------
                db.session.rollback()
                if request.values is not None and len(request.values):
                    if 'Name' in request.values:
                        row.Name = request.values.get('Name')
                    if 'Origin' in request.values:
                        row.Origin = request.values.get('Origin')
                    if 'Destiny' in request.values:
                        row.Destiny = request.values.get('Destiny')
                    if 'Customer' in request.values:
                        row.Customer = request.values.get('Customer')
                    if 'Platform' in request.values:
                        row.Platform = request.values.get('Platform')
                # ----------------------------------------------------------
                db.session.merge(row)
                db.session.flush()
                db.session.commit()
                db.session.flush()
                db.session.refresh(row)
                db.session.flush()
                message = f"Modified 'Migration_Groups' MG_Id = {id}"
                try:
                    row     = json.loads(row.get_json())
                except:
                    row     = None
            else:
                code    = API_NOT_FOUND
                message = f"Not found Migration_Groups with MG_Id = {id}"
                row     = None
                db.session.rollback()
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
            row     = None
            db.session.rollback()
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Migration_Groups',entities=[row],name=current_app.config['NAME'])

@main.route('/api/delete/Migration_Groups/<int:id>', methods=['DELETE'])
def api_delete_Migration_Groups(id):
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
            row   = Migration_Groups()
            query = db.session.query(Migration_Groups)
            
            # First loop mandatory for row population ----------------------
            query = query.filter(Migration_Groups.MG_Id == id)
            # --------------------------------------------------------------
            row = query.one_or_none()

            if row is not None:
                db.session.delete(row)
                db.session.flush()
                db.session.commit()
                db.session.flush()
                message = f"Deleted 'Migration_Groups' MG_Id = {id}"
                row     = json.loads(row.get_json())
            else:
                code    = API_NOT_FOUND
                message = f"Not found 'Migration_Groups' with MG_Id = {id}"
                row     = None        
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Migration_Groups',entities=[],name=current_app.config['NAME'])

# ======================================================================# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2022-03-23 18:29:41
# =============================================================================
# gen_views.py:32 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/views/view_migration_groups_vm.py

# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2022-03-23 18:29:43.861057
# ======================================================================        
# gen_views_delete.html:AG 2022-03-23 18:29:43.861075
@main.route('/forms/Migration_Groups_VM_delete', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DELETE)
@admin_required
def forms_Migration_Groups_VM_delete():
    """ Delete record handling function for table Migration_Groups_VM """
    logger.debug('forms_Migration_Groups_VM_delete(): Enter')
    MG_Id  =  request.args.get('MG_Id',0,type=int)
    vm_uuid  =  request.args.get('vm_uuid',0,type=int)
    row =  migration_groups_vm.query.filter(migration_groups_vm.MG_Id == MG_Id,migration_groups_vm.vm_uuid == vm_uuid).first()

    if row is None:
        row=migration_groups_vm()
    session['data'] =  {  'MG_Id':row.MG_Id, 'vm_uuid':row.vm_uuid, 'vm_cluster_uuid':row.vm_cluster_uuid, 'vm_name':row.vm_name, 'vm_state':row.vm_state, 'vm_has_pd':row.vm_has_pd, 'vm_pd_name':row.vm_pd_name, 'vm_pd_active':row.vm_pd_active, 'vm_pd_replicating':row.vm_pd_replicating, 'vm_pd_schedules':row.vm_pd_schedules, 'vm_last_replication':row.vm_last_replication, 'vm_migrate':row.vm_migrate, 'vm_project':row.vm_project }
                       
    form = frm_migration_groups_vm_delete()

    # Tab['has_fks'] True
    
    pass # Tab['has_fks'] True
    
            
    # Actual Form activation here
    if form.validate_on_submit():
    
    # Code for SAVE option
        if  form.submit_Delete.data:
            print('Delete Data Here...')

    
    #f.write(        "            print('Delete Data Here...')
            try:
                session['deleted_row']=str(row)
                db.session.flush()
                db.session.delete(row)
                db.session.commit()
                db.session.flush()
                logger.audit ( '%s:DEL:%s' % (current_user.username,session['deleted_row']) )
                flash('Migration_groups_vm MG_Id,vm_uuid deleted OK')
            except exc.IntegrityError as e:
                db.session.rollback()    
                flash('INTEGRITY ERROR: Are you sure there are no dependant records in other tables?')
                return redirect(url_for('.forms_Migration_Groups_VM_delete',MG_Id=session['data']['MG_Id'],vm_uuid=session['data']['vm_uuid']))    
    
            return redirect(url_for('.select_Migration_Groups_VM_query'))    
    # Code for CANCEL option 
        elif   form.submit_Cancel.data:
            print('Cancel Data Here ... does nothing')
            flash('Record modifications discarded ...')
            return redirect(url_for('.select_Migration_Groups_VM_query'))    
    # Code for ANY OTHER option should never get here
        else:
            print('form validated but not submited ???')
            return redirect(url_for('.select_Migration_Groups_VM_query'))    
    
    logger.debug('forms_Migration_Groups_VM_delete(): Exit')
    collectordata={}
    collectordata.update({"COLLECTOR_PERIOD":get_period_data(current_user.id,db.engine,Interface)})
    return render_template('migration_groups_vm_delete.html', form=form, data=session.get('data'),row=row,collectordata=collectordata)
#===============================================================================

# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2022-03-23 18:29:43.918502
# ======================================================================
# gen_views_api.html:AG 2022-03-23 18:29:43.918521
# table_name: Migration_Groups_VM
# class_name: migration_groups_vm
# is shardened: True
# Table 'Migration_Groups_VM' keys = MG_Id,vm_uuid
# Errors: None
# PK field found 'MG_Id' db.Integer
# Errors: None
# PK field found 'vm_uuid' db.String(45)
# Migration_Groups_VM id field is 'Migration_Groups_VM.MG_Id' of type 'int:'

@main.route('/api/get/Migration_Groups_VM'     , methods=['GET'])
@main.route('/api/get/Migration_Groups_VM/<int:id>', methods=['GET'])
def api_get_Migration_Groups_VM(id=None):
    code       = API_OK
    message    = 'OK'
    rows       = None
    authorized = api_check_authorization(request,current_app)
    if authorized:
        #response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        #response.headers['Pragma']        = 'no-cache'
        try:
            id_counter = 0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values=[id]
            # Codigo para un solo campo de id
            # chequear si marcado explicitamente
            db.session.flush()
            query = db.session.query(Migration_Groups_VM)
            if id is not None:
                query = query.filter(Migration_Groups_VM.MG_Id == id_values[id_counter])
                rows = query.one_or_none()
            else:
                if request.args is not None and len(request.args):
                    if 'MG_Id' in request.args:
                        query = query.filter(Migration_Groups_VM.MG_Id == request.args.get('MG_Id'))
                    if 'vm_uuid' in request.args:
                        query = query.filter(Migration_Groups_VM.vm_uuid == request.args.get('vm_uuid'))
                    if 'vm_cluster_uuid' in request.args:
                        query = query.filter(Migration_Groups_VM.vm_cluster_uuid == request.args.get('vm_cluster_uuid'))
                    if 'vm_name' in request.args:
                        query = query.filter(Migration_Groups_VM.vm_name == request.args.get('vm_name'))
                    if 'vm_state' in request.args:
                        query = query.filter(Migration_Groups_VM.vm_state == request.args.get('vm_state'))
                    if 'vm_has_pd' in request.args:
                        query = query.filter(Migration_Groups_VM.vm_has_pd == request.args.get('vm_has_pd'))
                    if 'vm_pd_name' in request.args:
                        query = query.filter(Migration_Groups_VM.vm_pd_name == request.args.get('vm_pd_name'))
                    if 'vm_pd_active' in request.args:
                        query = query.filter(Migration_Groups_VM.vm_pd_active == request.args.get('vm_pd_active'))
                    if 'vm_pd_replicating' in request.args:
                        query = query.filter(Migration_Groups_VM.vm_pd_replicating == request.args.get('vm_pd_replicating'))
                    if 'vm_pd_schedules' in request.args:
                        query = query.filter(Migration_Groups_VM.vm_pd_schedules == request.args.get('vm_pd_schedules'))
                    if 'vm_last_replication' in request.args:
                        query = query.filter(Migration_Groups_VM.vm_last_replication == request.args.get('vm_last_replication'))
                    if 'vm_migrate' in request.args:
                        query = query.filter(Migration_Groups_VM.vm_migrate == request.args.get('vm_migrate'))
                    if 'vm_project' in request.args:
                        query = query.filter(Migration_Groups_VM.vm_project == request.args.get('vm_project'))
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
                    message = f"No 'Migration_Groups_VM' records found"
                else:
                    message = f"No 'Migration_Groups_VM.MG_Id' = {id} record found"
                
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Migration_Groups_VM',entities=rows,name=current_app.config['NAME'])

@main.route('/api/post/Migration_Groups_VM', methods=['POST'])
def api_post_Migration_Groups_VM():
    code    = API_OK
    message = 'OK'
    row     = None
    authorized = api_check_authorization(request,current_app)
    if authorized:
        try:
            row = Migration_Groups_VM()
            # Populates row from json, if ID=int:autoincrement then None
            row.MG_Id = request.json.get('MG_Id',None)
            row.vm_uuid = request.json.get('vm_uuid',None)
            row.vm_cluster_uuid = request.json.get('vm_cluster_uuid',None)
            row.vm_name = request.json.get('vm_name',None)
            row.vm_state = request.json.get('vm_state',1)
            row.vm_has_pd = request.json.get('vm_has_pd',0)
            row.vm_pd_name = request.json.get('vm_pd_name',None)
            row.vm_pd_active = request.json.get('vm_pd_active',0)
            row.vm_pd_replicating = request.json.get('vm_pd_replicating',0)
            row.vm_pd_schedules = request.json.get('vm_pd_schedules',0)
            row.vm_last_replication = request.json.get('vm_last_replication',None)
            row.vm_migrate = request.json.get('vm_migrate',0)
            row.vm_project = request.json.get('vm_project',None)
            # ----------------------------------------------------------
            db.session.add(row)
            db.session.flush()
            db.session.commit()
            db.session.flush()
            db.session.refresh(row)
            db.session.flush()
            message = f"Created 'Migration_Groups_VM' MG_Id = {row.MG_Id}"
            row     = json.loads(row.get_json())
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
            row     = None
    else:
        code    = API_ERROR
        message = 'Unauthorized request'            
    return get_api_response(code=code,message=message,kind='Migration_Groups_VM',entities=[row],name=current_app.config['NAME'])

@main.route('/api/put/Migration_Groups_VM/<int:id>', methods=['PUT'])
def api_put_Migration_Groups_VM(id):
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
            row   = Migration_Groups_VM()
            query = db.session.query(Migration_Groups_VM)
            
            # First loop mandatory for row population ----------------------
            query = query.filter(Migration_Groups_VM.MG_Id == id_values[id_counter])
            id_counter += 1
            query = query.filter(Migration_Groups_VM.vm_uuid == id_values[id_counter])
            id_counter += 1
            # --------------------------------------------------------------
            row = query.one_or_none()
            # If row exists then continue:
            if row is not None:
                # Second loop seek for updated fields ----------------------
                if 'vm_cluster_uuid' in request.json.keys():
                    row.vm_cluster_uuid = request.json.get('vm_cluster_uuid')
                if 'vm_name' in request.json.keys():
                    row.vm_name = request.json.get('vm_name')
                if 'vm_state' in request.json.keys():
                    row.vm_state = request.json.get('vm_state')
                if 'vm_has_pd' in request.json.keys():
                    row.vm_has_pd = request.json.get('vm_has_pd')
                if 'vm_pd_name' in request.json.keys():
                    row.vm_pd_name = request.json.get('vm_pd_name')
                if 'vm_pd_active' in request.json.keys():
                    row.vm_pd_active = request.json.get('vm_pd_active')
                if 'vm_pd_replicating' in request.json.keys():
                    row.vm_pd_replicating = request.json.get('vm_pd_replicating')
                if 'vm_pd_schedules' in request.json.keys():
                    row.vm_pd_schedules = request.json.get('vm_pd_schedules')
                if 'vm_last_replication' in request.json.keys():
                    row.vm_last_replication = request.json.get('vm_last_replication')
                if 'vm_migrate' in request.json.keys():
                    row.vm_migrate = request.json.get('vm_migrate')
                if 'vm_project' in request.json.keys():
                    row.vm_project = request.json.get('vm_project')
                # ----------------------------------------------------------
                db.session.merge(row)
                db.session.flush()
                db.session.commit()
                db.session.flush()
                db.session.refresh(row)
                db.session.flush()
                message = f"Modified 'Migration_Groups_VM' MG_Id = {id}"
                row     = json.loads(row.get_json())
            else:
                code    = API_NOT_FOUND
                message = f"Not found Migration_Groups_VM with MG_Id = {id}"
                row     = None
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Migration_Groups_VM',entities=[row],name=current_app.config['NAME'])

@main.route('/api/patch/Migration_Groups_VM/<int:id>', methods=['PATCH'])
def api_patch_Migration_Groups_VM(id):
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
            row   = Migration_Groups_VM()
            query = db.session.query(Migration_Groups_VM)
            
            # First loop mandatory for row population ----------------------
            query = query.filter(Migration_Groups_VM.MG_Id == id_values[id_counter])
            id_counter += 1
            query = query.filter(Migration_Groups_VM.vm_uuid == id_values[id_counter])
            id_counter += 1
            # --------------------------------------------------------------
            row = query.one_or_none()
            # If row exists then continue:
            if row is not None:
                # Second loop seek for updated fields ----------------------
                db.session.rollback()
                if request.values is not None and len(request.values):
                    if 'vm_cluster_uuid' in request.values:
                        row.vm_cluster_uuid = request.values.get('vm_cluster_uuid')
                    if 'vm_name' in request.values:
                        row.vm_name = request.values.get('vm_name')
                    if 'vm_state' in request.values:
                        row.vm_state = request.values.get('vm_state')
                    if 'vm_has_pd' in request.values:
                        row.vm_has_pd = request.values.get('vm_has_pd')
                    if 'vm_pd_name' in request.values:
                        row.vm_pd_name = request.values.get('vm_pd_name')
                    if 'vm_pd_active' in request.values:
                        row.vm_pd_active = request.values.get('vm_pd_active')
                    if 'vm_pd_replicating' in request.values:
                        row.vm_pd_replicating = request.values.get('vm_pd_replicating')
                    if 'vm_pd_schedules' in request.values:
                        row.vm_pd_schedules = request.values.get('vm_pd_schedules')
                    if 'vm_last_replication' in request.values:
                        row.vm_last_replication = request.values.get('vm_last_replication')
                    if 'vm_migrate' in request.values:
                        row.vm_migrate = request.values.get('vm_migrate')
                    if 'vm_project' in request.values:
                        row.vm_project = request.values.get('vm_project')
                # ----------------------------------------------------------
                db.session.merge(row)
                db.session.flush()
                db.session.commit()
                db.session.flush()
                db.session.refresh(row)
                db.session.flush()
                message = f"Modified 'Migration_Groups_VM' MG_Id = {id}"
                try:
                    row     = json.loads(row.get_json())
                except:
                    row     = None
            else:
                code    = API_NOT_FOUND
                message = f"Not found Migration_Groups_VM with MG_Id = {id}"
                row     = None
                db.session.rollback()
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
            row     = None
            db.session.rollback()
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Migration_Groups_VM',entities=[row],name=current_app.config['NAME'])

@main.route('/api/delete/Migration_Groups_VM/<int:id>', methods=['DELETE'])
def api_delete_Migration_Groups_VM(id):
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
            row   = Migration_Groups_VM()
            query = db.session.query(Migration_Groups_VM)
            
            # First loop mandatory for row population ----------------------
            # detected primary key field: c.field
            query       = query.filter(Migration_Groups_VM.MG_Id == id_values[id_counter])
            id_counter +=1
            # detected primary key field: c.field
            query       = query.filter(Migration_Groups_VM.vm_uuid == id_values[id_counter])
            id_counter +=1
            # --------------------------------------------------------------
            row = query.one_or_none()

            if row is not None:
                db.session.delete(row)
                db.session.flush()
                db.session.commit()
                db.session.flush()
                message = f"Deleted 'Migration_Groups_VM' MG_Id = {id}"
                row     = json.loads(row.get_json())
            else:
                code    = API_NOT_FOUND
                message = f"Not found 'Migration_Groups_VM' with MG_Id = {id}"
                row     = None        
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
    else:
        code    = API_ERROR
        message = 'Unauthorized request'
    return get_api_response(code=code,message=message,kind='Migration_Groups_VM',entities=[],name=current_app.config['NAME'])

# ======================================================================# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2022-03-23 18:29:41
# =============================================================================
# gen_views.py:32 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/views/view_nutanix_prism_vm.py
# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2022-03-23 18:29:44.187334
# ======================================================================        
# gen_views_form.html:AG 2022-03-23 18:29:44.187351
@main.route('/forms/Nutanix_Prism_VM', methods=['GET', 'POST'])
@login_required

def forms_Nutanix_Prism_VM():
    """ Form handling function for table Nutanix_Prism_VM """
    logger.debug('forms_Nutanix_Prism_VM(): Enter')
    
    # Shardening Code goes her if needed
    collectordata={}
    collectordata.update({"COLLECTOR_PERIOD":get_period_data(current_user.id,db.engine,Interface)})
    collectordata.update({"CONFIG":current_app.config})
    suffix = collectordata['COLLECTOR_PERIOD']['active']
    table_name='Nutanix_Prism_VM'
    class_name='nutanix_prism_vm'
    template_name='Nutanix_Prism_VM'
    sharding=False
    Request_Id  =  request.args.get('Request_Id',0,type=int)
    
    # Ensures DB Data is commited prior main query
    try:
        db.session.commit()
    except:
        db.session.rollback()
    row =  nutanix_prism_vm.query.filter(nutanix_prism_vm.Request_Id == Request_Id).first()
    if row is None:
        row=nutanix_prism_vm()
        session['is_new_row']=True
    session['data'] =  {  'Request_Id':row.Request_Id, 'project_uuid':row.project_uuid, 'category_name':row.category_name, 'cluster_uuid':row.cluster_uuid, 'vm_name':row.vm_name, 'power_state':row.power_state, 'vcpus_per_socket':row.vcpus_per_socket, 'num_sockets':row.num_sockets, 'memory_size_mib':row.memory_size_mib, 'memory_size_gib':row.memory_size_gib, 'Comments':row.Comments, 'vm_uuid':row.vm_uuid, 'vm_ip':row.vm_ip, 'subnet_uuid':row.subnet_uuid, 'vm_username':row.vm_username, 'vm_password':row.vm_password, 'backup_set_1':row.backup_set_1, 'backup_set_2':row.backup_set_2, 'backup_set_3':row.backup_set_3, 'disk_type':row.disk_type, 'disk_0_image':row.disk_0_image, 'disk_0_size':row.disk_0_size, 'disk_1_image':row.disk_1_image, 'disk_1_size':row.disk_1_size, 'disk_2_image':row.disk_2_image, 'disk_2_size':row.disk_2_size, 'disk_3_image':row.disk_3_image, 'disk_3_size':row.disk_3_size, 'disk_4_image':row.disk_4_image, 'disk_4_size':row.disk_4_size, 'disk_5_image':row.disk_5_image, 'disk_5_size':row.disk_5_size, 'disk_6_image':row.disk_6_image, 'disk_6_size':row.disk_6_size, 'disk_7_image':row.disk_7_image, 'disk_7_size':row.disk_7_size, 'disk_8_image':row.disk_8_image, 'disk_8_size':row.disk_8_size, 'disk_9_image':row.disk_9_image, 'disk_9_size':row.disk_9_size, 'disk_10_image':row.disk_10_image, 'disk_10_size':row.disk_10_size, 'disk_11_image':row.disk_11_image, 'disk_11_size':row.disk_11_size, 'vm_drp':row.vm_drp, 'vm_drp_remote':row.vm_drp_remote, 'vm_cdrom':row.vm_cdrom, 'drp_cluster_uuid':row.drp_cluster_uuid, 'nic_0_vlan':row.nic_0_vlan, 'nic_0_ip':row.nic_0_ip, 'nic_0_mac':row.nic_0_mac, 'nic_1_vlan':row.nic_1_vlan, 'nic_1_ip':row.nic_1_ip, 'nic_1_mac':row.nic_1_mac, 'nic_2_vlan':row.nic_2_vlan, 'nic_2_ip':row.nic_2_ip, 'nic_2_mac':row.nic_2_mac, 'nic_3_vlan':row.nic_3_vlan, 'nic_3_ip':row.nic_3_ip, 'nic_3_mac':row.nic_3_mac, 'request_text':row.request_text }
    
    form = frm_nutanix_prism_vm()
    
    if form.has_FKs:
        form.Request_Id.choices = db.session.query(requests.Request_Id,requests.Id).order_by(requests.Id).all()
        form.project_uuid.choices = db.session.query(projects.project_uuid,projects.project_name).order_by(projects.project_name).all()
        form.category_name.choices = db.session.query(categories.category_name,categories.category_description).order_by(categories.category_description).all()
        form.cluster_uuid.choices = db.session.query(clusters.cluster_uuid,clusters.cluster_name).order_by(clusters.cluster_name).all()
        form.subnet_uuid.choices = db.session.query(subnets.subnet_uuid,subnets.name).order_by(subnets.name).all()

    
    # Actual Form activation here
    if form.validate_on_submit():
        # Code for SAVE option -----------------------------------------
        if form.submit_Save.data and current_user.role_id > 1:
            row.Request_Id = form.Request_Id.data
            row.project_uuid = form.project_uuid.data
            row.category_name = form.category_name.data
            row.cluster_uuid = form.cluster_uuid.data
            row.vm_name = form.vm_name.data
            row.power_state = form.power_state.data
            row.vcpus_per_socket = form.vcpus_per_socket.data
            row.num_sockets = form.num_sockets.data
            row.memory_size_mib = form.memory_size_mib.data
            row.memory_size_gib = form.memory_size_gib.data
            row.Comments = form.Comments.data
            row.vm_uuid = form.vm_uuid.data
            row.vm_ip = form.vm_ip.data
            row.subnet_uuid = form.subnet_uuid.data
            row.vm_username = form.vm_username.data
            row.vm_password = form.vm_password.data
            row.backup_set_1 = form.backup_set_1.data
            row.backup_set_2 = form.backup_set_2.data
            row.backup_set_3 = form.backup_set_3.data
            row.disk_type = form.disk_type.data
            row.disk_0_image = form.disk_0_image.data
            row.disk_0_size = form.disk_0_size.data
            row.disk_1_image = form.disk_1_image.data
            row.disk_1_size = form.disk_1_size.data
            row.disk_2_image = form.disk_2_image.data
            row.disk_2_size = form.disk_2_size.data
            row.disk_3_image = form.disk_3_image.data
            row.disk_3_size = form.disk_3_size.data
            row.disk_4_image = form.disk_4_image.data
            row.disk_4_size = form.disk_4_size.data
            row.disk_5_image = form.disk_5_image.data
            row.disk_5_size = form.disk_5_size.data
            row.disk_6_image = form.disk_6_image.data
            row.disk_6_size = form.disk_6_size.data
            row.disk_7_image = form.disk_7_image.data
            row.disk_7_size = form.disk_7_size.data
            row.disk_8_image = form.disk_8_image.data
            row.disk_8_size = form.disk_8_size.data
            row.disk_9_image = form.disk_9_image.data
            row.disk_9_size = form.disk_9_size.data
            row.disk_10_image = form.disk_10_image.data
            row.disk_10_size = form.disk_10_size.data
            row.disk_11_image = form.disk_11_image.data
            row.disk_11_size = form.disk_11_size.data
            row.vm_drp = form.vm_drp.data
            row.vm_drp_remote = form.vm_drp_remote.data
            row.vm_cdrom = form.vm_cdrom.data
            row.drp_cluster_uuid = form.drp_cluster_uuid.data
            row.nic_0_vlan = form.nic_0_vlan.data
            row.nic_0_ip = form.nic_0_ip.data
            row.nic_0_mac = form.nic_0_mac.data
            row.nic_1_vlan = form.nic_1_vlan.data
            row.nic_1_ip = form.nic_1_ip.data
            row.nic_1_mac = form.nic_1_mac.data
            row.nic_2_vlan = form.nic_2_vlan.data
            row.nic_2_ip = form.nic_2_ip.data
            row.nic_2_mac = form.nic_2_mac.data
            row.nic_3_vlan = form.nic_3_vlan.data
            row.nic_3_ip = form.nic_3_ip.data
            row.nic_3_mac = form.nic_3_mac.data
            row.request_text = form.request_text.data
            try:
               session['new_row']=str(row)
               db.session.flush()
               db.session.add(row)
               db.session.commit()
               db.session.flush()
               if session['is_new_row']==True:
                   logger.audit ( '%s:NEW:%s' % (current_user.username,session['new_row'] ) )
                   flash('New Nutanix_prism_vm created OK')
               else:
                   logger.audit ( '%s:OLD:%s' % (current_user.username,session['prev_row']) )
                   logger.audit ( '%s:UPD:%s' % (current_user.username,session['new_row'] ) )    
                   message=Markup('<b>Nutanix_prism_vm Request_Id saved OK</b>')
                   flash(message)
               db.session.flush()
            except Exception as e:
               db.session.rollback()
               db.session.flush()
               message=Markup('ERROR saving Nutanix_prism_vm record : %s'%(e))
               flash(message)
            return redirect(url_for('.select_Nutanix_Prism_VM_query'))
        # --------------------------------------------------------------
        # Code for NEW option
        # GV 20190109 f.write(        "        elif   form.submit_New.data:\n")
        elif   form.submit_New.data and current_user.role_id>1:
            #print('New Data Here ...')
            session['is_new_row']=True
            db.session.flush()
            row=nutanix_prism_vm()
    
            return redirect(url_for('.forms_Nutanix_Prism_VM'))    
    
        # Code for CANCEL option 
        elif   form.submit_Cancel.data:
            #print('Cancel Data Here ... does nothing')
            message=Markup('Nutanix_prism_vm Record modifications discarded ...')
            flash(message)
        # Code for ANY OTHER option should never get here
        else:
            #print('form validated but not submited ???')
            message=Markup("<b>Nutanix_prism_vm data modifications not allowed for user '%s'. Please contact EG Suite's Administrator ...</b>"%(current_user.username))    
            flash(message)
    
            return redirect(url_for('.forms_'))    
    
    
    form.Request_Id.data = row.Request_Id
    form.project_uuid.data = row.project_uuid
    form.category_name.data = row.category_name
    form.cluster_uuid.data = row.cluster_uuid
    form.vm_name.data = row.vm_name
    form.power_state.data = row.power_state
    form.vcpus_per_socket.data = row.vcpus_per_socket
    form.num_sockets.data = row.num_sockets
    form.memory_size_mib.data = row.memory_size_mib
    form.memory_size_gib.data = row.memory_size_gib
    form.Comments.data = row.Comments
    form.vm_uuid.data = row.vm_uuid
    form.vm_ip.data = row.vm_ip
    form.subnet_uuid.data = row.subnet_uuid
    form.vm_username.data = row.vm_username
    form.vm_password.data = row.vm_password
    form.backup_set_1.data = row.backup_set_1
    form.backup_set_2.data = row.backup_set_2
    form.backup_set_3.data = row.backup_set_3
    form.disk_type.data = row.disk_type
    form.disk_0_image.data = row.disk_0_image
    form.disk_0_size.data = row.disk_0_size
    form.disk_1_image.data = row.disk_1_image
    form.disk_1_size.data = row.disk_1_size
    form.disk_2_image.data = row.disk_2_image
    form.disk_2_size.data = row.disk_2_size
    form.disk_3_image.data = row.disk_3_image
    form.disk_3_size.data = row.disk_3_size
    form.disk_4_image.data = row.disk_4_image
    form.disk_4_size.data = row.disk_4_size
    form.disk_5_image.data = row.disk_5_image
    form.disk_5_size.data = row.disk_5_size
    form.disk_6_image.data = row.disk_6_image
    form.disk_6_size.data = row.disk_6_size
    form.disk_7_image.data = row.disk_7_image
    form.disk_7_size.data = row.disk_7_size
    form.disk_8_image.data = row.disk_8_image
    form.disk_8_size.data = row.disk_8_size
    form.disk_9_image.data = row.disk_9_image
    form.disk_9_size.data = row.disk_9_size
    form.disk_10_image.data = row.disk_10_image
    form.disk_10_size.data = row.disk_10_size
    form.disk_11_image.data = row.disk_11_image
    form.disk_11_size.data = row.disk_11_size
    form.vm_drp.data = row.vm_drp
    form.vm_drp_remote.data = row.vm_drp_remote
    form.vm_cdrom.data = row.vm_cdrom
    form.drp_cluster_uuid.data = row.drp_cluster_uuid
    form.nic_0_vlan.data = row.nic_0_vlan
    form.nic_0_ip.data = row.nic_0_ip
    form.nic_0_mac.data = row.nic_0_mac
    form.nic_1_vlan.data = row.nic_1_vlan
    form.nic_1_ip.data = row.nic_1_ip
    form.nic_1_mac.data = row.nic_1_mac
    form.nic_2_vlan.data = row.nic_2_vlan
    form.nic_2_ip.data = row.nic_2_ip
    form.nic_2_mac.data = row.nic_2_mac
    form.nic_3_vlan.data = row.nic_3_vlan
    form.nic_3_ip.data = row.nic_3_ip
    form.nic_3_mac.data = row.nic_3_mac
    form.request_text.data = row.request_text
    session['prev_row'] = str(row)
    session['is_new_row'] = False
    logger.debug('forms_Nutanix_Prism_VM(): Exit')
    # Generates pagination data here
    P=[]
    # Tab Relations = []
    
    # Generation of pagination data completed
    collectordata={}
    collectordata.update({"COLLECTOR_PERIOD":get_period_data(current_user.id,db.engine,Interface)})
    return render_template('nutanix_prism_vm.html', form=form, row=row, P=P,collectordata=collectordata)    
# ======================================================================



# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2022-03-23 18:29:44.197119
# ======================================================================        
# gen_views_delete.html:AG 2022-03-23 18:29:44.197134
@main.route('/forms/Nutanix_Prism_VM_delete', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DELETE)
@admin_required
def forms_Nutanix_Prism_VM_delete():
    """ Delete record handling function for table Nutanix_Prism_VM """
    logger.debug('forms_Nutanix_Prism_VM_delete(): Enter')
    Request_Id  =  request.args.get('Request_Id',0,type=int)
    row =  nutanix_prism_vm.query.filter(nutanix_prism_vm.Request_Id == Request_Id).first()

    if row is None:
        row=nutanix_prism_vm()
    session['data'] =  {  'Request_Id':row.Request_Id, 'project_uuid':row.project_uuid, 'category_name':row.category_name, 'cluster_uuid':row.cluster_uuid, 'vm_name':row.vm_name, 'power_state':row.power_state, 'vcpus_per_socket':row.vcpus_per_socket, 'num_sockets':row.num_sockets, 'memory_size_mib':row.memory_size_mib, 'memory_size_gib':row.memory_size_gib, 'Comments':row.Comments, 'vm_uuid':row.vm_uuid, 'vm_ip':row.vm_ip, 'subnet_uuid':row.subnet_uuid, 'vm_username':row.vm_username, 'vm_password':row.vm_password, 'backup_set_1':row.backup_set_1, 'backup_set_2':row.backup_set_2, 'backup_set_3':row.backup_set_3, 'disk_type':row.disk_type, 'disk_0_image':row.disk_0_image, 'disk_0_size':row.disk_0_size, 'disk_1_image':row.disk_1_image, 'disk_1_size':row.disk_1_size, 'disk_2_image':row.disk_2_image, 'disk_2_size':row.disk_2_size, 'disk_3_image':row.disk_3_image, 'disk_3_size':row.disk_3_size, 'disk_4_image':row.disk_4_image, 'disk_4_size':row.disk_4_size, 'disk_5_image':row.disk_5_image, 'disk_5_size':row.disk_5_size, 'disk_6_image':row.disk_6_image, 'disk_6_size':row.disk_6_size, 'disk_7_image':row.disk_7_image, 'disk_7_size':row.disk_7_size, 'disk_8_image':row.disk_8_image, 'disk_8_size':row.disk_8_size, 'disk_9_image':row.disk_9_image, 'disk_9_size':row.disk_9_size, 'disk_10_image':row.disk_10_image, 'disk_10_size':row.disk_10_size, 'disk_11_image':row.disk_11_image, 'disk_11_size':row.disk_11_size, 'vm_drp':row.vm_drp, 'vm_drp_remote':row.vm_drp_remote, 'vm_cdrom':row.vm_cdrom, 'drp_cluster_uuid':row.drp_cluster_uuid, 'nic_0_vlan':row.nic_0_vlan, 'nic_0_ip':row.nic_0_ip, 'nic_0_mac':row.nic_0_mac, 'nic_1_vlan':row.nic_1_vlan, 'nic_1_ip':row.nic_1_ip, 'nic_1_mac':row.nic_1_mac, 'nic_2_vlan':row.nic_2_vlan, 'nic_2_ip':row.nic_2_ip, 'nic_2_mac':row.nic_2_mac, 'nic_3_vlan':row.nic_3_vlan, 'nic_3_ip':row.nic_3_ip, 'nic_3_mac':row.nic_3_mac, 'request_text':row.request_text }
                       
    form = frm_nutanix_prism_vm_delete()

    # Tab['has_fks'] True
    
    pass # Tab['has_fks'] True
    
            
    # Actual Form activation here
    if form.validate_on_submit():
    
    # Code for SAVE option
        if  form.submit_Delete.data:
            print('Delete Data Here...')

    
    #f.write(        "            print('Delete Data Here...')
            try:
                session['deleted_row']=str(row)
                db.session.flush()
                db.session.delete(row)
                db.session.commit()
                db.session.flush()
                logger.audit ( '%s:DEL:%s' % (current_user.username,session['deleted_row']) )
                flash('Nutanix_prism_vm Request_Id deleted OK')
            except exc.IntegrityError as e:
                db.session.rollback()    
                flash('INTEGRITY ERROR: Are you sure there are no dependant records in other tables?')
                return redirect(url_for('.forms_Nutanix_Prism_VM_delete',Request_Id=session['data']['Request_Id']))    
    
            return redirect(url_for('.select_Nutanix_Prism_VM_query'))    
    # Code for CANCEL option 
        elif   form.submit_Cancel.data:
            print('Cancel Data Here ... does nothing')
            flash('Record modifications discarded ...')
            return redirect(url_for('.select_Nutanix_Prism_VM_query'))    
    # Code for ANY OTHER option should never get here
        else:
            print('form validated but not submited ???')
            return redirect(url_for('.select_Nutanix_Prism_VM_query'))    
    
    logger.debug('forms_Nutanix_Prism_VM_delete(): Exit')
    collectordata={}
    collectordata.update({"COLLECTOR_PERIOD":get_period_data(current_user.id,db.engine,Interface)})
    return render_template('nutanix_prism_vm_delete.html', form=form, data=session.get('data'),row=row,collectordata=collectordata)
#===============================================================================

# table_name: Nutanix_Prism_VM
# class_name: nutanix_prism_vm
# is shardened: False
# current_app: 
# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2022-03-23 18:29:44.217547
# ======================================================================

# gen_views_select_query.html:AG 2022-03-23 18:29:44.217565        
@main.route('/select/Nutanix_Prism_VM_Query', methods=['GET','POST'])
@login_required
@admin_required
def select_Nutanix_Prism_VM_query():
    """ Select rows handling function for table 'Nutanix_Prism_VM' """
    logger.debug('select_Nutanix_Prism_VM_query(): Enter')
    #chk_c000001(filename=os.path.join(current_app.root_path, '.c000001'),request=request,db=db,logger=logger)
    # Shardening Code goes her if needed
    collectordata={}
    collectordata.update({"COLLECTOR_PERIOD":get_period_data(current_user.id,db.engine,Interface)})
    collectordata.update({"CONFIG":current_app.config})
    suffix = collectordata['COLLECTOR_PERIOD']['active']
    table_name='Nutanix_Prism_VM'
    class_name='nutanix_prism_vm'
    template_name='Nutanix_Prism_VM'
    sharding=False


    logger.debug("-----------------------------------------------------------")
    logger.debug("%s: template_name            = %s",__name__,template_name)

    logger.debug("-----------------------------------------------------------")    
        
    # Get parameters from URL call
    ia       =  request.args.get('ia',     None,type=str)
    if ia is not None:
        ia=ia.split(',')
        if ia[0]=='ORDER':
            #set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name='nutanix_prism_vm',Option_Type=OPTION_ORDER_BY,Argument_1=ia[1],Argument_2=ia[2])
            set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name=class_name,Option_Type=OPTION_ORDER_BY,Argument_1=ia[1],Argument_2=ia[2])
        elif ia[0]=='GROUP':
            #set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name='nutanix_prism_vm',Option_Type=OPTION_GROUP_BY,Argument_1=ia[1])
            set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name=class_name,Option_Type=OPTION_GROUP_BY,Argument_1=ia[1])
        elif ia[0]=='LIMIT':
            #set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name='nutanix_prism_vm',Option_Type=OPTION_LIMIT,Argument_1=ia[1])
            set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name=class_name,Option_Type=OPTION_LIMIT,Argument_1=ia[1])

    iad      =  request.args.get('iad',     None,type=int)
    if iad is not None: delete_query_option(engine=db.engine,Interface=Interface,Id=iad) 
    
    field    =  request.args.get('field',   None,type=str)
    value    =  request.args.get('value',   None,type=str)
    
    # Populates a list of foreign keys used for advanced filtering
    # ------------------------------------------------------------------
    foreign_keys={}
    
    foreign_keys.update({'Request_Id':(requests,'requests','Id','Id','Request_Id')})
    foreign_keys.update({'project_uuid':(projects,'projects','project_uuid','project_name','project_uuid')})
    foreign_keys.update({'category_name':(categories,'categories','category_name','category_description','category_name')})
    foreign_keys.update({'cluster_uuid':(clusters,'clusters','cluster_uuid','cluster_name','cluster_uuid')})
    foreign_keys.update({'subnet_uuid':(subnets,'subnets','uuid','name','subnet_uuid')})
    # ------------------------------------------------------------------
    
    if field is not None:
        reset_query_options(    engine=db.engine,Interface=Interface,
                                User_Id=current_user.id,
                                #Table_name='nutanix_prism_vm'
                                Table_name=class_name
                                )

        
        if field in foreign_keys.keys():
            Class,referenced_classname,referenced_Field,referenced_Value,column_Header=foreign_keys[field]
            foreign_field='%s.%s:%s'%(referenced_classname,referenced_Value,column_Header)
            foreign_record=Class.query.get(value)
            foreign_description="'%s'"%getattr(foreign_record,referenced_Value)
        set_query_option(   engine=db.engine,Interface=Interface,
                        User_Id=current_user.id,
                        Table_name=class_name,
                        Option_Type=OPTION_FILTER,
                        Argument_1=foreign_field,
                        Argument_2='==',
                        Argument_3=foreign_description
                        )
    page     =  request.args.get('page',    1   ,type=int)
    addx     =  request.args.get('add.x',   None,type=int)
    addy     =  request.args.get('add.y',   None,type=int)
    exportx  =  request.args.get('export.x',None,type=int)
    exporty  =  request.args.get('export.y',None,type=int)
    filterx  =  request.args.get('filter.x',None,type=int)
    filtery  =  request.args.get('filter.y',None,type=int)
    # Select excluyent view mode
    if   addx    is not None: mode = 'add'
    elif exportx is not None: mode = 'export'
    elif filterx is not None: mode = 'filter'
    else:                     mode = 'select'
    Request_Id =  request.args.get('Request_Id',None,type=str)
    project_uuid =  request.args.get('project_uuid',None,type=str)
    category_name =  request.args.get('category_name',None,type=str)
    cluster_uuid =  request.args.get('cluster_uuid',None,type=str)
    vm_name =  request.args.get('vm_name',None,type=str)
    power_state =  request.args.get('power_state',None,type=str)
    vcpus_per_socket =  request.args.get('vcpus_per_socket',None,type=str)
    num_sockets =  request.args.get('num_sockets',None,type=str)
    memory_size_mib =  request.args.get('memory_size_mib',None,type=str)
    memory_size_gib =  request.args.get('memory_size_gib',None,type=str)
    Comments =  request.args.get('Comments',None,type=str)
    vm_uuid =  request.args.get('vm_uuid',None,type=str)
    vm_ip =  request.args.get('vm_ip',None,type=str)
    subnet_uuid =  request.args.get('subnet_uuid',None,type=str)
    vm_username =  request.args.get('vm_username',None,type=str)
    vm_password =  request.args.get('vm_password',None,type=str)
    backup_set_1 =  request.args.get('backup_set_1',None,type=str)
    backup_set_2 =  request.args.get('backup_set_2',None,type=str)
    backup_set_3 =  request.args.get('backup_set_3',None,type=str)
    disk_type =  request.args.get('disk_type',None,type=str)
    disk_0_image =  request.args.get('disk_0_image',None,type=str)
    disk_0_size =  request.args.get('disk_0_size',None,type=str)
    disk_1_image =  request.args.get('disk_1_image',None,type=str)
    disk_1_size =  request.args.get('disk_1_size',None,type=str)
    disk_2_image =  request.args.get('disk_2_image',None,type=str)
    disk_2_size =  request.args.get('disk_2_size',None,type=str)
    disk_3_image =  request.args.get('disk_3_image',None,type=str)
    disk_3_size =  request.args.get('disk_3_size',None,type=str)
    disk_4_image =  request.args.get('disk_4_image',None,type=str)
    disk_4_size =  request.args.get('disk_4_size',None,type=str)
    disk_5_image =  request.args.get('disk_5_image',None,type=str)
    disk_5_size =  request.args.get('disk_5_size',None,type=str)
    disk_6_image =  request.args.get('disk_6_image',None,type=str)
    disk_6_size =  request.args.get('disk_6_size',None,type=str)
    disk_7_image =  request.args.get('disk_7_image',None,type=str)
    disk_7_size =  request.args.get('disk_7_size',None,type=str)
    disk_8_image =  request.args.get('disk_8_image',None,type=str)
    disk_8_size =  request.args.get('disk_8_size',None,type=str)
    disk_9_image =  request.args.get('disk_9_image',None,type=str)
    disk_9_size =  request.args.get('disk_9_size',None,type=str)
    disk_10_image =  request.args.get('disk_10_image',None,type=str)
    disk_10_size =  request.args.get('disk_10_size',None,type=str)
    disk_11_image =  request.args.get('disk_11_image',None,type=str)
    disk_11_size =  request.args.get('disk_11_size',None,type=str)
    vm_drp =  request.args.get('vm_drp',None,type=str)
    vm_drp_remote =  request.args.get('vm_drp_remote',None,type=str)
    vm_cdrom =  request.args.get('vm_cdrom',None,type=str)
    drp_cluster_uuid =  request.args.get('drp_cluster_uuid',None,type=str)
    nic_0_vlan =  request.args.get('nic_0_vlan',None,type=str)
    nic_0_ip =  request.args.get('nic_0_ip',None,type=str)
    nic_0_mac =  request.args.get('nic_0_mac',None,type=str)
    nic_1_vlan =  request.args.get('nic_1_vlan',None,type=str)
    nic_1_ip =  request.args.get('nic_1_ip',None,type=str)
    nic_1_mac =  request.args.get('nic_1_mac',None,type=str)
    nic_2_vlan =  request.args.get('nic_2_vlan',None,type=str)
    nic_2_ip =  request.args.get('nic_2_ip',None,type=str)
    nic_2_mac =  request.args.get('nic_2_mac',None,type=str)
    nic_3_vlan =  request.args.get('nic_3_vlan',None,type=str)
    nic_3_ip =  request.args.get('nic_3_ip',None,type=str)
    nic_3_mac =  request.args.get('nic_3_mac',None,type=str)
    request_text =  request.args.get('request_text',None,type=str)
    
    # Build default query all fields from table
    

    if Request_Id is not None and len(Request_Id)>0:
            Class,referenced_classname,referenced_Field,referenced_Value,column_Header=foreign_keys['Request_Id']
            foreign_field='%s.%s:%s'%(referenced_classname,referenced_Value,column_Header)            
            set_query_option(   engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1=foreign_field,
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%Request_Id
                )
                                
    
    
    if project_uuid is not None and len(project_uuid)>0:
            Class,referenced_classname,referenced_Field,referenced_Value,column_Header=foreign_keys['project_uuid']
            foreign_field='%s.%s:%s'%(referenced_classname,referenced_Value,column_Header)            
            set_query_option(   engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1=foreign_field,
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%project_uuid
                )
                                
    
    
    if category_name is not None and len(category_name)>0:
            Class,referenced_classname,referenced_Field,referenced_Value,column_Header=foreign_keys['category_name']
            foreign_field='%s.%s:%s'%(referenced_classname,referenced_Value,column_Header)            
            set_query_option(   engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1=foreign_field,
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%category_name
                )
                                
    
    
    if cluster_uuid is not None and len(cluster_uuid)>0:
            Class,referenced_classname,referenced_Field,referenced_Value,column_Header=foreign_keys['cluster_uuid']
            foreign_field='%s.%s:%s'%(referenced_classname,referenced_Value,column_Header)            
            set_query_option(   engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1=foreign_field,
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%cluster_uuid
                )
                                
    
    
    if vm_name is not None and len(vm_name)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='vm_name:vm_name',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%vm_name
                )
    
    
    if power_state is not None and len(power_state)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='power_state:power_state',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%power_state
                )
    
    
    if vcpus_per_socket is not None and len(vcpus_per_socket)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='vcpus_per_socket:vcpus_per_socket',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%vcpus_per_socket
                )
    
    
    if num_sockets is not None and len(num_sockets)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='num_sockets:num_sockets',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%num_sockets
                )
    
    
    if memory_size_mib is not None and len(memory_size_mib)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='memory_size_mib:memory_size_mib',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%memory_size_mib
                )
    
    
    if memory_size_gib is not None and len(memory_size_gib)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='memory_size_gib:memory_size_gib',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%memory_size_gib
                )
    
    
    if Comments is not None and len(Comments)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='Comments:Comments',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%Comments
                )
    
    
    if vm_uuid is not None and len(vm_uuid)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='vm_uuid:vm_uuid',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%vm_uuid
                )
    
    
    if vm_ip is not None and len(vm_ip)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='vm_ip:vm_ip',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%vm_ip
                )
    
    
    if subnet_uuid is not None and len(subnet_uuid)>0:
            Class,referenced_classname,referenced_Field,referenced_Value,column_Header=foreign_keys['subnet_uuid']
            foreign_field='%s.%s:%s'%(referenced_classname,referenced_Value,column_Header)            
            set_query_option(   engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1=foreign_field,
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%subnet_uuid
                )
                                
    
    
    if vm_username is not None and len(vm_username)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='vm_username:vm_username',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%vm_username
                )
    
    
    if vm_password is not None and len(vm_password)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='vm_password:vm_password',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%vm_password
                )
    
    
    if backup_set_1 is not None and len(backup_set_1)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='backup_set_1:backup_set_1',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%backup_set_1
                )
    
    
    if backup_set_2 is not None and len(backup_set_2)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='backup_set_2:backup_set_2',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%backup_set_2
                )
    
    
    if backup_set_3 is not None and len(backup_set_3)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='backup_set_3:backup_set_3',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%backup_set_3
                )
    
    
    if disk_type is not None and len(disk_type)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='disk_type:disk_type',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%disk_type
                )
    
    
    if disk_0_image is not None and len(disk_0_image)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='disk_0_image:disk_0_image',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%disk_0_image
                )
    
    
    if disk_0_size is not None and len(disk_0_size)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='disk_0_size:disk_0_size',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%disk_0_size
                )
    
    
    if disk_1_image is not None and len(disk_1_image)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='disk_1_image:disk_1_image',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%disk_1_image
                )
    
    
    if disk_1_size is not None and len(disk_1_size)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='disk_1_size:disk_1_size',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%disk_1_size
                )
    
    
    if disk_2_image is not None and len(disk_2_image)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='disk_2_image:disk_2_image',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%disk_2_image
                )
    
    
    if disk_2_size is not None and len(disk_2_size)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='disk_2_size:disk_2_size',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%disk_2_size
                )
    
    
    if disk_3_image is not None and len(disk_3_image)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='disk_3_image:disk_3_image',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%disk_3_image
                )
    
    
    if disk_3_size is not None and len(disk_3_size)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='disk_3_size:disk_3_size',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%disk_3_size
                )
    
    
    if disk_4_image is not None and len(disk_4_image)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='disk_4_image:disk_4_image',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%disk_4_image
                )
    
    
    if disk_4_size is not None and len(disk_4_size)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='disk_4_size:disk_4_size',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%disk_4_size
                )
    
    
    if disk_5_image is not None and len(disk_5_image)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='disk_5_image:disk_5_image',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%disk_5_image
                )
    
    
    if disk_5_size is not None and len(disk_5_size)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='disk_5_size:disk_5_size',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%disk_5_size
                )
    
    
    if disk_6_image is not None and len(disk_6_image)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='disk_6_image:disk_6_image',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%disk_6_image
                )
    
    
    if disk_6_size is not None and len(disk_6_size)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='disk_6_size:disk_6_size',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%disk_6_size
                )
    
    
    if disk_7_image is not None and len(disk_7_image)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='disk_7_image:disk_7_image',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%disk_7_image
                )
    
    
    if disk_7_size is not None and len(disk_7_size)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='disk_7_size:disk_7_size',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%disk_7_size
                )
    
    
    if disk_8_image is not None and len(disk_8_image)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='disk_8_image:disk_8_image',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%disk_8_image
                )
    
    
    if disk_8_size is not None and len(disk_8_size)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='disk_8_size:disk_8_size',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%disk_8_size
                )
    
    
    if disk_9_image is not None and len(disk_9_image)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='disk_9_image:disk_9_image',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%disk_9_image
                )
    
    
    if disk_9_size is not None and len(disk_9_size)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='disk_9_size:disk_9_size',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%disk_9_size
                )
    
    
    if disk_10_image is not None and len(disk_10_image)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='disk_10_image:disk_10_image',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%disk_10_image
                )
    
    
    if disk_10_size is not None and len(disk_10_size)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='disk_10_size:disk_10_size',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%disk_10_size
                )
    
    
    if disk_11_image is not None and len(disk_11_image)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='disk_11_image:disk_11_image',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%disk_11_image
                )
    
    
    if disk_11_size is not None and len(disk_11_size)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='disk_11_size:disk_11_size',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%disk_11_size
                )
    
    
    if vm_drp is not None and len(vm_drp)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='vm_drp:vm_drp',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%vm_drp
                )
    
    
    if vm_drp_remote is not None and len(vm_drp_remote)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='vm_drp_remote:vm_drp_remote',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%vm_drp_remote
                )
    
    
    if vm_cdrom is not None and len(vm_cdrom)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='vm_cdrom:vm_cdrom',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%vm_cdrom
                )
    
    
    if drp_cluster_uuid is not None and len(drp_cluster_uuid)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='drp_cluster_uuid:drp_cluster_uuid',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%drp_cluster_uuid
                )
    
    
    if nic_0_vlan is not None and len(nic_0_vlan)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='nic_0_vlan:nic_0_vlan',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%nic_0_vlan
                )
    
    
    if nic_0_ip is not None and len(nic_0_ip)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='nic_0_ip:nic_0_ip',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%nic_0_ip
                )
    
    
    if nic_0_mac is not None and len(nic_0_mac)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='nic_0_mac:nic_0_mac',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%nic_0_mac
                )
    
    
    if nic_1_vlan is not None and len(nic_1_vlan)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='nic_1_vlan:nic_1_vlan',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%nic_1_vlan
                )
    
    
    if nic_1_ip is not None and len(nic_1_ip)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='nic_1_ip:nic_1_ip',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%nic_1_ip
                )
    
    
    if nic_1_mac is not None and len(nic_1_mac)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='nic_1_mac:nic_1_mac',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%nic_1_mac
                )
    
    
    if nic_2_vlan is not None and len(nic_2_vlan)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='nic_2_vlan:nic_2_vlan',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%nic_2_vlan
                )
    
    
    if nic_2_ip is not None and len(nic_2_ip)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='nic_2_ip:nic_2_ip',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%nic_2_ip
                )
    
    
    if nic_2_mac is not None and len(nic_2_mac)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='nic_2_mac:nic_2_mac',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%nic_2_mac
                )
    
    
    if nic_3_vlan is not None and len(nic_3_vlan)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='nic_3_vlan:nic_3_vlan',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%nic_3_vlan
                )
    
    
    if nic_3_ip is not None and len(nic_3_ip)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='nic_3_ip:nic_3_ip',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%nic_3_ip
                )
    
    
    if nic_3_mac is not None and len(nic_3_mac)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='nic_3_mac:nic_3_mac',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%nic_3_mac
                )
    
    
    if request_text is not None and len(request_text)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='request_text:request_text',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%request_text
                )
    
    
    
    statement_query,options=get_query_options(engine=db.engine,Interface=Interface,Table_name=class_name,User_Id=current_user.id)
    tracebox_log(statement_query,logger,length=80)
    query=eval(statement_query)
    filtered_query = query    
    if mode == 'filter':
        query=filtered_query
    elif mode == 'export':
        query=filtered_query
        fh,output_file = tempfile.mkstemp(suffix='', prefix='%s_'%table_name, dir=None, text=False)
        dict = {'header':{},'detail':[]}
        count = 0
        rows = query.all()
        for row in rows:
            dict['detail'].append({})
            for column in ['Request_Id', 'project_uuid', 'category_name', 'cluster_uuid', 'vm_name', 'power_state', 'vcpus_per_socket', 'num_sockets', 'memory_size_mib', 'memory_size_gib', 'Comments', 'vm_uuid', 'vm_ip', 'subnet_uuid', 'vm_username', 'vm_password', 'backup_set_1', 'backup_set_2', 'backup_set_3', 'disk_type', 'disk_0_image', 'disk_0_size', 'disk_1_image', 'disk_1_size', 'disk_2_image', 'disk_2_size', 'disk_3_image', 'disk_3_size', 'disk_4_image', 'disk_4_size', 'disk_5_image', 'disk_5_size', 'disk_6_image', 'disk_6_size', 'disk_7_image', 'disk_7_size', 'disk_8_image', 'disk_8_size', 'disk_9_image', 'disk_9_size', 'disk_10_image', 'disk_10_size', 'disk_11_image', 'disk_11_size', 'vm_drp', 'vm_drp_remote', 'vm_cdrom', 'drp_cluster_uuid', 'nic_0_vlan', 'nic_0_ip', 'nic_0_mac', 'nic_1_vlan', 'nic_1_ip', 'nic_1_mac', 'nic_2_vlan', 'nic_2_ip', 'nic_2_mac', 'nic_3_vlan', 'nic_3_ip', 'nic_3_mac', 'request_text']:
                dict['detail'][count].update( { column:str(row.__getattribute__(column))})
                
            count += 1
        dict['header'].update({'count':count})
        jsonarray      = json.dumps(dict)
        data           = json.loads(jsonarray)  
        dataframe      = json_normalize(data, 'detail').assign(**data['header'])
        fh,output_file = tempfile.mkstemp(suffix='', prefix='%_'%table_name, dir='/tmp', text=False)
        xlsx_file      = '%s/%s'%(current_app.root_path,url_for('static',filename='%s.xls'%(output_file)))
        dataframe.to_excel(xlsx_file,sheet_name=table_name,columns=['Request_Id', 'project_uuid', 'category_name', 'cluster_uuid', 'vm_name', 'power_state', 'vcpus_per_socket', 'num_sockets', 'memory_size_mib', 'memory_size_gib', 'Comments', 'vm_uuid', 'vm_ip', 'subnet_uuid', 'vm_username', 'vm_password', 'backup_set_1', 'backup_set_2', 'backup_set_3', 'disk_type', 'disk_0_image', 'disk_0_size', 'disk_1_image', 'disk_1_size', 'disk_2_image', 'disk_2_size', 'disk_3_image', 'disk_3_size', 'disk_4_image', 'disk_4_size', 'disk_5_image', 'disk_5_size', 'disk_6_image', 'disk_6_size', 'disk_7_image', 'disk_7_size', 'disk_8_image', 'disk_8_size', 'disk_9_image', 'disk_9_size', 'disk_10_image', 'disk_10_size', 'disk_11_image', 'disk_11_size', 'vm_drp', 'vm_drp_remote', 'vm_cdrom', 'drp_cluster_uuid', 'nic_0_vlan', 'nic_0_ip', 'nic_0_mac', 'nic_1_vlan', 'nic_1_ip', 'nic_1_mac', 'nic_2_vlan', 'nic_2_ip', 'nic_2_mac', 'nic_3_vlan', 'nic_3_ip', 'nic_3_mac', 'request_text'])
        return send_file(xlsx_file,as_attachment=True,attachment_filename=output_file.replace('/','_')+'.xls')
    elif mode == 'add':
        return redirect(url_for('.forms_%s'%table_name))
    elif mode == 'select':
        pass
        # if some filter is required
        if field is not None:
            if field == 'Request_Id':
                if value is not None:
                    query = query.filter_by(Request_Id=value)
            if field == 'project_uuid':
                if value is not None:
                    query = query.filter_by(project_uuid=value)
            if field == 'category_name':
                if value is not None:
                    query = query.filter_by(category_name=value)
            if field == 'cluster_uuid':
                if value is not None:
                    query = query.filter_by(cluster_uuid=value)
            if field == 'vm_name':
                if value is not None:
                    query = query.filter_by(vm_name=value)
            if field == 'power_state':
                if value is not None:
                    query = query.filter_by(power_state=value)
            if field == 'vcpus_per_socket':
                if value is not None:
                    query = query.filter_by(vcpus_per_socket=value)
            if field == 'num_sockets':
                if value is not None:
                    query = query.filter_by(num_sockets=value)
            if field == 'memory_size_mib':
                if value is not None:
                    query = query.filter_by(memory_size_mib=value)
            if field == 'memory_size_gib':
                if value is not None:
                    query = query.filter_by(memory_size_gib=value)
            if field == 'Comments':
                if value is not None:
                    query = query.filter_by(Comments=value)
            if field == 'vm_uuid':
                if value is not None:
                    query = query.filter_by(vm_uuid=value)
            if field == 'vm_ip':
                if value is not None:
                    query = query.filter_by(vm_ip=value)
            if field == 'subnet_uuid':
                if value is not None:
                    query = query.filter_by(subnet_uuid=value)
            if field == 'vm_username':
                if value is not None:
                    query = query.filter_by(vm_username=value)
            if field == 'vm_password':
                if value is not None:
                    query = query.filter_by(vm_password=value)
            if field == 'backup_set_1':
                if value is not None:
                    query = query.filter_by(backup_set_1=value)
            if field == 'backup_set_2':
                if value is not None:
                    query = query.filter_by(backup_set_2=value)
            if field == 'backup_set_3':
                if value is not None:
                    query = query.filter_by(backup_set_3=value)
            if field == 'disk_type':
                if value is not None:
                    query = query.filter_by(disk_type=value)
            if field == 'disk_0_image':
                if value is not None:
                    query = query.filter_by(disk_0_image=value)
            if field == 'disk_0_size':
                if value is not None:
                    query = query.filter_by(disk_0_size=value)
            if field == 'disk_1_image':
                if value is not None:
                    query = query.filter_by(disk_1_image=value)
            if field == 'disk_1_size':
                if value is not None:
                    query = query.filter_by(disk_1_size=value)
            if field == 'disk_2_image':
                if value is not None:
                    query = query.filter_by(disk_2_image=value)
            if field == 'disk_2_size':
                if value is not None:
                    query = query.filter_by(disk_2_size=value)
            if field == 'disk_3_image':
                if value is not None:
                    query = query.filter_by(disk_3_image=value)
            if field == 'disk_3_size':
                if value is not None:
                    query = query.filter_by(disk_3_size=value)
            if field == 'disk_4_image':
                if value is not None:
                    query = query.filter_by(disk_4_image=value)
            if field == 'disk_4_size':
                if value is not None:
                    query = query.filter_by(disk_4_size=value)
            if field == 'disk_5_image':
                if value is not None:
                    query = query.filter_by(disk_5_image=value)
            if field == 'disk_5_size':
                if value is not None:
                    query = query.filter_by(disk_5_size=value)
            if field == 'disk_6_image':
                if value is not None:
                    query = query.filter_by(disk_6_image=value)
            if field == 'disk_6_size':
                if value is not None:
                    query = query.filter_by(disk_6_size=value)
            if field == 'disk_7_image':
                if value is not None:
                    query = query.filter_by(disk_7_image=value)
            if field == 'disk_7_size':
                if value is not None:
                    query = query.filter_by(disk_7_size=value)
            if field == 'disk_8_image':
                if value is not None:
                    query = query.filter_by(disk_8_image=value)
            if field == 'disk_8_size':
                if value is not None:
                    query = query.filter_by(disk_8_size=value)
            if field == 'disk_9_image':
                if value is not None:
                    query = query.filter_by(disk_9_image=value)
            if field == 'disk_9_size':
                if value is not None:
                    query = query.filter_by(disk_9_size=value)
            if field == 'disk_10_image':
                if value is not None:
                    query = query.filter_by(disk_10_image=value)
            if field == 'disk_10_size':
                if value is not None:
                    query = query.filter_by(disk_10_size=value)
            if field == 'disk_11_image':
                if value is not None:
                    query = query.filter_by(disk_11_image=value)
            if field == 'disk_11_size':
                if value is not None:
                    query = query.filter_by(disk_11_size=value)
            if field == 'vm_drp':
                if value is not None:
                    query = query.filter_by(vm_drp=value)
            if field == 'vm_drp_remote':
                if value is not None:
                    query = query.filter_by(vm_drp_remote=value)
            if field == 'vm_cdrom':
                if value is not None:
                    query = query.filter_by(vm_cdrom=value)
            if field == 'drp_cluster_uuid':
                if value is not None:
                    query = query.filter_by(drp_cluster_uuid=value)
            if field == 'nic_0_vlan':
                if value is not None:
                    query = query.filter_by(nic_0_vlan=value)
            if field == 'nic_0_ip':
                if value is not None:
                    query = query.filter_by(nic_0_ip=value)
            if field == 'nic_0_mac':
                if value is not None:
                    query = query.filter_by(nic_0_mac=value)
            if field == 'nic_1_vlan':
                if value is not None:
                    query = query.filter_by(nic_1_vlan=value)
            if field == 'nic_1_ip':
                if value is not None:
                    query = query.filter_by(nic_1_ip=value)
            if field == 'nic_1_mac':
                if value is not None:
                    query = query.filter_by(nic_1_mac=value)
            if field == 'nic_2_vlan':
                if value is not None:
                    query = query.filter_by(nic_2_vlan=value)
            if field == 'nic_2_ip':
                if value is not None:
                    query = query.filter_by(nic_2_ip=value)
            if field == 'nic_2_mac':
                if value is not None:
                    query = query.filter_by(nic_2_mac=value)
            if field == 'nic_3_vlan':
                if value is not None:
                    query = query.filter_by(nic_3_vlan=value)
            if field == 'nic_3_ip':
                if value is not None:
                    query = query.filter_by(nic_3_ip=value)
            if field == 'nic_3_mac':
                if value is not None:
                    query = query.filter_by(nic_3_mac=value)
            if field == 'request_text':
                if value is not None:
                    query = query.filter_by(request_text=value)
            # ------------------------------------------------------------------
    # JOIN other tables and generate foreign fields
    # Will replace class name by sharding class in joins structure
    # will have no effect in no sharding environment
    query = query.join(requests,nutanix_prism_vm.Request_Id == requests.Id).add_columns(requests.Id).join(projects,nutanix_prism_vm.project_uuid == projects.project_uuid).add_columns(projects.project_name).join(categories,nutanix_prism_vm.category_name == categories.category_name).add_columns(categories.category_description).join(clusters,nutanix_prism_vm.cluster_uuid == clusters.cluster_uuid).add_columns(clusters.cluster_name).join(subnets,nutanix_prism_vm.subnet_uuid == subnets.uuid).add_columns(subnets.name)
    # ------------------------------------------------------------------
    
    # Actual request from DB follows
    tracebox_log(query,logger,length=80)
    # getting paginated rows for query
    rows = query.paginate(page, per_page=current_app.config['LINES_PER_PAGE'], error_out=False)
    # Setting pagination variables ...
    if field is not None:
       next_url = url_for('.select_%s_query'%template_name, field=field, value=value, page=rows.next_num) if rows.has_next else None
       prev_url = url_for('.select_%s_query'%template_name, field=field, value=value, page=rows.prev_num) if rows.has_prev else None
    else:
       next_url = url_for('.select_%s_query'%template_name, page=rows.next_num) if rows.has_next else None
       prev_url = url_for('.select_%s_query'%template_name, page=rows.prev_num) if rows.has_prev else None
    # Actual rendering ...
    if request.headers.get('Content-Type') is not None or request.args.get('JSON',None,type=str) is not None:
        # NOTE: needs review for JSONnifiyng output when needed (API Interface?)
        if "JSON" in request.headers.get('Content-Type') or request.args.get('JSON',None,type=str) is not None:
            logger.debug('select_%s_query(): will render: JSON rows'%template_name)
            logger.debug('select_%s_query(): Exit'%template_name)
            return json.dumps(serialize_object(rows.__dict__))
    logger.debug('select_%s_query(): will render: %s_All.html'%(template_name,table_name.lower()))
    logger.debug('select_%s_query(): Exit'%template_name)
    return render_template('%s_select_All.html'%template_name.lower(),rows=rows,options=options,collectordata=collectordata)
#===============================================================================
   
# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2022-03-23 18:29:44.257332
# ======================================================================
# gen_views_api.html:AG 2022-03-23 18:29:44.257350
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
        #response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        #response.headers['Pragma']        = 'no-cache'
        try:
            id_counter = 0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values=[id]
            # Codigo para un solo campo de id
            # chequear si marcado explicitamente
            db.session.flush()
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
                    if 'vm_uuid' in request.args:
                        query = query.filter(Nutanix_Prism_VM.vm_uuid == request.args.get('vm_uuid'))
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
                    if 'vm_drp' in request.args:
                        query = query.filter(Nutanix_Prism_VM.vm_drp == request.args.get('vm_drp'))
                    if 'vm_drp_remote' in request.args:
                        query = query.filter(Nutanix_Prism_VM.vm_drp_remote == request.args.get('vm_drp_remote'))
                    if 'vm_cdrom' in request.args:
                        query = query.filter(Nutanix_Prism_VM.vm_cdrom == request.args.get('vm_cdrom'))
                    if 'drp_cluster_uuid' in request.args:
                        query = query.filter(Nutanix_Prism_VM.drp_cluster_uuid == request.args.get('drp_cluster_uuid'))
                    if 'nic_0_vlan' in request.args:
                        query = query.filter(Nutanix_Prism_VM.nic_0_vlan == request.args.get('nic_0_vlan'))
                    if 'nic_0_ip' in request.args:
                        query = query.filter(Nutanix_Prism_VM.nic_0_ip == request.args.get('nic_0_ip'))
                    if 'nic_0_mac' in request.args:
                        query = query.filter(Nutanix_Prism_VM.nic_0_mac == request.args.get('nic_0_mac'))
                    if 'nic_1_vlan' in request.args:
                        query = query.filter(Nutanix_Prism_VM.nic_1_vlan == request.args.get('nic_1_vlan'))
                    if 'nic_1_ip' in request.args:
                        query = query.filter(Nutanix_Prism_VM.nic_1_ip == request.args.get('nic_1_ip'))
                    if 'nic_1_mac' in request.args:
                        query = query.filter(Nutanix_Prism_VM.nic_1_mac == request.args.get('nic_1_mac'))
                    if 'nic_2_vlan' in request.args:
                        query = query.filter(Nutanix_Prism_VM.nic_2_vlan == request.args.get('nic_2_vlan'))
                    if 'nic_2_ip' in request.args:
                        query = query.filter(Nutanix_Prism_VM.nic_2_ip == request.args.get('nic_2_ip'))
                    if 'nic_2_mac' in request.args:
                        query = query.filter(Nutanix_Prism_VM.nic_2_mac == request.args.get('nic_2_mac'))
                    if 'nic_3_vlan' in request.args:
                        query = query.filter(Nutanix_Prism_VM.nic_3_vlan == request.args.get('nic_3_vlan'))
                    if 'nic_3_ip' in request.args:
                        query = query.filter(Nutanix_Prism_VM.nic_3_ip == request.args.get('nic_3_ip'))
                    if 'nic_3_mac' in request.args:
                        query = query.filter(Nutanix_Prism_VM.nic_3_mac == request.args.get('nic_3_mac'))
                    if 'request_text' in request.args:
                        query = query.filter(Nutanix_Prism_VM.request_text == request.args.get('request_text'))
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
            row.vm_uuid = request.json.get('vm_uuid',None)
            row.vm_ip = request.json.get('vm_ip',None)
            row.subnet_uuid = request.json.get('subnet_uuid',None)
            row.vm_username = request.json.get('vm_username',None)
            row.vm_password = request.json.get('vm_password',None)
            row.backup_set_1 = request.json.get('backup_set_1',0)
            row.backup_set_2 = request.json.get('backup_set_2',0)
            row.backup_set_3 = request.json.get('backup_set_3',0)
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
            row.vm_drp = request.json.get('vm_drp',0)
            row.vm_drp_remote = request.json.get('vm_drp_remote',0)
            row.vm_cdrom = request.json.get('vm_cdrom',0)
            row.drp_cluster_uuid = request.json.get('drp_cluster_uuid',None)
            row.nic_0_vlan = request.json.get('nic_0_vlan',None)
            row.nic_0_ip = request.json.get('nic_0_ip',None)
            row.nic_0_mac = request.json.get('nic_0_mac',None)
            row.nic_1_vlan = request.json.get('nic_1_vlan',None)
            row.nic_1_ip = request.json.get('nic_1_ip',None)
            row.nic_1_mac = request.json.get('nic_1_mac',None)
            row.nic_2_vlan = request.json.get('nic_2_vlan',None)
            row.nic_2_ip = request.json.get('nic_2_ip',None)
            row.nic_2_mac = request.json.get('nic_2_mac',None)
            row.nic_3_vlan = request.json.get('nic_3_vlan',None)
            row.nic_3_ip = request.json.get('nic_3_ip',None)
            row.nic_3_mac = request.json.get('nic_3_mac',None)
            row.request_text = request.json.get('request_text',None)
            # ----------------------------------------------------------
            db.session.add(row)
            db.session.flush()
            db.session.commit()
            db.session.flush()
            db.session.refresh(row)
            db.session.flush()
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
                if 'vm_uuid' in request.json.keys():
                    row.vm_uuid = request.json.get('vm_uuid')
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
                if 'vm_drp' in request.json.keys():
                    row.vm_drp = request.json.get('vm_drp')
                if 'vm_drp_remote' in request.json.keys():
                    row.vm_drp_remote = request.json.get('vm_drp_remote')
                if 'vm_cdrom' in request.json.keys():
                    row.vm_cdrom = request.json.get('vm_cdrom')
                if 'drp_cluster_uuid' in request.json.keys():
                    row.drp_cluster_uuid = request.json.get('drp_cluster_uuid')
                if 'nic_0_vlan' in request.json.keys():
                    row.nic_0_vlan = request.json.get('nic_0_vlan')
                if 'nic_0_ip' in request.json.keys():
                    row.nic_0_ip = request.json.get('nic_0_ip')
                if 'nic_0_mac' in request.json.keys():
                    row.nic_0_mac = request.json.get('nic_0_mac')
                if 'nic_1_vlan' in request.json.keys():
                    row.nic_1_vlan = request.json.get('nic_1_vlan')
                if 'nic_1_ip' in request.json.keys():
                    row.nic_1_ip = request.json.get('nic_1_ip')
                if 'nic_1_mac' in request.json.keys():
                    row.nic_1_mac = request.json.get('nic_1_mac')
                if 'nic_2_vlan' in request.json.keys():
                    row.nic_2_vlan = request.json.get('nic_2_vlan')
                if 'nic_2_ip' in request.json.keys():
                    row.nic_2_ip = request.json.get('nic_2_ip')
                if 'nic_2_mac' in request.json.keys():
                    row.nic_2_mac = request.json.get('nic_2_mac')
                if 'nic_3_vlan' in request.json.keys():
                    row.nic_3_vlan = request.json.get('nic_3_vlan')
                if 'nic_3_ip' in request.json.keys():
                    row.nic_3_ip = request.json.get('nic_3_ip')
                if 'nic_3_mac' in request.json.keys():
                    row.nic_3_mac = request.json.get('nic_3_mac')
                if 'request_text' in request.json.keys():
                    row.request_text = request.json.get('request_text')
                # ----------------------------------------------------------
                db.session.merge(row)
                db.session.flush()
                db.session.commit()
                db.session.flush()
                db.session.refresh(row)
                db.session.flush()
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
                db.session.rollback()
                if request.values is not None and len(request.values):
                    if 'project_uuid' in request.values:
                        row.project_uuid = request.values.get('project_uuid')
                    if 'category_name' in request.values:
                        row.category_name = request.values.get('category_name')
                    if 'cluster_uuid' in request.values:
                        row.cluster_uuid = request.values.get('cluster_uuid')
                    if 'vm_name' in request.values:
                        row.vm_name = request.values.get('vm_name')
                    if 'power_state' in request.values:
                        row.power_state = request.values.get('power_state')
                    if 'vcpus_per_socket' in request.values:
                        row.vcpus_per_socket = request.values.get('vcpus_per_socket')
                    if 'num_sockets' in request.values:
                        row.num_sockets = request.values.get('num_sockets')
                    if 'memory_size_mib' in request.values:
                        row.memory_size_mib = request.values.get('memory_size_mib')
                    if 'memory_size_gib' in request.values:
                        row.memory_size_gib = request.values.get('memory_size_gib')
                    if 'Comments' in request.values:
                        row.Comments = request.values.get('Comments')
                    if 'vm_uuid' in request.values:
                        row.vm_uuid = request.values.get('vm_uuid')
                    if 'vm_ip' in request.values:
                        row.vm_ip = request.values.get('vm_ip')
                    if 'subnet_uuid' in request.values:
                        row.subnet_uuid = request.values.get('subnet_uuid')
                    if 'vm_username' in request.values:
                        row.vm_username = request.values.get('vm_username')
                    if 'vm_password' in request.values:
                        row.vm_password = request.values.get('vm_password')
                    if 'backup_set_1' in request.values:
                        row.backup_set_1 = request.values.get('backup_set_1')
                    if 'backup_set_2' in request.values:
                        row.backup_set_2 = request.values.get('backup_set_2')
                    if 'backup_set_3' in request.values:
                        row.backup_set_3 = request.values.get('backup_set_3')
                    if 'disk_type' in request.values:
                        row.disk_type = request.values.get('disk_type')
                    if 'disk_0_image' in request.values:
                        row.disk_0_image = request.values.get('disk_0_image')
                    if 'disk_0_size' in request.values:
                        row.disk_0_size = request.values.get('disk_0_size')
                    if 'disk_1_image' in request.values:
                        row.disk_1_image = request.values.get('disk_1_image')
                    if 'disk_1_size' in request.values:
                        row.disk_1_size = request.values.get('disk_1_size')
                    if 'disk_2_image' in request.values:
                        row.disk_2_image = request.values.get('disk_2_image')
                    if 'disk_2_size' in request.values:
                        row.disk_2_size = request.values.get('disk_2_size')
                    if 'disk_3_image' in request.values:
                        row.disk_3_image = request.values.get('disk_3_image')
                    if 'disk_3_size' in request.values:
                        row.disk_3_size = request.values.get('disk_3_size')
                    if 'disk_4_image' in request.values:
                        row.disk_4_image = request.values.get('disk_4_image')
                    if 'disk_4_size' in request.values:
                        row.disk_4_size = request.values.get('disk_4_size')
                    if 'disk_5_image' in request.values:
                        row.disk_5_image = request.values.get('disk_5_image')
                    if 'disk_5_size' in request.values:
                        row.disk_5_size = request.values.get('disk_5_size')
                    if 'disk_6_image' in request.values:
                        row.disk_6_image = request.values.get('disk_6_image')
                    if 'disk_6_size' in request.values:
                        row.disk_6_size = request.values.get('disk_6_size')
                    if 'disk_7_image' in request.values:
                        row.disk_7_image = request.values.get('disk_7_image')
                    if 'disk_7_size' in request.values:
                        row.disk_7_size = request.values.get('disk_7_size')
                    if 'disk_8_image' in request.values:
                        row.disk_8_image = request.values.get('disk_8_image')
                    if 'disk_8_size' in request.values:
                        row.disk_8_size = request.values.get('disk_8_size')
                    if 'disk_9_image' in request.values:
                        row.disk_9_image = request.values.get('disk_9_image')
                    if 'disk_9_size' in request.values:
                        row.disk_9_size = request.values.get('disk_9_size')
                    if 'disk_10_image' in request.values:
                        row.disk_10_image = request.values.get('disk_10_image')
                    if 'disk_10_size' in request.values:
                        row.disk_10_size = request.values.get('disk_10_size')
                    if 'disk_11_image' in request.values:
                        row.disk_11_image = request.values.get('disk_11_image')
                    if 'disk_11_size' in request.values:
                        row.disk_11_size = request.values.get('disk_11_size')
                    if 'vm_drp' in request.values:
                        row.vm_drp = request.values.get('vm_drp')
                    if 'vm_drp_remote' in request.values:
                        row.vm_drp_remote = request.values.get('vm_drp_remote')
                    if 'vm_cdrom' in request.values:
                        row.vm_cdrom = request.values.get('vm_cdrom')
                    if 'drp_cluster_uuid' in request.values:
                        row.drp_cluster_uuid = request.values.get('drp_cluster_uuid')
                    if 'nic_0_vlan' in request.values:
                        row.nic_0_vlan = request.values.get('nic_0_vlan')
                    if 'nic_0_ip' in request.values:
                        row.nic_0_ip = request.values.get('nic_0_ip')
                    if 'nic_0_mac' in request.values:
                        row.nic_0_mac = request.values.get('nic_0_mac')
                    if 'nic_1_vlan' in request.values:
                        row.nic_1_vlan = request.values.get('nic_1_vlan')
                    if 'nic_1_ip' in request.values:
                        row.nic_1_ip = request.values.get('nic_1_ip')
                    if 'nic_1_mac' in request.values:
                        row.nic_1_mac = request.values.get('nic_1_mac')
                    if 'nic_2_vlan' in request.values:
                        row.nic_2_vlan = request.values.get('nic_2_vlan')
                    if 'nic_2_ip' in request.values:
                        row.nic_2_ip = request.values.get('nic_2_ip')
                    if 'nic_2_mac' in request.values:
                        row.nic_2_mac = request.values.get('nic_2_mac')
                    if 'nic_3_vlan' in request.values:
                        row.nic_3_vlan = request.values.get('nic_3_vlan')
                    if 'nic_3_ip' in request.values:
                        row.nic_3_ip = request.values.get('nic_3_ip')
                    if 'nic_3_mac' in request.values:
                        row.nic_3_mac = request.values.get('nic_3_mac')
                    if 'request_text' in request.values:
                        row.request_text = request.values.get('request_text')
                # ----------------------------------------------------------
                db.session.merge(row)
                db.session.flush()
                db.session.commit()
                db.session.flush()
                db.session.refresh(row)
                db.session.flush()
                message = f"Modified 'Nutanix_Prism_VM' Request_Id = {id}"
                try:
                    row     = json.loads(row.get_json())
                except:
                    row     = None
            else:
                code    = API_NOT_FOUND
                message = f"Not found Nutanix_Prism_VM with Request_Id = {id}"
                row     = None
                db.session.rollback()
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
            row     = None
            db.session.rollback()
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
                db.session.flush()
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

# ======================================================================# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2022-03-23 18:29:41
# =============================================================================
# gen_views.py:32 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/views/view_nutanix_vm_images.py
# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2022-03-23 18:29:44.376299
# ======================================================================        
# gen_views_form.html:AG 2022-03-23 18:29:44.376321
@main.route('/forms/Nutanix_VM_Images', methods=['GET', 'POST'])
@login_required

def forms_Nutanix_VM_Images():
    """ Form handling function for table Nutanix_VM_Images """
    logger.debug('forms_Nutanix_VM_Images(): Enter')
    
    # Shardening Code goes her if needed
    collectordata={}
    collectordata.update({"COLLECTOR_PERIOD":get_period_data(current_user.id,db.engine,Interface)})
    collectordata.update({"CONFIG":current_app.config})
    suffix = collectordata['COLLECTOR_PERIOD']['active']
    table_name='Nutanix_VM_Images'
    class_name='nutanix_vm_images'
    template_name='Nutanix_VM_Images'
    sharding=False
    imageservice_uuid_diskclone  =  request.args.get('imageservice_uuid_diskclone',0,type=int)
    
    # Ensures DB Data is commited prior main query
    try:
        db.session.commit()
    except:
        db.session.rollback()
    row =  nutanix_vm_images.query.filter(nutanix_vm_images.imageservice_uuid_diskclone == imageservice_uuid_diskclone).first()
    if row is None:
        row=nutanix_vm_images()
        session['is_new_row']=True
    session['data'] =  {  'imageservice_uuid_diskclone':row.imageservice_uuid_diskclone, 'description':row.description, 'size_mib':row.size_mib, 'comments':row.comments }
    
    form = frm_nutanix_vm_images()
    
    # Actual Form activation here
    if form.validate_on_submit():
        # Code for SAVE option -----------------------------------------
        if form.submit_Save.data and current_user.role_id > 1:
            row.imageservice_uuid_diskclone = form.imageservice_uuid_diskclone.data
            row.description = form.description.data
            row.size_mib = form.size_mib.data
            row.comments = form.comments.data
            try:
               session['new_row']=str(row)
               db.session.flush()
               db.session.add(row)
               db.session.commit()
               db.session.flush()
               if session['is_new_row']==True:
                   logger.audit ( '%s:NEW:%s' % (current_user.username,session['new_row'] ) )
                   flash('New Nutanix_vm_images created OK')
               else:
                   logger.audit ( '%s:OLD:%s' % (current_user.username,session['prev_row']) )
                   logger.audit ( '%s:UPD:%s' % (current_user.username,session['new_row'] ) )    
                   message=Markup('<b>Nutanix_vm_images imageservice_uuid_diskclone saved OK</b>')
                   flash(message)
               db.session.flush()
            except Exception as e:
               db.session.rollback()
               db.session.flush()
               message=Markup('ERROR saving Nutanix_vm_images record : %s'%(e))
               flash(message)
            return redirect(url_for('.select_Nutanix_VM_Images_query'))
        # --------------------------------------------------------------
        # Code for NEW option
        # GV 20190109 f.write(        "        elif   form.submit_New.data:\n")
        elif   form.submit_New.data and current_user.role_id>1:
            #print('New Data Here ...')
            session['is_new_row']=True
            db.session.flush()
            row=nutanix_vm_images()
    
            return redirect(url_for('.forms_Nutanix_VM_Images'))    
    
        # Code for CANCEL option 
        elif   form.submit_Cancel.data:
            #print('Cancel Data Here ... does nothing')
            message=Markup('Nutanix_vm_images Record modifications discarded ...')
            flash(message)
        # Code for ANY OTHER option should never get here
        else:
            #print('form validated but not submited ???')
            message=Markup("<b>Nutanix_vm_images data modifications not allowed for user '%s'. Please contact EG Suite's Administrator ...</b>"%(current_user.username))    
            flash(message)
    
            return redirect(url_for('.forms_'))    
    
    
    form.imageservice_uuid_diskclone.data = row.imageservice_uuid_diskclone
    form.description.data = row.description
    form.size_mib.data = row.size_mib
    form.comments.data = row.comments
    session['prev_row'] = str(row)
    session['is_new_row'] = False
    logger.debug('forms_Nutanix_VM_Images(): Exit')
    # Generates pagination data here
    P=[]
    # Tab Relations = []
    
    # Generation of pagination data completed
    collectordata={}
    collectordata.update({"COLLECTOR_PERIOD":get_period_data(current_user.id,db.engine,Interface)})
    return render_template('nutanix_vm_images.html', form=form, row=row, P=P,collectordata=collectordata)    
# ======================================================================



# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2022-03-23 18:29:44.386697
# ======================================================================        
# gen_views_delete.html:AG 2022-03-23 18:29:44.386714
@main.route('/forms/Nutanix_VM_Images_delete', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DELETE)
@admin_required
def forms_Nutanix_VM_Images_delete():
    """ Delete record handling function for table Nutanix_VM_Images """
    logger.debug('forms_Nutanix_VM_Images_delete(): Enter')
    imageservice_uuid_diskclone  =  request.args.get('imageservice_uuid_diskclone',0,type=int)
    row =  nutanix_vm_images.query.filter(nutanix_vm_images.imageservice_uuid_diskclone == imageservice_uuid_diskclone).first()

    if row is None:
        row=nutanix_vm_images()
    session['data'] =  {  'imageservice_uuid_diskclone':row.imageservice_uuid_diskclone, 'description':row.description, 'size_mib':row.size_mib, 'comments':row.comments }
                       
    form = frm_nutanix_vm_images_delete()

    # Tab['has_fks'] False
    
            
    # Actual Form activation here
    if form.validate_on_submit():
    
    # Code for SAVE option
        if  form.submit_Delete.data:
            print('Delete Data Here...')

    
    #f.write(        "            print('Delete Data Here...')
            try:
                session['deleted_row']=str(row)
                db.session.flush()
                db.session.delete(row)
                db.session.commit()
                db.session.flush()
                logger.audit ( '%s:DEL:%s' % (current_user.username,session['deleted_row']) )
                flash('Nutanix_vm_images imageservice_uuid_diskclone deleted OK')
            except exc.IntegrityError as e:
                db.session.rollback()    
                flash('INTEGRITY ERROR: Are you sure there are no dependant records in other tables?')
                return redirect(url_for('.forms_Nutanix_VM_Images_delete',imageservice_uuid_diskclone=session['data']['imageservice_uuid_diskclone']))    
    
            return redirect(url_for('.select_Nutanix_VM_Images_query'))    
    # Code for CANCEL option 
        elif   form.submit_Cancel.data:
            print('Cancel Data Here ... does nothing')
            flash('Record modifications discarded ...')
            return redirect(url_for('.select_Nutanix_VM_Images_query'))    
    # Code for ANY OTHER option should never get here
        else:
            print('form validated but not submited ???')
            return redirect(url_for('.select_Nutanix_VM_Images_query'))    
    
    logger.debug('forms_Nutanix_VM_Images_delete(): Exit')
    collectordata={}
    collectordata.update({"COLLECTOR_PERIOD":get_period_data(current_user.id,db.engine,Interface)})
    return render_template('nutanix_vm_images_delete.html', form=form, data=session.get('data'),row=row,collectordata=collectordata)
#===============================================================================

# table_name: Nutanix_VM_Images
# class_name: nutanix_vm_images
# is shardened: False
# current_app: 
# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2022-03-23 18:29:44.408009
# ======================================================================

# gen_views_select_query.html:AG 2022-03-23 18:29:44.408027        
@main.route('/select/Nutanix_VM_Images_Query', methods=['GET','POST'])
@login_required
@admin_required
def select_Nutanix_VM_Images_query():
    """ Select rows handling function for table 'Nutanix_VM_Images' """
    logger.debug('select_Nutanix_VM_Images_query(): Enter')
    #chk_c000001(filename=os.path.join(current_app.root_path, '.c000001'),request=request,db=db,logger=logger)
    # Shardening Code goes her if needed
    collectordata={}
    collectordata.update({"COLLECTOR_PERIOD":get_period_data(current_user.id,db.engine,Interface)})
    collectordata.update({"CONFIG":current_app.config})
    suffix = collectordata['COLLECTOR_PERIOD']['active']
    table_name='Nutanix_VM_Images'
    class_name='nutanix_vm_images'
    template_name='Nutanix_VM_Images'
    sharding=False


    logger.debug("-----------------------------------------------------------")
    logger.debug("%s: template_name            = %s",__name__,template_name)

    logger.debug("-----------------------------------------------------------")    
        
    # Get parameters from URL call
    ia       =  request.args.get('ia',     None,type=str)
    if ia is not None:
        ia=ia.split(',')
        if ia[0]=='ORDER':
            #set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name='nutanix_vm_images',Option_Type=OPTION_ORDER_BY,Argument_1=ia[1],Argument_2=ia[2])
            set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name=class_name,Option_Type=OPTION_ORDER_BY,Argument_1=ia[1],Argument_2=ia[2])
        elif ia[0]=='GROUP':
            #set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name='nutanix_vm_images',Option_Type=OPTION_GROUP_BY,Argument_1=ia[1])
            set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name=class_name,Option_Type=OPTION_GROUP_BY,Argument_1=ia[1])
        elif ia[0]=='LIMIT':
            #set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name='nutanix_vm_images',Option_Type=OPTION_LIMIT,Argument_1=ia[1])
            set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name=class_name,Option_Type=OPTION_LIMIT,Argument_1=ia[1])

    iad      =  request.args.get('iad',     None,type=int)
    if iad is not None: delete_query_option(engine=db.engine,Interface=Interface,Id=iad) 
    
    field    =  request.args.get('field',   None,type=str)
    value    =  request.args.get('value',   None,type=str)
    
    # Populates a list of foreign keys used for advanced filtering
    # ------------------------------------------------------------------
    foreign_keys={}
    
    # ------------------------------------------------------------------
    
    if field is not None:
        reset_query_options(    engine=db.engine,Interface=Interface,
                                User_Id=current_user.id,
                                #Table_name='nutanix_vm_images'
                                Table_name=class_name
                                )

        
        if field in foreign_keys.keys():
            Class,referenced_classname,referenced_Field,referenced_Value,column_Header=foreign_keys[field]
            foreign_field='%s.%s:%s'%(referenced_classname,referenced_Value,column_Header)
            foreign_record=Class.query.get(value)
            foreign_description="'%s'"%getattr(foreign_record,referenced_Value)
        set_query_option(   engine=db.engine,Interface=Interface,
                        User_Id=current_user.id,
                        Table_name=class_name,
                        Option_Type=OPTION_FILTER,
                        Argument_1=foreign_field,
                        Argument_2='==',
                        Argument_3=foreign_description
                        )
    page     =  request.args.get('page',    1   ,type=int)
    addx     =  request.args.get('add.x',   None,type=int)
    addy     =  request.args.get('add.y',   None,type=int)
    exportx  =  request.args.get('export.x',None,type=int)
    exporty  =  request.args.get('export.y',None,type=int)
    filterx  =  request.args.get('filter.x',None,type=int)
    filtery  =  request.args.get('filter.y',None,type=int)
    # Select excluyent view mode
    if   addx    is not None: mode = 'add'
    elif exportx is not None: mode = 'export'
    elif filterx is not None: mode = 'filter'
    else:                     mode = 'select'
    imageservice_uuid_diskclone =  request.args.get('imageservice_uuid_diskclone',None,type=str)
    description =  request.args.get('description',None,type=str)
    size_mib =  request.args.get('size_mib',None,type=str)
    comments =  request.args.get('comments',None,type=str)
    
    # Build default query all fields from table
    

    if imageservice_uuid_diskclone is not None and len(imageservice_uuid_diskclone)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='imageservice_uuid_diskclone:imageservice_uuid_diskclone',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%imageservice_uuid_diskclone
                )
    
    
    if description is not None and len(description)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='description:description',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%description
                )
    
    
    if size_mib is not None and len(size_mib)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='size_mib:size_mib',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%size_mib
                )
    
    
    if comments is not None and len(comments)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='comments:comments',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%comments
                )
    
    
    
    statement_query,options=get_query_options(engine=db.engine,Interface=Interface,Table_name=class_name,User_Id=current_user.id)
    tracebox_log(statement_query,logger,length=80)
    query=eval(statement_query)
    filtered_query = query    
    if mode == 'filter':
        query=filtered_query
    elif mode == 'export':
        query=filtered_query
        fh,output_file = tempfile.mkstemp(suffix='', prefix='%s_'%table_name, dir=None, text=False)
        dict = {'header':{},'detail':[]}
        count = 0
        rows = query.all()
        for row in rows:
            dict['detail'].append({})
            for column in ['imageservice_uuid_diskclone', 'description', 'size_mib', 'comments']:
                dict['detail'][count].update( { column:str(row.__getattribute__(column))})
                
            count += 1
        dict['header'].update({'count':count})
        jsonarray      = json.dumps(dict)
        data           = json.loads(jsonarray)  
        dataframe      = json_normalize(data, 'detail').assign(**data['header'])
        fh,output_file = tempfile.mkstemp(suffix='', prefix='%_'%table_name, dir='/tmp', text=False)
        xlsx_file      = '%s/%s'%(current_app.root_path,url_for('static',filename='%s.xls'%(output_file)))
        dataframe.to_excel(xlsx_file,sheet_name=table_name,columns=['imageservice_uuid_diskclone', 'description', 'size_mib', 'comments'])
        return send_file(xlsx_file,as_attachment=True,attachment_filename=output_file.replace('/','_')+'.xls')
    elif mode == 'add':
        return redirect(url_for('.forms_%s'%table_name))
    elif mode == 'select':
        pass
        # if some filter is required
        if field is not None:
            if field == 'imageservice_uuid_diskclone':
                if value is not None:
                    query = query.filter_by(imageservice_uuid_diskclone=value)
            if field == 'description':
                if value is not None:
                    query = query.filter_by(description=value)
            if field == 'size_mib':
                if value is not None:
                    query = query.filter_by(size_mib=value)
            if field == 'comments':
                if value is not None:
                    query = query.filter_by(comments=value)
            
    # Actual request from DB follows
    tracebox_log(query,logger,length=80)
    # getting paginated rows for query
    rows = query.paginate(page, per_page=current_app.config['LINES_PER_PAGE'], error_out=False)
    # Setting pagination variables ...
    if field is not None:
       next_url = url_for('.select_%s_query'%template_name, field=field, value=value, page=rows.next_num) if rows.has_next else None
       prev_url = url_for('.select_%s_query'%template_name, field=field, value=value, page=rows.prev_num) if rows.has_prev else None
    else:
       next_url = url_for('.select_%s_query'%template_name, page=rows.next_num) if rows.has_next else None
       prev_url = url_for('.select_%s_query'%template_name, page=rows.prev_num) if rows.has_prev else None
    # Actual rendering ...
    if request.headers.get('Content-Type') is not None or request.args.get('JSON',None,type=str) is not None:
        # NOTE: needs review for JSONnifiyng output when needed (API Interface?)
        if "JSON" in request.headers.get('Content-Type') or request.args.get('JSON',None,type=str) is not None:
            logger.debug('select_%s_query(): will render: JSON rows'%template_name)
            logger.debug('select_%s_query(): Exit'%template_name)
            return json.dumps(serialize_object(rows.__dict__))
    logger.debug('select_%s_query(): will render: %s_All.html'%(template_name,table_name.lower()))
    logger.debug('select_%s_query(): Exit'%template_name)
    return render_template('%s_select_All.html'%template_name.lower(),rows=rows,options=options,collectordata=collectordata)
#===============================================================================
   
# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2022-03-23 18:29:44.443905
# ======================================================================
# gen_views_api.html:AG 2022-03-23 18:29:44.443923
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
        #response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        #response.headers['Pragma']        = 'no-cache'
        try:
            id_counter = 0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values=[id]
            # Codigo para un solo campo de id
            # chequear si marcado explicitamente
            db.session.flush()
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
            db.session.flush()
            db.session.refresh(row)
            db.session.flush()
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
                db.session.flush()
                db.session.refresh(row)
                db.session.flush()
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
                db.session.rollback()
                if request.values is not None and len(request.values):
                    if 'description' in request.values:
                        row.description = request.values.get('description')
                    if 'size_mib' in request.values:
                        row.size_mib = request.values.get('size_mib')
                    if 'comments' in request.values:
                        row.comments = request.values.get('comments')
                # ----------------------------------------------------------
                db.session.merge(row)
                db.session.flush()
                db.session.commit()
                db.session.flush()
                db.session.refresh(row)
                db.session.flush()
                message = f"Modified 'Nutanix_VM_Images' imageservice_uuid_diskclone = {id}"
                try:
                    row     = json.loads(row.get_json())
                except:
                    row     = None
            else:
                code    = API_NOT_FOUND
                message = f"Not found Nutanix_VM_Images with imageservice_uuid_diskclone = {id}"
                row     = None
                db.session.rollback()
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
            row     = None
            db.session.rollback()
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
                db.session.flush()
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

# ======================================================================# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2022-03-23 18:29:41
# =============================================================================
# gen_views.py:32 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/views/view_projects.py
# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2022-03-23 18:29:44.569370
# ======================================================================        
# gen_views_form.html:AG 2022-03-23 18:29:44.569395
@main.route('/forms/Projects', methods=['GET', 'POST'])
@login_required

def forms_Projects():
    """ Form handling function for table Projects """
    logger.debug('forms_Projects(): Enter')
    
    # Shardening Code goes her if needed
    collectordata={}
    collectordata.update({"COLLECTOR_PERIOD":get_period_data(current_user.id,db.engine,Interface)})
    collectordata.update({"CONFIG":current_app.config})
    suffix = collectordata['COLLECTOR_PERIOD']['active']
    table_name='Projects'
    class_name='projects'
    template_name='Projects'
    sharding=False
    project_uuid  =  request.args.get('project_uuid',0,type=int)
    
    # Ensures DB Data is commited prior main query
    try:
        db.session.commit()
    except:
        db.session.rollback()
    row =  projects.query.filter(projects.project_uuid == project_uuid).first()
    if row is None:
        row=projects()
        session['is_new_row']=True
    session['data'] =  {  'project_uuid':row.project_uuid, 'project_name':row.project_name, 'project_subnets':row.project_subnets }
    
    form = frm_projects()
    
    # Actual Form activation here
    if form.validate_on_submit():
        # Code for SAVE option -----------------------------------------
        if form.submit_Save.data and current_user.role_id > 1:
            row.project_uuid = form.project_uuid.data
            row.project_name = form.project_name.data
            row.project_subnets = form.project_subnets.data
            try:
               session['new_row']=str(row)
               db.session.flush()
               db.session.add(row)
               db.session.commit()
               db.session.flush()
               if session['is_new_row']==True:
                   logger.audit ( '%s:NEW:%s' % (current_user.username,session['new_row'] ) )
                   flash('New Projects created OK')
               else:
                   logger.audit ( '%s:OLD:%s' % (current_user.username,session['prev_row']) )
                   logger.audit ( '%s:UPD:%s' % (current_user.username,session['new_row'] ) )    
                   message=Markup('<b>Projects project_uuid saved OK</b>')
                   flash(message)
               db.session.flush()
            except Exception as e:
               db.session.rollback()
               db.session.flush()
               message=Markup('ERROR saving Projects record : %s'%(e))
               flash(message)
            return redirect(url_for('.select_Projects_query'))
        # --------------------------------------------------------------
        # Code for NEW option
        # GV 20190109 f.write(        "        elif   form.submit_New.data:\n")
        elif   form.submit_New.data and current_user.role_id>1:
            #print('New Data Here ...')
            session['is_new_row']=True
            db.session.flush()
            row=projects()
    
            return redirect(url_for('.forms_Projects'))    
    
        # Code for CANCEL option 
        elif   form.submit_Cancel.data:
            #print('Cancel Data Here ... does nothing')
            message=Markup('Projects Record modifications discarded ...')
            flash(message)
        # Code for ANY OTHER option should never get here
        else:
            #print('form validated but not submited ???')
            message=Markup("<b>Projects data modifications not allowed for user '%s'. Please contact EG Suite's Administrator ...</b>"%(current_user.username))    
            flash(message)
    
            return redirect(url_for('.forms_'))    
    
    
    form.project_uuid.data = row.project_uuid
    form.project_name.data = row.project_name
    form.project_subnets.data = row.project_subnets
    session['prev_row'] = str(row)
    session['is_new_row'] = False
    logger.debug('forms_Projects(): Exit')
    # Generates pagination data here
    P=[]
    # Tab Relations = [{'name': 'nutanix_prism_vm', 'class': 'nutanix_prism_vm', 'backref': 'projects', 'caption': 'NUTANIX_PRISM_VM', 'table': 'Nutanix_Prism_VM'}]
    
    from flask_sqlalchemy import Pagination
    # [{'name': 'nutanix_prism_vm', 'class': 'nutanix_prism_vm', 'backref': 'projects', 'caption': 'NUTANIX_PRISM_VM', 'table': 'Nutanix_Prism_VM'}]
    try:
        if hasattr(row, 'nutanix_prism_vm'):
            P.append(({'name': 'nutanix_prism_vm', 'class': 'nutanix_prism_vm', 'backref': 'projects', 'caption': 'NUTANIX_PRISM_VM', 'table': 'Nutanix_Prism_VM'},row.nutanix_prism_vm.paginate()))
    except Exception as e:
        print(f'Exception: {str(e)}')
    
    
    # Generation of pagination data completed
    collectordata={}
    collectordata.update({"COLLECTOR_PERIOD":get_period_data(current_user.id,db.engine,Interface)})
    return render_template('projects.html', form=form, row=row, P=P,collectordata=collectordata)    
# ======================================================================



# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2022-03-23 18:29:44.584597
# ======================================================================        
# gen_views_delete.html:AG 2022-03-23 18:29:44.584616
@main.route('/forms/Projects_delete', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DELETE)
@admin_required
def forms_Projects_delete():
    """ Delete record handling function for table Projects """
    logger.debug('forms_Projects_delete(): Enter')
    project_uuid  =  request.args.get('project_uuid',0,type=int)
    row =  projects.query.filter(projects.project_uuid == project_uuid).first()

    if row is None:
        row=projects()
    session['data'] =  {  'project_uuid':row.project_uuid, 'project_name':row.project_name, 'project_subnets':row.project_subnets }
                       
    form = frm_projects_delete()

    # Tab['has_fks'] False
    
            
    # Actual Form activation here
    if form.validate_on_submit():
    
    # Code for SAVE option
        if  form.submit_Delete.data:
            print('Delete Data Here...')

    
    #f.write(        "            print('Delete Data Here...')
            try:
                session['deleted_row']=str(row)
                db.session.flush()
                db.session.delete(row)
                db.session.commit()
                db.session.flush()
                logger.audit ( '%s:DEL:%s' % (current_user.username,session['deleted_row']) )
                flash('Projects project_uuid deleted OK')
            except exc.IntegrityError as e:
                db.session.rollback()    
                flash('INTEGRITY ERROR: Are you sure there are no dependant records in other tables?')
                return redirect(url_for('.forms_Projects_delete',project_uuid=session['data']['project_uuid']))    
    
            return redirect(url_for('.select_Projects_query'))    
    # Code for CANCEL option 
        elif   form.submit_Cancel.data:
            print('Cancel Data Here ... does nothing')
            flash('Record modifications discarded ...')
            return redirect(url_for('.select_Projects_query'))    
    # Code for ANY OTHER option should never get here
        else:
            print('form validated but not submited ???')
            return redirect(url_for('.select_Projects_query'))    
    
    logger.debug('forms_Projects_delete(): Exit')
    collectordata={}
    collectordata.update({"COLLECTOR_PERIOD":get_period_data(current_user.id,db.engine,Interface)})
    return render_template('projects_delete.html', form=form, data=session.get('data'),row=row,collectordata=collectordata)
#===============================================================================

# table_name: Projects
# class_name: projects
# is shardened: False
# current_app: 
# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2022-03-23 18:29:44.606688
# ======================================================================

# gen_views_select_query.html:AG 2022-03-23 18:29:44.606728        
@main.route('/select/Projects_Query', methods=['GET','POST'])
@login_required
@admin_required
def select_Projects_query():
    """ Select rows handling function for table 'Projects' """
    logger.debug('select_Projects_query(): Enter')
    #chk_c000001(filename=os.path.join(current_app.root_path, '.c000001'),request=request,db=db,logger=logger)
    # Shardening Code goes her if needed
    collectordata={}
    collectordata.update({"COLLECTOR_PERIOD":get_period_data(current_user.id,db.engine,Interface)})
    collectordata.update({"CONFIG":current_app.config})
    suffix = collectordata['COLLECTOR_PERIOD']['active']
    table_name='Projects'
    class_name='projects'
    template_name='Projects'
    sharding=False


    logger.debug("-----------------------------------------------------------")
    logger.debug("%s: template_name            = %s",__name__,template_name)

    logger.debug("-----------------------------------------------------------")    
        
    # Get parameters from URL call
    ia       =  request.args.get('ia',     None,type=str)
    if ia is not None:
        ia=ia.split(',')
        if ia[0]=='ORDER':
            #set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name='projects',Option_Type=OPTION_ORDER_BY,Argument_1=ia[1],Argument_2=ia[2])
            set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name=class_name,Option_Type=OPTION_ORDER_BY,Argument_1=ia[1],Argument_2=ia[2])
        elif ia[0]=='GROUP':
            #set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name='projects',Option_Type=OPTION_GROUP_BY,Argument_1=ia[1])
            set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name=class_name,Option_Type=OPTION_GROUP_BY,Argument_1=ia[1])
        elif ia[0]=='LIMIT':
            #set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name='projects',Option_Type=OPTION_LIMIT,Argument_1=ia[1])
            set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name=class_name,Option_Type=OPTION_LIMIT,Argument_1=ia[1])

    iad      =  request.args.get('iad',     None,type=int)
    if iad is not None: delete_query_option(engine=db.engine,Interface=Interface,Id=iad) 
    
    field    =  request.args.get('field',   None,type=str)
    value    =  request.args.get('value',   None,type=str)
    
    # Populates a list of foreign keys used for advanced filtering
    # ------------------------------------------------------------------
    foreign_keys={}
    
    # ------------------------------------------------------------------
    
    if field is not None:
        reset_query_options(    engine=db.engine,Interface=Interface,
                                User_Id=current_user.id,
                                #Table_name='projects'
                                Table_name=class_name
                                )

        
        if field in foreign_keys.keys():
            Class,referenced_classname,referenced_Field,referenced_Value,column_Header=foreign_keys[field]
            foreign_field='%s.%s:%s'%(referenced_classname,referenced_Value,column_Header)
            foreign_record=Class.query.get(value)
            foreign_description="'%s'"%getattr(foreign_record,referenced_Value)
        set_query_option(   engine=db.engine,Interface=Interface,
                        User_Id=current_user.id,
                        Table_name=class_name,
                        Option_Type=OPTION_FILTER,
                        Argument_1=foreign_field,
                        Argument_2='==',
                        Argument_3=foreign_description
                        )
    page     =  request.args.get('page',    1   ,type=int)
    addx     =  request.args.get('add.x',   None,type=int)
    addy     =  request.args.get('add.y',   None,type=int)
    exportx  =  request.args.get('export.x',None,type=int)
    exporty  =  request.args.get('export.y',None,type=int)
    filterx  =  request.args.get('filter.x',None,type=int)
    filtery  =  request.args.get('filter.y',None,type=int)
    # Select excluyent view mode
    if   addx    is not None: mode = 'add'
    elif exportx is not None: mode = 'export'
    elif filterx is not None: mode = 'filter'
    else:                     mode = 'select'
    project_uuid =  request.args.get('project_uuid',None,type=str)
    project_name =  request.args.get('project_name',None,type=str)
    project_subnets =  request.args.get('project_subnets',None,type=str)
    
    # Build default query all fields from table
    

    if project_uuid is not None and len(project_uuid)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='project_uuid:project_uuid',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%project_uuid
                )
    
    
    if project_name is not None and len(project_name)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='project_name:project_name',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%project_name
                )
    
    
    if project_subnets is not None and len(project_subnets)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='project_subnets:project_subnets',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%project_subnets
                )
    
    
    
    statement_query,options=get_query_options(engine=db.engine,Interface=Interface,Table_name=class_name,User_Id=current_user.id)
    tracebox_log(statement_query,logger,length=80)
    query=eval(statement_query)
    filtered_query = query    
    if mode == 'filter':
        query=filtered_query
    elif mode == 'export':
        query=filtered_query
        fh,output_file = tempfile.mkstemp(suffix='', prefix='%s_'%table_name, dir=None, text=False)
        dict = {'header':{},'detail':[]}
        count = 0
        rows = query.all()
        for row in rows:
            dict['detail'].append({})
            for column in ['project_uuid', 'project_name', 'project_subnets']:
                dict['detail'][count].update( { column:str(row.__getattribute__(column))})
                
            count += 1
        dict['header'].update({'count':count})
        jsonarray      = json.dumps(dict)
        data           = json.loads(jsonarray)  
        dataframe      = json_normalize(data, 'detail').assign(**data['header'])
        fh,output_file = tempfile.mkstemp(suffix='', prefix='%_'%table_name, dir='/tmp', text=False)
        xlsx_file      = '%s/%s'%(current_app.root_path,url_for('static',filename='%s.xls'%(output_file)))
        dataframe.to_excel(xlsx_file,sheet_name=table_name,columns=['project_uuid', 'project_name', 'project_subnets'])
        return send_file(xlsx_file,as_attachment=True,attachment_filename=output_file.replace('/','_')+'.xls')
    elif mode == 'add':
        return redirect(url_for('.forms_%s'%table_name))
    elif mode == 'select':
        pass
        # if some filter is required
        if field is not None:
            if field == 'project_uuid':
                if value is not None:
                    query = query.filter_by(project_uuid=value)
            if field == 'project_name':
                if value is not None:
                    query = query.filter_by(project_name=value)
            if field == 'project_subnets':
                if value is not None:
                    query = query.filter_by(project_subnets=value)
            
    # Actual request from DB follows
    tracebox_log(query,logger,length=80)
    # getting paginated rows for query
    rows = query.paginate(page, per_page=current_app.config['LINES_PER_PAGE'], error_out=False)
    # Setting pagination variables ...
    if field is not None:
       next_url = url_for('.select_%s_query'%template_name, field=field, value=value, page=rows.next_num) if rows.has_next else None
       prev_url = url_for('.select_%s_query'%template_name, field=field, value=value, page=rows.prev_num) if rows.has_prev else None
    else:
       next_url = url_for('.select_%s_query'%template_name, page=rows.next_num) if rows.has_next else None
       prev_url = url_for('.select_%s_query'%template_name, page=rows.prev_num) if rows.has_prev else None
    # Actual rendering ...
    if request.headers.get('Content-Type') is not None or request.args.get('JSON',None,type=str) is not None:
        # NOTE: needs review for JSONnifiyng output when needed (API Interface?)
        if "JSON" in request.headers.get('Content-Type') or request.args.get('JSON',None,type=str) is not None:
            logger.debug('select_%s_query(): will render: JSON rows'%template_name)
            logger.debug('select_%s_query(): Exit'%template_name)
            return json.dumps(serialize_object(rows.__dict__))
    logger.debug('select_%s_query(): will render: %s_All.html'%(template_name,table_name.lower()))
    logger.debug('select_%s_query(): Exit'%template_name)
    return render_template('%s_select_All.html'%template_name.lower(),rows=rows,options=options,collectordata=collectordata)
#===============================================================================
   
# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2022-03-23 18:29:44.646574
# ======================================================================
# gen_views_api.html:AG 2022-03-23 18:29:44.646594
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
        #response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        #response.headers['Pragma']        = 'no-cache'
        try:
            id_counter = 0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values=[id]
            # Codigo para un solo campo de id
            # chequear si marcado explicitamente
            db.session.flush()
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
                    if 'project_subnets' in request.args:
                        query = query.filter(Projects.project_subnets == request.args.get('project_subnets'))
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
            row.project_subnets = request.json.get('project_subnets',None)
            # ----------------------------------------------------------
            db.session.add(row)
            db.session.flush()
            db.session.commit()
            db.session.flush()
            db.session.refresh(row)
            db.session.flush()
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
                if 'project_subnets' in request.json.keys():
                    row.project_subnets = request.json.get('project_subnets')
                # ----------------------------------------------------------
                db.session.merge(row)
                db.session.flush()
                db.session.commit()
                db.session.flush()
                db.session.refresh(row)
                db.session.flush()
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
                db.session.rollback()
                if request.values is not None and len(request.values):
                    if 'project_name' in request.values:
                        row.project_name = request.values.get('project_name')
                    if 'project_subnets' in request.values:
                        row.project_subnets = request.values.get('project_subnets')
                # ----------------------------------------------------------
                db.session.merge(row)
                db.session.flush()
                db.session.commit()
                db.session.flush()
                db.session.refresh(row)
                db.session.flush()
                message = f"Modified 'Projects' project_uuid = {id}"
                try:
                    row     = json.loads(row.get_json())
                except:
                    row     = None
            else:
                code    = API_NOT_FOUND
                message = f"Not found Projects with project_uuid = {id}"
                row     = None
                db.session.rollback()
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
            row     = None
            db.session.rollback()
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
                db.session.flush()
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

# ======================================================================# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2022-03-23 18:29:41
# =============================================================================
# gen_views.py:32 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/views/view_rates.py

# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2022-03-23 18:29:44.799998
# ======================================================================        
# gen_views_delete.html:AG 2022-03-23 18:29:44.800016
@main.route('/forms/Rates_delete', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DELETE)
@admin_required
def forms_Rates_delete():
    """ Delete record handling function for table Rates """
    logger.debug('forms_Rates_delete(): Enter')
    Rat_Id  =  request.args.get('Rat_Id',0,type=int)
    row =  rates.query.filter(rates.Rat_Id == Rat_Id).first()

    if row is None:
        row=rates()
    session['data'] =  {  'Rat_Id':row.Rat_Id, 'Typ_Code':row.Typ_Code, 'Cus_Id':row.Cus_Id, 'Pla_Id':row.Pla_Id, 'CC_Id':row.CC_Id, 'CI_Id':row.CI_Id, 'Rat_Price':row.Rat_Price, 'Cur_Code':row.Cur_Code, 'MU_Code':row.MU_Code, 'Rat_Period':row.Rat_Period, 'Rat_Type':row.Rat_Type }
                       
    form = frm_rates_delete()

    # Tab['has_fks'] False
    
            
    # Actual Form activation here
    if form.validate_on_submit():
    
    # Code for SAVE option
        if  form.submit_Delete.data:
            print('Delete Data Here...')

    
    #f.write(        "            print('Delete Data Here...')
            try:
                session['deleted_row']=str(row)
                db.session.flush()
                db.session.delete(row)
                db.session.commit()
                db.session.flush()
                logger.audit ( '%s:DEL:%s' % (current_user.username,session['deleted_row']) )
                flash('Rates Rat_Id deleted OK')
            except exc.IntegrityError as e:
                db.session.rollback()    
                flash('INTEGRITY ERROR: Are you sure there are no dependant records in other tables?')
                return redirect(url_for('.forms_Rates_delete',Rat_Id=session['data']['Rat_Id']))    
    
            return redirect(url_for('.select_Rates_query'))    
    # Code for CANCEL option 
        elif   form.submit_Cancel.data:
            print('Cancel Data Here ... does nothing')
            flash('Record modifications discarded ...')
            return redirect(url_for('.select_Rates_query'))    
    # Code for ANY OTHER option should never get here
        else:
            print('form validated but not submited ???')
            return redirect(url_for('.select_Rates_query'))    
    
    logger.debug('forms_Rates_delete(): Exit')
    collectordata={}
    collectordata.update({"COLLECTOR_PERIOD":get_period_data(current_user.id,db.engine,Interface)})
    return render_template('rates_delete.html', form=form, data=session.get('data'),row=row,collectordata=collectordata)
#===============================================================================

# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2022-03-23 18:29:44.872386
# ======================================================================
# gen_views_api.html:AG 2022-03-23 18:29:44.872415
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
        #response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        #response.headers['Pragma']        = 'no-cache'
        try:
            id_counter = 0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values=[id]
            # Codigo para un solo campo de id
            # chequear si marcado explicitamente
            db.session.flush()
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
            db.session.flush()
            db.session.refresh(row)
            db.session.flush()
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
                db.session.flush()
                db.session.refresh(row)
                db.session.flush()
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
                db.session.rollback()
                if request.values is not None and len(request.values):
                    if 'Typ_Code' in request.values:
                        row.Typ_Code = request.values.get('Typ_Code')
                    if 'Cus_Id' in request.values:
                        row.Cus_Id = request.values.get('Cus_Id')
                    if 'Pla_Id' in request.values:
                        row.Pla_Id = request.values.get('Pla_Id')
                    if 'CC_Id' in request.values:
                        row.CC_Id = request.values.get('CC_Id')
                    if 'CI_Id' in request.values:
                        row.CI_Id = request.values.get('CI_Id')
                    if 'Rat_Price' in request.values:
                        row.Rat_Price = request.values.get('Rat_Price')
                    if 'Cur_Code' in request.values:
                        row.Cur_Code = request.values.get('Cur_Code')
                    if 'MU_Code' in request.values:
                        row.MU_Code = request.values.get('MU_Code')
                    if 'Rat_Period' in request.values:
                        row.Rat_Period = request.values.get('Rat_Period')
                    if 'Rat_Type' in request.values:
                        row.Rat_Type = request.values.get('Rat_Type')
                # ----------------------------------------------------------
                db.session.merge(row)
                db.session.flush()
                db.session.commit()
                db.session.flush()
                db.session.refresh(row)
                db.session.flush()
                message = f"Modified 'Rates' Rat_Id = {id}"
                try:
                    row     = json.loads(row.get_json())
                except:
                    row     = None
            else:
                code    = API_NOT_FOUND
                message = f"Not found Rates with Rat_Id = {id}"
                row     = None
                db.session.rollback()
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
            row     = None
            db.session.rollback()
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
                db.session.flush()
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

# ======================================================================# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2022-03-23 18:29:41
# =============================================================================
# gen_views.py:32 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/views/view_requests.py
# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2022-03-23 18:29:45.225583
# ======================================================================        
# gen_views_form.html:AG 2022-03-23 18:29:45.225599
@main.route('/forms/Requests', methods=['GET', 'POST'])
@login_required

def forms_Requests():
    """ Form handling function for table Requests """
    logger.debug('forms_Requests(): Enter')
    
    # Shardening Code goes her if needed
    collectordata={}
    collectordata.update({"COLLECTOR_PERIOD":get_period_data(current_user.id,db.engine,Interface)})
    collectordata.update({"CONFIG":current_app.config})
    suffix = collectordata['COLLECTOR_PERIOD']['active']
    table_name='Requests'
    class_name='requests'
    template_name='Requests'
    sharding=False
    Id  =  request.args.get('Id',0,type=int)
    
    # Ensures DB Data is commited prior main query
    try:
        db.session.commit()
    except:
        db.session.rollback()
    row =  requests.query.filter(requests.Id == Id).first()
    if row is None:
        row=requests()
        session['is_new_row']=True
    session['data'] =  {  'Id':row.Id, 'Type':row.Type, 'User_Id':row.User_Id, 'Approver_Id':row.Approver_Id, 'Status':row.Status, 'Creation_Time':row.Creation_Time, 'Last_Status_Time':row.Last_Status_Time, 'Comments':row.Comments, 'Task_uuid':row.Task_uuid, 'Task_status':row.Task_status, 'CC_Id':row.CC_Id, 'uuid':row.uuid, 'User_Comments':row.User_Comments }
    
    form = frm_requests()
    
    if form.has_FKs:
        form.Type.choices = db.session.query(request_type.Type,request_type.Description).order_by(request_type.Description).all()

    
    # Actual Form activation here
    if form.validate_on_submit():
        # Code for SAVE option -----------------------------------------
        if form.submit_Save.data and current_user.role_id > 1:
            
            row.Type = form.Type.data
            row.User_Id = form.User_Id.data
            row.Approver_Id = form.Approver_Id.data
            row.Status = form.Status.data
            row.Creation_Time = form.Creation_Time.data
            row.Last_Status_Time = form.Last_Status_Time.data
            row.Comments = form.Comments.data
            row.Task_uuid = form.Task_uuid.data
            row.Task_status = form.Task_status.data
            row.CC_Id = form.CC_Id.data
            row.uuid = form.uuid.data
            row.User_Comments = form.User_Comments.data
            try:
               session['new_row']=str(row)
               db.session.flush()
               db.session.add(row)
               db.session.commit()
               db.session.flush()
               if session['is_new_row']==True:
                   logger.audit ( '%s:NEW:%s' % (current_user.username,session['new_row'] ) )
                   flash('New Requests created OK')
               else:
                   logger.audit ( '%s:OLD:%s' % (current_user.username,session['prev_row']) )
                   logger.audit ( '%s:UPD:%s' % (current_user.username,session['new_row'] ) )    
                   message=Markup('<b>Requests Id saved OK</b>')
                   flash(message)
               db.session.flush()
            except Exception as e:
               db.session.rollback()
               db.session.flush()
               message=Markup('ERROR saving Requests record : %s'%(e))
               flash(message)
            return redirect(url_for('.select_Requests_query'))
        # --------------------------------------------------------------
        # Code for NEW option
        # GV 20190109 f.write(        "        elif   form.submit_New.data:\n")
        elif   form.submit_New.data and current_user.role_id>1:
            #print('New Data Here ...')
            session['is_new_row']=True
            db.session.flush()
            row=requests()
    
            return redirect(url_for('.forms_Requests',Id=row.Id))
    
        # Code for CANCEL option 
        elif   form.submit_Cancel.data:
            #print('Cancel Data Here ... does nothing')
            message=Markup('Requests Record modifications discarded ...')
            flash(message)
        # Code for ANY OTHER option should never get here
        else:
            #print('form validated but not submited ???')
            message=Markup("<b>Requests data modifications not allowed for user '%s'. Please contact EG Suite's Administrator ...</b>"%(current_user.username))    
            flash(message)
    
            return redirect(url_for('.forms_Requests',Id=row.Id))
    
    
    form.Type.data = row.Type
    form.User_Id.data = row.User_Id
    form.Approver_Id.data = row.Approver_Id
    form.Status.data = row.Status
    form.Creation_Time.data = row.Creation_Time
    form.Last_Status_Time.data = row.Last_Status_Time
    form.Comments.data = row.Comments
    form.Task_uuid.data = row.Task_uuid
    form.Task_status.data = row.Task_status
    form.CC_Id.data = row.CC_Id
    form.uuid.data = row.uuid
    form.User_Comments.data = row.User_Comments
    session['prev_row'] = str(row)
    session['is_new_row'] = False
    logger.debug('forms_Requests(): Exit')
    # Generates pagination data here
    P=[]
    # Tab Relations = [{'name': 'nutanix_prism_vm', 'class': 'nutanix_prism_vm', 'backref': 'requests', 'caption': 'NUTANIX_PRISM_VM', 'table': 'Nutanix_Prism_VM'}]
    
    from flask_sqlalchemy import Pagination
    # [{'name': 'nutanix_prism_vm', 'class': 'nutanix_prism_vm', 'backref': 'requests', 'caption': 'NUTANIX_PRISM_VM', 'table': 'Nutanix_Prism_VM'}]
    try:
        if hasattr(row, 'nutanix_prism_vm'):
            P.append(({'name': 'nutanix_prism_vm', 'class': 'nutanix_prism_vm', 'backref': 'requests', 'caption': 'NUTANIX_PRISM_VM', 'table': 'Nutanix_Prism_VM'},row.nutanix_prism_vm.paginate()))
    except Exception as e:
        print(f'Exception: {str(e)}')
    
    
    # Generation of pagination data completed
    collectordata={}
    collectordata.update({"COLLECTOR_PERIOD":get_period_data(current_user.id,db.engine,Interface)})
    return render_template('requests.html', form=form, row=row, P=P,collectordata=collectordata)    
# ======================================================================



# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2022-03-23 18:29:45.234828
# ======================================================================        
# gen_views_delete.html:AG 2022-03-23 18:29:45.234844
@main.route('/forms/Requests_delete', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DELETE)
@admin_required
def forms_Requests_delete():
    """ Delete record handling function for table Requests """
    logger.debug('forms_Requests_delete(): Enter')
    Id  =  request.args.get('Id',0,type=int)
    row =  requests.query.filter(requests.Id == Id).first()

    if row is None:
        row=requests()
    session['data'] =  {  'Id':row.Id, 'Type':row.Type, 'User_Id':row.User_Id, 'Approver_Id':row.Approver_Id, 'Status':row.Status, 'Creation_Time':row.Creation_Time, 'Last_Status_Time':row.Last_Status_Time, 'Comments':row.Comments, 'Task_uuid':row.Task_uuid, 'Task_status':row.Task_status, 'CC_Id':row.CC_Id, 'uuid':row.uuid, 'User_Comments':row.User_Comments }
                       
    form = frm_requests_delete()

    # Tab['has_fks'] True
    
    pass # Tab['has_fks'] True
    
            
    # Actual Form activation here
    if form.validate_on_submit():
    
    # Code for SAVE option
        if  form.submit_Delete.data:
            print('Delete Data Here...')

    
    #f.write(        "            print('Delete Data Here...')
            try:
                session['deleted_row']=str(row)
                db.session.flush()
                db.session.delete(row)
                db.session.commit()
                db.session.flush()
                logger.audit ( '%s:DEL:%s' % (current_user.username,session['deleted_row']) )
                flash('Requests Id deleted OK')
            except exc.IntegrityError as e:
                db.session.rollback()    
                flash('INTEGRITY ERROR: Are you sure there are no dependant records in other tables?')
                return redirect(url_for('.forms_Requests_delete',Id=session['data']['Id']))    
    
            return redirect(url_for('.select_Requests_query'))    
    # Code for CANCEL option 
        elif   form.submit_Cancel.data:
            print('Cancel Data Here ... does nothing')
            flash('Record modifications discarded ...')
            return redirect(url_for('.select_Requests_query'))    
    # Code for ANY OTHER option should never get here
        else:
            print('form validated but not submited ???')
            return redirect(url_for('.select_Requests_query'))    
    
    logger.debug('forms_Requests_delete(): Exit')
    collectordata={}
    collectordata.update({"COLLECTOR_PERIOD":get_period_data(current_user.id,db.engine,Interface)})
    return render_template('requests_delete.html', form=form, data=session.get('data'),row=row,collectordata=collectordata)
#===============================================================================

# table_name: Requests
# class_name: requests
# is shardened: False
# current_app: 
# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2022-03-23 18:29:45.254578
# ======================================================================

# gen_views_select_query.html:AG 2022-03-23 18:29:45.254595        
@main.route('/select/Requests_Query', methods=['GET','POST'])
@login_required
@admin_required
def select_Requests_query():
    """ Select rows handling function for table 'Requests' """
    logger.debug('select_Requests_query(): Enter')
    #chk_c000001(filename=os.path.join(current_app.root_path, '.c000001'),request=request,db=db,logger=logger)
    # Shardening Code goes her if needed
    collectordata={}
    collectordata.update({"COLLECTOR_PERIOD":get_period_data(current_user.id,db.engine,Interface)})
    collectordata.update({"CONFIG":current_app.config})
    suffix = collectordata['COLLECTOR_PERIOD']['active']
    table_name='Requests'
    class_name='requests'
    template_name='Requests'
    sharding=False


    logger.debug("-----------------------------------------------------------")
    logger.debug("%s: template_name            = %s",__name__,template_name)

    logger.debug("-----------------------------------------------------------")    
        
    # Get parameters from URL call
    ia       =  request.args.get('ia',     None,type=str)
    if ia is not None:
        ia=ia.split(',')
        if ia[0]=='ORDER':
            #set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name='requests',Option_Type=OPTION_ORDER_BY,Argument_1=ia[1],Argument_2=ia[2])
            set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name=class_name,Option_Type=OPTION_ORDER_BY,Argument_1=ia[1],Argument_2=ia[2])
        elif ia[0]=='GROUP':
            #set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name='requests',Option_Type=OPTION_GROUP_BY,Argument_1=ia[1])
            set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name=class_name,Option_Type=OPTION_GROUP_BY,Argument_1=ia[1])
        elif ia[0]=='LIMIT':
            #set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name='requests',Option_Type=OPTION_LIMIT,Argument_1=ia[1])
            set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name=class_name,Option_Type=OPTION_LIMIT,Argument_1=ia[1])

    iad      =  request.args.get('iad',     None,type=int)
    if iad is not None: delete_query_option(engine=db.engine,Interface=Interface,Id=iad) 
    
    field    =  request.args.get('field',   None,type=str)
    value    =  request.args.get('value',   None,type=str)
    
    # Populates a list of foreign keys used for advanced filtering
    # ------------------------------------------------------------------
    foreign_keys={}
    
    foreign_keys.update({'Type':(request_type,'request_type','Id','Description','Type')})
    # ------------------------------------------------------------------
    
    if field is not None:
        reset_query_options(    engine=db.engine,Interface=Interface,
                                User_Id=current_user.id,
                                #Table_name='requests'
                                Table_name=class_name
                                )

        
        if field in foreign_keys.keys():
            Class,referenced_classname,referenced_Field,referenced_Value,column_Header=foreign_keys[field]
            foreign_field='%s.%s:%s'%(referenced_classname,referenced_Value,column_Header)
            foreign_record=Class.query.get(value)
            foreign_description="'%s'"%getattr(foreign_record,referenced_Value)
        set_query_option(   engine=db.engine,Interface=Interface,
                        User_Id=current_user.id,
                        Table_name=class_name,
                        Option_Type=OPTION_FILTER,
                        Argument_1=foreign_field,
                        Argument_2='==',
                        Argument_3=foreign_description
                        )
    page     =  request.args.get('page',    1   ,type=int)
    addx     =  request.args.get('add.x',   None,type=int)
    addy     =  request.args.get('add.y',   None,type=int)
    exportx  =  request.args.get('export.x',None,type=int)
    exporty  =  request.args.get('export.y',None,type=int)
    filterx  =  request.args.get('filter.x',None,type=int)
    filtery  =  request.args.get('filter.y',None,type=int)
    # Select excluyent view mode
    if   addx    is not None: mode = 'add'
    elif exportx is not None: mode = 'export'
    elif filterx is not None: mode = 'filter'
    else:                     mode = 'select'
    Id =  request.args.get('Id',None,type=str)
    Type =  request.args.get('Type',None,type=str)
    User_Id =  request.args.get('User_Id',None,type=str)
    Approver_Id =  request.args.get('Approver_Id',None,type=str)
    Status =  request.args.get('Status',None,type=str)
    Creation_Time =  request.args.get('Creation_Time',None,type=str)
    Last_Status_Time =  request.args.get('Last_Status_Time',None,type=str)
    Comments =  request.args.get('Comments',None,type=str)
    Task_uuid =  request.args.get('Task_uuid',None,type=str)
    Task_status =  request.args.get('Task_status',None,type=str)
    CC_Id =  request.args.get('CC_Id',None,type=str)
    uuid =  request.args.get('uuid',None,type=str)
    User_Comments =  request.args.get('User_Comments',None,type=str)
    
    # Build default query all fields from table
    

    if Id is not None and len(Id)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='Id:Id',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%Id
                )
    
    
    if Type is not None and len(Type)>0:
            Class,referenced_classname,referenced_Field,referenced_Value,column_Header=foreign_keys['Type']
            foreign_field='%s.%s:%s'%(referenced_classname,referenced_Value,column_Header)            
            set_query_option(   engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1=foreign_field,
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%Type
                )
                                
    
    
    if User_Id is not None and len(User_Id)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='User_Id:User_Id',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%User_Id
                )
    
    
    if Approver_Id is not None and len(Approver_Id)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='Approver_Id:Approver_Id',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%Approver_Id
                )
    
    
    if Status is not None and len(Status)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='Status:Status',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%Status
                )
    
    
    if Creation_Time is not None and len(Creation_Time)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='Creation_Time:Creation_Time',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%Creation_Time
                )
    
    
    if Last_Status_Time is not None and len(Last_Status_Time)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='Last_Status_Time:Last_Status_Time',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%Last_Status_Time
                )
    
    
    if Comments is not None and len(Comments)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='Comments:Comments',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%Comments
                )
    
    
    if Task_uuid is not None and len(Task_uuid)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='Task_uuid:Task_uuid',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%Task_uuid
                )
    
    
    if Task_status is not None and len(Task_status)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='Task_status:Task_status',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%Task_status
                )
    
    
    if CC_Id is not None and len(CC_Id)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='CC_Id:CC_Id',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%CC_Id
                )
    
    
    if uuid is not None and len(uuid)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='uuid:uuid',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%uuid
                )
    
    
    if User_Comments is not None and len(User_Comments)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='User_Comments:User_Comments',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%User_Comments
                )
    
    
    
    statement_query,options=get_query_options(engine=db.engine,Interface=Interface,Table_name=class_name,User_Id=current_user.id)
    tracebox_log(statement_query,logger,length=80)
    query=eval(statement_query)
    filtered_query = query    
    if mode == 'filter':
        query=filtered_query
    elif mode == 'export':
        query=filtered_query
        fh,output_file = tempfile.mkstemp(suffix='', prefix='%s_'%table_name, dir=None, text=False)
        dict = {'header':{},'detail':[]}
        count = 0
        rows = query.all()
        for row in rows:
            dict['detail'].append({})
            for column in ['Id', 'Type', 'User_Id', 'Approver_Id', 'Status', 'Creation_Time', 'Last_Status_Time', 'Comments', 'Task_uuid', 'Task_status', 'CC_Id', 'uuid', 'User_Comments']:
                dict['detail'][count].update( { column:str(row.__getattribute__(column))})
                
            count += 1
        dict['header'].update({'count':count})
        jsonarray      = json.dumps(dict)
        data           = json.loads(jsonarray)  
        dataframe      = json_normalize(data, 'detail').assign(**data['header'])
        fh,output_file = tempfile.mkstemp(suffix='', prefix='%_'%table_name, dir='/tmp', text=False)
        xlsx_file      = '%s/%s'%(current_app.root_path,url_for('static',filename='%s.xls'%(output_file)))
        dataframe.to_excel(xlsx_file,sheet_name=table_name,columns=['Id', 'Type', 'User_Id', 'Approver_Id', 'Status', 'Creation_Time', 'Last_Status_Time', 'Comments', 'Task_uuid', 'Task_status', 'CC_Id', 'uuid', 'User_Comments'])
        return send_file(xlsx_file,as_attachment=True,attachment_filename=output_file.replace('/','_')+'.xls')
    elif mode == 'add':
        return redirect(url_for('.forms_%s'%table_name))
    elif mode == 'select':
        pass
        # if some filter is required
        if field is not None:
            if field == 'Id':
                if value is not None:
                    query = query.filter_by(Id=value)
            if field == 'Type':
                if value is not None:
                    query = query.filter_by(Type=value)
            if field == 'User_Id':
                if value is not None:
                    query = query.filter_by(User_Id=value)
            if field == 'Approver_Id':
                if value is not None:
                    query = query.filter_by(Approver_Id=value)
            if field == 'Status':
                if value is not None:
                    query = query.filter_by(Status=value)
            if field == 'Creation_Time':
                if value is not None:
                    query = query.filter_by(Creation_Time=value)
            if field == 'Last_Status_Time':
                if value is not None:
                    query = query.filter_by(Last_Status_Time=value)
            if field == 'Comments':
                if value is not None:
                    query = query.filter_by(Comments=value)
            if field == 'Task_uuid':
                if value is not None:
                    query = query.filter_by(Task_uuid=value)
            if field == 'Task_status':
                if value is not None:
                    query = query.filter_by(Task_status=value)
            if field == 'CC_Id':
                if value is not None:
                    query = query.filter_by(CC_Id=value)
            if field == 'uuid':
                if value is not None:
                    query = query.filter_by(uuid=value)
            if field == 'User_Comments':
                if value is not None:
                    query = query.filter_by(User_Comments=value)
            # ------------------------------------------------------------------
    # JOIN other tables and generate foreign fields
    # Will replace class name by sharding class in joins structure
    # will have no effect in no sharding environment
    query = query.join(request_type,requests.Type == request_type.Id).add_columns(request_type.Description)
    # ------------------------------------------------------------------
    
    # Actual request from DB follows
    tracebox_log(query,logger,length=80)
    # getting paginated rows for query
    rows = query.paginate(page, per_page=current_app.config['LINES_PER_PAGE'], error_out=False)
    # Setting pagination variables ...
    if field is not None:
       next_url = url_for('.select_%s_query'%template_name, field=field, value=value, page=rows.next_num) if rows.has_next else None
       prev_url = url_for('.select_%s_query'%template_name, field=field, value=value, page=rows.prev_num) if rows.has_prev else None
    else:
       next_url = url_for('.select_%s_query'%template_name, page=rows.next_num) if rows.has_next else None
       prev_url = url_for('.select_%s_query'%template_name, page=rows.prev_num) if rows.has_prev else None
    # Actual rendering ...
    if request.headers.get('Content-Type') is not None or request.args.get('JSON',None,type=str) is not None:
        # NOTE: needs review for JSONnifiyng output when needed (API Interface?)
        if "JSON" in request.headers.get('Content-Type') or request.args.get('JSON',None,type=str) is not None:
            logger.debug('select_%s_query(): will render: JSON rows'%template_name)
            logger.debug('select_%s_query(): Exit'%template_name)
            return json.dumps(serialize_object(rows.__dict__))
    logger.debug('select_%s_query(): will render: %s_All.html'%(template_name,table_name.lower()))
    logger.debug('select_%s_query(): Exit'%template_name)
    return render_template('%s_select_All.html'%template_name.lower(),rows=rows,options=options,collectordata=collectordata)
#===============================================================================
   
# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2022-03-23 18:29:45.293694
# ======================================================================
# gen_views_api.html:AG 2022-03-23 18:29:45.293713
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
        #response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        #response.headers['Pragma']        = 'no-cache'
        try:
            id_counter = 0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values=[id]
            # Codigo para un solo campo de id
            # chequear si marcado explicitamente
            db.session.flush()
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
                    if 'uuid' in request.args:
                        query = query.filter(Requests.uuid == request.args.get('uuid'))
                    if 'User_Comments' in request.args:
                        query = query.filter(Requests.User_Comments == request.args.get('User_Comments'))
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
            row.uuid = request.json.get('uuid',None)
            row.User_Comments = request.json.get('User_Comments',None)
            # ----------------------------------------------------------
            db.session.add(row)
            db.session.flush()
            db.session.commit()
            db.session.flush()
            db.session.refresh(row)
            db.session.flush()
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
                if 'uuid' in request.json.keys():
                    row.uuid = request.json.get('uuid')
                if 'User_Comments' in request.json.keys():
                    row.User_Comments = request.json.get('User_Comments')
                # ----------------------------------------------------------
                db.session.merge(row)
                db.session.flush()
                db.session.commit()
                db.session.flush()
                db.session.refresh(row)
                db.session.flush()
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
                db.session.rollback()
                if request.values is not None and len(request.values):
                    if 'Type' in request.values:
                        row.Type = request.values.get('Type')
                    if 'User_Id' in request.values:
                        row.User_Id = request.values.get('User_Id')
                    if 'Approver_Id' in request.values:
                        row.Approver_Id = request.values.get('Approver_Id')
                    if 'Status' in request.values:
                        row.Status = request.values.get('Status')
                    if 'Creation_Time' in request.values:
                        row.Creation_Time = request.values.get('Creation_Time')
                    if 'Last_Status_Time' in request.values:
                        row.Last_Status_Time = request.values.get('Last_Status_Time')
                    if 'Comments' in request.values:
                        row.Comments = request.values.get('Comments')
                    if 'Task_uuid' in request.values:
                        row.Task_uuid = request.values.get('Task_uuid')
                    if 'Task_status' in request.values:
                        row.Task_status = request.values.get('Task_status')
                    if 'CC_Id' in request.values:
                        row.CC_Id = request.values.get('CC_Id')
                    if 'uuid' in request.values:
                        row.uuid = request.values.get('uuid')
                    if 'User_Comments' in request.values:
                        row.User_Comments = request.values.get('User_Comments')
                # ----------------------------------------------------------
                db.session.merge(row)
                db.session.flush()
                db.session.commit()
                db.session.flush()
                db.session.refresh(row)
                db.session.flush()
                message = f"Modified 'Requests' Id = {id}"
                try:
                    row     = json.loads(row.get_json())
                except:
                    row     = None
            else:
                code    = API_NOT_FOUND
                message = f"Not found Requests with Id = {id}"
                row     = None
                db.session.rollback()
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
            row     = None
            db.session.rollback()
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
                db.session.flush()
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

# ======================================================================# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2022-03-23 18:29:41
# =============================================================================
# gen_views.py:32 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/views/view_request_type.py
# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2022-03-23 18:29:44.996098
# ======================================================================        
# gen_views_form.html:AG 2022-03-23 18:29:44.996117
@main.route('/forms/Request_Type', methods=['GET', 'POST'])
@login_required

def forms_Request_Type():
    """ Form handling function for table Request_Type """
    logger.debug('forms_Request_Type(): Enter')
    
    # Shardening Code goes her if needed
    collectordata={}
    collectordata.update({"COLLECTOR_PERIOD":get_period_data(current_user.id,db.engine,Interface)})
    collectordata.update({"CONFIG":current_app.config})
    suffix = collectordata['COLLECTOR_PERIOD']['active']
    table_name='Request_Type'
    class_name='request_type'
    template_name='Request_Type'
    sharding=False
    Id  =  request.args.get('Id',0,type=int)
    
    # Ensures DB Data is commited prior main query
    try:
        db.session.commit()
    except:
        db.session.rollback()
    row =  request_type.query.filter(request_type.Id == Id).first()
    if row is None:
        row=request_type()
        session['is_new_row']=True
    session['data'] =  {  'Id':row.Id, 'Description':row.Description, 'Table_Name':row.Table_Name }
    
    form = frm_request_type()
    
    # Actual Form activation here
    if form.validate_on_submit():
        # Code for SAVE option -----------------------------------------
        if form.submit_Save.data and current_user.role_id > 1:
            row.Id = form.Id.data
            row.Description = form.Description.data
            row.Table_Name = form.Table_Name.data
            try:
               session['new_row']=str(row)
               db.session.flush()
               db.session.add(row)
               db.session.commit()
               db.session.flush()
               if session['is_new_row']==True:
                   logger.audit ( '%s:NEW:%s' % (current_user.username,session['new_row'] ) )
                   flash('New Request_type created OK')
               else:
                   logger.audit ( '%s:OLD:%s' % (current_user.username,session['prev_row']) )
                   logger.audit ( '%s:UPD:%s' % (current_user.username,session['new_row'] ) )    
                   message=Markup('<b>Request_type Id saved OK</b>')
                   flash(message)
               db.session.flush()
            except Exception as e:
               db.session.rollback()
               db.session.flush()
               message=Markup('ERROR saving Request_type record : %s'%(e))
               flash(message)
            return redirect(url_for('.select_Request_Type_query'))
        # --------------------------------------------------------------
        # Code for NEW option
        # GV 20190109 f.write(        "        elif   form.submit_New.data:\n")
        elif   form.submit_New.data and current_user.role_id>1:
            #print('New Data Here ...')
            session['is_new_row']=True
            db.session.flush()
            row=request_type()
    
            return redirect(url_for('.forms_Request_Type'))    
    
        # Code for CANCEL option 
        elif   form.submit_Cancel.data:
            #print('Cancel Data Here ... does nothing')
            message=Markup('Request_type Record modifications discarded ...')
            flash(message)
        # Code for ANY OTHER option should never get here
        else:
            #print('form validated but not submited ???')
            message=Markup("<b>Request_type data modifications not allowed for user '%s'. Please contact EG Suite's Administrator ...</b>"%(current_user.username))    
            flash(message)
    
            return redirect(url_for('.forms_'))    
    
    
    form.Id.data = row.Id
    form.Description.data = row.Description
    form.Table_Name.data = row.Table_Name
    session['prev_row'] = str(row)
    session['is_new_row'] = False
    logger.debug('forms_Request_Type(): Exit')
    # Generates pagination data here
    P=[]
    # Tab Relations = [{'name': 'requests', 'class': 'requests', 'backref': 'request_type', 'caption': 'REQUESTS', 'table': 'Requests'}]
    
    from flask_sqlalchemy import Pagination
    # [{'name': 'requests', 'class': 'requests', 'backref': 'request_type', 'caption': 'REQUESTS', 'table': 'Requests'}]
    try:
        if hasattr(row, 'requests'):
            P.append(({'name': 'requests', 'class': 'requests', 'backref': 'request_type', 'caption': 'REQUESTS', 'table': 'Requests'},row.requests.paginate()))
    except Exception as e:
        print(f'Exception: {str(e)}')
    
    
    # Generation of pagination data completed
    collectordata={}
    collectordata.update({"COLLECTOR_PERIOD":get_period_data(current_user.id,db.engine,Interface)})
    return render_template('request_type.html', form=form, row=row, P=P,collectordata=collectordata)    
# ======================================================================



# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2022-03-23 18:29:45.008274
# ======================================================================        
# gen_views_delete.html:AG 2022-03-23 18:29:45.008292
@main.route('/forms/Request_Type_delete', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DELETE)
@admin_required
def forms_Request_Type_delete():
    """ Delete record handling function for table Request_Type """
    logger.debug('forms_Request_Type_delete(): Enter')
    Id  =  request.args.get('Id',0,type=int)
    row =  request_type.query.filter(request_type.Id == Id).first()

    if row is None:
        row=request_type()
    session['data'] =  {  'Id':row.Id, 'Description':row.Description, 'Table_Name':row.Table_Name }
                       
    form = frm_request_type_delete()

    # Tab['has_fks'] False
    
            
    # Actual Form activation here
    if form.validate_on_submit():
    
    # Code for SAVE option
        if  form.submit_Delete.data:
            print('Delete Data Here...')

    
    #f.write(        "            print('Delete Data Here...')
            try:
                session['deleted_row']=str(row)
                db.session.flush()
                db.session.delete(row)
                db.session.commit()
                db.session.flush()
                logger.audit ( '%s:DEL:%s' % (current_user.username,session['deleted_row']) )
                flash('Request_type Id deleted OK')
            except exc.IntegrityError as e:
                db.session.rollback()    
                flash('INTEGRITY ERROR: Are you sure there are no dependant records in other tables?')
                return redirect(url_for('.forms_Request_Type_delete',Id=session['data']['Id']))    
    
            return redirect(url_for('.select_Request_Type_query'))    
    # Code for CANCEL option 
        elif   form.submit_Cancel.data:
            print('Cancel Data Here ... does nothing')
            flash('Record modifications discarded ...')
            return redirect(url_for('.select_Request_Type_query'))    
    # Code for ANY OTHER option should never get here
        else:
            print('form validated but not submited ???')
            return redirect(url_for('.select_Request_Type_query'))    
    
    logger.debug('forms_Request_Type_delete(): Exit')
    collectordata={}
    collectordata.update({"COLLECTOR_PERIOD":get_period_data(current_user.id,db.engine,Interface)})
    return render_template('request_type_delete.html', form=form, data=session.get('data'),row=row,collectordata=collectordata)
#===============================================================================

# table_name: Request_Type
# class_name: request_type
# is shardened: False
# current_app: 
# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2022-03-23 18:29:45.032023
# ======================================================================

# gen_views_select_query.html:AG 2022-03-23 18:29:45.032072        
@main.route('/select/Request_Type_Query', methods=['GET','POST'])
@login_required
@admin_required
def select_Request_Type_query():
    """ Select rows handling function for table 'Request_Type' """
    logger.debug('select_Request_Type_query(): Enter')
    #chk_c000001(filename=os.path.join(current_app.root_path, '.c000001'),request=request,db=db,logger=logger)
    # Shardening Code goes her if needed
    collectordata={}
    collectordata.update({"COLLECTOR_PERIOD":get_period_data(current_user.id,db.engine,Interface)})
    collectordata.update({"CONFIG":current_app.config})
    suffix = collectordata['COLLECTOR_PERIOD']['active']
    table_name='Request_Type'
    class_name='request_type'
    template_name='Request_Type'
    sharding=False


    logger.debug("-----------------------------------------------------------")
    logger.debug("%s: template_name            = %s",__name__,template_name)

    logger.debug("-----------------------------------------------------------")    
        
    # Get parameters from URL call
    ia       =  request.args.get('ia',     None,type=str)
    if ia is not None:
        ia=ia.split(',')
        if ia[0]=='ORDER':
            #set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name='request_type',Option_Type=OPTION_ORDER_BY,Argument_1=ia[1],Argument_2=ia[2])
            set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name=class_name,Option_Type=OPTION_ORDER_BY,Argument_1=ia[1],Argument_2=ia[2])
        elif ia[0]=='GROUP':
            #set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name='request_type',Option_Type=OPTION_GROUP_BY,Argument_1=ia[1])
            set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name=class_name,Option_Type=OPTION_GROUP_BY,Argument_1=ia[1])
        elif ia[0]=='LIMIT':
            #set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name='request_type',Option_Type=OPTION_LIMIT,Argument_1=ia[1])
            set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name=class_name,Option_Type=OPTION_LIMIT,Argument_1=ia[1])

    iad      =  request.args.get('iad',     None,type=int)
    if iad is not None: delete_query_option(engine=db.engine,Interface=Interface,Id=iad) 
    
    field    =  request.args.get('field',   None,type=str)
    value    =  request.args.get('value',   None,type=str)
    
    # Populates a list of foreign keys used for advanced filtering
    # ------------------------------------------------------------------
    foreign_keys={}
    
    # ------------------------------------------------------------------
    
    if field is not None:
        reset_query_options(    engine=db.engine,Interface=Interface,
                                User_Id=current_user.id,
                                #Table_name='request_type'
                                Table_name=class_name
                                )

        
        if field in foreign_keys.keys():
            Class,referenced_classname,referenced_Field,referenced_Value,column_Header=foreign_keys[field]
            foreign_field='%s.%s:%s'%(referenced_classname,referenced_Value,column_Header)
            foreign_record=Class.query.get(value)
            foreign_description="'%s'"%getattr(foreign_record,referenced_Value)
        set_query_option(   engine=db.engine,Interface=Interface,
                        User_Id=current_user.id,
                        Table_name=class_name,
                        Option_Type=OPTION_FILTER,
                        Argument_1=foreign_field,
                        Argument_2='==',
                        Argument_3=foreign_description
                        )
    page     =  request.args.get('page',    1   ,type=int)
    addx     =  request.args.get('add.x',   None,type=int)
    addy     =  request.args.get('add.y',   None,type=int)
    exportx  =  request.args.get('export.x',None,type=int)
    exporty  =  request.args.get('export.y',None,type=int)
    filterx  =  request.args.get('filter.x',None,type=int)
    filtery  =  request.args.get('filter.y',None,type=int)
    # Select excluyent view mode
    if   addx    is not None: mode = 'add'
    elif exportx is not None: mode = 'export'
    elif filterx is not None: mode = 'filter'
    else:                     mode = 'select'
    Id =  request.args.get('Id',None,type=str)
    Description =  request.args.get('Description',None,type=str)
    Table_Name =  request.args.get('Table_Name',None,type=str)
    
    # Build default query all fields from table
    

    if Id is not None and len(Id)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='Id:Id',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%Id
                )
    
    
    if Description is not None and len(Description)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='Description:Description',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%Description
                )
    
    
    if Table_Name is not None and len(Table_Name)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='Table_Name:Table_Name',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%Table_Name
                )
    
    
    
    statement_query,options=get_query_options(engine=db.engine,Interface=Interface,Table_name=class_name,User_Id=current_user.id)
    tracebox_log(statement_query,logger,length=80)
    query=eval(statement_query)
    filtered_query = query    
    if mode == 'filter':
        query=filtered_query
    elif mode == 'export':
        query=filtered_query
        fh,output_file = tempfile.mkstemp(suffix='', prefix='%s_'%table_name, dir=None, text=False)
        dict = {'header':{},'detail':[]}
        count = 0
        rows = query.all()
        for row in rows:
            dict['detail'].append({})
            for column in ['Id', 'Description', 'Table_Name']:
                dict['detail'][count].update( { column:str(row.__getattribute__(column))})
                
            count += 1
        dict['header'].update({'count':count})
        jsonarray      = json.dumps(dict)
        data           = json.loads(jsonarray)  
        dataframe      = json_normalize(data, 'detail').assign(**data['header'])
        fh,output_file = tempfile.mkstemp(suffix='', prefix='%_'%table_name, dir='/tmp', text=False)
        xlsx_file      = '%s/%s'%(current_app.root_path,url_for('static',filename='%s.xls'%(output_file)))
        dataframe.to_excel(xlsx_file,sheet_name=table_name,columns=['Id', 'Description', 'Table_Name'])
        return send_file(xlsx_file,as_attachment=True,attachment_filename=output_file.replace('/','_')+'.xls')
    elif mode == 'add':
        return redirect(url_for('.forms_%s'%table_name))
    elif mode == 'select':
        pass
        # if some filter is required
        if field is not None:
            if field == 'Id':
                if value is not None:
                    query = query.filter_by(Id=value)
            if field == 'Description':
                if value is not None:
                    query = query.filter_by(Description=value)
            if field == 'Table_Name':
                if value is not None:
                    query = query.filter_by(Table_Name=value)
            
    # Actual request from DB follows
    tracebox_log(query,logger,length=80)
    # getting paginated rows for query
    rows = query.paginate(page, per_page=current_app.config['LINES_PER_PAGE'], error_out=False)
    # Setting pagination variables ...
    if field is not None:
       next_url = url_for('.select_%s_query'%template_name, field=field, value=value, page=rows.next_num) if rows.has_next else None
       prev_url = url_for('.select_%s_query'%template_name, field=field, value=value, page=rows.prev_num) if rows.has_prev else None
    else:
       next_url = url_for('.select_%s_query'%template_name, page=rows.next_num) if rows.has_next else None
       prev_url = url_for('.select_%s_query'%template_name, page=rows.prev_num) if rows.has_prev else None
    # Actual rendering ...
    if request.headers.get('Content-Type') is not None or request.args.get('JSON',None,type=str) is not None:
        # NOTE: needs review for JSONnifiyng output when needed (API Interface?)
        if "JSON" in request.headers.get('Content-Type') or request.args.get('JSON',None,type=str) is not None:
            logger.debug('select_%s_query(): will render: JSON rows'%template_name)
            logger.debug('select_%s_query(): Exit'%template_name)
            return json.dumps(serialize_object(rows.__dict__))
    logger.debug('select_%s_query(): will render: %s_All.html'%(template_name,table_name.lower()))
    logger.debug('select_%s_query(): Exit'%template_name)
    return render_template('%s_select_All.html'%template_name.lower(),rows=rows,options=options,collectordata=collectordata)
#===============================================================================
   
# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2022-03-23 18:29:45.072020
# ======================================================================
# gen_views_api.html:AG 2022-03-23 18:29:45.072039
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
        #response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        #response.headers['Pragma']        = 'no-cache'
        try:
            id_counter = 0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values=[id]
            # Codigo para un solo campo de id
            # chequear si marcado explicitamente
            db.session.flush()
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
            db.session.flush()
            db.session.refresh(row)
            db.session.flush()
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
                db.session.flush()
                db.session.refresh(row)
                db.session.flush()
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
                db.session.rollback()
                if request.values is not None and len(request.values):
                    if 'Description' in request.values:
                        row.Description = request.values.get('Description')
                    if 'Table_Name' in request.values:
                        row.Table_Name = request.values.get('Table_Name')
                # ----------------------------------------------------------
                db.session.merge(row)
                db.session.flush()
                db.session.commit()
                db.session.flush()
                db.session.refresh(row)
                db.session.flush()
                message = f"Modified 'Request_Type' Id = {id}"
                try:
                    row     = json.loads(row.get_json())
                except:
                    row     = None
            else:
                code    = API_NOT_FOUND
                message = f"Not found Request_Type with Id = {id}"
                row     = None
                db.session.rollback()
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
            row     = None
            db.session.rollback()
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
                db.session.flush()
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

# ======================================================================# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2022-03-23 18:29:41
# =============================================================================
# gen_views.py:32 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/views/view_roles.py
# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2022-03-23 18:29:45.406794
# ======================================================================        
# gen_views_form.html:AG 2022-03-23 18:29:45.406814
@main.route('/forms/Roles', methods=['GET', 'POST'])
@login_required

def forms_Roles():
    """ Form handling function for table Roles """
    logger.debug('forms_Roles(): Enter')
    
    # Shardening Code goes her if needed
    collectordata={}
    collectordata.update({"COLLECTOR_PERIOD":get_period_data(current_user.id,db.engine,Interface)})
    collectordata.update({"CONFIG":current_app.config})
    suffix = collectordata['COLLECTOR_PERIOD']['active']
    table_name='Roles'
    class_name='Role'
    template_name='Roles'
    sharding=False
    id  =  request.args.get('id',0,type=int)
    
    # Ensures DB Data is commited prior main query
    try:
        db.session.commit()
    except:
        db.session.rollback()
    row =  Role.query.filter(Role.id == id).first()
    if row is None:
        row=Role()
        session['is_new_row']=True
    session['data'] =  {  'id':row.id, 'name':row.name, 'default':row.default, 'permissions':row.permissions }
    
    form = frm_Role()
    
    # Actual Form activation here
    if form.validate_on_submit():
        # Code for SAVE option -----------------------------------------
        if form.submit_Save.data and current_user.role_id > 1:
            row.id = form.id.data
            row.name = form.name.data
            row.default = form.default.data
            row.permissions = form.permissions.data
            try:
               session['new_row']=str(row)
               db.session.flush()
               db.session.add(row)
               db.session.commit()
               db.session.flush()
               if session['is_new_row']==True:
                   logger.audit ( '%s:NEW:%s' % (current_user.username,session['new_row'] ) )
                   flash('New Role created OK')
               else:
                   logger.audit ( '%s:OLD:%s' % (current_user.username,session['prev_row']) )
                   logger.audit ( '%s:UPD:%s' % (current_user.username,session['new_row'] ) )    
                   message=Markup('<b>Role id saved OK</b>')
                   flash(message)
               db.session.flush()
            except Exception as e:
               db.session.rollback()
               db.session.flush()
               message=Markup('ERROR saving Role record : %s'%(e))
               flash(message)
            return redirect(url_for('.select_Roles_query'))
        # --------------------------------------------------------------
        # Code for NEW option
        # GV 20190109 f.write(        "        elif   form.submit_New.data:\n")
        elif   form.submit_New.data and current_user.role_id>1:
            #print('New Data Here ...')
            session['is_new_row']=True
            db.session.flush()
            row=Role()
    
            return redirect(url_for('.forms_Roles'))    
    
        # Code for CANCEL option 
        elif   form.submit_Cancel.data:
            #print('Cancel Data Here ... does nothing')
            message=Markup('Role Record modifications discarded ...')
            flash(message)
        # Code for ANY OTHER option should never get here
        else:
            #print('form validated but not submited ???')
            message=Markup("<b>Role data modifications not allowed for user '%s'. Please contact EG Suite's Administrator ...</b>"%(current_user.username))    
            flash(message)
    
            return redirect(url_for('.forms_'))    
    
    
    form.id.data = row.id
    form.name.data = row.name
    form.default.data = row.default
    form.permissions.data = row.permissions
    session['prev_row'] = str(row)
    session['is_new_row'] = False
    logger.debug('forms_Roles(): Exit')
    # Generates pagination data here
    P=[]
    # Tab Relations = [{'name': 'users', 'class': 'User', 'backref': 'Role', 'caption': 'USERS', 'table': 'Users'}]
    
    from flask_sqlalchemy import Pagination
    # [{'name': 'users', 'class': 'User', 'backref': 'Role', 'caption': 'USERS', 'table': 'Users'}]
    try:
        if hasattr(row, 'users'):
            P.append(({'name': 'users', 'class': 'User', 'backref': 'Role', 'caption': 'USERS', 'table': 'Users'},row.users.paginate()))
    except Exception as e:
        print(f'Exception: {str(e)}')
    
    
    # Generation of pagination data completed
    collectordata={}
    collectordata.update({"COLLECTOR_PERIOD":get_period_data(current_user.id,db.engine,Interface)})
    return render_template('roles.html', form=form, row=row, P=P,collectordata=collectordata)    
# ======================================================================



# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2022-03-23 18:29:45.416949
# ======================================================================        
# gen_views_delete.html:AG 2022-03-23 18:29:45.416968
@main.route('/forms/Roles_delete', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DELETE)
@admin_required
def forms_Roles_delete():
    """ Delete record handling function for table Roles """
    logger.debug('forms_Roles_delete(): Enter')
    id  =  request.args.get('id',0,type=int)
    row =  Role.query.filter(Role.id == id).first()

    if row is None:
        row=Role()
    session['data'] =  {  'id':row.id, 'name':row.name, 'default':row.default, 'permissions':row.permissions }
                       
    form = frm_Role_delete()

    # Tab['has_fks'] False
    
            
    # Actual Form activation here
    if form.validate_on_submit():
    
    # Code for SAVE option
        if  form.submit_Delete.data:
            print('Delete Data Here...')

    
    #f.write(        "            print('Delete Data Here...')
            try:
                session['deleted_row']=str(row)
                db.session.flush()
                db.session.delete(row)
                db.session.commit()
                db.session.flush()
                logger.audit ( '%s:DEL:%s' % (current_user.username,session['deleted_row']) )
                flash('Role id deleted OK')
            except exc.IntegrityError as e:
                db.session.rollback()    
                flash('INTEGRITY ERROR: Are you sure there are no dependant records in other tables?')
                return redirect(url_for('.forms_Roles_delete',id=session['data']['id']))    
    
            return redirect(url_for('.select_Roles_query'))    
    # Code for CANCEL option 
        elif   form.submit_Cancel.data:
            print('Cancel Data Here ... does nothing')
            flash('Record modifications discarded ...')
            return redirect(url_for('.select_Roles_query'))    
    # Code for ANY OTHER option should never get here
        else:
            print('form validated but not submited ???')
            return redirect(url_for('.select_Roles_query'))    
    
    logger.debug('forms_Roles_delete(): Exit')
    collectordata={}
    collectordata.update({"COLLECTOR_PERIOD":get_period_data(current_user.id,db.engine,Interface)})
    return render_template('roles_delete.html', form=form, data=session.get('data'),row=row,collectordata=collectordata)
#===============================================================================

# table_name: Roles
# class_name: Role
# is shardened: False
# current_app: 
# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2022-03-23 18:29:45.436730
# ======================================================================

# gen_views_select_query.html:AG 2022-03-23 18:29:45.436748        
@main.route('/select/Roles_Query', methods=['GET','POST'])
@login_required
@admin_required
def select_Roles_query():
    """ Select rows handling function for table 'Roles' """
    logger.debug('select_Roles_query(): Enter')
    #chk_c000001(filename=os.path.join(current_app.root_path, '.c000001'),request=request,db=db,logger=logger)
    # Shardening Code goes her if needed
    collectordata={}
    collectordata.update({"COLLECTOR_PERIOD":get_period_data(current_user.id,db.engine,Interface)})
    collectordata.update({"CONFIG":current_app.config})
    suffix = collectordata['COLLECTOR_PERIOD']['active']
    table_name='Roles'
    class_name='Role'
    template_name='Roles'
    sharding=False


    logger.debug("-----------------------------------------------------------")
    logger.debug("%s: template_name            = %s",__name__,template_name)

    logger.debug("-----------------------------------------------------------")    
        
    # Get parameters from URL call
    ia       =  request.args.get('ia',     None,type=str)
    if ia is not None:
        ia=ia.split(',')
        if ia[0]=='ORDER':
            #set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name='Role',Option_Type=OPTION_ORDER_BY,Argument_1=ia[1],Argument_2=ia[2])
            set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name=class_name,Option_Type=OPTION_ORDER_BY,Argument_1=ia[1],Argument_2=ia[2])
        elif ia[0]=='GROUP':
            #set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name='Role',Option_Type=OPTION_GROUP_BY,Argument_1=ia[1])
            set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name=class_name,Option_Type=OPTION_GROUP_BY,Argument_1=ia[1])
        elif ia[0]=='LIMIT':
            #set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name='Role',Option_Type=OPTION_LIMIT,Argument_1=ia[1])
            set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name=class_name,Option_Type=OPTION_LIMIT,Argument_1=ia[1])

    iad      =  request.args.get('iad',     None,type=int)
    if iad is not None: delete_query_option(engine=db.engine,Interface=Interface,Id=iad) 
    
    field    =  request.args.get('field',   None,type=str)
    value    =  request.args.get('value',   None,type=str)
    
    # Populates a list of foreign keys used for advanced filtering
    # ------------------------------------------------------------------
    foreign_keys={}
    
    # ------------------------------------------------------------------
    
    if field is not None:
        reset_query_options(    engine=db.engine,Interface=Interface,
                                User_Id=current_user.id,
                                #Table_name='Role'
                                Table_name=class_name
                                )

        
        if field in foreign_keys.keys():
            Class,referenced_classname,referenced_Field,referenced_Value,column_Header=foreign_keys[field]
            foreign_field='%s.%s:%s'%(referenced_classname,referenced_Value,column_Header)
            foreign_record=Class.query.get(value)
            foreign_description="'%s'"%getattr(foreign_record,referenced_Value)
        set_query_option(   engine=db.engine,Interface=Interface,
                        User_Id=current_user.id,
                        Table_name=class_name,
                        Option_Type=OPTION_FILTER,
                        Argument_1=foreign_field,
                        Argument_2='==',
                        Argument_3=foreign_description
                        )
    page     =  request.args.get('page',    1   ,type=int)
    addx     =  request.args.get('add.x',   None,type=int)
    addy     =  request.args.get('add.y',   None,type=int)
    exportx  =  request.args.get('export.x',None,type=int)
    exporty  =  request.args.get('export.y',None,type=int)
    filterx  =  request.args.get('filter.x',None,type=int)
    filtery  =  request.args.get('filter.y',None,type=int)
    # Select excluyent view mode
    if   addx    is not None: mode = 'add'
    elif exportx is not None: mode = 'export'
    elif filterx is not None: mode = 'filter'
    else:                     mode = 'select'
    id =  request.args.get('id',None,type=str)
    name =  request.args.get('name',None,type=str)
    default =  request.args.get('default',None,type=str)
    permissions =  request.args.get('permissions',None,type=str)
    
    # Build default query all fields from table
    

    if id is not None and len(id)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='id:id',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%id
                )
    
    
    if name is not None and len(name)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='name:name',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%name
                )
    
    
    if default is not None and len(default)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='default:default',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%default
                )
    
    
    if permissions is not None and len(permissions)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='permissions:permissions',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%permissions
                )
    
    
    
    statement_query,options=get_query_options(engine=db.engine,Interface=Interface,Table_name=class_name,User_Id=current_user.id)
    tracebox_log(statement_query,logger,length=80)
    query=eval(statement_query)
    filtered_query = query    
    if mode == 'filter':
        query=filtered_query
    elif mode == 'export':
        query=filtered_query
        fh,output_file = tempfile.mkstemp(suffix='', prefix='%s_'%table_name, dir=None, text=False)
        dict = {'header':{},'detail':[]}
        count = 0
        rows = query.all()
        for row in rows:
            dict['detail'].append({})
            for column in ['id', 'name', 'default', 'permissions']:
                dict['detail'][count].update( { column:str(row.__getattribute__(column))})
                
            count += 1
        dict['header'].update({'count':count})
        jsonarray      = json.dumps(dict)
        data           = json.loads(jsonarray)  
        dataframe      = json_normalize(data, 'detail').assign(**data['header'])
        fh,output_file = tempfile.mkstemp(suffix='', prefix='%_'%table_name, dir='/tmp', text=False)
        xlsx_file      = '%s/%s'%(current_app.root_path,url_for('static',filename='%s.xls'%(output_file)))
        dataframe.to_excel(xlsx_file,sheet_name=table_name,columns=['id', 'name', 'default', 'permissions'])
        return send_file(xlsx_file,as_attachment=True,attachment_filename=output_file.replace('/','_')+'.xls')
    elif mode == 'add':
        return redirect(url_for('.forms_%s'%table_name))
    elif mode == 'select':
        pass
        # if some filter is required
        if field is not None:
            if field == 'id':
                if value is not None:
                    query = query.filter_by(id=value)
            if field == 'name':
                if value is not None:
                    query = query.filter_by(name=value)
            if field == 'default':
                if value is not None:
                    query = query.filter_by(default=value)
            if field == 'permissions':
                if value is not None:
                    query = query.filter_by(permissions=value)
            
    # Actual request from DB follows
    tracebox_log(query,logger,length=80)
    # getting paginated rows for query
    rows = query.paginate(page, per_page=current_app.config['LINES_PER_PAGE'], error_out=False)
    # Setting pagination variables ...
    if field is not None:
       next_url = url_for('.select_%s_query'%template_name, field=field, value=value, page=rows.next_num) if rows.has_next else None
       prev_url = url_for('.select_%s_query'%template_name, field=field, value=value, page=rows.prev_num) if rows.has_prev else None
    else:
       next_url = url_for('.select_%s_query'%template_name, page=rows.next_num) if rows.has_next else None
       prev_url = url_for('.select_%s_query'%template_name, page=rows.prev_num) if rows.has_prev else None
    # Actual rendering ...
    if request.headers.get('Content-Type') is not None or request.args.get('JSON',None,type=str) is not None:
        # NOTE: needs review for JSONnifiyng output when needed (API Interface?)
        if "JSON" in request.headers.get('Content-Type') or request.args.get('JSON',None,type=str) is not None:
            logger.debug('select_%s_query(): will render: JSON rows'%template_name)
            logger.debug('select_%s_query(): Exit'%template_name)
            return json.dumps(serialize_object(rows.__dict__))
    logger.debug('select_%s_query(): will render: %s_All.html'%(template_name,table_name.lower()))
    logger.debug('select_%s_query(): Exit'%template_name)
    return render_template('%s_select_All.html'%template_name.lower(),rows=rows,options=options,collectordata=collectordata)
#===============================================================================
   
# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2022-03-23 18:29:45.468367
# ======================================================================
# gen_views_api.html:AG 2022-03-23 18:29:45.468384
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
        #response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        #response.headers['Pragma']        = 'no-cache'
        try:
            id_counter = 0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values=[id]
            # Codigo para un solo campo de id
            # chequear si marcado explicitamente
            db.session.flush()
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
            db.session.flush()
            db.session.refresh(row)
            db.session.flush()
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
                db.session.flush()
                db.session.refresh(row)
                db.session.flush()
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
                db.session.rollback()
                if request.values is not None and len(request.values):
                    if 'name' in request.values:
                        row.name = request.values.get('name')
                    if 'default' in request.values:
                        row.default = request.values.get('default')
                    if 'permissions' in request.values:
                        row.permissions = request.values.get('permissions')
                # ----------------------------------------------------------
                db.session.merge(row)
                db.session.flush()
                db.session.commit()
                db.session.flush()
                db.session.refresh(row)
                db.session.flush()
                message = f"Modified 'Roles' id = {id}"
                try:
                    row     = json.loads(row.get_json())
                except:
                    row     = None
            else:
                code    = API_NOT_FOUND
                message = f"Not found Roles with id = {id}"
                row     = None
                db.session.rollback()
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
            row     = None
            db.session.rollback()
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
                db.session.flush()
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

# ======================================================================# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2022-03-23 18:29:41
# =============================================================================
# gen_views.py:32 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/views/view_subnets.py
# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2022-03-23 18:29:45.611945
# ======================================================================        
# gen_views_form.html:AG 2022-03-23 18:29:45.611962
@main.route('/forms/Subnets', methods=['GET', 'POST'])
@login_required

def forms_Subnets():
    """ Form handling function for table Subnets """
    logger.debug('forms_Subnets(): Enter')
    
    # Shardening Code goes her if needed
    collectordata={}
    collectordata.update({"COLLECTOR_PERIOD":get_period_data(current_user.id,db.engine,Interface)})
    collectordata.update({"CONFIG":current_app.config})
    suffix = collectordata['COLLECTOR_PERIOD']['active']
    table_name='Subnets'
    class_name='subnets'
    template_name='Subnets'
    sharding=False
    uuid  =  request.args.get('uuid',0,type=int)
    
    # Ensures DB Data is commited prior main query
    try:
        db.session.commit()
    except:
        db.session.rollback()
    row =  subnets.query.filter(subnets.uuid == uuid).first()
    if row is None:
        row=subnets()
        session['is_new_row']=True
    session['data'] =  {  'uuid':row.uuid, 'name':row.name, 'vlan_id':row.vlan_id, 'vswitch_name':row.vswitch_name, 'type':row.type, 'default_gateway_ip':row.default_gateway_ip, 'range':row.range, 'prefix_length':row.prefix_length, 'subnet_ip':row.subnet_ip, 'cluster':row.cluster }
    
    form = frm_subnets()
    
    # Actual Form activation here
    if form.validate_on_submit():
        # Code for SAVE option -----------------------------------------
        if form.submit_Save.data and current_user.role_id > 1:
            row.uuid = form.uuid.data
            row.name = form.name.data
            row.vlan_id = form.vlan_id.data
            row.vswitch_name = form.vswitch_name.data
            row.type = form.type.data
            row.default_gateway_ip = form.default_gateway_ip.data
            row.range = form.range.data
            row.prefix_length = form.prefix_length.data
            row.subnet_ip = form.subnet_ip.data
            row.cluster = form.cluster.data
            try:
               session['new_row']=str(row)
               db.session.flush()
               db.session.add(row)
               db.session.commit()
               db.session.flush()
               if session['is_new_row']==True:
                   logger.audit ( '%s:NEW:%s' % (current_user.username,session['new_row'] ) )
                   flash('New Subnets created OK')
               else:
                   logger.audit ( '%s:OLD:%s' % (current_user.username,session['prev_row']) )
                   logger.audit ( '%s:UPD:%s' % (current_user.username,session['new_row'] ) )    
                   message=Markup('<b>Subnets uuid saved OK</b>')
                   flash(message)
               db.session.flush()
            except Exception as e:
               db.session.rollback()
               db.session.flush()
               message=Markup('ERROR saving Subnets record : %s'%(e))
               flash(message)
            return redirect(url_for('.select_Subnets_query'))
        # --------------------------------------------------------------
        # Code for NEW option
        # GV 20190109 f.write(        "        elif   form.submit_New.data:\n")
        elif   form.submit_New.data and current_user.role_id>1:
            #print('New Data Here ...')
            session['is_new_row']=True
            db.session.flush()
            row=subnets()
    
            return redirect(url_for('.forms_Subnets'))    
    
        # Code for CANCEL option 
        elif   form.submit_Cancel.data:
            #print('Cancel Data Here ... does nothing')
            message=Markup('Subnets Record modifications discarded ...')
            flash(message)
        # Code for ANY OTHER option should never get here
        else:
            #print('form validated but not submited ???')
            message=Markup("<b>Subnets data modifications not allowed for user '%s'. Please contact EG Suite's Administrator ...</b>"%(current_user.username))    
            flash(message)
    
            return redirect(url_for('.forms_'))    
    
    
    form.uuid.data = row.uuid
    form.name.data = row.name
    form.vlan_id.data = row.vlan_id
    form.vswitch_name.data = row.vswitch_name
    form.type.data = row.type
    form.default_gateway_ip.data = row.default_gateway_ip
    form.range.data = row.range
    form.prefix_length.data = row.prefix_length
    form.subnet_ip.data = row.subnet_ip
    form.cluster.data = row.cluster
    session['prev_row'] = str(row)
    session['is_new_row'] = False
    logger.debug('forms_Subnets(): Exit')
    # Generates pagination data here
    P=[]
    # Tab Relations = [{'name': 'nutanix_prism_vm', 'class': 'nutanix_prism_vm', 'backref': 'subnets', 'caption': 'NUTANIX_PRISM_VM', 'table': 'Nutanix_Prism_VM'}]
    
    from flask_sqlalchemy import Pagination
    # [{'name': 'nutanix_prism_vm', 'class': 'nutanix_prism_vm', 'backref': 'subnets', 'caption': 'NUTANIX_PRISM_VM', 'table': 'Nutanix_Prism_VM'}]
    try:
        if hasattr(row, 'nutanix_prism_vm'):
            P.append(({'name': 'nutanix_prism_vm', 'class': 'nutanix_prism_vm', 'backref': 'subnets', 'caption': 'NUTANIX_PRISM_VM', 'table': 'Nutanix_Prism_VM'},row.nutanix_prism_vm.paginate()))
    except Exception as e:
        print(f'Exception: {str(e)}')
    
    
    # Generation of pagination data completed
    collectordata={}
    collectordata.update({"COLLECTOR_PERIOD":get_period_data(current_user.id,db.engine,Interface)})
    return render_template('subnets.html', form=form, row=row, P=P,collectordata=collectordata)    
# ======================================================================



# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2022-03-23 18:29:45.627036
# ======================================================================        
# gen_views_delete.html:AG 2022-03-23 18:29:45.627053
@main.route('/forms/Subnets_delete', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DELETE)
@admin_required
def forms_Subnets_delete():
    """ Delete record handling function for table Subnets """
    logger.debug('forms_Subnets_delete(): Enter')
    uuid  =  request.args.get('uuid',0,type=int)
    row =  subnets.query.filter(subnets.uuid == uuid).first()

    if row is None:
        row=subnets()
    session['data'] =  {  'uuid':row.uuid, 'name':row.name, 'vlan_id':row.vlan_id, 'vswitch_name':row.vswitch_name, 'type':row.type, 'default_gateway_ip':row.default_gateway_ip, 'range':row.range, 'prefix_length':row.prefix_length, 'subnet_ip':row.subnet_ip, 'cluster':row.cluster }
                       
    form = frm_subnets_delete()

    # Tab['has_fks'] False
    
            
    # Actual Form activation here
    if form.validate_on_submit():
    
    # Code for SAVE option
        if  form.submit_Delete.data:
            print('Delete Data Here...')

    
    #f.write(        "            print('Delete Data Here...')
            try:
                session['deleted_row']=str(row)
                db.session.flush()
                db.session.delete(row)
                db.session.commit()
                db.session.flush()
                logger.audit ( '%s:DEL:%s' % (current_user.username,session['deleted_row']) )
                flash('Subnets uuid deleted OK')
            except exc.IntegrityError as e:
                db.session.rollback()    
                flash('INTEGRITY ERROR: Are you sure there are no dependant records in other tables?')
                return redirect(url_for('.forms_Subnets_delete',uuid=session['data']['uuid']))    
    
            return redirect(url_for('.select_Subnets_query'))    
    # Code for CANCEL option 
        elif   form.submit_Cancel.data:
            print('Cancel Data Here ... does nothing')
            flash('Record modifications discarded ...')
            return redirect(url_for('.select_Subnets_query'))    
    # Code for ANY OTHER option should never get here
        else:
            print('form validated but not submited ???')
            return redirect(url_for('.select_Subnets_query'))    
    
    logger.debug('forms_Subnets_delete(): Exit')
    collectordata={}
    collectordata.update({"COLLECTOR_PERIOD":get_period_data(current_user.id,db.engine,Interface)})
    return render_template('subnets_delete.html', form=form, data=session.get('data'),row=row,collectordata=collectordata)
#===============================================================================

# table_name: Subnets
# class_name: subnets
# is shardened: False
# current_app: 
# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2022-03-23 18:29:45.653539
# ======================================================================

# gen_views_select_query.html:AG 2022-03-23 18:29:45.653567        
@main.route('/select/Subnets_Query', methods=['GET','POST'])
@login_required
@admin_required
def select_Subnets_query():
    """ Select rows handling function for table 'Subnets' """
    logger.debug('select_Subnets_query(): Enter')
    #chk_c000001(filename=os.path.join(current_app.root_path, '.c000001'),request=request,db=db,logger=logger)
    # Shardening Code goes her if needed
    collectordata={}
    collectordata.update({"COLLECTOR_PERIOD":get_period_data(current_user.id,db.engine,Interface)})
    collectordata.update({"CONFIG":current_app.config})
    suffix = collectordata['COLLECTOR_PERIOD']['active']
    table_name='Subnets'
    class_name='subnets'
    template_name='Subnets'
    sharding=False


    logger.debug("-----------------------------------------------------------")
    logger.debug("%s: template_name            = %s",__name__,template_name)

    logger.debug("-----------------------------------------------------------")    
        
    # Get parameters from URL call
    ia       =  request.args.get('ia',     None,type=str)
    if ia is not None:
        ia=ia.split(',')
        if ia[0]=='ORDER':
            #set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name='subnets',Option_Type=OPTION_ORDER_BY,Argument_1=ia[1],Argument_2=ia[2])
            set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name=class_name,Option_Type=OPTION_ORDER_BY,Argument_1=ia[1],Argument_2=ia[2])
        elif ia[0]=='GROUP':
            #set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name='subnets',Option_Type=OPTION_GROUP_BY,Argument_1=ia[1])
            set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name=class_name,Option_Type=OPTION_GROUP_BY,Argument_1=ia[1])
        elif ia[0]=='LIMIT':
            #set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name='subnets',Option_Type=OPTION_LIMIT,Argument_1=ia[1])
            set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name=class_name,Option_Type=OPTION_LIMIT,Argument_1=ia[1])

    iad      =  request.args.get('iad',     None,type=int)
    if iad is not None: delete_query_option(engine=db.engine,Interface=Interface,Id=iad) 
    
    field    =  request.args.get('field',   None,type=str)
    value    =  request.args.get('value',   None,type=str)
    
    # Populates a list of foreign keys used for advanced filtering
    # ------------------------------------------------------------------
    foreign_keys={}
    
    # ------------------------------------------------------------------
    
    if field is not None:
        reset_query_options(    engine=db.engine,Interface=Interface,
                                User_Id=current_user.id,
                                #Table_name='subnets'
                                Table_name=class_name
                                )

        
        if field in foreign_keys.keys():
            Class,referenced_classname,referenced_Field,referenced_Value,column_Header=foreign_keys[field]
            foreign_field='%s.%s:%s'%(referenced_classname,referenced_Value,column_Header)
            foreign_record=Class.query.get(value)
            foreign_description="'%s'"%getattr(foreign_record,referenced_Value)
        set_query_option(   engine=db.engine,Interface=Interface,
                        User_Id=current_user.id,
                        Table_name=class_name,
                        Option_Type=OPTION_FILTER,
                        Argument_1=foreign_field,
                        Argument_2='==',
                        Argument_3=foreign_description
                        )
    page     =  request.args.get('page',    1   ,type=int)
    addx     =  request.args.get('add.x',   None,type=int)
    addy     =  request.args.get('add.y',   None,type=int)
    exportx  =  request.args.get('export.x',None,type=int)
    exporty  =  request.args.get('export.y',None,type=int)
    filterx  =  request.args.get('filter.x',None,type=int)
    filtery  =  request.args.get('filter.y',None,type=int)
    # Select excluyent view mode
    if   addx    is not None: mode = 'add'
    elif exportx is not None: mode = 'export'
    elif filterx is not None: mode = 'filter'
    else:                     mode = 'select'
    uuid =  request.args.get('uuid',None,type=str)
    name =  request.args.get('name',None,type=str)
    vlan_id =  request.args.get('vlan_id',None,type=str)
    vswitch_name =  request.args.get('vswitch_name',None,type=str)
    type =  request.args.get('type',None,type=str)
    default_gateway_ip =  request.args.get('default_gateway_ip',None,type=str)
    range =  request.args.get('range',None,type=str)
    prefix_length =  request.args.get('prefix_length',None,type=str)
    subnet_ip =  request.args.get('subnet_ip',None,type=str)
    cluster =  request.args.get('cluster',None,type=str)
    
    # Build default query all fields from table
    

    if uuid is not None and len(uuid)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='uuid:uuid',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%uuid
                )
    
    
    if name is not None and len(name)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='name:name',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%name
                )
    
    
    if vlan_id is not None and len(vlan_id)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='vlan_id:vlan_id',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%vlan_id
                )
    
    
    if vswitch_name is not None and len(vswitch_name)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='vswitch_name:vswitch_name',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%vswitch_name
                )
    
    
    if type is not None and len(type)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='type:type',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%type
                )
    
    
    if default_gateway_ip is not None and len(default_gateway_ip)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='default_gateway_ip:default_gateway_ip',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%default_gateway_ip
                )
    
    
    if range is not None and len(range)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='range:range',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%range
                )
    
    
    if prefix_length is not None and len(prefix_length)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='prefix_length:prefix_length',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%prefix_length
                )
    
    
    if subnet_ip is not None and len(subnet_ip)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='subnet_ip:subnet_ip',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%subnet_ip
                )
    
    
    if cluster is not None and len(cluster)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='cluster:cluster',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%cluster
                )
    
    
    
    statement_query,options=get_query_options(engine=db.engine,Interface=Interface,Table_name=class_name,User_Id=current_user.id)
    tracebox_log(statement_query,logger,length=80)
    query=eval(statement_query)
    filtered_query = query    
    if mode == 'filter':
        query=filtered_query
    elif mode == 'export':
        query=filtered_query
        fh,output_file = tempfile.mkstemp(suffix='', prefix='%s_'%table_name, dir=None, text=False)
        dict = {'header':{},'detail':[]}
        count = 0
        rows = query.all()
        for row in rows:
            dict['detail'].append({})
            for column in ['uuid', 'name', 'vlan_id', 'vswitch_name', 'type', 'default_gateway_ip', 'range', 'prefix_length', 'subnet_ip', 'cluster']:
                dict['detail'][count].update( { column:str(row.__getattribute__(column))})
                
            count += 1
        dict['header'].update({'count':count})
        jsonarray      = json.dumps(dict)
        data           = json.loads(jsonarray)  
        dataframe      = json_normalize(data, 'detail').assign(**data['header'])
        fh,output_file = tempfile.mkstemp(suffix='', prefix='%_'%table_name, dir='/tmp', text=False)
        xlsx_file      = '%s/%s'%(current_app.root_path,url_for('static',filename='%s.xls'%(output_file)))
        dataframe.to_excel(xlsx_file,sheet_name=table_name,columns=['uuid', 'name', 'vlan_id', 'vswitch_name', 'type', 'default_gateway_ip', 'range', 'prefix_length', 'subnet_ip', 'cluster'])
        return send_file(xlsx_file,as_attachment=True,attachment_filename=output_file.replace('/','_')+'.xls')
    elif mode == 'add':
        return redirect(url_for('.forms_%s'%table_name))
    elif mode == 'select':
        pass
        # if some filter is required
        if field is not None:
            if field == 'uuid':
                if value is not None:
                    query = query.filter_by(uuid=value)
            if field == 'name':
                if value is not None:
                    query = query.filter_by(name=value)
            if field == 'vlan_id':
                if value is not None:
                    query = query.filter_by(vlan_id=value)
            if field == 'vswitch_name':
                if value is not None:
                    query = query.filter_by(vswitch_name=value)
            if field == 'type':
                if value is not None:
                    query = query.filter_by(type=value)
            if field == 'default_gateway_ip':
                if value is not None:
                    query = query.filter_by(default_gateway_ip=value)
            if field == 'range':
                if value is not None:
                    query = query.filter_by(range=value)
            if field == 'prefix_length':
                if value is not None:
                    query = query.filter_by(prefix_length=value)
            if field == 'subnet_ip':
                if value is not None:
                    query = query.filter_by(subnet_ip=value)
            if field == 'cluster':
                if value is not None:
                    query = query.filter_by(cluster=value)
            
    # Actual request from DB follows
    tracebox_log(query,logger,length=80)
    # getting paginated rows for query
    rows = query.paginate(page, per_page=current_app.config['LINES_PER_PAGE'], error_out=False)
    # Setting pagination variables ...
    if field is not None:
       next_url = url_for('.select_%s_query'%template_name, field=field, value=value, page=rows.next_num) if rows.has_next else None
       prev_url = url_for('.select_%s_query'%template_name, field=field, value=value, page=rows.prev_num) if rows.has_prev else None
    else:
       next_url = url_for('.select_%s_query'%template_name, page=rows.next_num) if rows.has_next else None
       prev_url = url_for('.select_%s_query'%template_name, page=rows.prev_num) if rows.has_prev else None
    # Actual rendering ...
    if request.headers.get('Content-Type') is not None or request.args.get('JSON',None,type=str) is not None:
        # NOTE: needs review for JSONnifiyng output when needed (API Interface?)
        if "JSON" in request.headers.get('Content-Type') or request.args.get('JSON',None,type=str) is not None:
            logger.debug('select_%s_query(): will render: JSON rows'%template_name)
            logger.debug('select_%s_query(): Exit'%template_name)
            return json.dumps(serialize_object(rows.__dict__))
    logger.debug('select_%s_query(): will render: %s_All.html'%(template_name,table_name.lower()))
    logger.debug('select_%s_query(): Exit'%template_name)
    return render_template('%s_select_All.html'%template_name.lower(),rows=rows,options=options,collectordata=collectordata)
#===============================================================================
   
# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2022-03-23 18:29:45.692278
# ======================================================================
# gen_views_api.html:AG 2022-03-23 18:29:45.692296
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
        #response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        #response.headers['Pragma']        = 'no-cache'
        try:
            id_counter = 0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values=[id]
            # Codigo para un solo campo de id
            # chequear si marcado explicitamente
            db.session.flush()
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
            db.session.flush()
            db.session.refresh(row)
            db.session.flush()
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
                db.session.flush()
                db.session.refresh(row)
                db.session.flush()
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
                db.session.rollback()
                if request.values is not None and len(request.values):
                    if 'name' in request.values:
                        row.name = request.values.get('name')
                    if 'vlan_id' in request.values:
                        row.vlan_id = request.values.get('vlan_id')
                    if 'vswitch_name' in request.values:
                        row.vswitch_name = request.values.get('vswitch_name')
                    if 'type' in request.values:
                        row.type = request.values.get('type')
                    if 'default_gateway_ip' in request.values:
                        row.default_gateway_ip = request.values.get('default_gateway_ip')
                    if 'range' in request.values:
                        row.range = request.values.get('range')
                    if 'prefix_length' in request.values:
                        row.prefix_length = request.values.get('prefix_length')
                    if 'subnet_ip' in request.values:
                        row.subnet_ip = request.values.get('subnet_ip')
                    if 'cluster' in request.values:
                        row.cluster = request.values.get('cluster')
                # ----------------------------------------------------------
                db.session.merge(row)
                db.session.flush()
                db.session.commit()
                db.session.flush()
                db.session.refresh(row)
                db.session.flush()
                message = f"Modified 'Subnets' uuid = {id}"
                try:
                    row     = json.loads(row.get_json())
                except:
                    row     = None
            else:
                code    = API_NOT_FOUND
                message = f"Not found Subnets with uuid = {id}"
                row     = None
                db.session.rollback()
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
            row     = None
            db.session.rollback()
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
                db.session.flush()
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

# ======================================================================# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2022-03-23 18:29:41
# =============================================================================
# gen_views.py:32 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/views/view_users.py
# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2022-03-23 18:29:45.850496
# ======================================================================        
# gen_views_form.html:AG 2022-03-23 18:29:45.850514
@main.route('/forms/Users', methods=['GET', 'POST'])
@login_required

def forms_Users():
    """ Form handling function for table Users """
    logger.debug('forms_Users(): Enter')
    
    # Shardening Code goes her if needed
    collectordata={}
    collectordata.update({"COLLECTOR_PERIOD":get_period_data(current_user.id,db.engine,Interface)})
    collectordata.update({"CONFIG":current_app.config})
    suffix = collectordata['COLLECTOR_PERIOD']['active']
    table_name='Users'
    class_name='User'
    template_name='Users'
    sharding=False
    id  =  request.args.get('id',0,type=int)
    
    # Ensures DB Data is commited prior main query
    try:
        db.session.commit()
    except:
        db.session.rollback()
    row =  User.query.filter(User.id == id).first()
    if row is None:
        row=User()
        session['is_new_row']=True
    session['data'] =  {  'id':row.id, 'username':row.username, 'name':row.name, 'role_id':row.role_id, 'email':row.email, 'password_hash':row.password_hash, 'confirmed':row.confirmed, 'CC_Id':row.CC_Id, 'roles':row.roles, 'ldap':row.ldap, 'ldap_user':row.ldap_user, 'ldap_common':row.ldap_common, 'ldap_host':row.ldap_host, 'ldap_port':row.ldap_port, 'ldap_domain':row.ldap_domain, 'vars':row.vars }
    
    form = frm_User()
    
    if form.has_FKs:
        form.role_id.choices = db.session.query(Role.id,Role.name).order_by(Role.name).all()

    
    # Actual Form activation here
    if form.validate_on_submit():
        # Code for SAVE option -----------------------------------------
        if form.submit_Save.data and current_user.role_id > 1:
            
            row.username = form.username.data
            row.name = form.name.data
            row.role_id = form.role_id.data
            row.email = form.email.data
            row.password_hash = form.password_hash.data
            row.confirmed = form.confirmed.data
            row.CC_Id = form.CC_Id.data
            row.roles = form.roles.data
            row.ldap = form.ldap.data
            row.ldap_user = form.ldap_user.data
            row.ldap_common = form.ldap_common.data
            row.ldap_host = form.ldap_host.data
            row.ldap_port = form.ldap_port.data
            row.ldap_domain = form.ldap_domain.data
            row.vars = form.vars.data
            try:
               session['new_row']=str(row)
               db.session.flush()
               db.session.add(row)
               db.session.commit()
               db.session.flush()
               if session['is_new_row']==True:
                   logger.audit ( '%s:NEW:%s' % (current_user.username,session['new_row'] ) )
                   flash('New User created OK')
               else:
                   logger.audit ( '%s:OLD:%s' % (current_user.username,session['prev_row']) )
                   logger.audit ( '%s:UPD:%s' % (current_user.username,session['new_row'] ) )    
                   message=Markup('<b>User id saved OK</b>')
                   flash(message)
               db.session.flush()
            except Exception as e:
               db.session.rollback()
               db.session.flush()
               message=Markup('ERROR saving User record : %s'%(e))
               flash(message)
            return redirect(url_for('.select_Users_query'))
        # --------------------------------------------------------------
        # Code for NEW option
        # GV 20190109 f.write(        "        elif   form.submit_New.data:\n")
        elif   form.submit_New.data and current_user.role_id>1:
            #print('New Data Here ...')
            session['is_new_row']=True
            db.session.flush()
            row=User()
    
            return redirect(url_for('.forms_Users',id=row.id))
    
        # Code for CANCEL option 
        elif   form.submit_Cancel.data:
            #print('Cancel Data Here ... does nothing')
            message=Markup('User Record modifications discarded ...')
            flash(message)
        # Code for ANY OTHER option should never get here
        else:
            #print('form validated but not submited ???')
            message=Markup("<b>User data modifications not allowed for user '%s'. Please contact EG Suite's Administrator ...</b>"%(current_user.username))    
            flash(message)
    
            return redirect(url_for('.forms_Users',id=row.id))
    
    
    form.username.data = row.username
    form.name.data = row.name
    form.role_id.data = row.role_id
    form.email.data = row.email
    form.password_hash.data = row.password_hash
    form.confirmed.data = row.confirmed
    form.CC_Id.data = row.CC_Id
    form.roles.data = row.roles
    form.ldap.data = row.ldap
    form.ldap_user.data = row.ldap_user
    form.ldap_common.data = row.ldap_common
    form.ldap_host.data = row.ldap_host
    form.ldap_port.data = row.ldap_port
    form.ldap_domain.data = row.ldap_domain
    form.vars.data = row.vars
    session['prev_row'] = str(row)
    session['is_new_row'] = False
    logger.debug('forms_Users(): Exit')
    # Generates pagination data here
    P=[]
    # Tab Relations = []
    
    # Generation of pagination data completed
    collectordata={}
    collectordata.update({"COLLECTOR_PERIOD":get_period_data(current_user.id,db.engine,Interface)})
    return render_template('users.html', form=form, row=row, P=P,collectordata=collectordata)    
# ======================================================================



# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2022-03-23 18:29:45.861657
# ======================================================================        
# gen_views_delete.html:AG 2022-03-23 18:29:45.861673
@main.route('/forms/Users_delete', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.DELETE)
@admin_required
def forms_Users_delete():
    """ Delete record handling function for table Users """
    logger.debug('forms_Users_delete(): Enter')
    id  =  request.args.get('id',0,type=int)
    row =  User.query.filter(User.id == id).first()

    if row is None:
        row=User()
    session['data'] =  {  'id':row.id, 'username':row.username, 'name':row.name, 'role_id':row.role_id, 'email':row.email, 'password_hash':row.password_hash, 'confirmed':row.confirmed, 'CC_Id':row.CC_Id, 'roles':row.roles, 'ldap':row.ldap, 'ldap_user':row.ldap_user, 'ldap_common':row.ldap_common, 'ldap_host':row.ldap_host, 'ldap_port':row.ldap_port, 'ldap_domain':row.ldap_domain, 'vars':row.vars }
                       
    form = frm_User_delete()

    # Tab['has_fks'] True
    
    pass # Tab['has_fks'] True
    
            
    # Actual Form activation here
    if form.validate_on_submit():
    
    # Code for SAVE option
        if  form.submit_Delete.data:
            print('Delete Data Here...')

    
    #f.write(        "            print('Delete Data Here...')
            try:
                session['deleted_row']=str(row)
                db.session.flush()
                db.session.delete(row)
                db.session.commit()
                db.session.flush()
                logger.audit ( '%s:DEL:%s' % (current_user.username,session['deleted_row']) )
                flash('User id deleted OK')
            except exc.IntegrityError as e:
                db.session.rollback()    
                flash('INTEGRITY ERROR: Are you sure there are no dependant records in other tables?')
                return redirect(url_for('.forms_Users_delete',id=session['data']['id']))    
    
            return redirect(url_for('.select_Users_query'))    
    # Code for CANCEL option 
        elif   form.submit_Cancel.data:
            print('Cancel Data Here ... does nothing')
            flash('Record modifications discarded ...')
            return redirect(url_for('.select_Users_query'))    
    # Code for ANY OTHER option should never get here
        else:
            print('form validated but not submited ???')
            return redirect(url_for('.select_Users_query'))    
    
    logger.debug('forms_Users_delete(): Exit')
    collectordata={}
    collectordata.update({"COLLECTOR_PERIOD":get_period_data(current_user.id,db.engine,Interface)})
    return render_template('users_delete.html', form=form, data=session.get('data'),row=row,collectordata=collectordata)
#===============================================================================

# table_name: Users
# class_name: User
# is shardened: False
# current_app: 
# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2022-03-23 18:29:45.883235
# ======================================================================

# gen_views_select_query.html:AG 2022-03-23 18:29:45.883252        
@main.route('/select/Users_Query', methods=['GET','POST'])
@login_required
@admin_required
def select_Users_query():
    """ Select rows handling function for table 'Users' """
    logger.debug('select_Users_query(): Enter')
    #chk_c000001(filename=os.path.join(current_app.root_path, '.c000001'),request=request,db=db,logger=logger)
    # Shardening Code goes her if needed
    collectordata={}
    collectordata.update({"COLLECTOR_PERIOD":get_period_data(current_user.id,db.engine,Interface)})
    collectordata.update({"CONFIG":current_app.config})
    suffix = collectordata['COLLECTOR_PERIOD']['active']
    table_name='Users'
    class_name='User'
    template_name='Users'
    sharding=False


    logger.debug("-----------------------------------------------------------")
    logger.debug("%s: template_name            = %s",__name__,template_name)

    logger.debug("-----------------------------------------------------------")    
        
    # Get parameters from URL call
    ia       =  request.args.get('ia',     None,type=str)
    if ia is not None:
        ia=ia.split(',')
        if ia[0]=='ORDER':
            #set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name='User',Option_Type=OPTION_ORDER_BY,Argument_1=ia[1],Argument_2=ia[2])
            set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name=class_name,Option_Type=OPTION_ORDER_BY,Argument_1=ia[1],Argument_2=ia[2])
        elif ia[0]=='GROUP':
            #set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name='User',Option_Type=OPTION_GROUP_BY,Argument_1=ia[1])
            set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name=class_name,Option_Type=OPTION_GROUP_BY,Argument_1=ia[1])
        elif ia[0]=='LIMIT':
            #set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name='User',Option_Type=OPTION_LIMIT,Argument_1=ia[1])
            set_query_option(engine=db.engine,Interface=Interface,User_Id=current_user.id,Table_name=class_name,Option_Type=OPTION_LIMIT,Argument_1=ia[1])

    iad      =  request.args.get('iad',     None,type=int)
    if iad is not None: delete_query_option(engine=db.engine,Interface=Interface,Id=iad) 
    
    field    =  request.args.get('field',   None,type=str)
    value    =  request.args.get('value',   None,type=str)
    
    # Populates a list of foreign keys used for advanced filtering
    # ------------------------------------------------------------------
    foreign_keys={}
    
    foreign_keys.update({'role_id':(Role,'Role','id','name','role_id')})
    # ------------------------------------------------------------------
    
    if field is not None:
        reset_query_options(    engine=db.engine,Interface=Interface,
                                User_Id=current_user.id,
                                #Table_name='User'
                                Table_name=class_name
                                )

        
        if field in foreign_keys.keys():
            Class,referenced_classname,referenced_Field,referenced_Value,column_Header=foreign_keys[field]
            foreign_field='%s.%s:%s'%(referenced_classname,referenced_Value,column_Header)
            foreign_record=Class.query.get(value)
            foreign_description="'%s'"%getattr(foreign_record,referenced_Value)
        set_query_option(   engine=db.engine,Interface=Interface,
                        User_Id=current_user.id,
                        Table_name=class_name,
                        Option_Type=OPTION_FILTER,
                        Argument_1=foreign_field,
                        Argument_2='==',
                        Argument_3=foreign_description
                        )
    page     =  request.args.get('page',    1   ,type=int)
    addx     =  request.args.get('add.x',   None,type=int)
    addy     =  request.args.get('add.y',   None,type=int)
    exportx  =  request.args.get('export.x',None,type=int)
    exporty  =  request.args.get('export.y',None,type=int)
    filterx  =  request.args.get('filter.x',None,type=int)
    filtery  =  request.args.get('filter.y',None,type=int)
    # Select excluyent view mode
    if   addx    is not None: mode = 'add'
    elif exportx is not None: mode = 'export'
    elif filterx is not None: mode = 'filter'
    else:                     mode = 'select'
    id =  request.args.get('id',None,type=str)
    username =  request.args.get('username',None,type=str)
    name =  request.args.get('name',None,type=str)
    role_id =  request.args.get('role_id',None,type=str)
    email =  request.args.get('email',None,type=str)
    password_hash =  request.args.get('password_hash',None,type=str)
    confirmed =  request.args.get('confirmed',None,type=str)
    CC_Id =  request.args.get('CC_Id',None,type=str)
    roles =  request.args.get('roles',None,type=str)
    ldap =  request.args.get('ldap',None,type=str)
    ldap_user =  request.args.get('ldap_user',None,type=str)
    ldap_common =  request.args.get('ldap_common',None,type=str)
    ldap_host =  request.args.get('ldap_host',None,type=str)
    ldap_port =  request.args.get('ldap_port',None,type=str)
    ldap_domain =  request.args.get('ldap_domain',None,type=str)
    vars =  request.args.get('vars',None,type=str)
    
    # Build default query all fields from table
    

    if id is not None and len(id)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='id:id',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%id
                )
    
    
    if username is not None and len(username)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='username:username',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%username
                )
    
    
    if name is not None and len(name)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='name:name',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%name
                )
    
    
    if role_id is not None and len(role_id)>0:
            Class,referenced_classname,referenced_Field,referenced_Value,column_Header=foreign_keys['role_id']
            foreign_field='%s.%s:%s'%(referenced_classname,referenced_Value,column_Header)            
            set_query_option(   engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1=foreign_field,
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%role_id
                )
                                
    
    
    if email is not None and len(email)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='email:email',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%email
                )
    
    
    if password_hash is not None and len(password_hash)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='password_hash:password_hash',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%password_hash
                )
    
    
    if confirmed is not None and len(confirmed)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='confirmed:confirmed',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%confirmed
                )
    
    
    if CC_Id is not None and len(CC_Id)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='CC_Id:CC_Id',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%CC_Id
                )
    
    
    if roles is not None and len(roles)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='roles:roles',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%roles
                )
    
    
    if ldap is not None and len(ldap)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='ldap:ldap',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%ldap
                )
    
    
    if ldap_user is not None and len(ldap_user)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='ldap_user:ldap_user',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%ldap_user
                )
    
    
    if ldap_common is not None and len(ldap_common)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='ldap_common:ldap_common',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%ldap_common
                )
    
    
    if ldap_host is not None and len(ldap_host)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='ldap_host:ldap_host',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%ldap_host
                )
    
    
    if ldap_port is not None and len(ldap_port)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='ldap_port:ldap_port',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%ldap_port
                )
    
    
    if ldap_domain is not None and len(ldap_domain)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='ldap_domain:ldap_domain',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%ldap_domain
                )
    
    
    if vars is not None and len(vars)>0:
            set_query_option(engine=db.engine,Interface=Interface,
                User_Id=current_user.id,
                Table_name=class_name,
                Option_Type=OPTION_FILTER,
                Argument_1='vars:vars',
                Argument_2='LIKE',
                Argument_3='\"%%%s%%\"'%vars
                )
    
    
    
    statement_query,options=get_query_options(engine=db.engine,Interface=Interface,Table_name=class_name,User_Id=current_user.id)
    tracebox_log(statement_query,logger,length=80)
    query=eval(statement_query)
    filtered_query = query    
    if mode == 'filter':
        query=filtered_query
    elif mode == 'export':
        query=filtered_query
        fh,output_file = tempfile.mkstemp(suffix='', prefix='%s_'%table_name, dir=None, text=False)
        dict = {'header':{},'detail':[]}
        count = 0
        rows = query.all()
        for row in rows:
            dict['detail'].append({})
            for column in ['id', 'username', 'name', 'role_id', 'email', 'password_hash', 'confirmed', 'CC_Id', 'roles', 'ldap', 'ldap_user', 'ldap_common', 'ldap_host', 'ldap_port', 'ldap_domain', 'vars']:
                dict['detail'][count].update( { column:str(row.__getattribute__(column))})
                
            count += 1
        dict['header'].update({'count':count})
        jsonarray      = json.dumps(dict)
        data           = json.loads(jsonarray)  
        dataframe      = json_normalize(data, 'detail').assign(**data['header'])
        fh,output_file = tempfile.mkstemp(suffix='', prefix='%_'%table_name, dir='/tmp', text=False)
        xlsx_file      = '%s/%s'%(current_app.root_path,url_for('static',filename='%s.xls'%(output_file)))
        dataframe.to_excel(xlsx_file,sheet_name=table_name,columns=['id', 'username', 'name', 'role_id', 'email', 'password_hash', 'confirmed', 'CC_Id', 'roles', 'ldap', 'ldap_user', 'ldap_common', 'ldap_host', 'ldap_port', 'ldap_domain', 'vars'])
        return send_file(xlsx_file,as_attachment=True,attachment_filename=output_file.replace('/','_')+'.xls')
    elif mode == 'add':
        return redirect(url_for('.forms_%s'%table_name))
    elif mode == 'select':
        pass
        # if some filter is required
        if field is not None:
            if field == 'id':
                if value is not None:
                    query = query.filter_by(id=value)
            if field == 'username':
                if value is not None:
                    query = query.filter_by(username=value)
            if field == 'name':
                if value is not None:
                    query = query.filter_by(name=value)
            if field == 'role_id':
                if value is not None:
                    query = query.filter_by(role_id=value)
            if field == 'email':
                if value is not None:
                    query = query.filter_by(email=value)
            if field == 'password_hash':
                if value is not None:
                    query = query.filter_by(password_hash=value)
            if field == 'confirmed':
                if value is not None:
                    query = query.filter_by(confirmed=value)
            if field == 'CC_Id':
                if value is not None:
                    query = query.filter_by(CC_Id=value)
            if field == 'roles':
                if value is not None:
                    query = query.filter_by(roles=value)
            if field == 'ldap':
                if value is not None:
                    query = query.filter_by(ldap=value)
            if field == 'ldap_user':
                if value is not None:
                    query = query.filter_by(ldap_user=value)
            if field == 'ldap_common':
                if value is not None:
                    query = query.filter_by(ldap_common=value)
            if field == 'ldap_host':
                if value is not None:
                    query = query.filter_by(ldap_host=value)
            if field == 'ldap_port':
                if value is not None:
                    query = query.filter_by(ldap_port=value)
            if field == 'ldap_domain':
                if value is not None:
                    query = query.filter_by(ldap_domain=value)
            if field == 'vars':
                if value is not None:
                    query = query.filter_by(vars=value)
            # ------------------------------------------------------------------
    # JOIN other tables and generate foreign fields
    # Will replace class name by sharding class in joins structure
    # will have no effect in no sharding environment
    query = query.join(Role,User.role_id == Role.id).add_columns(Role.name)
    # ------------------------------------------------------------------
    
    # Actual request from DB follows
    tracebox_log(query,logger,length=80)
    # getting paginated rows for query
    rows = query.paginate(page, per_page=current_app.config['LINES_PER_PAGE'], error_out=False)
    # Setting pagination variables ...
    if field is not None:
       next_url = url_for('.select_%s_query'%template_name, field=field, value=value, page=rows.next_num) if rows.has_next else None
       prev_url = url_for('.select_%s_query'%template_name, field=field, value=value, page=rows.prev_num) if rows.has_prev else None
    else:
       next_url = url_for('.select_%s_query'%template_name, page=rows.next_num) if rows.has_next else None
       prev_url = url_for('.select_%s_query'%template_name, page=rows.prev_num) if rows.has_prev else None
    # Actual rendering ...
    if request.headers.get('Content-Type') is not None or request.args.get('JSON',None,type=str) is not None:
        # NOTE: needs review for JSONnifiyng output when needed (API Interface?)
        if "JSON" in request.headers.get('Content-Type') or request.args.get('JSON',None,type=str) is not None:
            logger.debug('select_%s_query(): will render: JSON rows'%template_name)
            logger.debug('select_%s_query(): Exit'%template_name)
            return json.dumps(serialize_object(rows.__dict__))
    logger.debug('select_%s_query(): will render: %s_All.html'%(template_name,table_name.lower()))
    logger.debug('select_%s_query(): Exit'%template_name)
    return render_template('%s_select_All.html'%template_name.lower(),rows=rows,options=options,collectordata=collectordata)
#===============================================================================
   
# ======================================================================
#  Auto-Generated code. Do not modify 
#  (C) Sertechno/Emtec Group (2018,2019,2020)
#  GLVH @ 2022-03-23 18:29:45.919975
# ======================================================================
# gen_views_api.html:AG 2022-03-23 18:29:45.919995
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
        #response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        #response.headers['Pragma']        = 'no-cache'
        try:
            id_counter = 0
            if type(id) == str and ',' in id:
                id_values = id.split(',')
            else:
                id_values=[id]
            # Codigo para un solo campo de id
            # chequear si marcado explicitamente
            db.session.flush()
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
                    if 'name' in request.args:
                        query = query.filter(Users.name == request.args.get('name'))
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
                    if 'roles' in request.args:
                        query = query.filter(Users.roles == request.args.get('roles'))
                    if 'ldap' in request.args:
                        query = query.filter(Users.ldap == request.args.get('ldap'))
                    if 'ldap_user' in request.args:
                        query = query.filter(Users.ldap_user == request.args.get('ldap_user'))
                    if 'ldap_common' in request.args:
                        query = query.filter(Users.ldap_common == request.args.get('ldap_common'))
                    if 'ldap_host' in request.args:
                        query = query.filter(Users.ldap_host == request.args.get('ldap_host'))
                    if 'ldap_port' in request.args:
                        query = query.filter(Users.ldap_port == request.args.get('ldap_port'))
                    if 'ldap_domain' in request.args:
                        query = query.filter(Users.ldap_domain == request.args.get('ldap_domain'))
                    if 'vars' in request.args:
                        query = query.filter(Users.vars == request.args.get('vars'))
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
            row.name = request.json.get('name',None)
            row.role_id = request.json.get('role_id',None)
            row.email = request.json.get('email',None)
            row.password_hash = request.json.get('password_hash',None)
            row.confirmed = request.json.get('confirmed',0)
            row.CC_Id = request.json.get('CC_Id',1)
            row.roles = request.json.get('roles',None)
            row.ldap = request.json.get('ldap',0)
            row.ldap_user = request.json.get('ldap_user',None)
            row.ldap_common = request.json.get('ldap_common',None)
            row.ldap_host = request.json.get('ldap_host',None)
            row.ldap_port = request.json.get('ldap_port',0)
            row.ldap_domain = request.json.get('ldap_domain',None)
            row.vars = request.json.get('vars',None)
            # ----------------------------------------------------------
            db.session.add(row)
            db.session.flush()
            db.session.commit()
            db.session.flush()
            db.session.refresh(row)
            db.session.flush()
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
                if 'name' in request.json.keys():
                    row.name = request.json.get('name')
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
                if 'roles' in request.json.keys():
                    row.roles = request.json.get('roles')
                if 'ldap' in request.json.keys():
                    row.ldap = request.json.get('ldap')
                if 'ldap_user' in request.json.keys():
                    row.ldap_user = request.json.get('ldap_user')
                if 'ldap_common' in request.json.keys():
                    row.ldap_common = request.json.get('ldap_common')
                if 'ldap_host' in request.json.keys():
                    row.ldap_host = request.json.get('ldap_host')
                if 'ldap_port' in request.json.keys():
                    row.ldap_port = request.json.get('ldap_port')
                if 'ldap_domain' in request.json.keys():
                    row.ldap_domain = request.json.get('ldap_domain')
                if 'vars' in request.json.keys():
                    row.vars = request.json.get('vars')
                # ----------------------------------------------------------
                db.session.merge(row)
                db.session.flush()
                db.session.commit()
                db.session.flush()
                db.session.refresh(row)
                db.session.flush()
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
                db.session.rollback()
                if request.values is not None and len(request.values):
                    if 'username' in request.values:
                        row.username = request.values.get('username')
                    if 'name' in request.values:
                        row.name = request.values.get('name')
                    if 'role_id' in request.values:
                        row.role_id = request.values.get('role_id')
                    if 'email' in request.values:
                        row.email = request.values.get('email')
                    if 'password_hash' in request.values:
                        row.password_hash = request.values.get('password_hash')
                    if 'confirmed' in request.values:
                        row.confirmed = request.values.get('confirmed')
                    if 'CC_Id' in request.values:
                        row.CC_Id = request.values.get('CC_Id')
                    if 'roles' in request.values:
                        row.roles = request.values.get('roles')
                    if 'ldap' in request.values:
                        row.ldap = request.values.get('ldap')
                    if 'ldap_user' in request.values:
                        row.ldap_user = request.values.get('ldap_user')
                    if 'ldap_common' in request.values:
                        row.ldap_common = request.values.get('ldap_common')
                    if 'ldap_host' in request.values:
                        row.ldap_host = request.values.get('ldap_host')
                    if 'ldap_port' in request.values:
                        row.ldap_port = request.values.get('ldap_port')
                    if 'ldap_domain' in request.values:
                        row.ldap_domain = request.values.get('ldap_domain')
                    if 'vars' in request.values:
                        row.vars = request.values.get('vars')
                # ----------------------------------------------------------
                db.session.merge(row)
                db.session.flush()
                db.session.commit()
                db.session.flush()
                db.session.refresh(row)
                db.session.flush()
                message = f"Modified 'Users' id = {id}"
                try:
                    row     = json.loads(row.get_json())
                except:
                    row     = None
            else:
                code    = API_NOT_FOUND
                message = f"Not found Users with id = {id}"
                row     = None
                db.session.rollback()
        except Exception as e:
            emtec_handle_general_exception(e,fp=sys.stderr)
            code    = API_SYSTEM_ERROR
            message = str(e)
            row     = None
            db.session.rollback()
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
                db.session.flush()
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

# ======================================================================# ======================================================================
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
# ======================================================================
# BUTLER REQUEST FUNCTIONS
# (c) Sertechno 2020
# GLVH @ 2020-12-31
# ======================================================================

# Templates will reside on view_request_template.py

# Support functions
import copy
from pprint import pprint,pformat

from emtec.butler.functions import *

# View functions        

# receives a code or Id and returns cost center object
def get_cost_center(code):
    cc = None
    try:
        if code is not None:
            if type(code) == int:
                cc = db.session.query(
                        Cost_Centers
                        ).filter(Cost_Centers.CC_Id==code
                        ).one_or_none()
            elif type(code) == str:
                cc = db.session.query(
                        Cost_Centers
                        ).filter(Cost_Centers.CC_Code==code
                        ).one_or_none()
    except Exception as e:
        logger.error(f"{this()} CC '{code} not found exception: {str(e)}'")
    return cc
    
# get cost centers uses codes NOT ids
def get_cost_centers(CC_TOP=None):
    # Recursively get a list of CCs descendants of CC_TOP
    cc_list = []
    #print(f"{this()}: CC_TOP={CC_TOP} {type(CC_TOP)}")
    try:
        if type(CC_TOP) == str:            
        #f CC_TOP is not None:            
            query = db.session.query(
                        Cost_Centers
                        ).filter(Cost_Centers.CC_Parent_Code==CC_TOP)
            logger.debug(f"{this()}: query = {query}")
            #print(f"{this()}: query = {query}")
            result = query.all()
            for row in result:
                # Load Top Cost Center if found (should be only 1)
                cc_list.append((row.CC_Id,row.CC_Code,row.CC_Description))
                children = db.session.query(
                            Cost_Centers
                            ).filter(Cost_Centers.CC_Parent_Code == row.CC_Code
                            ).all()
                for child in children:
                    cc_list.append((child.CC_Id,child.CC_Code,child.CC_Description))
                    # Recursive call to get deeper CCs
                    cc_list = cc_list + get_cost_centers(child.CC_Parent_Code)
            cc_list=unique_list(cc_list)
        # Returns a list of tuples with unique (Id,Code,Description)
        logger.trace(f"{this()}: {pformat(cc_list)}")
    except Exception as e:
        logger.error(f"{this()}: {len(cc_list)} CCs in list")        
        emtec_handle_general_exception(e,fp=sys.stderr)
    return cc_list    

def get_cost_centers_fast(CC_TOP,maximum=9999999999):
    # returns a list of CCs children of CC_TOP and below maximum
    cc_list = []
    try:
        result = db.session.query(
                    Cost_Centers
                    ).filter(Cost_Centers.CC_Id>CC_TOP
                    ).filter(Cost_Centers.CC_Id<maximum
                    ).all()
        for row in result:
            # Load Top Cost Center if found (should be only 1)
            cc_list.append((row.CC_Id,row.CC_Code,row.CC_Description,row.CC_Parent_Code))
        #cc_list=unique_list(cc_list)
        # Returns a list of tuples with unique (Id,Code,Description)
        logger.trace(f"{this()}: {pformat(cc_list)}")
    except Exception as e:
        logger.error(f"{this()}: {len(cc_list)} CCs in list")        
        emtec_handle_general_exception(e,fp=sys.stderr)
    logger.debug(f"{this()}: {len(cc_list)} CCs in list")        
    return cc_list    

""" --------------------------------------------------------------------
==>  13 corporativo CC_Code%30000000 != 0 and CC_Code%10000 == 0
==>  37 gerencias   CC_Code%30000000 != 0 and CC_Code%10000 != 0 and CC_Code%100 == 0 
==> 555 .........   CC_Code%30000000 != 0 and CC_Code%10000 != 0 and CC_Code%100 != 0 
==> 185 ambientes   CC_Code%30000000 != 0 and CC_Code%10000 != 0 and CC_Code%100 != 0 and CC_Code%10 == 0
==> 370 discos      CC_Code%30000000 != 0 and CC_Code%10000 != 0 and CC_Code%100 != 0 and CC_Code%10 != 0
    605 CCs
-------------------------------------------------------------------- """
# Corporativo
def get_corporate_list(top_cost_center_code,ccs=None):
    # Cost Center options need to be refreshed from Collector ----------
    # These need to come from Collector Cost Centers
    # Gets all depending cost centers and returns module 100 '00' in
    # list -------------------------------------------------------------
    corporate_list = []
    logger.debug(f"{this()}: top_cost_center_code={top_cost_center_code}")
    if ccs is None:
        ccs = get_cost_centers(top_cost_center_code)
    logger.debug(f"{this()}: {len(ccs)} CCs found below {top_cost_center_code}")
    for cc in ccs:
        code = int(cc[1])
        if code > int(top_cost_center_code) and code%10000 == 0:
            corporate_list.append([cc[0],cc[2]])
    logger.trace(f"{this()}: {pformat(corporate_list)}")
    logger.debug(f"{this()}: {len(corporate_list)} CCs Corporate")
    return corporate_list

# Gerencias
def get_department_list(top_cost_center_code,ccs=None):
    # Cost Center options need to be refreshed from Collector ----------
    # These need to come from Collector Cost Centers
    # Gets all depending cost centers and returns module 100 '00' in
    # list -------------------------------------------------------------
    department_list = []
    gd_map = {}
    logger.debug(f"{this()}: top_cost_center_code={top_cost_center_code}")
    if ccs is None:
        ccs = get_cost_centers(top_cost_center_code)
    logger.debug(f"{this()}: {len(ccs)} CCs found below {top_cost_center_code}")
    for cc in ccs:
        #f cc[0]> top_cost_center_code and cc[0]%10000 != 0 and cc[0]%10000:
        code = int(cc[1])
        if code > int(top_cost_center_code) and code%10000 != 0 and code%100 == 0:
            department_list.append([cc[0],cc[2]])
            gd_map.update({cc[0]:{'code':cc[1],'description':cc[2],'corporate':cc[3],}})
    logger.trace(f"{this()}: {pformat(department_list)}")
    logger.debug(f"{this()}: {len(department_list)} CCs Gerencias")
    return department_list,gd_map

#==> 185 ambientes   CC_Code%30000000 != 0 and CC_Code%10000 != 0 and CC_Code%100 != 0 and CC_Code%10 == 0
def get_cc_list(top_cost_center_code,ccs=None):
    # Cost Center options need to be refreshed from Collector ----------
    # These need to come from Collector Cost Centers
    # Gets all depending cost centers and returns module 100 '00' in
    # list -------------------------------------------------------------
    cc_list = []
    logger.debug(f"{this()}: top_cost_center_code={top_cost_center_code}")
    if ccs is None:
        ccs = get_cost_centers(top_cost_center_code)
    logger.debug(f"{this()}: {len(ccs)} CCs found below {top_cost_center_code}")
    for cc in ccs:
        # 20210401 ccid = cc[0]%top_cost_center_code
        #f cc[0] != top_cost_center_code and ccid < 10000 and cc[0]%100 == 0:
        code = int(cc[1])
        ccid = code%int(top_cost_center_code)
        if code != int(top_cost_center_code) and ccid<100 != 0 and ccid%10 == 0 :
            cc_list.append([cc[0],cc[2]])
    logger.trace(f"{this()}: {pformat(cc_list)}")
    logger.debug(f"{this()}: {len(cc_list)} CCs Ambientes")
    return cc_list

# Tipos de Discos 
def get_type_list(top_cost_center_code,ccs=None):
    # Cost Center options need to be refreshed from Collector ----------
    # These need to come from Collector Cost Centers
    # Gets all depending cost centers and returns module 100 '00' in
    # list -------------------------------------------------------------

    # Codigo omitido temporalmente elimnar hardcode luego
    ctype_list = []
    '''
    ctype_list = [
        ['HDD','Hard Disk Drive'],
        ['SSD','Solid State Disk'],
    ]
    '''
    logger.debug(f"{this()}: top_cost_center_code={top_cost_center_code}")
    if ccs is None:
        ccs = get_cost_centers(top_cost_center_code)
    else:
        logger.debug(f"{this()}: ccs ={len(ccs)}")
    logger.debug(f"{this()}: {len(ccs)} CCs found below {top_cost_center_code}")
    for cc in ccs:
        if int(cc[1]) % int(top_cost_center_code) < 10 :
            ctype_list.append([cc[0],cc[2]])
    logger.trace(f"{this()}: {pformat(ctype_list)}")
    logger.debug(f"{this()}: {len(ctype_list)} CCs Tipos de discos")
    return ctype_list
#    ==> 370 discos      CC_Code%30000000 != 0 and CC_Code%10000 != 0 and CC_Code%100 != 0 and CC_Code%10 != 0
        
'''
def get_image_list():
    # List of images need to be refreshed from Nutanix Cluster ---------
    # These need to come from Nutanix Images
    # and updated in local Table
    image_list =  db.session.query(Nutanix_VM_Images).all()
    logger.trace(f"{this()}: {pformat(image_list)}")
    return image_list

def get_disk_image_list():
    # List of images need to be refreshed from Nutanix Cluster ---------
    # These need to come from Nutanix Images
    # and updated in local Table
    image_list =  db.session.query(Disk_Images).all()
    logger.trace(f"{this()}: {pformat(image_list)}")
    return image_list
'''
def get_cluster_list():
    # List of clusters need to be refreshed from Nutanix ---------------
    # These need to come from Nutanix 
    # and updated in local Table
    cluster_list = []
    clusters =  db.session.query(Clusters).all()
    for cluster in clusters:
        if cluster.cluster_uuid not in ['','0',None]:
            cluster_list.append((cluster.cluster_uuid,cluster.cluster_name,cluster.cluster_ip))
    logger.trace(f"{this()}: {pformat(cluster_list)}")
    return cluster_list
    
def get_migration_group_list():
    migration_group_list = []
    migration_groups =  db.session.query(Migration_Groups).all()
    for migration_group in migration_groups:
        if migration_group.MG_Id not in ['','0',None]:
            migration_group_list.append((migration_group.MG_Id,migration_group.Name,migration_group.Origin,migration_group.Destiny))
    logger.trace(f"{this()}: {pformat(migration_group_list)}")
    return migration_group_list

def get_project_list():
    # List of projects need to be refreshed from Nutanix ---------------
    # These need to come from Nutanix 
    # and updated in local Table
    project_list = []
    projects =  db.session.query(Projects).all()
    for project in projects:
        project_list.append((project.project_uuid,project.project_name))
    logger.trace(f"{this()}: {pformat(project_list)}")
    return project_list

def get_category_list():
    # List of categories need to be refreshed from Nutanix Cluster -----
    # These need to come from Nutanix Images
    # and updated in local Table
    category_list = []
    categories =  db.session.query(Categories).all()
    for category in categories:
        category_list.append((category.category_name,category.category_description))
    logger.trace(f"{this()}: {pformat(category_list)}")
    return category_list

def get_subnet_list():
    # List of subnets need to be refreshed from Nutanix Cluster --------
    # These need to come from Nutanix Images
    # and updated in local Table
    subnet_list = []
    subnets =  db.session.query(Subnets).all()

    for subnet in subnets:
        subnet_list.append([subnet.get_dict()])
    logger.trace(f"{this()}: {pformat(subnet_list)}")
    return subnet_list

def get_subnet_name(uuid,subnet_list):
    logger.warning(f"{this()}: uuid = {uuid}")
    name = ''
    for subnet in subnet_list:
        if subnet[0] == uuid:
            name = subnet[1]
    logger.warning(f"{this()}: name = {name}")    
    return name

def get_cluster_uuid(data,cluster_name):
    for uuid,name in data.get('clusters'):
        if name == cluster_name:
            return uuid
    return None
    
def get_cluster_name(data,cluster_uuid):
    for uuid,name in data.get('clusters'):
        if uuid == cluster_uuid:
            return name
    return None
    
def get_project_uuid(data,project_name):
    for uuid,name in data.get('projects'):
        if name == project_name:
            return uuid
    return None

def get_category_description(data,category_name):
    for name,description in data.get('categories'):
        if name == category_name:
            return description
    return None

def get_environment_code(data,environment_name):
    logger.debug(f"{this()}: environment={environment_name} {data.get('ccs')}")
    for code,name in data.get('ccs'):
        logger.debug(f"{this()}: code={code} name={name}")
        if name == environment_name:
            return code
    return None

def get_environment_name(data,environment_code):
    logger.debug(f"{this()}: environment={environment_code} {data.get('ccs')}")
    for code,name in data.get('ccs'):
        logger.debug(f"{this()}: code={code} name={name}")
        if code == environment_code:
            return name
    return None
    
def get_environments(filename,data):
    environments = None
    logger.debug(f"{this()}: In filename={filename}")
    try:
        with open(filename,'r') as fp:
            environments = json.load(fp)
        logger.debug(f"{this()}: environments = {environments.keys()}")
        for e in environments.keys():
            environment = environments.get(e)
            logger.debug(f"{this()}: environment '{e}' clusters = {environment.keys()}")
            try:
                for c in environment.keys():
                    cluster_uuid     = get_cluster_uuid(data,c)
                    environment_code = get_environment_code(data,e)
                    environments[e][c].update({'uuid':cluster_uuid})
                    environments[e][c].update({'environment':environment_code})
                    if cluster_uuid is not None:
                        try:
                            logger.debug(f"{this()}: environment '{e}' cluster = {c}")
                            cluster = environment[c]
                            project_name         = cluster['project'].get('name')
                            category_name        = cluster['category'].get('name')
                            project_uuid         = get_project_uuid(data,project_name)
                            category_description = get_category_description(data,category_name)
                            environments[e][c]['project'].update({'uuid':project_uuid})
                            environments[e][c]['category'].update({'description':category_description})
                        except Exception as e:
                            logger.warning(f"{this()}: environment '{e}' cluster = {c} {str(e)}")
                    else:
                            logger.warning(f"{this()}: environment '{e}' cluster = {c} INVALID")                        
            except Exception as e:
                logger.error(f"{this()}: environment '{e}' cluster = {c} {str(e)}")
    except Exception as e:
        logger.critical(f"INVALID ENVIRONMENTS: filename={filename} exception: {str(e)}")
    return environments
    
def get_environments_codes(data,environments):
    logger.debug(f"{this()}: In")
    E={}
    try:
        logger.debug(f"{this()}: environments = {environments.keys()}")
        for e in environments.keys():
            environment_code = get_environment_code(data,e) 
            E.update({environment_code:{}})
            environment = environments.get(e)
            logger.debug(f"{this()}: environment '{e}' clusters = {environment.keys()}")
            try:
                for c in environment.keys():
                    cluster = environment[c]
                    cluster_uuid = get_cluster_uuid(data,c)
                    if cluster_uuid is not None:
                        E[environment_code].update({
                            cluster_uuid:{
                                'project' : get_project_uuid(data,cluster['project'].get('name')),
                                'category': cluster['category'].get('name'),
                                'project_name' : cluster['project'].get('name'),
                                'category_description': cluster['category'].get('description')
                            }
                        })
            except Exception as e:
                logger.error(f"{this()}: environment '{e}' cluster = {c} {str(e)}")
    except Exception as e:
        logger.critical(f"INVALID ENVIRONMENTS: exception: {str(e)}")
    return E
    
def get_environment_attributes(data,environment=None,cluster=None,code=None,uuid=None):
    if environment is None:
        environment = get_environment_name(data,code)
    if cluster is None:
        environment = get_cluster_name(data,uuid)
        
    cluster = data.get('environments').get('environment').get('cluster')
    project_uuid  = cluster.get('project').get('uuid')
    category_name = cluster.get('category').get('name')
    return project_uuid,category_name
    
def get_project_subnet_list():
    # List of subnets need to be refreshed from Nutanix Cluster --------
    # These need to come from Nutanix Images
    # and updated in local Table
    projects =  db.session.query(Projects).all()
    subnet_list = []
    for project in projects:
        subnets = []
        for project_subnet in project.project_subnets.split(','):
            try:
                if project_subnet not in ['','0',None]:
                    uuid,name=project_subnet.split(':')
                    # Load valid subnet pairs only
                    if uuid not in ['','0',None] and name not in ['','0',None]:
                        subnets.append([f'{uuid}:{project.project_uuid}',f'{name}'])
            except Exception as e:
                emtec_handle_general_exception(e,logger=logger)
        if len(subnets):
            # load valid subnets sublists only
            # since will be exploited with NodeJS thet list of lists is required
            subnet_list.append(
                [   project.project_name,
                    subnets
                ]
        )
    logger.trace(f"{this()}: {pformat(subnet_list)}")
    return subnet_list

def get_project_subnet_options():
    # List of subnets need to be refreshed from Nutanix Cluster --------
    # These need to come from Nutanix Images
    # and updated in local Table
    projects =  db.session.query(Projects).all()
    subnet_list = []
    for project in projects:
        subnets = []
        for project_subnet in project.project_subnets.split(','):
            try:
                if project_subnet not in ['','0',None]:
                    uuid,name=project_subnet.split(':')
                    # Load valid subnet pairs only
                    if uuid not in ['','0',None] and name not in ['','0',None]:
                        subnets.append([f'{uuid}',f'{name} @ {project.project_name}'])
            except Exception as e:
                emtec_handle_general_exception(e,logger=logger)
        if len(subnets):
            # load valid subnets sublists only
            # since will be exploited with NodeJS thet list of lists is required
            subnet_list.append(
                [   project.project_uuid,
                    subnets
                ]
        )
    logger.trace(f"{this()}: {pformat(subnet_list)}")
    return subnet_list

def get_user_list():
    # List of user need to be refreshed from Nutanix Cluster -----------
    # These need to come from Nutanix Images
    # and updated in local Table
    user_list = []
    users =  db.session.query(Users).all()
    for user in users:
        user_list.append((user.id,user.username))
    logger.trace(f"{this()}: {pformat(user_list)}")
    return user_list

def get_rates(margin=1,CC_Id=1):
    # Cost Centers related to Storage types ----------------------------
    # These need to come from Collector Cost Centers
    logger.debug(f"{this()}: cc={CC_Id} and a margin of {margin}") 
    rates = {}
    try:
        dsk_rate = 0
        rows = db.session.query(Rates).all()
        # Load Rates and margin factor
        for row in rows:
            logger.trace(f"row={row.Rat_Id} {row.Typ_Code} {row.Rat_Price} {row.CC_Id}")
            if row.Typ_Code == 'NUL':
                # Gets Margin Factor from scepcial NUL type rate
                margin = 1 + row.Rat_Price
            else:
                # Sets Rate to Monthly value
                if row.Rat_Period == 1:         # Hourly
                    rates.update({ row.Typ_Code:row.Rat_Price * 720 })
                elif row.Rat_Period == 2:       # Daily
                    rates.update({ row.Typ_Code:row.Rat_Price * 30 })
                else:
                    rates.update({ row.Typ_Code:row.Rat_Price })
                # Setup rate as per disk type
                if row.Typ_Code == 'DSK': # and row.CC_Id == CC_Id:
                    dsk_type = 'DSK'
                    if  row.CC_Id == CC_Id and row.CC_Id%10 == 1:
                        logger.debug(f'{this()}: {row.Typ_Code} {row.CC_Id} {CC_Id} -> DSK=*1 -> HDD')
                        rates.update({ 'HDD': rates[row.Typ_Code] })
                        dsk_rate = rates[row.Typ_Code]
                    elif  row.CC_Id == CC_Id and row.CC_Id%10 == 2:
                        logger.debug(f'{this()}: {row.Typ_Code} {row.CC_Id} {CC_Id} -> DSK=*2 -> SSD')
                        rates.update({ 'SSD'   : rates[row.Typ_Code] })
                        dsk_rate = rates[row.Typ_Code]
        if dsk_rate == 0:
            logger.error(f"{this()}: dsk_rate = {dsk_rate} No Disk Rate found for CC Id = {CC_Id}")
        rates.update({ 'DSK'   : dsk_rate })
        # adjust rates to estimate billing rate, applies margin factor
        for rate in rates:
            rates[rate] *= margin
        logger.debug(f"{this()}: \n{pformat(rates)}")
    except Exception as e:
        logger.error(f"{this()}: {str(e)}")
    return rates

def get_db_rates(margin=1):
    # Cost Centers related to Storage types ----------------------------
    # These need to come from Collector Cost Centers
    logger.debug(f"{this()}: loading rates for all CCs and a margin of {margin}") 
    rows = db.session.query(Rates).all()
    rates = {}
    # Load Rates and margin factor
    for row in rows:
        if row.Typ_Code == 'NUL':
            # Gets Margin Factor from scepcial NUL type rate
            margin = 1 + row.Rat_Price
        else:
            # Sets Rate to Monthly value
            if row.Rat_Period == 1:         # Hourly
                rates.update({ f'{row.Typ_Code}:{row.CC_Id}':row.Rat_Price * 720 })
            elif row.Rat_Period == 2:       # Daily
                rates.update({ f'{row.Typ_Code}:{row.CC_Id}':row.Rat_Price * 30 })
            else:
                rates.update({ f'{row.Typ_Code}:{row.CC_Id}':row.Rat_Price })
    # adjust rates to estimate billing rate, applies margin factor
    for rate in rates:
        rates[rate] *= margin
    logger.trace(f"{this()}: {len(rates)} rates loaded")
    logger.trace(f"{this()}: {pformat(rates)}")
    return rates

def get_monthly_rate(row,rox):
    logger.debug(f"{this()}: Enter")
    try:
        storage = 0
        # CC_Id need to be built
        rates = get_rates(CC_Id=row.CC_Id)
        logger.debug(f"{this()}: rates={rates}")
        logger.debug(f"{this()}: row.CC_Id     = {row.CC_Id}")
        logger.debug(f"{this()}: rox.disk_type = {rox.disk_type}")
        for i in range(12):
            storage += getattr(rox,f'disk_{i}_size')            
        cpu = rox.vcpus_per_socket * rox.num_sockets * rates['CPU']
        ram = rox.memory_size_gib * rates['RAM']
        dsk = storage * rates['DSK']
        '''
        try:
            if rox.disk_type%100 in [11,12,13]:
                storage_type = ['HDD','SSD','HYB'][rox.disk_type%100-11]
                dsk = storage * rates[storage_type]
            else:
                dsk = 0
        
        except Exception as e:
            logger.error(f'{this()}: excepcion = {str(e)}')
            dsk = 0
        
        logger.debug(f"{this()}: storage_type = {storage_type}")
        '''
        logger.debug(f"{this()}: cpu          = {cpu:15.10f} UF <= {rox.vcpus_per_socket*rox.num_sockets:4.0f}    x {rates['CPU']:.10f}")
        logger.debug(f"{this()}: ram          = {ram:15.10f} UF <= {rox.memory_size_gib:4.0f} GB x {rates['RAM']:.10f}")
        #ogger.debug(f"{this()}: dsk          = {dsk:15.10f} UF <= {storage:4.0f} GB x {rates[storage_type]:.10f}")
        logger.debug(f"{this()}: dsk          = {dsk:15.10f} UF <= {storage:4.0f} GB x {rates['DSK']:.10f}")
        logger.debug(f"{this()}: month        = {cpu+ram+dsk:15.10f} UF")
        return cpu + ram + dsk
    except Exception as e:
        logger.warning(f"{this()}: exception {str(e)}")
        return 0

#def butler_notify_request(subject_detail=None,data=None,recipients=None,html_function=None):
def notify_request(Id,subject_detail=None,data=None,recipients=None):
    logger.debug(f'{this()}:Enter')
    from    flask_mail          import Message
    if current_app.config['BUTLER_REQUEST_NOTIFICATIONS']:
        try:
            subject = f"{current_app.config['BUTLER_MAIL_SUBJECT_PREFIX']}: Solicitud # {Id}"
            if subject_detail is not None:
                subject = f'{subject}. {subject_detail}'
            sender = current_app.config['BUTLER_MAIL_SENDER']
            # Look for Requets's user's ids
            # row = requests.query.filter(requests.Id == Id).one()
            row = db.session.query(Requests).filter(Requests.Id == Id).one()
            # Look for all possible email recipients
            if recipients is None:
                rows = User.query.filter(
                            User.id.in_(
                                [   row.User_Id,
                                    row.Approver_Id,
                                    current_user.id
                                ]
                            )
                            ).filter(User.email.isnot(None)
                            ).all()
                recipients = []
                for row in rows:
                    recipients.append(row.email)
            # simplify list
            recipients = unique_list(recipients)
            logger.debug(f"{this()}: recipients = {recipients}")
            if len(recipients):
                msg = Message(  subject, sender = sender, recipients = recipients )
                logger.trace(f"{this()}: msg = {msg}")
                # HTML body
                logger.warning(f'{this()}: calling output request(Id={Id})')
                html = output_Request(Id,data=data).encode("ascii","xmlcharrefreplace")
                logger.trace(f'{this()}: html = {html}')
                msg.html = html
                logger.warning(f'{this()}: queueing email for request {Id} ...')
                mail.send(msg)
                logger.warning(f'{this()}: email queued  for request {Id}.')
        except Exception as e:
            emtec_handle_general_exception(e,logger=logger)
            flash(f'{this()}: Excepción: Solicitud: {Id}: {str(e)}')
    else:
        if current_app.config['DEBUG']:
            logger.warning(f'{this()}: Notificaciones deshabilitadas')
    logger.debug(f'{this()}: OUT')
    # ------------------------------------------------------------------

def dump_form(form):
    logger.debug(f'{this()}: form {form}')
    try:
        logger.debug(f'form.submit_Guardar.data    = {form.submit_Guardar.data}')
        logger.debug(f'form.submit_Retorno.data    = {form.submit_Retorno.data}')
        logger.debug(f'form.submit_Completado.data = {form.submit_Completado.data}')
        logger.debug(f'form.submit_Cancelar.data   = {form.submit_Cancelar.data}')
        logger.debug(f'form.submit_Aprobar.data    = {form.submit_Aprobar.data}')
        logger.debug(f'form.submit_Rechazar.data   = {form.submit_Rechazar.data}')
        logger.debug(f'form.submit_Retorno.data    = {form.submit_Retorno.data}')
        logger.debug(f'form.vmName                 = {form.vmName.data}')
        logger.debug(f'form.vmCPU                  = {form.vmCPU.data}')
        logger.debug(f'form.vmRAM                  = {form.vmRAM.data}')
        logger.debug(f'form.vmType                 = {form.vmType.data}')
        logger.debug(f'form.vmCC                   = {form.vmCC.data}')
        logger.debug(f'form.vmStatus               = {form.vmStatus.data}')
        for i in range(12):
            logger.debug(f"form.vmDisk{i}Size          = '{getattr(form,f'vmDisk{i}Size').data}' '{getattr(form,f'vmDisk{i}Image').data}'")
    except Exception as e:
        emtec_handle_general_exception(e,logger=logger)
    logger.debug(f'------------------------------------------------------')

def get_range_list(range_list):
    list_of_ranges=[]
    try:
        if type(range_list) == list:
            for i in range(len(range_list)):
                start,end = range_list[i].split(' ')
                start = start.split('.')
                end   = end.split('.')
                s=e=0
                if len(start) == 4 and len(end) == 4:
                    ok = True
                    # Check for range validity
                    for k in range(3):
                        if start[k] != end[k]: ok = False
                    if ok:
                        list_of_ranges.append((ip_to_int(start),ip_to_int(end)))
        else:
            list_of_ranges=[]
    except Exception as e:
        emtec_handle_general_exception(e,logger=logger,fp=sys.stderr)
    return list_of_ranges

def calculate_form(form,row,rox):
    logger.debug(f"{this()}: Enter. called by {caller()}")
    logger.debug(f"form.vmTopCC           = {form.vmTopCC}")
    logger.debug(f"form.vmCorporate.data  = {form.vmCorporate.data}")
    logger.debug(f"form.vmDepartment.data = {form.vmDepartment.data}")
    logger.debug(f"form.vmCC.data         = {form.vmCC.data}")
    logger.debug(f"form.vmType.data       = {form.vmType.data}")
    try:
        # Copy actual DB values into temp buffers
        tmp_row = copy.copy(row)
        tmp_rox = copy.copy(rox)
        # CC_Id need to be rebuild upon actual form data
        logger.debug(f"{this()}: top:{form.vmTopCC} co: {form.vmCorporate.data} dd:{form.vmDepartment.data} cc:{form.vmCC.data} tt:{form.vmType.data}")
        tmp_row.CC_Id = form.vmTopCC + form.vmCorporate.data%form.vmTopCC + form.vmDepartment.data%form.vmTopCC + form.vmCC.data%form.vmTopCC +form.vmType.data%form.vmTopCC
        logger.debug(f"{this()}: db CC = old {row.CC_Id} now {form.vmCorporate.data}+{form.vmDepartment.data}+{form.vmCC.data}+{form.vmType.data}-> {tmp_row.CC_Id}")
        # Save actual form values into temporary buffers
        save_form(form,tmp_row,tmp_rox)
        logger.debug(f"{this()}: now form CC = {tmp_row.CC_Id}")
        # Calculate form values upon temporary buffers
        form.vmData.update({'storage': 0})
        form.vmData.update({'month'  : 0})
        logger.debug(f"{this()}: form.vmData['month'] = {form.vmData['month']}")
        for i in range(12):
            form.vmData['storage'] += getattr(form,f'vmDisk{i}Size').data
        form.vmData.update({'month':get_monthly_rate(tmp_row,tmp_rox)})
        logger.debug(f"{this()}: form.vmData['storage'] = {form.vmData.get('storage',0)}")
        logger.debug(f"{this()}: form.vmData['month']   = {form.vmData.get('month',0)}")
    except Exception as e:
        logger.error(f"{this()}: called by {caller()} {str(e)}")
        emtec_handle_general_exception(e,logger=logger)
    logger.debug(f"{this()}: Exit")

def load_form(form,row,rox):
    logger.debug(f'{this()}: Enter. loading form from DB data ... called by {caller()}')
    try:
        if rox.vm_name is None or str(rox.vm_name)== 'None':
            rox.vm_name = ''
        form.vmName.data = rox.vm_name 
        if str(form.vmName.data) == 'None':
            form.vmName.data = ''
        form.vmCPS.data     = rox.vcpus_per_socket
        form.vmSockets.data = rox.num_sockets
        form.vmCPU          = form.vmCPS.data * form.vmSockets.data
        form.vmRAM.data     = max(1,rox.memory_size_gib)
        # row.CC_Id is a compound code need to be deconstructed here
        # rule is vmType is >=1 <100
        if row.CC_Id is not None:
            disk_type   = row.CC_Id % 10
            environment = row.CC_Id % 100 - disk_type
            management  = row.CC_Id % 10000 - environment - disk_type
            corporate   = row.CC_Id % 1000000 - management - environment - disk_type
            form.vmType.data       = form.vmTopCC + disk_type
            form.vmCC.data         = form.vmTopCC + environment
            form.vmDepartment.data = form.vmTopCC + management + corporate
            form.vmCorporate.data  = form.vmTopCC + corporate
            logger.debug(f"{this()}: top:{form.vmTopCC} co:{form.vmCorporate.data} dd:{form.vmDepartment.data} cc:{form.vmCC.data} tt:{form.vmType.data}")
        form.vmStatus.data   = row.Status
        for i in range(12):
            getattr(form,f'vmDisk{i}Size').data  = getattr(rox,f'disk_{i}_size')
            if i == 0: 
                getattr(form,f'vmDisk{i}Image').data = getattr(rox,f'disk_{i}_image')
        if form.vmCorporate.data is not None:
            calculate_form(form,row,rox)
        else:
            logger.debug(f"{this()}: form calculation not called. not enough data.")
        logger.debug(f"{this()}: form.vmData['month']   = {form.vmData.get('month',None)}")
        logger.debug(f"{this()}: form.vmData['storage'] = {form.vmData.get('storage',None)}")
        # Extra Fields
        # Ownership
        form.vmCluster.data     = rox.cluster_uuid
        form.vmProject.data     = rox.project_uuid
        form.vmCategory.data    = rox.category_name
        form.vmUsername.data    = rox.vm_username
        form.vmPassword.data    = rox.vm_password
        # Array of Backup sets
        form.vmBackUpSet1.data  = rox.backup_set_1
        form.vmBackUpSet2.data  = rox.backup_set_2
        form.vmBackUpSet3.data  = rox.backup_set_3
        # Flags
        form.vmCDROM.data       = rox.vm_cdrom
        form.vmDRP.data         = rox.vm_drp
        form.vmDRPRemote.data   = rox.vm_drp_remote
        
        # Fix some initial values --------------------------------------
        # networking
        # Populate Subnets data
        subnet_list = []
        for project in get_project_subnet_options():
            if project[0] == rox.project_uuid:
                subnet_list = project[1]
        # populates list of selected vlans
        
        form.vmVlan0Name.data = rox.nic_0_vlan
        form.vmVlan1Name.data = rox.nic_1_vlan
        form.vmVlan2Name.data = rox.nic_2_vlan
        form.vmVlan3Name.data = rox.nic_3_vlan

        if form.vmDRP.data is None:
            form.vmDRP.data = False
            logger.debug(f'{this()}: form.vmDRP.data adjusted to = {form.vmDRP.data}')
        if form.vmDRPRemote.data is None:
            form.vmDRPRemote.data = False
            logger.debug(f'{this()}: form.vmDRPRemote.data adjusted to = {form.vmDRPRemote.data}')
        if form.vmCDROM.data is None:
            form.vmCDROM.data = False
            logger.debug(f'{this()}: form.vmCDROM.data adjusted to = {form.vmCDROM.data}')
        form.vmRequestText.data    = rox.request_text if rox.request_text is not None else ''
        logger.debug(f"{this()}: rox.request_text        = {type(rox.request_text)} >{rox.request_text}<")
        logger.debug(f"{this()}: form.vmRequestText.data = {type(form.vmRequestText.data)} >{form.vmRequestText.data}<")
    except Exception as e:
        emtec_handle_general_exception(e,logger=logger)
    logger.debug(f'{this()}: Exit')

def save_form(form,row,rox):
    try:
        logger.debug(f'{this()}: saving form to DB records ...')
        # Identification ---------------------------------------------------
        rox.vm_name          = form.vmName.data
        #row.Status           = form.vmStatus.data
        # CC Id is a mix of distribution CC + Storage Type
        # row.CC_Id is a compound code need
        # to be deconstructed here
        # rule is vmType is >=1 <100
        # ##############################################################
        # Need to review use of CC Class instead of hardcoded calculation
        # ##############################################################
        
        disk_type   = form.vmType.data % 10
        logger.debug(f"{this()}: top:{form.vmTopCC} disk_type:{disk_type}")    
        environment = form.vmCC.data % 100
        logger.debug(f"{this()}: top:{form.vmTopCC} environment:{environment} disk_type:{disk_type}")    
        management  = form.vmDepartment.data   % 10000
        logger.debug(f"{this()}: top:{form.vmTopCC} management:{management} environment:{environment} disk_type:{disk_type}")    
        corporate   = form.vmCorporate.data % 1000000
        logger.debug(f"{this()}: top:{form.vmTopCC} corporate:{corporate} management:{management} environment:{environment} disk_type:{disk_type}")    
        
        row.CC_Id   = form.vmTopCC + corporate + management + environment + disk_type
        logger.debug(f"{this()}: top:{form.vmTopCC} corporate:{corporate} management:{management} environment:{environment} disk_type:{disk_type} -> {row.CC_Id}")    
        # Ownership
        rox.cluster_uuid  = form.vmCluster.data
        rox.project_uuid  = form.vmProject.data
        rox.category_name = form.vmCategory.data 
        # Specifications ---------------------------------------------------    
        rox.vcpus_per_socket = form.vmCPS.data 
        rox.num_sockets      = form.vmSockets.data 
        rox.memory_size_gib  = max(form.vmRAM.data,1)
        rox.memory_size_mib  = form.vmRAM.data * 1024
        # Storage ----------------------------------------------------------
        rox.disk_type        = form.vmType.data
        for i in range(12):
            setattr( rox, f'disk_{i}_size' , getattr( form, f'vmDisk{i}Size').data  ) 
            if i == 0:
                setattr( rox, f'disk_{i}_image', getattr( form, f'vmDisk{i}Image').data ) 

        rox.nic_0_vlan = form.vmVlan0Name.data
        rox.nic_1_vlan = form.vmVlan1Name.data
        rox.nic_2_vlan = form.vmVlan2Name.data
        rox.nic_3_vlan = form.vmVlan3Name.data
        # Networking      
        logger.debug(f"nic_0_vlan={rox.nic_0_vlan}")
        logger.debug(f"nic_1_vlan={rox.nic_1_vlan}")
        logger.debug(f"nic_2_vlan={rox.nic_2_vlan}")
        logger.debug(f"nic_3_vlan={rox.nic_3_vlan}")
        # Array of Backup sets
        rox.backup_set_1  = form.vmBackUpSet1.data
        rox.backup_set_2  = form.vmBackUpSet2.data
        rox.backup_set_3  = form.vmBackUpSet3.data
        # Flags
        rox.vm_drp        = form.vmDRP.data         
        rox.vm_drp_remote = form.vmDRPRemote.data         
        rox.vm_cdrom      = form.vmCDROM.data         
        # Security and other      
        rox.vm_username   = form.vmUsername.data 
        rox.vm_password   = form.vmPassword.data 
        rox.request_text  = form.vmRequestText.data 
        logger.debug(f"{this()}: Normal exit")
    except Exception as e:
        emtec_handle_general_exception(e,logger=logger)

# ======================================================================
# **********************************************************************
# NOTA Hay que ajustar esta funcion para trabajar bien con los rates !!!
# **********************************************************************
def output_Request(Id,data=None):
    import  jinja2
    logger.debug(f'{this()}: Enter')

    row=rox=None
    top_cost_center_code = data.get('top_cost_center_code')
    all_cc_list = get_cost_centers_fast(top_cost_center_code)
    logger.debug(f"all_cc_list={len(all_cc_list)} cost centers found") 
    logger.debug(f'{this()}: inicializa listas de opciones ...') 
    corporate_list         = get_corporate_list (top_cost_center_code,all_cc_list)
    department_list,gd_map = get_department_list(top_cost_center_code,all_cc_list)
    cc_list                = get_cc_list        (top_cost_center_code,all_cc_list)
    type_list              = get_type_list      (top_cost_center_code,all_cc_list)
    logger.debug(f"corporate_list ={len(corporate_list)} corporates") 
    logger.debug(f"department_list={len(department_list)} departments") 
    logger.debug(f"cc_list        ={len(cc_list)} ccs means environments in ths context") 
    logger.debug(f"type_list      ={len(type_list)} types (of disk)") 

    data.update({'corporates' :corporate_list})
    data.update({'departments':department_list})
    data.update({'ccs'        :cc_list})
    data.update({'types'      :type_list})

    #mage_list          = get_image_list()
    image_list          = Get_images_list(db)
    vmDiskImage_choices = [('','')]
    '''
    for image in image_list:
        vmDiskImage_choices.append(
            (image.imageservice_uuid_diskclone,
            f'{image.description} ({int(image.size_mib)/1024} GB)')
            )
        data['images'].append((image.imageservice_uuid_diskclone,image.description))
    '''   
    data.update({'images'     :image_list})
    
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
        if row is not None:
            # GV db.session.close()
            data.update({'status_description':get_request_status_description(row[0].Status)})
            #ata.update({'disk_images':[]})
            data.update({'month':0})
            # Gets Monthly Rates as per Rates Table
            rates = get_rates(CC_Id=row.Requests.CC_Id)
            for i in range(1):
                uuid=getattr(row.Nutanix_Prism_VM,f'disk_{i}_image')
                name=''
                for image in vmDiskImage_choices:
                    if image[0] == uuid:
                        name = image[1]
                        break
                #ata['disk_images'].append(name)
                #ata['images'].append(name)
                
            cpu = row.Nutanix_Prism_VM.num_sockets * rates['CPU']
            ram = row.Nutanix_Prism_VM.memory_size_gib * rates['RAM']
            data['storage'] = 0
            data['storage_type'] = ''
            for i in range(12):
                data['storage'] += getattr(row.Nutanix_Prism_VM,f'disk_{i}_size')
            try:
                if row.Nutanix_Prism_VM.disk_type%10 in [1,2,3]:
                    data['storage_type'] = ['HDD','SSD','HYB'][row.Nutanix_Prism_VM.disk_type%10-1]
                    dsk = data['storage'] * rates[data['storage_type']]
                else:
                    dsk = 0
            except Exception as e:
                logger.error(f'{this()}: exception = {str(e)}')
                dsk = 0
            data['month'] = cpu + ram + dsk
        else:
            data.update({'status_description':f'ERROR: Solicitud {Id} no encontrada.'})
            data.update({'disk_images':[]})
            data.update({'month':0})
            #ata['disk_images'].append(None)
            data['storage'] = 0
            data['storage_type'] = ''
            data['month'] = 0
        
    # will render template and return HTML text
    current_app.jinja_env.globals.update(get_request_status_description=get_request_status_description)
    current_app.jinja_env.globals.update(get_vm_resume=get_vm_resume)
    current_app.jinja_env.globals.update(has_status=has_status)
    current_app.jinja_env.globals.update(get_description=get_description)
    current_app.jinja_env.globals.update(object_to_html_table=object_to_html_table)
    template       = current_app.jinja_env.get_template('report_request.html')
    logger.warning(f"{this()}: will render data using template: {template} from: 'report_request.html'")
    logger.warning(f"{this()}: dir template = {dir(template)}")
    logger.warning(f"{this()}: template.filename = {template.filename}")
    output         = template.render(
            data      = data,
            row       = row,
            body_only = True
            )
    logger.debug(f'{this()}: return output = {len(output)} {type(output)}')
    return output

'''
curl -X POST --header "Content-Type: application/json" --header "Accept: application/json" --header "Authorization: Basic Z3ZhbGVyYTpQYXNzMTAxMC4s" -d "{
  \"kind\": \"vm\",
  \"filter\": \"vm_name==MV0628020\"
}" "https://10.26.1.227:9440/api/nutanix/v3/vms/list"
'''
'''
def get_vm_by_name(app,vmname):
    host      = app.config['NUTANIX_HOST']
    port      = app.config['NUTANIX_PORT']
    username  = app.config['NUTANIX_USERNAME']
    password  = app.config['NUTANIX_PASSWORD']
    protocol  = app.config['NUTANIX_PROTOCOL']
    endpoint  = f'api/nutanix/v3/vms/list{row.Task_uuid}'
    url       = f'{protocol}://{host}:{port}/{endpoint}'
    headers   = {'Accept':'application/json'}
    data     = {'kind':'vm','filter':f'vm_name=={vmname}'}
    # get Nutanix Response
    logger.warning(f'{this()}: url = {url} data={data}')
    
    response = api_request(    
                    'POST',
                    url,
                    data    =json.dumps(data),
                    headers =headers,
                    username=username,
                    password=password,
                    logger  = logger
                )
    logger.debug(f'{this()}: response = {response}')
    vms=None
    if response is not None:
        if response.ok:
            data=response.json()
            vms = data.get('entities')
    logger.warning(f'{this()}: vms = {vms}')
    return vms
'''

# EOF ******************************************************************
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
# ======================================================================
# BUTLER REQUEST TEMPLATES
# View for General request Edition
# (c) Sertechno 2020
# GLVH @ 2020-12-31 initial version
# GLVH @ 2021-03-20 adds support for 'other nics'
# Gerardo L Valera gvalera@emtecgroup.net
# ======================================================================
# src: view_request_templates.py

# Templates
# JavaScript/JQuery script templates

# Functions ------------------------------------------------------------
scr_function_subnets="""
// Updates Subnets options upon Selected project -----------------------
function subnets() {
    //window.alert("subnets(): IN" );            
    // GET UUID FOR CURRENT PROJECT, IMPORTANT ON ON CHANGE ... --------
    var project = $("#vmProject");
    var project_uuid = project.val();
    //window.alert( "project uuid: " + project_uuid );
    // POPULATE SUBNETS LIST FOR PROPER PROJECT, ON LINE ---------------
    var subnets = [];                
    {%- for project in subnet_options %}
        {%- if loop.index == 1 %}
            if (project_uuid == "{{project.0}}"){ subnets = {{project.1}}; }
        {%- else %}
            else if (project_uuid == "{{project.0}}"){ subnets = {{project.1}}; }
        {%- endif %}
    {%- endfor %}
    //window.alert( "subnets: " + subnets );
    // -----------------------------------------------------------------
    // SUBNETS OPTIONS INITIALIZATION ----------------------------
    // other nic cards may be empty ...
    //subnets.unshift(["",":"]);
    subnets.unshift(["",""]);
    {%- for i in range(4) %}
        var $nic{{i}} = $("#vmVlan{{i}}Name");    
        var nic_uuid = $nic{{i}}.val();
        $nic{{i}}.empty();
        $.each(subnets, function(index,[uuid,name]) {
            //window.alert("uuid="+uuid+" nic_uuid="+nic_uuid);
            if ( uuid == nic_uuid ) {
                $nic{{i}}.append("<option selected value='" + uuid + "'>" + name + "</option>");
            } else {
                $nic{{i}}.append("<option value='" + uuid + "'>" + name + "</option>");
            }
        });
    {%- endfor %}
    //subnet_names();
};
"""
scr_function_subnet_names="""
// Updates Subnets options upon Selected project -----------------------
function subnet_names() {
    //window.alert( "subnet_names(): IN" );            
    // GET UUID FOR CURRENT PROJECT, IMPORTANT ON ON CHANGE ... --------
    var project = $("#vmProject");
    var project_uuid = project.val();
    //window.alert( "subnet_names(): populate subnets" );            
    // POPULATE SUBNETS LIST FOR PROPER PROJECT, ON LINE ---------------
    var subnets = [];                
    var selected = [];
    // Sets projects's subnets arrays          
    {%- for project in subnet_options %}
        {%- if loop.index == 1 %}
    if (project_uuid == "{{project.0}}"){ subnets = {{project.1}}; }
        {%- else %}
    else if (project_uuid == "{{project.0}}"){ subnets = {{project.1}}; }
        {%- endif %}
    {%- endfor %}
    
    //window.alert( "subnet_names(): capture selected ..." );            
    // Capture selected uuids ------------------------------------------
    {%- for i in range(4) %}
        var $uid{{i}}  = $("#vmVlan{{i}}Uuid");    
        if ( document.getElementById("vmVlan{{i}}Selected").checked )  {
            selected.push( $uid{{i}}.val() );
        }
    {%- endfor %}

    //window.alert("selected = " + selected.length + " [" + selected+"]");
    //window.alert( "subnet_names(): reset subnets list ..." );            
    // RESET Subnets list ----------------------------------------------
    {%- for i in range(4) %}
        var $uid{{i}}  = $("#vmVlan{{i}}Uuid");    
        var $flag{{i}} = $("#vmVlan{{i}}Selected");    
        var $name{{i}} = $("#vmVlan{{i}}Name");  
        $uid{{i}}.val("<uuid>{{i}}");
        $name{{i}}.val("<name>{{i}}");
        //window.alert( "RESET Subnet {{i}}");
        // Load subnets data up to max or empty
        if ( {{i}} < subnets.length ) {
            $uid{{i}}.val(subnets[{{i}}][0]);
            $name{{i}}.val(subnets[{{i}}][1]);
            document.getElementById("vmVlan{{i}}Uuid").value = subnets[{{i}}][0];
            document.getElementById("vmVlan{{i}}Name").value = subnets[{{i}}][1];
            document.getElementById("vmVlan{{i}}Selected").disabled = false;
            if (selected.includes($uid{{i}}.val())) {
                document.getElementById("vmVlan{{i}}Selected").checked = true;
                document.getElementById("vmVlan{{i}}Selected").value = subnets[{{i}}][0];
            }
        } else {
            $uid{{i}}.val("");
            $name{{i}}.val("");
            document.getElementById("vmVlan{{i}}Selected").checked = false;
            document.getElementById("vmVlan{{i}}Selected").disabled = true;
        }
    {%- endfor %}
    /*
    window.alert(
        $uid0.val()+"|"+$name0.val()+"|"+document.getElementById("vmVlan0Selected").checked+" *** "+
        $uid1.val()+"|"+$name1.val()+"|"+document.getElementById("vmVlan1Selected").checked+" *** "+
        $uid2.val()+"|"+$name2.val()+"|"+document.getElementById("vmVlan2Selected").checked+" *** "+
        $uid3.val()+"|"+$name3.val()+"|"+document.getElementById("vmVlan3Selected").checked
    );
    */
    // window.alert("selected = " + selected.length + " " + selected);
      
    /*
    // -----------------------------------------------------------------
    // ALL SUBNETS OPTIONS INITIALIZATION ------------------------------
    {%- for i in range(4) %}
    var $uid{{i}}  = $("#vmVlan{{i}}Uuid");    
    var $flag{{i}} = $("#vmVlan{{i}}Selected");    
    var $name{{i}} = $("#vmVlan{{i}}Name");    
    var nic_uuid   = $uid{{i}}.val();
    $uid{{i}}.empty();
    document.getElementById('vmVlan{{i}}Selected').checked = false
    $name{{i}}.empty();
    $.each(selected, function(index,uuid) {
        if ( uuid == nic_uuid ) {
            document.getElementById('vmVlan{{i}}Selected').checked = true
        }
    });
    {%- endfor %}
    */
};
"""
scr_function_managements="""
function managements() {
    // GET Value FOR CURRENT Corporate, IMPORTANT ON ON CHANGE ... -----
    var $dropdown    = $("#vmCorporate");
    var corporate = $dropdown.val();
    // POPULATE "Gerencias" LIST FOR PROPER "Corporate", ON LINE -------
    var managements = [];                
    {%- for key in gd_map.keys() %}
    if (corporate == "{{gd_map[key].corporate}}"){managements.push([{{gd_map[key].code}},"{{gd_map[key].description}}"]);}
    {%- endfor %}
    // -----------------------------------------------------------------
    // PRIMARY Gerencias OPTIONS INITIALIZATION ------------------------    
    var $management = $("#vmDepartment");
    var olddepa=$management.val()
    $management.empty();    
    $.each(managements, function(index, [code,name]) {
        //window.alert("code="+code+" vs gerencia="+olddepa);
        //if ( code == $management.val() ) {
        if ( code == olddepa ) {
            $management.append("<option selected value='" + code + "'>" + name + "</option>");
        } else {
            $management.append("<option value='" + code + "'>" + name + "</option>");
        }
    });
    //window.alert("corp:"+corporate+" gerencias:"+managements+" old:"+olddepa);
};
"""
scr_function_get_storage="""
// Calculates total storage requested for provisioninig ----------------
function get_storage() {
    //window.alert( "get_storage(): IN" );            
    var storage = 0;
    var size    = 0;
    {%- for i in range(12) %}
    size = parseInt($("#vmDisk{{i}}Size").val(),10); if ( ! isNaN(size) ) {storage = storage + size}; 
    {%- endfor %}
    return storage ;
};
"""
scr_function_summary="""
// Summarize VM requirements -------------------------------------------
// Also recalculates expected monthly rate as per VM configuration
function summary() {
    try {
        var cps         = $("#vmCPS").val();
        var sockets     = $("#vmSockets").val();
        var ram         = $("#vmRAM").val();
        var cores       = cps * sockets;
        var storage     = get_storage();
        
        var topcc       = parseInt($("#vmTopCC").val());
        var corporate   = parseInt($("#vmCorporate").val())  - topcc;
        var department  = parseInt($("#vmDepartment").val()) - topcc - corporate;
        var environment = parseInt($("#vmCC").val())         - topcc;                
        var type        = parseInt($("#vmType").val())       - topcc;
        var cc          = topcc + corporate + department + environment + type;                
        $("#vmResume").val(cores + " CPU x " + ram + " GB RAM x " + storage + " GB");
        $("#vmMonth").val(get_month().toFixed(6) + " UF => " + cc);
        $("#vmMessage1").val(cores + " CPU x " + ram + " GB RAM x " + storage + " GB " + topcc + "+" + corporate + "+" + department + "+" + environment + "+" + type + "=" + cc );
        return $("#vmResume").val();
    } catch (e) {
        window.alert(e.name + ': ' + e.message);
    }
};
"""
scr_function_get_rate="""
// Look for proper rate upon cost center specification or default ------
function get_rate(type,cc) {
    //window.alert( "get_rate() IN type= "+type+" cc= "+cc  );            
    var rateid      = '' ;
    var ratedefault = '' ;
    var rate        = 0  ;
    var rateid      = 0  ;
    var ratedefault = 0 ;
    var Rates = [
    {%- for r in rates %}
        ["{{r}}",{{"%.24f"|format(rates[r])}}],
    {%- endfor %}
    ];
    
    // looks for specific rate code for CC
    for (r=0;r<Rates.length;r++){
        rateid      = type + ':' + cc ;
        if ( Rates[r][0] == rateid) {
            rate = Rates[r][1]; 
            break;
        }
    }
    if (rate == 0){
        // If specific rate not found then look for default rate
        for (r=0;r<Rates.length;r++){
            rateid = type + ':' + '1' ;
            if ( Rates[r][0] == rateid) {
                rate = Rates[r][1]; 
                break;
            }
        }
    }
    //window.alert( "get_rate() returns for " + type + ":" + cc + " rateid = " + rateid + " rate = "+rate  );            
    $("#vmMessage3").val("get_rate() returns for " + type + ":" + cc + " rateid = " + rateid + " rate = "+rate);
    return rate;
};
"""
scr_function_get_month="""
// Calculates expected monthy rate upon VM configuration ---------------
function get_month() {
    //window.alert( "get_month() IN" );            
    var cps          = $("#vmCPS").val();
    var sockets      = $("#vmSockets").val();
    var ram          = $("#vmRAM").val();
    var cores        = cps * sockets;
    var storage      = get_storage();
    // Will build actual detail level CC from components ---------------
    var topcc        = parseInt($("#vmTopCC").val());
    var corporate    = parseInt($("#vmCorporate").val())  - topcc;
    var management   = parseInt($("#vmDepartment").val()) - topcc - corporate;
    var environment  = parseInt($("#vmCC").val())         - topcc;                
    var disk_type    = parseInt($("#vmType").val())       - topcc;
    var cc           = topcc + corporate + management + environment + disk_type;                
    // Get actual rates ------------------------------------------------
    var rate_ram     = get_rate('RAM',cc);
    var rate_cores   = get_rate('CPU',cc);
    var rate_storage = get_rate('DSK',cc);                
    $("#vmMessage1").val("cc: " + cc +" ram: " + rate_ram + " cpu: " + rate_cores + " dsk: " + rate_storage);
    var month = cores * rate_cores + ram * rate_ram + storage * rate_storage ;
    $("#vmMessage2").val(cores+"*"+rate_cores+ "+" + ram+"*"+rate_ram+ "+" +storage+"*"+rate_storage+ " = "+month);
    return month ;
};        
"""
scr_function_load="""
// document ON LOAD event setup function -------------------------------
function load() {
    //window.alert( "load() IN" );            
    managements();
    set_attributes();
    subnets();
    //subnet_names();
    summary();
};
// ---------------------------------------------------------------------
"""

# Script functions templates array (script order is significative)
scr_functions_template="\n".join([
    scr_function_subnets,
    scr_function_subnet_names,
    scr_function_managements,
    scr_function_get_storage,
    scr_function_summary,
    scr_function_get_rate,
    scr_function_get_month,
    scr_function_load
    ])

# Request events functions ---------------------------------------------
scr_project_change="""
// Project change event ------------------------------------------------ 
$("#vmProject").on('change',function() {
    //window.alert( "vmProject.on.change(): IN" );            
    var key = $("#vmProject").val();
    var vals = [];                
    {%- for project in subnet_options %}
    if (key == "{{project.0}}"){
         vals =  {{project.1}};
    }
    {%- endfor %}
    //subnets();
    subnet_names();
});

$("#vmProjectName").on('change',function() {
    window.alert( "vmProjectName.on.change(): IN" );            
    var key = $("#vmProject").val();
    var vals = [];                
    {%- for project in subnet_options %}
    if (key == "{{project.0}}"){
         vals =  {{project.1}};
    }
    {%- endfor %}
    //subnets();
    subnet_names();
});
"""
scr_corporate_change="""
// Corporate change event ---------------------------------------------- 
$("#vmCorporate").on('change',function() {
    //window.alert( "#vmProject".on.change(): IN" );            
    var $dropdown = $(this);
    var key = $dropdown.val();
    var vals = [];                
    {%- for corporate in corporate_options %}
    if (key == "{{corporate.0}}"){
         vals =  {{corporate.1}};
    }
    {%- endfor %}
    managements();
    summary();
});
"""
scr_set_attributes="""
// sets Project and Category depending on Environment and Cluster ------
function set_attributes() {
    var environment = $("#vmCC").val();
    var cluster     = $("#vmCluster").val();
    var envid       = environment + ':' + cluster ;
    
    var envs = [
    {%- for e in environments_codes %}
        {%- for c in environments_codes[e] %}
        ["{{e}}:{{c}}","{{environments_codes[e][c]['project']}}","{{environments_codes[e][c]['category']}}","{{environments_codes[e][c]['project_name']}}","{{environments_codes[e][c]['category_description']}}"],
        {%- endfor %}
    {%- endfor %}
    ];
    
    // searchs specific environment:cluster pair for Project & Category
    //window.alert( "env id: " + envid + " len= " + envs.length );            
    for (e=0;e<envs.length;e++){
        //window.alert( "env" + e + ": " + envs[e][0] + envs[e][1] + envs[e][3] );            
        if ( envs[e][0] == envid) {
            //window.alert( "match env" + e + ": " + envs[e][0] + " " + envs[e][1] + " " + envs[e][3] );            
            //vmProject.val(envs[e][1]);
            $("#vmProject").val(envs[e][1]);
            $("#vmCategory").val(envs[e][2]);
            $("#vmProjectName").val(envs[e][3]);
            $("#vmCategoryName").val(envs[e][4]);
            break;
        }
    }
    //window.alert( "project: " + vmProject.val() + " " + vmProjectName.val()  );            

    //window.alert( "callig subnets ..."  );            
    //window.alert( "project: " + $("#vmProject").val() + " " + $("#vmProjectName").val()  );            
    
    $("#vmMessage4").val("project: " + $("#vmProject").val() + " " + $("#vmProjectName").val());

    subnets();
    //window.alert( "set attributes callig subnet_namess ..."  );            
    //subnet_names();
    return;           
};
"""
scr_cc_change="""
// Environment change event -------------------------------------------- 
$("#vmCC").on('change',function() {
    set_attributes();
    summary();
});
"""
scr_cluster_change="""
// Cluster change event ------------------------------------------------ 
$("#vmCluster").on('change',function() {
    set_attributes();
    summary();
});
"""
# Script templates array (script order is significative)
scr_request_template="\n".join([
    scr_project_change,
    scr_corporate_change,
    scr_set_attributes,
    scr_cc_change,
    scr_cluster_change
])
# Other templates ------------------------------------------------------
scr_cpu_template="""
// Cores per socket change event handler -------------------------------
$("#vmCPS").on('change',function() {
    //window.alert( "#vmCPS".on.change(): IN" );            
    var $vmCPS     = $(this);
    var $vmSockets = $("#vmSockets");
    var cps        = $vmCPS.val();
    var sockets    = $vmSockets.val();
    var cores      = cps * sockets;
    var $cpu       = $("#vmCPU");
    $cpu.val(cores);
    $cpu.text(cores);
    summary();
});
// Sockets change event handler ----------------------------------------
$("#vmSockets").on('change',function() {
    //window.alert( "#vmSockets".on.change(): IN" );            
    var $vmCPS     = $("#vmCPS");
    var $vmSockets = $(this);
    var cps        = $vmCPS.val();
    var sockets    = $vmSockets.val();
    var cores      = cps * sockets;
    var $cpu       = $("#vmCPU");
    $cpu.val(cores);
    $cpu.text(cores);
    summary();
});
"""
scr_storage_template="""
// Disk Image change event handler -------------------------------------
function check_image_size(i) {            
    //window.alert( "check_image_size("+i+") IN"   );            
    var Size     = $("#vmDisk"+i+"Size");            
    var Selected = $("#vmDisk"+i+"Image option:selected"    );
    //window.alert("Size="+Size.val()+ " Selected="+Selected.val());
    var imagesize = 0;
    var tokens = $(Selected).text().split("("); 
    var token1 = tokens[1].split(" "); 
    imagesize = parseInt(token1[0],10);
    if (parseInt(Size.val(),10) < imagesize){
        Size.val(imagesize);
        i = i + 1;
        window.alert( "Tamaño de disco " + i + " será expandido según requerimiento de imagen: " + $(Selected).text());
    }
    summary();
};
// Disk size change event handler --------------------------------------
function check_disk_size(i){
    //window.alert( "check_disk_size("+i+") IN"   );            
    var Image = $("#vmDisk"+i+"Image");
    if (i == 0){
        if ( ! Image.val() == "" ){
            check_image_size(i);
        }
    }
    summary();
};
"""

scr_events_template="""
// Configuration fields change event handlers --------------------------
$("#vmDebug").on('change',function() {window.alert( "#vmDebug.on.change(): IN" );window.repaint();});
$("#vmRAM").on( 'change' , function(){summary();} );
$("#vmDepartment").on( 'change' , function(){summary();} );
$("#vmCC").on( 'change' , function(){summary();} );
$("#vmType").on( 'change' , function(){summary();} );
{%- for i in range(12) %}
$("#vmDisk{{i}}Size").on('change',function(){check_disk_size({{i}});});
{%- if i == 0 %}
$("#vmDisk{{i}}Image").on('change',function(){check_image_size({{i}});});
{%- endif %}
{%- endfor %}
// document ON LOAD event setup ----------------------------------------
window.onload = load();
// ---------------------------------------------------------------------
"""
scr_help_template="""
function help(obj) {
    window.alert("Help IN obj="+obj);
    var Help = $("#vmHelp");
    var msg  = "";
    if      (obj=='vmName'){msg="Este es el nombre único de la MV";}
    else if (obj=='vmCPS') {msg="Número de CPU cores por socket";}
    window.alert("Help msg="+msg);
    $Help.val (msg);            
    $Help.text(msg);            
};
$("#vmName").on("click",help("vmName"));
$("#vmCPS").mouseover (help("vmCPS" ));
"""

# Scripts array (script order is significative)
Script_Templates = [
    scr_functions_template,
    scr_storage_template,
    scr_request_template,
    scr_cpu_template,
    scr_events_template,
]
# EOF ******************************************************************
