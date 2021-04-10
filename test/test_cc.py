import sys
from emtec.class_cc import *

def get_cc(top,department,group,stype):
    return top+department-top+group-top+stype-top

def get_cc1(top,department,group,stype):
    return top|department|group|stype

def get_cc2(top,cost_centers):
    cc = top
    for cost_center in cost_centers:
        cc += cost_center - top
    return cc
def get_cc3(top,cost_centers):
    cc = top
    for cost_center in cost_centers:
        cc &= cost_center
    return cc
def get_cc4(top,cost_centers):
    cc = top
    for cost_center in cost_centers:
        cc |= cost_center
    return cc
    
    
if __name__ == '__main__':
    top        = 30000000
    department = 30100000
    group      = 30001000
    stype      = 30000011
    print(f"top        = {top}")
    print(f"department = {department}")
    print(f"group      = {group}")
    print(f"type       = {stype}")
    print(f"cc         = {get_cc(top,department,group,stype)}")
    print(f"cc1        = {get_cc1(top,department,group,stype)}")
    print(f"cc2        = {get_cc2(top,[department,group,stype])}")
    print(f"cc3        = {get_cc3(top,[department,group,stype])}")
    print(f"cc4        = {get_cc4(top,[department,group,stype])}")

    ccmap = Costcenters_Structure(30000000,'AGUAS-ANDINAS','Aguas Andinas SPA')
    #print(f"ccmap={ccmap}")
    ccmap.add(100000,'RRHH','Recursos Humanos')
    ccmap.add(1000,'SAND','Sandbox'     ,parent='RRHH')
    ccmap.add(2000,'DESA','Desarrollo'  ,parent='RRHH')
    ccmap.add(3000,'QA'  ,'QA'          ,parent='RRHH')
    ccmap.add(4000,'PROD','Producción'  ,parent='RRHH')
    ccmap.add(5000,'CONT','Contingencia',parent='RRHH')
    ccmap.add(200000,'AAFF','Administración y Finanzas')
    print(f"ccmap={ccmap}")
    ccmap.add(1000,'SAND','Sandbox'     ,parent='AAFF')
    ccmap.add(2000,'DESA','Desarrollo'  ,parent='AAFF')
    ccmap.add(3000,'QA'  ,'QA'          ,parent='AAFF')
    ccmap.add(4000,'PROD','Producción'  ,parent='AAFF')
    ccmap.add(5000,'CONT','Contingencia',parent='AAFF')
    ccmap.tree(stream=sys.stdout)
    print(f"ccmap.costcenters:{type(ccmap.costcenters)}")
    print(f"ccmap.costcenters.keys():{ccmap.costcenters.keys()}")
    print(f"ccmap.costcenters.keys().sort():{list(ccmap.costcenters.keys()).sort()}")
    print(f"{pformat(ccmap.costcenters)}")
    ccmap.tree(stream=sys.stdout)
    #ccmap.sort()
    
