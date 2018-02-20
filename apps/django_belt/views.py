from django.shortcuts import render, redirect, HttpResponse
from models import *
from datetime import datetime, timedelta

def index(request):
	
	return render(request, "django_belt/index.html")

def join(request, trip_id):
	
	trip_id = int(trip_id)
	addtrip = TripDetails.objects.create(trip_id=trip_id, user_id=request.session['user_id'])

	messages.add_message(request, messages.INFO, "You have successfully added this event")

	# return render(request, "django_belt/main.html")
	return redirect("/main")
def main(request):
	if (valid_session(request)==False):
		return redirect('/')
	else:
		context={}
		alluser = TripDetails.objects.filter(user_id=request.session['user_id'])
		alltrips = Trip.objects.all()
		allusers = User.objects.all()
		othertrips = Trip.objects.exclude(planner_id=request.session['user_id'])
		context = {
			'alltrips': alltrips,
			'alluser': alluser,
			'othertrips': othertrips,
			'allusers': allusers
		}
	return render(request, "django_belt/main.html", context)

def submittrip(request):
	if request.method=="POST":
		error = Trip.objects.trip_validation(request.POST)
		if error=='':
			# clean up request data
			destination = request.POST['destination'].strip()
			description = request.POST['description'].strip()
			start_date = datetime.strptime(request.POST['start_date'], '%Y-%m-%d' )
			end_date = datetime.strptime(request.POST['end_date'], '%Y-%m-%d' )
			
			adduser = User.objects.get(id=request.session['user_id'])
			newtrip = Trip.objects.create(destination=destination, description=description, planner=adduser, start_date=start_date, end_date=end_date)
			addeduser = TripDetails.objects.create(user_id=request.session['user_id'], trip_id=newtrip.id)	
			messages.add_message(request, messages.INFO, "Your trip has been added ")
		else:
			messages.add_message(request, messages.INFO, error)
			return render(request, "django_belt/addtrip.html")
	return redirect("/main")

def addtrip(request):
	return render(request, "django_belt/addtrip.html")


def tripdetails(request, trip_id):
	context = {}
	trip_id = int(trip_id)
	tripinfo = Trip.objects.filter(id=trip_id)
	usersjoining = TripDetails.objects.filter(trip_id=trip_id)
	allusers = User.objects.all()

		
	if tripinfo:
		tripinfo = Trip.objects.get(id=trip_id) #requery so that i dont have to do the error checking
		context = {
			'id': tripinfo.id,
			'destination': tripinfo.destination,
			'description': tripinfo.description,
			'start_date': tripinfo.start_date,
			'end_date': tripinfo.end_date,
			'planned_id': tripinfo.planner_id,
			'usersjoining': usersjoining,
			'allusers' : allusers
		}
	else:
		messages.add_message(request, messages.INFO, "There were no trips by that id number")
	return render(request, "django_belt/tripdetails.html", context)

def login(request):
	#check the login credentials
	formdata={}
	if request.method=='POST':
		email = request.POST['email'].strip().lower()
		password = request.POST['password'].strip()
		validlogin = User.objects.login_validation(request.POST)
		if validlogin == True:
			user = User.objects.get(email=email)
			request.session['user_id'] = user.id
			return redirect('/main')
		else:
			messages.add_message(request, messages.INFO, validlogin)
	else:
		formdata={}
		if 'email' in request.POST:
			formdata={'loginemail': request.POST['email'].strip().lower()}
	return render(request, 'django_belt/index.html', formdata)
	

def register(request):
	formdata={}
	if request.method=='POST':
		error = User.objects.registration_validation(request.POST)
		first_name = request.POST['first_name'].strip()
		last_name = request.POST['last_name'].strip()
		email = request.POST['email'].strip().lower()
		password = request.POST['password'].strip()
		formdata={ #send this basic information back -- Do not return sensitive information -- this is to populate the form
			'first_name': first_name,
			'last_name': last_name,
			'email': email
		}
		if len(error)!=0:
			messages.add_message(request, messages.INFO, error)
		else:
			password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
			user_id = User.objects.create(first_name=first_name , last_name=last_name, email=email , password=password)
			if (user_id.id):
				messages.add_message(request, messages.INFO, "You registered succesfully!")
				request.session['user_id'] = user_id.id
			return redirect('/main')
	else:
		messages.add_message(request, messages.INFO, "You must first login to access this site")
		request.session.clear()
		
	return render(request, 'django_belt/index.html', formdata)

def logout(request):
	request.session['user_id']=0
	return redirect('/')

def valid_session(request):
	isValid = True
	if ('user_id' not in request.session):
		request.session.clear()
		isValid = False
	else:
		if request.session['user_id']==0:
			request.session.clear()
			isValid = False

	return isValid