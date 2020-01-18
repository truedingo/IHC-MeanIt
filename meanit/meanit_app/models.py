# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User


class Profile(User):
    class Meta:
        proxy = True
        ordering = ('username', )
    
    def __str__(self):
        return self.username



class Comments(models.Model):
    post_pic = models.CharField(max_length=512, blank=True, null=True)
    post_text = models.CharField(max_length=512, blank=True, null=True)
    cmnt_read = models.BooleanField(blank=True, null=True)
    cmnt_date = models.BooleanField(blank=True, null=True)
    profile_user = models.ForeignKey('Profile', on_delete = models.CASCADE)


class Follow(models.Model):
    username = models.CharField(unique=True, max_length=512, blank=True, null=True)
    hashtag = models.CharField(unique=True, max_length=512, blank=True, null=True)
    profile_user = models.ForeignKey('Profile', on_delete = models.CASCADE)


class MeanitUserQuestions(models.Model):
    profile_user = models.OneToOneField('Profile', models.CASCADE, primary_key=True)
    question = models.ForeignKey('Questions', on_delete = models.PROTECT, default = '')


class Message(models.Model):
    to_msg = models.CharField(unique=True, max_length=512)
    msg_text = models.CharField(max_length=512)
    msg_read = models.BooleanField(blank=True, null=True)
    msg_date = models.DateField()
    profile_user = models.ForeignKey('Profile', models.CASCADE)


class Post(models.Model):
    post_pic = models.ImageField(upload_to = 'images')
    post_text = models.CharField(max_length=512, blank=True, null=True)
    hashtag = models.CharField(max_length=512, blank=True, null=True)
    post_date = models.DateField(blank=True, null=True, auto_now_add=True)
    profile_user = models.ForeignKey('Profile', on_delete = models.CASCADE)

    def __str__(self):
        return "User: cx" + self.profile_user.username + " Post ID: " + str(self.pk)


class Questions(models.Model):
    question_name = models.CharField(unique=True, max_length=512)
    question_answer = models.CharField(max_length=512, blank=True, null=True)

    def __str__(self):
        return self.question_name
