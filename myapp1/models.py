import datetime

from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    """ renvoi 1 si la pub_date est vieille de moins d'un jours """

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    class Meta:
        verbose_name = 'Question a poser'
        verbose_name_plural = 'Questions a poser'

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField('Choix', max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

    class Meta:
        verbose_name = 'Choix de question'
        verbose_name_plural = 'Choix de Questions'


class Student(models.Model):
    name =  models.CharField(max_length=200)
    email = models.CharField('Email', max_length=200)
    passw = models.CharField('Password', max_length=200)
    color = models.CharField('Colors', max_length=200)
    date = models.DateField('Date', max_length=200) 
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of the model.
        """
        return reverse('myapp1:student_detail', args=[str(self.id)])

    class Meta:
        verbose_name = 'Gestion Elève'
        verbose_name_plural = 'Gestion Elèves'
        permissions = (("can_update", "can update"), ("can_delete", "can delete user"),) 
