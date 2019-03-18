from django.db import models


class Favourite(models.Model):
    user = models.ForeignKey('foodoclock.UserDetails',on_delete=models.PROTECT)
    recipe = models.ForeignKey('foodoclock.Recipe',on_delete=models.PROTECT)

    def __str__(self):
        return "Favourite"
