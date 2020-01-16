from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from meanit_app.forms import SignUpForm, CreatePostForm
from django.contrib.auth.hashers import make_password, check_password


# Create your views here.
from meanit_app.models import Profile, Post

class home_view(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('mainpage')
        signup_form = SignUpForm()
        return render(request, 'home.html', {"signup_form": signup_form})
    
    def post(self, request):
        signup_form = SignUpForm(request.POST)
        if signup_form.is_valid():
            signup_form = signup_form.save(commit=False)
            username = signup_form.username
            password = signup_form.password
            signup_form.password = make_password(password)
            signup_form.save()
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                posts = Post.objects.all()
                return render(request, 'main_page.html',{'posts': posts})
            else:
                print("Error registering user")
                return render(request, 'home.html', {"signup_form": signup_form})
        else:
            print("Not valid!")
            return render(request, 'home.html', {"signup_form": signup_form})


# Create your views here.
class feed_view(View):
    def get(self, request):
        #todo user verification
        posts = Post.objects.all()
        return render(request, 'feed.html',{'posts': posts})


class post_view(View):
    def get(self, request):
        if request.user.is_authenticated:
            createpost_form = CreatePostForm()
            return render(request, 'create_post.html', {'createpost_form': createpost_form})
        else:
            return redirect('home')
    def post(self, request):
        createpost_form = CreatePostForm(request.POST, request.FILES)
        if createpost_form.is_valid():
            createpost_form = createpost_form.save(commit=False)
            profile_user = request.user
            hashtag = createpost_form.hashtag
            h_list = hashtag.split(',')
            print(h_list)
            final = ''
            for each in h_list:
                if(each[0]!='#'):
                    final += ''+each+' '
                else:
                    final += each + ' '
            createpost_form.hashtag = final
            createpost_form.profile_user = profile_user
            createpost_form.save()
        else:
            print('failed')
        return redirect('home')


class main_page(View):
    def get(self, request):
        posts = Post.objects.all()
        return render(request, 'main_page.html', {'posts': posts})


class search_view(View):
    def get(self,request,query):
        users = Profile.objects.filter(username__contains=query)
        posts = Post.objects.filter(hashtag__contains=query)
        hashtags = []
        for each in posts:
            for w in each.hashtag.split(' '):
                if query in w and w[1:] not in hashtags:
                    print(w)
                    print(hashtags)
                    print('----------')
                    hashtags.append(w[1:])

        return render(request,'search_response.html',{'query': query,'users': users,'hashtags': hashtags})


class hashtag_view(View):
    def get(self,request,query):
        posts = Post.objects.filter(hashtag__contains=query)
        return render(request,'hashtag_feed.html',{'hashtag':query,'posts': posts})


def logout_view(request):
    logout(request)
    signup_form = SignUpForm()
    print("Logged out!")
    return redirect('home')
        
