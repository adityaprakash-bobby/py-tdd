from django.db import models
from django.core.urlresolvers import reverse
# Create your models here.
class List(models.Model):
    
    def get_absolute_url(self):
        return reverse('views_list', args=[self.id])
    
class Item(models.Model):

    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None)
