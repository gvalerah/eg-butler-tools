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
	DEBUG='-d "{"DEBUG": true}"'
else
	DEBUG=""
fi
echo arg 1 = $1
echo DEBUG = $DEBUG

clear
#set -x
echo
HOSTNAME=TEST-API
echo Testing Happy Transaction ... Deleting ${HOSTNAME} ... via BUTLER
ENDPOINT=api/eg-monitor/host-delete
echo curl -k -s -u ${USER}:${PASS} -H "${HEADER}" -X POST "${HTTP}://${HOST}:${PORT}/${ENDPOINT}/${HOSTNAME}"
     curl -k -s -u ${USER}:${PASS} -H "${HEADER}" -X POST "${HTTP}://${HOST}:${PORT}/${ENDPOINT}/${HOSTNAME}"
echo
echo

exit
