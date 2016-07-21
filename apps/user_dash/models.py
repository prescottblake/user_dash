from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.


class UserManager(models.Manager):
	def validateEmail(self, email):
		validate = {
			'valid' : False,
			'exists' : False
		}
		userExist = User.objects.filter(email=email)
		if EMAIL_REGEX.match(email) and len(email) > 5:
			validate['valid'] = True
		else:
			validate['valid'] = False
		if not userExist.count():
			validate['exists'] = False
		else:
			validate['exists'] = True
		return validate
	def hashPassword(self,password):
		preliminaryHash = password.encode(encoding='utf-8', errors='strict')
		pwhash = bcrypt.hashpw(preliminaryHash,bcrypt.gensalt())
		return pwhash

	def login(self, userRequest, request):
		email = userRequest['email']
		password = userRequest['password']
		password = password.encode(encoding='utf-8', errors='strict')

		errors = False
		checkEmail = self.validateEmail(email)
		checkUser = User.objects.get(email=email)
		if checkEmail['exists'] == False:
			messages.add_message(request, messages.INFO, 'Email is not registered.')
			return False
		if checkEmail['valid'] == False:
			messages.add_message(request, messages.INFO, 'Invalid email address.')
			errors = True
		if bcrypt.hashpw(password,checkUser.pwhash.encode(encoding='utf-8', errors='strict')) != checkUser.pwhash:
			messages.add_message(request, messages.INFO, 'Incorrect password')
			errors = True
		if errors == True:
			return False
		elif errors == False:
			return True

	def register(self, userRequest, request):
		errors = False
		email = userRequest['email']
		first_name = userRequest['first_name']
		last_name = userRequest['last_name']
		password = userRequest['password']
		confirm_password = userRequest['confirm_password']
		checkEmail = self.validateEmail(email)
		if checkEmail['exists'] == True:
			messages.add_message(request, messages.INFO, 'Email is already registered')
			errors = True
		if checkEmail['valid'] == False:
			messages.add_message(request, messages.INFO, 'Invalid email address')
			errors = True
		if len(first_name) < 2:
			messages.add_message(request, messages.INFO, 'First name is too short')
			errors = True
		if len(last_name) < 2:
			messages.add_message(request, messages.INFO, 'Last name is too short')
			errors = True
		if len(password) < 8:
			messages.add_message(request, messages.INFO, 'Password must be at least 8 characters')
			errors = True
		if confirm_password != password:
			messages.add_message(request, messages.INFO, 'Passwords do not match')
			errors = True
		if errors == True:
			return False
		elif errors == False:
			return True	
	def masterValidator(self, userRequest,id ,request):
		errors = False
		updateUser = User.objects.get(id=id)
		print "updateUser = : " + str(updateUser)
		if 'first_name' not in userRequest:
			userRequest['first_name'] = updateUser.first_name
			

		if 'last_name' not in userRequest:
			userRequest['last_name'] = updateUser.last_name
		

		if 'email' not in userRequest:
			userRequest['email'] = updateUser.email
		

		if 'description' not in userRequest:
			userRequest['description'] = updateUser.description
		

		if 'password' not in userRequest:
			userRequest['password'] = updateUser.pwhash
		
		if 'user_level' not in userRequest:
			userRequest['user_level'] = updateUser.user_level
		

		checkEmail = self.validateEmail(userRequest['email'])
		if checkEmail['valid'] == False:
			messages.add_message(request, messages.INFO, 'Invalid email address')
			errors = True
		if len(userRequest['first_name']) < 2:
			messages.add_message(request, messages.INFO, 'First name is too short')
			errors = True
		if len(userRequest['last_name']) < 2:
			messages.add_message(request, messages.INFO, 'Last name is too short')
			errors = True
		if len(userRequest['password']) < 8:
			messages.add_message(request, messages.INFO, 'Password must be at least 8 characters')
			errors = True
		if 'confirm_password' in userRequest:
			if userRequest['confirm_password'] != password:
				messages.add_message(request, messages.INFO, 'Passwords do not match')
				errors = True
		if len(userRequest['description']) > 1000:
			messages.add_message(request, messages.INFO, 'Description is too long')
			errors = True
		if errors == True:
			return False
		elif errors == False:
			return True	

	def createUser(self, userRequest, request):
		currentUsers = User.objects.all()
		userRequest['user_level'] = 'user'
		if not currentUsers.count():
			userRequest['user_level'] = 'admin'
		userRequest['password'] = self.hashPassword(userRequest['password'])
		User.objects.create(email=userRequest['email'], first_name=userRequest['first_name'], last_name=userRequest['last_name'], pwhash=userRequest['password'], user_level= userRequest['user_level'])

	def signInUser(self, userRequest, request):
		currentUser = User.objects.get(email=userRequest['email'])
		request.session['first_name'] = currentUser.first_name
		request.session['last_name'] = currentUser.last_name
		request.session['id'] = currentUser.id
		request.session['email'] = currentUser.email
		request.session['user_level'] = currentUser.user_level

	def updateUser(self, userRequest,id , request):
		updateUser = User.objects.get(id=id)
		if self.masterValidator(userRequest,id, request) == True:
			if not userRequest['first_name']:
				userRequest.first_name = updateUser.first_name
			else:
				updateUser.first_name = userRequest['first_name']

			if not userRequest['last_name']:
				userRequest['last_name'] = updateUser.last_name
			else:
				updateUser.last_name = userRequest['last_name']

			if not userRequest['email']:
				userRequest['email'] = updateUser.email
			else:
				updateUser.email = userRequest['email']

			if not userRequest['description']:
				userRequest['description'] = updateUser.description
			else:
				updateUser.description = userRequest['description']

			if not userRequest['password']:
				userRequest['password'] = updateUser.password
			else:
				updateUser.password = self.hashPassword(userRequest['password'])

			updateUser.save()
		else:
			pass

class User(models.Model):
	first_name = models.CharField(max_length = 45)
	last_name = models.CharField(max_length = 45)
	email = models.CharField(max_length = 100)
	pwhash = models.CharField(max_length= 255)
	user_level = models.CharField(max_length=20)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	description = models.TextField(max_length=1000, default='')

	userManager = UserManager()
	objects = models.Manager()

class Message(models.Model):
	user = models.ForeignKey(User,null=True, related_name='message_user')
	author = models.ForeignKey(User,null=True, related_name='message_author')
	message = models.TextField()
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = models.Manager()

class Comment(models.Model):
	user = models.ForeignKey(User,null=True, related_name='comment_user')
	author = models.ForeignKey(User,null=True, related_name='comment_author')
	message = models.ForeignKey(Message)
	comment = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = models.Manager()