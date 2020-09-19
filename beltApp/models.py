import re
from datetime import datetime
from django.db import models

import bcrypt

# Create your models here.
class UserManager(models.Manager):
    def register_validator(self, post_data):
        errors = {}

        if len(post_data['first_name']) < 2:
            errors["first_name"] = "Frist name should be at least 2 characters"

        if len(post_data['last_name']) < 2:
            errors["last_name"] = "Last name should be at least 2 characters"

        # email
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        # test whether a field matches the pattern
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = "Email/password is incorrect. Please try again."

        # password length
        if len(post_data['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"

        # check password == password confirm
        if (post_data['password'] != post_data['password_confirm']):
            errors['password_confirm'] = "Password confirm didn't match"

        user_list = User.objects.filter(email=post_data['email'])
        if (len(user_list) > 0):
            errors['email_password'] = 'Email/password is incorrect. Please try again.'
        return errors

    def login_validator(self, post_data):
        errors = {}
        # check the email format
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = "Invalid email format!"

        users_list = User.objects.filter(email=post_data['email'])
        # check the email is in the db
        if len(users_list) == 0:
            errors['email_password'] = "Email/password is incorrect. Please try again."
        else:
            # check the password
            if bcrypt.checkpw(
                post_data['password'].encode(),
                users_list[0].password.encode()
            ) != True:
                errors['email_password'] = "Email/password is incorrect. Please try again."
        return errors

    def wish_validator(self, post_data):
        errors = {}

        if len(post_data['wish_name']) < 3:
            errors["wish_name"] = "Wish should be at least 3 characters"

        if len(post_data['wish_desc']) < 3:
            errors["wish_desc"] = "Description should be at least 3 characters"

        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    liked_wishes = models.ManyToManyField('Wish', related_name='users_who_liked')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # wish uploaded_by
    # books_uploaded = a list of books uploaded by a given user
    objects = UserManager()

class Wish(models.Model):
    name = models.CharField(max_length=255)
    desc = models.TextField()
    uploaded_by = models.ForeignKey(User, related_name="wish", on_delete = models.CASCADE)
    #the user who uploaded a given book
    is_granted = models.BooleanField(default=False)
    # users_who_liked
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)