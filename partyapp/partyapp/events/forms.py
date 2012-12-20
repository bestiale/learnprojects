from django import forms
from django.forms import ModelForm, widgets
from django.template.defaultfilters import slugify

from .models import Party, Club, Guest

class PartyForm(ModelForm):
	party_date = forms.DateField(
			label='Datum der Party',
			widget=forms.DateInput()
	)
	class Meta:
		model = Party
		exclude = ('author', 'slug', 'date_created', 'date_updated', 'guests')


class VisitorForm(ModelForm):
	class Meta:
		model = Guest
		exclude = ('party', 'user', 'date_accepted')


class ClubForm(ModelForm):
	class Meta:
		model = Club