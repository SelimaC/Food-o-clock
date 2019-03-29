import hashlib
import random
import string

from django.contrib.auth.models import User
from foodoclock.models.Diet import Diet
from foodoclock.models.Cuisine import Cuisine
from django.db import models

from foodoclock.models.Favourite import Favourite


class UserDetails(models.Model):
    code = models.CharField(max_length=50)
    cuisine = models.ForeignKey(Cuisine, on_delete=models.CASCADE)
    diet = models.ForeignKey(Diet, on_delete=models.CASCADE)
    country = models.CharField(max_length=50)
    age = models.IntegerField()
    user = models.OneToOneField(User, unique=True, on_delete=models.PROTECT)
    visits = models.IntegerField(default=0)
    clicks = models.IntegerField(default=0)

    @classmethod
    def make_random_code(cls, username, length=8):
        hash = (int(hashlib.sha1(username.encode("utf-8")).hexdigest(), 16) % (10 ** 8)).__str__()
        return "".join([random.choice(string.ascii_letters) for c in range(length)]).upper() + hash

    @classmethod
    def newUserDetails(cls, user, cuisine, diet, country, age):
        flag = True
        while flag:
            code = UserDetails.make_random_code(user.username)
            try:
                UserDetails.objects.get(code=code)
                flag=True
            except UserDetails.DoesNotExist:
                flag=False

        details = UserDetails(code=code, cuisine=cuisine, diet=diet, country=country, age=age, user=user)
        details.save()

    @classmethod
    def getDetailByUser(cls, user):
        return UserDetails.objects.get(user=user)

    @classmethod
    def getFavouritesByUser(cls, user):
        return Favourite.objects.filter(user=user)

    def __str__(self):
        return self.code
