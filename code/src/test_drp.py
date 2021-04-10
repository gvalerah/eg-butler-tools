""" ####################################################################

TEST PROGRAM FOR SOME DRP TRANSACTIONS 

TRICKS:
Since transactions need a Flask app object, but they use the 
'app.config' member only, then a 'mock/fake' app object is implemented 
as a namedtuple at the very beginnig of the program

GLVH 2021-0313 Initial test version
gvalera@emtecgroup.net

#################################################################### """

# Required libraries here, simulates as close as possible production
# environment
from collections import namedtuple
try: print(f"18 logger={logger}")
except: print("19 logger not found")
from emtec.nutanix import *
try: print(f"21 logger={logger}")
except: print("22 logger not found")
from core.transactions import *
try: print(f"24 logger={logger}")
except: print("25 logger not found")
from pprint import pprint,pformat
try: print(f"27 logger={logger}")
except: print("28 logger not found")
import datetime
try: print(f"30 logger={logger}")
except: print("31 logger not found")

# Setting fake Flask app object and data
APP = namedtuple("App","config")
config = {
    'NUTANIX_HOST'    : '10.26.1.227',
    'NUTANIX_PORT'    : 9440,
    'NUTANIX_USERNAME': 'gvalera',
    'NUTANIX_PASSWORD': 'Pass1010.,',
    'NUTANIX_PROTOCOL': 'https',
}
app = APP(config)
# Configurate test program logger --------------------------------------
if "debug" in sys.argv:
    logger.setLevel  ( logging.DEBUG )
else:
    logger.setLevel  ( logging.INFO )
formatter        = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
console_handler  = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter )
logger.addHandler( console_handler )

# Actual test program starts here --------------------------------------
print()
print()
# setup test values
timeout = 3 # seconds
vmname  = "Test Lab 1"

logger.info(f"basic connectivity test ...")
logger.info("")
logger.info(f"INICIA TEST 1")
logger.info("")
logger.info(f"looking for vm '{vmname}' ...")
vm = get_nutanix_vm(app,vmname,timeout=timeout)
logger.debug(pformat(vm))
if vm is not None:
    logger.info(f"vm               = {vm['spec']['name']} {vm['status']['state']}")
    logger.info(f"looking for hosts in '{app.config.get('NUTANIX_HOST',None)}' ...")
else:
    logger.error(f"invalid VM")

hosts = get_hosts(app)
if hosts is not None:
    for host in hosts:
        if host['spec'].get('name',None) is not None:
            logger.info(f"{host['spec'].get('name',None)} {host['spec']['resources']['controller_vm']['ip']}")
        else:
            logger.info(f"Cluster: {host['spec']['resources']['controller_vm']['ip']}")
else:
    logger.error(f"No hosts found !!!")
trx1 = True
trx2 = False
trx3 = False
trx4 = False
trx5 = True
if trx1: 
    
    
    if vm is not None:
        remote_sites = []
        remote_cluster = None
        protection_domain = None
        if trx1:
            host = hosts[0]['spec']['resources']['controller_vm']['ip']
            logger.info(f"getting remote sites from host {host} ...")
            remote_sites = get_remote_sites(app,host,timeout=timeout)
        else:
            logger.warning(f"TRX1 not executed")
        logger.info(f"remote_sites = {remote_sites}")
        if remote_sites is not None and len(remote_sites):
            remote_cluster=remote_sites[0]['name']
        logger.info(f"remote_cluster = {remote_cluster}")
        # create protection domain
        if trx2 and remote_cluster is not None:
            logger.info(f"creating protection domain via host '{host}' for vm '{vmname}' ...")
            protection_domain = create_protection_domain(app,host=host,vmname=vmname,timeout=timeout)
            if protection_domain is not None:
                # protect VM
                logger.info(f"protecting {vmname} with protection domain {protection_domain } ...")
                if trx3 and protect_vms(app,vmname,host,protection_domain,timeout):
                    # create schedule
                    logger.info(f"creating schedule for {remote_cluster}:{protection_domain} ...")
                    if trx4 and create_schedule(app,host,protection_domain,remote_cluster,timeout=timeout):
                        logger.info(f"VM '{vmname}' is now protected in '{remote_cluster}:{protection_domain}'. SUCCESS !!!")
                    else: 
                        logger.error(f"ERROR could not create schedule for {vmname} in {remote_cluster}")
                else:
                    logger.error(f"ERROR could not protect {vmname} in {remote_cluster} ")
            else:
                logger.error(f"ERROR could not create pd {protection_domain} for vm {vmname}")
        else:
            logger.error(f"ERROR invalid remote cluster '{remote_cluster}'")
    else:
        logger.error(f"ERROR basic connectivity test failed.")
        
        
        
        
if trx2:
    logger.info("")
    logger.info(f"<<< EOT >>>")
    logger.info("")
    logger.info(f"INICIA TEST 2")
    logger.info("")
    for host in hosts:
        if host['spec'].get('name',None) is not None:
            logger.info(f"{host['spec']['name']}")
            ip = host['spec']['resources']['controller_vm']['ip']
            logger.info(f"getting remote sites from ip {ip} ...")
            remote_sites = get_remote_sites(app,ip,timeout=timeout)
            logger.info(f"remote_sites = {remote_sites}")
    logger.info(f"<<< EOT >>>")

if trx1:
    logger.info("")
    logger.info(f"INICIA TEST 3")
    logger.info("")
    if create_drp(
            app,
            vmname,
            timeout = timeout
            ):
        logger.info(f"DRP for VM: '{vmname}' Success !!!")
    else:
        logger.info(f"DRP for VM: '{vmname}' Failure !!!")

# Test de captura de snapshots
# esta funcion será util para collector
# analizar independencia de codigo entre aplicaciones
if trx5:
    logger.info("")
    logger.info(f"INICIA TEST 4 SNAPSHOTS")
    logger.info("")
    print(f"app     = {app}")
    host = hosts[0]['spec']['resources']['controller_vm']['ip']
    print(f"host    = {host}")
    print(f"timeout = {timeout}")
    
    snapshots = get_snapshots(app,host,timeout=timeout)
    total_bytes = 0
    snaps={}
    print(f"snapshots list = {len(snapshots)}")
    for snapshot in snapshots:
        size_bytes = snapshot['exclusive_usage_in_bytes']
        print(f"vm_name = {snapshot['vm_name']:25} {snapshot['vm_id']} {size_bytes:18,} B {size_bytes/(1024*1024*1024):12.6f} GB")
        total_bytes += size_bytes
    print(f"Total ahora: {total_bytes/(1024*1024*1024):.6f} GB")
    snaps = get_snapshots_dict(snapshots)
    print(f"snapshots dict = {len(snaps)}")
    pprint(snaps)
    usage_bytes = 0
    total_bytes = 0
    for snap in snaps:
        usage_bytes += snaps[snap]['exclusive_usage_in_bytes']
        total_bytes += snaps[snap]['size_in_bytes']
    print(f"Usage ahora: {usage_bytes/(1024*1024*1024):.6f} GB")
    print(f"Total ahora: {total_bytes/(1024*1024*1024):.6f} GB")
    print()
    for snap in snaps:
        vm = get_nutanix_vm(app,snaps[snap]['vm_name'])
        if vm is not None:
            print(f"{snaps[snap]['vm_name']}={vm}")
        else:
            print(f"no vm found for snapshot '{snaps[snap]['vm_name']}'")
    vm = get_nutanix_vm(app,"Test Lab 1",logger=logger)
    if vm is not None:
        print(f"Test Lab 1={vm['status']['state']} '{vm['spec']['name']}' {vm['metadata']['uuid']}")
        
