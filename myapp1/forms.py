import datetime
from django import forms
from .models import Student, User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin import widgets

BIRTH_YEAR_CHOICES = ','.join('{}'.format(i) for i in range(datetime.datetime.now().year-120, datetime.datetime.now().year+1)).split(',')
COLORS = (
    ('blue', 'Bleu'),
    ('green', 'Green'),
    ('black', 'Black'),
)

class NameForm(forms.ModelForm):
    #Permet de créer un formulaire à partir des champs d'une table (un modèle)

    #Pour vérifier que la date entrée est entre il y a 4 semaine et aujourd'hui
    def clean_date(self):
        data = self.cleaned_data['date']
        
        #Check date is not in past. 
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        #Check date is in range librarian allowed to change (+4 weeks).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        # Remember to always return the cleaned data.
        return data

    class Meta:
        model = Student
        #fields = ['name', 'email'] #créra les champs de formulaire pour les champs 'name' et 'date' du modèle
        fields = '__all__' #cré des champs de formulaire pour TOUS les champs du modèle
        #exclude = ['pass', 'color'] #créra les champs de formulaire pour tous les champs sauf les champs 'pass' et 'color' du modèle
        labels = { 'date': _('Prochaine visite?'), 'name': _('Nom') }
        help_texts = { 'date': _('Enter une date entre maintenant et dans 4 semaines max'), } 

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'email', 'color', 'date', 'creator' ]
    #creator = forms.ModelChoiceField(queryset=User.objects.filter(username='eleve1'), disabled=True)
    creator = forms.ModelChoiceField(queryset=User.objects.all(), disabled=True, to_field_name="username")
