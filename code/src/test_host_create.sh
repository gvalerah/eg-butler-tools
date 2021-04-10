#!/usr/bin/bash
#Creacion de objeto Host
USER=butler
PASS=butlerpassword
HTTP=http
HOST=192.168.0.6
PORT=8100
ENDPOINT=api/eg-monitor/host-create
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
echo Testing Happy Transaction ...
echo curl -k -s -u ${USER}:${PASS} -H "${HEADER}" -X POST "${HTTP}://${HOST}:${PORT}/${ENDPOINT}" -d "${DATA}"
     curl -k -s -u ${USER}:${PASS} -H "${HEADER}" -X POST "${HTTP}://${HOST}:${PORT}/${ENDPOINT}" -d "${DATA}"
echo
echo
echo Testing Bad formed Transaction ...
echo curl -k -s -u ${USER}:${PASS} -H "${HEADER}" -X POST "${HTTP}://${HOST}:${PORT}/${ENDPOINT}" -d "${DATAX}"
     curl -k -s -u ${USER}:${PASS} -H "${HEADER}" -X POST "${HTTP}://${HOST}:${PORT}/${ENDPOINT}" -d "${DATAX}"
echo
echo
echo Testing Remote rejected Transaction ...
echo curl -k -s -u ${USER}:${PASS} -H "${HEADER}" -X POST "${HTTP}://${HOST}:${PORT}/${ENDPOINT}" -d "${DATAY}"
     curl -k -s -u ${USER}:${PASS} -H "${HEADER}" -X POST "${HTTP}://${HOST}:${PORT}/${ENDPOINT}" -d "${DATAY}"
echo


#Resultado
#    {
#        "results": [
#            {
#                "code": 200.0,
#                "status": "Object was created."
#            }
#        ]
#    }
