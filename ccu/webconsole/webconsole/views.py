from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages as msg

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
	return render(req, 'webconsole/appliances.html', params)

@login_required
def users(req):
	'''
	Show the users list on the webpage
	'''
	params=dict()
	return render(req, 'webconsole/users.html', params)
