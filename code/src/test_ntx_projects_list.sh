#!/usr/bin/bash
#Creacion de objeto Host
USER=butler
PASS=butler
HTTP=http
HOST=mock
PORT=5000
ENDPOINT=api/nutanix/v3/projects/list
HEADER="'Accept: application/json'" 

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
echo
echo Testing Happy Transaction ...
echo curl -k -s -u ${USER}:${PASS} -H "${HEADER}" -X GET "${HTTP}://${HOST}:${PORT}/${ENDPOINT}${DEBUG}" 
     curl -k    -u ${USER}:${PASS} -H "${HEADER}" -X GET "${HTTP}://${HOST}:${PORT}/${ENDPOINT}${DEBUG}" 
echo
echo
exit
