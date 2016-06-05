from django.shortcuts import render, redirect, get_object_or_404 as getObj
from django.conf import settings
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages as msg
from django.http import HttpResponse
from webconsole.models import *

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
	if req.method=='POST':
		appliance=Appliance()
		if req.POST.get('id', None): appliance.id=req.POST['id']
		appliance.ipaddr=req.POST['ipaddr']
		appliance.name=req.POST['name']
		appliance.location=req.POST['loc']
		appliance.save()
		return redirect('appliances')
	elif req.method=='DELETE':
		appliance=getObj(Appliance, id=aid)
		appliance.delete()
		return redirect('appliances')
	elif aid=='new':
		params['cmd']=Appliance()
	elif aid=='search':
		import nmap
		import netifaces
		ipaddr=netifaces.ifaddresses(getattr(settings, 'BIND', 'eth0'))[2][0]['addr']
		nm=nmap.PortScanner()
		nm.scan('%s/24'%ipaddr, '80,443')
		rep=HttpResponse(content_type='application/json')
		cnt=0
		rep.write('[')
		for h in nm.all_hosts():
			if h==ipaddr: continue
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
