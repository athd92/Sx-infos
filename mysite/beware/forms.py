from django.contrib.auth.forms import UserCreationForm
from django import forms



class UserCustomLoginForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super(UserCustomLoginForm, self).__init__(*args, **kwargs)

        for fieldname in ["username", "email", "password1", "password2"]:
            self.fields[fieldname].help_text = None

    def save(self, commit=True):
        user = super(UserCustomLoginForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class ContactForm(forms.Form):
    contact_name = forms.CharField(required=True)
    contact_email = forms.EmailField(required=True)
    content = forms.CharField(
        required=True,
        widget=forms.Textarea
    )