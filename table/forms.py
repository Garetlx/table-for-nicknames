from django import forms
from .models import Player
from django.core.exceptions import ValidationError

class PlayerEditForm(forms.ModelForm):

    class Meta:
        model = Player
        fields = ('nickname','gangs','forts','fights','zvz','accepted_date')

class LoadFilesForm(forms.Form):

    class Meta:
        model = Player
        fields = ('nickname','gangs','forts','fights','zvz','accepted_date')