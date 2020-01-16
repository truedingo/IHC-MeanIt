from django import forms
from meanit_app.models import Profile, Post
from django.contrib.auth.models import User

class SignUpForm(forms.ModelForm):
    username = forms.CharField(label="Username", widget=forms.TextInput())
    password_check = forms.CharField(label="Password Confirmation", widget=forms.PasswordInput())
    email = forms.EmailField(label="Email")
    class Meta:
        model = Profile
        fields = ('username', 'email', 'password', 'password_check')
        widgets = {'password': forms.PasswordInput()}
    
    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        pass1 = cleaned_data.get('password_check')
        pass2 = cleaned_data.get('password')
        if pass1 != pass2:
            raise forms.ValidationError("The two password fields must match.")
        return cleaned_data


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('post_pic', 'post_text', 'hashtag')