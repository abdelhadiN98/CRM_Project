from django.db import models
import re
from datetime import datetime

class EmployeeManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors["first_name"] = "first_name should be at least 2 characters"
        name_REGEX = re.compile(r'^[a-zA-Z]+$')
        if not name_REGEX.match(postData['first_name']):               
            errors['first_name'] = "first_name should be letters only"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "last_name should be at least 2 characters"
        if not name_REGEX.match(postData['last_name']):               
            errors['last_name'] = "last_name should be letters only"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):              
            errors['email'] = "Invalid email address!"
        if len(postData['password']) < 8 :
            errors["password"] = "password should be at least 8 characters"
        if  postData['password'] != postData['confirm_password']:
            errors["matching_password"] = "Password dose not match confirm PW"
        return errors

    def login_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['login_email']):              
            errors['login_email'] = "Invalid email address!"
        if len(postData['login_password']) < 8 :
            errors["login_password"] = "password should be at least 8 characters"
        return errors


class Employee(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    objects = EmployeeManager()

class Customer(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    managed_by = models.ForeignKey(Employee , related_name="customers_managed", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Service(models.Model):
    title=models.CharField(max_length=255)
    desc=models.TextField()
    managed_by = models.ForeignKey(Employee , related_name="services_managed", on_delete = models.CASCADE)
    customers_have_servives = models.ManyToManyField(Customer , related_name="have_services")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

