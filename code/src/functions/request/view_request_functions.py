# ======================================================================
# BUTLER REQUEST FUNCTIONS
# (c) Sertechno 2020
# GLVH @ 2020-12-31
# ======================================================================

# Templates will reside on view_request_template.py

# Support functions
import copy

from emtec.butler.functions import *

# View functions        

# receives a code or Id and returns cost center object
def get_cost_center(code):
    cc = None
    try:
        if code is not None:
            if type(code) == int:
                cc = db.session.query(
                        Cost_Centers
                        ).filter(Cost_Centers.CC_Id==code
                        ).one_or_none()
            elif type(code) == str:
                cc = db.session.query(
                        Cost_Centers
                        ).filter(Cost_Centers.CC_Code==code
                        ).one_or_none()
    except Exception as e:
        logger.error(f"{this()} CC '{code} not found exception: {str(e)}'")
    return cc
    
# get cost centers uses codes NOT ids
def get_cost_centers(CC_TOP=None):
    cc_list = []
    print(f"{this()}: CC_TOP={CC_TOP} {type(CC_TOP)}")
    try:
        if type(CC_TOP) == str:            
        #f CC_TOP is not None:            
            query = db.session.query(
                        Cost_Centers
                        ).filter(Cost_Centers.CC_Parent_Code==CC_TOP)
            logger.debug(f"{this()}: query = {query}")
            print(f"{this()}: query = {query}")
            result = query.all()
            for row in result:
                # Load Top Cost Center if found (should be only 1)
                cc_list.append((row.CC_Id,row.CC_Code,row.CC_Description))
                children = db.session.query(
                            Cost_Centers
                            ).filter(Cost_Centers.CC_Parent_Code == row.CC_Code
                            ).all()
                for child in children:
                    cc_list.append((child.CC_Id,child.CC_Code,child.CC_Description))
                    # Recursive call to get deeper CCs
                    cc_list = cc_list + get_cost_centers(child.CC_Parent_Code)
            cc_list=unique_list(cc_list)
        # Returns a list of tuples with unique (Id,Code,Description)
        logger.trace(f"{this()}: {pformat(cc_list)}")
    except Exception as e:
        logger.error(f"{this()}: {len(cc_list)} CCs in list")        
        emtec_handle_general_exception(e,fp=sys.stderr)
    return cc_list    

def get_cost_centers_fast(CC_TOP,maximum=9999999999):
    cc_list = []
    try:
        result = db.session.query(
                    Cost_Centers
                    ).filter(Cost_Centers.CC_Id>CC_TOP
                    ).filter(Cost_Centers.CC_Id<maximum
                    ).all()
        for row in result:
            # Load Top Cost Center if found (should be only 1)
            cc_list.append((row.CC_Id,row.CC_Code,row.CC_Description,row.CC_Parent_Code))
        #cc_list=unique_list(cc_list)
        # Returns a list of tuples with unique (Id,Code,Description)
        logger.trace(f"{this()}: {pformat(cc_list)}")
    except Exception as e:
        logger.error(f"{this()}: {len(cc_list)} CCs in list")        
        emtec_handle_general_exception(e,fp=sys.stderr)
    logger.debug(f"{this()}: {len(cc_list)} CCs in list")        
    return cc_list    

""" --------------------------------------------------------------------
==>  13 corporativo CC_Code%30000000 != 0 and CC_Code%10000 == 0
==>  37 gerencias   CC_Code%30000000 != 0 and CC_Code%10000 != 0 and CC_Code%100 == 0 
==> 555 .........   CC_Code%30000000 != 0 and CC_Code%10000 != 0 and CC_Code%100 != 0 
==> 185 ambientes   CC_Code%30000000 != 0 and CC_Code%10000 != 0 and CC_Code%100 != 0 and CC_Code%10 == 0
==> 370 discos      CC_Code%30000000 != 0 and CC_Code%10000 != 0 and CC_Code%100 != 0 and CC_Code%10 != 0
    605 CCs
-------------------------------------------------------------------- """
# Corporativo
def get_corporate_list(top_cost_center_code,ccs=None):
    # Cost Center options need to be refreshed from Collector ----------
    # These need to come from Collector Cost Centers
    # Gets all depending cost centers and returns module 100 '00' in
    # list -------------------------------------------------------------
    corporate_list = []
    logger.debug(f"{this()}: top_cost_center_code={top_cost_center_code}")
    if ccs is None:
        ccs = get_cost_centers(top_cost_center_code)
    logger.debug(f"{this()}: {len(ccs)} CCs found below {top_cost_center_code}")
    for cc in ccs:
        code = int(cc[1])
        if code > int(top_cost_center_code) and code%10000 == 0:
            corporate_list.append([cc[0],cc[2]])
    logger.trace(f"{this()}: {pformat(corporate_list)}")
    logger.debug(f"{this()}: {len(corporate_list)} CCs Corporate")
    return corporate_list

# Gerencias
def get_department_list(top_cost_center_code,ccs=None):
    # Cost Center options need to be refreshed from Collector ----------
    # These need to come from Collector Cost Centers
    # Gets all depending cost centers and returns module 100 '00' in
    # list -------------------------------------------------------------
    department_list = []
    gd_map = {}
    logger.debug(f"{this()}: top_cost_center_code={top_cost_center_code}")
    if ccs is None:
        ccs = get_cost_centers(top_cost_center_code)
    logger.debug(f"{this()}: {len(ccs)} CCs found below {top_cost_center_code}")
    for cc in ccs:
        #f cc[0]> top_cost_center_code and cc[0]%10000 != 0 and cc[0]%10000:
        code = int(cc[1])
        if code > int(top_cost_center_code) and code%10000 != 0 and code%100 == 0:
            department_list.append([cc[0],cc[2]])
            gd_map.update({cc[0]:{'code':cc[1],'description':cc[2],'corporate':cc[3],}})
    logger.trace(f"{this()}: {pformat(department_list)}")
    logger.debug(f"{this()}: {len(department_list)} CCs Gerencias")
    return department_list,gd_map

#==> 185 ambientes   CC_Code%30000000 != 0 and CC_Code%10000 != 0 and CC_Code%100 != 0 and CC_Code%10 == 0
def get_cc_list(top_cost_center_code,ccs=None):
    # Cost Center options need to be refreshed from Collector ----------
    # These need to come from Collector Cost Centers
    # Gets all depending cost centers and returns module 100 '00' in
    # list -------------------------------------------------------------
    cc_list = []
    logger.debug(f"{this()}: top_cost_center_code={top_cost_center_code}")
    if ccs is None:
        ccs = get_cost_centers(top_cost_center_code)
    logger.debug(f"{this()}: {len(ccs)} CCs found below {top_cost_center_code}")
    for cc in ccs:
        # 20210401 ccid = cc[0]%top_cost_center_code
        #f cc[0] != top_cost_center_code and ccid < 10000 and cc[0]%100 == 0:
        code = int(cc[1])
        ccid = code%int(top_cost_center_code)
        if code != int(top_cost_center_code) and ccid<100 != 0 and ccid%10 == 0 :
            cc_list.append([cc[0],cc[2]])
    logger.trace(f"{this()}: {pformat(cc_list)}")
    logger.debug(f"{this()}: {len(cc_list)} CCs Ambientes")
    return cc_list

# Tipos de Discos 
def get_type_list(top_cost_center_code,ccs=None):
    # Cost Center options need to be refreshed from Collector ----------
    # These need to come from Collector Cost Centers
    # Gets all depending cost centers and returns module 100 '00' in
    # list -------------------------------------------------------------

    # Codigo omitido temporalmente elimnar hardcode luego
    ctype_list = []
    logger.debug(f"{this()}: top_cost_center_code={top_cost_center_code}")
    if ccs is None:
        ccs = get_cost_centers(top_cost_center_code)
    else:
        logger.debug(f"{this()}: ccs ={len(ccs)}")
    logger.debug(f"{this()}: {len(ccs)} CCs found below {top_cost_center_code}")
    for cc in ccs:
        if int(cc[1]) % int(top_cost_center_code) < 10 :
            ctype_list.append([cc[0],cc[2]])
    logger.trace(f"{this()}: {pformat(ctype_list)}")
    logger.debug(f"{this()}: {len(ctype_list)} CCs Tipos de discos")
    return ctype_list
#    ==> 370 discos      CC_Code%30000000 != 0 and CC_Code%10000 != 0 and CC_Code%100 != 0 and CC_Code%10 != 0
        
def get_image_list():
    # List of images need to be refreshed from Nutanix Cluster ---------
    # These need to come from Nutanix Images
    # and updated in local Table
    image_list =  db.session.query(Nutanix_VM_Images).all()
    logger.trace(f"{this()}: {pformat(image_list)}")
    return image_list

def get_disk_image_list():
    # List of images need to be refreshed from Nutanix Cluster ---------
    # These need to come from Nutanix Images
    # and updated in local Table
    image_list =  db.session.query(Disk_Images).all()
    logger.trace(f"{this()}: {pformat(image_list)}")
    return image_list

def get_cluster_list():
    # List of clusters need to be refreshed from Nutanix ---------------
    # These need to come from Nutanix 
    # and updated in local Table
    cluster_list = []
    clusters =  db.session.query(Clusters).all()
    for cluster in clusters:
        if cluster.cluster_uuid not in ['','0',None]:
            cluster_list.append((cluster.cluster_uuid,cluster.cluster_name))
    logger.trace(f"{this()}: {pformat(cluster_list)}")
    return cluster_list

def get_project_list():
    # List of projects need to be refreshed from Nutanix ---------------
    # These need to come from Nutanix 
    # and updated in local Table
    project_list = []
    projects =  db.session.query(Projects).all()
    for project in projects:
        project_list.append((project.project_uuid,project.project_name))
    logger.trace(f"{this()}: {pformat(project_list)}")
    return project_list

def get_category_list():
    # List of categories need to be refreshed from Nutanix Cluster -----
    # These need to come from Nutanix Images
    # and updated in local Table
    category_list = []
    categories =  db.session.query(Categories).all()
    for category in categories:
        category_list.append((category.category_name,category.category_description))
    logger.trace(f"{this()}: {pformat(category_list)}")
    return category_list

def get_subnet_list():
    # List of subnets need to be refreshed from Nutanix Cluster --------
    # These need to come from Nutanix Images
    # and updated in local Table
    subnet_list = []
    subnets =  db.session.query(Subnets).all()

    for subnet in subnets:
        subnet_list.append([subnet.get_dict()])
    logger.trace(f"{this()}: {pformat(subnet_list)}")
    return subnet_list

def get_subnet_name(uuid,subnet_list):
    logger.warning(f"{this()}: uuid = {uuid}")
    name = ''
    for subnet in subnet_list:
        if subnet[0] == uuid:
            name = subnet[1]
    logger.warning(f"{this()}: name = {name}")    
    return name

def get_cluster_uuid(data,cluster_name):
    for uuid,name in data.get('clusters'):
        if name == cluster_name:
            return uuid
    return None
    
def get_cluster_name(data,cluster_uuid):
    for uuid,name in data.get('clusters'):
        if uuid == cluster_uuid:
            return name
    return None
    
def get_project_uuid(data,project_name):
    for uuid,name in data.get('projects'):
        if name == project_name:
            return uuid
    return None

def get_category_description(data,category_name):
    for name,description in data.get('categories'):
        if name == category_name:
            return description
    return None

def get_environment_code(data,environment_name):
    logger.debug(f"{this()}: environment={environment_name} {data.get('ccs')}")
    for code,name in data.get('ccs'):
        logger.debug(f"{this()}: code={code} name={name}")
        if name == environment_name:
            return code
    return None

def get_environment_name(data,environment_code):
    logger.debug(f"{this()}: environment={environment_code} {data.get('ccs')}")
    for code,name in data.get('ccs'):
        logger.debug(f"{this()}: code={code} name={name}")
        if code == environment_code:
            return name
    return None
    
def get_environments(filename,data):
    environments = None
    logger.debug(f"{this()}: In filename={filename}")
    try:
        with open(filename,'r') as fp:
            environments = json.load(fp)
        logger.debug(f"{this()}: environments = {environments.keys()}")
        for e in environments.keys():
            environment = environments.get(e)
            logger.debug(f"{this()}: environment '{e}' clusters = {environment.keys()}")
            try:
                for c in environment.keys():
                    cluster_uuid     = get_cluster_uuid(data,c)
                    environment_code = get_environment_code(data,e)
                    environments[e][c].update({'uuid':cluster_uuid})
                    environments[e][c].update({'environment':environment_code})
                    if cluster_uuid is not None:
                        try:
                            logger.debug(f"{this()}: environment '{e}' cluster = {c}")
                            cluster = environment[c]
                            project_name         = cluster['project'].get('name')
                            category_name        = cluster['category'].get('name')
                            project_uuid         = get_project_uuid(data,project_name)
                            category_description = get_category_description(data,category_name)
                            environments[e][c]['project'].update({'uuid':project_uuid})
                            environments[e][c]['category'].update({'description':category_description})
                        except Exception as e:
                            logger.warning(f"{this()}: environment '{e}' cluster = {c} {str(e)}")
                    else:
                            logger.warning(f"{this()}: environment '{e}' cluster = {c} INVALID")                        
            except Exception as e:
                logger.error(f"{this()}: environment '{e}' cluster = {c} {str(e)}")
    except Exception as e:
        logger.critical(f"INVALID ENVIRONMENTS: filename={filename} exception: {str(e)}")
    return environments
    
def get_environments_codes(data,environments):
    logger.debug(f"{this()}: In")
    E={}
    try:
        logger.debug(f"{this()}: environments = {environments.keys()}")
        for e in environments.keys():
            environment_code = get_environment_code(data,e) 
            E.update({environment_code:{}})
            environment = environments.get(e)
            logger.debug(f"{this()}: environment '{e}' clusters = {environment.keys()}")
            try:
                for c in environment.keys():
                    cluster = environment[c]
                    cluster_uuid = get_cluster_uuid(data,c)
                    if cluster_uuid is not None:
                        E[environment_code].update({
                            cluster_uuid:{
                                'project' : get_project_uuid(data,cluster['project'].get('name')),
                                'category': cluster['category'].get('name'),
                                'project_name' : cluster['project'].get('name'),
                                'category_description': cluster['category'].get('description')
                            }
                        })
            except Exception as e:
                logger.error(f"{this()}: environment '{e}' cluster = {c} {str(e)}")
    except Exception as e:
        logger.critical(f"INVALID ENVIRONMENTS: exception: {str(e)}")
    return E
    
def get_environment_attributes(data,environment=None,cluster=None,code=None,uuid=None):
    if environment is None:
        environment = get_environment_name(data,code)
    if cluster is None:
        environment = get_cluster_name(data,uuid)
        
    cluster = data.get('environments').get('environment').get('cluster')
    project_uuid  = cluster.get('project').get('uuid')
    category_name = cluster.get('category').get('name')
    return project_uuid,category_name
    
def get_project_subnet_list():
    # List of subnets need to be refreshed from Nutanix Cluster --------
    # These need to come from Nutanix Images
    # and updated in local Table
    projects =  db.session.query(Projects).all()
    subnet_list = []
    for project in projects:
        subnets = []
        for project_subnet in project.project_subnets.split(','):
            try:
                if project_subnet not in ['','0',None]:
                    uuid,name=project_subnet.split(':')
                    # Load valid subnet pairs only
                    if uuid not in ['','0',None] and name not in ['','0',None]:
                        subnets.append([f'{uuid}:{project.project_uuid}',f'{name}'])
            except Exception as e:
                emtec_handle_general_exception(e,logger=logger)
        if len(subnets):
            # load valid subnets sublists only
            # since will be exploited with NodeJS thet list of lists is required
            subnet_list.append(
                [   project.project_name,
                    subnets
                ]
        )
    logger.trace(f"{this()}: {pformat(subnet_list)}")
    return subnet_list

def get_project_subnet_options():
    # List of subnets need to be refreshed from Nutanix Cluster --------
    # These need to come from Nutanix Images
    # and updated in local Table
    projects =  db.session.query(Projects).all()
    subnet_list = []
    for project in projects:
        subnets = []
        for project_subnet in project.project_subnets.split(','):
            try:
                if project_subnet not in ['','0',None]:
                    uuid,name=project_subnet.split(':')
                    # Load valid subnet pairs only
                    if uuid not in ['','0',None] and name not in ['','0',None]:
                        subnets.append([f'{uuid}',f'{name} @ {project.project_name}'])
            except Exception as e:
                emtec_handle_general_exception(e,logger=logger)
        if len(subnets):
            # load valid subnets sublists only
            # since will be exploited with NodeJS thet list of lists is required
            subnet_list.append(
                [   project.project_uuid,
                    subnets
                ]
        )
    logger.trace(f"{this()}: {pformat(subnet_list)}")
    return subnet_list

def get_user_list():
    # List of user need to be refreshed from Nutanix Cluster -----------
    # These need to come from Nutanix Images
    # and updated in local Table
    user_list = []
    users =  db.session.query(Users).all()
    for user in users:
        user_list.append((user.id,user.username))
    logger.trace(f"{this()}: {pformat(user_list)}")
    return user_list

def get_rates(margin=1,CC_Id=1):
    # Cost Centers related to Storage types ----------------------------
    # These need to come from Collector Cost Centers
    logger.debug(f"{this()}: cc={CC_Id} and a margin of {margin}") 
    rates = {}
    try:
        dsk_rate = 0
        rows = db.session.query(Rates).all()
        # Load Rates and margin factor
        for row in rows:
            logger.trace(f"row={row.Rat_Id} {row.Typ_Code} {row.Rat_Price} {row.CC_Id}")
            if row.Typ_Code == 'NUL':
                # Gets Margin Factor from scepcial NUL type rate
                margin = 1 + row.Rat_Price
            else:
                # Sets Rate to Monthly value
                if row.Rat_Period == 1:         # Hourly
                    rates.update({ row.Typ_Code:row.Rat_Price * 720 })
                elif row.Rat_Period == 2:       # Daily
                    rates.update({ row.Typ_Code:row.Rat_Price * 30 })
                else:
                    rates.update({ row.Typ_Code:row.Rat_Price })
                # Setup rate as per disk type
                if row.Typ_Code == 'DSK': # and row.CC_Id == CC_Id:
                    dsk_type = 'DSK'
                    if  row.CC_Id == CC_Id and row.CC_Id%10 == 1:
                        logger.debug(f'{this()}: {row.Typ_Code} {row.CC_Id} {CC_Id} -> DSK=*1 -> HDD')
                        rates.update({ 'HDD': rates[row.Typ_Code] })
                        dsk_rate = rates[row.Typ_Code]
                    elif  row.CC_Id == CC_Id and row.CC_Id%10 == 2:
                        logger.debug(f'{this()}: {row.Typ_Code} {row.CC_Id} {CC_Id} -> DSK=*2 -> SSD')
                        rates.update({ 'SSD'   : rates[row.Typ_Code] })
                        dsk_rate = rates[row.Typ_Code]
        if dsk_rate == 0:
            logger.error(f"{this()}: dsk_rate = {dsk_rate} No Disk Rate found for CC Id = {CC_Id}")
        rates.update({ 'DSK'   : dsk_rate })
        # adjust rates to estimate billing rate, applies margin factor
        for rate in rates:
            rates[rate] *= margin
        logger.debug(f"{this()}: \n{pformat(rates)}")
    except Exception as e:
        logger.error(f"{this()}: {str(e)}")
    return rates

def get_db_rates(margin=1):
    # Cost Centers related to Storage types ----------------------------
    # These need to come from Collector Cost Centers
    logger.debug(f"{this()}: loading rates for all CCs and a margin of {margin}") 
    rows = db.session.query(Rates).all()
    rates = {}
    # Load Rates and margin factor
    for row in rows:
        if row.Typ_Code == 'NUL':
            # Gets Margin Factor from scepcial NUL type rate
            margin = 1 + row.Rat_Price
        else:
            # Sets Rate to Monthly value
            if row.Rat_Period == 1:         # Hourly
                rates.update({ f'{row.Typ_Code}:{row.CC_Id}':row.Rat_Price * 720 })
            elif row.Rat_Period == 2:       # Daily
                rates.update({ f'{row.Typ_Code}:{row.CC_Id}':row.Rat_Price * 30 })
            else:
                rates.update({ f'{row.Typ_Code}:{row.CC_Id}':row.Rat_Price })
    # adjust rates to estimate billing rate, applies margin factor
    for rate in rates:
        rates[rate] *= margin
    logger.trace(f"{this()}: {len(rates)} rates loaded")
    logger.trace(f"{this()}: {pformat(rates)}")
    return rates

def get_monthly_rate(row,rox):
    logger.debug(f"{this()}: Enter")
    try:
        storage = 0
        # CC_Id need to be built
        rates = get_rates(CC_Id=row.CC_Id)
        logger.debug(f"{this()}: rates={rates}")
        logger.debug(f"{this()}: row.CC_Id     = {row.CC_Id}")
        logger.debug(f"{this()}: rox.disk_type = {rox.disk_type}")
        for i in range(12):
            storage += getattr(rox,f'disk_{i}_size')            
        cpu = rox.vcpus_per_socket * rox.num_sockets * rates['CPU']
        ram = rox.memory_size_gib * rates['RAM']
        dsk = storage * rates['DSK']
        '''
        try:
            if rox.disk_type%100 in [11,12,13]:
                storage_type = ['HDD','SSD','HYB'][rox.disk_type%100-11]
                dsk = storage * rates[storage_type]
            else:
                dsk = 0
        
        except Exception as e:
            logger.error(f'{this()}: excepcion = {str(e)}')
            dsk = 0
        
        logger.debug(f"{this()}: storage_type = {storage_type}")
        '''
        logger.debug(f"{this()}: cpu          = {cpu:15.10f} UF <= {rox.vcpus_per_socket*rox.num_sockets:4.0f}    x {rates['CPU']:.10f}")
        logger.debug(f"{this()}: ram          = {ram:15.10f} UF <= {rox.memory_size_gib:4.0f} GB x {rates['RAM']:.10f}")
        #ogger.debug(f"{this()}: dsk          = {dsk:15.10f} UF <= {storage:4.0f} GB x {rates[storage_type]:.10f}")
        logger.debug(f"{this()}: dsk          = {dsk:15.10f} UF <= {storage:4.0f} GB x {rates['DSK']:.10f}")
        logger.debug(f"{this()}: month        = {cpu+ram+dsk:15.10f} UF")
        return cpu + ram + dsk
    except Exception as e:
        logger.warning(f"{this()}: exception {str(e)}")
        return 0

""" def get_description(tabla,codigo,data):
    ''' Gets description for a table based system '''
    logger.debug(f'{this()}: tabla={tabla} codigo={codigo}')
    descripcion=''
    try:
        # lists of tuples: [(codigo,descripcion),...]
        if tabla in ['clusters','projects','categories','users','departments','ccs','types']:
            for item in data[tabla]:
                if item[0] == codigo: 
                    descripcion=item[1]
                    break
        # list of subnets (dictionaries)
        elif tabla=='subnets':
            for subnets_list in data['subnets']:
                for subnet in subnets_list:
                    if subnet['uuid'] == codigo: 
                        descripcion=subnet['name']
                        break                    
        elif tabla=='images':
            for image in data['images']:
                if image.uuid == codigo:
                    descripcion = image.name
                    break                    
    except Exception as e:
        logger.error(f"{this()}: exception: {str(e)}")
    logger.debug(f"{this()}: return descripcion = '{descripcion}'")
    return descripcion
"""    

""" def get_vm_resume(vm):    
    cpu=ram=dsk=tip=None
    if vm is not None:
        cpu = vm.num_sockets * vm.vcpus_per_socket
        ram = vm.memory_size_gib
        dsk = 0
        for i in range(12):
            dsk += getattr(vm,f'disk_{i}_size')
        # Tipos durante desarrollo
        if vm.disk_type%100 in [0,1,2]:
            tip = ['HDD','SSD','HYB'][vm.disk_type%100]
        # Tipos con codigo forzados ver funcion get_stype_list()
        elif vm.disk_type%100 in [11,12,13]:
            tip = ['HDD','SSD','HYB'][vm.disk_type%100-11]
        else:
            tip = None
    return f"{cpu} CPU x {ram} GB x {dsk} GB {tip}"
"""

def notify_request(Id,subject_detail=None,data=None,recipients=None):
    logger.debug(f'{this()}:Enter')
    from    flask_mail          import Message
    if current_app.config['BUTLER_REQUEST_NOTIFICATIONS']:
        try:
            subject = f"{current_app.config['BUTLER_MAIL_SUBJECT_PREFIX']}: Solicitud # {Id}"
            if subject_detail is not None:
                subject = f'{subject}. {subject_detail}'
            sender = current_app.config['BUTLER_MAIL_SENDER']
            # Look for Requets's user's ids
            # row = requests.query.filter(requests.Id == Id).one()
            row = db.session.query(Requests).filter(Requests.Id == Id).one()
            # Look for all possible email recipients
            if recipients is None:
                rows = User.query.filter(
                            User.id.in_(
                                [   row.User_Id,
                                    row.Approver_Id,
                                    current_user.id
                                ]
                            )
                            ).filter(User.email.isnot(None)
                            ).all()
                recipients = []
                for row in rows:
                    recipients.append(row.email)
            # simplify list
            recipients = unique_list(recipients)
            logger.debug(f"{this()}: recipients = {recipients}")
            if len(recipients):
                msg = Message(  subject, sender = sender, recipients = recipients )
                logger.trace(f"{this()}: msg = {msg}")
                # HTML body
                logger.warning(f'{this()}: calling output request(Id={Id})')
                html = output_Request(Id,data=data).encode("ascii","xmlcharrefreplace")
                logger.trace(f'{this()}: html = {html}')
                msg.html = html
                logger.warning(f'{this()}: queueing email for request {Id} ...')
                mail.send(msg)
                logger.warning(f'{this()}: email queued  for request {Id}.')
        except Exception as e:
            emtec_handle_general_exception(e,logger=logger)
            flash(f'{this()}: Excepción: Solicitud: {Id}: {str(e)}')
    else:
        if current_app.config['DEBUG']:
            logger.warning(f'{this()}: Notificaciones deshabilitadas')
    logger.debug(f'{this()}: OUT')
    # ------------------------------------------------------------------

def dump_form(form):
    logger.debug(f'{this()}: form {form}')
    try:
        logger.debug(f'form.submit_Guardar.data    = {form.submit_Guardar.data}')
        logger.debug(f'form.submit_Retorno.data    = {form.submit_Retorno.data}')
        logger.debug(f'form.submit_Completado.data = {form.submit_Completado.data}')
        logger.debug(f'form.submit_Cancelar.data   = {form.submit_Cancelar.data}')
        logger.debug(f'form.submit_Aprobar.data    = {form.submit_Aprobar.data}')
        logger.debug(f'form.submit_Rechazar.data   = {form.submit_Rechazar.data}')
        logger.debug(f'form.submit_Retorno.data    = {form.submit_Retorno.data}')
        logger.debug(f'form.vmName                 = {form.vmName.data}')
        logger.debug(f'form.vmCPU                  = {form.vmCPU.data}')
        logger.debug(f'form.vmRAM                  = {form.vmRAM.data}')
        logger.debug(f'form.vmType                 = {form.vmType.data}')
        logger.debug(f'form.vmCC                   = {form.vmCC.data}')
        logger.debug(f'form.vmStatus               = {form.vmStatus.data}')
        for i in range(12):
            logger.debug(f"form.vmDisk{i}Size          = '{getattr(form,f'vmDisk{i}Size').data}' '{getattr(form,f'vmDisk{i}Image').data}'")
    except Exception as e:
        emtec_handle_general_exception(e,logger=logger)
    logger.debug(f'------------------------------------------------------')

def get_range_list(range_list):
    list_of_ranges=[]
    try:
        if type(range_list) == list:
            for i in range(len(range_list)):
                start,end = range_list[i].split(' ')
                start = start.split('.')
                end   = end.split('.')
                s=e=0
                if len(start) == 4 and len(end) == 4:
                    ok = True
                    # Check for range validity
                    for k in range(3):
                        if start[k] != end[k]: ok = False
                    if ok:
                        list_of_ranges.append((ip_to_int(start),ip_to_int(end)))
        else:
            list_of_ranges=[]
    except Exception as e:
        emtec_handle_general_exception(e,logger=logger,fp=sys.stderr)
    return list_of_ranges

def calculate_form(form,row,rox):
    logger.debug(f"{this()}: Enter")
    try:
        # Copy actual DB values into temp buffers
        tmp_row = copy.copy(row)
        tmp_rox = copy.copy(rox)
        # CC_Id need to be rebuild upon actual form data
        logger.debug(f"{this()}: top:{form.vmTopCC} co: {form.vmCorporate.data} dd:{form.vmDepartment.data} cc:{form.vmCC.data} tt:{form.vmType.data}")
        tmp_row.CC_Id = form.vmTopCC + form.vmCorporate.data%form.vmTopCC + form.vmDepartment.data%form.vmTopCC + form.vmCC.data%form.vmTopCC +form.vmType.data%form.vmTopCC
        logger.debug(f"{this()}: db CC = old {row.CC_Id} now {form.vmCorporate.data}+{form.vmDepartment.data}+{form.vmCC.data}+{form.vmType.data}-> {tmp_row.CC_Id}")
        # Save actual form values into temporary buffers
        save_form(form,tmp_row,tmp_rox)
        logger.debug(f"{this()}: now form CC = {tmp_row.CC_Id}")
        # Calculate form values upon temporary buffers
        form.vmData.update({'storage': 0})
        form.vmData.update({'month'  : 0})
        logger.debug(f"{this()}: form.vmData['month'] = {form.vmData['month']}")
        for i in range(12):
            form.vmData['storage'] += getattr(form,f'vmDisk{i}Size').data
        form.vmData.update({'month':get_monthly_rate(tmp_row,tmp_rox)})
        logger.debug(f"{this()}: form.vmData['storage'] = {form.vmData.get('storage',0)}")
        logger.debug(f"{this()}: form.vmData['month']   = {form.vmData.get('month',0)}")
    except Exception as e:
        logger.error(f"{this()}: {str(e)}")
        #emtec_handle_general_exception(e,logger=logger)
    logger.debug(f"{this()}: Exit")
        
def load_form(form,row,rox):
    logger.warning(f'{this()}: Enter. loading form from DB data ...')
    try:
        if rox.vm_name is None or str(rox.vm_name)== 'None':
            rox.vm_name = ''
        form.vmName.data = rox.vm_name 
        if str(form.vmName.data) == 'None':
            form.vmName.data = ''
        form.vmCPS.data     = rox.vcpus_per_socket
        form.vmSockets.data = rox.num_sockets
        form.vmCPU          = rox.num_sockets * rox.vcpus_per_socket
        form.vmRAM.data     = rox.memory_size_gib
        # row.CC_Id is a compound code need to be deconstructed here
        # rule is vmType is >=1 <100
        if row.CC_Id is not None:
            disk_type   = row.CC_Id % 10
            environment = row.CC_Id % 100 - disk_type
            management  = row.CC_Id % 10000 - environment - disk_type
            corporate   = row.CC_Id % 1000000 - management - environment - disk_type
            form.vmType.data       = form.vmTopCC + disk_type
            form.vmCC.data         = form.vmTopCC + environment
            form.vmDepartment.data = form.vmTopCC + management
            form.vmCorporate.data  = form.vmTopCC + corporate
            logger.debug(f"{this()}: top:{form.vmTopCC} co:{form.vmCorporate.data} dd:{form.vmDepartment.data} cc:{form.vmCC.data} tt:{form.vmType.data}")
        form.vmStatus.data   = row.Status
        for i in range(12):
            getattr(form,f'vmDisk{i}Size').data  = getattr(rox,f'disk_{i}_size')
            if i == 0: 
                getattr(form,f'vmDisk{i}Image').data = getattr(rox,f'disk_{i}_image') 
        calculate_form(form,row,rox)
        logger.debug(f"{this()}: form.vmData['month']   = {form.vmData.get('month',None)}")
        logger.debug(f"{this()}: form.vmData['storage'] = {form.vmData.get('storage',None)}")
        # Extra Fields
        # Ownership
        form.vmCluster.data     = rox.cluster_uuid
        form.vmProject.data     = rox.project_uuid
        form.vmCategory.data    = rox.category_name
        form.vmUsername.data    = rox.vm_username
        form.vmPassword.data    = rox.vm_password
        # Array of Backup sets
        form.vmBackUpSet1.data  = rox.backup_set_1
        form.vmBackUpSet2.data  = rox.backup_set_2
        form.vmBackUpSet3.data  = rox.backup_set_3
        # Flags
        form.vmCDROM.data       = rox.vm_cdrom
        form.vmDRP.data         = rox.vm_drp
        form.vmDRPRemote.data   = rox.vm_drp_remote
        
        # Fix some initial values --------------------------------------
        # networking
        # Populate Subnets data
        subnet_list = []
        for project in get_project_subnet_options():
            if project[0] == rox.project_uuid:
                subnet_list = project[1]
        pprint(subnet_list)
        # populates list of selected vlans
        selected_list = []
        if rox.nic_0_vlan  is not None: selected_list.append(rox.nic_0_vlan)
        if rox.nic_1_vlan  is not None: selected_list.append(rox.nic_1_vlan)
        if rox.nic_2_vlan  is not None: selected_list.append(rox.nic_2_vlan)
        if rox.nic_3_vlan  is not None: selected_list.append(rox.nic_3_vlan)
        pprint(selected_list)
        for i in range(4):
            if i < len(subnet_list):
                uuid,name = subnet_list[i]
            else:
                uuid,name = ['','']
            flag = True if uuid in selected_list else False
            print(f"getattr(form,f'vmVlan{i}Selected.').data={getattr(form,f'vmVlan{i}Selected').data} {flag}")
            getattr(form,f'vmVlan{i}Name').data     = name
            getattr(form,f'vmVlan{i}Selected').data = flag                
            getattr(form,f'vmVlan{i}Uuid').data     = uuid                
            print(f"getattr(form,f'vmVlan{i}Selected').data={getattr(form,f'vmVlan{i}Selected').data} {flag}")
            logger.warning(f"{this()}: name: {name} uuid: {uuid} flag: {flag}")
            logger.warning(f"{this()}: form.vmVlan{i}Name = {getattr(form,f'vmVlan{i}Name')}")
            logger.warning(f"{this()}: form.vmVlan{i}Uuid = {getattr(form,f'vmVlan{i}Uuid')}")
            logger.warning(f"{this()}: form.vmVlan{i}Sele = {getattr(form,f'vmVlan{i}Selected')}")
        
        if form.vmDRP.data is None:
            form.vmDRP.data = False
            logger.debug(f'{this()}: form.vmDRP.data adjusted to = {form.vmDRP.data}')
        if form.vmDRPRemote.data is None:
            form.vmDRPRemote.data = False
            logger.debug(f'{this()}: form.vmDRPRemote.data adjusted to = {form.vmDRPRemote.data}')
        if form.vmCDROM.data is None:
            form.vmCDROM.data = False
            logger.debug(f'{this()}: form.vmCDROM.data adjusted to = {form.vmCDROM.data}')
        form.vmRequestText.data    = rox.request_text if rox.request_text is not None else ''
        logger.debug(f"{this()}: rox.request_text        = {type(rox.request_text)} >{rox.request_text}<")
        logger.debug(f"{this()}: form.vmRequestText.data = {type(form.vmRequestText.data)} >{form.vmRequestText.data}<")
    except Exception as e:
        emtec_handle_general_exception(e,logger=logger)
    logger.debug(f'{this()}: Exit')

def save_form(form,row,rox):
    try:
        logger.warning(f'{this()}: saving form to DB records ...')
        # Identification ---------------------------------------------------
        rox.vm_name          = form.vmName.data
        #row.Status           = form.vmStatus.data
        # CC Id is a mix of distribution CC + Storage Type
        # row.CC_Id is a compound code need
        # to be deconstructed here
        # rule is vmType is >=1 <100
        # ##############################################################
        # Need to review use of CC Class instead of hardcoded calculation
        # ##############################################################
        
        disk_type   = form.vmType.data % 10
        logger.debug(f"{this()}: top:{form.vmTopCC} disk_type:{disk_type}")    
        environment = form.vmCC.data % 100
        logger.debug(f"{this()}: top:{form.vmTopCC} environment:{environment} disk_type:{disk_type}")    
        management  = form.vmDepartment.data   % 10000
        logger.debug(f"{this()}: top:{form.vmTopCC} management:{management} environment:{environment} disk_type:{disk_type}")    
        corporate   = form.vmCorporate.data % 1000000
        logger.debug(f"{this()}: top:{form.vmTopCC} corporate:{corporate} management:{management} environment:{environment} disk_type:{disk_type}")    
        row.CC_Id   = form.vmTopCC + corporate + management + environment + disk_type
        logger.debug(f"{this()}: top:{form.vmTopCC} corporate:{corporate} management:{management} environment:{environment} disk_type:{disk_type} -> {row.CC_Id}")    
        # Ownership
        rox.cluster_uuid  = form.vmCluster.data
        rox.project_uuid  = form.vmProject.data
        rox.category_name = form.vmCategory.data 
        # Specifications ---------------------------------------------------    
        rox.vcpus_per_socket = form.vmCPS.data 
        rox.num_sockets      = form.vmSockets.data 
        rox.memory_size_gib  = form.vmRAM.data
        rox.memory_size_mib  = form.vmRAM.data * 1024
        # Storage ----------------------------------------------------------
        #ox.disk_type        = form.vmType.data % 10
        rox.disk_type        = form.vmType.data
        for i in range(12):
            setattr( rox, f'disk_{i}_size' , getattr( form, f'vmDisk{i}Size').data  ) 
            if i == 0:
                setattr( rox, f'disk_{i}_image', getattr( form, f'vmDisk{i}Image').data ) 
        logger.warning(f"form.vmVlan0Selected.data={form.vmVlan0Selected.data} >{form.vmVlan0Uuid.data}< >{form.vmVlan0Name.data}<")
        logger.warning(f"form.vmVlan1Selected.data={form.vmVlan1Selected.data} >{form.vmVlan1Uuid.data}< >{form.vmVlan1Name.data}<")
        logger.warning(f"form.vmVlan2Selected.data={form.vmVlan2Selected.data} >{form.vmVlan2Uuid.data}< >{form.vmVlan2Name.data}<")
        logger.warning(f"form.vmVlan3Selected.data={form.vmVlan3Selected.data} >{form.vmVlan3Uuid.data}< >{form.vmVlan3Name.data}<")

        rox.nic_0_vlan = form.vmVlan0Uuid.data if form.vmVlan0Selected.data else None
        rox.nic_1_vlan = form.vmVlan1Uuid.data if form.vmVlan1Selected.data else None
        rox.nic_2_vlan = form.vmVlan2Uuid.data if form.vmVlan2Selected.data else None
        rox.nic_3_vlan = form.vmVlan3Uuid.data if form.vmVlan3Selected.data else None        
        # Networking      
        logger.warning(f"nic_0_vlan={rox.nic_0_vlan}")
        logger.warning(f"nic_1_vlan={rox.nic_1_vlan}")
        logger.warning(f"nic_2_vlan={rox.nic_2_vlan}")
        logger.warning(f"nic_3_vlan={rox.nic_3_vlan}")
        # Array of Backup sets
        rox.backup_set_1  = form.vmBackUpSet1.data
        rox.backup_set_2  = form.vmBackUpSet2.data
        rox.backup_set_3  = form.vmBackUpSet3.data
        # Flags
        rox.vm_drp        = form.vmDRP.data         
        rox.vm_drp_remote = form.vmDRPRemote.data         
        rox.vm_cdrom      = form.vmCDROM.data         
        # Security and other      
        rox.vm_username   = form.vmUsername.data 
        rox.vm_password   = form.vmPassword.data 
        rox.request_text  = form.vmRequestText.data 
        logger.debug(f"{this()}: Normal exit")
    except Exception as e:
        emtec_handle_general_exception(e,logger=logger)

# ======================================================================
# **********************************************************************
# NOTA Hay que ajustar esta funcion para trabajar bien con los rates !!!
# **********************************************************************
def output_Request(Id,data=None):
    import  jinja2
    logger.debug(f'{this()}: Enter')

    row=rox=None
    top_cost_center_code = data.get('top_cost_center_code')
    all_cc_list = get_cost_centers_fast(top_cost_center_code)
    logger.debug(f"all_cc_list={len(all_cc_list)} cost centers found") 
    logger.debug(f'{this()}: inicializa listas de opciones ...') 
    corporate_list         = get_corporate_list (top_cost_center_code,all_cc_list)
    department_list,gd_map = get_department_list(top_cost_center_code,all_cc_list)
    cc_list                = get_cc_list        (top_cost_center_code,all_cc_list)
    type_list              = get_type_list      (top_cost_center_code,all_cc_list)
    logger.debug(f"corporate_list ={len(corporate_list)} corporates") 
    logger.debug(f"department_list={len(department_list)} departments") 
    logger.debug(f"cc_list        ={len(cc_list)} ccs means environments in ths context") 
    logger.debug(f"type_list      ={len(type_list)} types (of disk)") 

    data.update({'corporates' :corporate_list})
    data.update({'departments':department_list})
    data.update({'ccs'        :cc_list})
    data.update({'types'      :type_list})
    data.update({'images'     :[]})

    image_list          = get_image_list()
    vmDiskImage_choices = [('','')]
    
    for image in image_list:
        vmDiskImage_choices.append(
            (image.imageservice_uuid_diskclone,
            f'{image.description} ({int(image.size_mib)/1024} GB)')
            )
        data['images'].append((image.imageservice_uuid_diskclone,image.description))
        
    
    if Id > 0:
        # GV db.session.close()
        row = db.session.query(
                Requests,
                Nutanix_Prism_VM,
                Users,
                Cost_Centers,
                Request_Type
                ).join(Nutanix_Prism_VM,Nutanix_Prism_VM.Request_Id==Requests.Id
                ).join(Users,Users.id==Requests.User_Id
                ).join(Cost_Centers,Cost_Centers.CC_Id==Requests.CC_Id
                ).join(Request_Type,Request_Type.Id==Requests.Type
                ).filter(Requests.Id == Id
                ).first()
        if row is not None:
            # GV db.session.close()
            data.update({'status_description':get_request_status_description(row[0].Status)})
            data.update({'disk_images':[]})
            data.update({'month':0})
            # Gets Monthly Rates as per Rates Table
            rates = get_rates(CC_Id=row.Requests.CC_Id)
            for i in range(1):
                uuid=getattr(row.Nutanix_Prism_VM,f'disk_{i}_image')
                name=''
                for image in vmDiskImage_choices:
                    if image[0] == uuid:
                        name = image[1]
                        break
                data['disk_images'].append(name)
                data['images'].append(name)
                
            cpu = row.Nutanix_Prism_VM.num_sockets * rates['CPU']
            ram = row.Nutanix_Prism_VM.memory_size_gib * rates['RAM']
            data['storage'] = 0
            data['storage_type'] = ''
            for i in range(12):
                data['storage'] += getattr(row.Nutanix_Prism_VM,f'disk_{i}_size')
            try:
                if row.Nutanix_Prism_VM.disk_type%10 in [1,2,3]:
                    data['storage_type'] = ['HDD','SSD','HYB'][row.Nutanix_Prism_VM.disk_type%10-1]
                    dsk = data['storage'] * rates[data['storage_type']]
                else:
                    dsk = 0
            except Exception as e:
                logger.error(f'{this()}: exception = {str(e)}')
                dsk = 0
            data['month'] = cpu + ram + dsk
        else:
            data.update({'status_description':f'ERROR: Solicitud {Id} no encontrada.'})
            data.update({'disk_images':[]})
            data.update({'month':0})
            data['disk_images'].append(None)
            data['storage'] = 0
            data['storage_type'] = ''
            data['month'] = 0
        
    # will render template and return HTML text
    current_app.jinja_env.globals.update(get_request_status_description=get_request_status_description)
    current_app.jinja_env.globals.update(get_vm_resume=get_vm_resume)
    current_app.jinja_env.globals.update(has_status=has_status)
    current_app.jinja_env.globals.update(get_description=get_description)
    current_app.jinja_env.globals.update(object_to_html_table=object_to_html_table)
    template       = current_app.jinja_env.get_template('report_request.html')
    logger.warning(f"{this()}: will render data using template: {template} from: 'report_request.html'")
    logger.warning(f"{this()}: dir template = {dir(template)}")
    logger.warning(f"{this()}: template.filename = {template.filename}")
    output         = template.render(
            data      = data,
            row       = row,
            body_only = True
            )
    logger.debug(f'{this()}: return output = {len(output)} {type(output)}')
    return output

# EOF ******************************************************************
