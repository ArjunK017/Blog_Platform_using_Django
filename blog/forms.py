from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post



class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['username'].label = 'Username'  # Update the label text and style
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].label = 'Email'
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].label = 'Password'
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].label = 'Re Enter Password'  # Update the label text and style
        # Similarly, update label and style for other fields



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']