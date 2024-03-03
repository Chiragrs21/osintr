import requests


def ipv6_location(ip):
    def get_geolocation(ip_address, api_key):
        url = f"https://ipgeolocation.abstractapi.com/v1/?api_key={api_key}&ip_address={ip_address}"
        response = requests.get(url)
        data = response.json()
        return data

    # Example usage
    api_key = ""
    # Replace with the IP address you want to look up
    ip_address = ip  # only ipv6 works
    result = get_geolocation(ip_address, api_key)
    return result
