# encoding: utf-8
from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now


class Category(models.Model):
	"""Category model."""
	name = models.CharField(u'Name', max_length=100)
	slug = models.SlugField(unique=True)
	description = models.TextField(u'Beschreibung', blank=True)

	class Meta:
		verbose_name = u'Kategorie'
		verbose_name_plural = u'Kategorien'

	def __unicode__(self):
		return self.name


class Recipe(models.Model):
	"""Recipe model."""
	DIFFICULTY_EASY = 1
	DIFFICULTY_MEDIUM = 2
	DIFFICULTY_HARD = 3
	DIFFICULTIES = (
		(DIFFICULTY_EASY, u'einfach'),
		(DIFFICULTY_MEDIUM, u'normal'),
		(DIFFICULTY_HARD, u'schwer'),
	)

	title = models.CharField(u'Titel', max_length=255)
	slug = models.SlugField(unique=True)
	ingredients = models.TextField(u'Zutaten',
			help_text = u'Eine Zutat pro Zeile angeben')
	preparation = models.TextField(u'Zubereitung')
	time_for_preparation = models.IntegerField(u'Zubereitungszeit',
			help_text = u'Zeit in Minuten angeben', blank=True, null=True)
	number_of_portions = models.PositiveIntegerField(u'Anzahl der Portionen')
	difficulty = models.SmallIntegerField(u'Schwierigkeitsgrad')
	category = models.ManyToManyField(Category, verbose_name=u'Kategorien')
	author = models.ForeignKey(User, verbose_name=u'Author')
	date_created = models.DateTimeField(editable=False)
	date_updated = models.DateTimeField(editable=False)
	is_active = models.BooleanField(u'Aktiv')

	class Meta:
		verbose_name = u'Rezept'
		verbose_name_plural = u'Rezepte'
		ordering = ['-date_created']

	def __unicode__(self):
		return self.title

	def save(self, *args, **kwargs):
		if not self.id:
			self.date_created = now()
		self.date_updated = now()
		super(Recipe, self).save(*args, **kwargs)

	@models.permalink
	def get_absolute_url(self):
	    return ('recipes_recipe_detail', (), {'slug': self.slug})

def get_related_recipes(self):
	categories = self.category.all()
	related_recipes = Recipe.objects.all().filter(
		difficulty__exact=self.difficulty, category__in=categories)
	return related_recipes.exclude(pk=self.id).distinct()

class Comment(models.Model):
	"""Comments model."""
	recipe = models.ForeignKey(Recipe, related_name='comments')
	author = models.ForeignKey(User, verbose_name=u'Author')
	comment = models.CharField(u'Kommentar', max_length=1000)
	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = u'Kommentar'
		verbose_name_plural = u'Kommentare'
		ordering = ['-date_created']

	def __unicode__(self):
		return self.comment