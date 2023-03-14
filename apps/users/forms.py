import re
from django.core.exceptions import ValidationError
from django import forms
from apps.users.models import MyUser


# mobile number validator
def mobile_validate(value):
    mobile_re = re.compile(r'^0?(13|14|15|18|17)[0-9]{9}$')
    if not mobile_re.match(value):
        raise ValidationError('the formate of mobile number has some problems')


# user register form
class UserRegForm(forms.Form):
    username = forms.CharField(label='username', min_length=6,
                               widget=forms.widgets.TextInput(
                                   attrs={'class': 'form-control', 'placeholder': 'please input username'}),
                               error_messages={'required': 'username cannot be empty',
                                               'min_length': 'the length of username at least is 6 digit'})
    password = forms.CharField(label="password", max_length=10,
                               widget=forms.widgets.PasswordInput(
                                   render_value=True,
                                   attrs={"class": "form-control"},
                               ),
                               error_messages={'max_length': 'the max length of password is 10 digit',
                                               'required': 'password cannot be empty',
                                               'min_length': 'the length of password at least is 6 digit'})
    re_password = forms.CharField(label="re_password", max_length=10,
                                  widget=forms.widgets.PasswordInput(
                                      attrs={"class": "form-control"}, render_value=True),
                                  error_messages={
                                      'max_length': 'the max length of password is 10 digit',
                                      'required': 'password cannot be empty',
                                      'min_length': 'the length of password at least is 6 digit'})
    mobile = forms.CharField(label='mobile_number', validators=[mobile_validate], widget=forms.widgets.NumberInput(
        attrs={'class': 'form-control', 'placeholder': 'please input your mobile number'}),
                             error_messages={'invalid': 'Please enter a valid bid'})
    email = forms.CharField(label='email', min_length=4, max_length=50, widget=forms.widgets.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'please input email address'}),
                            error_messages={
                                'min_length': 'the length of email at least is 6 digit',
                                'max_length': 'the max length of email is 64'
                            })

    def clean_username(self):
        new_username = self.cleaned_data.get("username")
        users = MyUser.objects.all()
        for user in users:
            if user.username == new_username:
                self.add_error("username", ValidationError("the username has been existed"))

    def clean(self):
        password = self.cleaned_data.get("password")
        re_password = self.cleaned_data.get("re_password")
        if len(password) < 6:
            self.add_error("re_password", ValidationError("The password should at least 6 digital "))
        if len(re_password) < 6:
            self.add_error("re_password", ValidationError("The re_password should at least 6 digital "))
        print(password)
        if not any(char.isupper() for char in password):
            self.add_error("password", ValidationError(
                'This password must contain at least 1 uppercase character'))
        if not any(char.isdigit() for char in password):
            self.add_error("password", ValidationError(
                'This password must contain at least 1 digit'))
        if password != re_password:
            # raise forms.ValidationError("The two passwords are different")
            self.add_error("re_password", ValidationError("The two passwords are different"))

    def clean_email(self):
        new_email = self.cleaned_data.get("email")
        users = MyUser.objects.all()
        for user in users:
            if user.email == new_email:
                self.add_error("email", ValidationError("the email address has been existed"))


class UserChangePasswordForm(forms.Form):
    original_password = forms.CharField(label="original_password",  max_length=10,
                                        widget=forms.widgets.PasswordInput(
                                            render_value=True,
                                            attrs={"class": "form-control"},
                                        ),
                                        error_messages={'max_length': 'the max length of original password is 10 digit',
                                                        'required': 'original password cannot be empty',
                                                        'min_length': 'the length of original password at least is 6 digit'})

    new_password = forms.CharField(label="new_password",  max_length=10,
                                   widget=forms.widgets.PasswordInput(
                                       render_value=True,
                                       attrs={"class": "form-control"},
                                   ),
                                   error_messages={'max_length': 'the max length of new password is 10 digit',
                                                   'required': 'new password cannot be empty',
                                                   'min_length': 'the length of new password at least is 6 digit'})

    re_password = forms.CharField(label="re_password", max_length=10,
                                  widget=forms.widgets.PasswordInput(
                                      attrs={"class": "form-control"}, render_value=True),
                                  error_messages={
                                      'max_length': 'the max length of password is 10 digit',
                                      'required': 'password cannot be empty',
                                      'min_length': 'the length of password at least is 6 digit'})

    def clean(self):
        original_password = self.cleaned_data.get("original_password")
        password = self.cleaned_data.get("new_password")
        re_password = self.cleaned_data.get("re_password")
        if len(password) < 6:
            self.add_error("re_password", ValidationError("The password should at least 6 digital "))
        if len(re_password) < 6:
            self.add_error("re_password", ValidationError("The re_password should at least 6 digital "))
        if password != re_password:
            # raise forms.ValidationError("The two passwords are different")
            self.add_error("re_password", ValidationError("The two passwords are different"))
        if not any(char.isupper() for char in password):
            self.add_error("re_password", ValidationError('This password must contain at least 1 uppercase character'))
        if not any(char.isdigit() for char in password):
            self.add_error("re_password",
                           ValidationError('This password must contain at least 1 digit'))





