from __future__ import unicode_literals

from django.db import models
from django.contrib import messages
import re
import bcrypt
from datetime import datetime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class UserManager(models.Manager):
	def registration_validation(self, request_data):
		#this will return the error message one at a time.
		message=''
		if 'first_name' in request_data:
			first_name = request_data['first_name'].strip()
			if len(first_name)<=2:
				message = 'Please enter a first name longer than 2 characters.'
			elif first_name.isalpha() != True:
				message = 'Please enter a first name with no special characters or numbers.'
			if message != '':
				return message
		if 'last_name' in request_data:
			last_name = request_data['last_name'].strip()
			if len(last_name)<=2:
				message = 'Please enter a last name longer than 2 characters.'
			elif last_name.isalpha() == False:
				message = 'Please enter a last name with no special characters.'		
			if message != '':
				return message
		
		if 'email' in request_data:
			email = request_data['email'].strip().lower()
			print EMAIL_REGEX.match(email), "EMAIL_REGEX.match(email)"
			if len(email)<=2 or EMAIL_REGEX.match(email)==None:
				message = 'Please enter a valid email address.'
			elif self.duplicateEmail(email):
				message = 'This email address has already been used.'
			if message != '':
				return message

		if 'password' in request_data:
			password = request_data['password'].strip()
			if (len(password) < 8):
				message = "Password must be longer than eight characters."
				# print "it loaded the flash"
			elif (self.CheckUpperCase(password)!=True or self.CheckNumeric(password)!=True):
				message ="Password must be contain at least one capital letter and one number."
			if message!='':
				return message
		
		if 'passwordconfirm' in request_data:
			passwordconfirm = request_data['passwordconfirm'].strip()
			if passwordconfirm.strip() != request_data['password'].strip():
				message ="The password and cofirmation passwords do not match."
			if message!='':
				return message

		return message

	def login_validation(self, request):
		error = 'The email and password combination was not found.'
		if 'email' in request and 'password' in request:
			email = request['email'].strip().lower()
			password = request['password']
			if email=='' or password=='':
				error="Please enter both an email and password"
			else:
				user =  User.objects.filter(email=email)
				if (user):
					userinfo = User.objects.get(email=email)
					isfound = bcrypt.checkpw(request['password'].encode(), userinfo.password.encode())
					if isfound == True:
						return isfound

		return error

	def CheckUpperCase(self, val):
		isValid = False
		for i in range(0, len(val)):
			if val[i].isupper():
				return True
		return isValid

	def CheckNumeric(self, val):
		isValid = False
		for i in val:
			if i.isdigit():
				isValid = True
				return isValid
		return isValid

	def duplicateEmail(self, email):
		isDuplicate = False
		email = email.lower()
		checkemail = User.objects.all().filter(email=email)
		if checkemail:
			isDuplicate = True
		return isDuplicate


class User(models.Model):
	first_name = models.CharField(max_length=255, null=False)
	last_name = models.CharField(max_length=255, null=False)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	salt = models.CharField(max_length=255, null=False)
	created_at = models.DateTimeField(auto_now_add = True )
	updated_at = models.DateTimeField(auto_now = True )
	objects = UserManager()


class TripManager(models.Manager):
	def trip_validation(self, request):
		error=''
		if 'destination' in request and 'description' in request and 'start_date' in request and 'end_date' in request:
			if request['destination']=='':
				error = 'Please enter a destination'
			elif request['description']=='':
				error = 'Please enter a description'
			elif request['start_date']=='':
				error = 'Please enter a start date'
			elif request['end_date']=='':
				error = "Please enter an end date"
			else:
				start_date = datetime.strptime(request['start_date'], '%Y-%m-%d' )
				end_date = datetime.strptime(request['end_date'], '%Y-%m-%d' )
				if start_date < datetime.now():
					error = "Your start date must not be in the past"
				elif start_date >= end_date:
					error="Your start date of your trip must be earlier than your end date"
		else:
			error = "There was an error processing your request."
		return error

class Trip(models.Model):
	destination = models.CharField(max_length=255, null=True)
	description = models.TextField(null=True)
	planner = models.ForeignKey(User, related_name="planned", default=1)
	start_date = models.DateTimeField(null=True)
	end_date = models.DateTimeField(null=True)
	plan = models.TextField(null=True)
	created_at = models.DateTimeField(auto_now_add = True )
	updated_at = models.DateTimeField(auto_now = True )
	objects = TripManager()

class TripDetails(models.Model):
	user = models.ForeignKey(User, related_name="tripuser")
	trip = models.ForeignKey(Trip, related_name="tripplan")
	created_at = models.DateTimeField(auto_now_add = True )
	updated_at = models.DateTimeField(auto_now = True )





