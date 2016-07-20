from __future__ import unicode_literals
from django.db import models
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
		print password
		checkUser = User.objects.get(email=email)
		if checkEmail['exists'] == False:
			print 'error at email exists'
			return False
		if checkEmail['valid'] == False:
			print 'error at email valid'
			errors = True
		if bcrypt.hashpw(password,checkUser.pwhash.encode(encoding='utf-8', errors='strict')) != checkUser.pwhash:
		# if password != checkUser.pwhash:
			print 'error at password'
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
			print 'error at email exists'
			errors = True
		if checkEmail['valid'] == False:
			print 'error at email valid'
			errors = True
		if len(first_name) < 2:
			print 'error at first name'
			errors = True
		if len(last_name) < 2:
			print 'error at last name'
			errors = True
		if len(password) < 8:
			print 'error at password'
			errors = True
		if confirm_password != password:
			print 'error at password confirm'
			errors = True
		if errors == True:
			print 'errors = true, success = false'
			return False
		elif errors == False:
			print 'errors = false, success = true'
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

class User(models.Model):
	first_name = models.CharField(max_length = 45)
	last_name = models.CharField(max_length = 45)
	email = models.CharField(max_length = 100)
	pwhash = models.CharField(max_length= 255)
	user_level = models.CharField(max_length=20)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)

	userManager = UserManager()
	objects = models.Manager()

class Message(models.Model):
	user = models.ForeignKey(User)
	message = models.TextField()
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
class Comment(models.Model):
	message = models.ForeignKey(Message)
	comment = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)