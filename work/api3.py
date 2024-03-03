import requests

api_key = ""
domain_name = "www.google.com"  # Example IP address

url = f"https://api.ip2whois.com/v2?key={api_key}&domain={domain_name}"


response = requests.get(url)
response.raise_for_status()  # Raise an exception for HTTP errors
data = response.json()
print(data)
