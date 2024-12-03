# accounts/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import CustomUser, Task

CustomUser = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email',)

class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label='メールアドレス',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='パスワード',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'target_date', 'target_hours', 'start_tag', 'end_tag']
        widgets = {
            'target_date': forms.DateInput(attrs={'type': 'date'}),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['twitter_username']
