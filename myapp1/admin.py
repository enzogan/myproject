from django.contrib import admin
from . import models

class ChoiceInline(admin.TabularInline):
    model = models.Choice
    extra = 1

""" Permet de spécifie les champs à afficher lorsqu'on clique sur l'objet question """
""" Par défaut affiche ce que contient la classe __str__ uniquement """
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    search_fields = ('question_text', 'pub_date')
    list_filter = ('pub_date',)
    inlines = (ChoiceInline,)

class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('choice_text', 'votes', 'question')
    search_fields = ('choice_text',)
    list_filter = ('question',)

admin.site.register(models.Question, QuestionAdmin)
admin.site.register(models.Choice, ChoiceAdmin)


# Register your models here.
