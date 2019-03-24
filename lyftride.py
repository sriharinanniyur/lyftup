from lyft_rides.auth import ClientCredentialGrant
from lyft_rides.session import Session
import locator
from find_hospital import nearest_hospital
import creds
from lyft_rides.auth import AuthorizationCodeGrant
from lyft_rides.client import LyftRidesClient
import webbrowser
import time
import pprint
import json
pp = pprint.PrettyPrinter(indent=2)

lyft_start_latitude = locator.locate_me()[0]
lyft_start_longitude = locator.locate_me()[1]
lyft_end_latitude = nearest_hospital()[0]
lyft_end_longitude = nearest_hospital()[1]



def order():

    auth_flow = AuthorizationCodeGrant(
        creds.lyft_client_id,
        creds.lyft_client_secret,
        "public",
        )
    auth_url = auth_flow.get_authorization_url()
    my_redirect_url = input(print("Redirected URL: ")).strip()
    session = auth_flow.get_session(my_redirect_url)
    client = LyftRidesClient(session)
    x = len(client.get_pickup_time_estimates(lyft_start_latitude, lyft_start_longitude).json['eta_estimates'])
    y = 0
    lyft_eta_seconds = []
    while y < x:
        lyft_eta_seconds.append(client.get_pickup_time_estimates(lyft_start_latitude, lyft_start_longitude).json['eta_estimates'][y]['eta_seconds'])
        y += 1
    eta_seconds = int(min(lyft_eta_seconds))
    response = client.request_ride(
        ride_type='lyft',
        start_latitude=lyft_start_latitude,
        start_longitude=lyft_start_longitude,
        end_latitude=lyft_end_latitude,
        end_longitude=-lyft_end_longitude,
    )
