from django.shortcuts import get_object_or_404, render, redirect
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.conf.urls import patterns, include, url
import logging

from recipes.models import Recipe, Comment
from recipes.forms import RecipeForm, CommentForm

logger = logging.getLogger('cookbook.recipes.views')


def index(request):
	recipes = Recipe.objects.all()

	return render(request, 'recipes/index.html', {
		'object_list': recipes,
	})

def detail(request, slug):
	recipe = Recipe.objects.get(slug=slug)

	return render(request, 'recipes/detail.html',{
			'object': recipe,
	})

@login_required
def add(request):
    if request.method == 'POST':
        form = RecipeForm(user=request.user, data=request.POST)
        if form.is_valid():
            recipe = form.save()
            return HttpResponseRedirect(recipe.get_absolute_url())
    else:
        form = RecipeForm()
    return render(request, 'recipes/form.html',
        {'form': form, 'add': True})

@login_required
def edit(request, recipe_id):
	recipe = get_object_or_404(Recipe, pk=recipe_id)
	if recipe.author != request.user and not request.user.is_staff:
		return HttpResponseForbidden()
	if request.method == 'POST':
		form = RecipeForm(instance=recipe, data=request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(recipe.get_absolute_url())
	else:
		form = RecipeForm(instance=recipe)
		
	return render(request, 'recipes/form.html',
		{'form': form, 'add': False, 'object': recipe})


@login_required
def add_comment(request, slug):
	recipe = get_object_or_404(Recipe, slug=slug)

	if request.method == 'POST':
		form = CommentForm(data=request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.recipe = recipe
			comment.author = request.user
			comment.save()
			return redirect(recipe)
	else:
		form = CommentForm()

	return render(request, 'recipes/add_comment.html', {
			'form': form,
			'object': recipe
		})


@login_required
def edit_comment(request, comment_id):
	comment = get_object_or_404(Comment, pk=comment_id)

	if comment.author != request.user:
		return HttpResponseForbidden()

	if request.method == 'POST':
		form = CommentForm(request.POST, instance=comment)
		if form.is_valid():
			comment = form.save()
			return redirect(comment.recipe)
	else:
		form = CommentForm(instance=comment)

	return render(request, 'recipes/editcomment_form.html', {
		'form': form, 
		'object': comment
	})


@login_required
def delete_comment(request, comment_id):
	comment = get_object_or_404(Comment, pk=comment_id)

	if comment.author != request.user:
		return HttpResponseForbidden()
	else:	
		comment.delete()
		return redirect(comment.recipe)