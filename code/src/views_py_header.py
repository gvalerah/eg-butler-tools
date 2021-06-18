# ======================================================================
# Main Views Header
# source file name: views_py_header.py
# Static Header File. 
# GLVH 2020-10-11
# ----------------------------------------------------------------------
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

from .              import main

from ..             import db
from ..             import mail
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

""" Application decorators for routes """
""" Decorators specify main routes to be handled by Butler Solution """

@main.route('/', methods=['GET', 'POST'])
def index():
    logger.debug(f"@main.route('/', methods=['GET', 'POST'])")
    try: logger.debug(f'current_user={current_user}')
    except Exception as e: logger.debug(f'exception={str(e)}')
    # Espera a capitulo 3 para mejorar procedimiento de respuesta, hard coding mucho aqui
    
    # Aqui debo setear el ambiente de variables de periodo -------------
    try:
        Period = get_period_data(current_user.id,db.engine,Interface)
    except:
        Period = get_period_data()
    logger.debug(f"Period={Period}")    
    # ------------------------------------------------------------------
    # Setup all data to render in template
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

@main.route('/under_construction', methods=['GET','POST'])
def under_construction():   
    return render_template('under_construction.html')

@main.route('/demo', methods=['GET','POST'])
def demo():   
    return render_template('demo.html')

@main.route('/test_index', methods=['GET', 'POST'])
def test_index():
    
    # Espera a capitulo 3 para mejorar procedimiento de respuesta, hard coding mucho aqui

    if logger is not None:
        logger.debug("index() IN")
    else:
        print("*** WARNING *** Route: test_index: logger is undefined. !!! No logging functions possible. !!!")

    data =  {   "name":current_app.name,
                "app_name":C.app_name,
                "date_time":strftime('%Y-%m-%d %H:%M:%S'),
                "user_agent":request.headers.get('User-Agent'),
                "current_time":datetime.utcnow(),
                "db":db,
                "logger":logger,
                "C":C,
                "C.db":C.db,
                "C.logger":C.logger,
                "current_app":current_app,
                "current_app_dir":dir(current_app),
                "current_app_app_context":current_app.app_context(),
                "current_app_app_context DIR":dir(current_app.app_context()),
                }
    name = None
    password = None
    form = NameForm()

    return render_template('test.html',data=data, name=name,password=password, form=form)

from markdown import markdown
from markdown import markdownFromFile

@main.route('/butler_faq', methods=['GET','POST'])
def butler_faq():   
    main_page_md   = f'{current_app.template_folder}/butler_main.md'
    main_page_html = f'{current_app.template_folder}/butler_main.html'
    markdownFromFile(
        input=main_page_md,
        output=main_page_html,
        encoding='utf8',
        extensions=['tables']
        )
    return render_template('butler_faq.html')

@main.route('/butler_about', methods=['GET','POST'])
def butler_about():   
    return render_template('butler_about.html')

# ----------------------------------------------------------------------
