# ======================================================================
# Main Views Header
# source file name: EG-Butler-Tools/code/src/views_butler_api_py_header.py
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
from emtec.api                          import *

from markdown import markdown
from markdown import markdownFromFile
