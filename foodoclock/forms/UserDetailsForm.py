from django import forms

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from foodoclock.models.UserDetails import UserDetails
from foodoclock.models.MealType import MealType
from foodoclock.models.Diet import Diet
from foodoclock.models.Cousine import Cousine

class UserCreateForm(UserCreationForm):
    cousine = forms.ModelChoiceField(label='Cousine', queryset=Cousine.objects.all())
    diet = forms.ModelChoiceField(label='Diet', queryset=Diet.objects.all())
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
