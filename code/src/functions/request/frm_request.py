# ======================================================================
# EG Butler Main Requests FORM
# (c) Sertechno 2020
# GLVH @ 2020-12-19
# ======================================================================
# GLVH @ 2021-03-21 Add other NICS, and validartors complemented
# gvalera@emtecgroup.net
# ======================================================================

from emtec import *
from wtforms.validators import ValidationError

# Custom Validator functions for butler form request support
# very powerfull function to validate data prior submit
def disk_size(form,field):
    form.logger.debug(f"disk_size: IN field={field.name}")
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
                            raise ValidationError(f'Tamaño Mínimo es {ImageFieldSize} GB') 
            except Exception as e:
                raise ValidationError(f'{str(e)}') 
    form.logger.debug("disk_size: field={field.name} OUT")

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
                     raise ValidationError(f"IP '{field.data}' fuera de rango")                 
        #else:
            #print(f"{this()}: chequeo no requerido o no posible")
    except Exception as e:
        raise ValidationError(f'{str(e)}') 
    print("ip_address: field={field.name} OUT")

def subnet(form,field):
    form.logger.debug(f"subnet: IN field={field.name}")
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
            raise ValidationError(f'{this()}: {field.name}: Subred primaria invalida')
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
                raise ValidationError(f'{this()}: {field.name}: Subred especificación duplicada')
            else:
                form.vmSubnetKeys.append(key)
                form.logger.debug(f"{this()}: field {field.name} OK {key} accepted")
        else:
            raise ValidationError(f'{this()}: {field.name}: Subred invalida')
    form.logger.debug(f"{this()}: field={field.name} OUT")
 
class frm_request(Form):
    logger            = None
    #mTopCC           = IntegerField()
    vmTopCC           = 0
    vmTopCCCode       = ''
    # General
    vmStatus          = IntegerField()
    vmName            = StringField ('VM Name',
                        validators=[InputRequired('Nombre de MV es requerido')],default='')
    vmCPS             = IntegerField(
                        validators=[InputRequired('Número de CPUs por Socket es requerido'),
                                    NumberRange(min=1,message='CPS mínimo es 1')],default=1)
    vmSockets         = IntegerField(
                        validators=[InputRequired('Número de Sockets es requerido'),
                                    NumberRange(min=1,message='Sockets mínimo es 1')],default=1)
    vmCPU             = 1
    vmRAM             = IntegerField(
                        validators=[InputRequired('RAM mínima es requerida'),
                                    NumberRange(min=1,message='RAM mínima es 1 GB')],default=1)
    vmCorporate       = SelectField (
                        validators=[InputRequired('Se requiere Direccion')],coerce=int)
    vmDepartment      = SelectField (
                        validators=[InputRequired('Se requiere Departamento')],coerce=int)
    vmCC              = SelectField (
                        validators=[InputRequired('Se requiere CC')],coerce=int)
    vmType            = SelectField (
                        validators=[InputRequired('Debe definirse tipo de almacenamiento')],coerce=int)
    vmDisk0Size       = IntegerField(
                        validators=[NumberRange(min=0),disk_size],default=0)
    vmDisk0Image      = SelectField()
    vmDisk1Size       = IntegerField(validators=[NumberRange(min=0),disk_size],default=0)
    vmDisk1Image      = SelectField()
    vmDisk2Size       = IntegerField(validators=[NumberRange(min=0),disk_size],default=0)
    vmDisk2Image      = SelectField()
    vmDisk3Size       = IntegerField(validators=[NumberRange(min=0),disk_size],default=0)
    vmDisk3Image      = SelectField()
    vmDisk4Size       = IntegerField(validators=[NumberRange(min=0),disk_size],default=0)
    vmDisk4Image      = SelectField()
    vmDisk5Size       = IntegerField(validators=[NumberRange(min=0),disk_size],default=0)
    vmDisk5Image      = SelectField()
    vmDisk6Size       = IntegerField(validators=[NumberRange(min=0),disk_size],default=0)
    vmDisk6Image      = SelectField()
    vmDisk7Size       = IntegerField(validators=[NumberRange(min=0),disk_size],default=0)
    vmDisk7Image      = SelectField()
    vmDisk8Size       = IntegerField(validators=[NumberRange(min=0),disk_size],default=0)
    vmDisk8Image      = SelectField()
    vmDisk9Size       = IntegerField(validators=[NumberRange(min=0),disk_size],default=0)
    vmDisk9Image      = SelectField()
    vmDisk10Size      = IntegerField(validators=[NumberRange(min=0),disk_size],default=0)
    vmDisk10Image     = SelectField()
    vmDisk11Size      = IntegerField(validators=[NumberRange(min=0),disk_size],default=0)
    vmDisk11Image     = SelectField()
    # Ownership
    vmCluster         = SelectField()
    vmProject         = SelectField()
    vmCategory        = SelectField()
    # Networking      --------------------------------------------------
    vmSubnet          = SelectField(
                        validators=[subnet])
    vmAddress         = StringField(validators=[Optional(),IPAddress('IP inválida'),ip_address])
    vmMacAddress      = StringField(validators=[Optional()])
    # Matriz de datos para vlans
    vmNic0Vlan        = SelectField(validators=[subnet])
    vmNic1Vlan        = SelectField(validators=[subnet])
    vmNic2Vlan        = SelectField(validators=[subnet])
    vmNic0Ip          = StringField(validators=[Optional(),IPAddress('IP inválida'),ip_address])
    vmNic1Ip          = StringField(validators=[Optional(),IPAddress('IP inválida'),ip_address])
    vmNic2Ip          = StringField(validators=[Optional(),IPAddress('IP inválida'),ip_address])
    vmNic0Mac         = StringField(validators=[Optional()])
    vmNic1Mac         = StringField(validators=[Optional()])
    vmNic2Mac         = StringField(validators=[Optional()])
    #                 --------------------------------------------------
    vmUsername        = StringField()
    vmPassword        = StringField()
    # Backup sets
    vmBackUpSet1      = IntegerField()
    vmBackUpSet2      = IntegerField()
    vmBackUpSet3      = IntegerField()
    # Flags
    vmDRP             = BooleanField()         
    vmCDROM           = BooleanField()      
    # Request text field (falta guardarlo en BD)
    vmRequestText     = StringField()
    # Buttons ----------------------------------------------------------
    submit_Guardar    = SubmitField ('Guardar')
    submit_Completado = SubmitField ('Completado')
    submit_Eliminar   = SubmitField ('Eliminar')
    submit_Cancelar   = SubmitField ('Cancelar')
    submit_Rechazar   = SubmitField ('Rechazar')
    submit_Aprobar    = SubmitField ('Aprobar')
    submit_Retorno    = SubmitField ('Retorno')
    # Validation data, hidden fields -----------------------------------
    # List of valid subnet ranges should be filled in runtime
    #GV 20210317 vmSubnetRange     = None
    vmData            = {}
    # Interface only fields, this is volatile data
    vmDebug           = BooleanField()
    vmMessage1        = None
    vmMessage2        = None
    vmMessage3        = None
    # list used for subnet duplicity validation
    vmSubnetKeys      = []
    # ------------------------------------------------------------------
    
