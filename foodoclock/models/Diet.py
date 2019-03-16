from django.db import models


class Diet(models.Model):
    diet = models.CharField(max_length=100)

    def __str__(self):
        return self.diet
