from __future__ import division
from all.models import *
from django.shortcuts import HttpResponse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.views.decorators.csrf import csrf_exempt
import numpy as np
import os
import simplejson
import requests
import json
import certifi

def get_data_from_request(request,response_message,response_status=0):
    if request.method != 'POST':
        HttpResponse(simplejson.dumps({'Response Status':response_status,
                                       'Response Description':response_message[1]},
                                        separators=(',', ':'), sort_keys=True))
    else:
        data = simplejson.loads(request.body)
    return data

def validate_email_plum(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

def send_bug(message):
    from_email = os.environ['FROM_EMAIL']
    to_email = os.environ['TO_EMAIL']
    msg = EmailMessage('COCOON BUG REPORT', message, from_email, to_email)
    msg.send()
    return

def try_or_default(arg, default_value):
    return default_value if arg=="" else arg

def distance(lon1, lat1, lon2, lat2):
    lon1 = np.radians(lon1)
    lon2 = np.radians(lon2)
    lat1 = np.radians(lat1)
    lat2 = np.radians(lat2)
    R = 6371
    x = (lon2 - lon1) * np.cos( 0.5*(lat2+lat1) )
    y = lat2 - lat1
    d = R * np.sqrt( x*x + y*y )
    return round(d,2)

@csrf_exempt
def sign_up_login(request):
    """{name: False/name, email, password}"""
    response_message = {0:'Success',1:'request method must be POST',2:'password cannot be empty',
                        3:'invalid email address',4:'always send a "name" key, login ? name="" : name=name',
                        5:'Seems that someone else with the same email is in the dataset, plumSemPy has been notified',
                        6:'success', 7:'Invalid email or password', 8:'user already exists'}
    response_status = 0

    if request.method != 'POST':
        HttpResponse(simplejson.dumps({'Response Status':response_status,
                                       'Response Description':response_message[1]},
                                        separators=(',', ':'), sort_keys=True))
    else:
        data = simplejson.loads(request.body)
        try:
            name = data['name']
        except:
            HttpResponse(simplejson.dumps({'Response Status':response_status,
                                           'Response Description':response_message[4]}))

        email = data['email']
        password = data['password']

        if password=='':
            HttpResponse(simplejson.dumps({'Response Status':response_status,
                                           'Response Description':response_message[2]},
                                            separators=(',', ':'), sort_keys=True))

        if validate_email_plum(email)==False:
            HttpResponse(simplejson.dumps({'Response Status':response_status,
                                           'Response Description':response_message[3]},
                                            separators=(',', ':'), sort_keys=True))
        #######
        #Login#
        #######

        if name == '':
            user = Users.objects.filter(email=email)

            ### NON UNIQUE USER, this is JUST IN CASE, Django should catch it ###
            if len(user)>1:
                send_bug('NON UNIQUE USER')


                return HttpResponse(simplejson.dumps({'Response Status':response_status,
                                                      'Response Description':response_message[5]},
                                                      separators=(',', ':'), sort_keys=True))

            if user.exists()==1:
                if user[0].password == password:
                    response_status += 1
                    return HttpResponse(simplejson.dumps({'Response Status':response_status,
                                                          'Response Description':response_message[6]},
                                                          separators=(',', ':'), sort_keys=True))
                #Wrong password
                else:
                    return HttpResponse(simplejson.dumps({'Response Status':response_status,
                                                          'Response Description':response_message[7]},
                                                          separators=(',', ':'), sort_keys=True))
            #Not signed up
            else:
                return HttpResponse(simplejson.dumps({'Response Status':response_status,
                                                      'Response Description':response_message[7]},
                                                      separators=(',', ':'), sort_keys=True) )



        #########
        #Sign Up#
        #########
        else:
            user = Users.objects.filter(email=email)

            if user.exists()==1:
                return HttpResponse(simplejson.dumps({'Response Status':response_status,
                                                      'Response Description':response_message[8]},
                                                      separators=(',', ':'), sort_keys=True) )
            else:

                Users(email = email, name=name, password=password).save()
                response_status += 1
                return HttpResponse(simplejson.dumps({'Response Status':response_status,
                                                      'Response Description':response_message[6]},
                                                      separators=(',', ':'), sort_keys=True))

@csrf_exempt
def sound_push(request):
    """{name: False/name, email, password}"""
    response_message = {0:'Success',1:'request method must be POST',2:'password cannot be empty',
                        3:'invalid email address',4:'always send a "name" key, login ? name="" : name=name',
                        5:'Seems that someone else with the same email is in the dataset, plumSemPy has been notified',
                        6:'success', 7:'Invalid email or password'}
    response_status = 0


    data = get_data_from_request(request,response_message)
    email = data['email']
    password = data['password']
    intensity = data['intensity']
    lat = data['lat']
    lng = data['long']

    user = Users.objects.filter(email=email)
    if user.exists()==1:
        if user[0].password == password:
            SoundData(user = user[0], timestamp = tz.now(), lat = lat, long = lng, intensity = intensity).save()
            response_status += 1
            return HttpResponse(simplejson.dumps({'Response Status':response_status,
                                                  'Response Description':response_message[6]},
                                                   separators=(',', ':'), sort_keys=True))

        else:
            #Invalid password
            return HttpResponse(simplejson.dumps({'Response Status':response_status,
                                                  'Response Description':response_message[7]},
                                                  separators=(',', ':'), sort_keys=True) )
    else:
        #invalid user name
        return HttpResponse(simplejson.dumps({'Response Status':response_status,
                                                  'Response Description':response_message[7]},
                                                  separators=(',', ':'), sort_keys=True) )

@csrf_exempt
def sound_map(request):
    """{email, password, lat, long, offset}"""

    response_message = {0:'Success',1:'request method must be POST',2:'password cannot be empty',
                        3:'invalid email address',4:'always send a "name" key, login ? name="" : name=name',
                        5:'Seems that someone else with the same email is in the dataset, plumSemPy has been notified',
                        6:'success', 7:'Invalid email or password'}
    response_status = 0


    data = get_data_from_request(request,response_message)

    email = data['email']
    password = data['password']
    lat = float(data['lat'])
    lng = float(data['long'])
    offset = float(data['offset']) #to define the bounding box

    user = Users.objects.filter(email=email)
    if user.exists()==1:
        if user[0].password == password:

            sound_map = SoundData.objects.filter(lat__range=[lat-offset, lat+offset],
                                                 long__range=[lng-offset,lng+offset]).values_list('lat',
                                                                                                   'long',
                                                                                                   'intensity')
            #Making it JSON serlializable
            sound_map = [list(sound) for sound in sound_map]

            response_status += 1
            return HttpResponse(simplejson.dumps({'Response Status':response_status,
                                                  'Response Description':response_message[6],
                                                  'SoundMap':sound_map},
                                                   separators=(',', ':'), sort_keys=True))

        else:
            #Invalid password
            return HttpResponse(simplejson.dumps({'Response Status':response_status,
                                                  'Response Description':response_message[7]},
                                                  separators=(',', ':'), sort_keys=True) )
    else:
        #invalid user name
        return HttpResponse(simplejson.dumps({'Response Status':response_status,
                                                  'Response Description':response_message[7]},
                                                  separators=(',', ':'), sort_keys=True) )

@csrf_exempt
def recommend(request):
    """inputs : {'email' : EMAIL ,
                 'password' : PASS,
                 'lat' : CURRENT_LATITUDE,
                 'lng' : CURRENT_LONGITUDE,
                  **kwargs(required: see notes)}
        output : {SUCCESS or FAILURE, 'results':[{'cafe_distance': KM, 'cafe_lat': LAT, 'cafe_lng':LNG,
                                                  'cafe_name':NAME', 'noise_level': dB, 'pic_available': BOOL,
                                                  'pic_url': (see notes)}]}

        NOTES: The keyword arguments for the inputs are mandatory, I purposefully disallowed them to fail
        silently. If no values are provided there are default values in the API. For any key if the default
        value is okay, please pass "" as the value for that key. The keys are:
            'diameter' : (int or float) the diamater around the user, default is 4 kilometers,
            'granularity' : (int) number of grid nodes in each direction, default 4,
            'image_max_width: (int) this is required by the google api, default is 400,
            'noise_mu' : (int or float) the mean value of the sound intesity, default 70 dB,
            'noise_sigma' : (int or float) the STD value of the sound intensity, default 30 dB,
            'how_many_silent':(int) for each node, how many silent cafes should googel return? ,default 5. Also
            please be mindful of this number as each added number is another api call on my account.
            'radius_of_search':(int or float) how far should google search from a node to find cafes? default 500,
            Please note if this radius is bigger than the node distances then extraneous calls will be made

        In outputs, if no venues are found, a cute cactus image will be returned, along with the message.
                    if the venue has no pictures, a url to the cocoon logo will be returned.(could have made this
                    a kwarg too lol)"""

    response_message = {0:'Success',1:'request method must be POST',2:'password cannot be empty',
                        3:'invalid email address',4:'always send a "name" key, login ? name="" : name=name',
                        5:'Seems that someone else with the same email is in the dataset, plumSemPy has been notified',
                        6:'success', 7:'Invalid email or password', 8:'No venues found :('}
    response_status = 0


    data = get_data_from_request(request,response_message)

    email = data['email']
    password = data['password']
    lat = float(data['lat'])
    lng = float(data['lng'])
    kwargs = data['kwargs']
    diameter = try_or_default(kwargs['diameter'],4)
    image_max_width = try_or_default(kwargs['image_max_width'],400)
    granularity = try_or_default(kwargs['granularity'],4)
    noise_mu = try_or_default(kwargs['mu'],70)
    noise_sigma = try_or_default(kwargs['sigma'],30)
    how_many_silent = try_or_default(kwargs['how_many_silent'],1)
    radius_of_search = try_or_default(kwargs['radius_of_search'],500)


    #Verify user
    user = Users.objects.filter(email=email)
    if user.exists()==1:
        #if verified:
        if user[0].password == password:
            #Make noise distribution grid around them, query the n most silent ones
            #defining the bounding box
            start_lat = lat - (1/110.574) * (diameter/2)
            start_lng = lng - (1/(111.320*np.cos(start_lat))) * (diameter/2)

            end_lat = lat + (1/110.574) * (diameter/2)
            end_lng = lng + (1/(111.320*np.cos(start_lat))) * (diameter/2)

            #Making a mesh grid
            lat_grid, lng_grid = np.meshgrid(np.linspace(start_lat,end_lat,granularity),
                                     np.linspace(start_lng, end_lng, granularity))
            #Distributing noise levels
            noise_levels = np.random.randn(granularity**2)*noise_sigma+noise_mu

            #Making the noise data
            data = np.array([(lat,lng, noise) for lat,lng,noise in zip(lat_grid.ravel(),
                                                                       lng_grid.ravel(),
                                                                       noise_levels)])

            top_n_silent_index = data[:,2].argsort()[:how_many_silent]
            top_n_silent = data[top_n_silent_index]
            #call google to return cafes in 500 meters around that silent place
            key = os.environ['GOOGLE_API_KEY']
            results=[]
            for i,point in enumerate(top_n_silent):
                to_go_lat = point[0]
                to_go_lng = point[1]

                url = r'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={0},{1}&radius={2}&type=cafe&key={3}'.format(to_go_lat,
                                                                                                                                           to_go_lng,
                                                                                                                                           radius_of_search,
                                                                                                                                           key)

                r = requests.post(url,verify=certifi.old_where())

                try:
                    cafe_lat = r.json()['results'][0]['geometry']['location']['lat']
                    cafe_lng = r.json()['results'][0]['geometry']['location']['lng']
                    cafe_name = r.json()['results'][0]['name']
                    cafe_distance = distance(lng, lat, cafe_lng, cafe_lat)
                except IndexError:
                    if i==how_many_silent-1:
                        response_status +=1
                        return HttpResponse(simplejson.dumps({'Response Status':response_status,
                                                          'Response Description':response_message[8],
                                                          'results':['http://s2.favim.com/orig/37/aww-cactus-cute-friendship-green-Favim.com-304829.jpg']},
                                                           separators=(',', ':'), sort_keys=True) )
                    else:
                        continue

                try:
                    cafe_photo_reference = r.json()['results'][0]['photos'][0]['photo_reference']
                    pic_url = r'https://maps.googleapis.com/maps/api/place/photo?maxwidth={0}&photoreference={1}&key={2}'.format(image_max_width,
                                                                                                                             cafe_photo_reference,
                                                                                                                             key)
                    pic_available = 1

                except KeyError:
                    pic_url = r'http://s32.postimg.org/up9zw3udx/circle_logo.png'
                    pic_available = 0

                #get the name of the place, lat,long, and the image url and send back
                results.append({'cafe_lat':cafe_lat, 'cafe_lng':cafe_lng,'cafe_name':cafe_name,'pic_url':pic_url,
                                'noise_level':point[2], 'pic_available':pic_available,
                                'cafe_distance':cafe_distance})




            response_status +=1
            return HttpResponse(simplejson.dumps({'Response Status':response_status,
                                                  'Response Description':response_message[0],
                                                  'results':results},
                                                   separators=(',', ':'), sort_keys=True) )
        #if not verified : invalid user/pass
        else:
                #Invalid password
                return HttpResponse(simplejson.dumps({'Response Status':response_status,
                                                      'Response Description':response_message[7]},
                                                      separators=(',', ':'), sort_keys=True) )
    else:
        #invalid user name
        return HttpResponse(simplejson.dumps({'Response Status':response_status,
                                                  'Response Description':response_message[7]},
                                                  separators=(',', ':'), sort_keys=True) )



