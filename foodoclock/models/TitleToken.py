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

    @classmethod
    def getTokensByNames(cls, names):
        results = []
        for name in names:
            results.append(TitleToken.objects.filter(token__icontains=name))
        if len(results):
            final_results = results[0].union(*results[1:])
            return final_results.values_list('pk', flat=True)
        else:
            return []
