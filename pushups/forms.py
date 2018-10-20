from django import forms
from .models import Player

class AddPushupForm(forms.Form):
    
    class Meta:
        model = Player
        fields = ('pushups_done')

class LoginForm(forms.Form):
    username = forms.CharField(label="User Name", max_length=64)
    password = forms.CharField(widget=forms.PasswordInput())
