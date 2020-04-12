from django.db import models
# Create your models here.
from jsonfield import JSONField

class Specifications(models.Model):
    """
    This class is used to store all datas relative to a
    specific Spacex element
    """
    category= models.CharField(max_length=200)
    name = models.CharField(max_length=400)
    all_datas = JSONField()

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

