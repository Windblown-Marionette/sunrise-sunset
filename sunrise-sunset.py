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
from urllib.parse import _NetlocResultMixinStr


def radians_to_degrees(rad):
    return rad * (180 / math.pi)


def degrees_to_radians(deg):
    return deg * (math.pi / 180)


def scale_seconds(seconds):
    # scales seconds to fit within 0 - 1 days
    assert seconds < 60 * 60 * 24, 'Unexpected: more than a day\'s worth of seconds.'
    seconds_per_day = 60 * 60 * 24
    return seconds / seconds_per_day


def julian_day(days_since_unix_epoch=None, utc_offset=0):
    epoch_displacement = 25569  # distance from excel epoch to time.time epoch (unix epoch, January 1st 1970 00:00:00) 
    julian_date_offset = 2415018.5  # in-built conversion from excel epoch (12/30/1899) to julian days
    if days_since_unix_epoch is None:
        days_since_unix_epoch = time.time() / (60 * 60 * 24)  # time.time_ns() may improve accuracy
    return days_since_unix_epoch + epoch_displacement + julian_date_offset - (utc_offset / 24)


def julian_century(jul_day):
    return (jul_day - 2451545) / 36525


def geom_mean_long_sun(jul_cent):
    # the geometric mean of the longitude of the Sun
    # in degrees
    # math.fmod is recommended by the python documentation for floats
    return math.fmod((280.46646 + jul_cent * (36000.76983 + jul_cent * 0.0003032)), 360.0)


def geom_mean_anom_sun(jul_cent):
    # the geometric mean anomaly of the Sun
    # in degrees
    return 357.52911 + jul_cent * (35999.05029 - 0.0001537 * jul_cent)


def eccent_earth_orbit(jul_cent):
    # the eccentricity of Earth's orbit
    return 0.016708634 - jul_cent * (0.000042037 + 0.0000001267 * jul_cent)


def sun_eq_of_ctr(geom_mean_anom_sun, jul_cent):
    # the Sun's equation of the center
    return math.sin(degrees_to_radians(geom_mean_anom_sun)) * (1.914602 - jul_cent * (0.004817 + 0.000014 * jul_cent))+math.sin(degrees_to_radians(2 * geom_mean_anom_sun)) * (0.019993 - 0.000101 * jul_cent)+math.sin(degrees_to_radians(3 * geom_mean_anom_sun)) * 0.000289


def sun_true_long(geom_mean_long_sun, sun_eq_of_ctr):
    # the true longitude of the Sun
    # in degrees
    return geom_mean_long_sun + sun_eq_of_ctr


def sun_true_anom(geom_mean_anom_sun, sun_eq_of_ctr):
    # the true anomaly of the Sun
    # in degrees
    return geom_mean_anom_sun + sun_eq_of_ctr


def sun_rad_vector(eccent_earth_orbit, sun_true_anom):
    # the Sun radius vector
    # in AUs
    return (1.000001018 * (1 - eccent_earth_orbit * eccent_earth_orbit)) / (1 + eccent_earth_orbit * math.cos(degrees_to_radians(sun_true_anom)))


def sun_app_long(sun_true_long, julian_century):
    # the sun's apparent longitude
    # in degrees
    return sun_true_long - 0.00569 - 0.00478 * math.sin(degrees_to_radians(125.04 - 1934.136 * julian_century))


def mean_obliq_ecliptic(julian_century):
    # the sun's mean obliquity of the ecliptic
    # in degrees
    return 23 + (26 + ((21.448 - julian_century * (46.815 + julian_century * (0.00059 - julian_century * 0.001813)))) / 60) / 60
    

def obliq_corr(mean_oblique_ecliptic, julian_century):
    # I do not know what this term is
    # in degrees
    return mean_oblique_ecliptic + 0.00256 * math.cos(degrees_to_radians(125.04 - 0.136 * julian_century))


def sun_rt_ascen(sun_app_long, obliq_corr):
    # the right ascension of the Sun
    # in degrees
    return radians_to_degrees(math.arctan2(math.cos(degrees_to_radians(sun_app_long)), math.cos(degrees_to_radians(obliq_corr)) * math.sin(degrees_to_radians(sun_app_long))))


def sun_declin(sun_app_long, obliq_corr):
    # the declination angle of the Sun
    # in degrees
    return radians_to_degrees(math.asin(math.sin(degrees_to_radians(obliq_corr)) * math.sin(degrees_to_radians(sun_app_long))))


def var_y(obliq_corr):
    # I do not know what this term is
    return math.tan(degrees_to_radians(obliq_corr / 2)) * math.tan(degrees_to_radians(obliq_corr / 2))


def eq_of_time(geom_mean_long_sun, geom_mean_anom_sun, eccent_earth_orbit, var_y):
    # the equation of time
    # in minutes
    return 4 * radians_to_degrees(var_y * math.sin(2 * degrees_to_radians(geom_mean_long_sun)) - 2 * eccent_earth_orbit * math.sin(degrees_to_radians(geom_mean_anom_sun)) + 4 * eccent_earth_orbit * var_y * math.sin(degrees_to_radians(geom_mean_anom_sun)) * math.cos(2 * degrees_to_radians(geom_mean_long_sun)) - 0.5 * var_y * var_y * math.sin(4 * degrees_to_radians(geom_mean_long_sun)) - 1.25 * eccent_earth_orbit * eccent_earth_orbit * math.sin(2 * degrees_to_radians(geom_mean_anom_sun)))


def ha_sunrise(sun_declin, lattitude):
    # I do not know what this term is
    # lattitude is + to North
    # in degrees
    return radians_to_degrees(math.acos(math.cos(degrees_to_radians(90.833)) / (math.cos(degrees_to_radians(lattitude)) * math.cos(degrees_to_radians(sun_declin))) - math.tan(degrees_to_radians(lattitude)) * math.tan(degrees_to_radians(sun_declin))))


def solar_noon(eq_of_time, longitude, time_zone):
    # solar noon in LST, or Local Sidereal Time
    # https://greenbankobservatory.org/education/great-resources/lst-clock/
    # longitude is + to East
    # time zone is + to East
    return (720 - 4 * longitude - eq_of_time + time_zone * 60) / 1440


def sunrise_time(solar_noon, ha_sunrise):
    # sunrise time in LST, or Local Sidereal Time
    # https://greenbankobservatory.org/education/great-resources/lst-clock/
    return solar_noon - ha_sunrise * 4 / 1440


def sunset_time(solar_noon, ha_sunrise):
    # sunset time in LST, or Local Sidereal Time
    # https://greenbankobservatory.org/education/great-resources/lst-clock/
    return solar_noon + ha_sunrise * 4 / 1440


def sunlight_duration(ha_sunrise):
    # in minutes
    return 8 * ha_sunrise


def true_solar_time(seconds_since_midnight, eq_of_time, longitude, time_zone):
    # in minutes
    ##### seconds_since midnight may be the wrong variable for this
    ##### so I will convert it to minutes since midnight to match the 1440, which may be (60min/hr * 24hr)
    # longitude is + to East
    # time zone is + to East
    math.fmod(seconds_since_midnight / 60 * 1440 + eq_of_time + 4 * longitude - 60 * time_zone, 1440)


def hour_angle(true_solar_time):
    # in degrees
    if(true_solar_time / 4 < 0):
        return true_solar_time / 4 + 180
    else:
        return true_solar_time / 4 - 180


def solar_zenith_angle(sun_declin, hour_angle, latitude):
    # in degrees
    # latitude is + to North
    return radians_to_degrees(math.acos(math.sin(degrees_to_radians(latitude)) * math.sin(degrees_to_radians(sun_declin)) + math.cos(degrees_to_radians(latitude)) * math.cos(degrees_to_radians(sun_declin)) * math.cos(degrees_to_radians(hour_angle))))


def solar_elevation_angle(solar_zenith_angle):
    # in degrees
    return 90 - solar_zenith_angle


def approx_atmospheric_refraction(solar_elevation_angle):
    # approximate atmospheric refraction
    # in degrees
    if solar_elevation_angle>85:
        return 0
    elif solar_elevation_angle > 5:
        return 58.1 / math.tan(degrees_to_radians(solar_elevation_angle)) - 0.07 / (math.tan(degrees_to_radians(solar_elevation_angle)) ** 3) + 0.000086 / math.tan(degrees_to_radians(solar_elevation_angle)) ** 5
    elif solar_elevation_angle > -0.575:
        return 1735 + solar_elevation_angle * (-518.2 + solar_elevation_angle * (103.4 + solar_elevation_angle * (-12.79 + solar_elevation_angle * 0.711)))
    else:
        return -20.772 / math.tan(degrees_to_radians(solar_elevation_angle)) / 3600


def solar_elevation_using_atmospheric_refraction(solar_elevation_angle, approx_atmospheric_refraction):
    # solar elevation corrected for atmospheric refraction
    # in degrees
    return solar_elevation_angle + approx_atmospheric_refraction


def solar_azimuth_angle(latitude, sun_declin, hour_angle, solar_zenith_angle):
    # in degrees clockwise from North
    if hour_angle > 0:
        return math.fmod(radians_to_degrees(math.acos(((math.sin(degrees_to_radians(latitude)) * math.cos(degrees_to_radians(solar_zenith_angle))) - math.sin(degrees_to_radians(sun_declin))) / (math.cos(degrees_to_radians(latitude)) * math.sin(degrees_to_radians(solar_zenith_angle))))) + 180, 360.0)
    else:
        return math.fmod(540 - radians_to_degrees(math.acos(((math.sin(degrees_to_radians(latitude)) * math.cos(degrees_to_radians(solar_zenith_angle))) - math.sin(degrees_to_radians(sun_declin))) / (math.cos(degrees_to_radians(latitude)) * math.sin(degrees_to_radians(solar_zenith_angle))))), 360.0)


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
    
    seconds_per_day = 60 * 60 * 24

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


def compare_to_expected_outputs():
    # iterates through a list of the above calculation functions
    # compares the outputs to the original spreadsheet's outputs
    # the following values will be used to match the spreadsheet default for the top row: lat, long, time zone, date

    lat = 40  # + to N
    long = -105  # + to E
    time_zone = -6  # + to E
    epoch_sample_time = time.strptime('6 21 2010 6', '%m %d %Y %M')  # 6/21/2010 and 6 minutes
    epoch_sample_time = time.mktime(epoch_sample_time) / (60 * 60 * 24)  # converted to seconds and then to days
    
    function_dictionary = {'radians_to_degrees' : {'function' : radians_to_degrees, 'input' : [2], 'spreadsheet_output': None},
                           'degrees_to_radians' : {'function' : degrees_to_radians, 'input' : [2], 'spreadsheet_output': None},
                           'scale_seconds': {'function' : scale_seconds, 'input' : [2], 'spreadsheet_output' : None},
                           'julian_day' : {'function' : julian_day, 'input' : [epoch_sample_time, time_zone], 'spreadsheet_output' : 2455368.75}}

    for function in function_dictionary.keys():
        function_dictionary[function]['function_output'] = function_dictionary[function]['function'](*function_dictionary[function]['input'])
    for function in function_dictionary.keys():
        print('Function:', function, ' | Input value:', function_dictionary[function]['input'], 
        ' | Function output:', function_dictionary[function]['function_output'], 
        ' | Spreadsheet output:', function_dictionary[function]['spreadsheet_output'],
        )


if __name__ == '__main__':
    print('Well hello, Sonny.')
    print(time.localtime())
    #get_sunrise_sunset(1,1,1,1,1)
    compare_to_expected_outputs()