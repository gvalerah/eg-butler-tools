#!/usr/bin/bash
#Creacion de objeto Host
USER=butler
PASS=butlerpassword
HTTP=http
HOST=mock
PORT=5000
ENDPOINT=api/v3
HEADER="'Accept: application/json'" 

# butler call to egmonitor host create
if [ "$1" == "DEBUG" ]; then
	DEBUG=", \"DEBUG\": true"
	GET_DEBUG="?DEBUG"
else
	DEBUG=""
	GET_DEBUG=""
fi
echo arg 1 = $1
echo DEBUG = $DEBUG
ADDRESS='"address":"10.26.1.247"'
ADDRESX='"addresx":"10.26.1.247"'
ADDRESY='"address":"fail"'
VARS_OS=',"vars.os":"Linux"'
 PRETTY=',"pretty": true'
   DATA="{ ${ADDRESS} ${VARS_OS} ${PRETTY} ${DEBUG} }"
  DATAX="{ ${ADDRESX} ${VARS_OS} ${PRETTY} ${DEBUG} }"
  DATAY="{ ${ADDRESY} ${VARS_OS} ${PRETTY} ${DEBUG} }"

clear
#set -x
echo
echo Testing Happy Transaction Heartbeat ...
echo curl -k -s -u ${USER}:${PASS} -H "${HEADER}" -X GET "${HTTP}://${HOST}:${PORT}/${ENDPOINT}${GET_DEBUG}"
     curl -k -s -u ${USER}:${PASS} -H "${HEADER}" -X GET "${HTTP}://${HOST}:${PORT}/${ENDPOINT}${GET_DEBUG}"
echo
echo

ENDPOINT=api/v3/vmlist
echo
echo Testing Happy Transaction VM List ...
echo curl -k -s -u ${USER}:${PASS} -H "${HEADER}" -X GET "${HTTP}://${HOST}:${PORT}/${ENDPOINT}" -d "${DATA}" 
     curl -k -s -u ${USER}:${PASS} -H "${HEADER}" -X GET "${HTTP}://${HOST}:${PORT}/${ENDPOINT}" -d "${DATA}" 
echo
echo

ENDPOINT=api/v3/vm
echo
echo Testing Happy Transaction VM Status ...
echo curl -k -s -u ${USER}:${PASS} -H "${HEADER}" -X GET "${HTTP}://${HOST}:${PORT}/${ENDPOINT}" -d "${DATA}"
     curl -k -s -u ${USER}:${PASS} -H "${HEADER}" -X GET "${HTTP}://${HOST}:${PORT}/${ENDPOINT}" -d "${DATA}"
echo
echo

echo TESTS via BUTLER
echo ================
HOST=butler
PORT=8100
ENDPOINT=api/nutanix/heartbeat
echo
echo Testing Happy Transaction Heartbeat ...
echo curl -k -s -u ${USER}:${PASS} -H "${HEADER}" -X GET "${HTTP}://${HOST}:${PORT}/${ENDPOINT}${GET_DEBUG}" 
     curl -k -s -u ${USER}:${PASS} -H "${HEADER}" -X GET "${HTTP}://${HOST}:${PORT}/${ENDPOINT}${GET_DEBUG}"
echo
echo
ENDPOINT=api/nutanix/vmlist
echo
echo Testing Happy Transaction VM List ...
echo curl -k -s -u ${USER}:${PASS} -H "${HEADER}" -X GET "${HTTP}://${HOST}:${PORT}/${ENDPOINT}" -d "${DATA}"
     curl -k -s -u ${USER}:${PASS} -H "${HEADER}" -X GET "${HTTP}://${HOST}:${PORT}/${ENDPOINT}" -d "${DATA}"
echo
echo

ENDPOINT=api/nutanix/vm
echo
echo Testing Happy Transaction VM Status ...
echo curl -k -s -u ${USER}:${PASS} -H "${HEADER}" -X GET "${HTTP}://${HOST}:${PORT}/${ENDPOINT}" -d "${DATA}"
     curl -k -s -u ${USER}:${PASS} -H "${HEADER}" -X GET "${HTTP}://${HOST}:${PORT}/${ENDPOINT}" -d "${DATA}"
echo
echo
