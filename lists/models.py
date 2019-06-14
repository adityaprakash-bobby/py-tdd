from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
# Create your models here.
class List(models.Model):
    
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)

    @property
    def name(self):
        return self.item_set.first().text

    def get_absolute_url(self):
        return reverse('views_list', args=[self.id])
    
class Item(models.Model):

    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ('id',)
        unique_together = ('list', 'text')