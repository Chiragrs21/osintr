import requests
import ipaddress


def ip4_geolocator(ip):
    api_key = ''
    ip_address = '172.16.128.45'
    url = f'https://api.ipgeolocation.io/ipgeo?apiKey={api_key}&ip={ip_address}'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return 'Failed to fetch data. Status code: {response.status_code}'
