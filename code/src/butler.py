
#!/usr/bin/env python

# GV -------------------------------------------------------------------
# Top level required definitions
# GV -------------------------------------------------------------------
import  os
import  sys
import  getpass
from    pprint              import pprint
#from    flask_script        import Manager, Shell
#from    flask_migrate       import Migrate, MigrateCommand
from    flask_mail          import Message
import  logging
import  logging.handlers

import  configparser
from    configparser        import ConfigParser, ExtendedInterpolation
from    sqlalchemy          import create_engine
# GV -------------------------------------------------------------------

# GV -------------------------------------------------------------------
# GV G Unicorn required definitions
# GV -------------------------------------------------------------------
import  multiprocessing
import  gunicorn
from    gunicorn.app.base   import Application, Config
from    gunicorn            import glogging
from    gunicorn.workers    import sync

def number_of_workers(max_workers=0):
    if max_workers == 0:
        return (multiprocessing.cpu_count() * 2) + 1
    else:
        return min(max_workers,((multiprocessing.cpu_count() * 2) + 1))
        
class GUnicornFlaskApplication(Application):
    def __init__(self, app):
        self.usage, self.callable, self.prog, self.app = None, None, None, app

    def run(self, **options):
        self.cfg = Config()
        [self.cfg.set(key, value) for key, value in options.items()]
        return Application.run(self)

    load = lambda self:self.app
# GV -------------------------------------------------------------------

# GV -------------------------------------------------------------------
# Emtec group required definitions
# GV -------------------------------------------------------------------

# GV -------------------------------------------------------------------
from    emtec.common.functions             import *
from    emtec.butler.common.context     import Context
# GV -------------------------------------------------------------------

# GV Setup context data depending on configuration file

# GV Macro level default values
config_file = "butler.ini"
run_mode    = 'FLASK'

if len(sys.argv) < 2:
    print()
    print(f'{sys.argv[0]}: Usage is: {sys.argv[0]} <config file> [FLASK|GUNICORN]')
    print()
    sys.exit(1)

print(f"{this()}: 0 caller()    = {caller()}")
print(f"{this()}: 1 sys.argv    = {sys.argv}")
print(f"{this()}: 2 config_file = '{config_file}' default filename")
            
command     = sys.argv[0]

if len(sys.argv) >1:
    config_file = sys.argv[1]

print(f"{this()}: 3 config_file = '{config_file}' filename from command line.")
if len(sys.argv) > 2:        
    run_mode=sys.argv[2].upper()
print(f"{this()}: 4 run_mode    = '{run_mode}' from command line.")

if (os.path.isfile(config_file)):
        print(f"{this()}: 5 config_file = '{config_file}' is a valid file in file system")
        config_ini = configparser.ConfigParser(interpolation=ExtendedInterpolation())
        print(f"{this()}: 6 config_ini  = '{config_ini}'")
        config_ini.read( config_file )        
        run_mode      = config_ini.get   ('General','run_mode'     ,fallback='FLASK')
        flask_host    = config_ini.getint('General','flask_host'   ,fallback='0.0.0.0')
        flask_port    = config_ini.getint('General','flask_port'   ,fallback=8100)
        gunicorn_host = config_ini.getint('General','gunicorn_host',fallback='0.0.0.0')
        gunicorn_port = config_ini.getint('General','gunicorn_port',fallback=8100)
        max_workers   = config_ini.getint('General','max_workers'  ,fallback=0)
        log_when      = config_ini.get   ('General','log_when'     ,fallback='D')
        log_interval  = config_ini.getint('General','log_interval' ,fallback=7)
        log_counter   = config_ini.getint('General','log_counter'  ,fallback=53)
else:
    print(f"{this()}: ERROR invalid config_file '{config_file}'")
    sys.exit(1)

print(f'{this()}: 7 basic initialization completed.')

from    app                 import create_app,db,mail,logger,babel

C = Context(    "Butler Web Server",
                config_file,
                logger
            )
C.Set()

app = create_app(   config_file,
                    os.getenv('BUTLER_CONFIG') or 'production',
                    C
                )

# GV CONFIGURATION PATCH !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

logger.name = "Butler Web Server"
# GV Setup logger handlers
# GV Actual File system all logger -------------------------------------
file_handler = add_Logging_Handler(
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

# GV Default File logger filters (omits) AUDIT records, then an audit
# GV logger needs to be defined
file_handler.addFilter(LevelFilter(logging.AUDIT))
# GV -------------------------------------------------------------------

# GV Specialized AUDIT LOG logger --------------------------------------
audit_handler = add_Logging_Handler(
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
# GV -------------------------------------------------------------------

if config_ini.getboolean('General','DEBUG',fallback=False):
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    logFormatter = logging.Formatter("[%(levelname)-8.8s] %(lineno)d %(message)s")
    console_handler.setFormatter(logFormatter)
    logger.addHandler(console_handler)

logger.info    (f"{this}: logger       = {logger}")
logger.info    (f"{this}: C.log_folder = {C.log_folder}")
for handler in logger.handlers:
    logger.info(f"{this}: handler      = {handler}")
    
# GV Internationalization code -----------------------------------------
from flask_babel import Babel, gettext, ngettext, lazy_gettext, force_locale

print(f"Set App enabled Languages ...")
# GV This need to be read from configuration
setattr(app.config,'LANGUAGES',{
        'en': 'English',
        'es': 'Español'
    })
    
print(f"Set Default App Language ...")
setattr(app.config,'CURRENT_LANGUAGE',None)

print (f"Set Global multilanguage strings ...")

# GV -------------------------------------------------------------------

if __name__ == '__main__':
    app_ctx = app.app_context()
    app_ctx.push()
    
    logger.setLevel(C.log_level)
    db.logger = logger
    
    if logger is not None:
        db.logger = logger
        logger.info("****** Butler Server *****************xxx")
        logger.info(" * %s: as '%s' Using configuration: '%s'"%
            (sys.argv[0],getpass.getuser(),config_file))
        logger.info(" * %s: db connection is '%s'"%(sys.argv[0],db))
        logger.info("*****************************************")
        for variable in os.environ:
            logger.debug("%s=%s"%(variable,os.environ.get(variable)))
        logger.debug("logger                = %s"%logger)
        logger.debug("mail                  = %s"%mail)
        logger.debug("db                    = %s"%db)
        logger.debug("db.logger             = %s"%db.logger)
        logger.debug("app                   = %s"%app)
        logger.debug("app.root_path         = %s"%app.root_path)
        logger.debug("app.static_folder     = %s"%app.static_folder)
        logger.debug("app.template_folder 1 = %s"%app.template_folder)
        logger.debug("babel                 = %s"%babel)
        app.template_folder="%s/templates"%(app.root_path)
        logger.debug("app.template_folder 2 = %s"%app.template_folder)
        for key in app.config.keys():
            if key == key.upper():
                logger.debug("%-40s = %s"%(key,app.config[key]))
        logger.debug("%-40s = %s"%("app.root_path",app.root_path))

        logger.info("*****************************************")
        print("****** Butler Server *****************")
        print(" * %s: as '%s' Using configuration: '%s'"%
            (sys.argv[0],getpass.getuser(),config_file))
        print(" * %s: db connection is '%s'"%(sys.argv[0],db))
        print(" * logger is %s"%(logger))
        if True or logger.getEffectiveLevel() < logging.INFO:
            print("*** logger.handlers are :"%logger.handlers)        
            for h in logger.handlers:
                print(f"    *******")
                print(f"    handler {h,id(h)}")
                print(f"      formatter {h.formatter} {id(h.formatter)}")
                print(f"      filter {h.filter} {id(h.filter)}")
                print(f"      filters {h.filters} {id(h.filters)}")
                for f in h.filters:
                    print(f"       f = {f} {id(f)}")
                print(f"      when {h.when} every {h.interval} secs")
                print(f"      rollover at {h.rolloverAt} {datetime.datetime.fromtimestamp(h.rolloverAt)}")
                try:
                    print(f'      name {h.name} level {h.level} mode {h.mode}')
                except:
                    print(f'      name {h.name} level {h.level}')
        logger.trace    ("trace    Init butler Web Server Execution")
        logger.debug    ("debug    Init butler Web Server Execution")
        logger.info     ("info     Init butler Web Server Execution")
        logger.warning  ("warning  Init butler Web Server Execution")
        logger.error    ("error    Init butler Web Server Execution")
        logger.critical ("critical Init butler Web Server Execution")
        logger.audit    ("audit    Init butler Web Server Execution")
        logger.trace    ("os.environ=%s"%os.environ)
        logger.trace    ("app.config=%s"%app.config)
        logger.info("*****************************************")
        print("        *****************************************")
    else:
        print("****************************************")
        print("**** WARNING **** No logger defined ****")
        print("****************************************")

    print(f" * Will execute app here ({run_mode})")   
    # GV 20200217 LOCATION OPORTINITY CHANGE DUE TO CONFIG ISSUES
    from    emtec.butler.db.flask_models    import User
    from    emtec.butler.db.flask_models    import Role


    # GV print(f"app.config.get('NUTANIX_CLUSTERS')={app.config.get('NUTANIX_CLUSTERS')}")

    # GV Will be replaced by embedded Green Unicorn HTTP Server
    if run_mode == 'FLASK':
        print(f" * Running {app} in Flask app mode ({flask_host}:{flask_port})")
        app.run(host=flask_host,port=flask_port)
    else:
        options = {
            'bind': '%s:%s' % (gunicorn_host, gunicorn_port),
            'workers': number_of_workers(max_workers),
            'worker_class':"gunicorn.workers.sync.SyncWorker",
            'timeout':300
        }
        print(f" * Running {app} in Green Unicorn powered mode ( {options['bind']} {options['workers']} workers) ")
        logger.debug("Application CPUs   = %s" % multiprocessing.cpu_count())
        logger.debug("Application options= %s" % options)
        logger.debug("Application Flask  = %s" % app)
        gunicorn_app = GUnicornFlaskApplication(app)
        gunicorn_app.run(
            **options
        )

