from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import RegexValidator

from models import Tapper

class CreateUserForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField(max_length=30)
    email = forms.EmailField(required=True)
    password = forms.CharField(max_length=30, widget=forms.PasswordInput())
    password_confirmation = forms.CharField(max_length=30, widget=forms.PasswordInput())

    def clean_username(self):
        try:
            User.objects.get(username=self.cleaned_data['username'])
        except ObjectDoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError("This username is taken")

    def clean_email(self):
        try:
            User.objects.get(email=self.cleaned_data['email'])
        except ObjectDoesNotExist:
            return self.cleaned_data['email']
        raise forms.ValidationError("This email is taken")

    def clean(self):
        if 'password' in self.cleaned_data and 'password_confirmation' in self.cleaned_data:
            if self.cleaned_data['password'] != self.cleaned_data['password_confirmation']:
                raise forms.ValidationError("Passwords do not match")

        return self.cleaned_data

    def save(self, commit=False):
        new_user = User.objects.create_user(self.cleaned_data['username'],
                                            self.cleaned_data['email'],
                                            self.cleaned_data['password'])
        new_user.first_name = self.cleaned_data['first_name']
        new_user.last_name = self.cleaned_data['last_name']
        if commit:
            new_user.save()
        return new_user

class CreateTapperForm(forms.Form):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = forms.CharField(validators=[phone_regex], max_length=16)

    def save(self, commit=False):
        tapper = Tapper(phone_number=self.cleaned_data['phone_number'])
        if commit:
            tapper.save()
        return tapper


# class UserForm(forms.ModelForm):
#     class Meta:
#         model=User
#         fields = ['first_name', 'last_name', 'username', 'email', 'password']
#     def clean_email(self):
#         data = self.cleaned_data['email']
#         if User.objects.filter(email=data).exists():
#             raise forms.ValidationError("This email already used")
#         return data
#     def save(self, commit=True):
#         user = super(UserForm, self).save(commit=False)
#         user.set_password(self.cleaned_data["password"])
#         if commit:
#             user.save()
#         return user
