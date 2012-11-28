from django.conf.urls import patterns, include, url

urlpatterns = patterns('recipes.views',
    url(r'^erstellen/$', 'add', 
    	name='recipes_recipe_add'),
    url(r'^bearbeiten/(?P<recipe_id>\d+)/$', 'edit', 
    	name='recipes_recipe_edit'),

    url(r'^(?P<slug>[-\w]+)/comment/$', 'add_comment', 
    	name='recipes_recipe_add_comment'),
    url(r'^comment_edit/(?P<comment_id>\d+)/$', 'edit_comment',
       name='recipes_recipe_edit_comment'),
     url(r'^comment_delete/(?P<comment_id>\d+)/$', 'delete_comment',
       name='recipes_recipe_delete_comment'),

    url(r'^(?P<slug>[-\w]+)/$', 'detail',
       name='recipes_recipe_detail'),
    url(r'^$', 'index',
        name='recipes_index'),
)