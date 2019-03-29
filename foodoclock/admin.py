from django.contrib import admin

from foodoclock.models.UserDetails import UserDetails
from foodoclock.models.Recipe import Recipe
from foodoclock.models.Favourite import Favourite
from foodoclock.models.Ingredient import Ingredient
from foodoclock.models.MealType import MealType
from foodoclock.models.Diet import Diet
from foodoclock.models.Cuisine import Cuisine
from foodoclock.models.TitleToken import TitleToken

admin.site.register(Recipe)
admin.site.register(UserDetails)
admin.site.register(Favourite)
admin.site.register(Ingredient)
admin.site.register(MealType)
admin.site.register(Diet)
admin.site.register(Cuisine)
admin.site.register(TitleToken)
