from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class RegistrationForm(UserCreationForm):
    full_name = forms.CharField(max_length=150, required=True)
    class Meta:
        model = User
        fields = ('email','full_name')

class ThemeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('display_mode',)


class SignupExtraForm(forms.Form):
    """Additional fields collected by the allauth signup flow."""

    full_name = forms.CharField(max_length=150, required=True)

    def signup(self, request, user):
        user.full_name = self.cleaned_data['full_name']
        user.save(update_fields=['full_name'])
