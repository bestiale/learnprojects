from django import forms
from django.forms import ModelForm, widgets
from django.template.defaultfilters import slugify

from .models import Recipe, Comment

class RecipeForm(ModelForm):
	class Meta:
		model = Recipe
		exclude = ('slug', 'author', 'date_created', 'date_updated')

	def __init__(self, **kwargs):
		self.__user = kwargs.pop('user', None)
		super(RecipeForm, self).__init__(**kwargs)

	def save(self, commit=True):
		if self.instance.pk is None:
			if self.__user is None:
				raise TypeError("You didn't give an user argument to the constructor.")
			self.instance.slug = slugify(self.instance.title)
			self.instance.author = self.__user
		return super(RecipeForm, self).save(commit)

class CommentForm(ModelForm):
	comment = forms.CharField(
			label='Bla',
			widget=forms.Textarea(attrs={'cols': 50})
	)

	class Meta:
		model = Comment
		exclude = ('recipe', 'author')