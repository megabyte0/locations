from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Max
from locations.models import Location, KnownLocation
import json
DEBUG = True
#DEBUG = False

@csrf_exempt
def store(request,person_id):
    global DEBUG
    if (not DEBUG):
        timestamps=[]
    else:
        args = Location.objects.filter(owner=person_id)
        timestamps=[i.timestamp for i in args]
    locations=json.loads(request.body)
    for i in range(len(locations)):
        locations[i].update({'owner':person_id})
    to_store = [Location(**i) for i in locations if i['timestamp'] not in timestamps]
    Location.objects.bulk_create(to_store)
    res=[i['timestamp'] for i in locations]
    return JsonResponse(res,safe=False)
    #HttpResponse("Hello, %s. You're at the polls index. '%s'"%(person_id,request.body))

def display(request,person_id,time_sub):
    args = Location.objects.filter(owner=person_id)
    max_time = args.aggregate(Max('timestamp'))['timestamp__max']
    #return JsonResponse(max_time)
    if max_time == None:
        return JsonResponse([],safe=False)
    start_time = max_time - time_sub * 1000
    res = args.filter(timestamp__gte=start_time)
    res = [{
    'latitude': i.latitude,
    'longitude': i.longitude,
    'provider': i.provider,
    'accuracy': i.accuracy,
    'altitude': i.altitude,
    'bearing': i.bearing,
    'speed': i.speed,
    'time': i.time,
    'timestamp': i.timestamp,
    'owner': i.owner
    } for i in res]
    return JsonResponse(res,safe=False)

@csrf_exempt
def test(request):
    return HttpResponse("passed")

def known_locations(request):
    return JsonResponse([{
    'latitude': i.latitude,
    'longitude': i.longitude,
    'name': i.name.rstrip('\n')
    } for i in KnownLocation.objects.all()],safe=False)

@csrf_exempt
def store_known_locations(request):
    lat_lon = [(i.latitude,i.longitude) for i in KnownLocation.objects.all()]
    locations=json.loads(request.body)
    to_store = [KnownLocation(**i) for i in locations if (i['latitude'],i['longitude']) not in lat_lon]
    KnownLocation.objects.bulk_create(to_store)
    return HttpResponse("",status=204)
