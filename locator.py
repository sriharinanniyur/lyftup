def locate_me():
    import requests
    ip_request = requests.get('https://get.geojs.io/v1/ip.json')
    my_ip = ip_request.json()['ip']
    geo_request_url = 'https://get.geojs.io/v1/ip/geo/' + my_ip + '.json'
    geo_request = requests.get(geo_request_url)
    geo_data = geo_request.json()
    my_long = geo_data['longitude']
    my_lat = geo_data['latitude']
    return [float(my_lat), float(my_long)]
