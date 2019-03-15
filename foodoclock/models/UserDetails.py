import hashlib
import random
import string

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q

from foodoclock.models.Favourite import Favourite


class UserDetails(models.Model):
    code = models.CharField(max_length=50)
    cousine = models.CharField(max_length=50)
    diet = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    age = models.IntegerField()
    user = models.OneToOneField(User, unique=True, on_delete=models.PROTECT)

    @classmethod
    def make_random_code(cls, username, length=8):
        hash = (int(hashlib.sha1(username.encode("utf-8")).hexdigest(), 16) % (10 ** 8)).__str__()
        return "".join([random.choice(string.ascii_letters) for c in range(length)]).upper() + hash

    @classmethod
    def newUserDetails(cls, user, cousine, diet, country, age):
        flag = True
        while flag:
            code = UserDetails.make_random_code(user.username)
            try:
                UserDetails.objects.get(code=code)
                flag=True
            except UserDetails.DoesNotExist:
                flag=False

        details = UserDetails(code=code, cousine=cousine, diet=diet, country=country, age=age, user=user)
        details.save()

    @classmethod
    def getDetailByUser(cls, user):
        return UserDetails.objects.get(user=user)

    @classmethod
    def getFavouritesByUser(cls, user):
        return Favourite.objects.filter(user=user)

    def __unicode__(self):
        return self.code
