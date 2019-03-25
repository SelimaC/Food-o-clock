from django.db import models
from foodoclock.models.Ingredient import Ingredient
from foodoclock.models.MealType import MealType
from foodoclock.models.Diet import Diet
from foodoclock.models.Cuisine import Cuisine
from django.db.models import Q

class Recipe(models.Model):
    auto_increment_id = models.AutoField(primary_key=True)

    meal_type = models.ForeignKey(MealType, on_delete=models.CASCADE, blank=True, null=True)
    cuisine = models.ForeignKey(Cuisine, on_delete=models.CASCADE, blank=True, null=True)
    diet = models.ForeignKey(Diet, on_delete=models.CASCADE, blank=True, null=True)

    title = models.CharField(max_length=500)
    rating = models.FloatField(default=0)
    link = models.CharField(max_length=500)
    image_url = models.CharField(max_length=500,blank=True)
    corpus = models.CharField(max_length=10000, blank=True)
    meta_description = models.CharField(max_length=1000, blank=True)
    preparation_time = models.IntegerField(blank=True)
    cook_time = models.IntegerField(blank=True, default=0)
    ingredients = models.ManyToManyField(Ingredient, blank=True)
    ingredients_list = models.CharField(max_length=10000, blank=True)
    click=models.IntegerField(default=0)

    @classmethod
    def getRecipeById(cls, id):
        return Recipe.objects.get(auto_increment_id=id)

    @classmethod
    def getRecipeByTitle(cls, title):
        return Recipe.objects.get(title=title)

    @classmethod
    def getRecipeByLink(cls, link):
        return Recipe.objects.get(link=link)

    @classmethod
    def getRecipesByCusine(cls, cuisine):
        return Recipe.objects.filter(cusine=cuisine)


    @classmethod
    def getRecipesByMealType(cls, meal):
        return Recipe.objects.filter(meal_type=meal)

    @classmethod
    def getRecipesByDiet(cls, diet):
        return Recipe.objects.filter(diet=diet)

    @classmethod
    def getRecipesByIngredients(cls, ingredients):
        return Recipe.objects.filter(ingredients__in=ingredients)

    @classmethod
    def getRecipesMatchingIngredients(cls, not_ingredients, ingredients):
        return Recipe.objects.filter(ingredients__in=ingredients).exclude(ingredients__in=not_ingredients)

    def __str__(self):
        return "Title: " + str(self.title)