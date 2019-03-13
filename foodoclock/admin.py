from django.contrib import admin

from foodoclock.models.UserDetails import UserDetails
from foodoclock.models.Recipe import Recipe
from foodoclock.models.Favourite import Favourite

admin.site.register(Recipe)
admin.site.register(UserDetails)
admin.site.register(Favourite)
