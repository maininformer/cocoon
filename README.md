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


----------
Thank you.
