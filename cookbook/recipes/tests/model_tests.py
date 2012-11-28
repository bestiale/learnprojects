# -*- coding: utf-8 -*-

import datetime

from django.contrib.auth.models import User
from django.db import IntegrityError
from django.template.defaultfilters import slugify
from django.test import skipIfDBFeature, TestCase

from recipes.models import Recipe


class RecipeSaveTest(TestCase):
    title = u'Erbsensuppe mit Würstchen'
    number_of_portions = 4

    def setUp(self):
        self.author = User.objects.create_user('testuser', 'test@example.com',
            'testuser')

    def testDateCreatedAutoset(self):
        """Verify date_created is autoset correctly"""
        recipe = Recipe.objects.create(title=self.title, slug=slugify(self.title),
            number_of_portions=self.number_of_portions, author=self.author)
        now = datetime.datetime.now()
        self.assertEqual(recipe.date_created.date(), now.date())
        self.assertEqual(recipe.date_created.hour, now.hour)
        self.assertEqual(recipe.date_created.minute, now.minute)

    def testSlugIsUnique(self):
        """Verify if a slug is unique"""
        Recipe.objects.all().delete()
        Recipe.objects.create(title=self.title, slug=slugify(self.title),
            number_of_portions=self.number_of_portions, author=self.author)
        self.assertRaises(IntegrityError, Recipe.objects.create,
            title=self.title, slug=slugify(self.title),
            number_of_portions=self.number_of_portions, author=self.author)

    @skipIfDBFeature('supports_transactions')
    def testTransaction(self):
        """Demonstrate the skipIfDBFeature decorator."""
        assert False