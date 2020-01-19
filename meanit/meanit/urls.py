"""meanit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.urls import path
from django.contrib import admin
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from meanit_app import views
from meanit import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home_view.as_view(), name='home'),
    url(r'logout/', views.logout_view, name='logout'),
    url(r'^feed', views.feed_view.as_view(), name='feed'),
    url(r'^post', views.post_view.as_view(), name='post'),
    path('search/<slug:query>/', views.search_view.as_view(), name='search'),
    path('hashtag/<slug:query>/', views.hashtag_view.as_view(), name='hashtag'),
    path('user/<slug:query>/', views.profile_view.as_view(), name='profile'),
    url(r'^signup', views.signup_view.as_view(), name='signup'),
    url(r'^userprofileedit/', views.useredit_page.as_view(), name='edituser'),
    path('followuser/<slug:query>/', views.followuser_view.as_view(), name='hashtag'),
    path('newmessage',views.message_view.as_view(),name='newmessage'),
    path('inbox',views.inbox_view.as_view(),name='inbox')
]


urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)