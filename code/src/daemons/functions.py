# End point functions
def egmonitor_host_create(app,data):
	# process data here
	arguments=data
	# contact egmonitor
	response={'data':data,'config':{}}
	for section in app.egconfig.sections():
		response['config'].update({section:{}})
		for option in app.egconfig.options(section):
			response['config'][section].update({option:app.egconfig.get(section,option)})
	# return egmonitor response here as a JSON array
	return json.dumps(response)
