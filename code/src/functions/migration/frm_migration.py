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

