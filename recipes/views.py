from django.shortcuts import render, redirect
from .models import *
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from .forms import RecipeForm

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


def create_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = RecipeForm()
    return render(request, 'create.html', {'form': form})



def get_recipe(filter_recipe=None):
    if filter_recipe:
        print("DATA COMING FROM DB")

        recipes = Recipe.objects.filter(name__contains=filter_recipe)
    else:
        recipes = Recipe.objects.all()
    return recipes


def home(request):
    filter_recipe = request.GET.get('recipe')
    if cache.get(filter_recipe):
        print("DATA COMING FROM CACHE")
        redis_client = cache.client
        print(redis_client)
        recipe = cache.get(filter_recipe)
    else:
        if filter_recipe:
            recipe = get_recipe(filter_recipe)
            cache.set(filter_recipe, recipe)
        else:
            recipe = get_recipe()

    context = {'recipe': recipe}
    return render(request, 'home.html', context)


def show(request, id):
    if cache.get(id):
        print("DATA COMING FROM CACHE")
        redis_client = cache.client
        print(redis_client)
        recipe = cache.get(id)
    else:
        print("DATA COMING FROM DB")

        recipe = Recipe.objects.get(id=id)
        cache.set(id, recipe)
    context = {'recipe': recipe}
    return render(request, 'show.html', context)
