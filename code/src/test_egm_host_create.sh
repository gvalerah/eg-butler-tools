#!/usr/bin/bash
#Creacion de objeto Host
USER=butler
PASS=butler
HTTP=http
HOST=butler
PORT=8100
HEADER="'Accept: application/json'" 

# butler call to egmonitor host create
if [ "$1" == "DEBUG" ]; then
	DEBUG=", \"DEBUG\": true"
else
	DEBUG=""
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
HOSTNAME=TEST-API
echo Testing Happy Transaction ... Creating ${HOSTNAME} ... via BUTLER
ENDPOINT=api/eg-monitor/host-create
echo curl -k -s -u ${USER}:${PASS} -H "${HEADER}" -X POST "${HTTP}://${HOST}:${PORT}/${ENDPOINT}/${HOSTNAME}" -d "${DATA}"
     curl -k -s -u ${USER}:${PASS} -H "${HEADER}" -X POST "${HTTP}://${HOST}:${PORT}/${ENDPOINT}/${HOSTNAME}" -d "${DATA}"
echo
echo

exit
