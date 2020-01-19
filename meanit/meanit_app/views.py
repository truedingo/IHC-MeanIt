from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from meanit_app.forms import SignUpForm, CreatePostForm, LoginForm, UserEditForm, QuestionForm, CreateMeanitQuestionForm
from django.contrib.auth.hashers import make_password, check_password
from django.forms import formset_factory
from django.contrib import messages


# Create your views here.
from meanit_app.models import Profile, Post, Questions, Comments

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
            createpost_form.profile_user = Profile.objects.filter(username=request.user).first()
            createpost_form.save()
        else:
            print('failed')
        return redirect('home')

class onepost_view(View):
    def get(self, request, query):
        post = Post.objects.filter(pk=query).first()
        return render(request, 'post.html', {'post':post})

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
        posts = Post.objects.filter(hashtag__contains=query+' ')
        return render(request,'hashtag_feed.html',{'hashtag':query,'posts': posts})

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
                    messages.add_message(request, messages.INFO, str(post.pk))
            
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
            '''
            question_name = user_question_form.cleaned_data['question_name'].question_name
            question_answer = user_question_form.cleaned_data['question_answer']
            profile_user = Profile.objects.get(username=request.user)
            meanit_question = CreateMeanitQuestionForm()
            meanit_question.profile_user = profile_user
            meanit_question.question_name = question_name
            meanit_question.question_answer = question_answer
            meanit_question.save()
            '''
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
    def get(self, request):
        posts_query = Post.objects.filter(profile_user=request.user)
        return render(request, 'my_profile.html', {'posts': posts_query})
        
