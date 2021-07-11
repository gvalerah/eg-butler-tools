# ======================================================================
# EG Suite - EG Butler Core Service Application Transactions
# Purpose: To handle Butler API requests and orchestrate Butler Requests
# Live cycle
# (c) Emtec Group/Sertechno 2020
# GLVH gvalera@emtecgroup.net
# 2021-05-09 GVLH Refactoring to move functions to library and reuse
# 2021-05-18 GLVH adjust fur multiple subnets, and NO IP request
# 2021-05-23 GLVH QA and refactoring
# ======================================================================

import  sys
import  configparser
import  time
import  datetime
from    pprint                      import pprint
from    pprint                      import pformat
from    emtec                       import *
from    emtec.debug                 import *
from    emtec.box                   import *
from    emtec.butler.db.orm_model   import *
from    emtec.butler.constants      import *
from    emtec.api                   import *
from    emtec.data                  import *
from    emtec.nutanix               import *
#from    .                           import db
#from    .                           import logger
# Transactions
# Context Variables 
tracebox_log_length=80
# This structure will keep data cache between main loop executions

# Transaction support functions

def test_collector_queries(host,port,username,password,protocol='http',timeout=5,logger=None):
    box(f"{this()}: EG Collector {username}@{host}:{port}")
    # get cost centers
    endpoint  = 'api/get/Cost_Centers'
    arguments =''
    data      = {}        
    headers   = {'Content-Type': 'application/json'}
    url       = f'{protocol}://{host}:{port}/{endpoint}{arguments}'
    cost_centers = api_request('GET',url,data=data,headers=headers,username=username,password=password,logger=logger,timeout=timeout)
    # get rates
    endpoint = 'api/get/Rates'
    url      = f'{protocol}://{host}:{port}/{endpoint}{arguments}'
    rates = api_request('GET',url,headers=headers,username=username,password=password,timeout=timeout)
    print("COST CENTERS:")
    try:
        print(f"  {len(cost_centers.json().get('entities'))} cost centers")
    except Exception as e:
        logger.error(f"  cost_centers={cost_centers} {cost_centers.reason}: {str(e)}")
    print("RATES:")
    try:
        print(f"  {len(rates.json().get('entities'))} rates")
    except Exception as e:
        logger.error(f"  rates={rates} {rates.reason}: {str(e)}")
    
def test_nutanix_queries(host,port,username,password,protocol='https',timeout=5,logger=None):
    box(f"{this()}: Nutanix Prism Central {username}@{host}:{port}")
    arguments =''
    data      = {}        
    headers   = {'Content-Type': 'application/json'}
    # get hosts
    hosts = prism_central_get_hosts(host,port,username,password,protocol,timeout=timeout,logger=logger)
    # get clusters
    endpoint = 'api/nutanix/v3/clusters/list'
    data     = {'kind': 'cluster'}
    url      = f'{protocol}://{host}:{port}/{endpoint}{arguments}'
    clusters = api_request('POST',url,data=json.dumps(data),headers=headers,username=username,password=password,timeout=timeout)  
    remote_sites=[]
    for cluster in clusters.json()['entities']:
        node = cluster.get('spec').get('resources').get('network').get('external_ip')
        # get remote sites
        if node is not None:
            remote_sites.append(prism_central_get_remote_sites(node,port,username,password,protocol,timeout=timeout,logger=logger))

    # get projects
    endpoint = 'api/nutanix/v3/projects/list'
    data     = {'kind': 'project'}
    url      = f'{protocol}://{host}:{port}/{endpoint}{arguments}'
    projects = api_request('POST',url,data=json.dumps(data),headers=headers,username=username,password=password,timeout=timeout)        
    # get categories
    endpoint = 'api/nutanix/v3/categories/list'
    data     = {'kind': 'category'}
    url      = f'{protocol}://{host}:{port}/{endpoint}{arguments}'
    categories = api_request('POST',url,data=json.dumps(data),headers=headers,username=username,password=password,timeout=timeout)        
    print("HOSTS:")
    for host in hosts:
        print(  f"  {host.get('status').get('state')} "
                  f"{str(host.get('spec').get('name')):20} "
                  f"{host.get('metadata').get('kind'):6} "
                  f"{host.get('spec').get('resources').get('controller_vm').get('ip')}"
                )
    print("CLUSTERS:")
    for cluster in clusters.json().get('entities'):
        print(  f"  {cluster.get('status').get('state')} "
                  f"{cluster.get('spec').get('name'):20} "
                  f"{cluster.get('spec').get('resources').get('network').get('external_ip')}"
                )
    print("REMOTE SITES:")
    for sites in remote_sites:
        for site in sites:
            #rint(site)
            print(  f"  {site.get('name'):20} "
                      f"{','.join(site.get('remote_ip_ports').keys())} "
                      #f"{site.get('uuid')} "
                    )
    print("PROJECTS:")
    for project in projects.json().get('entities'):
        print(  f"  {project.get('status').get('state')} "
                  f"{project.get('spec').get('name')}"
                )
    print("CATEGORIES:")
    for category in categories.json().get('entities'):
        print(  f"  {str(category.get('system_defined')):5} "
                  f"{category.get('name'):20} "
                  f"{category.get('description'):40}"
                )
    
if __name__ == '__main__':
    logging.basicConfig(format="%(asctime)s  %(name)s  %(levelname)s: %(message)s")
    #20210710 GV logger not checkd is mandatiry now: logger=check_logger()
    logger=logging.getLogger()
    logger.setLevel(logging.INFO)
    #rint(f"logger={logger}")
    config = configparser.ConfigParser()
    config.read(sys.argv[1])
    collector = {
        'host': config.get('collector','host'),
        'port': config.getint('collector','port'),
        'username': config.get('collector','username'),
        'password': config.get('collector','password'),
        'timeout': config.getint('collector','timeout'),
    }
    nutanix = {
        'host': config.get('nutanix','host'),
        'port': config.getint('nutanix','port'),
        'username': config.get('nutanix','username'),
        'password': config.get('nutanix','password'),
        'timeout': config.getint('nutanix','timeout'),
    }
    test_collector_queries(
        host=collector.get('host'),
        port=collector.get('port'),
        username=collector.get('username'),
        password=collector.get('password'),
        protocol='http',
        timeout=collector.get('timeout'),
        logger=logger)
    test_nutanix_queries(
        host=nutanix.get('host'),
        port=nutanix.get('port'),
        username=nutanix.get('username'),
        password=nutanix.get('password'),
        protocol='https',
        timeout=nutanix.get('timeout'),
        logger=logger)
