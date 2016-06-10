from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone as tz
import logging
import uuid
import requests
import json

FMT='%Y-%m-%dT%H:%M:%S%z'

@csrf_exempt
def command(req):
	'''
	Executing the command that this appliance received
	'''
	logger=logging.getLogger('appliance')
	cmd=req.POST.get('CMD', None)
	logger.info('Receive CMD: %s'%cmd)
	if cmd=='REGISTER':
		register(req)
	elif cmd=='ADJUST':
		power(req)
	rep=HttpResponse('OK')
	rep.status_code=200
	return rep
	
def register(req):
	'''
	Execute the register command
	'''
	ccu=req.POST['SIP']
	cmd=json.loads(req.POST['PARAMS'])
	data=dict()
	data['UUID']=uuid.uuid4().__str__()
	data['CMD']='REGISTER'
	data['SNAME']=req.POST['TNAME']
	data['SIP']=req.POST['TIP']
	data['SPORT']=req.POST['TPORT']
	data['TNAME']=req.POST['SNAME']
	data['TIP']=req.POST['SIP']
	data['TPORT']=req.POST['SPORT']
	data['TIME']=tz.now().strftime(FMT)
	data['PARAMS']=json.dumps({'CMD':'ADJUST', 'AID':cmd[1], 'PARAMS':[{'NAME':'POWER','TYPE':'Boolean','REQUIRED':True},]})
	requests.post('http://%s:%s/cmd/'%(data['TIP'], data['TPORT']), data=data)

def power(req):
	'''
	Turn on/off the light
	'''
	cmd=json.loads(req.POST['PARAMS'])
	if 'POWER' in cmd:
		pin_light=5
		val=cmd['POWER'].upper()
		gpio.setmode(gpio.BOARD)
		gpio.setup(pin_light, gpio.OUT)
		gpio.output(pin_light, gpio.HIGHT if val in ['ON', 'YES', '1'] else gpio.LOW)
	else:
		print('Unknow power status: %s'%cmd)
