from lyft_rides.auth import ClientCredentialGrant
from lyft_rides.session import Session
from lyft_rides.client import LyftRidesClient
import json
import creds
auth_flow = ClientCredentialGrant(
    creds.lyft_client_id,
    creds.lyft_client_secret,
    "public",
    )
session = auth_flow.get_session()

client = LyftRidesClient(session)
response = client.get_drivers(37.7833, -122.4167)
ride_types = response.json.get('ride_types')

print(ride_types)
