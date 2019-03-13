from django.db import models


class Recipe(models.Model):
    auto_increment_id = models.AutoField(primary_key=True)
    meal_type = models.CharField(max_length=50)
    cousine = models.CharField(max_length=50)
    diet = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    rating  = models.FloatField()
    link = models.CharField(max_length=50)
    corpus = models.FileField()
    meta_description = models.CharField(max_length=50)
    preparation_time = models.IntegerField()
    image = models.ImageField()

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


    def __unicode__(self):
        return self.title