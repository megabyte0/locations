from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Max
from locations.models import Location, KnownLocation, TrackStatus
import json
DEBUG = True
#DEBUG = False

@csrf_exempt
def store(request,person_id):
    return JsonResponse(store_inner(request,person_id),safe=False)
    #HttpResponse("Hello, %s. You're at the polls index. '%s'"%(person_id,request.body))

def store_inner(request,person_id):
    global DEBUG
    locations_to_add=json.loads(request.body)
    if (not DEBUG):
        timestamps=[]
    else:
        locations_stored = Location.objects.filter(owner=person_id).filter(timestamp__in=[
            i['timestamp'] for i in locations_to_add
        ])
        timestamps=[i.timestamp for i in locations_stored]
    for i in range(len(locations_to_add)):
        locations_to_add[i].update({'owner':person_id})
    to_store = [
        Location(**i)
        for i in locations_to_add
        if i['timestamp'] not in timestamps
        ]
    Location.objects.bulk_create(to_store)
    locations_stored = Location.objects.filter(owner=person_id).filter(timestamp__in=[
        i['timestamp'] for i in locations_to_add
    ])
    res=[i.timestamp for i in locations_stored]
    return res

@csrf_exempt
def store_get(request,person_id,tracked_id,timestamp=None):
    stored = store_inner(request,person_id)
    if timestamp:
        update = track_inner(None,tracked_id,timestamp+1)
        TrackStatus.objects.bulk_create([
            TrackStatus(
                who=person_id,whom=tracked_id,
                timestamp=i['timestamp'])
            for i in update
            ])
        return JsonResponse({"stored":stored,"update":update})
    subquery = TrackStatus.objects.filter(
        who=person_id,
        whom=tracked_id
        ).values('timestamp')
    update = track_inner(None,tracked_id,None,subquery)
    return JsonResponse({"stored":stored,"update":update})

def track(request,person_id,time_sub):
    locations = Location.objects.filter(owner=person_id)
    max_time = locations.aggregate(Max('timestamp'))['timestamp__max']
    #return JsonResponse(max_time)
    if max_time == None:
        return JsonResponse([],safe=False)
    start_time = max_time - time_sub * 1000
    return JsonResponse(track_inner(locations,person_id,start_time),safe=False)

def track_inner(locations,person_id,start_time=None,excluded=[]):
    if locations == None:
        locations = Location.objects.filter(owner=person_id)
    res = locations
    if start_time != None:
        res = res.filter(timestamp__gte=start_time)
    if excluded:
        res=res.exclude(timestamp__in=excluded)##
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
    return res    

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
