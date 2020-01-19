from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from meanit_app.forms import SignUpForm, CreatePostForm, LoginForm, UserEditForm, QuestionForm, CreateMeanitQuestionForm, SendMessageForm
from django.contrib.auth.hashers import make_password, check_password


# Create your views here.
from meanit_app.models import Profile, Post, Follow, Questions, MeanitUserQuestions, Message

class home_view(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('feed')
        else:
            login_form = LoginForm()
            return render(request, 'home.html', {"login_form": login_form})
    
    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('feed')
            else:
                return redirect('home')
        else:
            return render(request, 'home.html', {"login_form": login_form})

class signup_view(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('feed')
        else:
            signup_form = SignUpForm()
            return render(request, 'signup.html', {'signup_form': signup_form})

    def post(self, request):
        signup_form = SignUpForm(request.POST)
        print(signup_form)
        if signup_form.is_valid():
            signup_form = signup_form.save(commit=False)
            username = signup_form.username
            password = signup_form.password
            signup_form.password = make_password(password)
            signup_form.save()
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('feed')
            else:
                return redirect('signup')
        else:
            return render(request, 'signup.html', {'signup_form': signup_form})

# Create your views here.
class feed_view(View):
    def get(self, request):
        posts = Post.objects.all()
        '''profile_user = Profile.objects.get(username=request.user)
        follow_list = Follow.objects.filter(profile_user=profile_user)
        for followers in follow_list:
            prof = Profile.objects.get(profile_user=followers.username)
            hashtag = follow_list.hashtag
            follow_post = Post.objects.filter()
        '''
        return render(request, 'new_feed.html',{'posts': posts})


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
            profile_user = Profile.objects.get(username = request.user)
            createpost_form = createpost_form.save(commit=False)
            final = ''
            if '#1' in request.POST:
                h1 = request.POST['#1']
                final+= '#'+h1
            if '#2' in request.POST:
                h2 = request.POST['#2']
                final+= ', #'+h2
            if '#3' in request.POST:
                h3 = request.POST['#3']
                final+= ', #'+h3
            if '#4' in request.POST:
                h4 = request.POST['#4']
                final+= ', #'+h4
            if '#5' in request.POST:
                h5 = request.POST['#5']
                final+= ', #'+h5
            createpost_form.hashtag = final
            createpost_form.profile_user = profile_user
            createpost_form.save()
            return redirect('feed')
        else:
            return redirect('post')


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
        posts = Post.objects.filter(hashtag__contains=query+' ')
        return render(request,'hashtag_feed.html',{'hashtag':query,'posts': posts})

class useredit_page(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('home')
        user_edit_form = UserEditForm()
        return render(request, 'profile_page.html', {"user_edit_form": user_edit_form})

    def post(self, request):
        user_edit_form = UserEditForm(request.POST)
        user = request.user
        if user_edit_form.is_valid() and user.check_password(user_edit_form.data['old_password']):
            username = user_edit_form.data['new_username']
            password = user_edit_form.data['new_password']
            user.password = make_password(user_edit_form.data['new_password'])
            user.username = user_edit_form.data['new_username']
            user.email = user_edit_form.data['new_email']
            user.save()
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return redirect('edituser')
        else:
            #meter erro aqui
            print('erro')
            return redirect('home')


def logout_view(request):
    logout(request)
    signup_form = SignUpForm()
    print("Logged out!")
    return redirect('home')

class profile_view(View):
    def get(self, request,query):
        user = Profile.objects.get(username=query)
        posts_query = Post.objects.all().filter(profile_user=user)
        p = Profile.objects.get(username = request.user)
        following = True if Follow.objects.all().filter(profile_user=p,username=query) else False
        return render(request, 'profile.html', {'posts': posts_query, 'username':query, 'following': following})



class useredit_page(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('home')

        question_form = QuestionForm()
        answer_form = CreateMeanitQuestionForm()
        user_edit_form = UserEditForm()
        return render(request, 'profile_page.html', {"question_form": question_form, "user_edit_form": user_edit_form, "answer_form": answer_form})

    def post(self, request):
        user_edit_form = UserEditForm(request.POST)
        user = request.user
        user_question_form = QuestionForm(request.POST)
        user_question_form2 = CreateMeanitQuestionForm(request.POST)

        if user_question_form.is_valid() and user_question_form2.is_valid():
            user_question_form2 = user_question_form2.save(commit=False)
            question_name = user_question_form.cleaned_data['question_name'].question_name
            profile_user = Profile.objects.get(username=request.user)
            question = Questions.objects.get(question_name=question_name)
            user_question_form2.profile_user = profile_user
            user_question_form2.question_name = question_name
            user_question_form2.save()
            return redirect('home')

        if user_edit_form.is_valid() and user.check_password(user_edit_form.data['old_password']):
            username = user_edit_form.data['new_username']
            password = user_edit_form.data['new_password']
            user.password = make_password(user_edit_form.data['new_password'])
            user.username = user_edit_form.data['new_username']
            user.email = user_edit_form.data['new_email']
            user.birthday = user_edit_form.data['new_birthday']
            user.save()
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return redirect('edituser')
        else:
            #meter erro aqui
            print('erro')
            return redirect('home')


class followuser_view(View):
    def get(self, request,query):
        if not request.user.is_authenticated:
            return redirect('home')
        p = Profile.objects.get(username = request.user)
        following = Follow.objects.all().filter(profile_user = p,username = query)
        if(len(following)==0):
            Follow(hashtag=None,username=query,profile_user =p).save()
            return redirect('profile', query=query)

        else:
            following.delete()
            return redirect('profile',query=query)


class message_view(View):
    def get(self, request):
        if request.user.is_authenticated:
            sendmessage_form = SendMessageForm()
            messages = Message.objects.all().filter(to_msg=request.user.username)
            return render(request, 'send_message.html', {'sendmessage_form': sendmessage_form})
        else:
            return redirect('home')

    def post(self,request):
        sendmessage_form = SendMessageForm(request.POST)
        if sendmessage_form.is_valid():
            sendmessage_form = sendmessage_form.save(commit=False)
            profile_user = Profile.objects.get(username=request.user)
            sendmessage_form.profile_user = profile_user
            sendmessage_form.msg_read = False
            sendmessage_form.save()
        else:
            print('failed')
        return redirect('home')

class inbox_view(View):
    def get(self,request):
        if request.user.is_authenticated:
            messages = Message.objects.all().filter(to_msg=request.user.username)
            return render(request, 'inbox.html', {'messages': messages})