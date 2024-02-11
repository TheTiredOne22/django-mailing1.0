from allauth.account.forms import SignupForm
from django import forms


class CustomSignUpForm(SignupForm):

    def __init__(self, *args, **kwargs):
        super(CustomSignUpForm, self).__init__(*args, **kwargs)

        self.fields['first_name'] = forms.CharField(label='First Name', required=True)
        self.fields['last_name'] = forms.CharField(label='Last Name', required=True)

    def save(self, request):
        user = super(CustomSignUpForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user
