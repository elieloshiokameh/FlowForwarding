# header.py
SERVER_PORT = 50000
BROADCAST_SUFFIX = '.255'

IDENTIFIERS = {
    b'client1': '192.168.0',     # Part of stub1 network
    b'client2': '192.168.10',    # Part of stub2 network
    b'client3': '192.168.20',    # Part of stub3 network
    b'client4': '192.168.30',    # Part of stub4 network
    b'router1': ['192.168.0.0/24', '172.21.0.0/24'],    # Connected to stub1 and trans1 networks
    b'router2': ['172.21.0.0/24', '172.22.0.0/24', '192.168.20.0/24'],  # Connected to trans1, trans2, and stub3 networks
    b'router3': ['192.168.10.0/24', '172.22.0.0/24', '192.168.30.0/24', '172.23.0.0/24'], # Connected to stub2, trans2, stub4, and trans3 networks
}
