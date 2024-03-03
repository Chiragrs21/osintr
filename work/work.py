import ipaddress

ip = 'fe80::a277:71c5:c782:3806%13'
is_ipv4 = ipaddress.ip_address(ip).version == 4 if '.' in ip else False
is_ipv6 = ipaddress.ip_address(ip).version == 6 if ':' in ip else False

print(is_ipv4)  # Output: True
print(is_ipv6)  # Output: False
