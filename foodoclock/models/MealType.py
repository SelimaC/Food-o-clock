from django.db import models


class MealType(models.Model):
    type = models.CharField(max_length=100)

    def __str__(self):
        return self.type

    @classmethod
    def getMealTypes(cls, meals):
        results = []
        for name in meals:
            results.append(MealType.objects.filter(type=name))
        if len(results):
            final_results = results[0].intersection(*results[1:])
            return final_results.values_list('pk', flat=True)
        else:
            return []