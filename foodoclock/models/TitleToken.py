from django.db import models


class TitleToken(models.Model):
    token = models.CharField(max_length=100)

    def __str__(self):
        return self.token

    @classmethod
    def getTokensByIds(cls, ids):
        return TitleToken.objects.filter(pk__in=ids)

    @classmethod
    def getTokenById(cls, id):
        return TitleToken.objects.get(pk=id)

    @classmethod
    def getAllTokens(cls):
        return TitleToken.objects.all()
