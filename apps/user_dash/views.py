from django.shortcuts import render, redirect, HttpResponse

from django.core.urlresolvers import reverse
from .models import User
# Create your views here.
def index(request):
	context ={
		'User' : User.objects.all()
	}
	return render(request, 'user_dash/index.html', context)

def registerPage(request):
	return render(request, 'user_dash/register.html')

def register(request):
	print request.POST
	userRequest = {
		'email' : request.POST['email'],
		'first_name' : request.POST['first_name'],
		'last_name' : request.POST['last_name'],
		'password' : request.POST['password'],
		'confirm_password' : request.POST['confirm_password']
	}
	success = User.userManager.register(userRequest, request)
	if success == True:
		User.userManager.createUser(userRequest, request)
		User.userManager.signInUser(userRequest,request)
		return redirect(reverse('dashboard'))
	else:
		return redirect(reverse('registerPage'))

def loginPage(request):
	return render(request, 'user_dash/login.html')

def login(request):
	userRequest = {
		'email' : request.POST['email'],
		'password' : request.POST['password']
	}
	success = User.userManager.login(userRequest, request)
	if success == True:
		User.userManager.signInUser(userRequest,request)
		return redirect(reverse('dashboard'))
	else:
		return redirect(reverse('loginPage'))

def addUserPage(request):
	return render(request, 'user_dash/create_user.html')

def addUser(request):
	userRequest = {
		'email' : request.POST['email'],
		'first_name' : request.POST['first_name'],
		'last_name' : request.POST['last_name'],
		'password' : request.POST['password'],
		'confirm_password' : request.POST['confirm_password']
	}
	success = User.userManager.register(userRequest,request)
	if success == True:
		User.userManager.createUser(userRequest, request)
		return redirect(reverse('dashboard'))
	else:
		return redirect(reverse('addUser'))

def dashboard(request):
	if not request.session['user_level']:
		return redirect(reverse('index'))
	else:
		context ={
			'User': User.objects.all()
		}
		return render(request,'user_dash/dashboard.html', context)
def remove(request,id):
	User.objects.get(id=id).delete()
	return redirect(reverse('dashboard'))

def edit(request,id):
	context = {
		'User' : User.objects.get(id=id)
	}
	return render(request,'user_dash/edit_user.html', context)

def update(request,id):
	updateUser = User.objects.get(id=id)
	updateUser.first_name = request.POST['first_name']
	updateUser.last_name = request.POST['last_name']
	updateUser.email = request.POST['email']
	updateUser.user_level = request.POST['user_level']
	updateUser.save()
	return redirect(reverse('dashboard'))

def profile(request, id):
	context={
		'User': User.objects.get(id=id)
	}
	return render(request, 'user_dash/show_user.html', context)