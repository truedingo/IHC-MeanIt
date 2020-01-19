from django import forms
from meanit_app.models import Profile, Post, Questions, MeanitUserQuestions, Comments
from django.contrib.auth.models import User

class SignUpForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': "caixa1", 'placeholder':'username', }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': "caixa1", 'placeholder': 'password'}))
    password_check = forms.CharField(widget=forms.PasswordInput(attrs={'class': "caixa1", 'placeholder': 'password confirmation'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': "caixa1", 'placeholder': 'email'}))
    birthday = forms.DateField(widget=forms.DateInput(attrs={'class': "caixa1", 'placeholder': 'birthday', 'type': 'date'}))
    class Meta:
        model = Profile
        fields = ('username', 'email', 'birthday' , 'password', 'password_check')
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

class LoginForm(forms.Form):
    username = forms.EmailField(widget=forms.TextInput(attrs={'class': "caixa1", 'placeholder':'username', }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': "caixa1", 'placeholder': 'password'}))


class UserEditForm(forms.Form):
    new_username = forms.CharField(label='New Username', widget=forms.TextInput(attrs={'class': "form-control"}),)
    new_email = forms.EmailField(label='New Email', widget=forms.TextInput(attrs={'class': "form-control"}),)
    old_password = forms.CharField(label="Old Password", widget=forms.PasswordInput(attrs={'class': "form-control"}),)
    new_password = forms.CharField(label="New Password", widget=forms.PasswordInput(attrs={'class': "form-control"}),)
    new_birthday = forms.DateField(widget=forms.DateInput(attrs={'class': "caixa1", 'placeholder': 'birthday', 'type': 'date'}))


class QuestionForm(forms.Form):
    question_name =  forms.ModelChoiceField(queryset=Questions.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}), required=True)

class CreateMeanitQuestionForm(forms.ModelForm):
    class Meta:
        model = MeanitUserQuestions
        fields = ('question_answer',)