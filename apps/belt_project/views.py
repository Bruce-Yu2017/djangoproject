from __future__ import unicode_literals
from django.shortcuts import render,redirect
from django.contrib import messages
from models import*
import bcrypt

def index(request):
  request.session['log'] = False
  return render(request,"belt_project/index.html")

def login(request):
  if request.method == 'POST':
    request.session['log_reg'] = 'log'
    error = User.objects.login_check(request.POST)
    if len(error):
      messages.error(request, error, extra_tags="login")
      return redirect('/')
    else:
      request.session['log'] = True
      request.session['user_id'] = User.objects.get(email = request.POST['email']).id
      return redirect('/travel')
  return redirect('/')

def register(request):
  if request.method == "POST":
    request.session['log_reg']='reg'
    errors = User.objects.reg_validator(request.POST)
    if len(errors):
      for tag,error in errors.iteritems():
        messages.error(request,error,extra_tags=tag)
      return redirect('/')
    secure_password = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt())
    User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email = request.POST['email'],password = secure_password)
    request.session['log'] = True
    request.session['user_id'] = User.objects.last().id
    return redirect('/travel')
  return redirect('/')

def travel(request):
  if request.session['log']:
    users = User.objects.get(id=request.session['user_id'])
    others = User.objects.exclude(id=request.session['user_id'])
    trips = Trip.objects.all().order_by('created_at')
    context = {
      'users': users,
      'trips': trips,
      'others': others
    }
    return render(request, 'belt_project/travel_dashboard.html', context)

def addplan(request):
    return render(request, 'belt_project/addtrip.html')

def addtrip(request):
  if request.session['log']:
    errors = Trip.objects.trip_check(request.POST)
    if len(errors):
      for tag, error in errors.iteritems():
        messages.error(request,error,extra_tags=tag)
      return redirect('/travel/add')
    else:
      Trip.objects.create(destination = request.POST['destination'], description = request.POST['description'], travel_date_from = request.POST['begindate'], travel_date_to = request.POST['enddate'])
      return redirect('/travel')

  return redirect('/')

def showtrip(request, usertrip_id):
  othertrip = Trip.objects.filter(id=usertrip_id)
  if othertrip:
    bulider = othertrip.user 
    context = {
      'othertrip': othertrip,
      'bulider': bulider
    }
    return render(request, 'belt_project/destination.html', context)
  return redirect('/travel')

def join(request, joiner_id):
  joiner = User.objects.filter(id=joiner_id)
  context = {
    'joiners': joiner 
  }
  return redirect(request, 'belt_project/destination.html', context)

def logout(request):
  logout(request)
  return redirect('/')





