from django.db import models
from foodoclock.models.Ingredient import Ingredient
from foodoclock.models.MealType import MealType
from foodoclock.models.Diet import Diet
from foodoclock.models.Cousine import Cousine


class Recipe(models.Model):
    auto_increment_id = models.AutoField(primary_key=True)

    meal_type = models.ForeignKey(MealType, on_delete=models.CASCADE)
    cousine = models.ForeignKey(Cousine, on_delete=models.CASCADE)
    diet = models.ForeignKey(Diet, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    rating = models.FloatField()
    link = models.CharField(max_length=200)
    corpus = models.CharField(max_length=10000)
    meta_description = models.CharField(max_length=500)
    preparation_time = models.IntegerField()
    image = models.ImageField()
    ingredients = models.ManyToManyField(Ingredient, blank=True)

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
    def getRecipesByCousine(cls, cousine):
        return Recipe.objects.filter(cousine=cousine)

    @classmethod
    def getRecipesByCousine(cls, cousine):
        return Recipe.objects.filter(cousine=cousine)

    @classmethod
    def getRecipesByMealType(cls, meal):
        return Recipe.objects.filter(meal_type=meal)

    @classmethod
    def getRecipesByDiet(cls, diet):
        return Recipe.objects.filter(diet=diet)

    def __str__(self):
        return "Title: " + str(self.title)