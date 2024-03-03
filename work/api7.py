import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning


def email_reader(email):
    url = f'https://api.eva.pingutil.com/email?email={email}'

    # Disable SSL certificate verification
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    response = requests.get(url, verify=False)

    if response.status_code == 200:
        data = response.json()
        # Process the data here
        return data
    else:
        return 'Failed to fetch data:', response.status_code, response.text
