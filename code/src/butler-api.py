#!/usr/bin/env python

# ----------------------------------------------------------------------
# Top level required definitions
# ----------------------------------------------------------------------
import  os
import  sys
import  getpass
from    pprint              import pprint
from    flask_script        import Manager, Shell
from    flask_migrate       import Migrate, MigrateCommand
#rom    flask_mail          import Message

import  configparser
from    configparser        import ConfigParser, ExtendedInterpolation
from    sqlalchemy          import create_engine
# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
# G Unicorn required definitions
# ----------------------------------------------------------------------
import  multiprocessing
import  gunicorn
from    gunicorn.app.base   import Application, Config
from    gunicorn            import glogging
from    gunicorn.workers    import sync

def number_of_workers():
    return (multiprocessing.cpu_count() * 2) + 1

class GUnicornFlaskApplication(Application):
    def __init__(self, app):
        self.usage, self.callable, self.prog, self.app = None, None, None, app

    def run(self, **options):
        self.cfg = Config()
        [self.cfg.set(key, value) for key, value in options.items()]
        return Application.run(self)

    load = lambda self:self.app
# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
# Emtec group required definitions
# ----------------------------------------------------------------------

from    emtec.common.functions             import *
from    emtec.butler.common.context     import Context
#from    emtec.collector.common.functions   import *
# ----------------------------------------------------------------------

# Setup context data depending on configuration file

# Macro level default values
config_file = "butler.ini"
run_mode    = 'GUNICORN'

if len(sys.argv) < 2:
    print()
    print(f'Usage is: {sys.argv[0]} <config file> [FLASK|GUNICORN]')
    print()
    sys.exit(1)
            
command     = sys.argv[0]
config_file = sys.argv[1]

if len(sys.argv) > 2:        
    run_mode=sys.argv[2]

if (os.path.isfile(config_file)):
        config_ini = configparser.ConfigParser(interpolation=ExtendedInterpolation())
        #config_ini.read( config_file )                 # GV 20210315     
        config_ini.read_file( open(config_file) )  # GV 20210315      
        run_mode      = config_ini.getint('General','run_mode'     ,fallback=run_mode)
        flask_host    = config_ini.getint('General','flask_host'   ,fallback='0.0.0.0')
        flask_port    = config_ini.getint('General','flask_port'   ,fallback=5200)
        gunicorn_host = config_ini.getint('General','gunicorn_host',fallback='0.0.0.0')
        gunicorn_port = config_ini.getint('General','gunicorn_port',fallback=8200)
else:
    sys.exit(1)

# **********************************************************************
# SPECIFIC APPLICATION FOLDER DIFFERS FROM APPLICATIONS
#from    api                 import create_app,db,mail,logger
from    api                 import create_app,db,logger
# **********************************************************************
C = Context("Butler API",config_file,logger)
C.Set()

app     = create_app(config_file,os.getenv('BUTLER_CONFIG') or 'production', C)


# CONFIGURATION PATCH !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

logger.name="Butler API"
# Setup logger handlers
# Actual File system all logger ----------------------------------------
file_handler=add_Logging_Handler(
    logger=logger,
    level=C.log_level,
    folder=C.log_folder,
    nameFormat="%s.log"%logger.name.replace(' ','_'),
    handlerType='TIME_ROTATING'
    )
# Default File logger filters (omits) AUDIT records, then an audit
# logger needs to be defined
file_handler.addFilter(LevelFilter(logging.AUDIT))
# ----------------------------------------------------------------------

# Specialized AUDIT LOG logger -----------------------------------------
audit_handler=add_Logging_Handler(
    logger=logger,
    level=logging.AUDIT,
    folder=C.log_folder,
    nameFormat="%s.aud"%logger.name.replace(' ','_'),
    handlerType='TIME_ROTATING'
    )
# ----------------------------------------------------------------------

if __name__ == '__main__':
    app_ctx = app.app_context()
    app_ctx.push()
    
    logger.setLevel(C.log_level)
    db.logger = logger
    
    
    if logger is not None:
        db.logger = logger
        logger.info("****** Butler API Server ****************")
        logger.info(" * %s: as '%s' Using configuration: '%s'"%
            (sys.argv[0],getpass.getuser(),config_file))
        logger.info(" * %s: db connection is '%s'"%(sys.argv[0],db))
        logger.info("*****************************************")
        for variable in os.environ:
            logger.debug("%s=%s"%(variable,os.environ.get(variable)))
        logger.debug("logger                = %s"%logger)
        #ogger.debug("mail                  = %s"%mail)
        logger.debug("db                    = %s"%db)
        logger.debug("db.logger             = %s"%db.logger)
        logger.debug("app                   = %s"%app)
        logger.debug("app.root_path         = %s"%app.root_path)
        logger.debug("app.static_folder     = %s"%app.static_folder)
        logger.debug("app.template_folder 1 = %s"%app.template_folder)
        app.template_folder="%s/templates"%(app.root_path)
        logger.debug("app.template_folder 2 = %s"%app.template_folder)
        for key in app.config.keys():
            if key == key.upper():
                logger.debug("%-40s = %s"%(key,app.config[key]))
        logger.debug("%-40s = %s"%("app.root_path",app.root_path))

        logger.info("*****************************************")
        print("****** Butler API Server *************")
        print(" * %s: as '%s' Using configuration: '%s'"%
            (sys.argv[0],getpass.getuser(),config_file))
        print(" * %s: db connection is '%s'"%(sys.argv[0],db))
        print(" * logger is %s"%(logger))
        if logger.getEffectiveLevel() < logging.INFO:
            print("*** logger.handlers are :"%logger.handlers)        
            for h in logger.handlers:
                print("    handler",h,id(h))
                print("      format",h.format,id(h.format))
                print("      formatter",h.formatter,id(h.formatter))
                print("      filter",h.filter,id(h.filter))
                print("      filters",h.filters,id(h.filters))
                print('      name',h.name,'level',h.level,'mode',h.mode)
        logger.trace    ("trace Init butler API Server Execution")
        logger.debug    ("debug Init butler API Server Execution")
        logger.info     ("info Init butler API Server Execution")
        logger.warning  ("warning Init butler API Server Execution")
        logger.error    ("error Init butler API Server Execution")
        logger.critical ("critical Init butler API Server Execution")
        logger.audit    ("audit Init butler API Server Execution")
        logger.trace("os.environ=%s"%os.environ)
        logger.trace("app.config=%s"%app.config)
        logger.info("*****************************************")
        print("*****************************************")
    else:
        print("****************************************")
        print("**** WARNING **** No logger defined ****")
        print("****************************************")

    print(" * Will execute app here")   
    # 20200217 LOCATION OPORTINITY CHANGE DUE TO CONFIG ISSUES
    from    emtec.butler.db.flask_models    import User
    from    emtec.butler.db.flask_models    import Role

    # Will be replaced by embedded Green Unicorn HTTP Server
    if run_mode == 'FLASK':
        print(" * Running in Flask app mode")
        app.run(host=flask_host,port=flask_port)
    else:
        options = {
            'bind': '%s:%s' % (gunicorn_host, gunicorn_port),
            'workers': number_of_workers(),
            'worker_class':"gunicorn.workers.sync.SyncWorker",
        }
        print(" * Running in Green Unicorn powered mode")
        logger.debug("Application CPUs   = %s" % multiprocessing.cpu_count())
        logger.debug("Application options= %s" % options)
        logger.debug("Application Flask  = %s" % app)
        gunicorn_app = GUnicornFlaskApplication(app)
        gunicorn_app.run(
            **options
        )

