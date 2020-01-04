from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from meanit_app.forms import SignUpForm
from django.contrib.auth.hashers import make_password, check_password


# Create your views here.
class home_view(View):
    def get(self, request):
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
                return render(request, 'main_page.html')
            else:
                print("Error registering user")
                return render(request, 'home.html', {"signup_form": signup_form})
        else:
            print("Not valid!")
            return render(request, 'home.html', {"signup_form": signup_form})

class main_page(View):
    def get(self, request):
        return render(request, 'main_page.html')


def logout_view(request):
    logout(request)
    signup_form = SignUpForm()
    print("Logged out!")
    return redirect('home')
        
