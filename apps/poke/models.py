from __future__ import unicode_literals
from django.db import models
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

#managers
class UserManager(models.Manager):
    def validation(self, email, password, conf_password, name, alias, bday):
        fields=[]
        if not EMAIL_REGEX.match(email):
            fields.append("Email is invalid")
        if len(name) < 1:
            fields.append("Full name is required")
        if len(alias) < 1:
            fields.append("An alias is required")
        if len(password) < 8:
            fields.append("Password must be at least 8 characters")
        if len(conf_password) < 8:
            fields.append("Password confirmation is required and must match")
        if password != conf_password:
            fields.append("Password confirmation must match")
        if email == Users.objects.filter(email=email):
            fields.append("Email already exists, please go to login")
        if len(fields) > 0:
            return fields
        elif fields == False:
            fields.append("Registration successful")
            return fields

    def login(self, email, password):
        l_fields=[]

        try:
            user = Users.objects.get(email=email)
            if user.pw_hash == bcrypt.hashpw(password.encode(), user.pw_hash.encode()):
                return user
            else:
                l_fields.append("Incorrect password")
        except:
            l_fields.append("Email does not match our records")
        return l_fields
#models
class Users(models.Model):
    name = models.CharField(max_length=45)
    alias = models.CharField(max_length=45)
    pw_hash=models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    bday = models.CharField(max_length=45)
    total_pokes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects=UserManager()

class Pokes(models.Model):
    user = models.ForeignKey(Users, related_name="user")
    poked_by = models.ForeignKey(Users, related_name="poker")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
