from django import forms
from .models import User

from django.contrib.auth.forms import UserCreationForm

class PofileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        
        user = kwargs.pop('user')
        super(PofileForm, self).__init__(*args, **kwargs)
        

        if not user.is_superuser:
                

            self.fields['username'].disabled = True
            self.fields['special_user'].disabled = True
            self.fields['email'].disabled = True
            self.fields['is_author'].disabled = True

            self.fields['username'].help_text = ''
        
        self.fields['username'].help_text = None
        

    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','special_user','is_author']


class SignupForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ['username', 'email', 'password1', 'password2']