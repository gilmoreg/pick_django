from django.db import models

class Poll(models.Model):
    '''
      Saves a user's list as a poll
    '''
    user = models.CharField(max_length=200)
    list_origin = models.CharField(max_length=15)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.list_origin + '/' + self.user

class Anime(models.Model):
    '''
    An individual Anime in a user's list
    '''
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    a_id = models.PositiveIntegerField()
    image = models.CharField(max_length=250)
    votes = models.PositiveIntegerField()

    def __str__(self):
        return self.a_id
