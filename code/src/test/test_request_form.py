from jinja2 import Template

# Cost Center options need to be refresed from Collector ---------------
cc_list=[
    (1005,'AAAA Produccion'),
    (1006,'AAAA Desarrollo'),
    (1007,'AAAA QA'),
    (1008,'AAAA Contingencia'),
]
# Cost Centers related to Storage types --------------------------------
stype_list=[
    (5,'Standard VM (SATA storage)'),
    (6,'Special  VM (SSD storage)'),
    (7,'Hybrid   VM (Hybrid storage)'),
]
# List of images need to be refresed from Nutanix Cluster --------------
image_list=[
    (0,None),
    (100,'Windows Server 2012 r3 sp 1',100),
    (192,'Centos 6 rel. 7945',60),
    (214,'Centos 7 rel. 8110',80),
    (318,'Centos 8 rel. 12345',120),
]
# ----------------------------------------------------------------------
# Creates empty list of disks, needed for testing, its a list of actual
# fields asociated to request
disks=[]
for i in range(12):
    disks.append((0,None))

# Prepares Data Structure for form -------------------------------------
data={
    'role':'Requestor',
    'vmname':'',
    'vmcpu':0,
    'vmram':0,
    'vmcc':0,
    'vmstype':5,
    'disk':disks,
    'cc_list':cc_list,
    'stype_list':stype_list,
    'image_list':image_list
}

with open('form1.j2') as f:
    template = Template(f.read())

print(template.render(data=data))
