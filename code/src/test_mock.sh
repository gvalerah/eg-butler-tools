#!/usr/bin/bash
#Creacion de objeto Host
USER=butler
PASS=butler
HTTP=http
HOST=192.168.56.111
PORT=5000
ENDPOINT=
HEADER="'Accept: application/json'" 

# butler call to egmonitor host create
if [ "$1" == "DEBUG" ]; then
	DEBUG=", \"DEBUG\": true"
else
	DEBUG=""
fi
echo arg 1 = $1
echo DEBUG = $DEBUG

clear
#set -x
echo
echo Testing Happy Transaction Heartbeat ...
echo curl -k -s -u ${USER}:${PASS} -H "${HEADER}" -X GET "${HTTP}://${HOST}:${PORT}/${ENDPOINT}" 
     curl -k -s -u ${USER}:${PASS} -H "${HEADER}" -X GET "${HTTP}://${HOST}:${PORT}/${ENDPOINT}" 
echo
HOST=eg-suite-lab
PORT=9440
echo
echo Testing Happy Transaction Heartbeat using Nutanix Port via EG Suite Lab Gateway...
echo curl -k -s -u ${USER}:${PASS} -H "${HEADER}" -X GET "${HTTP}://${HOST}:${PORT}/${ENDPOINT}" 
     curl -k -s -u ${USER}:${PASS} -H "${HEADER}" -X GET "${HTTP}://${HOST}:${PORT}/${ENDPOINT}" 
echo
