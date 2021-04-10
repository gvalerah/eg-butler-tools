#!/usr/bin/bash
#Creacion de objeto Host
USER=butler
PASS=butler
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
HTTP=https
HOST=monitor
PORT=5665
ENDPOINT=v1/objects/hosts
echo
echo Testing Happy Transaction Heartbeat via EG Monitor ...
echo curl -k -s -u ${USER}:${PASS} -H "${HEADER}" -X GET "${HTTP}://${HOST}:${PORT}/${ENDPOINT}"
     curl -k -s -u ${USER}:${PASS} -H "${HEADER}" -X GET "${HTTP}://${HOST}:${PORT}/${ENDPOINT}"
echo

HTTP=http
HOST=butler
PORT=8100
ENDPOINT=api/eg-monitor/host
echo
echo Testing Happy Transaction Heartbeat via Butler ...
echo curl -k -s -u ${USER}:${PASS} -H "${HEADER}" -X GET "${HTTP}://${HOST}:${PORT}/${ENDPOINT}"
     curl -k -s -u ${USER}:${PASS} -H "${HEADER}" -X GET "${HTTP}://${HOST}:${PORT}/${ENDPOINT}"
echo


exit
