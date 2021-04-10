#!/usr/bin/bash
#Creacion de objeto Host
USER=butler
PASS=butler
HEADER="'Accept: application/json'" 

# butler call to egcollector
if [ "$1" == "DEBUG" ]; then
	DEBUG=", \"DEBUG\": true"
else
	DEBUG=""
fi
echo arg 1 = $1
echo DEBUG = $DEBUG

clear
#set -x
HTTP=http
HOST=collector
PORT=80
ENDPOINT=/
echo
echo Testing Happy Transaction Heartbeat via EG Collector ...
echo curl -k -s -u ${USER}:${PASS} -H "${HEADER}" -X GET "${HTTP}://${HOST}:${PORT}/${ENDPOINT}"
     curl -k -s -u ${USER}:${PASS} -H "${HEADER}" -X GET "${HTTP}://${HOST}:${PORT}/${ENDPOINT}"
echo

HTTP=http
HOST=butler
PORT=8100
ENDPOINT=api/eg-collector/heartbeat
echo
echo Testing Happy Transaction Heartbeat via Butler ...
echo curl -k -s -u ${USER}:${PASS} -H "${HEADER}" -X GET "${HTTP}://${HOST}:${PORT}/${ENDPOINT}"
     curl -k -s -u ${USER}:${PASS} -H "${HEADER}" -X GET "${HTTP}://${HOST}:${PORT}/${ENDPOINT}"
echo


exit
