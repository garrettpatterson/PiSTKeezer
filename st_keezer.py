import requests
import os
import json
import time

conf = {
	'app_url':"YOUR-ST-IDE-GRAPH-API-URL-THING-HERE"
	, 'app_id':"YOUR-APP-ID-HERE"
	, 'token':"YOUR-TOKEN-HERE"
	, 'update_ignore_seconds':600
	,'last_update':0
	, 'last_event':{
		'multiSensor':[0,0]
		,'shanktemp':0
		,'psi':0
		,'door':'closed'
	}
}



def update_event(sensor, val):
	sensor_path = ['update']

	last_val = conf['last_event'][sensor]
	if last_val != val or time.time() - conf['last_update'] > conf['update_ignore_seconds']:
		print("updated data")
		conf['last_event'][sensor] = val
		sensor_path.append(sensor)
		if not isinstance(val,list):
			val = [val]

		sensor_path+=val
		print(sensor_path)

		update_path = '/'.join(map(str,sensor_path))

		headers = {"Authorization": "Bearer "+conf['token']}

		r = requests.put(conf['app_url'] + conf['app_id'] + '/' + update_path, headers=headers)

		if r.status_code in [200,204]:
			print("success")
			conf['last_update'] = time.time()
			with open('conf.json', 'w') as cfg:
				cfg.write(json.dumps(conf))
		else:
			print(r.text)
	else:
		print("no value change since last update %d seconds ago" % (time.time()-conf['last_update']))



if os.path.exists('conf.json'):
	with open('conf.json','r') as cf:
		conf = json.loads(cf.read())
		print('load existing conf'+ json.dumps(conf))
else:
	print('create conf.json')
	
	with open('conf.json','w+') as cf:
		cf.write(json.dumps(conf))


update_event('multiSensor',[32,55])
