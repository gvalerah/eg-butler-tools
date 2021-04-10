#!/usr/bin/bash
#Creacion de objeto Host
USER=butler
PASS=butler
HTTP=http
HOST=butler
PORT=8100
ENDPOINT=api/nutanix/heartbeat
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
     curl -k -s -u ${USER}:${PASS} -H "${HEADER}" -X GET "${HTTP}://${HOST}:${PORT}/${ENDPOINT}${DEBUG}" 
echo
echo
exit
echo Testing Bad formed Transaction ...
echo curl -k -s -u ${USER}:${PASS} -H "${HEADER}" -X POST "${HTTP}://${HOST}:${PORT}/${ENDPOINT}" -d "${DATAX}"
     curl -k -s -u ${USER}:${PASS} -H "${HEADER}" -X POST "${HTTP}://${HOST}:${PORT}/${ENDPOINT}" -d "${DATAX}"
echo
echo
echo Testing Remote rejected Transaction ...
echo curl -k -s -u ${USER}:${PASS} -H "${HEADER}" -X POST "${HTTP}://${HOST}:${PORT}/${ENDPOINT}" -d "${DATAY}"
     curl -k -s -u ${USER}:${PASS} -H "${HEADER}" -X POST "${HTTP}://${HOST}:${PORT}/${ENDPOINT}" -d "${DATAY}"
echo


