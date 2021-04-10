#!/usr/bin/bash
#Creacion de objeto Host
USER=butler
PASS=butler
HTTP=http
HOST=mock
PORT=5000
HEADER="'Accept: application/json'" 
HEADEA="'Authorization: Basic #${USER}#${PASS}#'"

# butler call to egmonitor host create
if [ "$1" == "DEBUG" ]; then
	DEBUG="?DEBUG=1"
else
	DEBUG=""
fi
echo arg 1 = $1
echo DEBUG = $DEBUG

clear
#set -x

ENDPOINT=api/nutanix/v3/projects/list
echo
echo Testing Transaction: Projects list ...
echo curl -k -s -u ${USER}:${PASS} -H "${HEADER}" -H "${HEADEA}" -X GET "${HTTP}://${HOST}:${PORT}/${ENDPOINT}${DEBUG}" 
     curl -k    -u ${USER}:${PASS} -H "${HEADER}" -H "${HEADEA}" -X GET "${HTTP}://${HOST}:${PORT}/${ENDPOINT}${DEBUG}"  | python -m json.tool
echo
echo

ENDPOINT=api/nutanix/v3/categories/list
echo
echo Testing Transaction: Categories list...
echo curl -k -s -u ${USER}:${PASS} -H "${HEADER}" -H "${HEADEA}" -X GET "${HTTP}://${HOST}:${PORT}/${ENDPOINT}${DEBUG}" 
     curl -k    -u ${USER}:${PASS} -H "${HEADER}" -H "${HEADEA}" -X GET "${HTTP}://${HOST}:${PORT}/${ENDPOINT}${DEBUG}"  | python -m json.tool
echo
echo

ENDPOINT=api/nutanix/v3/subnets/UUID_RED_30
echo
echo Testing Transaction: Subnets "<UUID_RED>" ...
echo curl -k -s -u ${USER}:${PASS} -H "${HEADER}" -H "${HEADEA}" -X GET "${HTTP}://${HOST}:${PORT}/${ENDPOINT}${DEBUG}" 
     curl -k    -u ${USER}:${PASS} -H "${HEADER}" -H "${HEADEA}" -X GET "${HTTP}://${HOST}:${PORT}/${ENDPOINT}${DEBUG}"  | python -m json.tool
echo
echo

ENDPOINT=api/nutanix/v3/clusters/list
echo
echo Testing Transaction: Clusters list ...
echo curl -k -s -u ${USER}:${PASS} -H "${HEADER}" -H "${HEADEA}" -X GET "${HTTP}://${HOST}:${PORT}/${ENDPOINT}${DEBUG}" 
     curl -k    -u ${USER}:${PASS} -H "${HEADER}" -H "${HEADEA}" -X GET "${HTTP}://${HOST}:${PORT}/${ENDPOINT}${DEBUG}"  | python -m json.tool
echo
echo

ENDPOINT=/PrismGateway/services/rest/v2.0/images/
echo
echo Testing Transaction: Get Images list vi Prism Gateway ...
echo curl -k -s -u ${USER}:${PASS} -H "${HEADER}" -H "${HEADEA}" -X GET "${HTTP}://${HOST}:${PORT}/${ENDPOINT}${DEBUG}" 
     curl -k    -u ${USER}:${PASS} -H "${HEADER}" -H "${HEADEA}" -X GET "${HTTP}://${HOST}:${PORT}/${ENDPOINT}${DEBUG}" | python -m json.tool 
echo
echo

ENDPOINT=/api/nutanix/v3/vms
echo
echo Testing Transaction: Create virtual machine ...
echo curl -k -s -u ${USER}:${PASS} -H "${HEADER}" -H "${HEADEA}" -X GET "${HTTP}://${HOST}:${PORT}/${ENDPOINT}${DEBUG}" 
     curl -k    -u ${USER}:${PASS} -H "${HEADER}" -H "${HEADEA}" -X GET "${HTTP}://${HOST}:${PORT}/${ENDPOINT}${DEBUG}" | python -m json.tool
echo
echo

ENDPOINT=/api/nutanix/v3/vms
TOKEN=$(echo -n ${USER}:${PASS}|base64)
echo $TOKEN
AUTHENTICATION="'Authentication: Basic ${TOKEN}'"
DATA="'{\
\"name\":\"Gerardo\",\
\"disks\":[\
\"disco1\",\"disco2\",\"disco3\"\
]\
}'"
echo
echo Testing Transaction: Create virtual machine ...
echo curl -k -s -H "${HEADER}" -H "${AUTHENTICATION}" -X POST "${HTTP}://${HOST}:${PORT}/${ENDPOINT}${DEBUG}" -d "${DATA}" 
     curl -k    -H "${HEADER}" -H "${AUTHENTICATION}" -X POST "${HTTP}://${HOST}:${PORT}/${ENDPOINT}${DEBUG}" -d "${DATA}" | python -m json.tool
echo
echo
