# ======================================================================
# Models File
# Assures ORM and Flask models are available for application
# source file name: models_py_header.py
# Static Header File. 
# source: models_py_header.py
# GLVH 2019-08-16
# GLVH 2020-01-30 JSON Serializing code added
# ----------------------------------------------------------------------
from app                    import db
from app                    import login_manager

from datetime               import datetime

from sqlalchemy             import Column
from sqlalchemy             import ForeignKey
from sqlalchemy             import String
from sqlalchemy             import Integer, BigInteger, Numeric
from sqlalchemy             import Date, Time, DateTime
from sqlalchemy             import Boolean

from flask_sqlalchemy       import SQLAlchemy
from copy                   import copy, deepcopy

# Required form Authorization subsystem
from werkzeug.security      import generate_password_hash, check_password_hash
from itsdangerous           import TimedJSONWebSignatureSerializer as Serializer
from flask                  import current_app
from flask_login            import UserMixin, AnonymousUserMixin

# JSON Serializing enabling code
from sqlalchemy.inspection import inspect

class Serializer(object):

    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]

# 20200224 GV force import of the whole emtec db library ---------------
from emtec.butler.db.orm_model       import *
from emtec.butler.db.flask_models    import *
# ======================================================================
# =============================================================================
# Models File
# Authorization subsystem. 
# Static File. 
# GLVH 2018-12-17
# source: models_py_header_auth.py
# =============================================================================

class Permission:
    CUSTOMER            = 0x001
    VIEW                = 0x002
    DELETE              = 0x004
    MODIFY              = 0x008
    REPORT              = 0x010
    EXPORT              = 0x020
    RESERVED040         = 0x040
    ADMINISTER          = 0x080
    AUDIT               = 0x100
    RESERVED200         = 0x200
    RESERVED400         = 0x400
    GOD                 = 0x8

class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2021-04-16 13:26:00
# =============================================================================

# gen_model_flask.py:115 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/models/flask_categories.py
class categories(db.Model,Serializer):
    __tablename__ = 'Categories'

    def set_shard(suffix=None):
       if suffix is not None:
           name='Categories_{suffix}'.format(suffix=suffix)
           __class__.__tablename__  = name
           __class__.__table__.name = name
       return __class__.__tablename__

    category_name        = db.Column( db.String(45), primary_key=True )
    category_description = db.Column( db.String(45) )

    # child_table=None gen_children=True
    nutanix_prism_vm     = db.relationship('nutanix_prism_vm',backref='categories',lazy='dynamic')

    # looking for include file: /home/gvalera/GIT/EG-Suite-Tools/Butler/code/src/include/models/flask_categories_properties.py
    # file: /home/gvalera/GIT/EG-Suite-Tools/Butler/code/src/include/models/flask_categories_properties.py not found
    def __init__(self, category_name='None', category_description='None'):
        self.category_name        = category_name
        self.category_description = category_description

    def __repr__(self):
        return "<Categories( category_name='%s', category_description='%s')>" % \
                ( self.category_name, self.category_description)

# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2021-04-16 13:26:00
# =============================================================================

# gen_model_flask.py:115 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/models/flask_clusters.py
class clusters(db.Model,Serializer):
    __tablename__ = 'Clusters'

    def set_shard(suffix=None):
       if suffix is not None:
           name='Clusters_{suffix}'.format(suffix=suffix)
           __class__.__tablename__  = name
           __class__.__table__.name = name
       return __class__.__tablename__

    cluster_uuid     = db.Column( db.String(45), primary_key=True )
    cluster_name     = db.Column( db.String(45) )
    cluster_username = db.Column( db.String(45) )
    cluster_password = db.Column( db.String(45) )
    cluster_ip       = db.Column( db.String(45) )

    # child_table=None gen_children=True
    nutanix_prism_vm = db.relationship('nutanix_prism_vm',backref='clusters',lazy='dynamic')

    # looking for include file: /home/gvalera/GIT/EG-Suite-Tools/Butler/code/src/include/models/flask_clusters_properties.py
    # file: /home/gvalera/GIT/EG-Suite-Tools/Butler/code/src/include/models/flask_clusters_properties.py not found
    def __init__(self, cluster_uuid='None', cluster_name='None', cluster_username='None', cluster_password='None', cluster_ip='None'):
        self.cluster_uuid     = cluster_uuid
        self.cluster_name     = cluster_name
        self.cluster_username = cluster_username
        self.cluster_password = cluster_password
        self.cluster_ip       = cluster_ip

    def __repr__(self):
        return "<Clusters( cluster_uuid='%s', cluster_name='%s', cluster_username='%s', cluster_password='%s', cluster_ip='%s')>" % \
                ( self.cluster_uuid, self.cluster_name, self.cluster_username, self.cluster_password, self.cluster_ip)

# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2021-04-16 13:26:00
# =============================================================================

# gen_model_flask.py:115 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/models/flask_cost_centers.py
class cost_centers(db.Model,Serializer):
    __tablename__ = 'Cost_Centers'

    def set_shard(suffix=None):
       if suffix is not None:
           name='Cost_Centers_{suffix}'.format(suffix=suffix)
           __class__.__tablename__  = name
           __class__.__table__.name = name
       return __class__.__tablename__

    CC_Id          = db.Column( db.Integer, primary_key=True, autoincrement=True )
    CC_Code        = db.Column( db.String(45) )
    CC_Description = db.Column( db.String(255) )
    Cur_Code       = db.Column( db.String(3) )
    CC_Parent_Code = db.Column( db.String(45), default='1' )
    CC_Reg_Exp     = db.Column( db.String(45) )
    CC_Reference   = db.Column( db.String(245) )


    # looking for include file: /home/gvalera/GIT/EG-Suite-Tools/Butler/code/src/include/models/flask_cost_centers_properties.py
    # file: /home/gvalera/GIT/EG-Suite-Tools/Butler/code/src/include/models/flask_cost_centers_properties.py not found
    def __init__(self, CC_Id=0, CC_Code='None', CC_Description='None', Cur_Code='None', CC_Parent_Code='1', CC_Reg_Exp='None', CC_Reference='None'):
        self.CC_Id          = CC_Id
        self.CC_Code        = CC_Code
        self.CC_Description = CC_Description
        self.Cur_Code       = Cur_Code
        self.CC_Parent_Code = CC_Parent_Code
        self.CC_Reg_Exp     = CC_Reg_Exp
        self.CC_Reference   = CC_Reference

    def __repr__(self):
        return "<Cost_Centers( CC_Id='%s', CC_Code='%s', CC_Description='%s', Cur_Code='%s', CC_Parent_Code='%s', CC_Reg_Exp='%s', CC_Reference='%s')>" % \
                ( self.CC_Id, self.CC_Code, self.CC_Description, self.Cur_Code, self.CC_Parent_Code, self.CC_Reg_Exp, self.CC_Reference)

# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2021-04-16 13:26:00
# =============================================================================

# gen_model_flask.py:670 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/models/flask_cost_centers.py
def get_cost_centers(table_name_suffix):
  # gen_model_flask.py:678 =>/home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/models/flask_cost_centers.py
  class cost_centers_Class(db.Model,Serializer):
    __tablename__ = 'Cost_Centers_%s'%(table_name_suffix)

    def set_shard(suffix=None):
        if suffix is not None:
           name='Cost_Centers_{suffix}'.format(suffix=suffix)
           __class__.__tablename__  = name
           __class__.__table__.name = name
        return __class__.__tablename__

    CC_Id          = db.Column( db.Integer, primary_key=True, autoincrement=True )
    CC_Code        = db.Column( db.String(45) )
    CC_Description = db.Column( db.String(255) )
    Cur_Code       = db.Column( db.String(3) )
    CC_Parent_Code = db.Column( db.String(45), default='1' )
    CC_Reg_Exp     = db.Column( db.String(45) )
    CC_Reference   = db.Column( db.String(245) )


    def __init__(self, CC_Id=0, CC_Code='None', CC_Description='None', Cur_Code='None', CC_Parent_Code='1', CC_Reg_Exp='None', CC_Reference='None'):
        self.CC_Id          = CC_Id
        self.CC_Code        = CC_Code
        self.CC_Description = CC_Description
        self.Cur_Code       = Cur_Code
        self.CC_Parent_Code = CC_Parent_Code
        self.CC_Reg_Exp     = CC_Reg_Exp
        self.CC_Reference   = CC_Reference

    def __repr__(self):
        return "<Cost_Centers( CC_Id='%s', CC_Code='%s', CC_Description='%s', Cur_Code='%s', CC_Parent_Code='%s', CC_Reg_Exp='%s', CC_Reference='%s')>" % \
                ( self.CC_Id, self.CC_Code, self.CC_Description, self.Cur_Code, self.CC_Parent_Code, self.CC_Reg_Exp, self.CC_Reference)

  cost_centers_Class.__name__ = 'cost_centers_%s'%(table_name_suffix)
  return cost_centers_Class
  # gen_model_flask.py 801 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/models/flask_cost_centers.py
# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2021-04-16 13:26:00
# =============================================================================

# gen_model_flask.py:115 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/models/flask_disk_images.py
class disk_images(db.Model,Serializer):
    __tablename__ = 'Disk_Images'

    def set_shard(suffix=None):
       if suffix is not None:
           name='Disk_Images_{suffix}'.format(suffix=suffix)
           __class__.__tablename__  = name
           __class__.__table__.name = name
       return __class__.__tablename__

    uuid             = db.Column( db.String(45), primary_key=True )
    name             = db.Column( db.String(45) )
    annotation       = db.Column( db.String(45) )
    image_type       = db.Column( db.String(45) )
    image_state      = db.Column( db.String(45) )
    vm_disk_size     = db.Column( db.BigInteger, default=0 )
    vm_disk_size_mib = db.Column( db.Integer, default=0 )
    vm_disk_size_gib = db.Column( db.Integer, default=0 )
    cluster          = db.Column( db.String(45) )


    # looking for include file: /home/gvalera/GIT/EG-Suite-Tools/Butler/code/src/include/models/flask_disk_images_properties.py
    # file: /home/gvalera/GIT/EG-Suite-Tools/Butler/code/src/include/models/flask_disk_images_properties.py not found
    def __init__(self, uuid='None', name='None', annotation='None', image_type='None', image_state='None', vm_disk_size=0, vm_disk_size_mib=0, vm_disk_size_gib=0, cluster='None'):
        self.uuid             = uuid
        self.name             = name
        self.annotation       = annotation
        self.image_type       = image_type
        self.image_state      = image_state
        self.vm_disk_size     = vm_disk_size
        self.vm_disk_size_mib = vm_disk_size_mib
        self.vm_disk_size_gib = vm_disk_size_gib
        self.cluster          = cluster

    def __repr__(self):
        return "<Disk_Images( uuid='%s', name='%s', annotation='%s', image_type='%s', image_state='%s', vm_disk_size='%s', vm_disk_size_mib='%s', vm_disk_size_gib='%s', cluster='%s')>" % \
                ( self.uuid, self.name, self.annotation, self.image_type, self.image_state, self.vm_disk_size, self.vm_disk_size_mib, self.vm_disk_size_gib, self.cluster)

# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2021-04-16 13:26:00
# =============================================================================

# gen_model_flask.py:115 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/models/flask_domains.py
class domains(db.Model,Serializer):
    __tablename__ = 'Domains'

    def set_shard(suffix=None):
       if suffix is not None:
           name='Domains_{suffix}'.format(suffix=suffix)
           __class__.__tablename__  = name
           __class__.__table__.name = name
       return __class__.__tablename__

    Domain_Id = db.Column( db.Integer, primary_key=True )
    Name      = db.Column( db.String(45) )
    Comments  = db.Column( db.Text )


    # looking for include file: /home/gvalera/GIT/EG-Suite-Tools/Butler/code/src/include/models/flask_domains_properties.py
    # file: /home/gvalera/GIT/EG-Suite-Tools/Butler/code/src/include/models/flask_domains_properties.py not found
    def __init__(self, Domain_Id=None, Name='None', Comments=None):
        self.Domain_Id = Domain_Id
        self.Name      = Name
        self.Comments  = Comments

    def __repr__(self):
        return "<Domains( Domain_Id='%s', Name='%s', Comments='%s')>" % \
                ( self.Domain_Id, self.Name, self.Comments)

# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2021-04-16 13:26:00
# =============================================================================

# gen_model_flask.py:115 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/models/flask_interface.py
class interface(db.Model,Serializer):
    __tablename__ = 'Interface'

    def set_shard(suffix=None):
       if suffix is not None:
           name='Interface_{suffix}'.format(suffix=suffix)
           __class__.__tablename__  = name
           __class__.__table__.name = name
       return __class__.__tablename__

    Id          = db.Column( db.Integer, primary_key=True, autoincrement=True )
    User_Id     = db.Column( db.Integer )
    Table_name  = db.Column( db.String(45) )
    Option_Type = db.Column( db.Integer )
    Argument_1  = db.Column( db.String(256) )
    Argument_2  = db.Column( db.String(256) )
    Argument_3  = db.Column( db.String(256) )
    Is_Active   = db.Column( db.Boolean )


    # looking for include file: /home/gvalera/GIT/EG-Suite-Tools/Butler/code/src/include/models/flask_interface_properties.py
    # file: /home/gvalera/GIT/EG-Suite-Tools/Butler/code/src/include/models/flask_interface_properties.py not found
    def __init__(self, Id=0, User_Id=None, Table_name='None', Option_Type=None, Argument_1='None', Argument_2='None', Argument_3='None', Is_Active=None):
        self.Id          = Id
        self.User_Id     = User_Id
        self.Table_name  = Table_name
        self.Option_Type = Option_Type
        self.Argument_1  = Argument_1
        self.Argument_2  = Argument_2
        self.Argument_3  = Argument_3
        self.Is_Active   = Is_Active

    def __repr__(self):
        return "<Interface( Id='%s', User_Id='%s', Table_name='%s', Option_Type='%s', Argument_1='%s', Argument_2='%s', Argument_3='%s', Is_Active='%s')>" % \
                ( self.Id, self.User_Id, self.Table_name, self.Option_Type, self.Argument_1, self.Argument_2, self.Argument_3, self.Is_Active)

# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2021-04-16 13:26:00
# =============================================================================

# gen_model_flask.py:115 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/models/flask_nutanix_prism_vm.py
class nutanix_prism_vm(db.Model,Serializer):
    __tablename__ = 'Nutanix_Prism_VM'

    def set_shard(suffix=None):
       if suffix is not None:
           name='Nutanix_Prism_VM_{suffix}'.format(suffix=suffix)
           __class__.__tablename__  = name
           __class__.__table__.name = name
       return __class__.__tablename__

    Request_Id       = db.Column( db.Integer, db.ForeignKey('Requests.Id'), primary_key=True )
    project_uuid     = db.Column( db.String(45), db.ForeignKey('Projects.project_uuid') )
    category_name    = db.Column( db.String(45), db.ForeignKey('Categories.category_name') )
    cluster_uuid     = db.Column( db.String(45), db.ForeignKey('Clusters.cluster_uuid') )
    vm_name          = db.Column( db.String(45) )
    power_state      = db.Column( db.Boolean, default=1 )
    vcpus_per_socket = db.Column( db.Integer, default=1 )
    num_sockets      = db.Column( db.Integer, default=1 )
    memory_size_mib  = db.Column( db.Integer, default=0 )
    memory_size_gib  = db.Column( db.Integer, default=0 )
    Comments         = db.Column( db.Text )
    vm_uuid          = db.Column( db.String(45) )
    vm_ip            = db.Column( db.String(45) )
    subnet_uuid      = db.Column( db.String(45), db.ForeignKey('Subnets.uuid') )
    vm_username      = db.Column( db.String(45) )
    vm_password      = db.Column( db.String(45) )
    backup_set_1     = db.Column( db.Boolean, default=0 )
    backup_set_2     = db.Column( db.Boolean, default=0 )
    backup_set_3     = db.Column( db.Boolean, default=0 )
    disk_type        = db.Column( db.Integer, default=0 )
    disk_0_image     = db.Column( db.String(45) )
    disk_0_size      = db.Column( db.Integer, default=0 )
    disk_1_image     = db.Column( db.String(45) )
    disk_1_size      = db.Column( db.Integer, default=0 )
    disk_2_image     = db.Column( db.String(45) )
    disk_2_size      = db.Column( db.Integer, default=0 )
    disk_3_image     = db.Column( db.String(45) )
    disk_3_size      = db.Column( db.Integer, default=0 )
    disk_4_image     = db.Column( db.String(45) )
    disk_4_size      = db.Column( db.Integer, default=0 )
    disk_5_image     = db.Column( db.String(45) )
    disk_5_size      = db.Column( db.Integer, default=0 )
    disk_6_image     = db.Column( db.String(45) )
    disk_6_size      = db.Column( db.Integer, default=0 )
    disk_7_image     = db.Column( db.String(45) )
    disk_7_size      = db.Column( db.Integer, default=0 )
    disk_8_image     = db.Column( db.String(45) )
    disk_8_size      = db.Column( db.Integer, default=0 )
    disk_9_image     = db.Column( db.String(45) )
    disk_9_size      = db.Column( db.Integer, default=0 )
    disk_10_image    = db.Column( db.String(45) )
    disk_10_size     = db.Column( db.Integer, default=0 )
    disk_11_image    = db.Column( db.String(45) )
    disk_11_size     = db.Column( db.Integer, default=0 )
    vm_drp           = db.Column( db.Boolean, default=0 )
    vm_cdrom         = db.Column( db.Boolean, default=0 )
    drp_cluster_uuid = db.Column( db.String(45) )
    nic_0_vlan       = db.Column( db.String(45) )
    nic_0_ip         = db.Column( db.String(45) )
    nic_0_mac        = db.Column( db.String(45) )
    nic_1_vlan       = db.Column( db.String(45) )
    nic_1_ip         = db.Column( db.String(45) )
    nic_1_mac        = db.Column( db.String(45) )
    nic_2_vlan       = db.Column( db.String(45) )
    nic_2_ip         = db.Column( db.String(45) )
    nic_2_mac        = db.Column( db.String(45) )
    request_text     = db.Column( db.Text )


    # looking for include file: /home/gvalera/GIT/EG-Suite-Tools/Butler/code/src/include/models/flask_nutanix_prism_vm_properties.py
    # file: /home/gvalera/GIT/EG-Suite-Tools/Butler/code/src/include/models/flask_nutanix_prism_vm_properties.py not found
    def __init__(self, Request_Id=None, project_uuid='None', category_name='None', cluster_uuid='None', vm_name='None', power_state=1, vcpus_per_socket=1, num_sockets=1, memory_size_mib=0, memory_size_gib=0, Comments=None, vm_uuid='None', vm_ip='None', subnet_uuid='None', vm_username='None', vm_password='None', backup_set_1=0, backup_set_2=0, backup_set_3=0, disk_type=0, disk_0_image='None', disk_0_size=0, disk_1_image='None', disk_1_size=0, disk_2_image='None', disk_2_size=0, disk_3_image='None', disk_3_size=0, disk_4_image='None', disk_4_size=0, disk_5_image='None', disk_5_size=0, disk_6_image='None', disk_6_size=0, disk_7_image='None', disk_7_size=0, disk_8_image='None', disk_8_size=0, disk_9_image='None', disk_9_size=0, disk_10_image='None', disk_10_size=0, disk_11_image='None', disk_11_size=0, vm_drp=0, vm_cdrom=0, drp_cluster_uuid='None', nic_0_vlan='None', nic_0_ip='None', nic_0_mac='None', nic_1_vlan='None', nic_1_ip='None', nic_1_mac='None', nic_2_vlan='None', nic_2_ip='None', nic_2_mac='None', request_text=None):
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
        self.request_text     = request_text

    def __repr__(self):
        return "<Nutanix_Prism_VM( Request_Id='%s', project_uuid='%s', category_name='%s', cluster_uuid='%s', vm_name='%s', power_state='%s', vcpus_per_socket='%s', num_sockets='%s', memory_size_mib='%s', memory_size_gib='%s', Comments='%s', vm_uuid='%s', vm_ip='%s', subnet_uuid='%s', vm_username='%s', vm_password='%s', backup_set_1='%s', backup_set_2='%s', backup_set_3='%s', disk_type='%s', disk_0_image='%s', disk_0_size='%s', disk_1_image='%s', disk_1_size='%s', disk_2_image='%s', disk_2_size='%s', disk_3_image='%s', disk_3_size='%s', disk_4_image='%s', disk_4_size='%s', disk_5_image='%s', disk_5_size='%s', disk_6_image='%s', disk_6_size='%s', disk_7_image='%s', disk_7_size='%s', disk_8_image='%s', disk_8_size='%s', disk_9_image='%s', disk_9_size='%s', disk_10_image='%s', disk_10_size='%s', disk_11_image='%s', disk_11_size='%s', vm_drp='%s', vm_cdrom='%s', drp_cluster_uuid='%s', nic_0_vlan='%s', nic_0_ip='%s', nic_0_mac='%s', nic_1_vlan='%s', nic_1_ip='%s', nic_1_mac='%s', nic_2_vlan='%s', nic_2_ip='%s', nic_2_mac='%s', request_text='%s')>" % \
                ( self.Request_Id, self.project_uuid, self.category_name, self.cluster_uuid, self.vm_name, self.power_state, self.vcpus_per_socket, self.num_sockets, self.memory_size_mib, self.memory_size_gib, self.Comments, self.vm_uuid, self.vm_ip, self.subnet_uuid, self.vm_username, self.vm_password, self.backup_set_1, self.backup_set_2, self.backup_set_3, self.disk_type, self.disk_0_image, self.disk_0_size, self.disk_1_image, self.disk_1_size, self.disk_2_image, self.disk_2_size, self.disk_3_image, self.disk_3_size, self.disk_4_image, self.disk_4_size, self.disk_5_image, self.disk_5_size, self.disk_6_image, self.disk_6_size, self.disk_7_image, self.disk_7_size, self.disk_8_image, self.disk_8_size, self.disk_9_image, self.disk_9_size, self.disk_10_image, self.disk_10_size, self.disk_11_image, self.disk_11_size, self.vm_drp, self.vm_cdrom, self.drp_cluster_uuid, self.nic_0_vlan, self.nic_0_ip, self.nic_0_mac, self.nic_1_vlan, self.nic_1_ip, self.nic_1_mac, self.nic_2_vlan, self.nic_2_ip, self.nic_2_mac, self.request_text)

# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2021-04-16 13:26:00
# =============================================================================

# gen_model_flask.py:115 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/models/flask_nutanix_vm_images.py
class nutanix_vm_images(db.Model,Serializer):
    __tablename__ = 'Nutanix_VM_Images'

    def set_shard(suffix=None):
       if suffix is not None:
           name='Nutanix_VM_Images_{suffix}'.format(suffix=suffix)
           __class__.__tablename__  = name
           __class__.__table__.name = name
       return __class__.__tablename__

    imageservice_uuid_diskclone = db.Column( db.String(45), primary_key=True )
    description                 = db.Column( db.String(45) )
    size_mib                    = db.Column( db.String(45) )
    comments                    = db.Column( db.String(45) )


    # looking for include file: /home/gvalera/GIT/EG-Suite-Tools/Butler/code/src/include/models/flask_nutanix_vm_images_properties.py
    # file: /home/gvalera/GIT/EG-Suite-Tools/Butler/code/src/include/models/flask_nutanix_vm_images_properties.py not found
    def __init__(self, imageservice_uuid_diskclone='None', description='None', size_mib='None', comments='None'):
        self.imageservice_uuid_diskclone = imageservice_uuid_diskclone
        self.description                 = description
        self.size_mib                    = size_mib
        self.comments                    = comments

    def __repr__(self):
        return "<Nutanix_VM_Images( imageservice_uuid_diskclone='%s', description='%s', size_mib='%s', comments='%s')>" % \
                ( self.imageservice_uuid_diskclone, self.description, self.size_mib, self.comments)

# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2021-04-16 13:26:00
# =============================================================================

# gen_model_flask.py:115 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/models/flask_projects.py
class projects(db.Model,Serializer):
    __tablename__ = 'Projects'

    def set_shard(suffix=None):
       if suffix is not None:
           name='Projects_{suffix}'.format(suffix=suffix)
           __class__.__tablename__  = name
           __class__.__table__.name = name
       return __class__.__tablename__

    project_uuid    = db.Column( db.String(45), primary_key=True )
    project_name    = db.Column( db.String(45) )
    project_subnets = db.Column( db.String(255) )

    # child_table=None gen_children=True
    nutanix_prism_vm = db.relationship('nutanix_prism_vm',backref='projects',lazy='dynamic')

    # looking for include file: /home/gvalera/GIT/EG-Suite-Tools/Butler/code/src/include/models/flask_projects_properties.py
    # file: /home/gvalera/GIT/EG-Suite-Tools/Butler/code/src/include/models/flask_projects_properties.py not found
    def __init__(self, project_uuid='None', project_name='None', project_subnets='None'):
        self.project_uuid    = project_uuid
        self.project_name    = project_name
        self.project_subnets = project_subnets

    def __repr__(self):
        return "<Projects( project_uuid='%s', project_name='%s', project_subnets='%s')>" % \
                ( self.project_uuid, self.project_name, self.project_subnets)

# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2021-04-16 13:26:00
# =============================================================================

# gen_model_flask.py:115 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/models/flask_rates.py
class rates(db.Model,Serializer):
    __tablename__ = 'Rates'

    def set_shard(suffix=None):
       if suffix is not None:
           name='Rates_{suffix}'.format(suffix=suffix)
           __class__.__tablename__  = name
           __class__.__table__.name = name
       return __class__.__tablename__

    Rat_Id     = db.Column( db.Integer, primary_key=True, autoincrement=True )
    Typ_Code   = db.Column( db.String(10) )
    Cus_Id     = db.Column( db.Integer )
    Pla_Id     = db.Column( db.Integer )
    CC_Id      = db.Column( db.Integer )
    CI_Id      = db.Column( db.Integer )
    Rat_Price  = db.Column( db.Numeric(20,12) )
    Cur_Code   = db.Column( db.String(3) )
    MU_Code    = db.Column( db.String(3) )
    Rat_Period = db.Column( db.Integer )
    Rat_Type   = db.Column( db.Integer )


    # looking for include file: /home/gvalera/GIT/EG-Suite-Tools/Butler/code/src/include/models/flask_rates_properties.py
    # including file: /home/gvalera/GIT/EG-Suite-Tools/Butler/code/src/include/models/flask_rates_properties.py
    # @property
    #
    
    def __init__(self, Rat_Id=0, Typ_Code='None', Cus_Id=None, Pla_Id=None, CC_Id=None, CI_Id=None, Rat_Price=None, Cur_Code='None', MU_Code='None', Rat_Period=None, Rat_Type=None):
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

    def __repr__(self):
        return "<Rates( Rat_Id='%s', Typ_Code='%s', Cus_Id='%s', Pla_Id='%s', CC_Id='%s', CI_Id='%s', Rat_Price='%s', Cur_Code='%s', MU_Code='%s', Rat_Period='%s', Rat_Type='%s')>" % \
                ( self.Rat_Id, self.Typ_Code, self.Cus_Id, self.Pla_Id, self.CC_Id, self.CI_Id, self.Rat_Price, self.Cur_Code, self.MU_Code, self.Rat_Period, self.Rat_Type)

    # method
    def method(self):
        pass
# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2021-04-16 13:26:00
# =============================================================================

# gen_model_flask.py:670 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/models/flask_rates.py
def get_rates(table_name_suffix):
  # gen_model_flask.py:678 =>/home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/models/flask_rates.py
  class rates_Class(db.Model,Serializer):
    __tablename__ = 'Rates_%s'%(table_name_suffix)

    def set_shard(suffix=None):
        if suffix is not None:
           name='Rates_{suffix}'.format(suffix=suffix)
           __class__.__tablename__  = name
           __class__.__table__.name = name
        return __class__.__tablename__

    Rat_Id     = db.Column( db.Integer, primary_key=True, autoincrement=True )
    Typ_Code   = db.Column( db.String(10) )
    Cus_Id     = db.Column( db.Integer )
    Pla_Id     = db.Column( db.Integer )
    CC_Id      = db.Column( db.Integer )
    CI_Id      = db.Column( db.Integer )
    Rat_Price  = db.Column( db.Numeric(20,12) )
    Cur_Code   = db.Column( db.String(3) )
    MU_Code    = db.Column( db.String(3) )
    Rat_Period = db.Column( db.Integer )
    Rat_Type   = db.Column( db.Integer )


    # @property
    #
    
    def __init__(self, Rat_Id=0, Typ_Code='None', Cus_Id=None, Pla_Id=None, CC_Id=None, CI_Id=None, Rat_Price=None, Cur_Code='None', MU_Code='None', Rat_Period=None, Rat_Type=None):
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

    def __repr__(self):
        return "<Rates( Rat_Id='%s', Typ_Code='%s', Cus_Id='%s', Pla_Id='%s', CC_Id='%s', CI_Id='%s', Rat_Price='%s', Cur_Code='%s', MU_Code='%s', Rat_Period='%s', Rat_Type='%s')>" % \
                ( self.Rat_Id, self.Typ_Code, self.Cus_Id, self.Pla_Id, self.CC_Id, self.CI_Id, self.Rat_Price, self.Cur_Code, self.MU_Code, self.Rat_Period, self.Rat_Type)

    # method
    def method(self):
        pass
  rates_Class.__name__ = 'rates_%s'%(table_name_suffix)
  return rates_Class
  # gen_model_flask.py 801 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/models/flask_rates.py
# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2021-04-16 13:26:00
# =============================================================================

# gen_model_flask.py:115 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/models/flask_requests.py
class requests(db.Model,Serializer):
    __tablename__ = 'Requests'

    def set_shard(suffix=None):
       if suffix is not None:
           name='Requests_{suffix}'.format(suffix=suffix)
           __class__.__tablename__  = name
           __class__.__table__.name = name
       return __class__.__tablename__

    Id               = db.Column( db.Integer, primary_key=True, autoincrement=True )
    Type             = db.Column( db.Integer, db.ForeignKey('Request_Type.Id'), default=1 )
    User_Id          = db.Column( db.Integer )
    Approver_Id      = db.Column( db.Integer )
    Status           = db.Column( db.Integer, default=0 )
    Creation_Time    = db.Column( db.DateTime )
    Last_Status_Time = db.Column( db.DateTime )
    Comments         = db.Column( db.Text )
    Task_uuid        = db.Column( db.String(45) )
    Task_status      = db.Column( db.Integer )
    CC_Id            = db.Column( db.Integer )
    uuid             = db.Column( db.String(45) )
    User_Comments    = db.Column( db.Text )

    # child_table=None gen_children=True
    nutanix_prism_vm = db.relationship('nutanix_prism_vm',backref='requests',lazy='dynamic')

    # looking for include file: /home/gvalera/GIT/EG-Suite-Tools/Butler/code/src/include/models/flask_requests_properties.py
    # file: /home/gvalera/GIT/EG-Suite-Tools/Butler/code/src/include/models/flask_requests_properties.py not found
    def __init__(self, Id=0, Type=1, User_Id=None, Approver_Id=None, Status=0, Creation_Time=None, Last_Status_Time=None, Comments=None, Task_uuid='None', Task_status=None, CC_Id=None, uuid='None', User_Comments=None):
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

    def __repr__(self):
        return "<Requests( Id='%s', Type='%s', User_Id='%s', Approver_Id='%s', Status='%s', Creation_Time='%s', Last_Status_Time='%s', Comments='%s', Task_uuid='%s', Task_status='%s', CC_Id='%s', uuid='%s', User_Comments='%s')>" % \
                ( self.Id, self.Type, self.User_Id, self.Approver_Id, self.Status, self.Creation_Time, self.Last_Status_Time, self.Comments, self.Task_uuid, self.Task_status, self.CC_Id, self.uuid, self.User_Comments)

# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2021-04-16 13:26:00
# =============================================================================

# gen_model_flask.py:115 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/models/flask_request_type.py
class request_type(db.Model,Serializer):
    __tablename__ = 'Request_Type'

    def set_shard(suffix=None):
       if suffix is not None:
           name='Request_Type_{suffix}'.format(suffix=suffix)
           __class__.__tablename__  = name
           __class__.__table__.name = name
       return __class__.__tablename__

    Id          = db.Column( db.Integer, primary_key=True )
    Description = db.Column( db.String(45) )
    Table_Name  = db.Column( db.String(45) )

    # child_table=None gen_children=True
    requests    = db.relationship('requests',backref='request_type',lazy='dynamic')

    # looking for include file: /home/gvalera/GIT/EG-Suite-Tools/Butler/code/src/include/models/flask_request_type_properties.py
    # file: /home/gvalera/GIT/EG-Suite-Tools/Butler/code/src/include/models/flask_request_type_properties.py not found
    def __init__(self, Id=None, Description='None', Table_Name='None'):
        self.Id          = Id
        self.Description = Description
        self.Table_Name  = Table_Name

    def __repr__(self):
        return "<Request_Type( Id='%s', Description='%s', Table_Name='%s')>" % \
                ( self.Id, self.Description, self.Table_Name)

# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2021-04-16 13:26:00
# =============================================================================

# gen_model_flask.py:115 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/models/flask_roles.py
class Role(db.Model,Serializer):
    __tablename__ = 'Roles'

    def set_shard(suffix=None):
       if suffix is not None:
           name='Roles_{suffix}'.format(suffix=suffix)
           __class__.__tablename__  = name
           __class__.__table__.name = name
       return __class__.__tablename__

    id          = db.Column( db.Integer, primary_key=True )
    name        = db.Column( db.String(64) )
    default     = db.Column( db.Boolean )
    permissions = db.Column( db.Integer )

    # child_table=None gen_children=True
    users       = db.relationship('User',backref='role',lazy='dynamic')

    # looking for include file: /home/gvalera/GIT/EG-Suite-Tools/Butler/code/src/include/models/flask_roles_properties.py
    # file: /home/gvalera/GIT/EG-Suite-Tools/Butler/code/src/include/models/flask_roles_properties.py not found
    @staticmethod
    def insert_roles():
        roles = {
            'Customer': (   Permission.CUSTOMER, False),
            'Reporter': (   Permission.VIEW |
                            Permission.REPORT |
                            Permission.EXPORT, True),
            'Charger': (    Permission.VIEW |
                            Permission.DELETE |
                            Permission.MODIFY |
                            Permission.REPORT, False),
            'Administrator':    (0xfe, False),                      # Administrator does not have 'Customer' permisions
            'Auditor':          (0x1fe, False),                      # Auditor does not have 'Customer' permissions
            'God':              (0xfff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()
    """
    def __repr__(self):
        return '<Role %r>' % self.name
    """
# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2021-04-16 13:26:00
# =============================================================================

# gen_model_flask.py:115 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/models/flask_subnets.py
class subnets(db.Model,Serializer):
    __tablename__ = 'Subnets'

    def set_shard(suffix=None):
       if suffix is not None:
           name='Subnets_{suffix}'.format(suffix=suffix)
           __class__.__tablename__  = name
           __class__.__table__.name = name
       return __class__.__tablename__

    uuid               = db.Column( db.String(45), primary_key=True )
    name               = db.Column( db.String(45) )
    vlan_id            = db.Column( db.Integer )
    vswitch_name       = db.Column( db.String(45) )
    type               = db.Column( db.String(45) )
    default_gateway_ip = db.Column( db.String(45) )
    range              = db.Column( db.String(45) )
    prefix_length      = db.Column( db.Integer )
    subnet_ip          = db.Column( db.String(45) )
    cluster            = db.Column( db.String(45) )

    # child_table=None gen_children=True
    nutanix_prism_vm   = db.relationship('nutanix_prism_vm',backref='subnets',lazy='dynamic')

    # looking for include file: /home/gvalera/GIT/EG-Suite-Tools/Butler/code/src/include/models/flask_subnets_properties.py
    # file: /home/gvalera/GIT/EG-Suite-Tools/Butler/code/src/include/models/flask_subnets_properties.py not found
    def __init__(self, uuid='None', name='None', vlan_id=None, vswitch_name='None', type='None', default_gateway_ip='None', range='None', prefix_length=None, subnet_ip='None', cluster='None'):
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

    def __repr__(self):
        return "<Subnets( uuid='%s', name='%s', vlan_id='%s', vswitch_name='%s', type='%s', default_gateway_ip='%s', range='%s', prefix_length='%s', subnet_ip='%s', cluster='%s')>" % \
                ( self.uuid, self.name, self.vlan_id, self.vswitch_name, self.type, self.default_gateway_ip, self.range, self.prefix_length, self.subnet_ip, self.cluster)

# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2021-04-16 13:26:00
# =============================================================================

# gen_model_flask.py:115 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/models/flask_users.py
class User(UserMixin, db.Model,Serializer):
    __tablename__ = 'Users'

    def set_shard(suffix=None):
       if suffix is not None:
           name='Users_{suffix}'.format(suffix=suffix)
           __class__.__tablename__  = name
           __class__.__table__.name = name
       return __class__.__tablename__

    id            = db.Column( db.Integer, primary_key=True, autoincrement=True )
    username      = db.Column( db.String(64) )
    role_id       = db.Column( db.Integer, db.ForeignKey('Roles.id') )
    email         = db.Column( db.String(64) )
    password_hash = db.Column( db.String(128) )
    confirmed     = db.Column( db.Boolean, default=0 )
    CC_Id         = db.Column( db.Integer, default=1 )


    # looking for include file: /home/gvalera/GIT/EG-Suite-Tools/Butler/code/src/include/models/flask_users_properties.py
    # file: /home/gvalera/GIT/EG-Suite-Tools/Butler/code/src/include/models/flask_users_properties.py not found
    # source: code/src/include/models/flask_users_methods.py
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.username == current_app.config['BUTLER_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xfe).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()


    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        return True

    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.id, 'new_email': new_email})

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        db.session.add(self)
        return True

    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def is_god(self):
        return self.can(Permission.GOD)

    def is_customer(self):
        return self.can(Permission.CUSTOMER)

    def __repr__(self):
        if hasattr(self,'role'):
            return '<User %r role=%r>' % (self.username,self.role)
        else:
            return '<User %r role=UNDEFINED>' % (self.username)

    # ================================================================== 
    # User Model footer file
    # Defines standard methods for User Classs
    # source file name: models_py_User_footer.py
    # Static Header File. 
    # GLVH 2019-08-16
    # GLVH 2020-10-11 EG Suite - EG Butler version setup
    # ------------------------------------------------------------------
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        return True

    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.id, 'new_email': new_email})

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        db.session.add(self)
        return True

    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def is_god(self):
        return self.can(Permission.GOD)

    def is_customer(self):
        return self.can(Permission.CUSTOMER)

    def __repr__(self):
        return '<User %r role=%r id=%r>' % (self.username,self.role,self.id)
    # ------------------------------------------------------------------
