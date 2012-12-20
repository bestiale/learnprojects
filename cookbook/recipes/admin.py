from django.contrib import admin
from .models import Category, Recipe, Comment

from .forms import RecipeForm

class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name', 'description')
	prepopulated_fields = {'slug' : ['name']}

class RecipeAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug' : ['title']}

class CommentAdmin(admin.ModelAdmin):
	pass

	
admin.site.register(Category, CategoryAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Comment)