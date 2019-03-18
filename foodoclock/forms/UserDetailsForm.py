from django import forms

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from foodoclock.models.UserDetails import UserDetails
from foodoclock.models.MealType import MealType
from foodoclock.models.Diet import Diet
from foodoclock.models.Cuisine import Cuisine

class UserCreateForm(UserCreationForm):
    cuisine = forms.ModelChoiceField(label='Cuisine', queryset=Cuisine.objects.all())
    diet = forms.ModelChoiceField(label='Diet', queryset=Diet.objects.all())
    country = forms.CharField(max_length=50)
    age = forms.IntegerField()

    class Meta:
        model = User
        fields = ("username", "cuisine", "diet", "country", "age", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)

        if commit:
            user.save()
            UserDetails.newUserDetails(user, self.cleaned_data["cuisine"], self.cleaned_data["diet"],
                                       self.cleaned_data["country"], self.cleaned_data["age"])
        return user
