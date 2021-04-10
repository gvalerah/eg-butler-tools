# Import configuration functions
import  configparser
from    configparser            import ConfigParser, ExtendedInterpolation

# Import logging functions
import  logging

# Import Emtec Modules
from emtec.common.log           import Log
from emtec.common.audit         import Audit

# Import App Modules
# Butler does not have specific DB functions , yet
#from emtec.butler.db.orm     import *

class Context:
    """ Butler Context Class """

    """ Members """
    # Application General Members
    config          = None
    app             = None
    app_ini_file    = None
    app_name        = None
    app_home        = None
    app_folder      = None
    
    # DB connection members
    rdbms           = "mysql"
    dialect         = "pymysql"
    driver          = "mysql+pymysql"
    user            = "user"
    password        = "Password"
    host            = "127.0.0.1"
    port            = 3306
    schema          = "butler"
    #engine_string   = None
    db              = None
    #engine          = None
    
    # Log Members
    L               = None
    logger          = None
    log_file_name   = None
    log_level       = logging.INFO
    log_folder      = None
    log_format      = None
    log_format_debug= None
    
    # Deamon Members
    pool_seconds    = 3600

    def __init__(self,app_name="Butler",app_ini_file="butler.ini",logger=None):
        self.app_name       = app_name
        self.app_ini_file   = app_ini_file
        if logger is not None:
            self.logger = logger
        self.Set()

    def init_app(self,app=None,app_name="Butler",app_ini_file="butler.ini"):
        self.app          = app
        self.app_name     = app_name
        self.app_ini_file = app_ini_file
        
    def Set(self): 
        self.Read_Configuration(self.app_ini_file)
        self.Set_Logger(self.log_level)
        
    def Read_Configuration(self,app_ini_file):
        self.app_ini_file     = app_ini_file
        self.config           = configparser.ConfigParser(interpolation=ExtendedInterpolation())
        self.config.read(self.app_ini_file)
        
        self.app_home         = self.config['General']['app_home']
        self.app_folder       = self.config['General']['app_folder']
        
        self.rdbms            = self.config['DB']['rdbms']
        self.dialect          = self.config['DB']['dialect']
        if self.rdbms is None and self.dialect is None:
            self.driver       = "%s+%s"%(self.rdbms,self.dialect)
        else:
            self.driver       = self.config['DB']['driver']
        self.user             = self.config['DB']['user']
        self.password         = self.config['DB']['password']
        self.host             = self.config['DB']['host']
        self.port             = self.config['DB']['port']
        self.schema           = self.config['DB']['schema']
        
        log_level             = self.config['General']['log_level'].capitalize()
        self.log_folder       = self.config['General']['log_folder']
        self.log_format       = self.config['General']['log_format']
        self.log_format_debug = self.config['General']['log_format_debug']

        if (log_level == 'Trace'):
            self.log_level    = logging.TRACE
        elif (log_level == 'Debug'):
            self.log_level    = logging.DEBUG
        elif (log_level == 'Information'):
            self.log_level    = logging.INFO
        elif (log_level == 'Warning'):
            self.log_level    = logging.WARNING
        elif (log_level == 'Error'):
            self.log_level    = logging.ERROR
        elif (log_level == 'Critical'):
            self.log_level    = logging.CRITICAL
        else:
            self.log_level    = logging.INFO
        self.pool_seconds = int(self.config['Daemon']['pool_seconds'])
       
    def Set_Logger(self,log_level):
        self.log_level = log_level
        if self.logger is None:
            self.L = Log(self.app_name,self.log_folder,self.log_format,self.log_format_debug,self.log_level,self.logger)    
            self.logger = self.L.logger
            self.log_file_name = self.L.file_name
