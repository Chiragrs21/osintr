import requests

# API key


def domain_search(domain):
    api_key = ''

    # Domain to search
    domain = 'www.bnmit.org'

    # API endpoint URL
    url = f'https://api.hunter.io/v2/domain-search?domain={domain}&api_key={api_key}'

    # Make the GET request
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        data = response.json()
        # Process the data as needed
        return data
    else:
        return 'Failed to retrieve data. Status code: {response.status_code}'
