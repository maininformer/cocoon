from all.models import *
from django.shortcuts import HttpResponse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.views.decorators.csrf import csrf_exempt
import os
import simplejson

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



