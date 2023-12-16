import netifaces
import random

def generate_address():
    # Generate a random 7-character hexadecimal address.
    return ''.join(random.choices('0123456789ABCDEF', k=7))

def get_active_interfaces():
    # Get active network interfaces and their IP addresses.
    active_interfaces = {}
    for interface in netifaces.interfaces():
        addrs = netifaces.ifaddresses(interface).get(netifaces.AF_INET)
        if addrs:
            ip_info = addrs[0]
            active_interfaces[interface] = ip_info.get('addr')
    return active_interfaces
