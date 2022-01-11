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

"""
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
                                raise ValidationError(f'Tamaño Mínimo es {ImageFieldSize} GB') 
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
            raise ValidationError(f"MV '{form.vmName.data}' ya existe.")
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
                     raise ValidationError(f"{this()}:  IP '{field.data}' fuera de rango")                 
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
"""
class frm_migration_01(Form):
    mgId         = 0
    mgName       = SelectField (
                        validators=[InputRequired('Se requiere Nombre de Grupo')],coerce=int)
    mgOrigin     = SelectField (
                        validators=[InputRequired('Se requiere Cluster de origen')],coerce=str)
    mgDestiny    = SelectField (
                        validators=[InputRequired('Se requiere Cluster de destino')],coerce=str)

    mgVms        = []
    
    mgOriginVms  = SelectField (validators=[],coerce=str)
    
    mgData       = None
    mgNewName    = StringField ('MG New Name',
                        validators=[],
                        default=''
                    )

    mgNewId      = IntegerField()
    
    # ------------------------------------------------------------------
    # Buttons ----------------------------------------------------------
    submit_Crear    = SubmitField ('Crear')
    submit_Agregar  = SubmitField ('Agregar')
    submit_Clonar   = SubmitField ('Clonar')
    submit_Salvar   = SubmitField ('Salvar')
    submit_Eliminar = SubmitField ('Eliminar')
    submit_Cancelar = SubmitField ('Cancelar')
    submit_Validar  = SubmitField ('Validar')
    submit_Migrar   = SubmitField ('Migrar')

