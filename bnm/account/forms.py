from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User, Advertisement_posting
from .validate import validate_instagram_account
import concurrent.futures


class CreateUserForm(UserCreationForm):
    privacy_policy_field = forms.BooleanField(help_text='I accept <a href="privacy-policy">privacy policy</a>',
                                              label='')

    class Meta:
        model = User
        fields = ['email', 'username', 'usertype', 'instagram_user_id', 'password1', 'password2', 'privacy_policy_field']

    def clean_instagram_user_id(self):
        instagram_user_id = self.cleaned_data.get('instagram_user_id')
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(validate_instagram_account, instagram_user_id)
            result = future.result()
        if result:
            return instagram_user_id
        else:
            raise forms.ValidationError('Wrong instagram user id')

class Advertisement_posting_form(ModelForm):
    class Meta:
        model = Advertisement_posting
        fields = ['title', 'description', 'platform']
