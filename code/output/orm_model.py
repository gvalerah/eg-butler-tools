# ======================================================================
# ORM Models header file
# source file name: orm_models_py_header.py
# Static Header File. 
# GLVH 2018-12-13
# ----------------------------------------------------------------------
from datetime               import datetime

from sqlalchemy             import Column, String, Integer, Numeric
from sqlalchemy             import Date, Time, Boolean, DateTime
from sqlalchemy             import ForeignKey
# ----------------------------------------------------------------------



# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2022-03-24 17:50:52
# =============================================================================

from sqlalchemy                 import Table, Column
from sqlalchemy                 import MetaData, ForeignKey
from sqlalchemy                 import Integer, BigInteger,SmallInteger
from sqlalchemy                 import String
from sqlalchemy                 import Date, Time
from sqlalchemy                 import Numeric, DateTime, Boolean, Text
from sqlalchemy                 import VARBINARY


# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2022-03-24 17:50:52
# =============================================================================
import json
import logging
from time import strftime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2022-03-24 17:50:52
# =============================================================================

# GV gen_model_flask.py:418 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/models/orm_categories.py
import sqlalchemy
class Categories(Base):
    __tablename__ = 'Categories'
    engine        = None
    logger        = None

    def check_shard(suffix=None,engine=None):
       if engine is not None:
           try:
               if sqlalchemy.__version__ >= '1.4':
                   inspector = sqlalchemy.inspect(engine)
                   table_exists = inspector.has_table(__class__.__tablename__,schema='butler')
               else:
                   table_exists = engine.dialect.has_table(engine, __class__.__tablename__)
               if not table_exists:
                   metadata=MetaData()
                   metadata.bind=engine
                   __class__.__table__.metadata=metadata
                   __class__.__table__.create(checkfirst=True)
                   if sqlalchemy.__version__ >= '1.4':
                       inspector = sqlalchemy.inspect(engine)
                       table_exists = inspector.has_table(__class__.__tablename__,schema='butler')
                   else:
                       table_exists = engine.dialect.has_table(engine, __class__.__tablename__)
                   if not table_exists:
                       print('460 Table %s does not exist. creation error?'% __class__.__tablename__)
                   else:
                       pass # GV print('462 Table %s exist !!!'% __class__.__tablename__)
               else:
                   pass # GV print('464 Table %s exist !!!'% __class__.__tablename__)
           except Exception as e:
              print(f'gen/gen_model_flask.py: 466 exception: {str(e)}')
           return
    def set_shard(suffix=None,engine=None):
       if suffix is not None:
           name='Categories_{suffix}'.format(suffix=suffix)
           __class__.__tablename__  = name
           __class__.__table__.name = name
       __class__.check_shard(suffix,engine)
       return __class__.__tablename__

    category_name        = Column( String(45), primary_key=True )
    category_description = Column( String(45) )
    
    def __init__(self, category_name='None', category_description='None',engine=None,logger=None):
        """ Initiates a Categories class record """
        self.engine=engine
        self.logger=logger
        self.category_name        = category_name
        self.category_description = category_description

        self.log('Created %s'%self)
    def __repr__(self):
        """ default class Categories representation function """
        return "<Categories( category_name='%s', category_description='%s')>" % \
                ( self.category_name, self.category_description)

    def get_list(self):
        """ Gets Categories record in list format """
        __list = [ self.category_name, self.category_description]
        return __list

    def get_tuple(self):
        """ Gets Categories record in tuple format """
        __tuple = ( self.category_name, self.category_description)
        return __tuple

    def get_dict(self):
        """ Gets Categories record in dict format """
        __dict={'category_name':self.category_name,'category_description':self.category_description}

        return __dict

    def get_json_dict(self,dateformat='%Y-%m-%d',timeformat='%H:%M:%S',datetimeformat=None):
        __dict = self.get_dict()
        if datetimeformat is None: 
            datetimeformat='%s %s'%(dateformat,timeformat)
        for key in __dict.keys():
            if   'datetime.datetime' in str(type(__dict[key])): __dict[key]=__dict[key].strftime(datetimeformat)
            elif 'datetime.date'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(dateformat)
            elif 'datetime.time'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(timeformat)
            elif 'decimal.Decimal'   in str(type(__dict[key])): __dict[key]=float(__dict[key])
        return __dict

    def get_json(self,dateformat='%Y-%m-%d',timeformat='%H:%M:%S',datetimeformat=None):
        __dict = self.get_dict()
        if datetimeformat is None: 
            datetimeformat='%s %s'%(dateformat,timeformat)
        for key in __dict.keys():
            if   'datetime.datetime' in str(type(__dict[key])): __dict[key]=__dict[key].strftime(datetimeformat)
            elif 'datetime.date'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(dateformat)
            elif 'datetime.time'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(timeformat)
            elif 'decimal.Decimal'   in str(type(__dict[key])): __dict[key]=float(__dict[key])
        return json.dumps(__dict)

    def post(self):
       return self

    def patch(self,**kwargs):
       for field in self.get_column_headers():
           if field in kwargs.keys():
               setattr(self,field,kwargs[field])
       return self

    def delete(self):
       return True

    def get_json_array(self,dateformat='%Y-%m-%d',timeformat='%H:%M:%S',datetimeformat=None):
        """ Gets Categories record in JSON array format """
        __list = self.get_list()
        if datetimeformat is None: 
            datetimeformat='%s %s'%(dateformat,timeformat)
        for field in range(len(__list)):
            if   'datetime.datetime' in str(type(__list[field])): __list[field]=__list[field].strftime(datetimeformat)
            elif 'datetime.date'     in str(type(__list[field])): __list[field]=__list[field].strftime(dateformat)
            elif 'datetime.time'     in str(type(__list[field])): __list[field]=__list[field].strftime(timeformat)
            elif 'decimal.Decimal'   in str(type(__list[field])): __list[field]=float(__list[field])
        return __list

    def get_columns(self):
        """ Gets Categories record column full details list """
        __list=[{'field': 'category_name', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'NO', 'key': 'PRI', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 1, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'category_name', 'is_time': False}, {'field': 'category_description', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 2, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'category_description', 'is_time': False}]

        return __list

    def get_column_headers(self):
        """ Gets Categories record column headers list """
        __list=['category_name', 'category_description']

        return __list

    def get_column_types(self):
        """ Gets Categories record column data types list """
        __list=['String(45)', 'String(45)']

        return __list

    def get_column_meta(self):
        """ Gets Categories record column data meta list """
        __list=[('category_name', 'String(45)'), ('category_description', 'String(45)')]

        return __list

    def search_key(self,category_name):
        """ Search for an unique Categories record using all key fields (category_name) """
        try:
            if self.engine is not None:
                Session=sessionmaker(bind=self.engine)
                session=Session()
                record = session.query(Categories).filter(Categories.category_name==category_name).one_or_none()
                session.flush()
            else:
                session.rollback()
                record = None
        except Exception as e:
            detail='Categories.search_key(%s): Exception: %s'%(category_name,e)
            emtec_handle_general_exception(e,detail=detail,module=__name__,function='Categories.search_key()',logger=self.logger)
            record = None
        return record

    def log(self,message,level=logging.DEBUG):
        """ Class Categories log function """
        if self.logger is not None:
            self.logger.log(level,message)

# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2022-03-24 17:50:52
# =============================================================================

# GV gen_model_flask.py:418 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/models/orm_clusters.py
import sqlalchemy
class Clusters(Base):
    __tablename__ = 'Clusters'
    engine        = None
    logger        = None

    def check_shard(suffix=None,engine=None):
       if engine is not None:
           try:
               if sqlalchemy.__version__ >= '1.4':
                   inspector = sqlalchemy.inspect(engine)
                   table_exists = inspector.has_table(__class__.__tablename__,schema='butler')
               else:
                   table_exists = engine.dialect.has_table(engine, __class__.__tablename__)
               if not table_exists:
                   metadata=MetaData()
                   metadata.bind=engine
                   __class__.__table__.metadata=metadata
                   __class__.__table__.create(checkfirst=True)
                   if sqlalchemy.__version__ >= '1.4':
                       inspector = sqlalchemy.inspect(engine)
                       table_exists = inspector.has_table(__class__.__tablename__,schema='butler')
                   else:
                       table_exists = engine.dialect.has_table(engine, __class__.__tablename__)
                   if not table_exists:
                       print('460 Table %s does not exist. creation error?'% __class__.__tablename__)
                   else:
                       pass # GV print('462 Table %s exist !!!'% __class__.__tablename__)
               else:
                   pass # GV print('464 Table %s exist !!!'% __class__.__tablename__)
           except Exception as e:
              print(f'gen/gen_model_flask.py: 466 exception: {str(e)}')
           return
    def set_shard(suffix=None,engine=None):
       if suffix is not None:
           name='Clusters_{suffix}'.format(suffix=suffix)
           __class__.__tablename__  = name
           __class__.__table__.name = name
       __class__.check_shard(suffix,engine)
       return __class__.__tablename__

    cluster_uuid     = Column( String(45), primary_key=True )
    cluster_name     = Column( String(45) )
    cluster_username = Column( String(45) )
    cluster_password = Column( String(45) )
    cluster_ip       = Column( String(45) )
    
    def __init__(self, cluster_uuid='None', cluster_name='None', cluster_username='None', cluster_password='None', cluster_ip='None',engine=None,logger=None):
        """ Initiates a Clusters class record """
        self.engine=engine
        self.logger=logger
        self.cluster_uuid     = cluster_uuid
        self.cluster_name     = cluster_name
        self.cluster_username = cluster_username
        self.cluster_password = cluster_password
        self.cluster_ip       = cluster_ip

        self.log('Created %s'%self)
    def __repr__(self):
        """ default class Clusters representation function """
        return "<Clusters( cluster_uuid='%s', cluster_name='%s', cluster_username='%s', cluster_password='%s', cluster_ip='%s')>" % \
                ( self.cluster_uuid, self.cluster_name, self.cluster_username, self.cluster_password, self.cluster_ip)

    def get_list(self):
        """ Gets Clusters record in list format """
        __list = [ self.cluster_uuid, self.cluster_name, self.cluster_username, self.cluster_password, self.cluster_ip]
        return __list

    def get_tuple(self):
        """ Gets Clusters record in tuple format """
        __tuple = ( self.cluster_uuid, self.cluster_name, self.cluster_username, self.cluster_password, self.cluster_ip)
        return __tuple

    def get_dict(self):
        """ Gets Clusters record in dict format """
        __dict={'cluster_uuid':self.cluster_uuid,'cluster_name':self.cluster_name,'cluster_username':self.cluster_username,'cluster_password':self.cluster_password,'cluster_ip':self.cluster_ip}

        return __dict

    def get_json_dict(self,dateformat='%Y-%m-%d',timeformat='%H:%M:%S',datetimeformat=None):
        __dict = self.get_dict()
        if datetimeformat is None: 
            datetimeformat='%s %s'%(dateformat,timeformat)
        for key in __dict.keys():
            if   'datetime.datetime' in str(type(__dict[key])): __dict[key]=__dict[key].strftime(datetimeformat)
            elif 'datetime.date'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(dateformat)
            elif 'datetime.time'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(timeformat)
            elif 'decimal.Decimal'   in str(type(__dict[key])): __dict[key]=float(__dict[key])
        return __dict

    def get_json(self,dateformat='%Y-%m-%d',timeformat='%H:%M:%S',datetimeformat=None):
        __dict = self.get_dict()
        if datetimeformat is None: 
            datetimeformat='%s %s'%(dateformat,timeformat)
        for key in __dict.keys():
            if   'datetime.datetime' in str(type(__dict[key])): __dict[key]=__dict[key].strftime(datetimeformat)
            elif 'datetime.date'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(dateformat)
            elif 'datetime.time'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(timeformat)
            elif 'decimal.Decimal'   in str(type(__dict[key])): __dict[key]=float(__dict[key])
        return json.dumps(__dict)

    def post(self):
       return self

    def patch(self,**kwargs):
       for field in self.get_column_headers():
           if field in kwargs.keys():
               setattr(self,field,kwargs[field])
       return self

    def delete(self):
       return True

    def get_json_array(self,dateformat='%Y-%m-%d',timeformat='%H:%M:%S',datetimeformat=None):
        """ Gets Clusters record in JSON array format """
        __list = self.get_list()
        if datetimeformat is None: 
            datetimeformat='%s %s'%(dateformat,timeformat)
        for field in range(len(__list)):
            if   'datetime.datetime' in str(type(__list[field])): __list[field]=__list[field].strftime(datetimeformat)
            elif 'datetime.date'     in str(type(__list[field])): __list[field]=__list[field].strftime(dateformat)
            elif 'datetime.time'     in str(type(__list[field])): __list[field]=__list[field].strftime(timeformat)
            elif 'decimal.Decimal'   in str(type(__list[field])): __list[field]=float(__list[field])
        return __list

    def get_columns(self):
        """ Gets Clusters record column full details list """
        __list=[{'field': 'cluster_uuid', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'NO', 'key': 'PRI', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 1, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'cluster_uuid', 'is_time': False}, {'field': 'cluster_name', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 2, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'cluster_name', 'is_time': False}, {'field': 'cluster_username', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 3, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'cluster_username', 'is_time': False}, {'field': 'cluster_password', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 4, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'cluster_password', 'is_time': False}, {'field': 'cluster_ip', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 5, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'cluster_ip', 'is_time': False}]

        return __list

    def get_column_headers(self):
        """ Gets Clusters record column headers list """
        __list=['cluster_uuid', 'cluster_name', 'cluster_username', 'cluster_password', 'cluster_ip']

        return __list

    def get_column_types(self):
        """ Gets Clusters record column data types list """
        __list=['String(45)', 'String(45)', 'String(45)', 'String(45)', 'String(45)']

        return __list

    def get_column_meta(self):
        """ Gets Clusters record column data meta list """
        __list=[('cluster_uuid', 'String(45)'), ('cluster_name', 'String(45)'), ('cluster_username', 'String(45)'), ('cluster_password', 'String(45)'), ('cluster_ip', 'String(45)')]

        return __list

    def search_key(self,cluster_uuid):
        """ Search for an unique Clusters record using all key fields (cluster_uuid) """
        try:
            if self.engine is not None:
                Session=sessionmaker(bind=self.engine)
                session=Session()
                record = session.query(Clusters).filter(Clusters.cluster_uuid==cluster_uuid).one_or_none()
                session.flush()
            else:
                session.rollback()
                record = None
        except Exception as e:
            detail='Clusters.search_key(%s): Exception: %s'%(cluster_uuid,e)
            emtec_handle_general_exception(e,detail=detail,module=__name__,function='Clusters.search_key()',logger=self.logger)
            record = None
        return record

    def log(self,message,level=logging.DEBUG):
        """ Class Clusters log function """
        if self.logger is not None:
            self.logger.log(level,message)

# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2022-03-24 17:50:52
# =============================================================================

# GV gen_model_flask.py:418 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/models/orm_cost_centers.py
import sqlalchemy
class Cost_Centers(Base):
    __tablename__ = 'Cost_Centers'
    engine        = None
    logger        = None

    def check_shard(suffix=None,engine=None):
       if engine is not None:
           try:
               if sqlalchemy.__version__ >= '1.4':
                   inspector = sqlalchemy.inspect(engine)
                   table_exists = inspector.has_table(__class__.__tablename__,schema='butler')
               else:
                   table_exists = engine.dialect.has_table(engine, __class__.__tablename__)
               if not table_exists:
                   metadata=MetaData()
                   metadata.bind=engine
                   __class__.__table__.metadata=metadata
                   __class__.__table__.create(checkfirst=True)
                   if sqlalchemy.__version__ >= '1.4':
                       inspector = sqlalchemy.inspect(engine)
                       table_exists = inspector.has_table(__class__.__tablename__,schema='butler')
                   else:
                       table_exists = engine.dialect.has_table(engine, __class__.__tablename__)
                   if not table_exists:
                       print('460 Table %s does not exist. creation error?'% __class__.__tablename__)
                   else:
                       pass # GV print('462 Table %s exist !!!'% __class__.__tablename__)
               else:
                   pass # GV print('464 Table %s exist !!!'% __class__.__tablename__)
           except Exception as e:
              print(f'gen/gen_model_flask.py: 466 exception: {str(e)}')
           return
    def set_shard(suffix=None,engine=None):
       if suffix is not None:
           name='Cost_Centers_{suffix}'.format(suffix=suffix)
           __class__.__tablename__  = name
           __class__.__table__.name = name
       __class__.check_shard(suffix,engine)
       return __class__.__tablename__

    CC_Id          = Column( Integer, primary_key=True, autoincrement=True )
    CC_Code        = Column( String(45) )
    CC_Description = Column( String(255) )
    Cur_Code       = Column( String(3) )
    CC_Parent_Code = Column( String(45) )
    CC_Reg_Exp     = Column( String(45) )
    CC_Reference   = Column( String(245) )
    
    def __init__(self, CC_Id=0, CC_Code='None', CC_Description='None', Cur_Code='None', CC_Parent_Code='1', CC_Reg_Exp='None', CC_Reference='None',engine=None,logger=None):
        """ Initiates a Cost_Centers class record """
        self.engine=engine
        self.logger=logger
        self.CC_Id          = CC_Id
        self.CC_Code        = CC_Code
        self.CC_Description = CC_Description
        self.Cur_Code       = Cur_Code
        self.CC_Parent_Code = CC_Parent_Code
        self.CC_Reg_Exp     = CC_Reg_Exp
        self.CC_Reference   = CC_Reference

        self.log('Created %s'%self)
    def __repr__(self):
        """ default class Cost_Centers representation function """
        return "<Cost_Centers( CC_Id='%s', CC_Code='%s', CC_Description='%s', Cur_Code='%s', CC_Parent_Code='%s', CC_Reg_Exp='%s', CC_Reference='%s')>" % \
                ( self.CC_Id, self.CC_Code, self.CC_Description, self.Cur_Code, self.CC_Parent_Code, self.CC_Reg_Exp, self.CC_Reference)

    def get_list(self):
        """ Gets Cost_Centers record in list format """
        __list = [ self.CC_Id, self.CC_Code, self.CC_Description, self.Cur_Code, self.CC_Parent_Code, self.CC_Reg_Exp, self.CC_Reference]
        return __list

    def get_tuple(self):
        """ Gets Cost_Centers record in tuple format """
        __tuple = ( self.CC_Id, self.CC_Code, self.CC_Description, self.Cur_Code, self.CC_Parent_Code, self.CC_Reg_Exp, self.CC_Reference)
        return __tuple

    def get_dict(self):
        """ Gets Cost_Centers record in dict format """
        __dict={'CC_Id':self.CC_Id,'CC_Code':self.CC_Code,'CC_Description':self.CC_Description,'Cur_Code':self.Cur_Code,'CC_Parent_Code':self.CC_Parent_Code,'CC_Reg_Exp':self.CC_Reg_Exp,'CC_Reference':self.CC_Reference}

        return __dict

    def get_json_dict(self,dateformat='%Y-%m-%d',timeformat='%H:%M:%S',datetimeformat=None):
        __dict = self.get_dict()
        if datetimeformat is None: 
            datetimeformat='%s %s'%(dateformat,timeformat)
        for key in __dict.keys():
            if   'datetime.datetime' in str(type(__dict[key])): __dict[key]=__dict[key].strftime(datetimeformat)
            elif 'datetime.date'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(dateformat)
            elif 'datetime.time'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(timeformat)
            elif 'decimal.Decimal'   in str(type(__dict[key])): __dict[key]=float(__dict[key])
        return __dict

    def get_json(self,dateformat='%Y-%m-%d',timeformat='%H:%M:%S',datetimeformat=None):
        __dict = self.get_dict()
        if datetimeformat is None: 
            datetimeformat='%s %s'%(dateformat,timeformat)
        for key in __dict.keys():
            if   'datetime.datetime' in str(type(__dict[key])): __dict[key]=__dict[key].strftime(datetimeformat)
            elif 'datetime.date'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(dateformat)
            elif 'datetime.time'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(timeformat)
            elif 'decimal.Decimal'   in str(type(__dict[key])): __dict[key]=float(__dict[key])
        return json.dumps(__dict)

    def post(self):
       return self

    def patch(self,**kwargs):
       for field in self.get_column_headers():
           if field in kwargs.keys():
               setattr(self,field,kwargs[field])
       return self

    def delete(self):
       return True

    def get_json_array(self,dateformat='%Y-%m-%d',timeformat='%H:%M:%S',datetimeformat=None):
        """ Gets Cost_Centers record in JSON array format """
        __list = self.get_list()
        if datetimeformat is None: 
            datetimeformat='%s %s'%(dateformat,timeformat)
        for field in range(len(__list)):
            if   'datetime.datetime' in str(type(__list[field])): __list[field]=__list[field].strftime(datetimeformat)
            elif 'datetime.date'     in str(type(__list[field])): __list[field]=__list[field].strftime(dateformat)
            elif 'datetime.time'     in str(type(__list[field])): __list[field]=__list[field].strftime(timeformat)
            elif 'decimal.Decimal'   in str(type(__list[field])): __list[field]=float(__list[field])
        return __list

    def get_columns(self):
        """ Gets Cost_Centers record column full details list """
        __list=[{'field': 'CC_Id', 'type': 'int', 'type_flask': 'db.Integer', 'type_sqlalchemy': 'Integer', 'null': 'NO', 'key': 'PRI', 'default': None, 'extra': 'auto_increment', 'is_form_editable': True, 'format': None, 'order': 1, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'IntegerField', 'is_id': True, 'header': 'CC_Id', 'is_time': False}, {'field': 'CC_Code', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 2, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'CC_Code', 'is_time': False}, {'field': 'CC_Description', 'type': 'varchar(255)', 'type_flask': 'db.String(255)', 'type_sqlalchemy': 'String(255)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 3, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'CC_Description', 'is_time': False}, {'field': 'Cur_Code', 'type': 'varchar(3)', 'type_flask': 'db.String(3)', 'type_sqlalchemy': 'String(3)', 'null': 'NO', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 4, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'Cur_Code', 'is_time': False}, {'field': 'CC_Parent_Code', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'NO', 'key': '', 'default': '1', 'extra': '', 'is_form_editable': True, 'format': None, 'order': 5, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'CC_Parent_Code', 'is_time': False}, {'field': 'CC_Reg_Exp', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 6, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'CC_Reg_Exp', 'is_time': False}, {'field': 'CC_Reference', 'type': 'varchar(245)', 'type_flask': 'db.String(245)', 'type_sqlalchemy': 'String(245)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 7, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'CC_Reference', 'is_time': False}]

        return __list

    def get_column_headers(self):
        """ Gets Cost_Centers record column headers list """
        __list=['CC_Id', 'CC_Code', 'CC_Description', 'Cur_Code', 'CC_Parent_Code', 'CC_Reg_Exp', 'CC_Reference']

        return __list

    def get_column_types(self):
        """ Gets Cost_Centers record column data types list """
        __list=['Integer', 'String(45)', 'String(255)', 'String(3)', 'String(45)', 'String(45)', 'String(245)']

        return __list

    def get_column_meta(self):
        """ Gets Cost_Centers record column data meta list """
        __list=[('CC_Id', 'Integer'), ('CC_Code', 'String(45)'), ('CC_Description', 'String(255)'), ('Cur_Code', 'String(3)'), ('CC_Parent_Code', 'String(45)'), ('CC_Reg_Exp', 'String(45)'), ('CC_Reference', 'String(245)')]

        return __list

    def search_key(self,CC_Id):
        """ Search for an unique Cost_Centers record using all key fields (CC_Id) """
        try:
            if self.engine is not None:
                Session=sessionmaker(bind=self.engine)
                session=Session()
                record = session.query(Cost_Centers).filter(Cost_Centers.CC_Id==CC_Id).one_or_none()
                session.flush()
            else:
                session.rollback()
                record = None
        except Exception as e:
            detail='Cost_Centers.search_key(%s): Exception: %s'%(CC_Id,e)
            emtec_handle_general_exception(e,detail=detail,module=__name__,function='Cost_Centers.search_key()',logger=self.logger)
            record = None
        return record

    def log(self,message,level=logging.DEBUG):
        """ Class Cost_Centers log function """
        if self.logger is not None:
            self.logger.log(level,message)

# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2022-03-24 17:50:52
# =============================================================================

# gen_model_flask.py:865 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/models/orm_cost_centers.py
# gen_model_flask.py:866 Table sharding code follows:
def get_Cost_Centers(table_name_suffix):
  class Cost_Centers_Class(Base):
    __tablename__ = 'Cost_Centers_%s'%(table_name_suffix)
    engine        = None
    logger        = None

    def set_shard(suffix=None,engine=None):
       if suffix is not None:
           name='Cost_Centers_{suffix}'.format(suffix=suffix)
           __class__.__tablename__  = name
           __class__.__table_args__ = {'extend_existing':True}
           __class__.__table__.name = name
           __class__.check_shard(suffix,engine)
       return __class__.__tablename__

    CC_Id          = Column( Integer, primary_key=True, autoincrement=True )
    CC_Code        = Column( String(45) )
    CC_Description = Column( String(255) )
    Cur_Code       = Column( String(3) )
    CC_Parent_Code = Column( String(45) )
    CC_Reg_Exp     = Column( String(45) )
    CC_Reference   = Column( String(245) )
    
    def __init__(self, CC_Id=0, CC_Code='None', CC_Description='None', Cur_Code='None', CC_Parent_Code='1', CC_Reg_Exp='None', CC_Reference='None',engine=None,logger=None):
        """ Initiates a Cost_Centers class record """
        self.engine=engine
        self.logger=logger
        self.CC_Id          = CC_Id
        self.CC_Code        = CC_Code
        self.CC_Description = CC_Description
        self.Cur_Code       = Cur_Code
        self.CC_Parent_Code = CC_Parent_Code
        self.CC_Reg_Exp     = CC_Reg_Exp
        self.CC_Reference   = CC_Reference

        self.log('Created %s'%self)
    def __repr__(self):
        """ default class Cost_Centers representation function """
        return "<Cost_Centers( CC_Id='%s', CC_Code='%s', CC_Description='%s', Cur_Code='%s', CC_Parent_Code='%s', CC_Reg_Exp='%s', CC_Reference='%s')>" % \
                ( self.CC_Id, self.CC_Code, self.CC_Description, self.Cur_Code, self.CC_Parent_Code, self.CC_Reg_Exp, self.CC_Reference)

    def get_list(self):
        """ Gets Cost_Centers record in list format """
        __list = [ self.CC_Id, self.CC_Code, self.CC_Description, self.Cur_Code, self.CC_Parent_Code, self.CC_Reg_Exp, self.CC_Reference]
        return __list

    def get_tuple(self):
        """ Gets Cost_Centers record in tuple format """
        __tuple = ( self.CC_Id, self.CC_Code, self.CC_Description, self.Cur_Code, self.CC_Parent_Code, self.CC_Reg_Exp, self.CC_Reference)
        return __tuple

    def get_dict(self):
        """ Gets Cost_Centers record in dict format """
        __dict={'CC_Id':self.CC_Id,'CC_Code':self.CC_Code,'CC_Description':self.CC_Description,'Cur_Code':self.Cur_Code,'CC_Parent_Code':self.CC_Parent_Code,'CC_Reg_Exp':self.CC_Reg_Exp,'CC_Reference':self.CC_Reference}

        return __dict

    def get_json_dict(self,dateformat='%Y-%m-%d',timeformat='%H:%M:%S',datetimeformat=None):
        __dict = self.get_dict()
        if datetimeformat is None: 
            datetimeformat='%s %s'%(dateformat,timeformat)
        for key in __dict.keys():
            if   'datetime.datetime' in str(type(__dict[key])): __dict[key]=__dict[key].strftime(datetimeformat)
            elif 'datetime.date'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(dateformat)
            elif 'datetime.time'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(timeformat)
            elif 'decimal.Decimal'   in str(type(__dict[key])): __dict[key]=float(__dict[key])
        return __dict

    def get_json(self,dateformat='%Y-%m-%d',timeformat='%H:%M:%S',datetimeformat=None):
        __dict = self.get_dict()
        if datetimeformat is None: 
            datetimeformat='%s %s'%(dateformat,timeformat)
        for key in __dict.keys():
            if   'datetime.datetime' in str(type(__dict[key])): __dict[key]=__dict[key].strftime(datetimeformat)
            elif 'datetime.date'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(dateformat)
            elif 'datetime.time'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(timeformat)
            elif 'decimal.Decimal'   in str(type(__dict[key])): __dict[key]=float(__dict[key])
        return json.dumps(__dict)

    def post(self):
       return self

    def patch(self,**kwargs):
       for field in self.get_column_headers():
           if field in kwargs.keys():
               setattr(self,field,kwargs[field])
       return self

    def delete(self):
       return True

    def get_json_array(self,dateformat='%Y-%m-%d',timeformat='%H:%M:%S',datetimeformat=None):
        """ Gets Cost_Centers record in JSON array format """
        __list = self.get_list()
        if datetimeformat is None: 
            datetimeformat='%s %s'%(dateformat,timeformat)
        for field in range(len(__list)):
            if   'datetime.datetime' in str(type(__list[field])): __list[field]=__list[field].strftime(datetimeformat)
            elif 'datetime.date'     in str(type(__list[field])): __list[field]=__list[field].strftime(dateformat)
            elif 'datetime.time'     in str(type(__list[field])): __list[field]=__list[field].strftime(timeformat)
            elif 'decimal.Decimal'   in str(type(__list[field])): __list[field]=float(__list[field])
        return __list

    def get_columns(self):
        """ Gets Cost_Centers record column full details list """
        __list=[{'field': 'CC_Id', 'type': 'int', 'type_flask': 'db.Integer', 'type_sqlalchemy': 'Integer', 'null': 'NO', 'key': 'PRI', 'default': None, 'extra': 'auto_increment', 'is_form_editable': True, 'format': None, 'order': 1, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'IntegerField', 'is_id': True, 'header': 'CC_Id', 'is_time': False}, {'field': 'CC_Code', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 2, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'CC_Code', 'is_time': False}, {'field': 'CC_Description', 'type': 'varchar(255)', 'type_flask': 'db.String(255)', 'type_sqlalchemy': 'String(255)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 3, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'CC_Description', 'is_time': False}, {'field': 'Cur_Code', 'type': 'varchar(3)', 'type_flask': 'db.String(3)', 'type_sqlalchemy': 'String(3)', 'null': 'NO', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 4, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'Cur_Code', 'is_time': False}, {'field': 'CC_Parent_Code', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'NO', 'key': '', 'default': '1', 'extra': '', 'is_form_editable': True, 'format': None, 'order': 5, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'CC_Parent_Code', 'is_time': False}, {'field': 'CC_Reg_Exp', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 6, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'CC_Reg_Exp', 'is_time': False}, {'field': 'CC_Reference', 'type': 'varchar(245)', 'type_flask': 'db.String(245)', 'type_sqlalchemy': 'String(245)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 7, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'CC_Reference', 'is_time': False}]

        return __list

    def get_column_headers(self):
        """ Gets Cost_Centers record column headers list """
        __list=['CC_Id', 'CC_Code', 'CC_Description', 'Cur_Code', 'CC_Parent_Code', 'CC_Reg_Exp', 'CC_Reference']

        return __list

    def get_column_types(self):
        """ Gets Cost_Centers record column data types list """
        __list=['Integer', 'String(45)', 'String(255)', 'String(3)', 'String(45)', 'String(45)', 'String(245)']

        return __list

    def get_column_meta(self):
        """ Gets Cost_Centers record column data meta list """
        __list=[('CC_Id', 'Integer'), ('CC_Code', 'String(45)'), ('CC_Description', 'String(255)'), ('Cur_Code', 'String(3)'), ('CC_Parent_Code', 'String(45)'), ('CC_Reg_Exp', 'String(45)'), ('CC_Reference', 'String(245)')]

        return __list

    def search_key(self,CC_Id):
        """ Search for an unique Cost_Centers record using all key fields (CC_Id) """
        try:
            if self.engine is not None:
                Session=sessionmaker(bind=self.engine)
                session=Session()
                record = session.query(Cost_Centers).filter(Cost_Centers.CC_Id==CC_Id).one_or_none()
                session.flush()
            else:
                session.rollback()
                record = None
        except Exception as e:
            detail='Cost_Centers.search_key(%s): Exception: %s'%(CC_Id,e)
            emtec_handle_general_exception(e,detail=detail,module=__name__,function='Cost_Centers.search_key()',logger=self.logger)
            record = None
        return record

    def log(self,message,level=logging.DEBUG):
        """ Class Cost_Centers log function """
        if self.logger is not None:
            self.logger.log(level,message)

  Cost_Centers_Class.__name__ = 'Cost_Centers_%s'%(table_name_suffix)
  x = Cost_Centers_Class
  return x

# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2022-03-24 17:50:52
# =============================================================================

# GV gen_model_flask.py:418 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/models/orm_disk_images.py
import sqlalchemy
class Disk_Images(Base):
    __tablename__ = 'Disk_Images'
    engine        = None
    logger        = None

    def check_shard(suffix=None,engine=None):
       if engine is not None:
           try:
               if sqlalchemy.__version__ >= '1.4':
                   inspector = sqlalchemy.inspect(engine)
                   table_exists = inspector.has_table(__class__.__tablename__,schema='butler')
               else:
                   table_exists = engine.dialect.has_table(engine, __class__.__tablename__)
               if not table_exists:
                   metadata=MetaData()
                   metadata.bind=engine
                   __class__.__table__.metadata=metadata
                   __class__.__table__.create(checkfirst=True)
                   if sqlalchemy.__version__ >= '1.4':
                       inspector = sqlalchemy.inspect(engine)
                       table_exists = inspector.has_table(__class__.__tablename__,schema='butler')
                   else:
                       table_exists = engine.dialect.has_table(engine, __class__.__tablename__)
                   if not table_exists:
                       print('460 Table %s does not exist. creation error?'% __class__.__tablename__)
                   else:
                       pass # GV print('462 Table %s exist !!!'% __class__.__tablename__)
               else:
                   pass # GV print('464 Table %s exist !!!'% __class__.__tablename__)
           except Exception as e:
              print(f'gen/gen_model_flask.py: 466 exception: {str(e)}')
           return
    def set_shard(suffix=None,engine=None):
       if suffix is not None:
           name='Disk_Images_{suffix}'.format(suffix=suffix)
           __class__.__tablename__  = name
           __class__.__table__.name = name
       __class__.check_shard(suffix,engine)
       return __class__.__tablename__

    uuid             = Column( String(45), primary_key=True )
    name             = Column( String(45) )
    annotation       = Column( String(45) )
    image_type       = Column( String(45) )
    image_state      = Column( String(45) )
    vm_disk_size     = Column( BigInteger )
    vm_disk_size_mib = Column( Integer )
    vm_disk_size_gib = Column( Integer )
    cluster          = Column( String(45) )
    
    def __init__(self, uuid='None', name='None', annotation='None', image_type='None', image_state='None', vm_disk_size=0, vm_disk_size_mib=0, vm_disk_size_gib=0, cluster='None',engine=None,logger=None):
        """ Initiates a Disk_Images class record """
        self.engine=engine
        self.logger=logger
        self.uuid             = uuid
        self.name             = name
        self.annotation       = annotation
        self.image_type       = image_type
        self.image_state      = image_state
        self.vm_disk_size     = vm_disk_size
        self.vm_disk_size_mib = vm_disk_size_mib
        self.vm_disk_size_gib = vm_disk_size_gib
        self.cluster          = cluster

        self.log('Created %s'%self)
    def __repr__(self):
        """ default class Disk_Images representation function """
        return "<Disk_Images( uuid='%s', name='%s', annotation='%s', image_type='%s', image_state='%s', vm_disk_size='%s', vm_disk_size_mib='%s', vm_disk_size_gib='%s', cluster='%s')>" % \
                ( self.uuid, self.name, self.annotation, self.image_type, self.image_state, self.vm_disk_size, self.vm_disk_size_mib, self.vm_disk_size_gib, self.cluster)

    def get_list(self):
        """ Gets Disk_Images record in list format """
        __list = [ self.uuid, self.name, self.annotation, self.image_type, self.image_state, self.vm_disk_size, self.vm_disk_size_mib, self.vm_disk_size_gib, self.cluster]
        return __list

    def get_tuple(self):
        """ Gets Disk_Images record in tuple format """
        __tuple = ( self.uuid, self.name, self.annotation, self.image_type, self.image_state, self.vm_disk_size, self.vm_disk_size_mib, self.vm_disk_size_gib, self.cluster)
        return __tuple

    def get_dict(self):
        """ Gets Disk_Images record in dict format """
        __dict={'uuid':self.uuid,'name':self.name,'annotation':self.annotation,'image_type':self.image_type,'image_state':self.image_state,'vm_disk_size':self.vm_disk_size,'vm_disk_size_mib':self.vm_disk_size_mib,'vm_disk_size_gib':self.vm_disk_size_gib,'cluster':self.cluster}

        return __dict

    def get_json_dict(self,dateformat='%Y-%m-%d',timeformat='%H:%M:%S',datetimeformat=None):
        __dict = self.get_dict()
        if datetimeformat is None: 
            datetimeformat='%s %s'%(dateformat,timeformat)
        for key in __dict.keys():
            if   'datetime.datetime' in str(type(__dict[key])): __dict[key]=__dict[key].strftime(datetimeformat)
            elif 'datetime.date'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(dateformat)
            elif 'datetime.time'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(timeformat)
            elif 'decimal.Decimal'   in str(type(__dict[key])): __dict[key]=float(__dict[key])
        return __dict

    def get_json(self,dateformat='%Y-%m-%d',timeformat='%H:%M:%S',datetimeformat=None):
        __dict = self.get_dict()
        if datetimeformat is None: 
            datetimeformat='%s %s'%(dateformat,timeformat)
        for key in __dict.keys():
            if   'datetime.datetime' in str(type(__dict[key])): __dict[key]=__dict[key].strftime(datetimeformat)
            elif 'datetime.date'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(dateformat)
            elif 'datetime.time'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(timeformat)
            elif 'decimal.Decimal'   in str(type(__dict[key])): __dict[key]=float(__dict[key])
        return json.dumps(__dict)

    def post(self):
       return self

    def patch(self,**kwargs):
       for field in self.get_column_headers():
           if field in kwargs.keys():
               setattr(self,field,kwargs[field])
       return self

    def delete(self):
       return True

    def get_json_array(self,dateformat='%Y-%m-%d',timeformat='%H:%M:%S',datetimeformat=None):
        """ Gets Disk_Images record in JSON array format """
        __list = self.get_list()
        if datetimeformat is None: 
            datetimeformat='%s %s'%(dateformat,timeformat)
        for field in range(len(__list)):
            if   'datetime.datetime' in str(type(__list[field])): __list[field]=__list[field].strftime(datetimeformat)
            elif 'datetime.date'     in str(type(__list[field])): __list[field]=__list[field].strftime(dateformat)
            elif 'datetime.time'     in str(type(__list[field])): __list[field]=__list[field].strftime(timeformat)
            elif 'decimal.Decimal'   in str(type(__list[field])): __list[field]=float(__list[field])
        return __list

    def get_columns(self):
        """ Gets Disk_Images record column full details list """
        __list=[{'field': 'uuid', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'NO', 'key': 'PRI', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 1, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'uuid', 'is_time': False}, {'field': 'name', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'NO', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 2, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'name', 'is_time': False}, {'field': 'annotation', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 3, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'annotation', 'is_time': False}, {'field': 'image_type', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'NO', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 4, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'image_type', 'is_time': False}, {'field': 'image_state', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'NO', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 5, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'image_state', 'is_time': False}, {'field': 'vm_disk_size', 'type': 'bigint', 'type_flask': 'db.BigInteger', 'type_sqlalchemy': 'BigInteger', 'null': 'NO', 'key': '', 'default': '0', 'extra': '', 'is_form_editable': True, 'format': None, 'order': 6, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'is_id': False, 'header': 'vm_disk_size', 'is_time': False}, {'field': 'vm_disk_size_mib', 'type': 'int', 'type_flask': 'db.Integer', 'type_sqlalchemy': 'Integer', 'null': 'NO', 'key': '', 'default': '0', 'extra': '', 'is_form_editable': True, 'format': None, 'order': 7, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'IntegerField', 'is_id': False, 'header': 'vm_disk_size_mib', 'is_time': False}, {'field': 'vm_disk_size_gib', 'type': 'int', 'type_flask': 'db.Integer', 'type_sqlalchemy': 'Integer', 'null': 'NO', 'key': '', 'default': '0', 'extra': '', 'is_form_editable': True, 'format': None, 'order': 8, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'IntegerField', 'is_id': False, 'header': 'vm_disk_size_gib', 'is_time': False}, {'field': 'cluster', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'NO', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 9, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'cluster', 'is_time': False}]

        return __list

    def get_column_headers(self):
        """ Gets Disk_Images record column headers list """
        __list=['uuid', 'name', 'annotation', 'image_type', 'image_state', 'vm_disk_size', 'vm_disk_size_mib', 'vm_disk_size_gib', 'cluster']

        return __list

    def get_column_types(self):
        """ Gets Disk_Images record column data types list """
        __list=['String(45)', 'String(45)', 'String(45)', 'String(45)', 'String(45)', 'BigInteger', 'Integer', 'Integer', 'String(45)']

        return __list

    def get_column_meta(self):
        """ Gets Disk_Images record column data meta list """
        __list=[('uuid', 'String(45)'), ('name', 'String(45)'), ('annotation', 'String(45)'), ('image_type', 'String(45)'), ('image_state', 'String(45)'), ('vm_disk_size', 'BigInteger'), ('vm_disk_size_mib', 'Integer'), ('vm_disk_size_gib', 'Integer'), ('cluster', 'String(45)')]

        return __list

    def search_key(self,uuid):
        """ Search for an unique Disk_Images record using all key fields (uuid) """
        try:
            if self.engine is not None:
                Session=sessionmaker(bind=self.engine)
                session=Session()
                record = session.query(Disk_Images).filter(Disk_Images.uuid==uuid).one_or_none()
                session.flush()
            else:
                session.rollback()
                record = None
        except Exception as e:
            detail='Disk_Images.search_key(%s): Exception: %s'%(uuid,e)
            emtec_handle_general_exception(e,detail=detail,module=__name__,function='Disk_Images.search_key()',logger=self.logger)
            record = None
        return record

    def log(self,message,level=logging.DEBUG):
        """ Class Disk_Images log function """
        if self.logger is not None:
            self.logger.log(level,message)

# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2022-03-24 17:50:52
# =============================================================================

# GV gen_model_flask.py:418 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/models/orm_domains.py
import sqlalchemy
class Domains(Base):
    __tablename__ = 'Domains'
    engine        = None
    logger        = None

    def check_shard(suffix=None,engine=None):
       if engine is not None:
           try:
               if sqlalchemy.__version__ >= '1.4':
                   inspector = sqlalchemy.inspect(engine)
                   table_exists = inspector.has_table(__class__.__tablename__,schema='butler')
               else:
                   table_exists = engine.dialect.has_table(engine, __class__.__tablename__)
               if not table_exists:
                   metadata=MetaData()
                   metadata.bind=engine
                   __class__.__table__.metadata=metadata
                   __class__.__table__.create(checkfirst=True)
                   if sqlalchemy.__version__ >= '1.4':
                       inspector = sqlalchemy.inspect(engine)
                       table_exists = inspector.has_table(__class__.__tablename__,schema='butler')
                   else:
                       table_exists = engine.dialect.has_table(engine, __class__.__tablename__)
                   if not table_exists:
                       print('460 Table %s does not exist. creation error?'% __class__.__tablename__)
                   else:
                       pass # GV print('462 Table %s exist !!!'% __class__.__tablename__)
               else:
                   pass # GV print('464 Table %s exist !!!'% __class__.__tablename__)
           except Exception as e:
              print(f'gen/gen_model_flask.py: 466 exception: {str(e)}')
           return
    def set_shard(suffix=None,engine=None):
       if suffix is not None:
           name='Domains_{suffix}'.format(suffix=suffix)
           __class__.__tablename__  = name
           __class__.__table__.name = name
       __class__.check_shard(suffix,engine)
       return __class__.__tablename__

    Domain_Id = Column( Integer, primary_key=True )
    Name      = Column( String(45) )
    Comments  = Column( Text )
    
    def __init__(self, Domain_Id=None, Name='None', Comments=None,engine=None,logger=None):
        """ Initiates a Domains class record """
        self.engine=engine
        self.logger=logger
        self.Domain_Id = Domain_Id
        self.Name      = Name
        self.Comments  = Comments

        self.log('Created %s'%self)
    def __repr__(self):
        """ default class Domains representation function """
        return "<Domains( Domain_Id='%s', Name='%s', Comments='%s')>" % \
                ( self.Domain_Id, self.Name, self.Comments)

    def get_list(self):
        """ Gets Domains record in list format """
        __list = [ self.Domain_Id, self.Name, self.Comments]
        return __list

    def get_tuple(self):
        """ Gets Domains record in tuple format """
        __tuple = ( self.Domain_Id, self.Name, self.Comments)
        return __tuple

    def get_dict(self):
        """ Gets Domains record in dict format """
        __dict={'Domain_Id':self.Domain_Id,'Name':self.Name,'Comments':self.Comments}

        return __dict

    def get_json_dict(self,dateformat='%Y-%m-%d',timeformat='%H:%M:%S',datetimeformat=None):
        __dict = self.get_dict()
        if datetimeformat is None: 
            datetimeformat='%s %s'%(dateformat,timeformat)
        for key in __dict.keys():
            if   'datetime.datetime' in str(type(__dict[key])): __dict[key]=__dict[key].strftime(datetimeformat)
            elif 'datetime.date'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(dateformat)
            elif 'datetime.time'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(timeformat)
            elif 'decimal.Decimal'   in str(type(__dict[key])): __dict[key]=float(__dict[key])
        return __dict

    def get_json(self,dateformat='%Y-%m-%d',timeformat='%H:%M:%S',datetimeformat=None):
        __dict = self.get_dict()
        if datetimeformat is None: 
            datetimeformat='%s %s'%(dateformat,timeformat)
        for key in __dict.keys():
            if   'datetime.datetime' in str(type(__dict[key])): __dict[key]=__dict[key].strftime(datetimeformat)
            elif 'datetime.date'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(dateformat)
            elif 'datetime.time'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(timeformat)
            elif 'decimal.Decimal'   in str(type(__dict[key])): __dict[key]=float(__dict[key])
        return json.dumps(__dict)

    def post(self):
       return self

    def patch(self,**kwargs):
       for field in self.get_column_headers():
           if field in kwargs.keys():
               setattr(self,field,kwargs[field])
       return self

    def delete(self):
       return True

    def get_json_array(self,dateformat='%Y-%m-%d',timeformat='%H:%M:%S',datetimeformat=None):
        """ Gets Domains record in JSON array format """
        __list = self.get_list()
        if datetimeformat is None: 
            datetimeformat='%s %s'%(dateformat,timeformat)
        for field in range(len(__list)):
            if   'datetime.datetime' in str(type(__list[field])): __list[field]=__list[field].strftime(datetimeformat)
            elif 'datetime.date'     in str(type(__list[field])): __list[field]=__list[field].strftime(dateformat)
            elif 'datetime.time'     in str(type(__list[field])): __list[field]=__list[field].strftime(timeformat)
            elif 'decimal.Decimal'   in str(type(__list[field])): __list[field]=float(__list[field])
        return __list

    def get_columns(self):
        """ Gets Domains record column full details list """
        __list=[{'field': 'Domain_Id', 'type': 'int', 'type_flask': 'db.Integer', 'type_sqlalchemy': 'Integer', 'null': 'NO', 'key': 'PRI', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 1, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'IntegerField', 'is_id': False, 'header': 'Domain_Id', 'is_time': False}, {'field': 'Name', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 2, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'Name', 'is_time': False}, {'field': 'Comments', 'type': 'text', 'type_flask': 'db.Text', 'type_sqlalchemy': 'Text', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 3, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'Comments', 'is_time': False}]

        return __list

    def get_column_headers(self):
        """ Gets Domains record column headers list """
        __list=['Domain_Id', 'Name', 'Comments']

        return __list

    def get_column_types(self):
        """ Gets Domains record column data types list """
        __list=['Integer', 'String(45)', 'Text']

        return __list

    def get_column_meta(self):
        """ Gets Domains record column data meta list """
        __list=[('Domain_Id', 'Integer'), ('Name', 'String(45)'), ('Comments', 'Text')]

        return __list

    def get_id(self,Name):
        """ Search for a 'Domains' Id looking for field 'Name' """
        Id = None
        try:
            if self.engine is not None:
                Session=sessionmaker(bind=self.engine)
                session=Session()
                Id = session.query(Domains.Id).filter(Domains.Name==Name).scalar()
                session.flush()
            else:
                session.rollback()
                Id = None
        except Exception as e:
            detail='Domains.get_id(%s): Exception: %s'%(Name,e)
            emtec_handle_general_exception(e,detail=detail,module=__name__,function='Domains.get_id()',logger=self.logger)
            Id = None
        return Id

    def search(self,Name):
        """ Search for a 'Domains' record looking for field 'Name' """
        Id = self.get_id(Name)
        if Id is not None:
            try:
                if self.engine is not None:
                    Session=sessionmaker(bind=self.engine)
                    session=Session()
                    record = session.query(Domains).filter(Domains.Id==Id).one_or_none()
                    session.flush()
                else:
                    session.rollback()
                    record = None
            except Exception as e:
                detail='Domains.search(%s): Exception: %s'%(Name,e)
                emtec_handle_general_exception(e,detail=detail,module=__name__,function='Domains.search()',logger=self.logger)
                record = None
        return record

    def search_key(self,Domain_Id):
        """ Search for an unique Domains record using all key fields (Domain_Id) """
        try:
            if self.engine is not None:
                Session=sessionmaker(bind=self.engine)
                session=Session()
                record = session.query(Domains).filter(Domains.Domain_Id==Domain_Id).one_or_none()
                session.flush()
            else:
                session.rollback()
                record = None
        except Exception as e:
            detail='Domains.search_key(%s): Exception: %s'%(Domain_Id,e)
            emtec_handle_general_exception(e,detail=detail,module=__name__,function='Domains.search_key()',logger=self.logger)
            record = None
        return record

    def log(self,message,level=logging.DEBUG):
        """ Class Domains log function """
        if self.logger is not None:
            self.logger.log(level,message)

# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2022-03-24 17:50:52
# =============================================================================

# GV gen_model_flask.py:418 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/models/orm_interface.py
import sqlalchemy
class Interface(Base):
    __tablename__ = 'Interface'
    engine        = None
    logger        = None

    def check_shard(suffix=None,engine=None):
       if engine is not None:
           try:
               if sqlalchemy.__version__ >= '1.4':
                   inspector = sqlalchemy.inspect(engine)
                   table_exists = inspector.has_table(__class__.__tablename__,schema='butler')
               else:
                   table_exists = engine.dialect.has_table(engine, __class__.__tablename__)
               if not table_exists:
                   metadata=MetaData()
                   metadata.bind=engine
                   __class__.__table__.metadata=metadata
                   __class__.__table__.create(checkfirst=True)
                   if sqlalchemy.__version__ >= '1.4':
                       inspector = sqlalchemy.inspect(engine)
                       table_exists = inspector.has_table(__class__.__tablename__,schema='butler')
                   else:
                       table_exists = engine.dialect.has_table(engine, __class__.__tablename__)
                   if not table_exists:
                       print('460 Table %s does not exist. creation error?'% __class__.__tablename__)
                   else:
                       pass # GV print('462 Table %s exist !!!'% __class__.__tablename__)
               else:
                   pass # GV print('464 Table %s exist !!!'% __class__.__tablename__)
           except Exception as e:
              print(f'gen/gen_model_flask.py: 466 exception: {str(e)}')
           return
    def set_shard(suffix=None,engine=None):
       if suffix is not None:
           name='Interface_{suffix}'.format(suffix=suffix)
           __class__.__tablename__  = name
           __class__.__table__.name = name
       __class__.check_shard(suffix,engine)
       return __class__.__tablename__

    Id          = Column( Integer, primary_key=True, autoincrement=True )
    User_Id     = Column( Integer )
    Table_name  = Column( String(45) )
    Option_Type = Column( Integer )
    Argument_1  = Column( String(256) )
    Argument_2  = Column( String(256) )
    Argument_3  = Column( String(256) )
    Is_Active   = Column( Boolean )
    
    def __init__(self, Id=0, User_Id=None, Table_name='None', Option_Type=None, Argument_1='None', Argument_2='None', Argument_3='None', Is_Active=None,engine=None,logger=None):
        """ Initiates a Interface class record """
        self.engine=engine
        self.logger=logger
        self.Id          = Id
        self.User_Id     = User_Id
        self.Table_name  = Table_name
        self.Option_Type = Option_Type
        self.Argument_1  = Argument_1
        self.Argument_2  = Argument_2
        self.Argument_3  = Argument_3
        self.Is_Active   = Is_Active

        self.log('Created %s'%self)
    def __repr__(self):
        """ default class Interface representation function """
        return "<Interface( Id='%s', User_Id='%s', Table_name='%s', Option_Type='%s', Argument_1='%s', Argument_2='%s', Argument_3='%s', Is_Active='%s')>" % \
                ( self.Id, self.User_Id, self.Table_name, self.Option_Type, self.Argument_1, self.Argument_2, self.Argument_3, self.Is_Active)

    def get_list(self):
        """ Gets Interface record in list format """
        __list = [ self.Id, self.User_Id, self.Table_name, self.Option_Type, self.Argument_1, self.Argument_2, self.Argument_3, self.Is_Active]
        return __list

    def get_tuple(self):
        """ Gets Interface record in tuple format """
        __tuple = ( self.Id, self.User_Id, self.Table_name, self.Option_Type, self.Argument_1, self.Argument_2, self.Argument_3, self.Is_Active)
        return __tuple

    def get_dict(self):
        """ Gets Interface record in dict format """
        __dict={'Id':self.Id,'User_Id':self.User_Id,'Table_name':self.Table_name,'Option_Type':self.Option_Type,'Argument_1':self.Argument_1,'Argument_2':self.Argument_2,'Argument_3':self.Argument_3,'Is_Active':self.Is_Active}

        return __dict

    def get_json_dict(self,dateformat='%Y-%m-%d',timeformat='%H:%M:%S',datetimeformat=None):
        __dict = self.get_dict()
        if datetimeformat is None: 
            datetimeformat='%s %s'%(dateformat,timeformat)
        for key in __dict.keys():
            if   'datetime.datetime' in str(type(__dict[key])): __dict[key]=__dict[key].strftime(datetimeformat)
            elif 'datetime.date'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(dateformat)
            elif 'datetime.time'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(timeformat)
            elif 'decimal.Decimal'   in str(type(__dict[key])): __dict[key]=float(__dict[key])
        return __dict

    def get_json(self,dateformat='%Y-%m-%d',timeformat='%H:%M:%S',datetimeformat=None):
        __dict = self.get_dict()
        if datetimeformat is None: 
            datetimeformat='%s %s'%(dateformat,timeformat)
        for key in __dict.keys():
            if   'datetime.datetime' in str(type(__dict[key])): __dict[key]=__dict[key].strftime(datetimeformat)
            elif 'datetime.date'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(dateformat)
            elif 'datetime.time'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(timeformat)
            elif 'decimal.Decimal'   in str(type(__dict[key])): __dict[key]=float(__dict[key])
        return json.dumps(__dict)

    def post(self):
       return self

    def patch(self,**kwargs):
       for field in self.get_column_headers():
           if field in kwargs.keys():
               setattr(self,field,kwargs[field])
       return self

    def delete(self):
       return True

    def get_json_array(self,dateformat='%Y-%m-%d',timeformat='%H:%M:%S',datetimeformat=None):
        """ Gets Interface record in JSON array format """
        __list = self.get_list()
        if datetimeformat is None: 
            datetimeformat='%s %s'%(dateformat,timeformat)
        for field in range(len(__list)):
            if   'datetime.datetime' in str(type(__list[field])): __list[field]=__list[field].strftime(datetimeformat)
            elif 'datetime.date'     in str(type(__list[field])): __list[field]=__list[field].strftime(dateformat)
            elif 'datetime.time'     in str(type(__list[field])): __list[field]=__list[field].strftime(timeformat)
            elif 'decimal.Decimal'   in str(type(__list[field])): __list[field]=float(__list[field])
        return __list

    def get_columns(self):
        """ Gets Interface record column full details list """
        __list=[{'field': 'Id', 'type': 'int', 'type_flask': 'db.Integer', 'type_sqlalchemy': 'Integer', 'null': 'NO', 'key': 'PRI', 'default': None, 'extra': 'auto_increment', 'is_form_editable': True, 'format': None, 'order': 1, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'IntegerField', 'is_id': True, 'header': 'Id', 'is_time': False}, {'field': 'User_Id', 'type': 'int', 'type_flask': 'db.Integer', 'type_sqlalchemy': 'Integer', 'null': 'NO', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 2, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'IntegerField', 'is_id': False, 'header': 'User_Id', 'is_time': False}, {'field': 'Table_name', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'NO', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 3, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'Table_name', 'is_time': False}, {'field': 'Option_Type', 'type': 'int', 'type_flask': 'db.Integer', 'type_sqlalchemy': 'Integer', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 4, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'IntegerField', 'is_id': False, 'header': 'Option_Type', 'is_time': False}, {'field': 'Argument_1', 'type': 'varchar(256)', 'type_flask': 'db.String(256)', 'type_sqlalchemy': 'String(256)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 5, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'Argument_1', 'is_time': False}, {'field': 'Argument_2', 'type': 'varchar(256)', 'type_flask': 'db.String(256)', 'type_sqlalchemy': 'String(256)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 6, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'Argument_2', 'is_time': False}, {'field': 'Argument_3', 'type': 'varchar(256)', 'type_flask': 'db.String(256)', 'type_sqlalchemy': 'String(256)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 7, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'Argument_3', 'is_time': False}, {'field': 'Is_Active', 'type': 'tinyint', 'type_flask': 'db.Boolean', 'type_sqlalchemy': 'Boolean', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 8, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'BooleanField', 'is_id': False, 'header': 'Is_Active', 'is_time': False}]

        return __list

    def get_column_headers(self):
        """ Gets Interface record column headers list """
        __list=['Id', 'User_Id', 'Table_name', 'Option_Type', 'Argument_1', 'Argument_2', 'Argument_3', 'Is_Active']

        return __list

    def get_column_types(self):
        """ Gets Interface record column data types list """
        __list=['Integer', 'Integer', 'String(45)', 'Integer', 'String(256)', 'String(256)', 'String(256)', 'Boolean']

        return __list

    def get_column_meta(self):
        """ Gets Interface record column data meta list """
        __list=[('Id', 'Integer'), ('User_Id', 'Integer'), ('Table_name', 'String(45)'), ('Option_Type', 'Integer'), ('Argument_1', 'String(256)'), ('Argument_2', 'String(256)'), ('Argument_3', 'String(256)'), ('Is_Active', 'Boolean')]

        return __list

    def search_key(self,Id):
        """ Search for an unique Interface record using all key fields (Id) """
        try:
            if self.engine is not None:
                Session=sessionmaker(bind=self.engine)
                session=Session()
                record = session.query(Interface).filter(Interface.Id==Id).one_or_none()
                session.flush()
            else:
                session.rollback()
                record = None
        except Exception as e:
            detail='Interface.search_key(%s): Exception: %s'%(Id,e)
            emtec_handle_general_exception(e,detail=detail,module=__name__,function='Interface.search_key()',logger=self.logger)
            record = None
        return record

    def log(self,message,level=logging.DEBUG):
        """ Class Interface log function """
        if self.logger is not None:
            self.logger.log(level,message)

# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2022-03-24 17:50:52
# =============================================================================

# GV gen_model_flask.py:418 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/models/orm_migration_groups.py
import sqlalchemy
class Migration_Groups(Base):
    __tablename__ = 'Migration_Groups'
    engine        = None
    logger        = None

    def check_shard(suffix=None,engine=None):
       if engine is not None:
           try:
               if sqlalchemy.__version__ >= '1.4':
                   inspector = sqlalchemy.inspect(engine)
                   table_exists = inspector.has_table(__class__.__tablename__,schema='butler')
               else:
                   table_exists = engine.dialect.has_table(engine, __class__.__tablename__)
               if not table_exists:
                   metadata=MetaData()
                   metadata.bind=engine
                   __class__.__table__.metadata=metadata
                   __class__.__table__.create(checkfirst=True)
                   if sqlalchemy.__version__ >= '1.4':
                       inspector = sqlalchemy.inspect(engine)
                       table_exists = inspector.has_table(__class__.__tablename__,schema='butler')
                   else:
                       table_exists = engine.dialect.has_table(engine, __class__.__tablename__)
                   if not table_exists:
                       print('460 Table %s does not exist. creation error?'% __class__.__tablename__)
                   else:
                       pass # GV print('462 Table %s exist !!!'% __class__.__tablename__)
               else:
                   pass # GV print('464 Table %s exist !!!'% __class__.__tablename__)
           except Exception as e:
              print(f'gen/gen_model_flask.py: 466 exception: {str(e)}')
           return
    def set_shard(suffix=None,engine=None):
       if suffix is not None:
           name='Migration_Groups_{suffix}'.format(suffix=suffix)
           __class__.__tablename__  = name
           __class__.__table__.name = name
       __class__.check_shard(suffix,engine)
       return __class__.__tablename__

    MG_Id    = Column( Integer, primary_key=True, autoincrement=True )
    Name     = Column( String(256) )
    Origin   = Column( String(45) )
    Destiny  = Column( String(45) )
    Customer = Column( Integer )
    Platform = Column( Integer )
    
    def __init__(self, MG_Id=0, Name='None', Origin='None', Destiny='None', Customer=None, Platform=None,engine=None,logger=None):
        """ Initiates a Migration_Groups class record """
        self.engine=engine
        self.logger=logger
        self.MG_Id    = MG_Id
        self.Name     = Name
        self.Origin   = Origin
        self.Destiny  = Destiny
        self.Customer = Customer
        self.Platform = Platform

        self.log('Created %s'%self)
    def __repr__(self):
        """ default class Migration_Groups representation function """
        return "<Migration_Groups( MG_Id='%s', Name='%s', Origin='%s', Destiny='%s', Customer='%s', Platform='%s')>" % \
                ( self.MG_Id, self.Name, self.Origin, self.Destiny, self.Customer, self.Platform)

    def get_list(self):
        """ Gets Migration_Groups record in list format """
        __list = [ self.MG_Id, self.Name, self.Origin, self.Destiny, self.Customer, self.Platform]
        return __list

    def get_tuple(self):
        """ Gets Migration_Groups record in tuple format """
        __tuple = ( self.MG_Id, self.Name, self.Origin, self.Destiny, self.Customer, self.Platform)
        return __tuple

    def get_dict(self):
        """ Gets Migration_Groups record in dict format """
        __dict={'MG_Id':self.MG_Id,'Name':self.Name,'Origin':self.Origin,'Destiny':self.Destiny,'Customer':self.Customer,'Platform':self.Platform}

        return __dict

    def get_json_dict(self,dateformat='%Y-%m-%d',timeformat='%H:%M:%S',datetimeformat=None):
        __dict = self.get_dict()
        if datetimeformat is None: 
            datetimeformat='%s %s'%(dateformat,timeformat)
        for key in __dict.keys():
            if   'datetime.datetime' in str(type(__dict[key])): __dict[key]=__dict[key].strftime(datetimeformat)
            elif 'datetime.date'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(dateformat)
            elif 'datetime.time'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(timeformat)
            elif 'decimal.Decimal'   in str(type(__dict[key])): __dict[key]=float(__dict[key])
        return __dict

    def get_json(self,dateformat='%Y-%m-%d',timeformat='%H:%M:%S',datetimeformat=None):
        __dict = self.get_dict()
        if datetimeformat is None: 
            datetimeformat='%s %s'%(dateformat,timeformat)
        for key in __dict.keys():
            if   'datetime.datetime' in str(type(__dict[key])): __dict[key]=__dict[key].strftime(datetimeformat)
            elif 'datetime.date'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(dateformat)
            elif 'datetime.time'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(timeformat)
            elif 'decimal.Decimal'   in str(type(__dict[key])): __dict[key]=float(__dict[key])
        return json.dumps(__dict)

    def post(self):
       return self

    def patch(self,**kwargs):
       for field in self.get_column_headers():
           if field in kwargs.keys():
               setattr(self,field,kwargs[field])
       return self

    def delete(self):
       return True

    def get_json_array(self,dateformat='%Y-%m-%d',timeformat='%H:%M:%S',datetimeformat=None):
        """ Gets Migration_Groups record in JSON array format """
        __list = self.get_list()
        if datetimeformat is None: 
            datetimeformat='%s %s'%(dateformat,timeformat)
        for field in range(len(__list)):
            if   'datetime.datetime' in str(type(__list[field])): __list[field]=__list[field].strftime(datetimeformat)
            elif 'datetime.date'     in str(type(__list[field])): __list[field]=__list[field].strftime(dateformat)
            elif 'datetime.time'     in str(type(__list[field])): __list[field]=__list[field].strftime(timeformat)
            elif 'decimal.Decimal'   in str(type(__list[field])): __list[field]=float(__list[field])
        return __list

    def get_columns(self):
        """ Gets Migration_Groups record column full details list """
        __list=[{'field': 'MG_Id', 'type': 'int', 'type_flask': 'db.Integer', 'type_sqlalchemy': 'Integer', 'null': 'NO', 'key': 'PRI', 'default': None, 'extra': 'auto_increment', 'is_form_editable': True, 'format': None, 'order': 1, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'IntegerField', 'is_id': True, 'header': 'MG_Id', 'is_time': False}, {'field': 'Name', 'type': 'varchar(256)', 'type_flask': 'db.String(256)', 'type_sqlalchemy': 'String(256)', 'null': 'NO', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 2, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'Name', 'is_time': False}, {'field': 'Origin', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'NO', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 3, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'Origin', 'is_time': False}, {'field': 'Destiny', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'NO', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 4, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'Destiny', 'is_time': False}, {'field': 'Customer', 'type': 'int', 'type_flask': 'db.Integer', 'type_sqlalchemy': 'Integer', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 5, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'IntegerField', 'is_id': False, 'header': 'Customer', 'is_time': False}, {'field': 'Platform', 'type': 'int', 'type_flask': 'db.Integer', 'type_sqlalchemy': 'Integer', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 6, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'IntegerField', 'is_id': False, 'header': 'Platform', 'is_time': False}]

        return __list

    def get_column_headers(self):
        """ Gets Migration_Groups record column headers list """
        __list=['MG_Id', 'Name', 'Origin', 'Destiny', 'Customer', 'Platform']

        return __list

    def get_column_types(self):
        """ Gets Migration_Groups record column data types list """
        __list=['Integer', 'String(256)', 'String(45)', 'String(45)', 'Integer', 'Integer']

        return __list

    def get_column_meta(self):
        """ Gets Migration_Groups record column data meta list """
        __list=[('MG_Id', 'Integer'), ('Name', 'String(256)'), ('Origin', 'String(45)'), ('Destiny', 'String(45)'), ('Customer', 'Integer'), ('Platform', 'Integer')]

        return __list

    def get_id(self,Name):
        """ Search for a 'Migration_Groups' Id looking for field 'Name' """
        Id = None
        try:
            if self.engine is not None:
                Session=sessionmaker(bind=self.engine)
                session=Session()
                Id = session.query(Migration_Groups.Id).filter(Migration_Groups.Name==Name).scalar()
                session.flush()
            else:
                session.rollback()
                Id = None
        except Exception as e:
            detail='Migration_Groups.get_id(%s): Exception: %s'%(Name,e)
            emtec_handle_general_exception(e,detail=detail,module=__name__,function='Migration_Groups.get_id()',logger=self.logger)
            Id = None
        return Id

    def search(self,Name):
        """ Search for a 'Migration_Groups' record looking for field 'Name' """
        Id = self.get_id(Name)
        if Id is not None:
            try:
                if self.engine is not None:
                    Session=sessionmaker(bind=self.engine)
                    session=Session()
                    record = session.query(Migration_Groups).filter(Migration_Groups.Id==Id).one_or_none()
                    session.flush()
                else:
                    session.rollback()
                    record = None
            except Exception as e:
                detail='Migration_Groups.search(%s): Exception: %s'%(Name,e)
                emtec_handle_general_exception(e,detail=detail,module=__name__,function='Migration_Groups.search()',logger=self.logger)
                record = None
        return record

    def search_key(self,MG_Id):
        """ Search for an unique Migration_Groups record using all key fields (MG_Id) """
        try:
            if self.engine is not None:
                Session=sessionmaker(bind=self.engine)
                session=Session()
                record = session.query(Migration_Groups).filter(Migration_Groups.MG_Id==MG_Id).one_or_none()
                session.flush()
            else:
                session.rollback()
                record = None
        except Exception as e:
            detail='Migration_Groups.search_key(%s): Exception: %s'%(MG_Id,e)
            emtec_handle_general_exception(e,detail=detail,module=__name__,function='Migration_Groups.search_key()',logger=self.logger)
            record = None
        return record

    def log(self,message,level=logging.DEBUG):
        """ Class Migration_Groups log function """
        if self.logger is not None:
            self.logger.log(level,message)

# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2022-03-24 17:50:52
# =============================================================================

# gen_model_flask.py:865 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/models/orm_migration_groups.py
# gen_model_flask.py:866 Table sharding code follows:
def get_Migration_Groups(table_name_suffix):
  class Migration_Groups_Class(Base):
    __tablename__ = 'Migration_Groups_%s'%(table_name_suffix)
    engine        = None
    logger        = None

    def set_shard(suffix=None,engine=None):
       if suffix is not None:
           name='Migration_Groups_{suffix}'.format(suffix=suffix)
           __class__.__tablename__  = name
           __class__.__table_args__ = {'extend_existing':True}
           __class__.__table__.name = name
           __class__.check_shard(suffix,engine)
       return __class__.__tablename__

    MG_Id    = Column( Integer, primary_key=True, autoincrement=True )
    Name     = Column( String(256) )
    Origin   = Column( String(45) )
    Destiny  = Column( String(45) )
    Customer = Column( Integer )
    Platform = Column( Integer )
    
    def __init__(self, MG_Id=0, Name='None', Origin='None', Destiny='None', Customer=None, Platform=None,engine=None,logger=None):
        """ Initiates a Migration_Groups class record """
        self.engine=engine
        self.logger=logger
        self.MG_Id    = MG_Id
        self.Name     = Name
        self.Origin   = Origin
        self.Destiny  = Destiny
        self.Customer = Customer
        self.Platform = Platform

        self.log('Created %s'%self)
    def __repr__(self):
        """ default class Migration_Groups representation function """
        return "<Migration_Groups( MG_Id='%s', Name='%s', Origin='%s', Destiny='%s', Customer='%s', Platform='%s')>" % \
                ( self.MG_Id, self.Name, self.Origin, self.Destiny, self.Customer, self.Platform)

    def get_list(self):
        """ Gets Migration_Groups record in list format """
        __list = [ self.MG_Id, self.Name, self.Origin, self.Destiny, self.Customer, self.Platform]
        return __list

    def get_tuple(self):
        """ Gets Migration_Groups record in tuple format """
        __tuple = ( self.MG_Id, self.Name, self.Origin, self.Destiny, self.Customer, self.Platform)
        return __tuple

    def get_dict(self):
        """ Gets Migration_Groups record in dict format """
        __dict={'MG_Id':self.MG_Id,'Name':self.Name,'Origin':self.Origin,'Destiny':self.Destiny,'Customer':self.Customer,'Platform':self.Platform}

        return __dict

    def get_json_dict(self,dateformat='%Y-%m-%d',timeformat='%H:%M:%S',datetimeformat=None):
        __dict = self.get_dict()
        if datetimeformat is None: 
            datetimeformat='%s %s'%(dateformat,timeformat)
        for key in __dict.keys():
            if   'datetime.datetime' in str(type(__dict[key])): __dict[key]=__dict[key].strftime(datetimeformat)
            elif 'datetime.date'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(dateformat)
            elif 'datetime.time'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(timeformat)
            elif 'decimal.Decimal'   in str(type(__dict[key])): __dict[key]=float(__dict[key])
        return __dict

    def get_json(self,dateformat='%Y-%m-%d',timeformat='%H:%M:%S',datetimeformat=None):
        __dict = self.get_dict()
        if datetimeformat is None: 
            datetimeformat='%s %s'%(dateformat,timeformat)
        for key in __dict.keys():
            if   'datetime.datetime' in str(type(__dict[key])): __dict[key]=__dict[key].strftime(datetimeformat)
            elif 'datetime.date'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(dateformat)
            elif 'datetime.time'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(timeformat)
            elif 'decimal.Decimal'   in str(type(__dict[key])): __dict[key]=float(__dict[key])
        return json.dumps(__dict)

    def post(self):
       return self

    def patch(self,**kwargs):
       for field in self.get_column_headers():
           if field in kwargs.keys():
               setattr(self,field,kwargs[field])
       return self

    def delete(self):
       return True

    def get_json_array(self,dateformat='%Y-%m-%d',timeformat='%H:%M:%S',datetimeformat=None):
        """ Gets Migration_Groups record in JSON array format """
        __list = self.get_list()
        if datetimeformat is None: 
            datetimeformat='%s %s'%(dateformat,timeformat)
        for field in range(len(__list)):
            if   'datetime.datetime' in str(type(__list[field])): __list[field]=__list[field].strftime(datetimeformat)
            elif 'datetime.date'     in str(type(__list[field])): __list[field]=__list[field].strftime(dateformat)
            elif 'datetime.time'     in str(type(__list[field])): __list[field]=__list[field].strftime(timeformat)
            elif 'decimal.Decimal'   in str(type(__list[field])): __list[field]=float(__list[field])
        return __list

    def get_columns(self):
        """ Gets Migration_Groups record column full details list """
        __list=[{'field': 'MG_Id', 'type': 'int', 'type_flask': 'db.Integer', 'type_sqlalchemy': 'Integer', 'null': 'NO', 'key': 'PRI', 'default': None, 'extra': 'auto_increment', 'is_form_editable': True, 'format': None, 'order': 1, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'IntegerField', 'is_id': True, 'header': 'MG_Id', 'is_time': False}, {'field': 'Name', 'type': 'varchar(256)', 'type_flask': 'db.String(256)', 'type_sqlalchemy': 'String(256)', 'null': 'NO', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 2, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'Name', 'is_time': False}, {'field': 'Origin', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'NO', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 3, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'Origin', 'is_time': False}, {'field': 'Destiny', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'NO', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 4, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'Destiny', 'is_time': False}, {'field': 'Customer', 'type': 'int', 'type_flask': 'db.Integer', 'type_sqlalchemy': 'Integer', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 5, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'IntegerField', 'is_id': False, 'header': 'Customer', 'is_time': False}, {'field': 'Platform', 'type': 'int', 'type_flask': 'db.Integer', 'type_sqlalchemy': 'Integer', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 6, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'IntegerField', 'is_id': False, 'header': 'Platform', 'is_time': False}]

        return __list

    def get_column_headers(self):
        """ Gets Migration_Groups record column headers list """
        __list=['MG_Id', 'Name', 'Origin', 'Destiny', 'Customer', 'Platform']

        return __list

    def get_column_types(self):
        """ Gets Migration_Groups record column data types list """
        __list=['Integer', 'String(256)', 'String(45)', 'String(45)', 'Integer', 'Integer']

        return __list

    def get_column_meta(self):
        """ Gets Migration_Groups record column data meta list """
        __list=[('MG_Id', 'Integer'), ('Name', 'String(256)'), ('Origin', 'String(45)'), ('Destiny', 'String(45)'), ('Customer', 'Integer'), ('Platform', 'Integer')]

        return __list

    def get_id(self,Name):
        """ Search for a 'Migration_Groups' Id looking for field 'Name' """
        Id = None
        try:
            if self.engine is not None:
                Session=sessionmaker(bind=self.engine)
                session=Session()
                Id = session.query(Migration_Groups.Id).filter(Migration_Groups.Name==Name).scalar()
                session.flush()
            else:
                session.rollback()
                Id = None
        except Exception as e:
            detail='Migration_Groups.get_id(%s): Exception: %s'%(Name,e)
            emtec_handle_general_exception(e,detail=detail,module=__name__,function='Migration_Groups.get_id()',logger=self.logger)
            Id = None
        return Id

    def search(self,Name):
        """ Search for a 'Migration_Groups' record looking for field 'Name' """
        Id = self.get_id(Name)
        if Id is not None:
            try:
                if self.engine is not None:
                    Session=sessionmaker(bind=self.engine)
                    session=Session()
                    record = session.query(Migration_Groups).filter(Migration_Groups.Id==Id).one_or_none()
                    session.flush()
                else:
                    session.rollback()
                    record = None
            except Exception as e:
                detail='Migration_Groups.search(%s): Exception: %s'%(Name,e)
                emtec_handle_general_exception(e,detail=detail,module=__name__,function='Migration_Groups.search()',logger=self.logger)
                record = None
        return record

    def search_key(self,MG_Id):
        """ Search for an unique Migration_Groups record using all key fields (MG_Id) """
        try:
            if self.engine is not None:
                Session=sessionmaker(bind=self.engine)
                session=Session()
                record = session.query(Migration_Groups).filter(Migration_Groups.MG_Id==MG_Id).one_or_none()
                session.flush()
            else:
                session.rollback()
                record = None
        except Exception as e:
            detail='Migration_Groups.search_key(%s): Exception: %s'%(MG_Id,e)
            emtec_handle_general_exception(e,detail=detail,module=__name__,function='Migration_Groups.search_key()',logger=self.logger)
            record = None
        return record

    def log(self,message,level=logging.DEBUG):
        """ Class Migration_Groups log function """
        if self.logger is not None:
            self.logger.log(level,message)

  Migration_Groups_Class.__name__ = 'Migration_Groups_%s'%(table_name_suffix)
  x = Migration_Groups_Class
  return x

# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2022-03-24 17:50:52
# =============================================================================

# GV gen_model_flask.py:418 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/models/orm_migration_groups_vm.py
import sqlalchemy
class Migration_Groups_VM(Base):
    __tablename__ = 'Migration_Groups_VM'
    engine        = None
    logger        = None

    def check_shard(suffix=None,engine=None):
       if engine is not None:
           try:
               if sqlalchemy.__version__ >= '1.4':
                   inspector = sqlalchemy.inspect(engine)
                   table_exists = inspector.has_table(__class__.__tablename__,schema='butler')
               else:
                   table_exists = engine.dialect.has_table(engine, __class__.__tablename__)
               if not table_exists:
                   metadata=MetaData()
                   metadata.bind=engine
                   __class__.__table__.metadata=metadata
                   __class__.__table__.create(checkfirst=True)
                   if sqlalchemy.__version__ >= '1.4':
                       inspector = sqlalchemy.inspect(engine)
                       table_exists = inspector.has_table(__class__.__tablename__,schema='butler')
                   else:
                       table_exists = engine.dialect.has_table(engine, __class__.__tablename__)
                   if not table_exists:
                       print('460 Table %s does not exist. creation error?'% __class__.__tablename__)
                   else:
                       pass # GV print('462 Table %s exist !!!'% __class__.__tablename__)
               else:
                   pass # GV print('464 Table %s exist !!!'% __class__.__tablename__)
           except Exception as e:
              print(f'gen/gen_model_flask.py: 466 exception: {str(e)}')
           return
    def set_shard(suffix=None,engine=None):
       if suffix is not None:
           name='Migration_Groups_VM_{suffix}'.format(suffix=suffix)
           __class__.__tablename__  = name
           __class__.__table__.name = name
       __class__.check_shard(suffix,engine)
       return __class__.__tablename__

    MG_Id               = Column( Integer, ForeignKey('Migration_Groups.MG_Id'), primary_key=True )
    vm_uuid             = Column( String(45), primary_key=True )
    vm_cluster_uuid     = Column( String(45) )
    vm_name             = Column( String(256) )
    vm_state            = Column( Boolean )
    vm_has_pd           = Column( Boolean )
    vm_pd_name          = Column( String(45) )
    vm_pd_active        = Column( Boolean )
    vm_pd_replicating   = Column( Boolean )
    vm_pd_schedules     = Column( Integer )
    vm_last_replication = Column( DateTime )
    vm_migrate          = Column( Boolean )
    vm_project          = Column( String(45) )
    
    def __init__(self, MG_Id=None, vm_uuid='None', vm_cluster_uuid='None', vm_name='None', vm_state=1, vm_has_pd=0, vm_pd_name='None', vm_pd_active=0, vm_pd_replicating=0, vm_pd_schedules=0, vm_last_replication=None, vm_migrate=0, vm_project='None',engine=None,logger=None):
        """ Initiates a Migration_Groups_VM class record """
        self.engine=engine
        self.logger=logger
        self.MG_Id               = MG_Id
        self.vm_uuid             = vm_uuid
        self.vm_cluster_uuid     = vm_cluster_uuid
        self.vm_name             = vm_name
        self.vm_state            = vm_state
        self.vm_has_pd           = vm_has_pd
        self.vm_pd_name          = vm_pd_name
        self.vm_pd_active        = vm_pd_active
        self.vm_pd_replicating   = vm_pd_replicating
        self.vm_pd_schedules     = vm_pd_schedules
        self.vm_last_replication = vm_last_replication
        self.vm_migrate          = vm_migrate
        self.vm_project          = vm_project

        self.log('Created %s'%self)
    def __repr__(self):
        """ default class Migration_Groups_VM representation function """
        return "<Migration_Groups_VM( MG_Id='%s', vm_uuid='%s', vm_cluster_uuid='%s', vm_name='%s', vm_state='%s', vm_has_pd='%s', vm_pd_name='%s', vm_pd_active='%s', vm_pd_replicating='%s', vm_pd_schedules='%s', vm_last_replication='%s', vm_migrate='%s', vm_project='%s')>" % \
                ( self.MG_Id, self.vm_uuid, self.vm_cluster_uuid, self.vm_name, self.vm_state, self.vm_has_pd, self.vm_pd_name, self.vm_pd_active, self.vm_pd_replicating, self.vm_pd_schedules, self.vm_last_replication, self.vm_migrate, self.vm_project)

    def get_list(self):
        """ Gets Migration_Groups_VM record in list format """
        __list = [ self.MG_Id, self.vm_uuid, self.vm_cluster_uuid, self.vm_name, self.vm_state, self.vm_has_pd, self.vm_pd_name, self.vm_pd_active, self.vm_pd_replicating, self.vm_pd_schedules, self.vm_last_replication, self.vm_migrate, self.vm_project]
        return __list

    def get_tuple(self):
        """ Gets Migration_Groups_VM record in tuple format """
        __tuple = ( self.MG_Id, self.vm_uuid, self.vm_cluster_uuid, self.vm_name, self.vm_state, self.vm_has_pd, self.vm_pd_name, self.vm_pd_active, self.vm_pd_replicating, self.vm_pd_schedules, self.vm_last_replication, self.vm_migrate, self.vm_project)
        return __tuple

    def get_dict(self):
        """ Gets Migration_Groups_VM record in dict format """
        __dict={'MG_Id':self.MG_Id,'vm_uuid':self.vm_uuid,'vm_cluster_uuid':self.vm_cluster_uuid,'vm_name':self.vm_name,'vm_state':self.vm_state,'vm_has_pd':self.vm_has_pd,'vm_pd_name':self.vm_pd_name,'vm_pd_active':self.vm_pd_active,'vm_pd_replicating':self.vm_pd_replicating,'vm_pd_schedules':self.vm_pd_schedules,'vm_last_replication':self.vm_last_replication,'vm_migrate':self.vm_migrate,'vm_project':self.vm_project}

        return __dict

    def get_json_dict(self,dateformat='%Y-%m-%d',timeformat='%H:%M:%S',datetimeformat=None):
        __dict = self.get_dict()
        if datetimeformat is None: 
            datetimeformat='%s %s'%(dateformat,timeformat)
        for key in __dict.keys():
            if   'datetime.datetime' in str(type(__dict[key])): __dict[key]=__dict[key].strftime(datetimeformat)
            elif 'datetime.date'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(dateformat)
            elif 'datetime.time'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(timeformat)
            elif 'decimal.Decimal'   in str(type(__dict[key])): __dict[key]=float(__dict[key])
        return __dict

    def get_json(self,dateformat='%Y-%m-%d',timeformat='%H:%M:%S',datetimeformat=None):
        __dict = self.get_dict()
        if datetimeformat is None: 
            datetimeformat='%s %s'%(dateformat,timeformat)
        for key in __dict.keys():
            if   'datetime.datetime' in str(type(__dict[key])): __dict[key]=__dict[key].strftime(datetimeformat)
            elif 'datetime.date'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(dateformat)
            elif 'datetime.time'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(timeformat)
            elif 'decimal.Decimal'   in str(type(__dict[key])): __dict[key]=float(__dict[key])
        return json.dumps(__dict)

    def post(self):
       return self

    def patch(self,**kwargs):
       for field in self.get_column_headers():
           if field in kwargs.keys():
               setattr(self,field,kwargs[field])
       return self

    def delete(self):
       return True

    def get_json_array(self,dateformat='%Y-%m-%d',timeformat='%H:%M:%S',datetimeformat=None):
        """ Gets Migration_Groups_VM record in JSON array format """
        __list = self.get_list()
        if datetimeformat is None: 
            datetimeformat='%s %s'%(dateformat,timeformat)
        for field in range(len(__list)):
            if   'datetime.datetime' in str(type(__list[field])): __list[field]=__list[field].strftime(datetimeformat)
            elif 'datetime.date'     in str(type(__list[field])): __list[field]=__list[field].strftime(dateformat)
            elif 'datetime.time'     in str(type(__list[field])): __list[field]=__list[field].strftime(timeformat)
            elif 'decimal.Decimal'   in str(type(__list[field])): __list[field]=float(__list[field])
        return __list

    def get_columns(self):
        """ Gets Migration_Groups_VM record column full details list """
        __list=[{'field': 'MG_Id', 'type': 'int', 'type_flask': 'db.Integer', 'type_sqlalchemy': 'Integer', 'null': 'NO', 'key': 'PRI', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 1, 'is_searchable': True, 'is_fk': True, 'referenced_table': 'Migration_Groups', 'referenced_class': 'migration_groups', 'foreign_key': 'MG_Id', 'foreign_field': 'MG_Id', 'foreign_value': 'Name', 'is_numeric': False, 'form_type': 'SelectField', 'is_id': False, 'header': 'MG_Id', 'is_time': False}, {'field': 'vm_uuid', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'NO', 'key': 'PRI', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 2, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'vm_uuid', 'is_time': False}, {'field': 'vm_cluster_uuid', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 3, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'vm_cluster_uuid', 'is_time': False}, {'field': 'vm_name', 'type': 'varchar(256)', 'type_flask': 'db.String(256)', 'type_sqlalchemy': 'String(256)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 4, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'vm_name', 'is_time': False}, {'field': 'vm_state', 'type': 'tinyint', 'type_flask': 'db.Boolean', 'type_sqlalchemy': 'Boolean', 'null': 'YES', 'key': '', 'default': '1', 'extra': '', 'is_form_editable': True, 'format': None, 'order': 5, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'BooleanField', 'is_id': False, 'header': 'vm_state', 'is_time': False}, {'field': 'vm_has_pd', 'type': 'tinyint', 'type_flask': 'db.Boolean', 'type_sqlalchemy': 'Boolean', 'null': 'YES', 'key': '', 'default': '0', 'extra': '', 'is_form_editable': True, 'format': None, 'order': 6, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'BooleanField', 'is_id': False, 'header': 'vm_has_pd', 'is_time': False}, {'field': 'vm_pd_name', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 7, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'vm_pd_name', 'is_time': False}, {'field': 'vm_pd_active', 'type': 'tinyint', 'type_flask': 'db.Boolean', 'type_sqlalchemy': 'Boolean', 'null': 'YES', 'key': '', 'default': '0', 'extra': '', 'is_form_editable': True, 'format': None, 'order': 8, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'BooleanField', 'is_id': False, 'header': 'vm_pd_active', 'is_time': False}, {'field': 'vm_pd_replicating', 'type': 'tinyint', 'type_flask': 'db.Boolean', 'type_sqlalchemy': 'Boolean', 'null': 'YES', 'key': '', 'default': '0', 'extra': '', 'is_form_editable': True, 'format': None, 'order': 9, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'BooleanField', 'is_id': False, 'header': 'vm_pd_replicating', 'is_time': False}, {'field': 'vm_pd_schedules', 'type': 'int', 'type_flask': 'db.Integer', 'type_sqlalchemy': 'Integer', 'null': 'YES', 'key': '', 'default': '0', 'extra': '', 'is_form_editable': True, 'format': None, 'order': 10, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'IntegerField', 'is_id': False, 'header': 'vm_pd_schedules', 'is_time': False}, {'field': 'vm_last_replication', 'type': 'timestamp', 'type_flask': 'db.DateTime', 'type_sqlalchemy': 'DateTime', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 11, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'DateTimeField', 'is_id': False, 'header': 'vm_last_replication', 'is_time': False}, {'field': 'vm_migrate', 'type': 'tinyint', 'type_flask': 'db.Boolean', 'type_sqlalchemy': 'Boolean', 'null': 'YES', 'key': '', 'default': '0', 'extra': '', 'is_form_editable': True, 'format': None, 'order': 12, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'BooleanField', 'is_id': False, 'header': 'vm_migrate', 'is_time': False}, {'field': 'vm_project', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 13, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'vm_project', 'is_time': False}]

        return __list

    def get_column_headers(self):
        """ Gets Migration_Groups_VM record column headers list """
        __list=['MG_Id', 'vm_uuid', 'vm_cluster_uuid', 'vm_name', 'vm_state', 'vm_has_pd', 'vm_pd_name', 'vm_pd_active', 'vm_pd_replicating', 'vm_pd_schedules', 'vm_last_replication', 'vm_migrate', 'vm_project']

        return __list

    def get_column_types(self):
        """ Gets Migration_Groups_VM record column data types list """
        __list=['Integer', 'String(45)', 'String(45)', 'String(256)', 'Boolean', 'Boolean', 'String(45)', 'Boolean', 'Boolean', 'Integer', 'DateTime', 'Boolean', 'String(45)']

        return __list

    def get_column_meta(self):
        """ Gets Migration_Groups_VM record column data meta list """
        __list=[('MG_Id', 'Integer'), ('vm_uuid', 'String(45)'), ('vm_cluster_uuid', 'String(45)'), ('vm_name', 'String(256)'), ('vm_state', 'Boolean'), ('vm_has_pd', 'Boolean'), ('vm_pd_name', 'String(45)'), ('vm_pd_active', 'Boolean'), ('vm_pd_replicating', 'Boolean'), ('vm_pd_schedules', 'Integer'), ('vm_last_replication', 'DateTime'), ('vm_migrate', 'Boolean'), ('vm_project', 'String(45)')]

        return __list

    def search_key(self,MG_Id,vm_uuid):
        """ Search for an unique Migration_Groups_VM record using all key fields (MG_Id,vm_uuid) """
        try:
            if self.engine is not None:
                Session=sessionmaker(bind=self.engine)
                session=Session()
                record = session.query(Migration_Groups_VM).filter(Migration_Groups_VM.MG_Id==MG_Id).filter(Migration_Groups_VM.vm_uuid==vm_uuid).one_or_none()
                session.flush()
            else:
                session.rollback()
                record = None
        except Exception as e:
            detail='Migration_Groups_VM.search_key(%s,%s): Exception: %s'%(MG_Id,vm_uuid,e)
            emtec_handle_general_exception(e,detail=detail,module=__name__,function='Migration_Groups_VM.search_key()',logger=self.logger)
            record = None
        return record

    def log(self,message,level=logging.DEBUG):
        """ Class Migration_Groups_VM log function """
        if self.logger is not None:
            self.logger.log(level,message)

# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2022-03-24 17:50:52
# =============================================================================

# gen_model_flask.py:865 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/models/orm_migration_groups_vm.py
# gen_model_flask.py:866 Table sharding code follows:
def get_Migration_Groups_VM(table_name_suffix):
  class Migration_Groups_VM_Class(Base):
    __tablename__ = 'Migration_Groups_VM_%s'%(table_name_suffix)
    engine        = None
    logger        = None

    def set_shard(suffix=None,engine=None):
       if suffix is not None:
           name='Migration_Groups_VM_{suffix}'.format(suffix=suffix)
           __class__.__tablename__  = name
           __class__.__table_args__ = {'extend_existing':True}
           __class__.__table__.name = name
           __class__.check_shard(suffix,engine)
       return __class__.__tablename__

    MG_Id               = Column( Integer, ForeignKey('Migration_Groups.MG_Id'), primary_key=True )
    vm_uuid             = Column( String(45), primary_key=True )
    vm_cluster_uuid     = Column( String(45) )
    vm_name             = Column( String(256) )
    vm_state            = Column( Boolean )
    vm_has_pd           = Column( Boolean )
    vm_pd_name          = Column( String(45) )
    vm_pd_active        = Column( Boolean )
    vm_pd_replicating   = Column( Boolean )
    vm_pd_schedules     = Column( Integer )
    vm_last_replication = Column( DateTime )
    vm_migrate          = Column( Boolean )
    vm_project          = Column( String(45) )
    
    def __init__(self, MG_Id=None, vm_uuid='None', vm_cluster_uuid='None', vm_name='None', vm_state=1, vm_has_pd=0, vm_pd_name='None', vm_pd_active=0, vm_pd_replicating=0, vm_pd_schedules=0, vm_last_replication=None, vm_migrate=0, vm_project='None',engine=None,logger=None):
        """ Initiates a Migration_Groups_VM class record """
        self.engine=engine
        self.logger=logger
        self.MG_Id               = MG_Id
        self.vm_uuid             = vm_uuid
        self.vm_cluster_uuid     = vm_cluster_uuid
        self.vm_name             = vm_name
        self.vm_state            = vm_state
        self.vm_has_pd           = vm_has_pd
        self.vm_pd_name          = vm_pd_name
        self.vm_pd_active        = vm_pd_active
        self.vm_pd_replicating   = vm_pd_replicating
        self.vm_pd_schedules     = vm_pd_schedules
        self.vm_last_replication = vm_last_replication
        self.vm_migrate          = vm_migrate
        self.vm_project          = vm_project

        self.log('Created %s'%self)
    def __repr__(self):
        """ default class Migration_Groups_VM representation function """
        return "<Migration_Groups_VM( MG_Id='%s', vm_uuid='%s', vm_cluster_uuid='%s', vm_name='%s', vm_state='%s', vm_has_pd='%s', vm_pd_name='%s', vm_pd_active='%s', vm_pd_replicating='%s', vm_pd_schedules='%s', vm_last_replication='%s', vm_migrate='%s', vm_project='%s')>" % \
                ( self.MG_Id, self.vm_uuid, self.vm_cluster_uuid, self.vm_name, self.vm_state, self.vm_has_pd, self.vm_pd_name, self.vm_pd_active, self.vm_pd_replicating, self.vm_pd_schedules, self.vm_last_replication, self.vm_migrate, self.vm_project)

    def get_list(self):
        """ Gets Migration_Groups_VM record in list format """
        __list = [ self.MG_Id, self.vm_uuid, self.vm_cluster_uuid, self.vm_name, self.vm_state, self.vm_has_pd, self.vm_pd_name, self.vm_pd_active, self.vm_pd_replicating, self.vm_pd_schedules, self.vm_last_replication, self.vm_migrate, self.vm_project]
        return __list

    def get_tuple(self):
        """ Gets Migration_Groups_VM record in tuple format """
        __tuple = ( self.MG_Id, self.vm_uuid, self.vm_cluster_uuid, self.vm_name, self.vm_state, self.vm_has_pd, self.vm_pd_name, self.vm_pd_active, self.vm_pd_replicating, self.vm_pd_schedules, self.vm_last_replication, self.vm_migrate, self.vm_project)
        return __tuple

    def get_dict(self):
        """ Gets Migration_Groups_VM record in dict format """
        __dict={'MG_Id':self.MG_Id,'vm_uuid':self.vm_uuid,'vm_cluster_uuid':self.vm_cluster_uuid,'vm_name':self.vm_name,'vm_state':self.vm_state,'vm_has_pd':self.vm_has_pd,'vm_pd_name':self.vm_pd_name,'vm_pd_active':self.vm_pd_active,'vm_pd_replicating':self.vm_pd_replicating,'vm_pd_schedules':self.vm_pd_schedules,'vm_last_replication':self.vm_last_replication,'vm_migrate':self.vm_migrate,'vm_project':self.vm_project}

        return __dict

    def get_json_dict(self,dateformat='%Y-%m-%d',timeformat='%H:%M:%S',datetimeformat=None):
        __dict = self.get_dict()
        if datetimeformat is None: 
            datetimeformat='%s %s'%(dateformat,timeformat)
        for key in __dict.keys():
            if   'datetime.datetime' in str(type(__dict[key])): __dict[key]=__dict[key].strftime(datetimeformat)
            elif 'datetime.date'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(dateformat)
            elif 'datetime.time'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(timeformat)
            elif 'decimal.Decimal'   in str(type(__dict[key])): __dict[key]=float(__dict[key])
        return __dict

    def get_json(self,dateformat='%Y-%m-%d',timeformat='%H:%M:%S',datetimeformat=None):
        __dict = self.get_dict()
        if datetimeformat is None: 
            datetimeformat='%s %s'%(dateformat,timeformat)
        for key in __dict.keys():
            if   'datetime.datetime' in str(type(__dict[key])): __dict[key]=__dict[key].strftime(datetimeformat)
            elif 'datetime.date'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(dateformat)
            elif 'datetime.time'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(timeformat)
            elif 'decimal.Decimal'   in str(type(__dict[key])): __dict[key]=float(__dict[key])
        return json.dumps(__dict)

    def post(self):
       return self

    def patch(self,**kwargs):
       for field in self.get_column_headers():
           if field in kwargs.keys():
               setattr(self,field,kwargs[field])
       return self

    def delete(self):
       return True

    def get_json_array(self,dateformat='%Y-%m-%d',timeformat='%H:%M:%S',datetimeformat=None):
        """ Gets Migration_Groups_VM record in JSON array format """
        __list = self.get_list()
        if datetimeformat is None: 
            datetimeformat='%s %s'%(dateformat,timeformat)
        for field in range(len(__list)):
            if   'datetime.datetime' in str(type(__list[field])): __list[field]=__list[field].strftime(datetimeformat)
            elif 'datetime.date'     in str(type(__list[field])): __list[field]=__list[field].strftime(dateformat)
            elif 'datetime.time'     in str(type(__list[field])): __list[field]=__list[field].strftime(timeformat)
            elif 'decimal.Decimal'   in str(type(__list[field])): __list[field]=float(__list[field])
        return __list

    def get_columns(self):
        """ Gets Migration_Groups_VM record column full details list """
        __list=[{'field': 'MG_Id', 'type': 'int', 'type_flask': 'db.Integer', 'type_sqlalchemy': 'Integer', 'null': 'NO', 'key': 'PRI', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 1, 'is_searchable': True, 'is_fk': True, 'referenced_table': 'Migration_Groups', 'referenced_class': 'migration_groups', 'foreign_key': 'MG_Id', 'foreign_field': 'MG_Id', 'foreign_value': 'Name', 'is_numeric': False, 'form_type': 'SelectField', 'is_id': False, 'header': 'MG_Id', 'is_time': False}, {'field': 'vm_uuid', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'NO', 'key': 'PRI', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 2, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'vm_uuid', 'is_time': False}, {'field': 'vm_cluster_uuid', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 3, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'vm_cluster_uuid', 'is_time': False}, {'field': 'vm_name', 'type': 'varchar(256)', 'type_flask': 'db.String(256)', 'type_sqlalchemy': 'String(256)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 4, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'vm_name', 'is_time': False}, {'field': 'vm_state', 'type': 'tinyint', 'type_flask': 'db.Boolean', 'type_sqlalchemy': 'Boolean', 'null': 'YES', 'key': '', 'default': '1', 'extra': '', 'is_form_editable': True, 'format': None, 'order': 5, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'BooleanField', 'is_id': False, 'header': 'vm_state', 'is_time': False}, {'field': 'vm_has_pd', 'type': 'tinyint', 'type_flask': 'db.Boolean', 'type_sqlalchemy': 'Boolean', 'null': 'YES', 'key': '', 'default': '0', 'extra': '', 'is_form_editable': True, 'format': None, 'order': 6, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'BooleanField', 'is_id': False, 'header': 'vm_has_pd', 'is_time': False}, {'field': 'vm_pd_name', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 7, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'vm_pd_name', 'is_time': False}, {'field': 'vm_pd_active', 'type': 'tinyint', 'type_flask': 'db.Boolean', 'type_sqlalchemy': 'Boolean', 'null': 'YES', 'key': '', 'default': '0', 'extra': '', 'is_form_editable': True, 'format': None, 'order': 8, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'BooleanField', 'is_id': False, 'header': 'vm_pd_active', 'is_time': False}, {'field': 'vm_pd_replicating', 'type': 'tinyint', 'type_flask': 'db.Boolean', 'type_sqlalchemy': 'Boolean', 'null': 'YES', 'key': '', 'default': '0', 'extra': '', 'is_form_editable': True, 'format': None, 'order': 9, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'BooleanField', 'is_id': False, 'header': 'vm_pd_replicating', 'is_time': False}, {'field': 'vm_pd_schedules', 'type': 'int', 'type_flask': 'db.Integer', 'type_sqlalchemy': 'Integer', 'null': 'YES', 'key': '', 'default': '0', 'extra': '', 'is_form_editable': True, 'format': None, 'order': 10, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'IntegerField', 'is_id': False, 'header': 'vm_pd_schedules', 'is_time': False}, {'field': 'vm_last_replication', 'type': 'timestamp', 'type_flask': 'db.DateTime', 'type_sqlalchemy': 'DateTime', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 11, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'DateTimeField', 'is_id': False, 'header': 'vm_last_replication', 'is_time': False}, {'field': 'vm_migrate', 'type': 'tinyint', 'type_flask': 'db.Boolean', 'type_sqlalchemy': 'Boolean', 'null': 'YES', 'key': '', 'default': '0', 'extra': '', 'is_form_editable': True, 'format': None, 'order': 12, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'BooleanField', 'is_id': False, 'header': 'vm_migrate', 'is_time': False}, {'field': 'vm_project', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 13, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'vm_project', 'is_time': False}]

        return __list

    def get_column_headers(self):
        """ Gets Migration_Groups_VM record column headers list """
        __list=['MG_Id', 'vm_uuid', 'vm_cluster_uuid', 'vm_name', 'vm_state', 'vm_has_pd', 'vm_pd_name', 'vm_pd_active', 'vm_pd_replicating', 'vm_pd_schedules', 'vm_last_replication', 'vm_migrate', 'vm_project']

        return __list

    def get_column_types(self):
        """ Gets Migration_Groups_VM record column data types list """
        __list=['Integer', 'String(45)', 'String(45)', 'String(256)', 'Boolean', 'Boolean', 'String(45)', 'Boolean', 'Boolean', 'Integer', 'DateTime', 'Boolean', 'String(45)']

        return __list

    def get_column_meta(self):
        """ Gets Migration_Groups_VM record column data meta list """
        __list=[('MG_Id', 'Integer'), ('vm_uuid', 'String(45)'), ('vm_cluster_uuid', 'String(45)'), ('vm_name', 'String(256)'), ('vm_state', 'Boolean'), ('vm_has_pd', 'Boolean'), ('vm_pd_name', 'String(45)'), ('vm_pd_active', 'Boolean'), ('vm_pd_replicating', 'Boolean'), ('vm_pd_schedules', 'Integer'), ('vm_last_replication', 'DateTime'), ('vm_migrate', 'Boolean'), ('vm_project', 'String(45)')]

        return __list

    def search_key(self,MG_Id,vm_uuid):
        """ Search for an unique Migration_Groups_VM record using all key fields (MG_Id,vm_uuid) """
        try:
            if self.engine is not None:
                Session=sessionmaker(bind=self.engine)
                session=Session()
                record = session.query(Migration_Groups_VM).filter(Migration_Groups_VM.MG_Id==MG_Id).filter(Migration_Groups_VM.vm_uuid==vm_uuid).one_or_none()
                session.flush()
            else:
                session.rollback()
                record = None
        except Exception as e:
            detail='Migration_Groups_VM.search_key(%s,%s): Exception: %s'%(MG_Id,vm_uuid,e)
            emtec_handle_general_exception(e,detail=detail,module=__name__,function='Migration_Groups_VM.search_key()',logger=self.logger)
            record = None
        return record

    def log(self,message,level=logging.DEBUG):
        """ Class Migration_Groups_VM log function """
        if self.logger is not None:
            self.logger.log(level,message)

  Migration_Groups_VM_Class.__name__ = 'Migration_Groups_VM_%s'%(table_name_suffix)
  x = Migration_Groups_VM_Class
  return x

# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2022-03-24 17:50:52
# =============================================================================

# GV gen_model_flask.py:418 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/models/orm_nutanix_prism_vm.py
import sqlalchemy
class Nutanix_Prism_VM(Base):
    __tablename__ = 'Nutanix_Prism_VM'
    engine        = None
    logger        = None

    def check_shard(suffix=None,engine=None):
       if engine is not None:
           try:
               if sqlalchemy.__version__ >= '1.4':
                   inspector = sqlalchemy.inspect(engine)
                   table_exists = inspector.has_table(__class__.__tablename__,schema='butler')
               else:
                   table_exists = engine.dialect.has_table(engine, __class__.__tablename__)
               if not table_exists:
                   metadata=MetaData()
                   metadata.bind=engine
                   __class__.__table__.metadata=metadata
                   __class__.__table__.create(checkfirst=True)
                   if sqlalchemy.__version__ >= '1.4':
                       inspector = sqlalchemy.inspect(engine)
                       table_exists = inspector.has_table(__class__.__tablename__,schema='butler')
                   else:
                       table_exists = engine.dialect.has_table(engine, __class__.__tablename__)
                   if not table_exists:
                       print('460 Table %s does not exist. creation error?'% __class__.__tablename__)
                   else:
                       pass # GV print('462 Table %s exist !!!'% __class__.__tablename__)
               else:
                   pass # GV print('464 Table %s exist !!!'% __class__.__tablename__)
           except Exception as e:
              print(f'gen/gen_model_flask.py: 466 exception: {str(e)}')
           return
    def set_shard(suffix=None,engine=None):
       if suffix is not None:
           name='Nutanix_Prism_VM_{suffix}'.format(suffix=suffix)
           __class__.__tablename__  = name
           __class__.__table__.name = name
       __class__.check_shard(suffix,engine)
       return __class__.__tablename__

    Request_Id       = Column( Integer, ForeignKey('Requests.Id'), primary_key=True )
    project_uuid     = Column( String(45), ForeignKey('Projects.project_uuid') )
    category_name    = Column( String(45), ForeignKey('Categories.category_name') )
    cluster_uuid     = Column( String(45), ForeignKey('Clusters.cluster_uuid') )
    vm_name          = Column( String(45) )
    power_state      = Column( Boolean )
    vcpus_per_socket = Column( Integer )
    num_sockets      = Column( Integer )
    memory_size_mib  = Column( Integer )
    memory_size_gib  = Column( Integer )
    Comments         = Column( Text )
    vm_uuid          = Column( String(45) )
    vm_ip            = Column( String(45) )
    subnet_uuid      = Column( String(45), ForeignKey('Subnets.uuid') )
    vm_username      = Column( String(45) )
    vm_password      = Column( String(45) )
    backup_set_1     = Column( Boolean )
    backup_set_2     = Column( Boolean )
    backup_set_3     = Column( Boolean )
    disk_type        = Column( Integer )
    disk_0_image     = Column( String(45) )
    disk_0_size      = Column( Integer )
    disk_1_image     = Column( String(45) )
    disk_1_size      = Column( Integer )
    disk_2_image     = Column( String(45) )
    disk_2_size      = Column( Integer )
    disk_3_image     = Column( String(45) )
    disk_3_size      = Column( Integer )
    disk_4_image     = Column( String(45) )
    disk_4_size      = Column( Integer )
    disk_5_image     = Column( String(45) )
    disk_5_size      = Column( Integer )
    disk_6_image     = Column( String(45) )
    disk_6_size      = Column( Integer )
    disk_7_image     = Column( String(45) )
    disk_7_size      = Column( Integer )
    disk_8_image     = Column( String(45) )
    disk_8_size      = Column( Integer )
    disk_9_image     = Column( String(45) )
    disk_9_size      = Column( Integer )
    disk_10_image    = Column( String(45) )
    disk_10_size     = Column( Integer )
    disk_11_image    = Column( String(45) )
    disk_11_size     = Column( Integer )
    vm_drp           = Column( Boolean )
    vm_drp_remote    = Column( Boolean )
    vm_cdrom         = Column( Boolean )
    drp_cluster_uuid = Column( String(45) )
    nic_0_vlan       = Column( String(45) )
    nic_0_ip         = Column( String(45) )
    nic_0_mac        = Column( String(45) )
    nic_1_vlan       = Column( String(45) )
    nic_1_ip         = Column( String(45) )
    nic_1_mac        = Column( String(45) )
    nic_2_vlan       = Column( String(45) )
    nic_2_ip         = Column( String(45) )
    nic_2_mac        = Column( String(45) )
    nic_3_vlan       = Column( String(45) )
    nic_3_ip         = Column( String(45) )
    nic_3_mac        = Column( String(45) )
    request_text     = Column( Text )
    
    def __init__(self, Request_Id=None, project_uuid='None', category_name='None', cluster_uuid='None', vm_name='None', power_state=1, vcpus_per_socket=1, num_sockets=1, memory_size_mib=0, memory_size_gib=0, Comments=None, vm_uuid='None', vm_ip='None', subnet_uuid='None', vm_username='None', vm_password='None', backup_set_1=0, backup_set_2=0, backup_set_3=0, disk_type=0, disk_0_image='None', disk_0_size=0, disk_1_image='None', disk_1_size=0, disk_2_image='None', disk_2_size=0, disk_3_image='None', disk_3_size=0, disk_4_image='None', disk_4_size=0, disk_5_image='None', disk_5_size=0, disk_6_image='None', disk_6_size=0, disk_7_image='None', disk_7_size=0, disk_8_image='None', disk_8_size=0, disk_9_image='None', disk_9_size=0, disk_10_image='None', disk_10_size=0, disk_11_image='None', disk_11_size=0, vm_drp=0, vm_drp_remote=0, vm_cdrom=0, drp_cluster_uuid='None', nic_0_vlan='None', nic_0_ip='None', nic_0_mac='None', nic_1_vlan='None', nic_1_ip='None', nic_1_mac='None', nic_2_vlan='None', nic_2_ip='None', nic_2_mac='None', nic_3_vlan='None', nic_3_ip='None', nic_3_mac='None', request_text=None,engine=None,logger=None):
        """ Initiates a Nutanix_Prism_VM class record """
        self.engine=engine
        self.logger=logger
        self.Request_Id       = Request_Id
        self.project_uuid     = project_uuid
        self.category_name    = category_name
        self.cluster_uuid     = cluster_uuid
        self.vm_name          = vm_name
        self.power_state      = power_state
        self.vcpus_per_socket = vcpus_per_socket
        self.num_sockets      = num_sockets
        self.memory_size_mib  = memory_size_mib
        self.memory_size_gib  = memory_size_gib
        self.Comments         = Comments
        self.vm_uuid          = vm_uuid
        self.vm_ip            = vm_ip
        self.subnet_uuid      = subnet_uuid
        self.vm_username      = vm_username
        self.vm_password      = vm_password
        self.backup_set_1     = backup_set_1
        self.backup_set_2     = backup_set_2
        self.backup_set_3     = backup_set_3
        self.disk_type        = disk_type
        self.disk_0_image     = disk_0_image
        self.disk_0_size      = disk_0_size
        self.disk_1_image     = disk_1_image
        self.disk_1_size      = disk_1_size
        self.disk_2_image     = disk_2_image
        self.disk_2_size      = disk_2_size
        self.disk_3_image     = disk_3_image
        self.disk_3_size      = disk_3_size
        self.disk_4_image     = disk_4_image
        self.disk_4_size      = disk_4_size
        self.disk_5_image     = disk_5_image
        self.disk_5_size      = disk_5_size
        self.disk_6_image     = disk_6_image
        self.disk_6_size      = disk_6_size
        self.disk_7_image     = disk_7_image
        self.disk_7_size      = disk_7_size
        self.disk_8_image     = disk_8_image
        self.disk_8_size      = disk_8_size
        self.disk_9_image     = disk_9_image
        self.disk_9_size      = disk_9_size
        self.disk_10_image    = disk_10_image
        self.disk_10_size     = disk_10_size
        self.disk_11_image    = disk_11_image
        self.disk_11_size     = disk_11_size
        self.vm_drp           = vm_drp
        self.vm_drp_remote    = vm_drp_remote
        self.vm_cdrom         = vm_cdrom
        self.drp_cluster_uuid = drp_cluster_uuid
        self.nic_0_vlan       = nic_0_vlan
        self.nic_0_ip         = nic_0_ip
        self.nic_0_mac        = nic_0_mac
        self.nic_1_vlan       = nic_1_vlan
        self.nic_1_ip         = nic_1_ip
        self.nic_1_mac        = nic_1_mac
        self.nic_2_vlan       = nic_2_vlan
        self.nic_2_ip         = nic_2_ip
        self.nic_2_mac        = nic_2_mac
        self.nic_3_vlan       = nic_3_vlan
        self.nic_3_ip         = nic_3_ip
        self.nic_3_mac        = nic_3_mac
        self.request_text     = request_text

        self.log('Created %s'%self)
    def __repr__(self):
        """ default class Nutanix_Prism_VM representation function """
        return "<Nutanix_Prism_VM( Request_Id='%s', project_uuid='%s', category_name='%s', cluster_uuid='%s', vm_name='%s', power_state='%s', vcpus_per_socket='%s', num_sockets='%s', memory_size_mib='%s', memory_size_gib='%s', Comments='%s', vm_uuid='%s', vm_ip='%s', subnet_uuid='%s', vm_username='%s', vm_password='%s', backup_set_1='%s', backup_set_2='%s', backup_set_3='%s', disk_type='%s', disk_0_image='%s', disk_0_size='%s', disk_1_image='%s', disk_1_size='%s', disk_2_image='%s', disk_2_size='%s', disk_3_image='%s', disk_3_size='%s', disk_4_image='%s', disk_4_size='%s', disk_5_image='%s', disk_5_size='%s', disk_6_image='%s', disk_6_size='%s', disk_7_image='%s', disk_7_size='%s', disk_8_image='%s', disk_8_size='%s', disk_9_image='%s', disk_9_size='%s', disk_10_image='%s', disk_10_size='%s', disk_11_image='%s', disk_11_size='%s', vm_drp='%s', vm_drp_remote='%s', vm_cdrom='%s', drp_cluster_uuid='%s', nic_0_vlan='%s', nic_0_ip='%s', nic_0_mac='%s', nic_1_vlan='%s', nic_1_ip='%s', nic_1_mac='%s', nic_2_vlan='%s', nic_2_ip='%s', nic_2_mac='%s', nic_3_vlan='%s', nic_3_ip='%s', nic_3_mac='%s', request_text='%s')>" % \
                ( self.Request_Id, self.project_uuid, self.category_name, self.cluster_uuid, self.vm_name, self.power_state, self.vcpus_per_socket, self.num_sockets, self.memory_size_mib, self.memory_size_gib, self.Comments, self.vm_uuid, self.vm_ip, self.subnet_uuid, self.vm_username, self.vm_password, self.backup_set_1, self.backup_set_2, self.backup_set_3, self.disk_type, self.disk_0_image, self.disk_0_size, self.disk_1_image, self.disk_1_size, self.disk_2_image, self.disk_2_size, self.disk_3_image, self.disk_3_size, self.disk_4_image, self.disk_4_size, self.disk_5_image, self.disk_5_size, self.disk_6_image, self.disk_6_size, self.disk_7_image, self.disk_7_size, self.disk_8_image, self.disk_8_size, self.disk_9_image, self.disk_9_size, self.disk_10_image, self.disk_10_size, self.disk_11_image, self.disk_11_size, self.vm_drp, self.vm_drp_remote, self.vm_cdrom, self.drp_cluster_uuid, self.nic_0_vlan, self.nic_0_ip, self.nic_0_mac, self.nic_1_vlan, self.nic_1_ip, self.nic_1_mac, self.nic_2_vlan, self.nic_2_ip, self.nic_2_mac, self.nic_3_vlan, self.nic_3_ip, self.nic_3_mac, self.request_text)

    def get_list(self):
        """ Gets Nutanix_Prism_VM record in list format """
        __list = [ self.Request_Id, self.project_uuid, self.category_name, self.cluster_uuid, self.vm_name, self.power_state, self.vcpus_per_socket, self.num_sockets, self.memory_size_mib, self.memory_size_gib, self.Comments, self.vm_uuid, self.vm_ip, self.subnet_uuid, self.vm_username, self.vm_password, self.backup_set_1, self.backup_set_2, self.backup_set_3, self.disk_type, self.disk_0_image, self.disk_0_size, self.disk_1_image, self.disk_1_size, self.disk_2_image, self.disk_2_size, self.disk_3_image, self.disk_3_size, self.disk_4_image, self.disk_4_size, self.disk_5_image, self.disk_5_size, self.disk_6_image, self.disk_6_size, self.disk_7_image, self.disk_7_size, self.disk_8_image, self.disk_8_size, self.disk_9_image, self.disk_9_size, self.disk_10_image, self.disk_10_size, self.disk_11_image, self.disk_11_size, self.vm_drp, self.vm_drp_remote, self.vm_cdrom, self.drp_cluster_uuid, self.nic_0_vlan, self.nic_0_ip, self.nic_0_mac, self.nic_1_vlan, self.nic_1_ip, self.nic_1_mac, self.nic_2_vlan, self.nic_2_ip, self.nic_2_mac, self.nic_3_vlan, self.nic_3_ip, self.nic_3_mac, self.request_text]
        return __list

    def get_tuple(self):
        """ Gets Nutanix_Prism_VM record in tuple format """
        __tuple = ( self.Request_Id, self.project_uuid, self.category_name, self.cluster_uuid, self.vm_name, self.power_state, self.vcpus_per_socket, self.num_sockets, self.memory_size_mib, self.memory_size_gib, self.Comments, self.vm_uuid, self.vm_ip, self.subnet_uuid, self.vm_username, self.vm_password, self.backup_set_1, self.backup_set_2, self.backup_set_3, self.disk_type, self.disk_0_image, self.disk_0_size, self.disk_1_image, self.disk_1_size, self.disk_2_image, self.disk_2_size, self.disk_3_image, self.disk_3_size, self.disk_4_image, self.disk_4_size, self.disk_5_image, self.disk_5_size, self.disk_6_image, self.disk_6_size, self.disk_7_image, self.disk_7_size, self.disk_8_image, self.disk_8_size, self.disk_9_image, self.disk_9_size, self.disk_10_image, self.disk_10_size, self.disk_11_image, self.disk_11_size, self.vm_drp, self.vm_drp_remote, self.vm_cdrom, self.drp_cluster_uuid, self.nic_0_vlan, self.nic_0_ip, self.nic_0_mac, self.nic_1_vlan, self.nic_1_ip, self.nic_1_mac, self.nic_2_vlan, self.nic_2_ip, self.nic_2_mac, self.nic_3_vlan, self.nic_3_ip, self.nic_3_mac, self.request_text)
        return __tuple

    def get_dict(self):
        """ Gets Nutanix_Prism_VM record in dict format """
        __dict={'Request_Id':self.Request_Id,'project_uuid':self.project_uuid,'category_name':self.category_name,'cluster_uuid':self.cluster_uuid,'vm_name':self.vm_name,'power_state':self.power_state,'vcpus_per_socket':self.vcpus_per_socket,'num_sockets':self.num_sockets,'memory_size_mib':self.memory_size_mib,'memory_size_gib':self.memory_size_gib,'Comments':self.Comments,'vm_uuid':self.vm_uuid,'vm_ip':self.vm_ip,'subnet_uuid':self.subnet_uuid,'vm_username':self.vm_username,'vm_password':self.vm_password,'backup_set_1':self.backup_set_1,'backup_set_2':self.backup_set_2,'backup_set_3':self.backup_set_3,'disk_type':self.disk_type,'disk_0_image':self.disk_0_image,'disk_0_size':self.disk_0_size,'disk_1_image':self.disk_1_image,'disk_1_size':self.disk_1_size,'disk_2_image':self.disk_2_image,'disk_2_size':self.disk_2_size,'disk_3_image':self.disk_3_image,'disk_3_size':self.disk_3_size,'disk_4_image':self.disk_4_image,'disk_4_size':self.disk_4_size,'disk_5_image':self.disk_5_image,'disk_5_size':self.disk_5_size,'disk_6_image':self.disk_6_image,'disk_6_size':self.disk_6_size,'disk_7_image':self.disk_7_image,'disk_7_size':self.disk_7_size,'disk_8_image':self.disk_8_image,'disk_8_size':self.disk_8_size,'disk_9_image':self.disk_9_image,'disk_9_size':self.disk_9_size,'disk_10_image':self.disk_10_image,'disk_10_size':self.disk_10_size,'disk_11_image':self.disk_11_image,'disk_11_size':self.disk_11_size,'vm_drp':self.vm_drp,'vm_drp_remote':self.vm_drp_remote,'vm_cdrom':self.vm_cdrom,'drp_cluster_uuid':self.drp_cluster_uuid,'nic_0_vlan':self.nic_0_vlan,'nic_0_ip':self.nic_0_ip,'nic_0_mac':self.nic_0_mac,'nic_1_vlan':self.nic_1_vlan,'nic_1_ip':self.nic_1_ip,'nic_1_mac':self.nic_1_mac,'nic_2_vlan':self.nic_2_vlan,'nic_2_ip':self.nic_2_ip,'nic_2_mac':self.nic_2_mac,'nic_3_vlan':self.nic_3_vlan,'nic_3_ip':self.nic_3_ip,'nic_3_mac':self.nic_3_mac,'request_text':self.request_text}

        return __dict

    def get_json_dict(self,dateformat='%Y-%m-%d',timeformat='%H:%M:%S',datetimeformat=None):
        __dict = self.get_dict()
        if datetimeformat is None: 
            datetimeformat='%s %s'%(dateformat,timeformat)
        for key in __dict.keys():
            if   'datetime.datetime' in str(type(__dict[key])): __dict[key]=__dict[key].strftime(datetimeformat)
            elif 'datetime.date'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(dateformat)
            elif 'datetime.time'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(timeformat)
            elif 'decimal.Decimal'   in str(type(__dict[key])): __dict[key]=float(__dict[key])
        return __dict

    def get_json(self,dateformat='%Y-%m-%d',timeformat='%H:%M:%S',datetimeformat=None):
        __dict = self.get_dict()
        if datetimeformat is None: 
            datetimeformat='%s %s'%(dateformat,timeformat)
        for key in __dict.keys():
            if   'datetime.datetime' in str(type(__dict[key])): __dict[key]=__dict[key].strftime(datetimeformat)
            elif 'datetime.date'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(dateformat)
            elif 'datetime.time'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(timeformat)
            elif 'decimal.Decimal'   in str(type(__dict[key])): __dict[key]=float(__dict[key])
        return json.dumps(__dict)

    def post(self):
       return self

    def patch(self,**kwargs):
       for field in self.get_column_headers():
           if field in kwargs.keys():
               setattr(self,field,kwargs[field])
       return self

    def delete(self):
       return True

    def get_json_array(self,dateformat='%Y-%m-%d',timeformat='%H:%M:%S',datetimeformat=None):
        """ Gets Nutanix_Prism_VM record in JSON array format """
        __list = self.get_list()
        if datetimeformat is None: 
            datetimeformat='%s %s'%(dateformat,timeformat)
        for field in range(len(__list)):
            if   'datetime.datetime' in str(type(__list[field])): __list[field]=__list[field].strftime(datetimeformat)
            elif 'datetime.date'     in str(type(__list[field])): __list[field]=__list[field].strftime(dateformat)
            elif 'datetime.time'     in str(type(__list[field])): __list[field]=__list[field].strftime(timeformat)
            elif 'decimal.Decimal'   in str(type(__list[field])): __list[field]=float(__list[field])
        return __list

    def get_columns(self):
        """ Gets Nutanix_Prism_VM record column full details list """
        __list=[{'field': 'Request_Id', 'type': 'int', 'type_flask': 'db.Integer', 'type_sqlalchemy': 'Integer', 'null': 'NO', 'key': 'PRI', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 1, 'is_searchable': True, 'is_fk': True, 'foreign_field': 'Id', 'referenced_table': 'Requests', 'referenced_class': 'requests', 'foreign_key': 'Request_Id', 'foreign_value': 'Id', 'is_numeric': False, 'form_type': 'SelectField', 'is_id': False, 'header': 'Request_Id', 'is_time': False}, {'field': 'project_uuid', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'NO', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 2, 'is_searchable': True, 'is_fk': True, 'foreign_field': 'project_uuid', 'referenced_table': 'Projects', 'referenced_class': 'projects', 'foreign_key': 'project_uuid', 'foreign_value': 'project_name', 'is_numeric': False, 'form_type': 'SelectField', 'is_id': False, 'header': 'project_uuid', 'is_time': False}, {'field': 'category_name', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'NO', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 3, 'is_searchable': True, 'is_fk': True, 'foreign_field': 'category_name', 'referenced_table': 'Categories', 'referenced_class': 'categories', 'foreign_key': 'category_name', 'foreign_value': 'category_description', 'is_numeric': False, 'form_type': 'SelectField', 'is_id': False, 'header': 'category_name', 'is_time': False}, {'field': 'cluster_uuid', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'NO', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 4, 'is_searchable': True, 'is_fk': True, 'foreign_field': 'cluster_uuid', 'referenced_table': 'Clusters', 'referenced_class': 'clusters', 'foreign_key': 'cluster_uuid', 'foreign_value': 'cluster_name', 'is_numeric': False, 'form_type': 'SelectField', 'is_id': False, 'header': 'cluster_uuid', 'is_time': False}, {'field': 'vm_name', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'NO', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 5, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'vm_name', 'is_time': False}, {'field': 'power_state', 'type': 'tinyint', 'type_flask': 'db.Boolean', 'type_sqlalchemy': 'Boolean', 'null': 'YES', 'key': '', 'default': '1', 'extra': '', 'is_form_editable': True, 'format': None, 'order': 6, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'BooleanField', 'is_id': False, 'header': 'power_state', 'is_time': False}, {'field': 'vcpus_per_socket', 'type': 'int', 'type_flask': 'db.Integer', 'type_sqlalchemy': 'Integer', 'null': 'YES', 'key': '', 'default': '1', 'extra': '', 'is_form_editable': True, 'format': None, 'order': 7, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'IntegerField', 'is_id': False, 'header': 'vcpus_per_socket', 'is_time': False}, {'field': 'num_sockets', 'type': 'int', 'type_flask': 'db.Integer', 'type_sqlalchemy': 'Integer', 'null': 'YES', 'key': '', 'default': '1', 'extra': '', 'is_form_editable': True, 'format': None, 'order': 8, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'IntegerField', 'is_id': False, 'header': 'num_sockets', 'is_time': False}, {'field': 'memory_size_mib', 'type': 'int', 'type_flask': 'db.Integer', 'type_sqlalchemy': 'Integer', 'null': 'YES', 'key': '', 'default': '0', 'extra': '', 'is_form_editable': True, 'format': None, 'order': 9, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'IntegerField', 'is_id': False, 'header': 'memory_size_mib', 'is_time': False}, {'field': 'memory_size_gib', 'type': 'int', 'type_flask': 'db.Integer', 'type_sqlalchemy': 'Integer', 'null': 'YES', 'key': '', 'default': '0', 'extra': '', 'is_form_editable': True, 'format': None, 'order': 10, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'IntegerField', 'is_id': False, 'header': 'memory_size_gib', 'is_time': False}, {'field': 'Comments', 'type': 'text', 'type_flask': 'db.Text', 'type_sqlalchemy': 'Text', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 11, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'Comments', 'is_time': False}, {'field': 'vm_uuid', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 12, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'vm_uuid', 'is_time': False}, {'field': 'vm_ip', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 13, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'vm_ip', 'is_time': False}, {'field': 'subnet_uuid', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'NO', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 14, 'is_searchable': True, 'is_fk': True, 'foreign_field': 'uuid', 'referenced_table': 'Subnets', 'referenced_class': 'subnets', 'foreign_key': 'subnet_uuid', 'foreign_value': 'name', 'is_numeric': False, 'form_type': 'SelectField', 'is_id': False, 'header': 'subnet_uuid', 'is_time': False}, {'field': 'vm_username', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 15, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'vm_username', 'is_time': False}, {'field': 'vm_password', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 16, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'vm_password', 'is_time': False}, {'field': 'backup_set_1', 'type': 'tinyint', 'type_flask': 'db.Boolean', 'type_sqlalchemy': 'Boolean', 'null': 'YES', 'key': '', 'default': '0', 'extra': '', 'is_form_editable': True, 'format': None, 'order': 17, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'BooleanField', 'is_id': False, 'header': 'backup_set_1', 'is_time': False}, {'field': 'backup_set_2', 'type': 'tinyint', 'type_flask': 'db.Boolean', 'type_sqlalchemy': 'Boolean', 'null': 'YES', 'key': '', 'default': '0', 'extra': '', 'is_form_editable': True, 'format': None, 'order': 18, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'BooleanField', 'is_id': False, 'header': 'backup_set_2', 'is_time': False}, {'field': 'backup_set_3', 'type': 'tinyint', 'type_flask': 'db.Boolean', 'type_sqlalchemy': 'Boolean', 'null': 'YES', 'key': '', 'default': '0', 'extra': '', 'is_form_editable': True, 'format': None, 'order': 19, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'BooleanField', 'is_id': False, 'header': 'backup_set_3', 'is_time': False}, {'field': 'disk_type', 'type': 'int', 'type_flask': 'db.Integer', 'type_sqlalchemy': 'Integer', 'null': 'NO', 'key': '', 'default': '0', 'extra': '', 'is_form_editable': True, 'format': None, 'order': 20, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'IntegerField', 'is_id': False, 'header': 'disk_type', 'is_time': False}, {'field': 'disk_0_image', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 21, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'disk_0_image', 'is_time': False}, {'field': 'disk_0_size', 'type': 'int', 'type_flask': 'db.Integer', 'type_sqlalchemy': 'Integer', 'null': 'YES', 'key': '', 'default': '0', 'extra': '', 'is_form_editable': True, 'format': None, 'order': 22, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'IntegerField', 'is_id': False, 'header': 'disk_0_size', 'is_time': False}, {'field': 'disk_1_image', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 23, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'disk_1_image', 'is_time': False}, {'field': 'disk_1_size', 'type': 'int', 'type_flask': 'db.Integer', 'type_sqlalchemy': 'Integer', 'null': 'YES', 'key': '', 'default': '0', 'extra': '', 'is_form_editable': True, 'format': None, 'order': 24, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'IntegerField', 'is_id': False, 'header': 'disk_1_size', 'is_time': False}, {'field': 'disk_2_image', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 25, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'disk_2_image', 'is_time': False}, {'field': 'disk_2_size', 'type': 'int', 'type_flask': 'db.Integer', 'type_sqlalchemy': 'Integer', 'null': 'YES', 'key': '', 'default': '0', 'extra': '', 'is_form_editable': True, 'format': None, 'order': 26, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'IntegerField', 'is_id': False, 'header': 'disk_2_size', 'is_time': False}, {'field': 'disk_3_image', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 27, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'disk_3_image', 'is_time': False}, {'field': 'disk_3_size', 'type': 'int', 'type_flask': 'db.Integer', 'type_sqlalchemy': 'Integer', 'null': 'YES', 'key': '', 'default': '0', 'extra': '', 'is_form_editable': True, 'format': None, 'order': 28, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'IntegerField', 'is_id': False, 'header': 'disk_3_size', 'is_time': False}, {'field': 'disk_4_image', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 29, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'disk_4_image', 'is_time': False}, {'field': 'disk_4_size', 'type': 'int', 'type_flask': 'db.Integer', 'type_sqlalchemy': 'Integer', 'null': 'YES', 'key': '', 'default': '0', 'extra': '', 'is_form_editable': True, 'format': None, 'order': 30, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'IntegerField', 'is_id': False, 'header': 'disk_4_size', 'is_time': False}, {'field': 'disk_5_image', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 31, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'disk_5_image', 'is_time': False}, {'field': 'disk_5_size', 'type': 'int', 'type_flask': 'db.Integer', 'type_sqlalchemy': 'Integer', 'null': 'YES', 'key': '', 'default': '0', 'extra': '', 'is_form_editable': True, 'format': None, 'order': 32, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'IntegerField', 'is_id': False, 'header': 'disk_5_size', 'is_time': False}, {'field': 'disk_6_image', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 33, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'disk_6_image', 'is_time': False}, {'field': 'disk_6_size', 'type': 'int', 'type_flask': 'db.Integer', 'type_sqlalchemy': 'Integer', 'null': 'YES', 'key': '', 'default': '0', 'extra': '', 'is_form_editable': True, 'format': None, 'order': 34, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'IntegerField', 'is_id': False, 'header': 'disk_6_size', 'is_time': False}, {'field': 'disk_7_image', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 35, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'disk_7_image', 'is_time': False}, {'field': 'disk_7_size', 'type': 'int', 'type_flask': 'db.Integer', 'type_sqlalchemy': 'Integer', 'null': 'YES', 'key': '', 'default': '0', 'extra': '', 'is_form_editable': True, 'format': None, 'order': 36, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'IntegerField', 'is_id': False, 'header': 'disk_7_size', 'is_time': False}, {'field': 'disk_8_image', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 37, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'disk_8_image', 'is_time': False}, {'field': 'disk_8_size', 'type': 'int', 'type_flask': 'db.Integer', 'type_sqlalchemy': 'Integer', 'null': 'YES', 'key': '', 'default': '0', 'extra': '', 'is_form_editable': True, 'format': None, 'order': 38, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'IntegerField', 'is_id': False, 'header': 'disk_8_size', 'is_time': False}, {'field': 'disk_9_image', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 39, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'disk_9_image', 'is_time': False}, {'field': 'disk_9_size', 'type': 'int', 'type_flask': 'db.Integer', 'type_sqlalchemy': 'Integer', 'null': 'YES', 'key': '', 'default': '0', 'extra': '', 'is_form_editable': True, 'format': None, 'order': 40, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'IntegerField', 'is_id': False, 'header': 'disk_9_size', 'is_time': False}, {'field': 'disk_10_image', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 41, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'disk_10_image', 'is_time': False}, {'field': 'disk_10_size', 'type': 'int', 'type_flask': 'db.Integer', 'type_sqlalchemy': 'Integer', 'null': 'YES', 'key': '', 'default': '0', 'extra': '', 'is_form_editable': True, 'format': None, 'order': 42, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'IntegerField', 'is_id': False, 'header': 'disk_10_size', 'is_time': False}, {'field': 'disk_11_image', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 43, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'disk_11_image', 'is_time': False}, {'field': 'disk_11_size', 'type': 'int', 'type_flask': 'db.Integer', 'type_sqlalchemy': 'Integer', 'null': 'YES', 'key': '', 'default': '0', 'extra': '', 'is_form_editable': True, 'format': None, 'order': 44, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'IntegerField', 'is_id': False, 'header': 'disk_11_size', 'is_time': False}, {'field': 'vm_drp', 'type': 'tinyint', 'type_flask': 'db.Boolean', 'type_sqlalchemy': 'Boolean', 'null': 'YES', 'key': '', 'default': '0', 'extra': '', 'is_form_editable': True, 'format': None, 'order': 45, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'BooleanField', 'is_id': False, 'header': 'vm_drp', 'is_time': False}, {'field': 'vm_drp_remote', 'type': 'tinyint', 'type_flask': 'db.Boolean', 'type_sqlalchemy': 'Boolean', 'null': 'YES', 'key': '', 'default': '0', 'extra': '', 'is_form_editable': True, 'format': None, 'order': 46, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'BooleanField', 'is_id': False, 'header': 'vm_drp_remote', 'is_time': False}, {'field': 'vm_cdrom', 'type': 'tinyint', 'type_flask': 'db.Boolean', 'type_sqlalchemy': 'Boolean', 'null': 'YES', 'key': '', 'default': '0', 'extra': '', 'is_form_editable': True, 'format': None, 'order': 47, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'BooleanField', 'is_id': False, 'header': 'vm_cdrom', 'is_time': False}, {'field': 'drp_cluster_uuid', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 48, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'drp_cluster_uuid', 'is_time': False}, {'field': 'nic_0_vlan', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 49, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'nic_0_vlan', 'is_time': False}, {'field': 'nic_0_ip', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 50, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'nic_0_ip', 'is_time': False}, {'field': 'nic_0_mac', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 51, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'nic_0_mac', 'is_time': False}, {'field': 'nic_1_vlan', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 52, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'nic_1_vlan', 'is_time': False}, {'field': 'nic_1_ip', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 53, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'nic_1_ip', 'is_time': False}, {'field': 'nic_1_mac', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 54, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'nic_1_mac', 'is_time': False}, {'field': 'nic_2_vlan', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 55, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'nic_2_vlan', 'is_time': False}, {'field': 'nic_2_ip', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 56, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'nic_2_ip', 'is_time': False}, {'field': 'nic_2_mac', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 57, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'nic_2_mac', 'is_time': False}, {'field': 'nic_3_vlan', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 58, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'nic_3_vlan', 'is_time': False}, {'field': 'nic_3_ip', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 59, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'nic_3_ip', 'is_time': False}, {'field': 'nic_3_mac', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 60, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'nic_3_mac', 'is_time': False}, {'field': 'request_text', 'type': 'text', 'type_flask': 'db.Text', 'type_sqlalchemy': 'Text', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 61, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'request_text', 'is_time': False}]

        return __list

    def get_column_headers(self):
        """ Gets Nutanix_Prism_VM record column headers list """
        __list=['Request_Id', 'project_uuid', 'category_name', 'cluster_uuid', 'vm_name', 'power_state', 'vcpus_per_socket', 'num_sockets', 'memory_size_mib', 'memory_size_gib', 'Comments', 'vm_uuid', 'vm_ip', 'subnet_uuid', 'vm_username', 'vm_password', 'backup_set_1', 'backup_set_2', 'backup_set_3', 'disk_type', 'disk_0_image', 'disk_0_size', 'disk_1_image', 'disk_1_size', 'disk_2_image', 'disk_2_size', 'disk_3_image', 'disk_3_size', 'disk_4_image', 'disk_4_size', 'disk_5_image', 'disk_5_size', 'disk_6_image', 'disk_6_size', 'disk_7_image', 'disk_7_size', 'disk_8_image', 'disk_8_size', 'disk_9_image', 'disk_9_size', 'disk_10_image', 'disk_10_size', 'disk_11_image', 'disk_11_size', 'vm_drp', 'vm_drp_remote', 'vm_cdrom', 'drp_cluster_uuid', 'nic_0_vlan', 'nic_0_ip', 'nic_0_mac', 'nic_1_vlan', 'nic_1_ip', 'nic_1_mac', 'nic_2_vlan', 'nic_2_ip', 'nic_2_mac', 'nic_3_vlan', 'nic_3_ip', 'nic_3_mac', 'request_text']

        return __list

    def get_column_types(self):
        """ Gets Nutanix_Prism_VM record column data types list """
        __list=['Integer', 'String(45)', 'String(45)', 'String(45)', 'String(45)', 'Boolean', 'Integer', 'Integer', 'Integer', 'Integer', 'Text', 'String(45)', 'String(45)', 'String(45)', 'String(45)', 'String(45)', 'Boolean', 'Boolean', 'Boolean', 'Integer', 'String(45)', 'Integer', 'String(45)', 'Integer', 'String(45)', 'Integer', 'String(45)', 'Integer', 'String(45)', 'Integer', 'String(45)', 'Integer', 'String(45)', 'Integer', 'String(45)', 'Integer', 'String(45)', 'Integer', 'String(45)', 'Integer', 'String(45)', 'Integer', 'String(45)', 'Integer', 'Boolean', 'Boolean', 'Boolean', 'String(45)', 'String(45)', 'String(45)', 'String(45)', 'String(45)', 'String(45)', 'String(45)', 'String(45)', 'String(45)', 'String(45)', 'String(45)', 'String(45)', 'String(45)', 'Text']

        return __list

    def get_column_meta(self):
        """ Gets Nutanix_Prism_VM record column data meta list """
        __list=[('Request_Id', 'Integer'), ('project_uuid', 'String(45)'), ('category_name', 'String(45)'), ('cluster_uuid', 'String(45)'), ('vm_name', 'String(45)'), ('power_state', 'Boolean'), ('vcpus_per_socket', 'Integer'), ('num_sockets', 'Integer'), ('memory_size_mib', 'Integer'), ('memory_size_gib', 'Integer'), ('Comments', 'Text'), ('vm_uuid', 'String(45)'), ('vm_ip', 'String(45)'), ('subnet_uuid', 'String(45)'), ('vm_username', 'String(45)'), ('vm_password', 'String(45)'), ('backup_set_1', 'Boolean'), ('backup_set_2', 'Boolean'), ('backup_set_3', 'Boolean'), ('disk_type', 'Integer'), ('disk_0_image', 'String(45)'), ('disk_0_size', 'Integer'), ('disk_1_image', 'String(45)'), ('disk_1_size', 'Integer'), ('disk_2_image', 'String(45)'), ('disk_2_size', 'Integer'), ('disk_3_image', 'String(45)'), ('disk_3_size', 'Integer'), ('disk_4_image', 'String(45)'), ('disk_4_size', 'Integer'), ('disk_5_image', 'String(45)'), ('disk_5_size', 'Integer'), ('disk_6_image', 'String(45)'), ('disk_6_size', 'Integer'), ('disk_7_image', 'String(45)'), ('disk_7_size', 'Integer'), ('disk_8_image', 'String(45)'), ('disk_8_size', 'Integer'), ('disk_9_image', 'String(45)'), ('disk_9_size', 'Integer'), ('disk_10_image', 'String(45)'), ('disk_10_size', 'Integer'), ('disk_11_image', 'String(45)'), ('disk_11_size', 'Integer'), ('vm_drp', 'Boolean'), ('vm_drp_remote', 'Boolean'), ('vm_cdrom', 'Boolean'), ('drp_cluster_uuid', 'String(45)'), ('nic_0_vlan', 'String(45)'), ('nic_0_ip', 'String(45)'), ('nic_0_mac', 'String(45)'), ('nic_1_vlan', 'String(45)'), ('nic_1_ip', 'String(45)'), ('nic_1_mac', 'String(45)'), ('nic_2_vlan', 'String(45)'), ('nic_2_ip', 'String(45)'), ('nic_2_mac', 'String(45)'), ('nic_3_vlan', 'String(45)'), ('nic_3_ip', 'String(45)'), ('nic_3_mac', 'String(45)'), ('request_text', 'Text')]

        return __list

    def search_key(self,Request_Id):
        """ Search for an unique Nutanix_Prism_VM record using all key fields (Request_Id) """
        try:
            if self.engine is not None:
                Session=sessionmaker(bind=self.engine)
                session=Session()
                record = session.query(Nutanix_Prism_VM).filter(Nutanix_Prism_VM.Request_Id==Request_Id).one_or_none()
                session.flush()
            else:
                session.rollback()
                record = None
        except Exception as e:
            detail='Nutanix_Prism_VM.search_key(%s): Exception: %s'%(Request_Id,e)
            emtec_handle_general_exception(e,detail=detail,module=__name__,function='Nutanix_Prism_VM.search_key()',logger=self.logger)
            record = None
        return record

    def log(self,message,level=logging.DEBUG):
        """ Class Nutanix_Prism_VM log function """
        if self.logger is not None:
            self.logger.log(level,message)

# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2022-03-24 17:50:52
# =============================================================================

# GV gen_model_flask.py:418 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/models/orm_nutanix_vm_images.py
import sqlalchemy
class Nutanix_VM_Images(Base):
    __tablename__ = 'Nutanix_VM_Images'
    engine        = None
    logger        = None

    def check_shard(suffix=None,engine=None):
       if engine is not None:
           try:
               if sqlalchemy.__version__ >= '1.4':
                   inspector = sqlalchemy.inspect(engine)
                   table_exists = inspector.has_table(__class__.__tablename__,schema='butler')
               else:
                   table_exists = engine.dialect.has_table(engine, __class__.__tablename__)
               if not table_exists:
                   metadata=MetaData()
                   metadata.bind=engine
                   __class__.__table__.metadata=metadata
                   __class__.__table__.create(checkfirst=True)
                   if sqlalchemy.__version__ >= '1.4':
                       inspector = sqlalchemy.inspect(engine)
                       table_exists = inspector.has_table(__class__.__tablename__,schema='butler')
                   else:
                       table_exists = engine.dialect.has_table(engine, __class__.__tablename__)
                   if not table_exists:
                       print('460 Table %s does not exist. creation error?'% __class__.__tablename__)
                   else:
                       pass # GV print('462 Table %s exist !!!'% __class__.__tablename__)
               else:
                   pass # GV print('464 Table %s exist !!!'% __class__.__tablename__)
           except Exception as e:
              print(f'gen/gen_model_flask.py: 466 exception: {str(e)}')
           return
    def set_shard(suffix=None,engine=None):
       if suffix is not None:
           name='Nutanix_VM_Images_{suffix}'.format(suffix=suffix)
           __class__.__tablename__  = name
           __class__.__table__.name = name
       __class__.check_shard(suffix,engine)
       return __class__.__tablename__

    imageservice_uuid_diskclone = Column( String(45), primary_key=True )
    description                 = Column( String(45) )
    size_mib                    = Column( String(45) )
    comments                    = Column( String(45) )
    
    def __init__(self, imageservice_uuid_diskclone='None', description='None', size_mib='None', comments='None',engine=None,logger=None):
        """ Initiates a Nutanix_VM_Images class record """
        self.engine=engine
        self.logger=logger
        self.imageservice_uuid_diskclone = imageservice_uuid_diskclone
        self.description                 = description
        self.size_mib                    = size_mib
        self.comments                    = comments

        self.log('Created %s'%self)
    def __repr__(self):
        """ default class Nutanix_VM_Images representation function """
        return "<Nutanix_VM_Images( imageservice_uuid_diskclone='%s', description='%s', size_mib='%s', comments='%s')>" % \
                ( self.imageservice_uuid_diskclone, self.description, self.size_mib, self.comments)

    def get_list(self):
        """ Gets Nutanix_VM_Images record in list format """
        __list = [ self.imageservice_uuid_diskclone, self.description, self.size_mib, self.comments]
        return __list

    def get_tuple(self):
        """ Gets Nutanix_VM_Images record in tuple format """
        __tuple = ( self.imageservice_uuid_diskclone, self.description, self.size_mib, self.comments)
        return __tuple

    def get_dict(self):
        """ Gets Nutanix_VM_Images record in dict format """
        __dict={'imageservice_uuid_diskclone':self.imageservice_uuid_diskclone,'description':self.description,'size_mib':self.size_mib,'comments':self.comments}

        return __dict

    def get_json_dict(self,dateformat='%Y-%m-%d',timeformat='%H:%M:%S',datetimeformat=None):
        __dict = self.get_dict()
        if datetimeformat is None: 
            datetimeformat='%s %s'%(dateformat,timeformat)
        for key in __dict.keys():
            if   'datetime.datetime' in str(type(__dict[key])): __dict[key]=__dict[key].strftime(datetimeformat)
            elif 'datetime.date'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(dateformat)
            elif 'datetime.time'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(timeformat)
            elif 'decimal.Decimal'   in str(type(__dict[key])): __dict[key]=float(__dict[key])
        return __dict

    def get_json(self,dateformat='%Y-%m-%d',timeformat='%H:%M:%S',datetimeformat=None):
        __dict = self.get_dict()
        if datetimeformat is None: 
            datetimeformat='%s %s'%(dateformat,timeformat)
        for key in __dict.keys():
            if   'datetime.datetime' in str(type(__dict[key])): __dict[key]=__dict[key].strftime(datetimeformat)
            elif 'datetime.date'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(dateformat)
            elif 'datetime.time'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(timeformat)
            elif 'decimal.Decimal'   in str(type(__dict[key])): __dict[key]=float(__dict[key])
        return json.dumps(__dict)

    def post(self):
       return self

    def patch(self,**kwargs):
       for field in self.get_column_headers():
           if field in kwargs.keys():
               setattr(self,field,kwargs[field])
       return self

    def delete(self):
       return True

    def get_json_array(self,dateformat='%Y-%m-%d',timeformat='%H:%M:%S',datetimeformat=None):
        """ Gets Nutanix_VM_Images record in JSON array format """
        __list = self.get_list()
        if datetimeformat is None: 
            datetimeformat='%s %s'%(dateformat,timeformat)
        for field in range(len(__list)):
            if   'datetime.datetime' in str(type(__list[field])): __list[field]=__list[field].strftime(datetimeformat)
            elif 'datetime.date'     in str(type(__list[field])): __list[field]=__list[field].strftime(dateformat)
            elif 'datetime.time'     in str(type(__list[field])): __list[field]=__list[field].strftime(timeformat)
            elif 'decimal.Decimal'   in str(type(__list[field])): __list[field]=float(__list[field])
        return __list

    def get_columns(self):
        """ Gets Nutanix_VM_Images record column full details list """
        __list=[{'field': 'imageservice_uuid_diskclone', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'NO', 'key': 'PRI', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 1, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'imageservice_uuid_diskclone', 'is_time': False}, {'field': 'description', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 2, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'description', 'is_time': False}, {'field': 'size_mib', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 3, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'size_mib', 'is_time': False}, {'field': 'comments', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 4, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'comments', 'is_time': False}]

        return __list

    def get_column_headers(self):
        """ Gets Nutanix_VM_Images record column headers list """
        __list=['imageservice_uuid_diskclone', 'description', 'size_mib', 'comments']

        return __list

    def get_column_types(self):
        """ Gets Nutanix_VM_Images record column data types list """
        __list=['String(45)', 'String(45)', 'String(45)', 'String(45)']

        return __list

    def get_column_meta(self):
        """ Gets Nutanix_VM_Images record column data meta list """
        __list=[('imageservice_uuid_diskclone', 'String(45)'), ('description', 'String(45)'), ('size_mib', 'String(45)'), ('comments', 'String(45)')]

        return __list

    def search_key(self,imageservice_uuid_diskclone):
        """ Search for an unique Nutanix_VM_Images record using all key fields (imageservice_uuid_diskclone) """
        try:
            if self.engine is not None:
                Session=sessionmaker(bind=self.engine)
                session=Session()
                record = session.query(Nutanix_VM_Images).filter(Nutanix_VM_Images.imageservice_uuid_diskclone==imageservice_uuid_diskclone).one_or_none()
                session.flush()
            else:
                session.rollback()
                record = None
        except Exception as e:
            detail='Nutanix_VM_Images.search_key(%s): Exception: %s'%(imageservice_uuid_diskclone,e)
            emtec_handle_general_exception(e,detail=detail,module=__name__,function='Nutanix_VM_Images.search_key()',logger=self.logger)
            record = None
        return record

    def log(self,message,level=logging.DEBUG):
        """ Class Nutanix_VM_Images log function """
        if self.logger is not None:
            self.logger.log(level,message)

# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2022-03-24 17:50:52
# =============================================================================

# GV gen_model_flask.py:418 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/models/orm_projects.py
import sqlalchemy
class Projects(Base):
    __tablename__ = 'Projects'
    engine        = None
    logger        = None

    def check_shard(suffix=None,engine=None):
       if engine is not None:
           try:
               if sqlalchemy.__version__ >= '1.4':
                   inspector = sqlalchemy.inspect(engine)
                   table_exists = inspector.has_table(__class__.__tablename__,schema='butler')
               else:
                   table_exists = engine.dialect.has_table(engine, __class__.__tablename__)
               if not table_exists:
                   metadata=MetaData()
                   metadata.bind=engine
                   __class__.__table__.metadata=metadata
                   __class__.__table__.create(checkfirst=True)
                   if sqlalchemy.__version__ >= '1.4':
                       inspector = sqlalchemy.inspect(engine)
                       table_exists = inspector.has_table(__class__.__tablename__,schema='butler')
                   else:
                       table_exists = engine.dialect.has_table(engine, __class__.__tablename__)
                   if not table_exists:
                       print('460 Table %s does not exist. creation error?'% __class__.__tablename__)
                   else:
                       pass # GV print('462 Table %s exist !!!'% __class__.__tablename__)
               else:
                   pass # GV print('464 Table %s exist !!!'% __class__.__tablename__)
           except Exception as e:
              print(f'gen/gen_model_flask.py: 466 exception: {str(e)}')
           return
    def set_shard(suffix=None,engine=None):
       if suffix is not None:
           name='Projects_{suffix}'.format(suffix=suffix)
           __class__.__tablename__  = name
           __class__.__table__.name = name
       __class__.check_shard(suffix,engine)
       return __class__.__tablename__

    project_uuid    = Column( String(45), primary_key=True )
    project_name    = Column( String(45) )
    project_subnets = Column( String(1024) )
    
    def __init__(self, project_uuid='None', project_name='None', project_subnets='None',engine=None,logger=None):
        """ Initiates a Projects class record """
        self.engine=engine
        self.logger=logger
        self.project_uuid    = project_uuid
        self.project_name    = project_name
        self.project_subnets = project_subnets

        self.log('Created %s'%self)
    def __repr__(self):
        """ default class Projects representation function """
        return "<Projects( project_uuid='%s', project_name='%s', project_subnets='%s')>" % \
                ( self.project_uuid, self.project_name, self.project_subnets)

    def get_list(self):
        """ Gets Projects record in list format """
        __list = [ self.project_uuid, self.project_name, self.project_subnets]
        return __list

    def get_tuple(self):
        """ Gets Projects record in tuple format """
        __tuple = ( self.project_uuid, self.project_name, self.project_subnets)
        return __tuple

    def get_dict(self):
        """ Gets Projects record in dict format """
        __dict={'project_uuid':self.project_uuid,'project_name':self.project_name,'project_subnets':self.project_subnets}

        return __dict

    def get_json_dict(self,dateformat='%Y-%m-%d',timeformat='%H:%M:%S',datetimeformat=None):
        __dict = self.get_dict()
        if datetimeformat is None: 
            datetimeformat='%s %s'%(dateformat,timeformat)
        for key in __dict.keys():
            if   'datetime.datetime' in str(type(__dict[key])): __dict[key]=__dict[key].strftime(datetimeformat)
            elif 'datetime.date'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(dateformat)
            elif 'datetime.time'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(timeformat)
            elif 'decimal.Decimal'   in str(type(__dict[key])): __dict[key]=float(__dict[key])
        return __dict

    def get_json(self,dateformat='%Y-%m-%d',timeformat='%H:%M:%S',datetimeformat=None):
        __dict = self.get_dict()
        if datetimeformat is None: 
            datetimeformat='%s %s'%(dateformat,timeformat)
        for key in __dict.keys():
            if   'datetime.datetime' in str(type(__dict[key])): __dict[key]=__dict[key].strftime(datetimeformat)
            elif 'datetime.date'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(dateformat)
            elif 'datetime.time'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(timeformat)
            elif 'decimal.Decimal'   in str(type(__dict[key])): __dict[key]=float(__dict[key])
        return json.dumps(__dict)

    def post(self):
       return self

    def patch(self,**kwargs):
       for field in self.get_column_headers():
           if field in kwargs.keys():
               setattr(self,field,kwargs[field])
       return self

    def delete(self):
       return True

    def get_json_array(self,dateformat='%Y-%m-%d',timeformat='%H:%M:%S',datetimeformat=None):
        """ Gets Projects record in JSON array format """
        __list = self.get_list()
        if datetimeformat is None: 
            datetimeformat='%s %s'%(dateformat,timeformat)
        for field in range(len(__list)):
            if   'datetime.datetime' in str(type(__list[field])): __list[field]=__list[field].strftime(datetimeformat)
            elif 'datetime.date'     in str(type(__list[field])): __list[field]=__list[field].strftime(dateformat)
            elif 'datetime.time'     in str(type(__list[field])): __list[field]=__list[field].strftime(timeformat)
            elif 'decimal.Decimal'   in str(type(__list[field])): __list[field]=float(__list[field])
        return __list

    def get_columns(self):
        """ Gets Projects record column full details list """
        __list=[{'field': 'project_uuid', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'NO', 'key': 'PRI', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 1, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'project_uuid', 'is_time': False}, {'field': 'project_name', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 2, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'project_name', 'is_time': False}, {'field': 'project_subnets', 'type': 'varchar(1024)', 'type_flask': 'db.String(1024)', 'type_sqlalchemy': 'String(1024)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 3, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'project_subnets', 'is_time': False}]

        return __list

    def get_column_headers(self):
        """ Gets Projects record column headers list """
        __list=['project_uuid', 'project_name', 'project_subnets']

        return __list

    def get_column_types(self):
        """ Gets Projects record column data types list """
        __list=['String(45)', 'String(45)', 'String(1024)']

        return __list

    def get_column_meta(self):
        """ Gets Projects record column data meta list """
        __list=[('project_uuid', 'String(45)'), ('project_name', 'String(45)'), ('project_subnets', 'String(1024)')]

        return __list

    def search_key(self,project_uuid):
        """ Search for an unique Projects record using all key fields (project_uuid) """
        try:
            if self.engine is not None:
                Session=sessionmaker(bind=self.engine)
                session=Session()
                record = session.query(Projects).filter(Projects.project_uuid==project_uuid).one_or_none()
                session.flush()
            else:
                session.rollback()
                record = None
        except Exception as e:
            detail='Projects.search_key(%s): Exception: %s'%(project_uuid,e)
            emtec_handle_general_exception(e,detail=detail,module=__name__,function='Projects.search_key()',logger=self.logger)
            record = None
        return record

    def log(self,message,level=logging.DEBUG):
        """ Class Projects log function """
        if self.logger is not None:
            self.logger.log(level,message)

# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2022-03-24 17:50:52
# =============================================================================

# GV gen_model_flask.py:418 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/models/orm_rates.py
import sqlalchemy
class Rates(Base):
    __tablename__ = 'Rates'
    engine        = None
    logger        = None

    def check_shard(suffix=None,engine=None):
       if engine is not None:
           try:
               if sqlalchemy.__version__ >= '1.4':
                   inspector = sqlalchemy.inspect(engine)
                   table_exists = inspector.has_table(__class__.__tablename__,schema='butler')
               else:
                   table_exists = engine.dialect.has_table(engine, __class__.__tablename__)
               if not table_exists:
                   metadata=MetaData()
                   metadata.bind=engine
                   __class__.__table__.metadata=metadata
                   __class__.__table__.create(checkfirst=True)
                   if sqlalchemy.__version__ >= '1.4':
                       inspector = sqlalchemy.inspect(engine)
                       table_exists = inspector.has_table(__class__.__tablename__,schema='butler')
                   else:
                       table_exists = engine.dialect.has_table(engine, __class__.__tablename__)
                   if not table_exists:
                       print('460 Table %s does not exist. creation error?'% __class__.__tablename__)
                   else:
                       pass # GV print('462 Table %s exist !!!'% __class__.__tablename__)
               else:
                   pass # GV print('464 Table %s exist !!!'% __class__.__tablename__)
           except Exception as e:
              print(f'gen/gen_model_flask.py: 466 exception: {str(e)}')
           return
    def set_shard(suffix=None,engine=None):
       if suffix is not None:
           name='Rates_{suffix}'.format(suffix=suffix)
           __class__.__tablename__  = name
           __class__.__table__.name = name
       __class__.check_shard(suffix,engine)
       return __class__.__tablename__

    Rat_Id     = Column( Integer, primary_key=True, autoincrement=True )
    Typ_Code   = Column( String(10) )
    Cus_Id     = Column( Integer )
    Pla_Id     = Column( Integer )
    CC_Id      = Column( Integer )
    CI_Id      = Column( Integer )
    Rat_Price  = Column( Numeric(20,12) )
    Cur_Code   = Column( String(3) )
    MU_Code    = Column( String(3) )
    Rat_Period = Column( Integer )
    Rat_Type   = Column( Integer )
    # @property
    #
    
    
    def __init__(self, Rat_Id=0, Typ_Code='None', Cus_Id=None, Pla_Id=None, CC_Id=None, CI_Id=None, Rat_Price=None, Cur_Code='None', MU_Code='None', Rat_Period=None, Rat_Type=None,engine=None,logger=None):
        """ Initiates a Rates class record """
        self.engine=engine
        self.logger=logger
        self.Rat_Id     = Rat_Id
        self.Typ_Code   = Typ_Code
        self.Cus_Id     = Cus_Id
        self.Pla_Id     = Pla_Id
        self.CC_Id      = CC_Id
        self.CI_Id      = CI_Id
        self.Rat_Price  = Rat_Price
        self.Cur_Code   = Cur_Code
        self.MU_Code    = MU_Code
        self.Rat_Period = Rat_Period
        self.Rat_Type   = Rat_Type

        self.log('Created %s'%self)
    def __repr__(self):
        """ default class Rates representation function """
        return "<Rates( Rat_Id='%s', Typ_Code='%s', Cus_Id='%s', Pla_Id='%s', CC_Id='%s', CI_Id='%s', Rat_Price='%s', Cur_Code='%s', MU_Code='%s', Rat_Period='%s', Rat_Type='%s')>" % \
                ( self.Rat_Id, self.Typ_Code, self.Cus_Id, self.Pla_Id, self.CC_Id, self.CI_Id, self.Rat_Price, self.Cur_Code, self.MU_Code, self.Rat_Period, self.Rat_Type)

    def get_list(self):
        """ Gets Rates record in list format """
        __list = [ self.Rat_Id, self.Typ_Code, self.Cus_Id, self.Pla_Id, self.CC_Id, self.CI_Id, self.Rat_Price, self.Cur_Code, self.MU_Code, self.Rat_Period, self.Rat_Type]
        return __list

    def get_tuple(self):
        """ Gets Rates record in tuple format """
        __tuple = ( self.Rat_Id, self.Typ_Code, self.Cus_Id, self.Pla_Id, self.CC_Id, self.CI_Id, self.Rat_Price, self.Cur_Code, self.MU_Code, self.Rat_Period, self.Rat_Type)
        return __tuple

    def get_dict(self):
        """ Gets Rates record in dict format """
        __dict={'Rat_Id':self.Rat_Id,'Typ_Code':self.Typ_Code,'Cus_Id':self.Cus_Id,'Pla_Id':self.Pla_Id,'CC_Id':self.CC_Id,'CI_Id':self.CI_Id,'Rat_Price':self.Rat_Price,'Cur_Code':self.Cur_Code,'MU_Code':self.MU_Code,'Rat_Period':self.Rat_Period,'Rat_Type':self.Rat_Type}

        return __dict

    def get_json_dict(self,dateformat='%Y-%m-%d',timeformat='%H:%M:%S',datetimeformat=None):
        __dict = self.get_dict()
        if datetimeformat is None: 
            datetimeformat='%s %s'%(dateformat,timeformat)
        for key in __dict.keys():
            if   'datetime.datetime' in str(type(__dict[key])): __dict[key]=__dict[key].strftime(datetimeformat)
            elif 'datetime.date'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(dateformat)
            elif 'datetime.time'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(timeformat)
            elif 'decimal.Decimal'   in str(type(__dict[key])): __dict[key]=float(__dict[key])
        return __dict

    def get_json(self,dateformat='%Y-%m-%d',timeformat='%H:%M:%S',datetimeformat=None):
        __dict = self.get_dict()
        if datetimeformat is None: 
            datetimeformat='%s %s'%(dateformat,timeformat)
        for key in __dict.keys():
            if   'datetime.datetime' in str(type(__dict[key])): __dict[key]=__dict[key].strftime(datetimeformat)
            elif 'datetime.date'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(dateformat)
            elif 'datetime.time'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(timeformat)
            elif 'decimal.Decimal'   in str(type(__dict[key])): __dict[key]=float(__dict[key])
        return json.dumps(__dict)

    def post(self):
       return self

    def patch(self,**kwargs):
       for field in self.get_column_headers():
           if field in kwargs.keys():
               setattr(self,field,kwargs[field])
       return self

    def delete(self):
       return True

    def get_json_array(self,dateformat='%Y-%m-%d',timeformat='%H:%M:%S',datetimeformat=None):
        """ Gets Rates record in JSON array format """
        __list = self.get_list()
        if datetimeformat is None: 
            datetimeformat='%s %s'%(dateformat,timeformat)
        for field in range(len(__list)):
            if   'datetime.datetime' in str(type(__list[field])): __list[field]=__list[field].strftime(datetimeformat)
            elif 'datetime.date'     in str(type(__list[field])): __list[field]=__list[field].strftime(dateformat)
            elif 'datetime.time'     in str(type(__list[field])): __list[field]=__list[field].strftime(timeformat)
            elif 'decimal.Decimal'   in str(type(__list[field])): __list[field]=float(__list[field])
        return __list

    def get_columns(self):
        """ Gets Rates record column full details list """
        __list=[{'field': 'Rat_Id', 'type': 'int', 'type_flask': 'db.Integer', 'type_sqlalchemy': 'Integer', 'null': 'NO', 'key': 'PRI', 'default': None, 'extra': 'auto_increment', 'is_form_editable': True, 'format': None, 'order': 1, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'IntegerField', 'is_id': True, 'header': 'Rat_Id', 'is_time': False}, {'field': 'Typ_Code', 'type': 'varchar(10)', 'type_flask': 'db.String(10)', 'type_sqlalchemy': 'String(10)', 'null': 'NO', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 2, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'Typ_Code', 'is_time': False}, {'field': 'Cus_Id', 'type': 'int', 'type_flask': 'db.Integer', 'type_sqlalchemy': 'Integer', 'null': 'NO', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 3, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'IntegerField', 'is_id': False, 'header': 'Cus_Id', 'is_time': False}, {'field': 'Pla_Id', 'type': 'int', 'type_flask': 'db.Integer', 'type_sqlalchemy': 'Integer', 'null': 'NO', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 4, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'IntegerField', 'is_id': False, 'header': 'Pla_Id', 'is_time': False}, {'field': 'CC_Id', 'type': 'int', 'type_flask': 'db.Integer', 'type_sqlalchemy': 'Integer', 'null': 'NO', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 5, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'IntegerField', 'is_id': False, 'header': 'CC_Id', 'is_time': False}, {'field': 'CI_Id', 'type': 'int', 'type_flask': 'db.Integer', 'type_sqlalchemy': 'Integer', 'null': 'NO', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 6, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'IntegerField', 'is_id': False, 'header': 'CI_Id', 'is_time': False}, {'field': 'Rat_Price', 'type': 'decimal(20,12)', 'type_flask': 'db.Numeric(20,12)', 'type_sqlalchemy': 'Numeric(20,12)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 7, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': True, 'form_type': 'DecimalField', 'is_id': False, 'header': 'Rat_Price', 'is_time': False}, {'field': 'Cur_Code', 'type': 'varchar(3)', 'type_flask': 'db.String(3)', 'type_sqlalchemy': 'String(3)', 'null': 'NO', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 8, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'Cur_Code', 'is_time': False}, {'field': 'MU_Code', 'type': 'varchar(3)', 'type_flask': 'db.String(3)', 'type_sqlalchemy': 'String(3)', 'null': 'NO', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 9, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'MU_Code', 'is_time': False}, {'field': 'Rat_Period', 'type': 'int', 'type_flask': 'db.Integer', 'type_sqlalchemy': 'Integer', 'null': 'NO', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 10, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'IntegerField', 'is_id': False, 'header': 'Rat_Period', 'is_time': False}, {'field': 'Rat_Type', 'type': 'int', 'type_flask': 'db.Integer', 'type_sqlalchemy': 'Integer', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 11, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'IntegerField', 'is_id': False, 'header': 'Rat_Type', 'is_time': False}]

        return __list

    def get_column_headers(self):
        """ Gets Rates record column headers list """
        __list=['Rat_Id', 'Typ_Code', 'Cus_Id', 'Pla_Id', 'CC_Id', 'CI_Id', 'Rat_Price', 'Cur_Code', 'MU_Code', 'Rat_Period', 'Rat_Type']

        return __list

    def get_column_types(self):
        """ Gets Rates record column data types list """
        __list=['Integer', 'String(10)', 'Integer', 'Integer', 'Integer', 'Integer', 'Numeric(20,12)', 'String(3)', 'String(3)', 'Integer', 'Integer']

        return __list

    def get_column_meta(self):
        """ Gets Rates record column data meta list """
        __list=[('Rat_Id', 'Integer'), ('Typ_Code', 'String(10)'), ('Cus_Id', 'Integer'), ('Pla_Id', 'Integer'), ('CC_Id', 'Integer'), ('CI_Id', 'Integer'), ('Rat_Price', 'Numeric(20,12)'), ('Cur_Code', 'String(3)'), ('MU_Code', 'String(3)'), ('Rat_Period', 'Integer'), ('Rat_Type', 'Integer')]

        return __list

    def search_key(self,Rat_Id):
        """ Search for an unique Rates record using all key fields (Rat_Id) """
        try:
            if self.engine is not None:
                Session=sessionmaker(bind=self.engine)
                session=Session()
                record = session.query(Rates).filter(Rates.Rat_Id==Rat_Id).one_or_none()
                session.flush()
            else:
                session.rollback()
                record = None
        except Exception as e:
            detail='Rates.search_key(%s): Exception: %s'%(Rat_Id,e)
            emtec_handle_general_exception(e,detail=detail,module=__name__,function='Rates.search_key()',logger=self.logger)
            record = None
        return record

    def log(self,message,level=logging.DEBUG):
        """ Class Rates log function """
        if self.logger is not None:
            self.logger.log(level,message)
    # method
    def method(self):
        pass

# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2022-03-24 17:50:52
# =============================================================================

# gen_model_flask.py:865 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/models/orm_rates.py
# gen_model_flask.py:866 Table sharding code follows:
def get_Rates(table_name_suffix):
  class Rates_Class(Base):
    __tablename__ = 'Rates_%s'%(table_name_suffix)
    engine        = None
    logger        = None

    def set_shard(suffix=None,engine=None):
       if suffix is not None:
           name='Rates_{suffix}'.format(suffix=suffix)
           __class__.__tablename__  = name
           __class__.__table_args__ = {'extend_existing':True}
           __class__.__table__.name = name
           __class__.check_shard(suffix,engine)
       return __class__.__tablename__

    Rat_Id     = Column( Integer, primary_key=True, autoincrement=True )
    Typ_Code   = Column( String(10) )
    Cus_Id     = Column( Integer )
    Pla_Id     = Column( Integer )
    CC_Id      = Column( Integer )
    CI_Id      = Column( Integer )
    Rat_Price  = Column( Numeric(20,12) )
    Cur_Code   = Column( String(3) )
    MU_Code    = Column( String(3) )
    Rat_Period = Column( Integer )
    Rat_Type   = Column( Integer )
    # @property
    #
    
    
    def __init__(self, Rat_Id=0, Typ_Code='None', Cus_Id=None, Pla_Id=None, CC_Id=None, CI_Id=None, Rat_Price=None, Cur_Code='None', MU_Code='None', Rat_Period=None, Rat_Type=None,engine=None,logger=None):
        """ Initiates a Rates class record """
        self.engine=engine
        self.logger=logger
        self.Rat_Id     = Rat_Id
        self.Typ_Code   = Typ_Code
        self.Cus_Id     = Cus_Id
        self.Pla_Id     = Pla_Id
        self.CC_Id      = CC_Id
        self.CI_Id      = CI_Id
        self.Rat_Price  = Rat_Price
        self.Cur_Code   = Cur_Code
        self.MU_Code    = MU_Code
        self.Rat_Period = Rat_Period
        self.Rat_Type   = Rat_Type

        self.log('Created %s'%self)
    def __repr__(self):
        """ default class Rates representation function """
        return "<Rates( Rat_Id='%s', Typ_Code='%s', Cus_Id='%s', Pla_Id='%s', CC_Id='%s', CI_Id='%s', Rat_Price='%s', Cur_Code='%s', MU_Code='%s', Rat_Period='%s', Rat_Type='%s')>" % \
                ( self.Rat_Id, self.Typ_Code, self.Cus_Id, self.Pla_Id, self.CC_Id, self.CI_Id, self.Rat_Price, self.Cur_Code, self.MU_Code, self.Rat_Period, self.Rat_Type)

    def get_list(self):
        """ Gets Rates record in list format """
        __list = [ self.Rat_Id, self.Typ_Code, self.Cus_Id, self.Pla_Id, self.CC_Id, self.CI_Id, self.Rat_Price, self.Cur_Code, self.MU_Code, self.Rat_Period, self.Rat_Type]
        return __list

    def get_tuple(self):
        """ Gets Rates record in tuple format """
        __tuple = ( self.Rat_Id, self.Typ_Code, self.Cus_Id, self.Pla_Id, self.CC_Id, self.CI_Id, self.Rat_Price, self.Cur_Code, self.MU_Code, self.Rat_Period, self.Rat_Type)
        return __tuple

    def get_dict(self):
        """ Gets Rates record in dict format """
        __dict={'Rat_Id':self.Rat_Id,'Typ_Code':self.Typ_Code,'Cus_Id':self.Cus_Id,'Pla_Id':self.Pla_Id,'CC_Id':self.CC_Id,'CI_Id':self.CI_Id,'Rat_Price':self.Rat_Price,'Cur_Code':self.Cur_Code,'MU_Code':self.MU_Code,'Rat_Period':self.Rat_Period,'Rat_Type':self.Rat_Type}

        return __dict

    def get_json_dict(self,dateformat='%Y-%m-%d',timeformat='%H:%M:%S',datetimeformat=None):
        __dict = self.get_dict()
        if datetimeformat is None: 
            datetimeformat='%s %s'%(dateformat,timeformat)
        for key in __dict.keys():
            if   'datetime.datetime' in str(type(__dict[key])): __dict[key]=__dict[key].strftime(datetimeformat)
            elif 'datetime.date'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(dateformat)
            elif 'datetime.time'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(timeformat)
            elif 'decimal.Decimal'   in str(type(__dict[key])): __dict[key]=float(__dict[key])
        return __dict

    def get_json(self,dateformat='%Y-%m-%d',timeformat='%H:%M:%S',datetimeformat=None):
        __dict = self.get_dict()
        if datetimeformat is None: 
            datetimeformat='%s %s'%(dateformat,timeformat)
        for key in __dict.keys():
            if   'datetime.datetime' in str(type(__dict[key])): __dict[key]=__dict[key].strftime(datetimeformat)
            elif 'datetime.date'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(dateformat)
            elif 'datetime.time'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(timeformat)
            elif 'decimal.Decimal'   in str(type(__dict[key])): __dict[key]=float(__dict[key])
        return json.dumps(__dict)

    def post(self):
       return self

    def patch(self,**kwargs):
       for field in self.get_column_headers():
           if field in kwargs.keys():
               setattr(self,field,kwargs[field])
       return self

    def delete(self):
       return True

    def get_json_array(self,dateformat='%Y-%m-%d',timeformat='%H:%M:%S',datetimeformat=None):
        """ Gets Rates record in JSON array format """
        __list = self.get_list()
        if datetimeformat is None: 
            datetimeformat='%s %s'%(dateformat,timeformat)
        for field in range(len(__list)):
            if   'datetime.datetime' in str(type(__list[field])): __list[field]=__list[field].strftime(datetimeformat)
            elif 'datetime.date'     in str(type(__list[field])): __list[field]=__list[field].strftime(dateformat)
            elif 'datetime.time'     in str(type(__list[field])): __list[field]=__list[field].strftime(timeformat)
            elif 'decimal.Decimal'   in str(type(__list[field])): __list[field]=float(__list[field])
        return __list

    def get_columns(self):
        """ Gets Rates record column full details list """
        __list=[{'field': 'Rat_Id', 'type': 'int', 'type_flask': 'db.Integer', 'type_sqlalchemy': 'Integer', 'null': 'NO', 'key': 'PRI', 'default': None, 'extra': 'auto_increment', 'is_form_editable': True, 'format': None, 'order': 1, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'IntegerField', 'is_id': True, 'header': 'Rat_Id', 'is_time': False}, {'field': 'Typ_Code', 'type': 'varchar(10)', 'type_flask': 'db.String(10)', 'type_sqlalchemy': 'String(10)', 'null': 'NO', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 2, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'Typ_Code', 'is_time': False}, {'field': 'Cus_Id', 'type': 'int', 'type_flask': 'db.Integer', 'type_sqlalchemy': 'Integer', 'null': 'NO', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 3, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'IntegerField', 'is_id': False, 'header': 'Cus_Id', 'is_time': False}, {'field': 'Pla_Id', 'type': 'int', 'type_flask': 'db.Integer', 'type_sqlalchemy': 'Integer', 'null': 'NO', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 4, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'IntegerField', 'is_id': False, 'header': 'Pla_Id', 'is_time': False}, {'field': 'CC_Id', 'type': 'int', 'type_flask': 'db.Integer', 'type_sqlalchemy': 'Integer', 'null': 'NO', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 5, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'IntegerField', 'is_id': False, 'header': 'CC_Id', 'is_time': False}, {'field': 'CI_Id', 'type': 'int', 'type_flask': 'db.Integer', 'type_sqlalchemy': 'Integer', 'null': 'NO', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 6, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'IntegerField', 'is_id': False, 'header': 'CI_Id', 'is_time': False}, {'field': 'Rat_Price', 'type': 'decimal(20,12)', 'type_flask': 'db.Numeric(20,12)', 'type_sqlalchemy': 'Numeric(20,12)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 7, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': True, 'form_type': 'DecimalField', 'is_id': False, 'header': 'Rat_Price', 'is_time': False}, {'field': 'Cur_Code', 'type': 'varchar(3)', 'type_flask': 'db.String(3)', 'type_sqlalchemy': 'String(3)', 'null': 'NO', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 8, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'Cur_Code', 'is_time': False}, {'field': 'MU_Code', 'type': 'varchar(3)', 'type_flask': 'db.String(3)', 'type_sqlalchemy': 'String(3)', 'null': 'NO', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 9, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'MU_Code', 'is_time': False}, {'field': 'Rat_Period', 'type': 'int', 'type_flask': 'db.Integer', 'type_sqlalchemy': 'Integer', 'null': 'NO', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 10, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'IntegerField', 'is_id': False, 'header': 'Rat_Period', 'is_time': False}, {'field': 'Rat_Type', 'type': 'int', 'type_flask': 'db.Integer', 'type_sqlalchemy': 'Integer', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 11, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'IntegerField', 'is_id': False, 'header': 'Rat_Type', 'is_time': False}]

        return __list

    def get_column_headers(self):
        """ Gets Rates record column headers list """
        __list=['Rat_Id', 'Typ_Code', 'Cus_Id', 'Pla_Id', 'CC_Id', 'CI_Id', 'Rat_Price', 'Cur_Code', 'MU_Code', 'Rat_Period', 'Rat_Type']

        return __list

    def get_column_types(self):
        """ Gets Rates record column data types list """
        __list=['Integer', 'String(10)', 'Integer', 'Integer', 'Integer', 'Integer', 'Numeric(20,12)', 'String(3)', 'String(3)', 'Integer', 'Integer']

        return __list

    def get_column_meta(self):
        """ Gets Rates record column data meta list """
        __list=[('Rat_Id', 'Integer'), ('Typ_Code', 'String(10)'), ('Cus_Id', 'Integer'), ('Pla_Id', 'Integer'), ('CC_Id', 'Integer'), ('CI_Id', 'Integer'), ('Rat_Price', 'Numeric(20,12)'), ('Cur_Code', 'String(3)'), ('MU_Code', 'String(3)'), ('Rat_Period', 'Integer'), ('Rat_Type', 'Integer')]

        return __list

    def search_key(self,Rat_Id):
        """ Search for an unique Rates record using all key fields (Rat_Id) """
        try:
            if self.engine is not None:
                Session=sessionmaker(bind=self.engine)
                session=Session()
                record = session.query(Rates).filter(Rates.Rat_Id==Rat_Id).one_or_none()
                session.flush()
            else:
                session.rollback()
                record = None
        except Exception as e:
            detail='Rates.search_key(%s): Exception: %s'%(Rat_Id,e)
            emtec_handle_general_exception(e,detail=detail,module=__name__,function='Rates.search_key()',logger=self.logger)
            record = None
        return record

    def log(self,message,level=logging.DEBUG):
        """ Class Rates log function """
        if self.logger is not None:
            self.logger.log(level,message)

    # method
    def method(self):
        pass
  Rates_Class.__name__ = 'Rates_%s'%(table_name_suffix)
  x = Rates_Class
  return x

# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2022-03-24 17:50:52
# =============================================================================

# GV gen_model_flask.py:418 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/models/orm_request_type.py
import sqlalchemy
class Request_Type(Base):
    __tablename__ = 'Request_Type'
    engine        = None
    logger        = None

    def check_shard(suffix=None,engine=None):
       if engine is not None:
           try:
               if sqlalchemy.__version__ >= '1.4':
                   inspector = sqlalchemy.inspect(engine)
                   table_exists = inspector.has_table(__class__.__tablename__,schema='butler')
               else:
                   table_exists = engine.dialect.has_table(engine, __class__.__tablename__)
               if not table_exists:
                   metadata=MetaData()
                   metadata.bind=engine
                   __class__.__table__.metadata=metadata
                   __class__.__table__.create(checkfirst=True)
                   if sqlalchemy.__version__ >= '1.4':
                       inspector = sqlalchemy.inspect(engine)
                       table_exists = inspector.has_table(__class__.__tablename__,schema='butler')
                   else:
                       table_exists = engine.dialect.has_table(engine, __class__.__tablename__)
                   if not table_exists:
                       print('460 Table %s does not exist. creation error?'% __class__.__tablename__)
                   else:
                       pass # GV print('462 Table %s exist !!!'% __class__.__tablename__)
               else:
                   pass # GV print('464 Table %s exist !!!'% __class__.__tablename__)
           except Exception as e:
              print(f'gen/gen_model_flask.py: 466 exception: {str(e)}')
           return
    def set_shard(suffix=None,engine=None):
       if suffix is not None:
           name='Request_Type_{suffix}'.format(suffix=suffix)
           __class__.__tablename__  = name
           __class__.__table__.name = name
       __class__.check_shard(suffix,engine)
       return __class__.__tablename__

    Id          = Column( Integer, primary_key=True )
    Description = Column( String(45) )
    Table_Name  = Column( String(45) )
    
    def __init__(self, Id=None, Description='None', Table_Name='None',engine=None,logger=None):
        """ Initiates a Request_Type class record """
        self.engine=engine
        self.logger=logger
        self.Id          = Id
        self.Description = Description
        self.Table_Name  = Table_Name

        self.log('Created %s'%self)
    def __repr__(self):
        """ default class Request_Type representation function """
        return "<Request_Type( Id='%s', Description='%s', Table_Name='%s')>" % \
                ( self.Id, self.Description, self.Table_Name)

    def get_list(self):
        """ Gets Request_Type record in list format """
        __list = [ self.Id, self.Description, self.Table_Name]
        return __list

    def get_tuple(self):
        """ Gets Request_Type record in tuple format """
        __tuple = ( self.Id, self.Description, self.Table_Name)
        return __tuple

    def get_dict(self):
        """ Gets Request_Type record in dict format """
        __dict={'Id':self.Id,'Description':self.Description,'Table_Name':self.Table_Name}

        return __dict

    def get_json_dict(self,dateformat='%Y-%m-%d',timeformat='%H:%M:%S',datetimeformat=None):
        __dict = self.get_dict()
        if datetimeformat is None: 
            datetimeformat='%s %s'%(dateformat,timeformat)
        for key in __dict.keys():
            if   'datetime.datetime' in str(type(__dict[key])): __dict[key]=__dict[key].strftime(datetimeformat)
            elif 'datetime.date'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(dateformat)
            elif 'datetime.time'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(timeformat)
            elif 'decimal.Decimal'   in str(type(__dict[key])): __dict[key]=float(__dict[key])
        return __dict

    def get_json(self,dateformat='%Y-%m-%d',timeformat='%H:%M:%S',datetimeformat=None):
        __dict = self.get_dict()
        if datetimeformat is None: 
            datetimeformat='%s %s'%(dateformat,timeformat)
        for key in __dict.keys():
            if   'datetime.datetime' in str(type(__dict[key])): __dict[key]=__dict[key].strftime(datetimeformat)
            elif 'datetime.date'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(dateformat)
            elif 'datetime.time'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(timeformat)
            elif 'decimal.Decimal'   in str(type(__dict[key])): __dict[key]=float(__dict[key])
        return json.dumps(__dict)

    def post(self):
       return self

    def patch(self,**kwargs):
       for field in self.get_column_headers():
           if field in kwargs.keys():
               setattr(self,field,kwargs[field])
       return self

    def delete(self):
       return True

    def get_json_array(self,dateformat='%Y-%m-%d',timeformat='%H:%M:%S',datetimeformat=None):
        """ Gets Request_Type record in JSON array format """
        __list = self.get_list()
        if datetimeformat is None: 
            datetimeformat='%s %s'%(dateformat,timeformat)
        for field in range(len(__list)):
            if   'datetime.datetime' in str(type(__list[field])): __list[field]=__list[field].strftime(datetimeformat)
            elif 'datetime.date'     in str(type(__list[field])): __list[field]=__list[field].strftime(dateformat)
            elif 'datetime.time'     in str(type(__list[field])): __list[field]=__list[field].strftime(timeformat)
            elif 'decimal.Decimal'   in str(type(__list[field])): __list[field]=float(__list[field])
        return __list

    def get_columns(self):
        """ Gets Request_Type record column full details list """
        __list=[{'field': 'Id', 'type': 'int', 'type_flask': 'db.Integer', 'type_sqlalchemy': 'Integer', 'null': 'NO', 'key': 'PRI', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 1, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'IntegerField', 'is_id': False, 'header': 'Id', 'is_time': False}, {'field': 'Description', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 2, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'Description', 'is_time': False}, {'field': 'Table_Name', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 3, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'Table_Name', 'is_time': False}]

        return __list

    def get_column_headers(self):
        """ Gets Request_Type record column headers list """
        __list=['Id', 'Description', 'Table_Name']

        return __list

    def get_column_types(self):
        """ Gets Request_Type record column data types list """
        __list=['Integer', 'String(45)', 'String(45)']

        return __list

    def get_column_meta(self):
        """ Gets Request_Type record column data meta list """
        __list=[('Id', 'Integer'), ('Description', 'String(45)'), ('Table_Name', 'String(45)')]

        return __list

    def get_id(self,Name):
        """ Search for a 'Request_Type' Id looking for field 'Description' """
        Id = None
        try:
            if self.engine is not None:
                Session=sessionmaker(bind=self.engine)
                session=Session()
                Id = session.query(Request_Type.Id).filter(Request_Type.Description==Name).scalar()
                session.flush()
            else:
                session.rollback()
                Id = None
        except Exception as e:
            detail='Request_Type.get_id(%s): Exception: %s'%(Name,e)
            emtec_handle_general_exception(e,detail=detail,module=__name__,function='Request_Type.get_id()',logger=self.logger)
            Id = None
        return Id

    def search(self,Name):
        """ Search for a 'Request_Type' record looking for field 'Description' """
        Id = self.get_id(Name)
        if Id is not None:
            try:
                if self.engine is not None:
                    Session=sessionmaker(bind=self.engine)
                    session=Session()
                    record = session.query(Request_Type).filter(Request_Type.Id==Id).one_or_none()
                    session.flush()
                else:
                    session.rollback()
                    record = None
            except Exception as e:
                detail='Request_Type.search(%s): Exception: %s'%(Name,e)
                emtec_handle_general_exception(e,detail=detail,module=__name__,function='Request_Type.search()',logger=self.logger)
                record = None
        return record

    def search_key(self,Id):
        """ Search for an unique Request_Type record using all key fields (Id) """
        try:
            if self.engine is not None:
                Session=sessionmaker(bind=self.engine)
                session=Session()
                record = session.query(Request_Type).filter(Request_Type.Id==Id).one_or_none()
                session.flush()
            else:
                session.rollback()
                record = None
        except Exception as e:
            detail='Request_Type.search_key(%s): Exception: %s'%(Id,e)
            emtec_handle_general_exception(e,detail=detail,module=__name__,function='Request_Type.search_key()',logger=self.logger)
            record = None
        return record

    def log(self,message,level=logging.DEBUG):
        """ Class Request_Type log function """
        if self.logger is not None:
            self.logger.log(level,message)

# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2022-03-24 17:50:52
# =============================================================================

# GV gen_model_flask.py:418 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/models/orm_requests.py
import sqlalchemy
class Requests(Base):
    __tablename__ = 'Requests'
    engine        = None
    logger        = None

    def check_shard(suffix=None,engine=None):
       if engine is not None:
           try:
               if sqlalchemy.__version__ >= '1.4':
                   inspector = sqlalchemy.inspect(engine)
                   table_exists = inspector.has_table(__class__.__tablename__,schema='butler')
               else:
                   table_exists = engine.dialect.has_table(engine, __class__.__tablename__)
               if not table_exists:
                   metadata=MetaData()
                   metadata.bind=engine
                   __class__.__table__.metadata=metadata
                   __class__.__table__.create(checkfirst=True)
                   if sqlalchemy.__version__ >= '1.4':
                       inspector = sqlalchemy.inspect(engine)
                       table_exists = inspector.has_table(__class__.__tablename__,schema='butler')
                   else:
                       table_exists = engine.dialect.has_table(engine, __class__.__tablename__)
                   if not table_exists:
                       print('460 Table %s does not exist. creation error?'% __class__.__tablename__)
                   else:
                       pass # GV print('462 Table %s exist !!!'% __class__.__tablename__)
               else:
                   pass # GV print('464 Table %s exist !!!'% __class__.__tablename__)
           except Exception as e:
              print(f'gen/gen_model_flask.py: 466 exception: {str(e)}')
           return
    def set_shard(suffix=None,engine=None):
       if suffix is not None:
           name='Requests_{suffix}'.format(suffix=suffix)
           __class__.__tablename__  = name
           __class__.__table__.name = name
       __class__.check_shard(suffix,engine)
       return __class__.__tablename__

    Id               = Column( Integer, primary_key=True, autoincrement=True )
    Type             = Column( Integer, ForeignKey('Request_Type.Id') )
    User_Id          = Column( Integer )
    Approver_Id      = Column( Integer )
    Status           = Column( Integer )
    Creation_Time    = Column( DateTime )
    Last_Status_Time = Column( DateTime )
    Comments         = Column( Text )
    Task_uuid        = Column( String(45) )
    Task_status      = Column( Integer )
    CC_Id            = Column( Integer )
    uuid             = Column( String(45) )
    User_Comments    = Column( Text )
    
    def __init__(self, Id=0, Type=1, User_Id=None, Approver_Id=None, Status=0, Creation_Time=None, Last_Status_Time=None, Comments=None, Task_uuid='None', Task_status=None, CC_Id=None, uuid='None', User_Comments=None,engine=None,logger=None):
        """ Initiates a Requests class record """
        self.engine=engine
        self.logger=logger
        self.Id               = Id
        self.Type             = Type
        self.User_Id          = User_Id
        self.Approver_Id      = Approver_Id
        self.Status           = Status
        self.Creation_Time    = Creation_Time
        self.Last_Status_Time = Last_Status_Time
        self.Comments         = Comments
        self.Task_uuid        = Task_uuid
        self.Task_status      = Task_status
        self.CC_Id            = CC_Id
        self.uuid             = uuid
        self.User_Comments    = User_Comments

        self.log('Created %s'%self)
    def __repr__(self):
        """ default class Requests representation function """
        return "<Requests( Id='%s', Type='%s', User_Id='%s', Approver_Id='%s', Status='%s', Creation_Time='%s', Last_Status_Time='%s', Comments='%s', Task_uuid='%s', Task_status='%s', CC_Id='%s', uuid='%s', User_Comments='%s')>" % \
                ( self.Id, self.Type, self.User_Id, self.Approver_Id, self.Status, self.Creation_Time, self.Last_Status_Time, self.Comments, self.Task_uuid, self.Task_status, self.CC_Id, self.uuid, self.User_Comments)

    def get_list(self):
        """ Gets Requests record in list format """
        __list = [ self.Id, self.Type, self.User_Id, self.Approver_Id, self.Status, self.Creation_Time, self.Last_Status_Time, self.Comments, self.Task_uuid, self.Task_status, self.CC_Id, self.uuid, self.User_Comments]
        return __list

    def get_tuple(self):
        """ Gets Requests record in tuple format """
        __tuple = ( self.Id, self.Type, self.User_Id, self.Approver_Id, self.Status, self.Creation_Time, self.Last_Status_Time, self.Comments, self.Task_uuid, self.Task_status, self.CC_Id, self.uuid, self.User_Comments)
        return __tuple

    def get_dict(self):
        """ Gets Requests record in dict format """
        __dict={'Id':self.Id,'Type':self.Type,'User_Id':self.User_Id,'Approver_Id':self.Approver_Id,'Status':self.Status,'Creation_Time':self.Creation_Time,'Last_Status_Time':self.Last_Status_Time,'Comments':self.Comments,'Task_uuid':self.Task_uuid,'Task_status':self.Task_status,'CC_Id':self.CC_Id,'uuid':self.uuid,'User_Comments':self.User_Comments}

        return __dict

    def get_json_dict(self,dateformat='%Y-%m-%d',timeformat='%H:%M:%S',datetimeformat=None):
        __dict = self.get_dict()
        if datetimeformat is None: 
            datetimeformat='%s %s'%(dateformat,timeformat)
        for key in __dict.keys():
            if   'datetime.datetime' in str(type(__dict[key])): __dict[key]=__dict[key].strftime(datetimeformat)
            elif 'datetime.date'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(dateformat)
            elif 'datetime.time'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(timeformat)
            elif 'decimal.Decimal'   in str(type(__dict[key])): __dict[key]=float(__dict[key])
        return __dict

    def get_json(self,dateformat='%Y-%m-%d',timeformat='%H:%M:%S',datetimeformat=None):
        __dict = self.get_dict()
        if datetimeformat is None: 
            datetimeformat='%s %s'%(dateformat,timeformat)
        for key in __dict.keys():
            if   'datetime.datetime' in str(type(__dict[key])): __dict[key]=__dict[key].strftime(datetimeformat)
            elif 'datetime.date'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(dateformat)
            elif 'datetime.time'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(timeformat)
            elif 'decimal.Decimal'   in str(type(__dict[key])): __dict[key]=float(__dict[key])
        return json.dumps(__dict)

    def post(self):
       return self

    def patch(self,**kwargs):
       for field in self.get_column_headers():
           if field in kwargs.keys():
               setattr(self,field,kwargs[field])
       return self

    def delete(self):
       return True

    def get_json_array(self,dateformat='%Y-%m-%d',timeformat='%H:%M:%S',datetimeformat=None):
        """ Gets Requests record in JSON array format """
        __list = self.get_list()
        if datetimeformat is None: 
            datetimeformat='%s %s'%(dateformat,timeformat)
        for field in range(len(__list)):
            if   'datetime.datetime' in str(type(__list[field])): __list[field]=__list[field].strftime(datetimeformat)
            elif 'datetime.date'     in str(type(__list[field])): __list[field]=__list[field].strftime(dateformat)
            elif 'datetime.time'     in str(type(__list[field])): __list[field]=__list[field].strftime(timeformat)
            elif 'decimal.Decimal'   in str(type(__list[field])): __list[field]=float(__list[field])
        return __list

    def get_columns(self):
        """ Gets Requests record column full details list """
        __list=[{'field': 'Id', 'type': 'int', 'type_flask': 'db.Integer', 'type_sqlalchemy': 'Integer', 'null': 'NO', 'key': 'PRI', 'default': None, 'extra': 'auto_increment', 'is_form_editable': True, 'format': None, 'order': 1, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'IntegerField', 'is_id': True, 'header': 'Id', 'is_time': False}, {'field': 'Type', 'type': 'int', 'type_flask': 'db.Integer', 'type_sqlalchemy': 'Integer', 'null': 'NO', 'key': 'MUL', 'default': '1', 'extra': '', 'is_form_editable': True, 'format': None, 'order': 2, 'is_searchable': True, 'is_fk': True, 'foreign_field': 'Id', 'referenced_table': 'Request_Type', 'referenced_class': 'request_type', 'foreign_key': 'Type', 'foreign_value': 'Description', 'is_numeric': False, 'form_type': 'SelectField', 'is_id': False, 'header': 'Type', 'is_time': False}, {'field': 'User_Id', 'type': 'int', 'type_flask': 'db.Integer', 'type_sqlalchemy': 'Integer', 'null': 'NO', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 3, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'IntegerField', 'is_id': False, 'header': 'User_Id', 'is_time': False}, {'field': 'Approver_Id', 'type': 'int', 'type_flask': 'db.Integer', 'type_sqlalchemy': 'Integer', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 4, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'IntegerField', 'is_id': False, 'header': 'Approver_Id', 'is_time': False}, {'field': 'Status', 'type': 'int', 'type_flask': 'db.Integer', 'type_sqlalchemy': 'Integer', 'null': 'NO', 'key': '', 'default': '0', 'extra': '', 'is_form_editable': True, 'format': None, 'order': 5, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'IntegerField', 'is_id': False, 'header': 'Status', 'is_time': False}, {'field': 'Creation_Time', 'type': 'timestamp', 'type_flask': 'db.DateTime', 'type_sqlalchemy': 'DateTime', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 6, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'DateTimeField', 'is_id': False, 'header': 'Creation_Time', 'is_time': False}, {'field': 'Last_Status_Time', 'type': 'timestamp', 'type_flask': 'db.DateTime', 'type_sqlalchemy': 'DateTime', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 7, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'DateTimeField', 'is_id': False, 'header': 'Last_Status_Time', 'is_time': False}, {'field': 'Comments', 'type': 'text', 'type_flask': 'db.Text', 'type_sqlalchemy': 'Text', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 8, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'Comments', 'is_time': False}, {'field': 'Task_uuid', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 9, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'Task_uuid', 'is_time': False}, {'field': 'Task_status', 'type': 'int', 'type_flask': 'db.Integer', 'type_sqlalchemy': 'Integer', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 10, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'IntegerField', 'is_id': False, 'header': 'Task_status', 'is_time': False}, {'field': 'CC_Id', 'type': 'int', 'type_flask': 'db.Integer', 'type_sqlalchemy': 'Integer', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 11, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'IntegerField', 'is_id': False, 'header': 'CC_Id', 'is_time': False}, {'field': 'uuid', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 12, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'uuid', 'is_time': False}, {'field': 'User_Comments', 'type': 'text', 'type_flask': 'db.Text', 'type_sqlalchemy': 'Text', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 13, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'User_Comments', 'is_time': False}]

        return __list

    def get_column_headers(self):
        """ Gets Requests record column headers list """
        __list=['Id', 'Type', 'User_Id', 'Approver_Id', 'Status', 'Creation_Time', 'Last_Status_Time', 'Comments', 'Task_uuid', 'Task_status', 'CC_Id', 'uuid', 'User_Comments']

        return __list

    def get_column_types(self):
        """ Gets Requests record column data types list """
        __list=['Integer', 'Integer', 'Integer', 'Integer', 'Integer', 'DateTime', 'DateTime', 'Text', 'String(45)', 'Integer', 'Integer', 'String(45)', 'Text']

        return __list

    def get_column_meta(self):
        """ Gets Requests record column data meta list """
        __list=[('Id', 'Integer'), ('Type', 'Integer'), ('User_Id', 'Integer'), ('Approver_Id', 'Integer'), ('Status', 'Integer'), ('Creation_Time', 'DateTime'), ('Last_Status_Time', 'DateTime'), ('Comments', 'Text'), ('Task_uuid', 'String(45)'), ('Task_status', 'Integer'), ('CC_Id', 'Integer'), ('uuid', 'String(45)'), ('User_Comments', 'Text')]

        return __list

    def search_key(self,Id):
        """ Search for an unique Requests record using all key fields (Id) """
        try:
            if self.engine is not None:
                Session=sessionmaker(bind=self.engine)
                session=Session()
                record = session.query(Requests).filter(Requests.Id==Id).one_or_none()
                session.flush()
            else:
                session.rollback()
                record = None
        except Exception as e:
            detail='Requests.search_key(%s): Exception: %s'%(Id,e)
            emtec_handle_general_exception(e,detail=detail,module=__name__,function='Requests.search_key()',logger=self.logger)
            record = None
        return record

    def log(self,message,level=logging.DEBUG):
        """ Class Requests log function """
        if self.logger is not None:
            self.logger.log(level,message)

# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2022-03-24 17:50:52
# =============================================================================

# GV gen_model_flask.py:418 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/models/orm_roles.py
import sqlalchemy
class Roles(Base):
    __tablename__ = 'Roles'
    engine        = None
    logger        = None

    def check_shard(suffix=None,engine=None):
       if engine is not None:
           try:
               if sqlalchemy.__version__ >= '1.4':
                   inspector = sqlalchemy.inspect(engine)
                   table_exists = inspector.has_table(__class__.__tablename__,schema='butler')
               else:
                   table_exists = engine.dialect.has_table(engine, __class__.__tablename__)
               if not table_exists:
                   metadata=MetaData()
                   metadata.bind=engine
                   __class__.__table__.metadata=metadata
                   __class__.__table__.create(checkfirst=True)
                   if sqlalchemy.__version__ >= '1.4':
                       inspector = sqlalchemy.inspect(engine)
                       table_exists = inspector.has_table(__class__.__tablename__,schema='butler')
                   else:
                       table_exists = engine.dialect.has_table(engine, __class__.__tablename__)
                   if not table_exists:
                       print('460 Table %s does not exist. creation error?'% __class__.__tablename__)
                   else:
                       pass # GV print('462 Table %s exist !!!'% __class__.__tablename__)
               else:
                   pass # GV print('464 Table %s exist !!!'% __class__.__tablename__)
           except Exception as e:
              print(f'gen/gen_model_flask.py: 466 exception: {str(e)}')
           return
    def set_shard(suffix=None,engine=None):
       if suffix is not None:
           name='Roles_{suffix}'.format(suffix=suffix)
           __class__.__tablename__  = name
           __class__.__table__.name = name
       __class__.check_shard(suffix,engine)
       return __class__.__tablename__

    id          = Column( Integer, primary_key=True )
    name        = Column( String(64) )
    default     = Column( Boolean )
    permissions = Column( Integer )
    
    def __init__(self, id=None, name='None', default=None, permissions=None,engine=None,logger=None):
        """ Initiates a Roles class record """
        self.engine=engine
        self.logger=logger
        self.id          = id
        self.name        = name
        self.default     = default
        self.permissions = permissions

        self.log('Created %s'%self)
    def __repr__(self):
        """ default class Roles representation function """
        return "<Roles( id='%s', name='%s', default='%s', permissions='%s')>" % \
                ( self.id, self.name, self.default, self.permissions)

    def get_list(self):
        """ Gets Roles record in list format """
        __list = [ self.id, self.name, self.default, self.permissions]
        return __list

    def get_tuple(self):
        """ Gets Roles record in tuple format """
        __tuple = ( self.id, self.name, self.default, self.permissions)
        return __tuple

    def get_dict(self):
        """ Gets Roles record in dict format """
        __dict={'id':self.id,'name':self.name,'default':self.default,'permissions':self.permissions}

        return __dict

    def get_json_dict(self,dateformat='%Y-%m-%d',timeformat='%H:%M:%S',datetimeformat=None):
        __dict = self.get_dict()
        if datetimeformat is None: 
            datetimeformat='%s %s'%(dateformat,timeformat)
        for key in __dict.keys():
            if   'datetime.datetime' in str(type(__dict[key])): __dict[key]=__dict[key].strftime(datetimeformat)
            elif 'datetime.date'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(dateformat)
            elif 'datetime.time'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(timeformat)
            elif 'decimal.Decimal'   in str(type(__dict[key])): __dict[key]=float(__dict[key])
        return __dict

    def get_json(self,dateformat='%Y-%m-%d',timeformat='%H:%M:%S',datetimeformat=None):
        __dict = self.get_dict()
        if datetimeformat is None: 
            datetimeformat='%s %s'%(dateformat,timeformat)
        for key in __dict.keys():
            if   'datetime.datetime' in str(type(__dict[key])): __dict[key]=__dict[key].strftime(datetimeformat)
            elif 'datetime.date'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(dateformat)
            elif 'datetime.time'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(timeformat)
            elif 'decimal.Decimal'   in str(type(__dict[key])): __dict[key]=float(__dict[key])
        return json.dumps(__dict)

    def post(self):
       return self

    def patch(self,**kwargs):
       for field in self.get_column_headers():
           if field in kwargs.keys():
               setattr(self,field,kwargs[field])
       return self

    def delete(self):
       return True

    def get_json_array(self,dateformat='%Y-%m-%d',timeformat='%H:%M:%S',datetimeformat=None):
        """ Gets Roles record in JSON array format """
        __list = self.get_list()
        if datetimeformat is None: 
            datetimeformat='%s %s'%(dateformat,timeformat)
        for field in range(len(__list)):
            if   'datetime.datetime' in str(type(__list[field])): __list[field]=__list[field].strftime(datetimeformat)
            elif 'datetime.date'     in str(type(__list[field])): __list[field]=__list[field].strftime(dateformat)
            elif 'datetime.time'     in str(type(__list[field])): __list[field]=__list[field].strftime(timeformat)
            elif 'decimal.Decimal'   in str(type(__list[field])): __list[field]=float(__list[field])
        return __list

    def get_columns(self):
        """ Gets Roles record column full details list """
        __list=[{'field': 'id', 'type': 'int', 'type_flask': 'db.Integer', 'type_sqlalchemy': 'Integer', 'null': 'NO', 'key': 'PRI', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 1, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'IntegerField', 'is_id': False, 'header': 'id', 'is_time': False}, {'field': 'name', 'type': 'varchar(64)', 'type_flask': 'db.String(64)', 'type_sqlalchemy': 'String(64)', 'null': 'YES', 'key': 'UNI', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 2, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'name', 'is_time': False}, {'field': 'default', 'type': 'tinyint', 'type_flask': 'db.Boolean', 'type_sqlalchemy': 'Boolean', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 3, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'BooleanField', 'is_id': False, 'header': 'default', 'is_time': False}, {'field': 'permissions', 'type': 'int', 'type_flask': 'db.Integer', 'type_sqlalchemy': 'Integer', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 4, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'IntegerField', 'is_id': False, 'header': 'permissions', 'is_time': False}]

        return __list

    def get_column_headers(self):
        """ Gets Roles record column headers list """
        __list=['id', 'name', 'default', 'permissions']

        return __list

    def get_column_types(self):
        """ Gets Roles record column data types list """
        __list=['Integer', 'String(64)', 'Boolean', 'Integer']

        return __list

    def get_column_meta(self):
        """ Gets Roles record column data meta list """
        __list=[('id', 'Integer'), ('name', 'String(64)'), ('default', 'Boolean'), ('permissions', 'Integer')]

        return __list

    def search_key(self,id):
        """ Search for an unique Roles record using all key fields (id) """
        try:
            if self.engine is not None:
                Session=sessionmaker(bind=self.engine)
                session=Session()
                record = session.query(Roles).filter(Roles.id==id).one_or_none()
                session.flush()
            else:
                session.rollback()
                record = None
        except Exception as e:
            detail='Roles.search_key(%s): Exception: %s'%(id,e)
            emtec_handle_general_exception(e,detail=detail,module=__name__,function='Roles.search_key()',logger=self.logger)
            record = None
        return record

    def log(self,message,level=logging.DEBUG):
        """ Class Roles log function """
        if self.logger is not None:
            self.logger.log(level,message)

# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2022-03-24 17:50:52
# =============================================================================

# GV gen_model_flask.py:418 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/models/orm_subnets.py
import sqlalchemy
class Subnets(Base):
    __tablename__ = 'Subnets'
    engine        = None
    logger        = None

    def check_shard(suffix=None,engine=None):
       if engine is not None:
           try:
               if sqlalchemy.__version__ >= '1.4':
                   inspector = sqlalchemy.inspect(engine)
                   table_exists = inspector.has_table(__class__.__tablename__,schema='butler')
               else:
                   table_exists = engine.dialect.has_table(engine, __class__.__tablename__)
               if not table_exists:
                   metadata=MetaData()
                   metadata.bind=engine
                   __class__.__table__.metadata=metadata
                   __class__.__table__.create(checkfirst=True)
                   if sqlalchemy.__version__ >= '1.4':
                       inspector = sqlalchemy.inspect(engine)
                       table_exists = inspector.has_table(__class__.__tablename__,schema='butler')
                   else:
                       table_exists = engine.dialect.has_table(engine, __class__.__tablename__)
                   if not table_exists:
                       print('460 Table %s does not exist. creation error?'% __class__.__tablename__)
                   else:
                       pass # GV print('462 Table %s exist !!!'% __class__.__tablename__)
               else:
                   pass # GV print('464 Table %s exist !!!'% __class__.__tablename__)
           except Exception as e:
              print(f'gen/gen_model_flask.py: 466 exception: {str(e)}')
           return
    def set_shard(suffix=None,engine=None):
       if suffix is not None:
           name='Subnets_{suffix}'.format(suffix=suffix)
           __class__.__tablename__  = name
           __class__.__table__.name = name
       __class__.check_shard(suffix,engine)
       return __class__.__tablename__

    uuid               = Column( String(45), primary_key=True )
    name               = Column( String(45) )
    vlan_id            = Column( Integer )
    vswitch_name       = Column( String(45) )
    type               = Column( String(45) )
    default_gateway_ip = Column( String(45) )
    range              = Column( String(45) )
    prefix_length      = Column( Integer )
    subnet_ip          = Column( String(45) )
    cluster            = Column( String(45) )
    
    def __init__(self, uuid='None', name='None', vlan_id=None, vswitch_name='None', type='None', default_gateway_ip='None', range='None', prefix_length=None, subnet_ip='None', cluster='None',engine=None,logger=None):
        """ Initiates a Subnets class record """
        self.engine=engine
        self.logger=logger
        self.uuid               = uuid
        self.name               = name
        self.vlan_id            = vlan_id
        self.vswitch_name       = vswitch_name
        self.type               = type
        self.default_gateway_ip = default_gateway_ip
        self.range              = range
        self.prefix_length      = prefix_length
        self.subnet_ip          = subnet_ip
        self.cluster            = cluster

        self.log('Created %s'%self)
    def __repr__(self):
        """ default class Subnets representation function """
        return "<Subnets( uuid='%s', name='%s', vlan_id='%s', vswitch_name='%s', type='%s', default_gateway_ip='%s', range='%s', prefix_length='%s', subnet_ip='%s', cluster='%s')>" % \
                ( self.uuid, self.name, self.vlan_id, self.vswitch_name, self.type, self.default_gateway_ip, self.range, self.prefix_length, self.subnet_ip, self.cluster)

    def get_list(self):
        """ Gets Subnets record in list format """
        __list = [ self.uuid, self.name, self.vlan_id, self.vswitch_name, self.type, self.default_gateway_ip, self.range, self.prefix_length, self.subnet_ip, self.cluster]
        return __list

    def get_tuple(self):
        """ Gets Subnets record in tuple format """
        __tuple = ( self.uuid, self.name, self.vlan_id, self.vswitch_name, self.type, self.default_gateway_ip, self.range, self.prefix_length, self.subnet_ip, self.cluster)
        return __tuple

    def get_dict(self):
        """ Gets Subnets record in dict format """
        __dict={'uuid':self.uuid,'name':self.name,'vlan_id':self.vlan_id,'vswitch_name':self.vswitch_name,'type':self.type,'default_gateway_ip':self.default_gateway_ip,'range':self.range,'prefix_length':self.prefix_length,'subnet_ip':self.subnet_ip,'cluster':self.cluster}

        return __dict

    def get_json_dict(self,dateformat='%Y-%m-%d',timeformat='%H:%M:%S',datetimeformat=None):
        __dict = self.get_dict()
        if datetimeformat is None: 
            datetimeformat='%s %s'%(dateformat,timeformat)
        for key in __dict.keys():
            if   'datetime.datetime' in str(type(__dict[key])): __dict[key]=__dict[key].strftime(datetimeformat)
            elif 'datetime.date'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(dateformat)
            elif 'datetime.time'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(timeformat)
            elif 'decimal.Decimal'   in str(type(__dict[key])): __dict[key]=float(__dict[key])
        return __dict

    def get_json(self,dateformat='%Y-%m-%d',timeformat='%H:%M:%S',datetimeformat=None):
        __dict = self.get_dict()
        if datetimeformat is None: 
            datetimeformat='%s %s'%(dateformat,timeformat)
        for key in __dict.keys():
            if   'datetime.datetime' in str(type(__dict[key])): __dict[key]=__dict[key].strftime(datetimeformat)
            elif 'datetime.date'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(dateformat)
            elif 'datetime.time'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(timeformat)
            elif 'decimal.Decimal'   in str(type(__dict[key])): __dict[key]=float(__dict[key])
        return json.dumps(__dict)

    def post(self):
       return self

    def patch(self,**kwargs):
       for field in self.get_column_headers():
           if field in kwargs.keys():
               setattr(self,field,kwargs[field])
       return self

    def delete(self):
       return True

    def get_json_array(self,dateformat='%Y-%m-%d',timeformat='%H:%M:%S',datetimeformat=None):
        """ Gets Subnets record in JSON array format """
        __list = self.get_list()
        if datetimeformat is None: 
            datetimeformat='%s %s'%(dateformat,timeformat)
        for field in range(len(__list)):
            if   'datetime.datetime' in str(type(__list[field])): __list[field]=__list[field].strftime(datetimeformat)
            elif 'datetime.date'     in str(type(__list[field])): __list[field]=__list[field].strftime(dateformat)
            elif 'datetime.time'     in str(type(__list[field])): __list[field]=__list[field].strftime(timeformat)
            elif 'decimal.Decimal'   in str(type(__list[field])): __list[field]=float(__list[field])
        return __list

    def get_columns(self):
        """ Gets Subnets record column full details list """
        __list=[{'field': 'uuid', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'NO', 'key': 'PRI', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 1, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'uuid', 'is_time': False}, {'field': 'name', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 2, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'name', 'is_time': False}, {'field': 'vlan_id', 'type': 'int', 'type_flask': 'db.Integer', 'type_sqlalchemy': 'Integer', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 3, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'IntegerField', 'is_id': False, 'header': 'vlan_id', 'is_time': False}, {'field': 'vswitch_name', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 4, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'vswitch_name', 'is_time': False}, {'field': 'type', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 5, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'type', 'is_time': False}, {'field': 'default_gateway_ip', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 6, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'default_gateway_ip', 'is_time': False}, {'field': 'range', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 7, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'range', 'is_time': False}, {'field': 'prefix_length', 'type': 'int', 'type_flask': 'db.Integer', 'type_sqlalchemy': 'Integer', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 8, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'IntegerField', 'is_id': False, 'header': 'prefix_length', 'is_time': False}, {'field': 'subnet_ip', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 9, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'subnet_ip', 'is_time': False}, {'field': 'cluster', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 10, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'cluster', 'is_time': False}]

        return __list

    def get_column_headers(self):
        """ Gets Subnets record column headers list """
        __list=['uuid', 'name', 'vlan_id', 'vswitch_name', 'type', 'default_gateway_ip', 'range', 'prefix_length', 'subnet_ip', 'cluster']

        return __list

    def get_column_types(self):
        """ Gets Subnets record column data types list """
        __list=['String(45)', 'String(45)', 'Integer', 'String(45)', 'String(45)', 'String(45)', 'String(45)', 'Integer', 'String(45)', 'String(45)']

        return __list

    def get_column_meta(self):
        """ Gets Subnets record column data meta list """
        __list=[('uuid', 'String(45)'), ('name', 'String(45)'), ('vlan_id', 'Integer'), ('vswitch_name', 'String(45)'), ('type', 'String(45)'), ('default_gateway_ip', 'String(45)'), ('range', 'String(45)'), ('prefix_length', 'Integer'), ('subnet_ip', 'String(45)'), ('cluster', 'String(45)')]

        return __list

    def search_key(self,uuid):
        """ Search for an unique Subnets record using all key fields (uuid) """
        try:
            if self.engine is not None:
                Session=sessionmaker(bind=self.engine)
                session=Session()
                record = session.query(Subnets).filter(Subnets.uuid==uuid).one_or_none()
                session.flush()
            else:
                session.rollback()
                record = None
        except Exception as e:
            detail='Subnets.search_key(%s): Exception: %s'%(uuid,e)
            emtec_handle_general_exception(e,detail=detail,module=__name__,function='Subnets.search_key()',logger=self.logger)
            record = None
        return record

    def log(self,message,level=logging.DEBUG):
        """ Class Subnets log function """
        if self.logger is not None:
            self.logger.log(level,message)

# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2022-03-24 17:50:52
# =============================================================================

# GV gen_model_flask.py:418 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/models/orm_users.py
import sqlalchemy
class Users(Base):
    __tablename__ = 'Users'
    engine        = None
    logger        = None

    def check_shard(suffix=None,engine=None):
       if engine is not None:
           try:
               if sqlalchemy.__version__ >= '1.4':
                   inspector = sqlalchemy.inspect(engine)
                   table_exists = inspector.has_table(__class__.__tablename__,schema='butler')
               else:
                   table_exists = engine.dialect.has_table(engine, __class__.__tablename__)
               if not table_exists:
                   metadata=MetaData()
                   metadata.bind=engine
                   __class__.__table__.metadata=metadata
                   __class__.__table__.create(checkfirst=True)
                   if sqlalchemy.__version__ >= '1.4':
                       inspector = sqlalchemy.inspect(engine)
                       table_exists = inspector.has_table(__class__.__tablename__,schema='butler')
                   else:
                       table_exists = engine.dialect.has_table(engine, __class__.__tablename__)
                   if not table_exists:
                       print('460 Table %s does not exist. creation error?'% __class__.__tablename__)
                   else:
                       pass # GV print('462 Table %s exist !!!'% __class__.__tablename__)
               else:
                   pass # GV print('464 Table %s exist !!!'% __class__.__tablename__)
           except Exception as e:
              print(f'gen/gen_model_flask.py: 466 exception: {str(e)}')
           return
    def set_shard(suffix=None,engine=None):
       if suffix is not None:
           name='Users_{suffix}'.format(suffix=suffix)
           __class__.__tablename__  = name
           __class__.__table__.name = name
       __class__.check_shard(suffix,engine)
       return __class__.__tablename__

    id            = Column( Integer, primary_key=True, autoincrement=True )
    username      = Column( String(64) )
    name          = Column( String(255) )
    role_id       = Column( Integer, ForeignKey('Roles.id') )
    email         = Column( String(64) )
    password_hash = Column( String(128) )
    confirmed     = Column( Boolean )
    CC_Id         = Column( Integer )
    roles         = Column( String(255) )
    ldap          = Column( Boolean )
    ldap_method   = Column( String(45) )
    ldap_user     = Column( String(45) )
    ldap_common   = Column( String(45) )
    ldap_host     = Column( String(45) )
    ldap_port     = Column( Integer )
    ldap_domain   = Column( String(45) )
    vars          = Column( String(255) )
    
    def __init__(self, id=0, username='None', name='None', role_id=None, email='None', password_hash='None', confirmed=0, CC_Id=1, roles='None', ldap=0, ldap_method='None', ldap_user='None', ldap_common='None', ldap_host='None', ldap_port=0, ldap_domain='None', vars='None',engine=None,logger=None):
        """ Initiates a Users class record """
        self.engine=engine
        self.logger=logger
        self.id            = id
        self.username      = username
        self.name          = name
        self.role_id       = role_id
        self.email         = email
        self.password_hash = password_hash
        self.confirmed     = confirmed
        self.CC_Id         = CC_Id
        self.roles         = roles
        self.ldap          = ldap
        self.ldap_method   = ldap_method
        self.ldap_user     = ldap_user
        self.ldap_common   = ldap_common
        self.ldap_host     = ldap_host
        self.ldap_port     = ldap_port
        self.ldap_domain   = ldap_domain
        self.vars          = vars

        self.log('Created %s'%self)
    def __repr__(self):
        """ default class Users representation function """
        return "<Users( id='%s', username='%s', name='%s', role_id='%s', email='%s', password_hash='%s', confirmed='%s', CC_Id='%s', roles='%s', ldap='%s', ldap_method='%s', ldap_user='%s', ldap_common='%s', ldap_host='%s', ldap_port='%s', ldap_domain='%s', vars='%s')>" % \
                ( self.id, self.username, self.name, self.role_id, self.email, self.password_hash, self.confirmed, self.CC_Id, self.roles, self.ldap, self.ldap_method, self.ldap_user, self.ldap_common, self.ldap_host, self.ldap_port, self.ldap_domain, self.vars)

    def get_list(self):
        """ Gets Users record in list format """
        __list = [ self.id, self.username, self.name, self.role_id, self.email, self.password_hash, self.confirmed, self.CC_Id, self.roles, self.ldap, self.ldap_method, self.ldap_user, self.ldap_common, self.ldap_host, self.ldap_port, self.ldap_domain, self.vars]
        return __list

    def get_tuple(self):
        """ Gets Users record in tuple format """
        __tuple = ( self.id, self.username, self.name, self.role_id, self.email, self.password_hash, self.confirmed, self.CC_Id, self.roles, self.ldap, self.ldap_method, self.ldap_user, self.ldap_common, self.ldap_host, self.ldap_port, self.ldap_domain, self.vars)
        return __tuple

    def get_dict(self):
        """ Gets Users record in dict format """
        __dict={'id':self.id,'username':self.username,'name':self.name,'role_id':self.role_id,'email':self.email,'password_hash':self.password_hash,'confirmed':self.confirmed,'CC_Id':self.CC_Id,'roles':self.roles,'ldap':self.ldap,'ldap_method':self.ldap_method,'ldap_user':self.ldap_user,'ldap_common':self.ldap_common,'ldap_host':self.ldap_host,'ldap_port':self.ldap_port,'ldap_domain':self.ldap_domain,'vars':self.vars}

        return __dict

    def get_json_dict(self,dateformat='%Y-%m-%d',timeformat='%H:%M:%S',datetimeformat=None):
        __dict = self.get_dict()
        if datetimeformat is None: 
            datetimeformat='%s %s'%(dateformat,timeformat)
        for key in __dict.keys():
            if   'datetime.datetime' in str(type(__dict[key])): __dict[key]=__dict[key].strftime(datetimeformat)
            elif 'datetime.date'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(dateformat)
            elif 'datetime.time'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(timeformat)
            elif 'decimal.Decimal'   in str(type(__dict[key])): __dict[key]=float(__dict[key])
        return __dict

    def get_json(self,dateformat='%Y-%m-%d',timeformat='%H:%M:%S',datetimeformat=None):
        __dict = self.get_dict()
        if datetimeformat is None: 
            datetimeformat='%s %s'%(dateformat,timeformat)
        for key in __dict.keys():
            if   'datetime.datetime' in str(type(__dict[key])): __dict[key]=__dict[key].strftime(datetimeformat)
            elif 'datetime.date'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(dateformat)
            elif 'datetime.time'     in str(type(__dict[key])): __dict[key]=__dict[key].strftime(timeformat)
            elif 'decimal.Decimal'   in str(type(__dict[key])): __dict[key]=float(__dict[key])
        return json.dumps(__dict)

    def post(self):
       return self

    def patch(self,**kwargs):
       for field in self.get_column_headers():
           if field in kwargs.keys():
               setattr(self,field,kwargs[field])
       return self

    def delete(self):
       return True

    def get_json_array(self,dateformat='%Y-%m-%d',timeformat='%H:%M:%S',datetimeformat=None):
        """ Gets Users record in JSON array format """
        __list = self.get_list()
        if datetimeformat is None: 
            datetimeformat='%s %s'%(dateformat,timeformat)
        for field in range(len(__list)):
            if   'datetime.datetime' in str(type(__list[field])): __list[field]=__list[field].strftime(datetimeformat)
            elif 'datetime.date'     in str(type(__list[field])): __list[field]=__list[field].strftime(dateformat)
            elif 'datetime.time'     in str(type(__list[field])): __list[field]=__list[field].strftime(timeformat)
            elif 'decimal.Decimal'   in str(type(__list[field])): __list[field]=float(__list[field])
        return __list

    def get_columns(self):
        """ Gets Users record column full details list """
        __list=[{'field': 'id', 'type': 'int', 'type_flask': 'db.Integer', 'type_sqlalchemy': 'Integer', 'null': 'NO', 'key': 'PRI', 'default': None, 'extra': 'auto_increment', 'is_form_editable': True, 'format': None, 'order': 1, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'IntegerField', 'is_id': True, 'header': 'id', 'is_time': False}, {'field': 'username', 'type': 'varchar(64)', 'type_flask': 'db.String(64)', 'type_sqlalchemy': 'String(64)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 2, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'username', 'is_time': False}, {'field': 'name', 'type': 'varchar(255)', 'type_flask': 'db.String(255)', 'type_sqlalchemy': 'String(255)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 3, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'name', 'is_time': False}, {'field': 'role_id', 'type': 'int', 'type_flask': 'db.Integer', 'type_sqlalchemy': 'Integer', 'null': 'NO', 'key': 'MUL', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 4, 'is_searchable': True, 'is_fk': True, 'foreign_field': 'id', 'referenced_table': 'Roles', 'referenced_class': 'Role', 'foreign_key': 'id', 'foreign_value': 'name', 'is_numeric': False, 'form_type': 'SelectField', 'is_id': False, 'header': 'role_id', 'is_time': False}, {'field': 'email', 'type': 'varchar(64)', 'type_flask': 'db.String(64)', 'type_sqlalchemy': 'String(64)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 5, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'email', 'is_time': False}, {'field': 'password_hash', 'type': 'varchar(128)', 'type_flask': 'db.String(128)', 'type_sqlalchemy': 'String(128)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 6, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'password_hash', 'is_time': False}, {'field': 'confirmed', 'type': 'tinyint', 'type_flask': 'db.Boolean', 'type_sqlalchemy': 'Boolean', 'null': 'YES', 'key': '', 'default': '0', 'extra': '', 'is_form_editable': True, 'format': None, 'order': 7, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'BooleanField', 'is_id': False, 'header': 'confirmed', 'is_time': False}, {'field': 'CC_Id', 'type': 'int', 'type_flask': 'db.Integer', 'type_sqlalchemy': 'Integer', 'null': 'YES', 'key': '', 'default': '1', 'extra': '', 'is_form_editable': True, 'format': None, 'order': 8, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'IntegerField', 'is_id': False, 'header': 'CC_Id', 'is_time': False}, {'field': 'roles', 'type': 'varchar(255)', 'type_flask': 'db.String(255)', 'type_sqlalchemy': 'String(255)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 9, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'roles', 'is_time': False}, {'field': 'ldap', 'type': 'tinyint', 'type_flask': 'db.Boolean', 'type_sqlalchemy': 'Boolean', 'null': 'YES', 'key': '', 'default': '0', 'extra': '', 'is_form_editable': True, 'format': None, 'order': 10, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'BooleanField', 'is_id': False, 'header': 'ldap', 'is_time': False}, {'field': 'ldap_method', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 11, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'ldap_method', 'is_time': False}, {'field': 'ldap_user', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 12, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'ldap_user', 'is_time': False}, {'field': 'ldap_common', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 13, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'ldap_common', 'is_time': False}, {'field': 'ldap_host', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 14, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'ldap_host', 'is_time': False}, {'field': 'ldap_port', 'type': 'int', 'type_flask': 'db.Integer', 'type_sqlalchemy': 'Integer', 'null': 'YES', 'key': '', 'default': '0', 'extra': '', 'is_form_editable': True, 'format': None, 'order': 15, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'IntegerField', 'is_id': False, 'header': 'ldap_port', 'is_time': False}, {'field': 'ldap_domain', 'type': 'varchar(45)', 'type_flask': 'db.String(45)', 'type_sqlalchemy': 'String(45)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 16, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'ldap_domain', 'is_time': False}, {'field': 'vars', 'type': 'varchar(255)', 'type_flask': 'db.String(255)', 'type_sqlalchemy': 'String(255)', 'null': 'YES', 'key': '', 'default': None, 'extra': '', 'is_form_editable': True, 'format': None, 'order': 17, 'is_searchable': True, 'is_fk': False, 'foreign_field': None, 'is_numeric': False, 'form_type': 'StringField', 'is_id': False, 'header': 'vars', 'is_time': False}]

        return __list

    def get_column_headers(self):
        """ Gets Users record column headers list """
        __list=['id', 'username', 'name', 'role_id', 'email', 'password_hash', 'confirmed', 'CC_Id', 'roles', 'ldap', 'ldap_method', 'ldap_user', 'ldap_common', 'ldap_host', 'ldap_port', 'ldap_domain', 'vars']

        return __list

    def get_column_types(self):
        """ Gets Users record column data types list """
        __list=['Integer', 'String(64)', 'String(255)', 'Integer', 'String(64)', 'String(128)', 'Boolean', 'Integer', 'String(255)', 'Boolean', 'String(45)', 'String(45)', 'String(45)', 'String(45)', 'Integer', 'String(45)', 'String(255)']

        return __list

    def get_column_meta(self):
        """ Gets Users record column data meta list """
        __list=[('id', 'Integer'), ('username', 'String(64)'), ('name', 'String(255)'), ('role_id', 'Integer'), ('email', 'String(64)'), ('password_hash', 'String(128)'), ('confirmed', 'Boolean'), ('CC_Id', 'Integer'), ('roles', 'String(255)'), ('ldap', 'Boolean'), ('ldap_method', 'String(45)'), ('ldap_user', 'String(45)'), ('ldap_common', 'String(45)'), ('ldap_host', 'String(45)'), ('ldap_port', 'Integer'), ('ldap_domain', 'String(45)'), ('vars', 'String(255)')]

        return __list

    def search_key(self,id):
        """ Search for an unique Users record using all key fields (id) """
        try:
            if self.engine is not None:
                Session=sessionmaker(bind=self.engine)
                session=Session()
                record = session.query(Users).filter(Users.id==id).one_or_none()
                session.flush()
            else:
                session.rollback()
                record = None
        except Exception as e:
            detail='Users.search_key(%s): Exception: %s'%(id,e)
            emtec_handle_general_exception(e,detail=detail,module=__name__,function='Users.search_key()',logger=self.logger)
            record = None
        return record

    def log(self,message,level=logging.DEBUG):
        """ Class Users log function """
        if self.logger is not None:
            self.logger.log(level,message)


