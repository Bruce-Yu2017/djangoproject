from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
# Create your models here.
NAME_REGEX = re.compile(r'^[A-Za-z]+$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
  def reg_validator(self,postData):
    errors = {}
    if "first_name" not in postData or not NAME_REGEX.match(postData['first_name']):
      errors['first_name'] = "Please enter a valid first name"
    if "last_name" not in postData or not NAME_REGEX.match(postData['last_name']):
      errors['last_name'] = "Please enter a valid last name"
    if "email" not in postData or not EMAIL_REGEX.match(postData['email']):
      errors['email'] = "Please enter a valid email"
    if 'password' not in postData or len(postData['password'])<8:
      errors['password'] = "Password must have at least 8 characters"
    elif "confirm" not in postData or postData['password'] != postData['confirm']:
      errors['password'] = "Please enter your password again"
    if not len(errors):
      users = User.objects.filter(email = postData['email'])
      if users:
        errors['email'] = "Please enter a valid email"
    return errors

  def login_check(self,postData):
    error = {}
    users = User.objects.filter(email = postData['email'])
    if not users or not bcrypt.checkpw(postData['password'].encode(),users[0].password.encode()):
      error['login'] = "Email and password not match"
    return error

class TripManage(models.Manager):
  def trip_check(self, postData):
    errors = {}
    if len(postData['destination']) <1:
      errors['destination'] = "Please enter a valid destination"
    if len(postData['description']) <1:
      errors['description'] = "Please enter a valid description"
    return errors


class User(models.Model):
  first_name = models.CharField(max_length=255)
  last_name = models.CharField(max_length=255)
  email = models.CharField(max_length=255)
  password = models.CharField(max_length=255)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = UserManager()

class Trip(models.Model):
  destination = models.CharField(max_length=255)
  description = models.TextField()
  travel_date_from = models.DateTimeField(auto_now_add=True)
  travel_date_to = models.DateTimeField(auto_now_add=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  user = models.ForeignKey(User, related_name = "trips")
  objects = TripManage()













