from django.conf.urls import patterns, include, url

urlpatterns = patterns('partyapp.events.views',

	url(r'^$', 'list',
		name = 'party_list'),

	url(r'^add/$', 'add',
		name = 'add_party'),
	url(r'^userpartys/$', 'userpartys',
		name = 'user_partys'),
	url(r'^visitpartys/$', 'userpartyvisit',
		name = 'user_visit_partys'),
	url(r'^addclub/$', 'add_club',
		name = 'add_club'),
	url(r'^(?P<slug>[-\w]+)/$', 'detail',
		name = 'party_detail'),
	url(r'^(?P<slug>[-\w]+)/edit/$', 'edit',
		name = 'party_edit'),

	url(r'^(?P<slug>[-\w]+)/signparty/$', 'signparty',
		name = 'sign_party'),
)