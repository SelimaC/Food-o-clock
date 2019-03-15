from django import forms

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from foodoclock.models.UserDetails import UserDetails

class UserCreateForm(UserCreationForm):
    cousine = forms.CharField(max_length=50)
    diet = forms.CharField(max_length=50)
    country = forms.CharField(max_length=50)
    age = forms.IntegerField()

    class Meta:
        model = User
        fields = ("username", "cousine", "diet", "country", "age", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)

        if commit:
            user.save()
            UserDetails.newUserDetails(user, self.cleaned_data["cousine"], self.cleaned_data["diet"],
                                       self.cleaned_data["country"], self.cleaned_data["age"])
        return user
