from flask import *
from flask_googlemaps import GoogleMaps
from lyftride import order
from find_hospital import nearest_hospital
from locator import locate_me
from lyft_rides.auth import ClientCredentialGrant
from lyft_rides.session import Session
import locator, creds, webbrowser, time, pprint, json
from find_hospital import nearest_hospital
from lyft_rides.auth import AuthorizationCodeGrant
from lyft_rides.client import LyftRidesClient
from flask_googlemaps import Map

mymap = Map(
    identifier="mymap",
    lat=37.4419,
    lng=-122.1419,
    markers=[{
        'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
        'lat': 37.4419,
        'lng': -122.1419,
        'infobox': "Your Location"
    },
    {   'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
        'lat': nearest_hospital()[0],
        'lng': nearest_hospital()[1],
        'infobox': "Nearest Hospital"
    }
    ]
)
yourmap = Map(
    identifier="yourmap",
    lat=37.4419,
    lng=-122.1419,
    markers=[{
        'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
        'lat': 37.4419,
        'lng': -122.1419,
        'infobox': "Your Location"
    },
    {   'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
        'lat': nearest_hospital()[0],
        'lng': nearest_hospital()[1],
        'infobox': "Nearest Hospital"
    }
    ]
)

medics = []

app = Flask(__name__)
app.config['GOOGLEMAPS_KEY'] = "AIzaSyAMIY4ozo4newtFCoD-7wno2dJlHvSDwFc"
GoogleMaps(app)

@app.route('/', methods=["GET","POST"])
def home():
    return render_template('index.html', mymap=mymap, medic_list=medics)

@app.route('/register_page')
def register_page():
    return render_template("register_medic.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        medics.append(request.form['driver_id'])
    return render_template('index.html',mymap=mymap, medic_list=medics)

@app.route('/order',methods=['GET', 'POST'])
def order():
    if request.method == "POST":
        mymap = Map(
            identifier="mymap",
            lat=37.4419,
            lng=-122.1419,
            markers=[{
                'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
                'lat': 37.4419,
                'lng': -122.1419,
                'infobox': "Your Location"
            },
            {   'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
                'lat': nearest_hospital()[0],
                'lng': nearest_hospital()[1],
                'infobox': "Nearest Hospital"
            }
            ]
        )
        lyft_start_latitude = locator.locate_me()[0]
        lyft_start_longitude = locator.locate_me()[1]
        lyft_end_latitude = nearest_hospital()[0]
        lyft_end_longitude = nearest_hospital()[1]
        auth_flow = ClientCredentialGrant(
            creds.lyft_client_id,
            creds.lyft_client_secret,
            "public"
        )
        session = auth_flow.get_session()
        client = LyftRidesClient(session)
        x=len(client.get_pickup_time_estimates(lyft_start_latitude, lyft_start_longitude).json['eta_estimates'])
        lyft_eta_seconds = []
        myauth_flow = AuthorizationCodeGrant(
            creds.lyft_client_id,
            creds.lyft_client_secret,
            "public",
        )
        auth_url = myauth_flow.get_authorization_url()
        y = 0
        while y < x:
            lyft_eta_seconds.append(client.get_pickup_time_estimates(lyft_start_latitude, lyft_start_longitude).json['eta_estimates'][y]['eta_seconds'])
            y += 1
        eta_seconds = int(min(lyft_eta_seconds))
        return render_template('order.html',eta_seconds=eta_seconds,auth_url=auth_url, yourmap=yourmap)
    return render_template('order.html',eta_seconds=eta_seconds,auth_url=auth_url, yourmap=yourmap)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
