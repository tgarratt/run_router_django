from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect

import googlemaps
import json

import environ
env = environ.Env()
environ.Env.read_env()

# Create your views here.

def RunRouter(request):
    if request.method == 'POST':

        data = json.loads(request.body.decode('utf-8'))
        rangeInt = int(data.get("range"))

        origin = data.get("start")
        destination = data.get("maxRangePoint")
        # take the number of km, half it to account for there and back, turn it to meters, then add a bit of wiggle room
        max_distance = rangeInt / 2 + 50


        # routes coords
        gmaps = googlemaps.Client(key=env('CLOUD_API_KEY'))
        directions = gmaps.directions(origin, destination, mode="walking", units="metric")


        # extract the coords from the response
        total_distance = 0
        generated_waypoint = []
        for step in directions[0]['legs'][0]['steps']:
            step_distance = step['distance']['value']

            if total_distance + step_distance <= max_distance :
                generated_waypoint = [step['end_location']['lat'], step['end_location']['lng']]
                total_distance += step_distance
            else:
                # If the next step would exceed the maximum distance, break the loop
                break

        generated_waypoint_json = json.dumps(generated_waypoint)
        request.session['generatedWaypoint'] = generated_waypoint_json

        return HttpResponse(generated_waypoint_json, content_type='application/json')
    else:
        no_post_response = request.session.get('generatedWaypoint', 'no data provided')

        return HttpResponse(no_post_response, content_type='application/json')
