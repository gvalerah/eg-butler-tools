# ----------------------------------------------------------------------
# code/src/forms_py_header.py
# Flask required modules
import os
from flask                  import current_app
from flask_wtf              import FlaskForm as Form
from wtforms                import Field
from wtforms                import StringField
# GV 20220224  Obsolete TextField will be replaced by StrigField
# GV System Wide 
# GV from wtforms           import TextField
from wtforms                import TextAreaField
from wtforms                import IntegerField
from wtforms                import DecimalField
from wtforms                import DateTimeField
from wtforms                import BooleanField
from wtforms                import SelectField
from wtforms                import SubmitField
from wtforms                import RadioField
from wtforms_components     import TimeField
#if wtforms.__version__ < "3.0.0":
#    from wtforms.fields.html5   import DateField
#else:
#    from wtforms.fields     import DateField
from wtforms.fields         import DateField
from wtforms.validators     import DataRequired as Required
from wtforms.validators     import AnyOf, DataRequired, Email
from wtforms.validators     import EqualTo, HostnameValidation
from wtforms.validators     import IPAddress, InputRequired, Length
from wtforms.validators     import MacAddress, NoneOf, NumberRange
from wtforms.validators     import Optional
from wtforms.validators     import Regexp
# ----------------------------------------------------------------------

# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2022-03-16 19:41:36
# =============================================================================

# gen_model_flask.py:289 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/forms/frm_categories.py
from decimal import ROUND_HALF_UP

class frm_categories(Form):
    category_name                = StringField("category_name?", validators=[DataRequired()])
    category_description         = StringField("category_description?")

    submit_Save                  = SubmitField  ('Save')
    submit_New                   = SubmitField  ('New')
    submit_Cancel                = SubmitField  ('Cancel')

    has_FKs                      = False

class frm_categories_delete(Form):
    submit_Delete                = SubmitField  ('Delete')
    submit_Cancel                = SubmitField  ('Cancel')

# =============================================================================
# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2022-03-16 19:41:36
# =============================================================================

# gen_model_flask.py:289 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/forms/frm_clusters.py
from decimal import ROUND_HALF_UP

class frm_clusters(Form):
    cluster_uuid             = StringField("cluster_uuid?", validators=[DataRequired()])
    cluster_name             = StringField("cluster_name?")
    cluster_username         = StringField("cluster_username?")
    cluster_password         = StringField("cluster_password?")
    cluster_ip               = StringField("cluster_ip?")

    submit_Save              = SubmitField  ('Save')
    submit_New               = SubmitField  ('New')
    submit_Cancel            = SubmitField  ('Cancel')

    has_FKs                  = False

class frm_clusters_delete(Form):
    submit_Delete            = SubmitField  ('Delete')
    submit_Cancel            = SubmitField  ('Cancel')

# =============================================================================
# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2022-03-16 19:41:36
# =============================================================================

# gen_model_flask.py:289 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/forms/frm_cost_centers.py
from decimal import ROUND_HALF_UP

class frm_cost_centers(Form):
    CC_Code                = StringField("CC_Code?")
    CC_Description         = StringField("CC_Description?")
    Cur_Code               = StringField("Cur_Code?")
    CC_Parent_Code         = StringField("CC_Parent_Code?")
    CC_Reg_Exp             = StringField("CC_Reg_Exp?")
    CC_Reference           = StringField("CC_Reference?")

    submit_Save            = SubmitField  ('Save')
    submit_New             = SubmitField  ('New')
    submit_Cancel          = SubmitField  ('Cancel')

    has_FKs                = False

class frm_cost_centers_delete(Form):
    submit_Delete          = SubmitField  ('Delete')
    submit_Cancel          = SubmitField  ('Cancel')

# =============================================================================
# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2022-03-16 19:41:36
# =============================================================================

# gen_model_flask.py:289 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/forms/frm_disk_images.py
from decimal import ROUND_HALF_UP

class frm_disk_images(Form):
    uuid                     = StringField("uuid?", validators=[DataRequired()])
    name                     = StringField("name?")
    annotation               = StringField("annotation?")
    image_type               = StringField("image_type?")
    image_state              = StringField("image_state?")
    #ERROR campo 'vm_disk_size' no tiene 'form_type' type is: 'bigint'
    vm_disk_size_mib         = IntegerField("vm_disk_size_mib?")
    vm_disk_size_gib         = IntegerField("vm_disk_size_gib?")
    cluster                  = StringField("cluster?")

    submit_Save              = SubmitField  ('Save')
    submit_New               = SubmitField  ('New')
    submit_Cancel            = SubmitField  ('Cancel')

    has_FKs                  = False

class frm_disk_images_delete(Form):
    submit_Delete            = SubmitField  ('Delete')
    submit_Cancel            = SubmitField  ('Cancel')

# =============================================================================
# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2022-03-16 19:41:36
# =============================================================================

# gen_model_flask.py:289 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/forms/frm_domains.py
from decimal import ROUND_HALF_UP

class frm_domains(Form):
    Domain_Id         = IntegerField("Domain_Id?", validators=[DataRequired()])
    Name              = StringField("Name?")
    Comments          = StringField("Comments?")

    submit_Save       = SubmitField  ('Save')
    submit_New        = SubmitField  ('New')
    submit_Cancel     = SubmitField  ('Cancel')

    has_FKs           = False

class frm_domains_delete(Form):
    submit_Delete     = SubmitField  ('Delete')
    submit_Cancel     = SubmitField  ('Cancel')

# =============================================================================
# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2022-03-16 19:41:36
# =============================================================================

# gen_model_flask.py:289 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/forms/frm_interface.py
from decimal import ROUND_HALF_UP

class frm_interface(Form):
    User_Id             = IntegerField("User_Id?")
    Table_name          = StringField("Table_name?")
    Option_Type         = IntegerField("Option_Type?")
    Argument_1          = StringField("Argument_1?")
    Argument_2          = StringField("Argument_2?")
    Argument_3          = StringField("Argument_3?")
    Is_Active           = BooleanField("Is_Active?")

    submit_Save         = SubmitField  ('Save')
    submit_New          = SubmitField  ('New')
    submit_Cancel       = SubmitField  ('Cancel')

    has_FKs             = False

class frm_interface_delete(Form):
    submit_Delete       = SubmitField  ('Delete')
    submit_Cancel       = SubmitField  ('Cancel')

# =============================================================================
# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2022-03-16 19:41:36
# =============================================================================

# gen_model_flask.py:289 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/forms/frm_migration_groups.py
from decimal import ROUND_HALF_UP

class frm_migration_groups(Form):
    Name             = StringField("Name?")
    Origin           = StringField("Origin?")
    Destiny          = StringField("Destiny?")
    Customer         = IntegerField("Customer?")
    Platform         = IntegerField("Platform?")

    submit_Save      = SubmitField  ('Save')
    submit_New       = SubmitField  ('New')
    submit_Cancel    = SubmitField  ('Cancel')

    has_FKs          = False

class frm_migration_groups_delete(Form):
    submit_Delete    = SubmitField  ('Delete')
    submit_Cancel    = SubmitField  ('Cancel')

# =============================================================================
# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2022-03-16 19:41:36
# =============================================================================

# gen_model_flask.py:289 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/forms/frm_migration_groups_vm.py
from decimal import ROUND_HALF_UP

class frm_migration_groups_vm(Form):
    MG_Id                       = SelectField("MG_Id?", coerce=int, validators=[DataRequired()])
    vm_uuid                     = StringField("vm_uuid?", validators=[DataRequired()])
    vm_cluster_uuid             = StringField("vm_cluster_uuid?")
    vm_name                     = StringField("vm_name?")
    vm_state                    = BooleanField("vm_state?")
    vm_has_pd                   = BooleanField("vm_has_pd?")
    vm_pd_name                  = StringField("vm_pd_name?")
    vm_pd_active                = BooleanField("vm_pd_active?")
    vm_pd_replicating           = BooleanField("vm_pd_replicating?")
    vm_pd_schedules             = IntegerField("vm_pd_schedules?")
    vm_last_replication         = DateTimeField("vm_last_replication?", format='%Y-%m-%d %H:%M:%S')
    vm_migrate                  = BooleanField("vm_migrate?")
    vm_project                  = StringField("vm_project?")

    submit_Save                 = SubmitField  ('Save')
    submit_New                  = SubmitField  ('New')
    submit_Cancel               = SubmitField  ('Cancel')

    has_FKs                     = True

class frm_migration_groups_vm_delete(Form):
    submit_Delete               = SubmitField  ('Delete')
    submit_Cancel               = SubmitField  ('Cancel')

# =============================================================================
# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2022-03-16 19:41:36
# =============================================================================

# gen_model_flask.py:289 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/forms/frm_nutanix_prism_vm.py
from decimal import ROUND_HALF_UP

class frm_nutanix_prism_vm(Form):
    Request_Id               = SelectField("Request_Id?", coerce=int, validators=[DataRequired()])
    project_uuid             = SelectField("project_uuid?")
    category_name            = SelectField("category_name?")
    cluster_uuid             = SelectField("cluster_uuid?")
    vm_name                  = StringField("vm_name?")
    power_state              = BooleanField("power_state?")
    vcpus_per_socket         = IntegerField("vcpus_per_socket?")
    num_sockets              = IntegerField("num_sockets?")
    memory_size_mib          = IntegerField("memory_size_mib?")
    memory_size_gib          = IntegerField("memory_size_gib?")
    Comments                 = StringField("Comments?")
    vm_uuid                  = StringField("vm_uuid?")
    vm_ip                    = StringField("vm_ip?")
    subnet_uuid              = SelectField("subnet_uuid?")
    vm_username              = StringField("vm_username?")
    vm_password              = StringField("vm_password?")
    backup_set_1             = BooleanField("backup_set_1?")
    backup_set_2             = BooleanField("backup_set_2?")
    backup_set_3             = BooleanField("backup_set_3?")
    disk_type                = IntegerField("disk_type?")
    disk_0_image             = StringField("disk_0_image?")
    disk_0_size              = IntegerField("disk_0_size?")
    disk_1_image             = StringField("disk_1_image?")
    disk_1_size              = IntegerField("disk_1_size?")
    disk_2_image             = StringField("disk_2_image?")
    disk_2_size              = IntegerField("disk_2_size?")
    disk_3_image             = StringField("disk_3_image?")
    disk_3_size              = IntegerField("disk_3_size?")
    disk_4_image             = StringField("disk_4_image?")
    disk_4_size              = IntegerField("disk_4_size?")
    disk_5_image             = StringField("disk_5_image?")
    disk_5_size              = IntegerField("disk_5_size?")
    disk_6_image             = StringField("disk_6_image?")
    disk_6_size              = IntegerField("disk_6_size?")
    disk_7_image             = StringField("disk_7_image?")
    disk_7_size              = IntegerField("disk_7_size?")
    disk_8_image             = StringField("disk_8_image?")
    disk_8_size              = IntegerField("disk_8_size?")
    disk_9_image             = StringField("disk_9_image?")
    disk_9_size              = IntegerField("disk_9_size?")
    disk_10_image            = StringField("disk_10_image?")
    disk_10_size             = IntegerField("disk_10_size?")
    disk_11_image            = StringField("disk_11_image?")
    disk_11_size             = IntegerField("disk_11_size?")
    vm_drp                   = BooleanField("vm_drp?")
    vm_drp_remote            = BooleanField("vm_drp_remote?")
    vm_cdrom                 = BooleanField("vm_cdrom?")
    drp_cluster_uuid         = StringField("drp_cluster_uuid?")
    nic_0_vlan               = StringField("nic_0_vlan?")
    nic_0_ip                 = StringField("nic_0_ip?")
    nic_0_mac                = StringField("nic_0_mac?")
    nic_1_vlan               = StringField("nic_1_vlan?")
    nic_1_ip                 = StringField("nic_1_ip?")
    nic_1_mac                = StringField("nic_1_mac?")
    nic_2_vlan               = StringField("nic_2_vlan?")
    nic_2_ip                 = StringField("nic_2_ip?")
    nic_2_mac                = StringField("nic_2_mac?")
    nic_3_vlan               = StringField("nic_3_vlan?")
    nic_3_ip                 = StringField("nic_3_ip?")
    nic_3_mac                = StringField("nic_3_mac?")
    request_text             = StringField("request_text?")

    submit_Save              = SubmitField  ('Save')
    submit_New               = SubmitField  ('New')
    submit_Cancel            = SubmitField  ('Cancel')

    has_FKs                  = True

class frm_nutanix_prism_vm_delete(Form):
    submit_Delete            = SubmitField  ('Delete')
    submit_Cancel            = SubmitField  ('Cancel')

# =============================================================================
# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2022-03-16 19:41:36
# =============================================================================

# gen_model_flask.py:289 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/forms/frm_nutanix_vm_images.py
from decimal import ROUND_HALF_UP

class frm_nutanix_vm_images(Form):
    imageservice_uuid_diskclone         = StringField("imageservice_uuid_diskclone?", validators=[DataRequired()])
    description                         = StringField("description?")
    size_mib                            = StringField("size_mib?")
    comments                            = StringField("comments?")

    submit_Save                         = SubmitField  ('Save')
    submit_New                          = SubmitField  ('New')
    submit_Cancel                       = SubmitField  ('Cancel')

    has_FKs                             = False

class frm_nutanix_vm_images_delete(Form):
    submit_Delete                       = SubmitField  ('Delete')
    submit_Cancel                       = SubmitField  ('Cancel')

# =============================================================================
# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2022-03-16 19:41:36
# =============================================================================

# gen_model_flask.py:289 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/forms/frm_projects.py
from decimal import ROUND_HALF_UP

class frm_projects(Form):
    project_uuid            = StringField("project_uuid?", validators=[DataRequired()])
    project_name            = StringField("project_name?")
    project_subnets         = StringField("project_subnets?")

    submit_Save             = SubmitField  ('Save')
    submit_New              = SubmitField  ('New')
    submit_Cancel           = SubmitField  ('Cancel')

    has_FKs                 = False

class frm_projects_delete(Form):
    submit_Delete           = SubmitField  ('Delete')
    submit_Cancel           = SubmitField  ('Cancel')

# =============================================================================
# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2022-03-16 19:41:36
# =============================================================================

# gen_model_flask.py:289 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/forms/frm_rates.py
from decimal import ROUND_HALF_UP

class frm_rates(Form):
    Typ_Code           = StringField("Typ_Code?")
    Cus_Id             = IntegerField("Cus_Id?")
    Pla_Id             = IntegerField("Pla_Id?")
    CC_Id              = IntegerField("CC_Id?")
    CI_Id              = IntegerField("CI_Id?")
    Rat_Price          = DecimalField("Rat_Price?", places=12, rounding=ROUND_HALF_UP)
    Cur_Code           = StringField("Cur_Code?")
    MU_Code            = StringField("MU_Code?")
    Rat_Period         = IntegerField("Rat_Period?")
    Rat_Type           = IntegerField("Rat_Type?")

    submit_Save        = SubmitField  ('Save')
    submit_New         = SubmitField  ('New')
    submit_Cancel      = SubmitField  ('Cancel')

    has_FKs            = False

class frm_rates_delete(Form):
    submit_Delete      = SubmitField  ('Delete')
    submit_Cancel      = SubmitField  ('Cancel')

# =============================================================================
# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2022-03-16 19:41:36
# =============================================================================

# gen_model_flask.py:289 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/forms/frm_requests.py
from decimal import ROUND_HALF_UP

class frm_requests(Form):
    Type                     = SelectField("Type?", coerce=int)
    User_Id                  = IntegerField("User_Id?")
    Approver_Id              = IntegerField("Approver_Id?")
    Status                   = IntegerField("Status?")
    Creation_Time            = DateTimeField("Creation_Time?", format='%Y-%m-%d %H:%M:%S')
    Last_Status_Time         = DateTimeField("Last_Status_Time?", format='%Y-%m-%d %H:%M:%S')
    Comments                 = StringField("Comments?")
    Task_uuid                = StringField("Task_uuid?")
    Task_status              = IntegerField("Task_status?")
    CC_Id                    = IntegerField("CC_Id?")
    uuid                     = StringField("uuid?")
    User_Comments            = StringField("User_Comments?")

    submit_Save              = SubmitField  ('Save')
    submit_New               = SubmitField  ('New')
    submit_Cancel            = SubmitField  ('Cancel')

    has_FKs                  = True

class frm_requests_delete(Form):
    submit_Delete            = SubmitField  ('Delete')
    submit_Cancel            = SubmitField  ('Cancel')

# =============================================================================
# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2022-03-16 19:41:36
# =============================================================================

# gen_model_flask.py:289 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/forms/frm_request_type.py
from decimal import ROUND_HALF_UP

class frm_request_type(Form):
    Id                  = IntegerField("Id?", validators=[DataRequired()])
    Description         = StringField("Description?")
    Table_Name          = StringField("Table_Name?")

    submit_Save         = SubmitField  ('Save')
    submit_New          = SubmitField  ('New')
    submit_Cancel       = SubmitField  ('Cancel')

    has_FKs             = False

class frm_request_type_delete(Form):
    submit_Delete       = SubmitField  ('Delete')
    submit_Cancel       = SubmitField  ('Cancel')

# =============================================================================
# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2022-03-16 19:41:36
# =============================================================================

# gen_model_flask.py:289 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/forms/frm_roles.py
from decimal import ROUND_HALF_UP

class frm_Role(Form):
    id                  = IntegerField("id?", validators=[DataRequired()])
    name                = StringField("name?")
    default             = BooleanField("default?")
    permissions         = IntegerField("permissions?")

    submit_Save         = SubmitField  ('Save')
    submit_New          = SubmitField  ('New')
    submit_Cancel       = SubmitField  ('Cancel')

    has_FKs             = False

class frm_Role_delete(Form):
    submit_Delete       = SubmitField  ('Delete')
    submit_Cancel       = SubmitField  ('Cancel')

# =============================================================================
# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2022-03-16 19:41:36
# =============================================================================

# gen_model_flask.py:289 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/forms/frm_subnets.py
from decimal import ROUND_HALF_UP

class frm_subnets(Form):
    uuid                       = StringField("uuid?", validators=[DataRequired()])
    name                       = StringField("name?")
    vlan_id                    = IntegerField("vlan_id?")
    vswitch_name               = StringField("vswitch_name?")
    type                       = StringField("type?")
    default_gateway_ip         = StringField("default_gateway_ip?")
    range                      = StringField("range?")
    prefix_length              = IntegerField("prefix_length?")
    subnet_ip                  = StringField("subnet_ip?")
    cluster                    = StringField("cluster?")

    submit_Save                = SubmitField  ('Save')
    submit_New                 = SubmitField  ('New')
    submit_Cancel              = SubmitField  ('Cancel')

    has_FKs                    = False

class frm_subnets_delete(Form):
    submit_Delete              = SubmitField  ('Delete')
    submit_Cancel              = SubmitField  ('Cancel')

# =============================================================================
# =============================================================================
# Auto-Generated code. do not modify
# (c) Sertechno 2018
# GLVH @ 2022-03-16 19:41:36
# =============================================================================

# gen_model_flask.py:289 => /home/gvalera/GIT/EG-Suite-Tools/Butler/code/auto/forms/frm_users.py
from decimal import ROUND_HALF_UP

class frm_User(Form):
    username              = StringField("username?")
    name                  = StringField("name?")
    role_id               = SelectField("role_id?", coerce=int)
    email                 = StringField("email?")
    password_hash         = StringField("password_hash?")
    confirmed             = BooleanField("confirmed?")
    CC_Id                 = IntegerField("CC_Id?")
    roles                 = StringField("roles?")

    submit_Save           = SubmitField  ('Save')
    submit_New            = SubmitField  ('New')
    submit_Cancel         = SubmitField  ('Cancel')

    has_FKs               = True

class frm_User_delete(Form):
    submit_Delete         = SubmitField  ('Delete')
    submit_Cancel         = SubmitField  ('Cancel')

# =============================================================================
# ======================================================================
# EG Butler Main Migrations FORM
# (c) Sertechno 2022
# GLVH @ 2022-01-20
# ======================================================================
# gvalera@emtecgroup.net
# ======================================================================

from emtec import *
from emtec.nutanix import *
from emtec.butler.constants import *
from wtforms            import FormField
from wtforms            import FieldList
from wtforms.validators import ValidationError

# GV Required for Field List of variable VMs
class cbx_vm(Form):
    name = BooleanField()

# GV Main Migration form object
class frm_migration_01(Form):
    # GV Basic Form
    mgId         = 0
    mgName       = SelectField (coerce=int)
    mgOrigin     = SelectField ()
    mgDestiny    = SelectField ()
    mgCustomer   = 0
    mgPlatform   = 0
    # GV Asociated fields
    # GV List of Vms
    mgVms        = []
    # GV Migration checkboxes list, one per each vm
    mgMigration  = FieldList(FormField(cbx_vm),min_entries=0)
    # GV Interface/Support fields
    mgNewName    = StringField ('MG New Name',
                        validators=[],
                        default=''
                    )
    mgEditName   = StringField ('MG Edit Name',
                        validators=[],
                        default=''
                    )
    mgCloneName  = StringField ('MG Clone Name',
                        validators=[],
                        default=''
                    )
    mgNewId            = IntegerField()
    mgAllVms           = SelectField ()
    # Buffer Data
    mgData       = {'can_migrate':False}
    # ------------------------------------------------------------------
    # Buttons ----------------------------------------------------------
    # MG Buttons
    submit_Choose   = SubmitField ('Choose')
    submit_Create   = SubmitField ('Create')
    submit_Clone    = SubmitField ('Clone')
    submit_Edit     = SubmitField ('Edit')
    submit_Switch   = SubmitField ('Switch')
    # VM Buttons
    submit_Add      = SubmitField ('Add')
    # Form Action Buttons
    submit_Save     = SubmitField ('Save')
    submit_Delete   = SubmitField ('Delete')
    submit_Cancel   = SubmitField ('Cancel')
    submit_Validate = SubmitField ('Validate')
    submit_Migrate  = SubmitField ('Migrate')

def get_discos():
    table_discos="""
            <table> <!-- DISCOS ------------------------------------ -->
                <thead>
                    <tr>
                        <th width=32><b>Disco #</b></th>
                        <th width=64><b>Tamaño en GB</b></th>
                        <th width=32><b></b></th>
                        <th width=384><b>Imagen de Disco</b></th>
                        <th width=32><b></b></th>
                        <th width=256><b>Otra Subnet</b></th>
                    </tr>
                </thead>
                <tbody>
                """
    for i in range(12):
        table_discos = table_discos+f"""
                    <tr>
                        <td align=center>{i+1}</td>
                        <td><input class="form-control" id="vmDisk{i}Size" name="vmDisk{i}Size" type="number" value={{{{form.vmDisk{i}Size.data}}}}></td>
                        <td></td>
                        <td>
                            <select class="form-control" name="vmDisk{i}Image" id="vmDisk{i}Image">
                              {{%- for value,option in form.vmDisk0Image.choices %}}
                                {{%- if value == form.vmDisk{i}Image.data %}}
                                <option selected value="{{value}}">{{option}}</option>
                                {{%- else %}}
                                <option value="{{value}}">{{option}}</option>
                                {{%- endif %}}
                              {{%- endfor %}}
                            </select>
                        </td>
                        """
        if i <3:
            table_discos=table_discos+f"""
                        <td></td>
                        <td><select class="form-control" name="vmNic{i}Vlan" id="vmNic{i}Vlan"></select></td>
                        """
        table_discos = table_discos+"""
                    </tr>
                    """
    table_discos = table_discos+f"""
            </tbody>
        </table>
        """
    return table_discos

frm_request_html="""
<form method="post" class="form" role="form">
    <!-- csrf_token: {{ form.csrf_token }} hidden_tag(): {{ form.hidden_tag() }} name: {{ form.name }} -->
    <table bgcolor=white> <!-- MAIN TABLE -------------------------- -->
        <tr>
            <td>
                <table> <!-- Main VM fields request form ----------- -->
                    <tr>
                        <td width=256><b>Solicitud</b></td>
                        {%- if row.Id > 0 %}
                        <td style="color:blue">{{row.Id}} <b>{{get_request_status_description(row.Status)|join(', ')}}</b></td>
                        {%- else %}
                        <td style="color:blue"><b>Nueva solicitud</b></td>
                        {%- endif %}
                    </tr>
                    <tr>
                        <td width=256><b>Nombre de MV   </b></td>
                        <!-- <td><input class="form-control" id="vmName" name="vmName" type="text" value="{ {rox.vm_name} }"></td> -->
                        <td><input class="form-control" id="vmName" name="vmName" type="text" value="{{form.vmName.data}}"></td>
                        {# %- if 'vmName' in form.errors %}<td><font color=red>{% for error in form.errors.vmName %}{{error}}{% endfor %}</td>{% endif % #}
                        {%- if form.vmData.extra is defined and form.vmData.extra %}
                            <td width=32></td>
                            <td width=256><b>Cluster</b></td>
                            <td>
                              <select class="form-control" name="vmCluster" id="vmCluster">
                                {%- for value,option in form.vmCluster.choices %}
                                  {%- if value == form.vmCluster.data %}
                                  <option selected value="{{value}}">{{option}}</option>
                                  {%- else %}
                                  <option             value="{{value}}">{{option}}</option>
                                  {%- endif %}
                                {%- endfor %}
                              </select>
                            </td>
                        {%- endif %}
                    </tr>
                    <tr>
                        <td><b>CPU cores por Socket</b></td>
                        <!-- td><input class="form-control" id="vmCPS" name="vmCPS" type="number" value="{{form.vmCPS.data}}" onchange="get_cpu()"></td -->
                        <td><input class="form-control" id="vmCPS" name="vmCPS" type="number" value="{{form.vmCPS.data}}"></td>
                        {%- if form.vmData.extra is defined and form.vmData.extra %}
                            <td width=32></td>
                            <td width=256><b>Proyecto</b></td>
                            <td>
                              <!-- GV 202010318 select class="form-control" name="vmProject" id="vmProject" onchange="get_subnet_options(this.value)" -->
                              <select class="form-control" name="vmProject" id="vmProject" onchange="get_project_subnet_options(this.value)">
                                {%- for value,option in form.vmProject.choices %}
                                  {%- if value == form.vmProject.data %}
                                  <option selected value="{{value}}">{{option}}</option>
                                  {%- else %}
                                  <option value="{{value}}">{{option}}</option>
                                  {%- endif %}
                                {%- endfor %}
                              </select>
                            </td>
                        {%- endif %}
                    </tr>
                    <tr>
                        <td><b>Sockets</b></td>
                        <!-- td><input class="form-control" id="vmSockets" name="vmSockets" type="number" value="{{form.vmSockets.data}}" onchange="get_cpu()"></td -->
                        <td><input class="form-control" id="vmSockets" name="vmSockets" type="number" value="{{form.vmSockets.data}}"></td>
                        {%- if form.vmData.extra is defined and form.vmData.extra %}
                            <td width=32></td>
                            <td width=256><b>Categoria</b></td>
                            <td>
                              <select class="form-control" name="vmCategory" id="vmCategory">
                                {%- for value,option in form.vmCategory.choices %}
                                  {%- if value == form.vmCategory.data %}
                                  <option selected value="{{value}}">{{option}}</option>
                                  {%- else %}
                                  <option             value="{{value}}">{{option}}</option>
                                  {%- endif %}
                                {%- endfor %}
                              </select>
                            </td>
                        {%- endif  %}
                    </tr>
                    <!--tr>
                        <td><b>Número de CPUs </b></td>
                        <! -- td style="color:blue"><b>{{ form.vmCPS.data * form.vmSockets.data }}</b></td - ->
                        <td style="color:blue"><b>
                            <input class="form-control-plaintext" id="vmCPU" name="vmCPU" type="text" style="color:blue;font-weight:bold;" value="{{ form.vmCPS.data * form.vmSockets.data }}">
                        </b></td>
                    </tr-->
                    <tr>
                        <td><b>Memoria RAM en GB</b></td>
                        <!-- <td><input class="form-control" id="vmRAM" name="vmRAM" type="number" value="{{rox.memory_size_gib}}"></td> -->
                        <td><input class="form-control" id="vmRAM" name="vmRAM" type="number" value="{{form.vmRAM.data}}"></td>
                        <td width=32></td>
                        <td width=256><b>Subred</b></td>
                        <td><select class="form-control" name="vmSubnet" id="vmSubnet"></select></td>
                    </tr>
                    <tr>
                        <td><b>Corporativa</b></td>
                        <td>
                          <select class="form-control" name="vmCorporate" id="vmCorporate">
                            {%- for value,option in form.vmCorporate.choices %}
                              {%- if value == form.vmCorporate.data %}
                              <option selected value="{{value}}">{{option}}</option>
                              {%- else %}
                              <option value="{{value}}">{{option}}</option>
                              {%- endif %}
                            {%- endfor %}
                          </select>
                        </td>
                        <td width=32></td>
                        <td><b>DRP</b></td>
                        <td>{{ form.vmDRP }}</td>
                    </tr>
                    <tr>
                        <td><b>Gerencia</b></td>
                        <td>
                          <select class="form-control" name="vmDepartment" id="vmDepartment">
                            {%- for value,option in form.vmDepartment.choices %}
                              {%- if value == form.vmDepartment.data %}
                              <option selected value="{{value}}">{{option}}</option>
                              {%- else %}
                              <option value="{{value}}">{{option}}</option>
                              {%- endif %}
                            {%- endfor %}
                          </select>
                        </td>
                        <td width=32></td>
                        <td><b>CD ROM</b></td>
                        <td>{{ form.vmCDROM }}</td>
                    </tr>
                    <tr>
                        <td><b>Centro de Costo</b></td>
                        <td>
                          <select class="form-control" name="vmCC" id="vmCC">
                            {%- for value,option in form.vmCC.choices %}
                              {%- if value == form.vmCC.data %}
                              <option selected value="{{value}}">{{option}}</option>
                              {%- else %}
                              <option value="{{value}}">{{option}}</option>
                              {%- endif %}
                            {%- endfor %}
                          </select>
                        </td>
                        <td></td>
                        <td><b>Resumen de MV</b></td>
                        <td><input class="form-control-plaintext" id="vmResume" name="vmResume" type="text" value="Resume" style="color:blue;font-weight:bold;"></td>
                    </tr>
                    <tr>
                        <td><b>Tipo de disco</b></td>
                        <td>
                          <select class="form-control" name="vmType" id="vmType">
                            {%- for value,option in form.vmType.choices %}
                              {%- if value == form.vmType.data %}
                              <option selected value="{{value}}">{{option}}</option>
                              {%- else %}
                              <option value="{{value}}">{{option}}</option>
                              {%- endif %}
                            {%- endfor %}
                          </select>
                        </td>
                        <td></td>
                        <td><b>Mensual estimado UF</b></td>
                        <td><input class="form-control-plaintext" id="vmMonth" name="vmMonth" type="text" value="Month" style="color:blue;font-weight:bold;"></td>
                    </tr>
                </table>
            </td>
        </tr>
        <hr>
        <!-- td><input class="form-control-plaintext" id="vmHelp" name="vmHelp" type="text" value="" style="color:red"></td -->
        {%- if form.vmData.debug is defined and form.vmData.debug %}
        <tr>
        <td><input class="form-control-plaintext" id="vmMessage" name="vmMessage" type="text" value="Message" style="color:red;font-weight:bold;"></td>
        </tr>
        {%- endif %}
        <tr>
            <td>
            <hr>
            <!-- VM required storage specifications ---------------- -->
            """+get_discos(
)+"""
            <hr>
            </td>
        </tr>
        <tr><td>
        <table> <!-- REQUERIMIENTO ESPECIAL ---------------------------- -->
            <thead>
                <tr><th width=1024><b>Requerimiento especial</b></th></tr>
            </thead>
            <tbody>
                <tr><td><input class="form-control" id="vmRequestText" name="vmRequestText" type="text" value="{{form.vmRequestText.data}}"></td></tr>  
            </tbody>
        </table>
        </td></tr>
    </table>
    <hr>
    <!-- Button options as per user role --------------------------- -->
    {%- if form.vmData.rolename == 'Requestor' %}
        <!-- Options for Requestor role ---------------------------- -->
        {# %- if row.Status is none or has_status(row.Status,form.vmData.status.NONE) % #}
        {%- if row.Status is none or row.Status == 0 or has_status(row.Status,form.vmData.status.NONE) %}
            <!-- Options for non Created Request ----------------------- -->
            <input class="btn btn-default" id="submit_Guardar"    name="submit_Guardar"    type="submit" value="Guardar">
            <input class="btn btn-default" id="submit_Retorno"   name="submit_Retorno"   type="submit" value="Retorno">
        {%- elif has_status(row.Status,form.vmData.status.CREATED) %}
            <!-- Options for Created Request ----------------------- -->
            <input class="btn btn-default" id="submit_Guardar"    name="submit_Guardar"    type="submit" value="Guardar">
            <input class="btn btn-default" id="submit_Completado" name="submit_Completado" type="submit" value="Completado" >
            <input class="btn btn-default" id="submit_Cancelar"   name="submit_Cancelar"   type="submit" value="Cancelar">
            <input class="btn btn-default" id="submit_Retorno"   name="submit_Retorno"   type="submit" value="Retorno">
        {%- elif has_status(row.Status,form.vmData.status.REQUESTED) %}
            <!-- Options for Requested Request - ---------------------->
            <input class="btn btn-default" id="submit_Cancelar"   name="submit_Cancelar"   type="submit" value="Cancelar">
            <input class="btn btn-default" id="submit_Retorno"   name="submit_Retorno"   type="submit" value="Retorno">    
        {%- else %}
            <!-- Options for Inactive Request ---------------------- -->
            <input class="btn btn-default" id="submit_Retorno"   name="submit_Retorno"     type="submit" value="Retorno">
        {%- endif %}
    {%- elif form.vmData.rolename == 'Approver' %}
        <!-- Options for Approver role ----------------------------- -->
        {%- if has_status(row.Status,[form.vmData.status.REQUESTED,form.vmData.status.REVIEWED]) %}
            <!-- Options for Requested Request --------------------- -->
            <input class="btn btn-default" id="submit_Guardar"    name="submit_Guardar"    type="submit" value="Guardar">
            <input class="btn btn-default" id="submit_Rechazar"   name="submit_Rechazar"   type="submit" value="Rechazar">
            <input class="btn btn-default" id="submit_Aprobar"    name="submit_Aprobar"    type="submit" value="Aprobar">
            <input class="btn btn-default" id="submit_Retorno"   name="submit_Retorno"   type="submit" value="Retorno">
        {%- elif has_status(row.Status,[form.vmData.status.REJECTED,form.vmData.status.APPROVED]) %}
            <!-- Options for Handled Request ----------------------- -->
            <input class="btn btn-default" id="submit_Retorno"   name="submit_Retorno"   type="submit" value="Retorno">    
        {%- else %}
            <!-- Options for Inactive or post approved Request ----- -->
            <input class="btn btn-default" id="submit_Retorno"   name="submit_Retorno"     type="submit" value="Retorno">
        {%- endif %}
    {%- else %}
        <!-- Options for Other/Viewer role ------------------------- -->
            <input class="btn btn-default" id="submit_Retorno"   name="submit_Retorno"     type="submit" value="Retorno">
    {%- endif %}
    <hr>
    <!-- HIDDEN DATA -->
    <input id="vmTopCC"   name="vmTopCC"     type="hidden" value="{{form.vmTopCC}}">
    <!-- HIDDEN DATA COMPLETE -->
    {%- if form.vmData.debug is defined and form.vmData.debug %}
        <!--DEBUG DATA FOLLOWS ------------------------------------- -->
        <b>DEBUG MODE is ON: form.vmData.debug is defined and True then debug data follows:</b><br>
        <hr> 
        <p>form.vmTopCC={{form.vmTopCC}}</p>
        row = {{row}}<br>
        top cost center = {{form.vmData.top_cost_center}} {{form.vmData.top_cost_center_id}}<br>
        {%- for status in form.vmData.status %}
            {%- if has_status(row.Status,form.vmData.status[status]) %}
                Status = {{row.Status}} has status {{status}} {{form.vmData.status[status]}}<br> 
            {%- endif %}
        {%- endfor %}
        <hr>
        rox = {{rox}}
        <hr>
        form.vmData = {{form.vmData}}
        <!--DEBUG DATA complete ------------------------------------ -->
    {%- endif %}
</form>
"""

if __name__ == "__main__":
    print(frm_request_html)
# ======================================================================
# EG Butler Main Requests FORM
# (c) Sertechno 2020
# GLVH @ 2020-12-19
# ======================================================================
# GLVH @ 2021-03-21 Add other NICS, and validartors complemented
# GLVH @ 2021-05-12 Copias de seguridad locales y remotas
# gvalera@emtecgroup.net
# ======================================================================

from emtec import *
from emtec.nutanix import *
from emtec.butler.constants import *
from wtforms.validators import ValidationError
from flask_babel import lazy_gettext

# Custom Validator functions for butler form request support
# very powerfull function to validate data prior submit
def disk_size(form,field):
    form.logger.debug(f"disk_size: IN field={field.name}")
    if field.name == 'vmDisk0Size':
        ImageFieldName=field.name.replace('Size','Image')
        ImageField=getattr(form,ImageFieldName)
        for choice in ImageField.iter_choices():
            if choice[2]:
                try:
                    if '(' in choice[1]:
                        ImageFieldSize = choice[1].split('(')[1] 
                        if len(ImageFieldSize) and ' ' in ImageFieldSize:
                            ImageFieldSize = float(ImageFieldSize.split(' ')[0])
                            if ImageFieldSize > int(ImageFieldSize):
                                ImageFieldSize =  int(ImageFieldSize) + 1
                            if field.data < ImageFieldSize:
                                raise ValidationError( lazy_gettext('Minimal size is %s GB')%ImageFieldSize ) 
                except Exception as e:
                    raise ValidationError(f'{this()}: {str(e)}') 
        form.logger.debug("disk_size: field={field.name} OUT")
    return

def name(form,field):
    ''' validates that vmName does not exist in Nutanix '''
    form.logger.debug(f"{this()}: IN field={field.name}")
    if form.vmData.get('row') is None or form.vmData.get('row').Status<REQUEST_APPROVED:
        vm = get_nutanix_vm(form.vmData.get('app'),form.vmName.data,timeout=3,logger=form.logger)
        if vm is None:
            return
        else:
            error = lazy_gettext("VM '%s' already exists.")
            raise ValidationError(error%form.vmName.data)
    form.logger.debug(f"{this()}: field={field.name} OUT")
    return

def ip_address(form,field):
    form.logger.warning("ip_address: field={field.name} IN WARNING WARNING WARNING OJO NO ESTA ACTIVA LA VALIDACION AUN")
    return
    try:
        #print(f"{this()}: form.vmSubnet.data = {form.vmSubnet.data}")
        #print(f"{this()}: field.data = {field.data}")
        if form.vmSubnet.data is not None and field.data not in [None,'','None']:
            ip = ip_to_int(field.data.split('.'))
            #print(f"{this()}: field.data = {field.data} ip = {ip}")
            #print(f"{this()}: form.vmData = {form.vmData is not None}")
            in_range=False
            if form.vmData is not None:
                #print(f"{this()}: form.vmData['subnets'] = {form.vmData['subnets']}")
                for subnet in form.vmData['subnets']:
                    # Check will be valid if on selecte subnet range only
                    #print(f"'{this()}: subnet = {subnet}")
                    #print(f"{this()}: subnet['uuid'] = {subnet['uuid']}")
                    if subnet['uuid'] == form.vmSubnet.data:
                        # Will check all vaid ranges for this subnet
                        #print(f"{this()}: subnet['range'] = {subnet['range']}")
                        for subnet_range in subnet['range'].split(','):
                            start,end=subnet_range.split(' ')
                            #print(f"{this()}: ip={ip} start={ip_to_int(start.split('.'))} end={ip_to_int(end.split('.'))}")
                            if ip >= ip_to_int(start.split('.')) and ip <= ip_to_int(end.split('.')):
                                in_range=True
                                #print(f"'{this()}: '{field.data}' en rango. exito")
                if not in_range:
                     #print(f"IP '{field.data}' fuera de rango")
                     error = lazy_gettext("IP '%s' out of range")
                     raise ValidationError(f"{this()}: {error}")                 
        #else:
            #print(f"{this()}: chequeo no requerido o no posible")
    except Exception as e:
        raise ValidationError(f'{this()}: {str(e)}') 
    #print("ip_address: field={field.name} OUT")

def subnet(form,field):
    form.logger.debug(f"subnet: IN field={field.name}")
    return
    # removes any previous errors
    subnet_keys = []
    form.errors.pop('vmSubnet',None)
    choices     = getattr(form,field.name).choices
    subnets     = []
    for choice in choices:
        subnets = choice[1]
    valid_subnets = []
    for subnet in subnets:
        valid_subnets.append(subnet[0].split(':')[0])
    # Actual validation here
    if field.name == 'vmSubnet':
        # Reset form list of valid keys ...
        form.vmSubnetKeys.append(f"{form.vmSubnet.data}:{form.vmAddress.data}")
        if field.data in valid_subnets:
            #print(f"{this()}: {field.name}: Subnet primaria  OK")         
            pass
        else:
            error = lazy_gettext("invalid primary subnetwork")
            raise ValidationError(f'{this()}: {field.name}: {error}')
    else:
        # Other NICs , none/null is valid value
        valid_subnets.append("")
        if field.data in valid_subnets:            
            ipname  = field.name.replace("Vlan","Ip")
            macname = field.name.replace("Vlan","Mac")
            if getattr(form,ipname).data is None:
                key     = f"{field.data}:{getattr(form,ipname).data}"
            else:
                key     = f"{field.data}:"
            # will check if not duplicated
            if key in form.vmSubnetKeys:
                # do not allow duplicates, then reset data
                field.data = None
                setattr(getattr(form,ipname),"data",None)
                setattr(getattr(form,macname),"data",None)
                form.logger.warning(f"{this()}: NIC especificacion duplicada data reseted")
                error = lazy_gettext("Duplicated subnetwork specification")
                raise ValidationError(f'{this()}: {field.name}: {error}')
            else:
                form.vmSubnetKeys.append(key)
                form.logger.debug(f"{this()}: field {field.name} OK {key} accepted")
        else:
            error = lazy_gettext("Invalid subnetwork")
            raise ValidationError(f'{this()}: {field.name}: {error}')
    form.logger.debug(f"{this()}: field={field.name} OUT")

def form_log(form,l):
    l(f"FORM")
    l(f"Status       = {form.vmStatus.data}")
    l(f"Name         = {form.vmName.data}")
    l(f"CPS          = {form.vmCPS.data}")
    l(f"Sockets      = {form.vmSockets.data}")
    l(f"CPU          = {form.vmCPU}")
    l(f"RAM          = {form.vmRAM.data}")
    l(f"Corporate    = {form.vmCorporate.data}")
    l(f"Department   = {form.vmDepartment.data}")
    l(f"CC           = {form.vmCC.data}")
    l(f"Type         = {form.vmType.data}")
    l(f"D0           = {form.vmDisk0Size.data} {form.vmDisk0Image.data}")
    l(f"D1           = {form.vmDisk1Size.data}")
    l(f"D2           = {form.vmDisk2Size.data}")
    l(f"D3           = {form.vmDisk3Size.data}")
    l(f"D4           = {form.vmDisk4Size.data}")
    l(f"D5           = {form.vmDisk5Size.data}")
    l(f"D6           = {form.vmDisk6Size.data}")
    l(f"D7           = {form.vmDisk7Size.data}")
    l(f"D8           = {form.vmDisk8Size.data}")
    l(f"D9           = {form.vmDisk9Size.data}")
    l(f"D10          = {form.vmDisk10Size.data}")
    l(f"D11          = {form.vmDisk11Size.data}")
    l(f"Cluster      = {form.vmCluster.data}")
    l(f"Project      = {form.vmProject.data}")
    l(f"Category     = {form.vmCategory.data}")
    l(f"ProjectName  = {form.vmProjectName.data}")
    l(f"CategoryName = {form.vmCategoryName.data}")
    l(f"VLAN 0       = {form.vmVlan0Name.data}")
    l(f"VLAN 1       = {form.vmVlan1Name.data}")
    l(f"VLAN 2       = {form.vmVlan2Name.data}")
    l(f"VLAN 3       = {form.vmVlan3Name.data}")
    l(f"DRP          = {form.vmDRP.data}")
    l(f"DRPRemote    = {form.vmDRPRemote.data}")
    l(f"CDROM        = {form.vmCDROM.data}")

class frm_request(Form):
    logger            = None
    vmTopCC           = 0
    vmTopCCCode       = ''
    # General
    vmStatus          = IntegerField()
    vmName            = StringField ('VM Name',
                            validators=[
                                InputRequired(
                                    lazy_gettext('VM name is required')
                                ),
                                name]
                            ,default=''
                        )
    vmCPS             = IntegerField(
                            validators=[
                                InputRequired(
                                    lazy_gettext('Number of CPUs per Socket is required')
                                ),
                                NumberRange(min=1,message=lazy_gettext('Minimal CPS is 1'))
                                ],
                            default=1
                            )
    vmSockets         = IntegerField(
                            validators=[
                                InputRequired(
                                    lazy_gettext('Number of Sockets is required')
                                ),
                                NumberRange(
                                    min=1,
                                    message=lazy_gettext('Mínimal Sockets are 1')
                                    )
                                ],
                            default=1
                        )
    vmCPU             = 1
    vmRAM             = IntegerField(
                            validators=[
                                InputRequired(
                                    lazy_gettext('Minimal 1 GB of RAM is required')
                                ),
                                NumberRange(
                                    min=1,
                                    message=lazy_gettext('Minimal RAM is 1 GB')
                                )
                            ],
                            default=1
                        )
    vmCorporate       = SelectField (
                            validators=[
                                InputRequired(
                                    lazy_gettext('Corporate is required')
                                )
                            ],
                            coerce=int
                        )
    vmDepartment      = SelectField (
                            validators=[
                                InputRequired(
                                    lazy_gettext('Management required')
                                )
                            ],
                            coerce=int
                        )
    vmCC              = SelectField (
                            validators=[
                                InputRequired(
                                    lazy_gettext('CC required')
                                )
                            ],
                            coerce=int
                        )
    vmType            = SelectField (
                            validators=[
                                InputRequired(
                                    lazy_gettext('Disk type must me defined')
                                )
                            ],
                            coerce=int
                        )
    vmDisk0Size       = IntegerField(
                        validators=[NumberRange(min=0),disk_size],default=0)
    vmDisk0Image      = SelectField()
    vmDisk1Size       = IntegerField(validators=[NumberRange(min=0)],default=0)
    vmDisk2Size       = IntegerField(validators=[NumberRange(min=0)],default=0)
    vmDisk3Size       = IntegerField(validators=[NumberRange(min=0)],default=0)
    vmDisk4Size       = IntegerField(validators=[NumberRange(min=0)],default=0)
    vmDisk5Size       = IntegerField(validators=[NumberRange(min=0)],default=0)
    vmDisk6Size       = IntegerField(validators=[NumberRange(min=0)],default=0)
    vmDisk7Size       = IntegerField(validators=[NumberRange(min=0)],default=0)
    vmDisk8Size       = IntegerField(validators=[NumberRange(min=0)],default=0)
    vmDisk9Size       = IntegerField(validators=[NumberRange(min=0)],default=0)
    vmDisk10Size      = IntegerField(validators=[NumberRange(min=0)],default=0)
    vmDisk11Size      = IntegerField(validators=[NumberRange(min=0)],default=0)
    # Ownership
    vmCluster         = SelectField()
    vmProject         = StringField()
    vmCategory        = StringField()
    vmProjectName     = StringField()
    vmCategoryName    = StringField()
    
    # Networking      --------------------------------------------------
    '''
    vmVlan0Name        = SelectField (validators=[],coerce=str)
    vmVlan1Name        = SelectField (validators=[],coerce=str)
    vmVlan2Name        = SelectField (validators=[],coerce=str)
    vmVlan3Name        = SelectField (validators=[],coerce=str)
    '''
    vmVlan0Name        = SelectField (coerce=str)
    vmVlan1Name        = SelectField (coerce=str)
    vmVlan2Name        = SelectField (coerce=str)
    vmVlan3Name        = SelectField (coerce=str)

    #                 --------------------------------------------------
    vmUsername        = StringField()
    vmPassword        = StringField()
    # Backup sets
    vmBackUpSet1      = IntegerField()
    vmBackUpSet2      = IntegerField()
    vmBackUpSet3      = IntegerField()
    # Flags
    vmDRP             = BooleanField()         
    vmDRPRemote       = BooleanField()         
    vmCDROM           = BooleanField()      
    # Request text field (falta guardarlo en BD)
    vmRequestText     = StringField()
    # Buttons ----------------------------------------------------------
    submit_Guardar    = SubmitField (lazy_gettext('Save'))
    submit_Completado = SubmitField (lazy_gettext('Completed'))
    submit_Eliminar   = SubmitField (lazy_gettext('Delete'))
    submit_Cancelar   = SubmitField (lazy_gettext('Cancel'))
    submit_Rechazar   = SubmitField (lazy_gettext('Reject'))
    submit_Aprobar    = SubmitField (lazy_gettext('Approve'))
    submit_Retorno    = SubmitField (lazy_gettext('Return'))
    # Validation data, hidden fields -----------------------------------
    vmData            = {}
    # Interface only fields, this is volatile data
    vmDebug           = BooleanField()
    vmMessage1        = None
    vmMessage2        = None
    vmMessage3        = None
    vmMessage4        = None
    vmMessage5        = None
    vmMessage6        = None
    vmMessage7        = None
    vmMessage8        = None
    # list used for subnet duplicity validation
    vmSubnetKeys      = []
    # ------------------------------------------------------------------
    
