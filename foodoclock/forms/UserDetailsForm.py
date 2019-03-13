from django import forms



class UserDetailsForm(forms.Form):
    code = forms.CharField(max_length=50)
    cousine = forms.CharField(max_length=50)
    diet = forms.CharField(max_length=50)
    country = forms.CharField(max_length=50)
    age = forms.IntegerField()
