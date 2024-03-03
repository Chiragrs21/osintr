import requests

api_key = ""
ip_address = " 2409:40f2:1007:3897:3cfd:c42e:8cca:9f5c"  # Example IP address

url = f"https://api.ip2location.io/?key={api_key}&ip={ip_address}&format=json    "


response = requests.get(url)
response.raise_for_status()  # Raise an exception for HTTP errors
data = response.json()
print(data)
