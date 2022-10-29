# in progress

# estimates apparent sunrise and sunset times
# includes effects of atmospheric refraction
# does not include effects of mountain ranges, etc.

# based on Richard Droste (2022). sunRiseSet( lat, lng, UTCoff, date, PLOT) (https://www.mathworks.com/matlabcentral/fileexchange/62180-sunriseset-lat-lng-utcoff-date-plot), MATLAB Central File Exchange. Retrieved October 28, 2022. 
# which was based on these spreadsheets by the NOAA https://gml.noaa.gov/grad/solcalc/calcdetails.html
# which were based on equations from Astronomical Algorithms, by Jean Meeus
# adaptations in other languages can be found at https://math.stackexchange.com/questions/2186683/how-to-calculate-sunrise-and-sunset-times/2598266#2598266


import time
import math


def radians_to_degrees(rad):
    return rad * (180 / math.pi)


def degrees_to_radians(deg):
    return deg * (math.pi / 180)


def scale_seconds(seconds):
    # scales seconds to fit within 0 - 1
    seconds_per_day = 60 * 60 * 24
    return seconds / seconds_per_day


def julian_day(days_since_epoch, seconds_scaled, utc_offset):
    return days_since_epoch + 2415018.5 + seconds_scaled - (utc_offset / 24)


def julian_century(jul_day):
    return (jul_day - 2451545) / 36525


def geom_mean_long_sun(jul_cent):
    # the geometric mean of the longitude of the sun
    # in degrees
    # math.fmod is recommended by the python documentation for floats
    return math.fmod((280.46646 + jul_cent * (36000.76983 + jul_cent * 0.0003032)), 360.0)

def geom_mean_anom_sun(jul_cent):
    # the geometric mean anomaly of the sun
    # in degrees
    return 357.52911 + jul_cent * (35999.05029 - 0.0001537 * jul_cent)


def eccent_earth_orbit(jul_cent):
    # the eccentricity of earth's orbit
    return 0.016708634 - jul_cent * (0.000042037 + 0.0000001267 * jul_cent)


def sun_eq_of_ctr(geom_mean_anom_sun, jul_cent):
    # the sun's equation of the center
    return math.sin(degrees_to_radians(geom_mean_anom_sun)) * (1.914602 - jul_cent * (0.004817 + 0.000014 * jul_cent))+math.sin(degrees_to_radians(2 * geom_mean_anom_sun)) * (0.019993 - 0.000101 * jul_cent)+math.sin(degrees_to_radians(3 * geom_mean_anom_sun)) * 0.000289

def estimate_sunrise_sunset(latitude, longitude, utc_offset, date, seconds_since_midnight, return_seconds = False):
    ''' estimates the apparent sunrise and sunset times
        inputs latitude, longitude, utc_offset, date
        outputs sunrise_time, sunset_time, error

        ex. ->
    '''
    ###### validation of latitude and longitude

    ###### validation of utc_offset

    ###### validation of date

    ###### days since 12/30/1899
    #! note this is the epoch for microsoft office
    #! the ancestor of this code was made in Excel
    #! the epoch in my system is January 1, 1970
    #! I wonder whether this will cause trouble
    
    sunrise = 5
    sunset = 5
    if return_seconds:
        print(sunrise, sunset)
        return {'sunrise' : sunrise, 'sunset' : sunset}
    else:
        ######convert sunrise and sunset to hours + minutes + seconds
        print("under construction")
        return {'sunrise' : sunrise, 'sunset' : sunset}


def get_sunrise_sunset(latitude, longitude, utc_offset, date, event):
    ''' as time passes, the estimated sunrise and sunset times for this day change
        this function uses a loop to find the time where the (time of day) and (estimated sunrise, sunset times) intersect '''
    

    # get sunrise
    for time_elapsed in range(1, seconds_per_day + 1):
        if time_elapsed < estimate_sunrise_sunset(latitude, longitude, utc_offset, date, seconds_since_midnight=time_elapsed, return_seconds=True)['sunrise']:
            continue
        else:
            print('got sunrise')
            sunrise_in_seconds = time_elapsed
            break
    # get sunset
    for time_elapsed in range(1, seconds_per_day + 1):
        if time_elapsed < estimate_sunrise_sunset(latitude, longitude, utc_offset, date, seconds_since_midnight=time_elapsed, return_seconds=True)['sunset']:
            continue
        else:
            print('got sunset')
            sunset_in_seconds = time_elapsed
            break
    ######convert sunrise_in_seconds, sunset_in_seconds to datetime format
    return sunrise_in_datetime, sunset_in_datetime

if __name__ == '__main__':
    print('Well hello, Sonny.')
    print(time.localtime())
    get_sunrise_sunset(1,1,1,1,1)
 