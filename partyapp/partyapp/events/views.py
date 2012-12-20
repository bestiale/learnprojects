from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify

from .models import Club, Party, Guest
from .forms import PartyForm, VisitorForm, ClubForm


def list(request):
	partys = Party.objects.all()

	return render(request, 'events/list.html', { 
		'object_list': partys,
	})


def detail(request, slug):
	party = get_object_or_404(Party, slug=slug)

	return render(request, 'events/detail.html', {
		'party': party,
		'guests': party.guests.all(),
	})

def add(request):
    if request.method == 'POST':
        form = PartyForm(request.POST, request.FILES)
        if form.is_valid():
        	party = form.save(commit=False)
        	party.author = request.user
        	party.slug = slugify(party.title)
        	party.save()
        	return redirect(party.get_absolute_url())
    else:
        form = PartyForm()
    return render(request, 'events/addpartyform.html',
        {'form': form })


def edit(request, slug):
	party = get_object_or_404(Party, slug=slug)

	if request.method == 'POST':
		form = PartyForm(instance=party, data=request.POST)
		if form.is_valid():
			party = form.save()
			return redirect(party.get_absolute_url())
	else:
		form = PartyForm(instance=party)
	return render(request, 'events/editpartyform.html',
		{'form': form, })


@login_required
def signparty(request, slug):
	party = get_object_or_404(Party, slug=slug)

	form = VisitorForm(data=request.POST)

	if form.is_valid():
		sign = form.save(commit=False)
		sign.party = party
		sign.user = request.user
		sign.save()
		return redirect(party)

	else:
		form = VisitorForm()

	return redirect(party.slug)


@login_required
def unsignparty(request, slug):
	party = get_object_or_404(Party, slug=slug)

	guest.delete()
	return redirect('party_list')


@login_required
def userpartys(request):
	partys = Party.objects.filter(author=request.user)

	return render(request, 'events/userpartys.html',{
			'object_list': partys,
	})


@login_required
def userpartyvisit(request):
	partys = Guest.objects.filter(user=request.user)

	return render(request, 'events/govisit.html',{
			'object_list': partys,
	})


def add_club(request):
	form = ClubForm(request.POST)
	if form.is_valid():
		form.save()
		return redirect('add_party')
	else:
		form = ClubForm()
	return render(request, 'events/addclubform.html',{
			'form': form,
	})