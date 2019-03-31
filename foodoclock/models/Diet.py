from django.db import models


class Diet(models.Model):
    diet = models.CharField(max_length=100)

    def __str__(self):
        return self.diet

    @classmethod
    def getDiets(cls, diets):
        results = []
        for name in diets:
            results.append(Diet.objects.filter(diet=name))
        if len(results):
            final_results = results[0].union(*results[1:])
            return final_results.values_list('pk', flat=True)
        else:
            return []