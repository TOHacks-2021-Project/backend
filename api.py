from main import app
from processes import location, recipe
from flask import json, jsonify
from flask import request
import urllib.parse
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join('.env')
load_dotenv(dotenv_path)

HERE_MAPS_API_KEY = os.environ.get("HERE_MAPS_API_KEY")
RECIPE_API_KEY = os.environ.get("RECIPE_API_KEY")
RECIPE_APP_ID = os.environ.get("RECIPE_APP_ID")

@app.route("/api/get_locations", methods=['GET'])
def get_locations():
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    radius = request.args.get("radius")
    if lat is None or lon is None:
        return "Lat and Lon not Provided", 400
    if radius is None:
        radius = 5000
    else:
        radius = int(radius)

    lat, lon = map(float, (lat, lon))
    res = location.getStores(HERE_MAPS_API_KEY, lat, lon, radius=radius)

    return jsonify(res)

@app.route("/api/get_recipes", methods=['GET'])
def get_recipes():
    query = request.args.get("q")
    if query is None:
        return "Query Not Provided!", 400
    else:
        query = urllib.parse.unquote(query)

    params = {}
    for k, v in request.args.items():
        if k in ["meal_type", "cuisine_type", "calorie_range", "health_labels", "excluded_ingredients"]:
            params[k] = v

    res = recipe.get_recipes(
        RECIPE_API_KEY, 
        RECIPE_APP_ID, 
        query, 
        **params
    )
    return jsonify(res)

@app.route("/api/get_recipes_simplify", methods=['GET'])
def get_recipes_simplify():
    query = request.args.get("q")
    if query is None:
        return "Query Not Provided!", 400
    else:
        query = urllib.parse.unquote(query)

    params = {}
    for k, v in request.args.items():
        if k in ["meal_type", "cuisine_type", "calorie_range", "health_labels", "excluded_ingredients"]:
            params[k] = v

    res = recipe.get_recipes_simplify(
        RECIPE_API_KEY, 
        RECIPE_APP_ID, 
        query, 
        **params
    )
    return jsonify(res)

@app.route("/api/get_recipe_by_id", methods=['GET'])
def get_recipe_by_id():
    query = request.args.get("q")
    if query is None:
        return "Query Not Provided!", 400

    res = recipe.get_recipe_by_id(
        RECIPE_API_KEY, 
        RECIPE_APP_ID, 
        urllib.parse.quote(query)
    )
    return jsonify(res)

