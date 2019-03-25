from django.db import models


class Ingredient(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    @classmethod
    def getIngredientsByIds(cls, ids):
        return Ingredient.objects.filter(pk__in=ids)

    @classmethod
    def getIngredienteById(cls, id):
        return Ingredient.objects.get(auto_increment_id=id)

    @classmethod
    def getAllIngredients(cls):
        return Ingredient.objects.getAll()

    @classmethod
    def getIngredientsByNames(cls, names):
        return Ingredient.objects.filter(name__in=names)