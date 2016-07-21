from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.core.urlresolvers import reverse
from .models import User, Message, Comment
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
def logout(request):
	request.session['first_name'] = None
	request.session['last_name'] = None
	request.session['id'] = None
	request.session['email'] = None
	request.session['user_level'] = None
	return redirect(reverse('index'))
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
		return redirect(reverse('addUserPage'))

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
	userRequest = {
		'email' : request.POST['email'],
		'first_name' : request.POST['first_name'],
		'last_name' : request.POST['last_name'],
		'user_level' : request.POST['user_level']
	}
	User.userManager.updateUser(userRequest, id, request)
	return redirect(reverse('edit', kwargs={'id':id}))

def profile(request, id):
	context={
		'User': User.objects.get(id=id),
		'Message' : Message.objects.all(),
		'Comment' : Comment.objects.all()
	}
	return render(request, 'user_dash/show_user.html', context)

def editProfile(request,id):
	context = {
		'User' : User.objects.get(id=id)
	}
	return render(request, 'user_dash/edit_profile.html', context)

def editProfileProcess(request, id):
	updateUser = User.objects.get(id=id)
	User.userManager.updateUser(updateUser, id, request)
	return redirect(reverse('editProfile', kwargs={'id':id}))

def writeMessage(request, id, page_id):

	if len(request.POST['message']) > 10:
		author = User.objects.get(id=id)
		user = User.objects.get(id=page_id)
		Message.objects.create(message=request.POST['message'], author=author, user=user)
	return redirect(reverse('profile', kwargs={'id':page_id}))

def writeComment(request, id, page_id, message_id):
	if len(request.POST['comment']) > 0:
		Comment.objects.create(comment=request.POST['comment'], user=User.objects.get(id=page_id), author=User.objects.get(id=id), message=Message.objects.get(id=message_id))
	return redirect(reverse('profile', kwargs={'id':page_id}))