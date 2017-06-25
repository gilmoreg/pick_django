from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
''' Django Models '''

class Poll(models.Model):
    '''
      Saves a user's list as a poll
    '''
    user = models.CharField(max_length=200)
    list_origin = models.CharField(max_length=15)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.list_origin + '/' + self.user

@python_2_unicode_compatible
class Anime(models.Model):
    '''
    An individual Anime in a user's list
    '''
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    a_id = models.CharField(max_length=20)
    image = models.CharField(max_length=250)
    votes = models.CharField(max_length=20)

    def __str__(self):
        return self.a_id
