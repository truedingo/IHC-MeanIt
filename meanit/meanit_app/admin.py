from django.contrib import admin

# Register your models here.
from meanit_app.models import Profile, Post, Questions, MeanitUserQuestions, Comments

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Questions)
admin.site.register(MeanitUserQuestions)
admin.site.register(Comments)