from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

import json

from saved_routes.models import SavedRoute

def SaveRoute(request):
    data = json.loads(request.body.decode('utf-8'))

    user = request.user

    route = SavedRoute.objects.create(
    user=user,
    destination_origin=data.get('origin'),
    destination_waypoint=data.get('waypoint'),
    distance=data.get('distance'),
    name=data.get('name'),
    description=data.get('description'),
    )

    if route is not None:
        return JsonResponse({'message': 'Route successfully saved'}, status=201)
    else: 
        return JsonResponse({'error': 'Save unsuccessful'}, status=400)

def SavedRoutes(request):
    try:
        user = request.user
        userRoutes = SavedRoute.objects.filter(user=user)
        routesList = list(userRoutes.values())

        # Transforming the routes into the desired structure
        formattedRoutes = []
        for route in userRoutes:
            try:
                origin = json.loads(route.destination_origin.replace("'", '"'))
                waypoint = json.loads(route.destination_waypoint.replace("'", '"'))
            except json.JSONDecodeError as e:
                # Handle the error if the JSON is invalid
                continue

            formattedRoutes.append({
                'id': route.id,
                'name': route.name,
                'description': route.description,
                'distance': route.distance,
                'isFavorite': route.is_favorite,
                'origin': [origin['lat'], origin['lng']],
                'waypoint': [waypoint['lat'], waypoint['lng']]
            })

        return JsonResponse({
            'allRoutes': formattedRoutes,
            }, content_type='application/json')
    except json.JSONDecodeError as e:
        return HttpResponse({'There has been an Error'}, content_type='application/json')


def EditRoute(request):
    try:
        user = request.user

        data = json.loads(request.body.decode('utf-8'))

        route = SavedRoute.objects.get(user=user, pk=data.get('routeId'))

        route.name = data.get('name')
        route.description = data.get('description')
        route.save()

        return HttpResponse({'Route Edited'}, content_type='application/json')
    except json.JSONDecodeError as e:
        return HttpResponse({'There has been an Error'}, content_type='application/json')


def FavoriteRoute(request):
    try:
        user = request.user

        data = json.loads(request.body.decode('utf-8'))

        route = SavedRoute.objects.get(user=user, pk=data.get('routeId'))

        route.is_favorite = not route.is_favorite
        route.save()

        return HttpResponse({'Route Saved'}, content_type='application/json')
    except json.JSONDecodeError as e:
        return HttpResponse({'There has been an Error'}, content_type='application/json')


def DeleteRoute(request):
    try:
        user = request.user

        data = json.loads(request.body.decode('utf-8'))

        route = SavedRoute.objects.get(user=user, pk=data.get('routeId'))

        route.delete()

        return HttpResponse({'Route Deleted'}, content_type='application/json')
    except json.JSONDecodeError as e:
        return HttpResponse({'There has been an Error'}, content_type='application/json')
