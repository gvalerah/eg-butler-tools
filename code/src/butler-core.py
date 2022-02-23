#!/usr/bin/env python

# 20210523 GLVH QA and refactoring
# ----------------------------------------------------------------------
# Top level required definitions
# ----------------------------------------------------------------------
import  os
import  sys
import  getpass
from    pprint              import pprint
from    flask_script        import Manager, Shell
from    flask_migrate       import Migrate, MigrateCommand

import  configparser
from    configparser        import ConfigParser, ExtendedInterpolation
from    sqlalchemy          import create_engine
# ----------------------------------------------------------------------
# Emtec group required definitions
# ----------------------------------------------------------------------
from    emtec.common.functions      import *
from    emtec.butler.common.context import Context
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
        config_ini.read( config_file )        
        run_mode      = config_ini.getint('General','run_mode'     ,fallback=run_mode)
        flask_host    = config_ini.getint('General','core_flask_host'   ,fallback='0.0.0.0')
        flask_port    = config_ini.getint('General','core_flask_port'   ,fallback=5300)
        gunicorn_host = config_ini.getint('General','core_gunicorn_host',fallback='0.0.0.0')
        gunicorn_port = config_ini.getint('General','core_gunicorn_port',fallback=8300)
        log_when      = config_ini.get   ('General','log_when'     ,fallback='D')
        log_interval  = config_ini.getint('General','log_interval' ,fallback=7)
        log_counter   = config_ini.getint('General','log_counter'  ,fallback=53)
else:
    sys.exit(1)

# **********************************************************************
# SPECIFIC APPLICATION FOLDER DIFFERS FROM APPLICATIONS
from core import create_app,db,logger,mail
# **********************************************************************
C = Context("Butler CORE",config_file,logger)
C.Set()

app     = create_app(config_file,os.getenv('BUTLER_CONFIG') or 'production', C)


# CONFIGURATION PATCH !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

logger.name="Butler CORE"
# Setup logger handlers
# Actual File system all logger ----------------------------------------
file_handler=add_Logging_Handler(
    logger=logger,
    level=C.log_level,
    folder=C.log_folder,
    nameFormat="%s.log"%logger.name.replace(' ','_'),
    handlerType='TIME_ROTATING',
    when=log_when,
    interval=log_interval,
    backupCount=log_counter
    )
print(f'{this()}: file_handler = {file_handler}')
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
    handlerType='TIME_ROTATING',
    when=log_when,
    interval=log_interval,
    backupCount=log_counter
    )
print(f'{this()}: audit_handler = {audit_handler}')
# ----------------------------------------------------------------------

from core.transactions import *

# ----------------------------------------------------------------------
if __name__ == '__main__':
    app_ctx = app.app_context()
    app_ctx.push()
    
    logger.setLevel(C.log_level)
    db.logger = logger
    
    if logger is not None:
        db.logger = logger
        logger.info("****** Butler CORE Server ***************")
        logger.info(" * %s: as '%s' Using configuration: '%s'"%
            (sys.argv[0],getpass.getuser(),config_file))
        logger.info(" * %s: db connection is '%s'"%(sys.argv[0],db))
        logger.info("*****************************************")
        for variable in os.environ:
            logger.debug("%s=%s"%(variable,os.environ.get(variable)))
        logger.debug("logger                = %s"%logger)
        logger.info ("mail                  = %s"%mail)
        logger.info ("db                    = %s"%db)
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
        print("****** Butler CORE Server ************")
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

    try:
        while True:
            #xecute_transactions(app=app,db=db,mail=mail)
            execute_transactions(app)
            wait_seconds = app.config.get('CORE_POOL_SECONDS',59)
            logger.info('----------------------------------------------------')
            logger.info(f'EG Butler CORE probe will wait for {wait_seconds} seconds ...')
            print      (f'EG Butler CORE probe will wait for {wait_seconds} seconds ...')
            time.sleep (wait_seconds)
    except KeyboardInterrupt:
        logger.warning(f'EG Butler CORE probe Interrupted.')
        logger.warning(f'EG Butler CORE probe cleaning UP ...')
        # A Tidy up process here
        logger.warning(f'EG Butler CORE probe Good Bye.')
        logger.warning('----------------------------------------------')
        sys.exit(1)
    except Exception as e:
        logger.critical(f'EG Butler CORE probe EXCEPTION: {str(e)}')
        raise e
