# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2021-11-24 17:14:00
# =============================================================================

# gen_model_flask.py:67 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/models/ORM_model_schema.py
from sqlalchemy                 import Table, Column, MetaData, ForeignKey
from sqlalchemy                 import Integer, String, Date, Time, Numeric, DateTime, Boolean
from sqlalchemy                 import Text,VARBINARY
from emtec                      import *

Meta = MetaData()

def Create_Tables(engine):
    try:
        Categories = Table(
                'Categories',Meta,
                Column( 'category_name',String(45), primary_key=True ),
                Column( 'category_description',String(45) ),
        )
    except Exception as e:
        print('EXCEPTION:',e)
    try:
        Clusters = Table(
                'Clusters',Meta,
                Column( 'cluster_uuid',String(45), primary_key=True ),
                Column( 'cluster_name',String(45) ),
                Column( 'cluster_username',String(45) ),
                Column( 'cluster_password',String(45) ),
                Column( 'cluster_ip',String(45) ),
        )
    except Exception as e:
        print('EXCEPTION:',e)
    try:
        Cost_Centers = Table(
                'Cost_Centers',Meta,
                Column( 'CC_Id',Integer, primary_key=True, autoincrement=True ),
                Column( 'CC_Code',String(45) ),
                Column( 'CC_Description',String(255) ),
                Column( 'Cur_Code',String(3) ),
                Column( 'CC_Parent_Code',String(45) ),
                Column( 'CC_Reg_Exp',String(45) ),
                Column( 'CC_Reference',String(245) ),
        )
    except Exception as e:
        print('EXCEPTION:',e)
    try:
        Disk_Images = Table(
                'Disk_Images',Meta,
                Column( 'uuid',String(45), primary_key=True ),
                Column( 'name',String(45) ),
                Column( 'annotation',String(45) ),
                Column( 'image_type',String(45) ),
                Column( 'image_state',String(45) ),
                Column( 'vm_disk_size',BigInteger ),
                Column( 'vm_disk_size_mib',Integer ),
                Column( 'vm_disk_size_gib',Integer ),
                Column( 'cluster',String(45) ),
        )
    except Exception as e:
        print('EXCEPTION:',e)
    try:
        Domains = Table(
                'Domains',Meta,
                Column( 'Domain_Id',Integer, primary_key=True ),
                Column( 'Name',String(45) ),
                Column( 'Comments',Text ),
        )
    except Exception as e:
        print('EXCEPTION:',e)
    try:
        Interface = Table(
                'Interface',Meta,
                Column( 'Id',Integer, primary_key=True, autoincrement=True ),
                Column( 'User_Id',Integer ),
                Column( 'Table_name',String(45) ),
                Column( 'Option_Type',Integer ),
                Column( 'Argument_1',String(256) ),
                Column( 'Argument_2',String(256) ),
                Column( 'Argument_3',String(256) ),
                Column( 'Is_Active',Boolean ),
        )
    except Exception as e:
        print('EXCEPTION:',e)
    try:
        Nutanix_Prism_VM = Table(
                'Nutanix_Prism_VM',Meta,
                Column( 'Request_Id',Integer, ForeignKey('Requests.Id'), primary_key=True ),
                Column( 'project_uuid',String(45), ForeignKey('Projects.project_uuid') ),
                Column( 'category_name',String(45), ForeignKey('Categories.category_name') ),
                Column( 'cluster_uuid',String(45), ForeignKey('Clusters.cluster_uuid') ),
                Column( 'vm_name',String(45) ),
                Column( 'power_state',Boolean ),
                Column( 'vcpus_per_socket',Integer ),
                Column( 'num_sockets',Integer ),
                Column( 'memory_size_mib',Integer ),
                Column( 'memory_size_gib',Integer ),
                Column( 'Comments',Text ),
                Column( 'vm_uuid',String(45) ),
                Column( 'vm_ip',String(45) ),
                Column( 'subnet_uuid',String(45), ForeignKey('Subnets.uuid') ),
                Column( 'vm_username',String(45) ),
                Column( 'vm_password',String(45) ),
                Column( 'backup_set_1',Boolean ),
                Column( 'backup_set_2',Boolean ),
                Column( 'backup_set_3',Boolean ),
                Column( 'disk_type',Integer ),
                Column( 'disk_0_image',String(45) ),
                Column( 'disk_0_size',Integer ),
                Column( 'disk_1_image',String(45) ),
                Column( 'disk_1_size',Integer ),
                Column( 'disk_2_image',String(45) ),
                Column( 'disk_2_size',Integer ),
                Column( 'disk_3_image',String(45) ),
                Column( 'disk_3_size',Integer ),
                Column( 'disk_4_image',String(45) ),
                Column( 'disk_4_size',Integer ),
                Column( 'disk_5_image',String(45) ),
                Column( 'disk_5_size',Integer ),
                Column( 'disk_6_image',String(45) ),
                Column( 'disk_6_size',Integer ),
                Column( 'disk_7_image',String(45) ),
                Column( 'disk_7_size',Integer ),
                Column( 'disk_8_image',String(45) ),
                Column( 'disk_8_size',Integer ),
                Column( 'disk_9_image',String(45) ),
                Column( 'disk_9_size',Integer ),
                Column( 'disk_10_image',String(45) ),
                Column( 'disk_10_size',Integer ),
                Column( 'disk_11_image',String(45) ),
                Column( 'disk_11_size',Integer ),
                Column( 'vm_drp',Boolean ),
                Column( 'vm_drp_remote',Boolean ),
                Column( 'vm_cdrom',Boolean ),
                Column( 'drp_cluster_uuid',String(45) ),
                Column( 'nic_0_vlan',String(45) ),
                Column( 'nic_0_ip',String(45) ),
                Column( 'nic_0_mac',String(45) ),
                Column( 'nic_1_vlan',String(45) ),
                Column( 'nic_1_ip',String(45) ),
                Column( 'nic_1_mac',String(45) ),
                Column( 'nic_2_vlan',String(45) ),
                Column( 'nic_2_ip',String(45) ),
                Column( 'nic_2_mac',String(45) ),
                Column( 'nic_3_vlan',String(45) ),
                Column( 'nic_3_ip',String(45) ),
                Column( 'nic_3_mac',String(45) ),
                Column( 'request_text',Text ),
        )
    except Exception as e:
        print('EXCEPTION:',e)
    try:
        Nutanix_VM_Images = Table(
                'Nutanix_VM_Images',Meta,
                Column( 'imageservice_uuid_diskclone',String(45), primary_key=True ),
                Column( 'description',String(45) ),
                Column( 'size_mib',String(45) ),
                Column( 'comments',String(45) ),
        )
    except Exception as e:
        print('EXCEPTION:',e)
    try:
        Projects = Table(
                'Projects',Meta,
                Column( 'project_uuid',String(45), primary_key=True ),
                Column( 'project_name',String(45) ),
                Column( 'project_subnets',String(255) ),
        )
    except Exception as e:
        print('EXCEPTION:',e)
    try:
        Rates = Table(
                'Rates',Meta,
                Column( 'Rat_Id',Integer, primary_key=True, autoincrement=True ),
                Column( 'Typ_Code',String(10) ),
                Column( 'Cus_Id',Integer ),
                Column( 'Pla_Id',Integer ),
                Column( 'CC_Id',Integer ),
                Column( 'CI_Id',Integer ),
                Column( 'Rat_Price',Numeric(20,12) ),
                Column( 'Cur_Code',String(3) ),
                Column( 'MU_Code',String(3) ),
                Column( 'Rat_Period',Integer ),
                Column( 'Rat_Type',Integer ),
        )
    except Exception as e:
        print('EXCEPTION:',e)
    try:
        Request_Type = Table(
                'Request_Type',Meta,
                Column( 'Id',Integer, primary_key=True ),
                Column( 'Description',String(45) ),
                Column( 'Table_Name',String(45) ),
        )
    except Exception as e:
        print('EXCEPTION:',e)
    try:
        Requests = Table(
                'Requests',Meta,
                Column( 'Id',Integer, primary_key=True, autoincrement=True ),
                Column( 'Type',Integer, ForeignKey('Request_Type.Id') ),
                Column( 'User_Id',Integer ),
                Column( 'Approver_Id',Integer ),
                Column( 'Status',Integer ),
                Column( 'Creation_Time',DateTime ),
                Column( 'Last_Status_Time',DateTime ),
                Column( 'Comments',Text ),
                Column( 'Task_uuid',String(45) ),
                Column( 'Task_status',Integer ),
                Column( 'CC_Id',Integer ),
                Column( 'uuid',String(45) ),
                Column( 'User_Comments',Text ),
        )
    except Exception as e:
        print('EXCEPTION:',e)
    try:
        Roles = Table(
                'Roles',Meta,
                Column( 'id',Integer, primary_key=True ),
                Column( 'name',String(64) ),
                Column( 'default',Boolean ),
                Column( 'permissions',Integer ),
        )
    except Exception as e:
        print('EXCEPTION:',e)
    try:
        Subnets = Table(
                'Subnets',Meta,
                Column( 'uuid',String(45), primary_key=True ),
                Column( 'name',String(45) ),
                Column( 'vlan_id',Integer ),
                Column( 'vswitch_name',String(45) ),
                Column( 'type',String(45) ),
                Column( 'default_gateway_ip',String(45) ),
                Column( 'range',String(45) ),
                Column( 'prefix_length',Integer ),
                Column( 'subnet_ip',String(45) ),
                Column( 'cluster',String(45) ),
        )
    except Exception as e:
        print('EXCEPTION:',e)
    try:
        Users = Table(
                'Users',Meta,
                Column( 'id',Integer, primary_key=True, autoincrement=True ),
                Column( 'username',String(64) ),
                Column( 'role_id',Integer, ForeignKey('Roles.id') ),
                Column( 'email',String(64) ),
                Column( 'password_hash',String(128) ),
                Column( 'confirmed',Boolean ),
                Column( 'CC_Id',Integer ),
        )
    except Exception as e:
        print('EXCEPTION:',e)
    try:
        Meta.create_all(engine)
    except Exception as e:
        print("EXCEPTION: on Meta.create_all(engine=%s)"%engine,e,"!!!!")

# source: code/src/include/models/flask_users_methods.py
# Required for Load_Table Function
import  pandas      as      pandas
from    pathlib     import  Path
# imports orm_model as local definitions for DB popuplation
import  emtec.butler.orm_models   as      orm_model
       
def Load_Table(self,class_name,filename,separator=','):
    my_file = Path(filename)
    if my_file.is_file():
        # file exists
        # Gets type of recodr class by name
        table_class=getattr(orm_model,class_name)
        # reads data from CSV (separator can be specified to change format
        # if needed, no default NaN values will be used
        df=pandas.read_csv(filename,sep=separator,keep_default_na=False)
        # iterate over rows with iterrows()
        for index, row in df.iterrows():
            instance=table_class()
            # access data using column names
            for column in list(df.columns.values):
                value = None if pandas.isnull(row[column]) else row[column]
                setattr(instance, column, value)
                try:
                    self.session.add(instance)
                except Exception as e:
                    print("Load_table: Could not add instance of %s: %s %s"%(instance,class_name,e))
                    return False
        try:
            self.session.commit()
        except Exception as e:
            #print("Load_table: Could not commit session: %s %s"%(self.session,e))
            print("Load_table: Could not commit session: %s %s"%(self.session,'e'))
            self.session.rollback()
            return False
        return True
    else:
        return False

