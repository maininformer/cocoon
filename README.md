# Cocoon

This is the backend for the app Cocoon : https://github.com/cs160-sp16/Group-30-Project

#### Domain : cocoon-healthcare.herokuapp.com
#### Video : https://youtu.be/d1S3OY9g25Y

### APIs:

#### /login:

 - Inputs : { "name" : "" OR NAME, "email": EMAIL, "password": PASSWORD}
 - Output : SUCCESS or FAILURE to login or signup

NOTE: if it is a login, just send email and password and let name be "". But always do send a key for name as both signup and login use the same API.

#### /push :

 - Inputs : { "email": EMAIL, "password":PASSWORD, "intensity":INTENSITY(float), "lat": LATITUDE(float), "long": LONGITUDE(float)}
 - Output : SUCCESS or FAILURE to save the pushed data
 
#### /map :

 - Inputs : { "email": EMAIL, "password":PASSWORD, "offset":OFFSET(float), "lat": LATITUDE(float), "long": LONGITUDE(float)}
 - Output : {SUCCESS or FAILURE,"SoundMap":[[lat_1, long_1, intensity_1],...,[lat_i, long_i, intensity_i]]}

NOTE: The offset is a float that will define a bounding box relative to the sent latitude and longitude in the form, range(lat-offset, lat+offset), range(long-offset, long+offset). 

#### /recommend :
- Inputs : {'email' : EMAIL ,
                 'password' : PASS,
                 'lat' : CURRENT_LATITUDE,
                 'lng' : CURRENT_LONGITUDE,
                  **kwargs(required: see notes)}
-  Output : {SUCCESS or FAILURE, 'results':[{'cafe_distance': KM, 'cafe_lat': LAT, 'cafe_lng':LNG,
                                                  'cafe_name':NAME', 'noise_level': dB, 'pic_available': BOOL,
                                                  'pic_url': (see notes)},...,{...},...]}

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

In outputs,

            if no venues are found, a cute cactus image will be returned, along with the message.
            if the venue has no pictures, a url to the cocoon logo will be returned.(could have made this
            a kwarg too lol)
----------
Thank you.
