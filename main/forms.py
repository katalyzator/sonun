from django import forms
from captcha.fields import ReCaptchaField
from django.core.exceptions import ValidationError

from .utils import validNumber
from .models import Subscribe

from django.utils.translation import ugettext_lazy as _

class SendLetter(forms.Form):

    fullname = forms.CharField(max_length=60, 
        widget=forms.TextInput(attrs={'class' : 'uk-input', 'placeholder' : _('Fullname')}))
    telephone = forms.CharField(max_length=14, 
        widget=forms.TextInput(attrs={'class' : 'uk-input', 'placeholder' : _('Telephone')}))
    email = forms.CharField(max_length=60, 
        widget=forms.EmailInput(attrs={'class' : 'uk-input', 'placeholder' : 'E-mail'}))
    captcha = ReCaptchaField(attrs={
        'theme' : 'dark',
        'lang' : 'ru'
    })

class Subscription(forms.Form):

    email = forms.CharField(max_length=60, 
        widget=forms.EmailInput(attrs={'class' : 'uk-input emailSubscribtion', 'placeholder' : _('Your E-mail')}))

    # def clean_email(self):
    #     email = self.cleaned_data['email']
    #     try:
    #         Subscribe.objects.get(email=email)
    #     except User.DoesNotExist:
    #         return email
    #     raise forms.ValidationError("email already taken.")

    #     return email