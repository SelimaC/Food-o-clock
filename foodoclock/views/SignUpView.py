from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from foodoclock.models.UserDetails import UserDetails
from foodoclock.forms.UserDetailsForm import UserCreateForm

def signup(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            return redirect('home')
    else:
        form = UserCreateForm()
    return render(request, 'signup.html', {'form': form, 'signup': True})
