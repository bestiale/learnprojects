# encoding: utf-8
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

class Party(models.Model):
	author = models.ForeignKey(User, verbose_name='author')
	club = models.ForeignKey('Club', verbose_name='club')
	slug = models.SlugField(unique=True)
	title = models.CharField(u'Titel', max_length=255)
	description = models.TextField(u'Beschreibung', max_length=1000)
	party_date = models.DateTimeField()
	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)
	public = models.BooleanField()
	picture = models.ImageField(upload_to='images/')
	guests = models.ManyToManyField('auth.User', through='Guest',
		related_name='parties')

	class Meta:
		verbose_name = u'Party'
		verbose_name_plural = u'Partys'

	def __unicode__(self):
		return self.title

	@property
	def is_past(self):
		return self.party_date <= now()

	@models.permalink
	def get_absolute_url(self):
	    return ('party_detail', (), {'slug': self.slug})


class Club(models.Model):
	name = models.CharField(u'Clubname', max_length=255)
	street_nr = models.CharField(u'Strasse', max_length=255)
	plz = models.IntegerField(u'PLZ')
	city = models.CharField(u'Stadt', max_length=255)

	class Meta:
		verbose_name = u'Club'
		verbose_name_plural = u'Clubs'

	def __unicode__(self):
		return self.name


class Guest(models.Model):
	party = models.ForeignKey('Party')
	user = models.ForeignKey(User)
	date_accepted = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = u'Gast'
		verbose_name_plural = u'Gäste'

	def __unicode__(self):
		return self.party.title


class UserProfile(models.Model):
	user = models.OneToOneField(User)
	name = models.CharField(u'Name', max_length=255)
	gender = models.CharField(u'Geschlecht', max_length=50)
	birthdate = models.DateField(u'Geburtsdatum')