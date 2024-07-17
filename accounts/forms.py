from django import forms
from django.contrib.auth.models import User
from . models import Account
from django.core.exceptions import ValidationError
# customize:
class RegistationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholter': 'Enter Password',
        'class': 'form-control',
    }))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholter': 'Confirm Password',
    }))
    class Meta:
        model = Account
        fields = ['first_name','last_name','phone_number','email','password']

# amra akn a akta function Create korbo jar kaj  hoibo amra jodi password ar jaigai je password dibo oita oita jodi amra confirm_password ar same password nah diye taki tahole amader akta error dibe jeno amara same password diyr taki
    def clean(self):
        cleaned_data = super(RegistationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError(
                "Password dosen't Match"
            )

    def __init__(self, *args, **kwargs):
        super(RegistationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter Your First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Your Last Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Your Email'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Your Number'
        self.fields['password'].widget.attrs['placeholder'] = 'Enter Your Password'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
