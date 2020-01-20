from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from meanit_app.forms import SignUpForm, CreatePostForm, LoginForm, UserEditForm, QuestionForm, CreateMeanitQuestionForm, SendMessageForm,ReplyPostForm
from django.contrib.auth.hashers import make_password, check_password
from django.forms import formset_factory
from django.contrib import messages
from django.db.models import Q

from random import randint

# Create your views here.
from meanit_app.models import Profile, Post, Questions, Comments, MeanitUserQuestions, Message,Follow
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
        posts = Post.objects.all().exclude(profile_user=request.user)
        int = randint(1,6)
        with open('/Users/dingo/Desktop/Mestrado/IHC/mockups/texts/quotes.txt','r') as f:
            for i in range(int-1):
                f.readline()
                f.readline()
            quote = f.readline()
            author = f.readline()
        return render(request, 'new_feed.html',{'posts': posts,'quote': quote,'author': author})


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
            if '#1' in request.POST:
                createpost_form.hashtag = request.POST['#1']
            if '#2' in request.POST:
                createpost_form.hashtag2 = request.POST['#2']
            if '#3' in request.POST:
                createpost_form.hashtag3 = request.POST['#3']
            if '#4' in request.POST:
                createpost_form.hashtag4 =  request.POST['#4']
            if '#5' in request.POST:
                createpost_form.hashtag5 =  request.POST['#5']
            createpost_form.profile_user = Profile.objects.filter(username=request.user).first()
            createpost_form.save()
            return redirect('feed')
        else:
            print('failed')
        return redirect('home')

class onepost_view(View):
    def get(self, request, id):
        post = Post.objects.filter(pk=id).first()
        replyform = ReplyPostForm()
        replies = Comments.objects.all().filter(original_post=id)
        return render(request, 'post.html', {'post':post,'reply_form': replyform,'posts': replies})

    def post(self,request,id):
        createcomment_form = ReplyPostForm(request.POST, request.FILES)
        if createcomment_form.is_valid():
            createcomment_form = createcomment_form.save(commit=False)
            createcomment_form.profile_comment = Profile.objects.get(username=request.user)
            createcomment_form.original_post = Post.objects.filter(pk=id).first()
            createcomment_form.cmnt_read = False
            createcomment_form.save()
            post = Post.objects.filter(pk=id).first()
            replyform = ReplyPostForm()
            replies = Comments.objects.all().filter(original_post=id)
            return render(request, 'post.html', {'post': post, 'reply_form': replyform, 'posts': replies})

class main_page(View):
    def get(self, request):
        posts = Post.objects.all()
        return render(request, 'main_page.html', {'posts': posts})


class search_view(View):
    def post(self,request):
        query = request.POST['search_result']
        users = Profile.objects.all().filter(username__contains=query)
        posts = Post.objects.all()
        hashtags = []
        for each in posts:
            w = each.hashtag
            print(w)
            if w != None and query in w :
                    hashtags.append(w)
            w = each.hashtag2
            if w != None and query in w :
                    hashtags.append(w)
            w = each.hashtag3
            if w != None and query in w :
                    hashtags.append(w)
            w = each.hashtag4
            if w != None and query in w :
                    hashtags.append(w)
            w = each.hashtag5
            if w != None and query in w :
                    hashtags.append(w)
        return render(request,'search_response.html',{'query': query,'users': users,'hashtags': hashtags})


class hashtag_view(View):
    def get(self,request,query):
        posts = Post.objects.all().filter(Q(hashtag=query) |Q(hashtag2=query) |Q(hashtag3=query)|Q(hashtag4=query)|Q(hashtag5=query))
        return render(request,'new_feed.html',{'posts': posts})

class useredit_page(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('home')

        question_form = QuestionForm()
        answer_form = CreateMeanitQuestionForm()
        user_edit_form = UserEditForm()

        for post in Post.objects.filter(profile_user=request.user):
            for comment in Comments.objects.filter(original_post=post):
                if comment.cmnt_read == False:
                    messages.add_message(request, messages.INFO, str(post.profile_user) + " has commented on one of your posts", extra_tags=str(post.pk))
            
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
        questions = MeanitUserQuestions.objects.all().filter(profile_user=p)
        return render(request, 'profile.html', {'posts': posts_query, 'username':query, 'following': following, 'questions': questions})



class useredit_page(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('home')

        question_form = QuestionForm()
        answer_form = CreateMeanitQuestionForm()
        user_edit_form = UserEditForm()

        for post in Post.objects.filter(profile_user=request.user):
            for comment in Comments.objects.filter(original_post=post):
                if comment.cmnt_read == False:
                    messages.add_message(request, messages.INFO, str(post.profile_user) + " has commented on one of your posts", extra_tags=str(post.pk))
        
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
