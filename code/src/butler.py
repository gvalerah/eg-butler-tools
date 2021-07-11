
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
from    flask_mail          import Message
import  logging
import  logging.handlers

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
#elif len(sys.argv) == 4:
#    config_file = sys.argv[2]

print(f"{this()}: 3 config_file = '{config_file}' filename from command line.")
if len(sys.argv) > 2:        
    run_mode=sys.argv[-1]
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
else:
    print(f"{this()}: ERROR invalid config_file '{config_file}'")
    sys.exit(1)

print(f'{this()}: 7 basic initialization completed.')

from    app                 import create_app,db,mail,logger

C = Context(    "Butler Web Server",
                config_file,
                logger
            )
C.Set()

app = create_app(   config_file,
                    os.getenv('BUTLER_CONFIG') or 'production',
                    C
                )

# CONFIGURATION PATCH !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

logger.name = "Butler Web Server"
# Setup logger handlers
# Actual File system all logger ----------------------------------------
file_handler = add_Logging_Handler(
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
audit_handler = add_Logging_Handler(
                    logger=logger,
                    level=logging.AUDIT,
                    folder=C.log_folder,
                    nameFormat="%s.aud"%logger.name.replace(' ','_'),
                    handlerType='TIME_ROTATING'
                    )
# ----------------------------------------------------------------------

if config_ini.getboolean('General','DEBUG',fallback=False):
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    logFormatter = logging.Formatter("[%(levelname)-8.8s] %(lineno)d %(message)s")
    console_handler.setFormatter(logFormatter)
    logger.addHandler(console_handler)

if __name__ == '__main__':
    app_ctx = app.app_context()
    app_ctx.push()
    
    logger.setLevel(C.log_level)
    db.logger = logger
    
    # test email send here ---------------------------------------------
    """
    try:
        print(f'Creando mensaje SMTP ...')
        msg = Message(  f'Prueba de Correo Butler @ {datetime.now()}',
                        sender = 'gerardovalera@hotmail.com',
                        recipients = [
                            'gerardovalera@hotmail.com',
                            'gvalera@emtecgroup.net',
                            'gvalera@sertechno.com'
                            ]
                    )
        # Plain/Text body
        msg.body = "EG Butler\n"
        # HTML body
        msg.html = f"<h2>EG Butler</h2>\n"
        for key in app.config:
           msg.body += f'{key} = {app.config[key]}\n' 
           msg.html += f'<b>{key}</b> = {app.config[key]}<br>' 
        print(f'enviando mensaje ....')
        print(f'msg={msg}')
        mail.send(msg)
        print(f'mensaje enviado ...')
    except Exception as e:
        emtec_handle_general_exception(e,fp=sys.stderr)
    # ------------------------------------------------------------------
    """
    
    if logger is not None:
        db.logger = logger
        logger.info("****** Butler Server *****************")
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
        if logger.getEffectiveLevel() < logging.INFO:
            print("*** logger.handlers are :"%logger.handlers)        
            for h in logger.handlers:
                print("    *******")
                print("    handler",h,id(h))
                print("      format",h.format,id(h.format))
                print("      formatter",h.formatter,id(h.formatter))
                print("      filter",h.filter,id(h.filter))
                print("      filters",h.filters,id(h.filters))
                try:
                    print('      name',h.name,'level',h.level,'mode',h.mode)
                except:
                    print('      name',h.name,'level',h.level)
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
    # 20200217 LOCATION OPORTINITY CHANGE DUE TO CONFIG ISSUES
    from    emtec.butler.db.flask_models    import User
    from    emtec.butler.db.flask_models    import Role

    # Will be replaced by embedded Green Unicorn HTTP Server
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

