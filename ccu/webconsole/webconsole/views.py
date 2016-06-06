from django.shortcuts import render, redirect, get_object_or_404 as getObj
from django.conf import settings
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages as msg
from django.http import HttpResponse
from django.utils import timezone as tz
from django.views.decorators.csrf import csrf_exempt
from webconsole.models import *
import uuid
import requests
import json

FMT='%Y-%m-%dT%H:%M:%S%z'

@csrf_exempt
def cmd(req):
	'''
	Show the command
	'''
	cmd=req.POST['CMD']
	if cmd=='REGISTER':
		cmd=json.loads(req.POST['PARAMS'])
		command=Command()
		command.name=req.POST['CMD']
		command.appliance_id=cmd['AID']
		command.save()
		for p in cmd['PARAMS']:
			print(p)
			param=Parameter()
			param.command=command
			param.name=p['NAME']
			param.typ=p['TYPE']
			param.save()
	return HttpResponse('OK')

def login(req):
	params=dict()
	if req.method=='POST':
		username=req.POST.get('username', None)
		password=req.POST.get('password', None)
		user=authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				auth_login(req, user)
				return redirect(req.POST.get('next', '/'))
			else:
				msg.warning(req, 'The user is not active')
		else:
			msg.warning(req, 'Authentication failed due to incorrect username or password')
		
	return render(req, 'webconsole/login.html', params)

def logout(req):
	auth_logout(req)
	return redirect(settings.ABSOLUTE_PATH)

@login_required
def dashboard(req):
	'''
	Show the dashboard to user
	'''
	params=dict()
	return render(req, 'webconsole/dashboard.html', params)

@login_required
def appliances(req):
	'''
	Show the appliances list on the webconsole
	'''
	params=dict()
	params['cmd']=Appliance.objects.all()
	return render(req, 'webconsole/appliances.html', params)

@login_required
def appliance(req, aid):
	'''
	Show the specified appliance information and let user to modified.
	@param aid  	- The appliance id. It should be the appliance UUID, 
			  if this is equals to "new", show the register form;
			  if this is equals to "search", search the available appliance;
	'''
	params=dict()
	params['aid']=aid
	import netifaces
	ipaddr=netifaces.ifaddresses(getattr(settings, 'BIND', 'eth0'))[2][0]['addr']
	if req.method=='POST':
		appliance=Appliance()
		if req.POST.get('id', None): appliance.id=req.POST['id']
		appliance.ipaddr=req.POST['ipaddr']
		appliance.port=req.POST['port']
		appliance.name=req.POST['name']
		appliance.location=req.POST['loc']
		appliance.save()
		#Sending the REGISTER command to appliance
		data=dict()
		data['UUID']=uuid.uuid4().__str__()
		data['CMD']='REGISTER'
		data['SNAME']='CCU'
		data['SIP']=ipaddr
		data['SPORT']=getattr(settings, 'PORT', '8000')
		data['TNAME']=appliance.name
		data['TIP']=appliance.ipaddr
		data['TPORT']=appliance.port
		data['PARAMS']=json.dumps([req.POST.get('securecode', 'ABC1234'),appliance.id])
		data['TIME']=tz.now().strftime(FMT)
		requests.post('http://%s:%s/'%(appliance.ipaddr, appliance.port), data=data)
		return redirect('appliances')
	elif req.method=='DELETE':
		appliance=getObj(Appliance, id=aid)
		appliance.delete()
		return redirect('appliances')
	elif aid=='new':
		params['cmd']=Appliance()
	elif aid=='search':
		import nmap
		nm=nmap.PortScanner()
		nm.scan('%s/24'%ipaddr, '80,443')
		rep=HttpResponse(content_type='application/json')
		cnt=0
		rep.write('[')
		for h in nm.all_hosts():
			if h==ipaddr: continue #Skip the CCU itself
			if Appliance.objects.filter(ipaddr=h): continue #Skip the registered appliance
			if cnt>0: rep.write(', ')
			rep.write('{\"IPAddr\": \"%s\", \"Name\": \"%s\"}'%(h, nm[h]['tcp'][80]['product']))
			cnt+=1
		rep.write(']')
		return rep
	else:
		params['cmd']=getObj(Appliance, id=aid)
	return render(req, 'webconsole/appliance.html', params)

@login_required
def users(req):
	'''
	Show the users list on the webpage
	'''
	params=dict()
	return render(req, 'webconsole/users.html', params)
