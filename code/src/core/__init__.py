# ======================================================================
# Module app initialization file
# Application Package constructor
# source file name: __init__.py
# Static Header File. 
# GLVH 2020-11-23
# ----------------------------------------------------------------------
from pprint         import pprint,pformat
from requests.auth  import HTTPBasicAuth   
from requests.auth  import HTTPDigestAuth
import base64

import  logging
from    configparser                    import ConfigParser
from    configparser                    import ExtendedInterpolation

from    flask                           import Flask, render_template
from    flask_bootstrap                 import Bootstrap
from    flask_mail                      import Mail
from    flask_mail                      import Message
from    flask_moment                    import Moment
from    flask_sqlalchemy                import SQLAlchemy
from    flask_login                     import LoginManager

from    emtec.common.functions          import *
from    emtec.butler.common.context     import Context
# required if specific SQLAlchemy class is required , see below
from    emtec.butler.db.orm_model       import *

import re

mail                                = Mail()
db                                  = SQLAlchemy()
#login_manager                       = LoginManager()

# Setup Login manager
#login_manager.session_protection    = 'strong'
#login_manager.login_view            = 'auth.login'

# create logger logger
add_Logging_Levels()
logger                              = logging.getLogger('Butler-CORE')

def create_app(config_file='butler.ini',config_name='production',C=None):
    config_ini = ConfigParser(interpolation=ExtendedInterpolation())
    config_ini.read( config_file )
    
    app = Flask(__name__,root_path='%s/core'%C.app_folder)
    # Calls configuration Manager
    # setup all driver specifics here
    rdbms=config_ini.get('DB','rdbms',fallback='mysql')
    dialect=config_ini.get('DB','dialect',fallback='pymysql')
    if dialect is not None and len(dialect)>0:
        driver="%s+%s"%(rdbms,dialect)
    else:
        driver=rdbms
    # setup engine specifics
    if rdbms == 'mysql':
        charset=config_ini.get('DB','charset',fallback=None)
        if charset is not None:
            charset='?charset=%s'%str(charset)
        else:
            charset=''
    else:
        charset=''
    # setup full connection engine here
    DATABASE_URL = "%s://%s:%s@%s:%s/%s%s"%(
            config_ini.get('DB','driver',   fallback=driver),
            config_ini.get('DB','user',     ),
            config_ini.get('DB','password', ),
            config_ini.get('DB','host',     fallback='localhost'),
            config_ini.get('DB','port',     fallback=3306),
            config_ini.get('DB','schema',   fallback='butler'),
            charset
            )
    # Butler app config variables here
    app.config.update({'BUTLER_CONFIG_FILE':           config_file})
    app.config.update({'app_home':                     config_ini.get       ('General','app_home')})
    app.config.update({'app_folder':                   config_ini.get       ('General','app_folder')})
    app.config.update({'BUTLER_MAIL_SUBJECT_PREFIX':   config_ini.get       ('General','BUTLER_MAIL_SUBJECT_PREFIX',fallback='[EG Butler]')})
    #pp.config.update({'BUTLER_MAIL_SENDER':           config_ini.get       ('General','BUTLER_MAIL_SENDER',fallback='Butler Admin <gvalera@emtecgroup.net>')})
    app.config.update({'BUTLER_MAIL_SENDER':           config_ini.get       ('General','BUTLER_MAIL_SENDER',fallback='Butler Admin')})
    app.config.update({'BUTLER_ADMIN':                 config_ini.get       ('General','BUTLER_ADMIN',fallback='butler')})
    app.config.update({'BUTLER_CIT_SHARDING':          config_ini.getboolean('General','BUTLER_CIT_SHARDING',fallback=False)})
    app.config.update({'BUTLER_TOP_COST_CENTER':       config_ini.get       ('General','BUTLER_TOP_COST_CENTER',fallback='BUTLER')})
    app.config.update({'BUTLER_REQUEST_NOTIFICATIONS': config_ini.getboolean('General','BUTLER_REQUEST_NOTIFICATIONS',fallback=False)})
    # default app config settings
    app.config.update({'NAME':                          config_ini.get       ('General','NAME',fallback='Butler')})
    app.config.update({'SECRET_KEY':                    config_ini.get       ('General','SECRET_KEY',fallback='Hard to guess string')})
    app.config.update({'SQLALCHEMY_DATABASE_URI':       DATABASE_URL})
    app.config.update({'SQLALCHEMY_COMMIT_ON_TEARDOWN': config_ini.getboolean('General','SQLALCHEMY_COMMIT_ON_TEARDOWN',fallback=True)})
    app.config.update({'SQLALCHEMY_TRACK_MODIFICATIONS':config_ini.getboolean('General','SQLALCHEMY_TRACK_MODIFICATIONS',fallback=False)})
    app.config.update({'MAIL_SERVER':                   config_ini.get       ('General','MAIL_SERVER',fallback='localhost')})
    app.config.update({'MAIL_PORT':                     config_ini.get       ('General','MAIL_PORT',fallback=25)})
    app.config.update({'MAIL_USE_TLS':                  config_ini.getboolean('General','MAIL_USE_TLS',fallback=False)})
    app.config.update({'MAIL_USE_SSL':                  config_ini.getboolean('General','MAIL_USE_SSL',fallback=False)})
    app.config.update({'MAIL_USERNAME':                 config_ini.get       ('General','MAIL_USERNAME',fallback=None)})
    app.config.update({'MAIL_PASSWORD':                 config_ini.get       ('General','MAIL_PASSWORD',fallback=None)})
    app.config.update({'LINES_PER_PAGE':                config_ini.getint    ('General','LINES_PER_PAGE',fallback=5)})
    app.config.update({'DEBUG':                         config_ini.getboolean('General','DEBUG',fallback=False)})
    app.config.update({'TESTING':                       config_ini.getboolean('General','TESTING',fallback=False)})
    app.config.update({'WTF_CSRF_ENABLED':              config_ini.getboolean('General','WTF_CSRF_ENABLED',fallback=False)})
    # Force no caching of FLASK JS CSS files & Updates -----------------
    app.config.update({'SEND_FILE_MAX_AGE_DEFAULT':     0})
    app.config.update({'API_USERS':                     config_ini.get       ('API'    ,'USERS',fallback='butler:butler')})
    temp_API_Users = app.config['API_USERS'].split(',')
    API_Users= []
    for userpass in temp_API_Users:
        API_Users.append(f'Basic {base64.b64encode(userpass.encode()).decode()}')
    app.config['API_USERS'] = API_Users
    #pprint(app.config['API_USERS'])
    # CORE Daemon Configuration ----------------------------------------
    #pprint(app.config)
    #print("CORE ****************")
    try:
        #print(f'config_ini.sections()={config_ini.sections()}')
        if 'Daemon' in config_ini.sections():
            #print(f"config_ini.options(Daemon)={config_ini.options('Daemon')}")
            options = config_ini.options('Daemon')
            # Load Daemon Transaction flags
            for option in options:
                if option[:3].lower() == 'trx':
                    app.config.update({option.upper():config_ini.getboolean('Daemon',option,fallback=True)})
            # Must have keys
            app.config.update({'CORE_POOL_SECONDS':             config_ini.getint    ('Daemon'    ,'Pool_Seconds',fallback=59)})
        else:
            print(f"{this()}: No 'Daemon' section found in {config_file}")            
    except Exception as e:
        print(f'{this()}: exception = {str(e)}')

    #pprint(app.config)
    #print("CORE ****************")

    # Butler app config variables here
    app.config.update({'API_HOST'    :   config_ini.get    ('API','HOST'    ,fallback='localhost')})
    app.config.update({'API_PORT'    :   config_ini.getint ('API','PORT'    ,fallback=5100       )})
    app.config.update({'API_USERNAME':   config_ini.get    ('API','USERNAME',fallback='collector')})
    app.config.update({'API_PASSWORD':   config_ini.get    ('API','PASSWORD',fallback=None       )})
    app.config.update({'API_PROTOCOL':   config_ini.get    ('API','PROTOCOL',fallback='http'     )})

    app.config.update({'COLLECTOR_HOST'    :   config_ini.get    ('Collector','HOST'    ,fallback='localhost')})
    app.config.update({'COLLECTOR_PORT'    :   config_ini.getint ('Collector','PORT'    ,fallback=8000       )})
    app.config.update({'COLLECTOR_USERNAME':   config_ini.get    ('Collector','USERNAME',fallback='collector')})
    app.config.update({'COLLECTOR_PASSWORD':   config_ini.get    ('Collector','PASSWORD',fallback=None       )})
    app.config.update({'COLLECTOR_PROTOCOL':   config_ini.get    ('Collector','PROTOCOL',fallback='http'     )})

    app.config.update({'MONITOR_HOST'      :   config_ini.get    ('Monitor'  ,'HOST'    ,fallback='localhost')})
    app.config.update({'MONITOR_PORT'      :   config_ini.getint ('Monitor'  ,'PORT'    ,fallback=5665       )})
    app.config.update({'MONITOR_USERNAME'  :   config_ini.get    ('Monitor'  ,'USERNAME',fallback='collector')})
    app.config.update({'MONITOR_PASSWORD'  :   config_ini.get    ('Monitor'  ,'PASSWORD',fallback=None       )})
    app.config.update({'MONITOR_PROTOCOL'  :   config_ini.get    ('Monitor'  ,'PROTOCOL',fallback='http'     )})

    app.config.update({'NUTANIX_HOST'      :   config_ini.get    ('Nutanix'  ,'HOST'    ,fallback='localhost')})
    app.config.update({'NUTANIX_PORT'      :   config_ini.getint ('Nutanix'  ,'PORT'    ,fallback=9440       )})
    app.config.update({'NUTANIX_USERNAME'  :   config_ini.get    ('Nutanix'  ,'USERNAME',fallback='collector')})
    app.config.update({'NUTANIX_PASSWORD'  :   config_ini.get    ('Nutanix'  ,'PASSWORD',fallback=None       )})
    app.config.update({'NUTANIX_PROTOCOL'  :   config_ini.get    ('Nutanix'  ,'PROTOCOL',fallback='https'    )})
    app.config.update({'NUTANIX_PROJECT'   :   config_ini.get    ('Nutanix'  ,'PROJECT' ,fallback='Butler'   )})
    app.config.update({'NUTANIX_PROJECT_UUID': config_ini.get    ('Nutanix'  ,'PROJECT_UUID' ,fallback=None  )})
    app.config.update({'NUTANIX_TIMEOUT'   :   config_ini.getint ('Nutanix'  ,'TIMEOUT' ,fallback=5  )})
    app.config.update({'NUTANIX_IMAGE_NAME':   config_ini.get    ('Nutanix'  ,'IMAGE_NAME' ,fallback=None  )})
    app.config.update({'NUTANIX_LOCAL_SCHEDULE_TYPE'        : config_ini.get   ('Nutanix','LOCAL_SCHEDULE_TYPE'        ,fallback=None )})
    app.config.update({'NUTANIX_LOCAL_EVERY_NTH'            : config_ini.getint('Nutanix','LOCAL_EVERY_NTH'            ,fallback=0    )})
    app.config.update({'NUTANIX_LOCAL_LOCAL_MAX_SNAPSHOTS'  : config_ini.getint('Nutanix','LOCAL_LOCAL_MAX_SNAPSHOTS'  ,fallback=0    )})
    app.config.update({'NUTANIX_LOCAL_REMOTE_MAX_SNAPSHOTS' : config_ini.getint('Nutanix','LOCAL_REMOTE_MAX_SNAPSHOTS' ,fallback=0    )})
    app.config.update({'NUTANIX_REMOTE_SCHEDULE_TYPE'       : config_ini.get   ('Nutanix','REMOTE_SCHEDULE_TYPE'       ,fallback=None )})
    app.config.update({'NUTANIX_REMOTE_EVERY_NTH'           : config_ini.getint('Nutanix','REMOTE_EVERY_NTH'           ,fallback=0    )})
    app.config.update({'NUTANIX_REMOTE_LOCAL_MAX_SNAPSHOTS' : config_ini.getint('Nutanix','REMOTE_LOCAL_MAX_SNAPSHOTS' ,fallback=0    )})
    app.config.update({'NUTANIX_REMOTE_REMOTE_MAX_SNAPSHOTS': config_ini.getint('Nutanix','REMOTE_REMOTE_MAX_SNAPSHOTS',fallback=0    )})
    
    # get all keys in General Section
    # this lets setup app config variable without
    # modifying this initialization code
    # if key is not in app.config then its appended
    all_keys = dict(config_ini.items('General'))
    for key in all_keys:
        if re.match("^butler_.*$",key) is not None:
            if key.upper() not in app.config.keys():
                app.config.update({key.upper():config_ini.get('General',key)})

    if app.config['DEBUG']:
        print("create_app: %-40s = %s"%("name",__name__))
        print("create_app: %-40s = %s"%("config_file",config_file))
        print("create_app: %-40s = %s"%("config_name",config_name))
        print("create_app: %-40s = %s"%("C",C))
        print("create_app: %-40s = %s"%("C.app_folder",C.app_folder))
        print("create_app: %-40s = %s"%("config_ini",config_ini))
        for key in app.config.keys():
            if key == key.upper() or True:
                print("create_app: %-40s = %s"%(key,app.config[key]))
        print("%-40s = %s"%("create_app: app.root_path",app.root_path))

    #sys.exit(1)
    
    # Inititializes applications (incomplete by now)
    #bootstrap.init_app      (app)
    mail.init_app           (app)
    #moment.init_app         (app)
    db.init_app             (app)
    #login_manager.init_app  (app)
    # Butler's modules
    
    # attach routes and custom error pages here
    """
    from api.main   import main as main_blueprint          # NOTE: Example talks on main here .main was required . (Why?)
    app.register_blueprint(main_blueprint)
    
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    """
    print(f'app={app}')
    print(f'db={db}')
    print(f'mail={mail}')
    #print(f'main_blueprint={main_blueprint}')
    #print(f'auth_blueprint={auth_blueprint}')

    return app
    
# ----------------------------------------------------------------------
