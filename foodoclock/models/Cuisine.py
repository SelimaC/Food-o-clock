from django.db import models


class Cuisine(models.Model):
    cuisine = models.CharField(max_length=100)

    def __str__(self):
        return self.cuisine
