import requests


def ip_verification(ip):

    headers = {
        "X-API-KEY": ""
    }

    url = f"https://api.us-east-1-main.seon.io/SeonRestService/ip-api/v1.1/{ip}"

    r = requests.get(url, headers=headers)

    return r.text
