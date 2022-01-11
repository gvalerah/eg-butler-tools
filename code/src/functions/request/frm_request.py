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
    
