import requests
import json

def get_recipes(
    api_key, app_id, query, image_type='THUMBNAIL', 
    meal_type=None, cuisine_type=None, calorie_range=None, health_labels=None, excluded_ingredients=None
):
    url = f"https://api.edamam.com/search?q={query}&app_id={app_id}&app_key={api_key}" 

    opt_args = [
        meal_type,
        cuisine_type,
        calorie_range,
        health_labels,
        excluded_ingredients
    ]

    opt_query_params = [
        'mealType',
        'cuisineType',
        'calories',
        'health',
        'excluded'
    ]

    for (arg, param) in zip(opt_args, opt_query_params):
        if arg:
            url += '&' + param + '=' + arg

    response = requests.get(url)
    content = json.loads(response.content)
    
    recipes = []
    for recipe in content['hits']:
        try:
            x = recipe['recipe']
            
            y = {
                "name": x['label'],
                "thumbnail": x['image'],
                "diets_label": x['dietLabels'],
                "health_labels": x['healthLabels'],
                "cautions": x['cautions'],
                "servings": round(x['yield']),
                "calories": round(x['calories'])
            }

            if meal_type:
                y['meal_type'] = x['mealType']
            
            if cuisine_type:
                y['dish_type'] = x['dishType']

            ingredients = []
            for ingr in x['ingredients']:
                ingredients.append({
                    "name": ingr['text'], 
                    "grams": ingr['weight'],  # WEIGHT IS IN GRAMS
                    "image": ingr['image']
                })
            
            y['ingredients'] = ingredients

            recipes.append(y)
        except Exception as e:
            print(f"ERROR WHILE PROCESSING RECIPES! ERROR: {e}")

    return recipes

def get_recipes_simplify(
    api_key, app_id, query, image_type='THUMBNAIL', 
    meal_type=None, cuisine_type=None, calorie_range=None, health_labels=None, excluded_ingredients=None
):
    url = f"https://api.edamam.com/search?q={query}&app_id={app_id}&app_key={api_key}" 

    opt_args = [
        meal_type,
        cuisine_type,
        calorie_range,
        health_labels,
        excluded_ingredients
    ]

    opt_query_params = [
        'mealType',
        'cuisineType',
        'calories',
        'health',
        'excluded'
    ]

    for (arg, param) in zip(opt_args, opt_query_params):
        if arg:
            url += '&' + param + '=' + arg

    response = requests.get(url)
    content = json.loads(response.content)
    
    recipes = []
    for recipe in content['hits']:
        try:
            x = recipe['recipe']
            
            y = {
                "name": x['label'],
                "thumbnail": x['image'],
                "id": x['uri'],
                "servings": round(x['yield']),
                "calories": round(x['calories'])
            }

            recipes.append(y)
        except Exception as e:
            print(f"ERROR WHILE PROCESSING RECIPES! ERROR: {e}")

    return recipes


def get_recipe_by_id(
    api_key, app_id, query
):
    url = f"https://api.edamam.com/search?r={query}&app_id={app_id}&app_key={api_key}"
    response = requests.get(url)
    print(response.content)

    content = json.loads(response.content)
    
    try:
        x = content[0]

        y = {
            "name": x['label'],
            "thumbnail": x['image'],
            "diets_label": x['dietLabels'],
            "health_labels": x['healthLabels'],
            "cautions": x['cautions'],
            "servings": round(x['yield']),
            "calories": round(x['calories'])
        }

        ingredients = []
        for ingr in x['ingredients']:
            ingredients.append({
                "name": ingr['text'], 
                "grams": ingr['weight'],  # WEIGHT IS IN GRAMS
                "image": ingr['image']
            })
            
        y['ingredients'] = ingredients

        return y
    except Exception as e:
        print(f"ERROR WHILE PROCESSING RECIPES! ERROR: {e}")
        return "error"
