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
        return Ingredient.objects.all()

    @classmethod
    def getIngredientsByNames(cls, names):
        results = []

        for name in names:
            results.append(Ingredient.objects.filter(name__icontains=name))

        if len(results) == 1:
            final_results = results[0]
            return final_results.values_list('pk', flat=True)
        elif len(results) > 0:
            final_results = results[0].union(*results[1:])
            return final_results.values_list('pk', flat=True)
        else:
            return []


    @ classmethod
    def getIngredientsByName(cls, name):
        result = (Ingredient.objects.filter(name__icontains=name))
        return result.values_list('pk', flat=True)
