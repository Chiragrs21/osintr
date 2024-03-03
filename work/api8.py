import requests


def email_social_media(email):

    headers = {
        "X-API-KEY": ""
    }

    email_address = email
    url = f"https://api.us-east-1-main.seon.io/SeonRestService/email-api/v2/{email_address}"

    r = requests.get(url, headers=headers)

    return r.text
