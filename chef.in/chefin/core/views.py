from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import SignUpForm
import math
import requests

def index(request):
    return render(request, 'core/index.html')

def contact(request):
    return render(request, 'core/contact.html')

def detail(request, recipe_id):
    app_id = 'cd43c4fc'
    app_key = 'c92cb870ea5eeea683bbe8caec487222'

    url = f'https://api.edamam.com/api/recipes/v2/{recipe_id}'
    params = {
        'type': 'public',
        'app_id': app_id,
        'app_key': app_key,
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        recipe_data = response.json()

        recipe_name = recipe_data['recipe']['label']
        recipe_image = recipe_data['recipe']['image']
        recipe_ingredients = recipe_data['recipe']['ingredientLines']
        recipe_url = recipe_data['recipe']['url']
        recipe_source = recipe_data['recipe']['source']
        recipe_calories = math.ceil(recipe_data['recipe']['calories'])
        recipe_mealType = recipe_data['recipe']['mealType']
        recipe_cuisineType = recipe_data['recipe']['cuisineType']

        cleaned_mealType = str(recipe_mealType).strip("[]").replace("'", "")
        cleaned_cuisineType = str(recipe_cuisineType).strip("[]").replace("'", "")

        print(recipe_data)

        recipe_info = {
            'label': recipe_name,
            'image': recipe_image,
            'ingredients': recipe_ingredients,
            'url': recipe_url,
            'source': recipe_source,
            'calories': recipe_calories,
            'mealType': cleaned_mealType,
            'cuisineType': cleaned_cuisineType
        }
        

        return render(request, 'core/recipe.html', {'recipe': recipe_info})
    else:
        return HttpResponse('Error fetching recipe details. Please try again later.')

def fetch_recipes(query, from_index=0, to_index=48):
    app_id = 'cd43c4fc' 
    app_key = 'c92cb870ea5eeea683bbe8caec487222'
    url = 'https://api.edamam.com/search'
    params = {
        'q': query,
        'app_id': app_id,
        'app_key': app_key,
        'from': from_index,
        'to': to_index
    }
    response = requests.get(url, params=params)
    data = response.json()
    recipes = data.get('hits', [])
    for hit in recipes: 
        hit['recipe']['recipe_id'] = hit['recipe']['uri'].split('#')[1]
    return recipes

def home(request):
    query = request.GET.get('query', 'chicken')
    page = request.GET.get('page', 1)
    
    try:
        page = int(page)
    except ValueError:
        page = 1
    
    from_index = (page - 1) * 48
    to_index = page * 48
    
    recipes = fetch_recipes(query, from_index, to_index)
    
    paginator = Paginator(recipes, 48)
    
    try:
        recipes_page = paginator.page(page)
    except PageNotAnInteger:
        recipes_page = paginator.page(1)
    except EmptyPage:
        recipes_page = paginator.page(paginator.num_pages)
    
    print(recipes)

    context = {
        'recipes': recipes_page,
        'query': query,
        'current_page': page,
        'total_pages': len(recipes)
    }
    
    return render(request, 'core/index.html', context)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('/login')
    else:
        form = SignUpForm()

    return render(request, 'core/signup.html', {'form': form})