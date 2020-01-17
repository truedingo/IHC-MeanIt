from django.contrib import admin

# Register your models here.
from meanit_app.models import Profile, Post, Questions

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Questions)