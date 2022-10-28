# in progress

# estimates apparent sunrise and sunset times
# includes effects of atmospheric refraction
# does not include effects of mountain ranges, etc.
# based on https://github.com/kelvins/sunrisesunset
# based on Richard Droste (2022). sunRiseSet( lat, lng, UTCoff, date, PLOT) (https://www.mathworks.com/matlabcentral/fileexchange/62180-sunriseset-lat-lng-utcoff-date-plot), MATLAB Central File Exchange. Retrieved October 28, 2022. 
# adaptations in other languages can be found at https://math.stackexchange.com/questions/2186683/how-to-calculate-sunrise-and-sunset-times/2598266#2598266


import time
import math


def radians_to_degrees(rad):
    return rad * (180 / math.pi)


def degrees_to_radians(deg):
    return deg * (180 / math.pi)

    
def get_sunrise_sunset(latitude, longitude, utc_offset, date):
    ''' estimates the apparent sunrise and sunset times
        inputs latitude, longitude, utc_offset, date
        outputs sunrise_time, sunset_time, error

        ex. ->
    '''
    # validation of latitude and longitude

    # validation of utc_offset

    # validation of date

    # days since 12/30/1899
    #! note this is the epoch for microsoft office
    #! the ancestor of this code was made in Excel
    #! the epoch in my system is January 1, 1970
    #! I wonder whether this will cause trouble



if __name__ == '__main__':
    print('Well hello, Sonny.')
    print(time.localtime())
    #get_sunrise_sunset()
 