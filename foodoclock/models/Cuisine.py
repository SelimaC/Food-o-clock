from django.db import models


class Cuisine(models.Model):
    cuisine = models.CharField(max_length=100)

    def __str__(self):
        return self.cuisine

    @classmethod
    def getCuisineByNames(cls, cuisine):
        results = []
        for name in cuisine:
            results.append(Cuisine.objects.filter(cuisine=name))
        if len(results):
            final_results = results[0].union(*results[1:])
            return final_results.values_list('pk', flat=True)
        else:
            return []
