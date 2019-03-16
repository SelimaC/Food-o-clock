from django.db import models


class Cousine(models.Model):
    cousine = models.CharField(max_length=100)

    def __str__(self):
        return self.cousine
