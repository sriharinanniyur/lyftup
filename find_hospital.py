from locator import locate_me
import math

hospital_locations = {
 "Alexian Extended Care Medical": [37.3801156, -121.828145],
 "Sequoia Hospital": [37.5487593, -122.3247962],
 "Kaiser Permanente Fremont Medical Center": [37.5327032, -121.9352979],
 "El Camino Hospital Los Gatos": [35.4591641294135, -78.2718824656421],
 "Npmhu San Jose Branch": [33.167531860302, -101.808302151291],
 "Evergreen Urgent Care": [33.9896778738004, -80.5205634987476],
 "Action Urgent Care": [37.3004037, -121.8211606],
 "Instant Urgent Care": [39.33357, -76.597417],
 "Action Urgent Care - Campbell": [40.4554274, -79.9009681],
 "San Jose Medical Group Urgent Care Center": [37.3742080820157, -122.115569621584],
 "Santa Clara Urgent Care": [42.4799992, -83.2439504],
 "CareNow Urgent Care - North San Jose": [37.3827114788186, -121.896779133865],
 "CareNow Urgent Care - Milpitas": [37.4150355306122, -121.87812144898],
 "U.S. HealthWorks Urgent Care": [40.1596227006798, -74.9235541310756],
 "Instant Urgent Care - Sunnyvale": [37.4274653, -122.1490025]
}
hospital_data_list = [
    {'lat': 37.3691, 'lon': -122.0799},
    {'lat': 37.3136, 'lon': -121.9343},
    {'lat': 37.3276, 'lon': -121.9390},
    {'lat': 37.2520, 'lon': -121.9465},
    {'lat': 37.3356, 'lon': -121.9989},
    {'lat': 37.3823, 'lon': -121.8984},
    {'lat': 37.4399, 'lon': -122.1612},

]

def distance_between_coordinates(a, b):
    return abs(math.hypot(abs(b[0] - a[0]), abs(b[1] - a[1])))

def nearest_hospital():
    my_location = locate_me()
    closest = [37.3801156, -121.828145]
    for coord in hospital_data_list:
        if (distance_between_coordinates(my_location, [coord['lat'], coord['lon']]) < distance_between_coordinates(my_location, closest)):
            closest = [coord['lat'], coord['lon']]
    return closest
