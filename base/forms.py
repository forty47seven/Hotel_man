from django.forms import ModelForm
from .models import GymUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class GymForm(ModelForm):
    class Meta():
        model = GymUser
        fields = ['membership_group', 'trainer', 'customer', 'subscription']

class CreateUserForm(UserCreationForm):
    class Meta():
        model = User
        fields = ['username', 'email', 'password1', 'password2']
