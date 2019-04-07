from django.db import models

# Create your models here.
class Item(models.Model):

    text = models.TextField(max_length=30,default='')