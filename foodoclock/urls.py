"""foodoclock URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from django.contrib.auth import views as auth_views

from foodoclock.views import FavouritesView
from foodoclock.views import AccountDetailsView
from foodoclock.views import HomeView, SignUpView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', HomeView.home, name='home'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name= 'login.html', redirect_authenticated_user= '/'), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), {'next_page': 'login'}, name='logout'),
    url(r'^signup/$', SignUpView.signup, name='signup'),
    url(r'^account/$', AccountDetailsView.show, name='account'),
    url(r'^favourites/$', FavouritesView.list, name='favourites')
]
