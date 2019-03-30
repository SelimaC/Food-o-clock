from django.db import models


class Query(models.Model):
    query = models.CharField(max_length=100)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.query

    @classmethod
    def getQueryById(cls, id):
        return Query.objects.get(pk=id)

    @classmethod
    def getAllQueries(cls):
        return Query.objects.all()

    @classmethod
    def getQueryByString(cls, query):
        return Query.objects.filter(query__icontains=name)
