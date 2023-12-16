import time

class RoutingTable:
    def __init__(self, router_address, interfaces):
        self.router_address = router_address
        self.interfaces = interfaces
        self.table = {}

    def update_route(self, identifier, next_hop_ip):
        self.table[identifier] = (next_hop_ip, time.time())

    def get_next_hop(self, identifier):
        if identifier in self.table:
            next_hop, timestamp = self.table[identifier]
            if time.time() - timestamp < 30:  # 30 seconds timeout
                return next_hop
        return None

    def remove_stale_routes(self):
        current_time = time.time()
        stale_keys = [key for key, (_, timestamp) in self.table.items() if current_time - timestamp >= 30]
        for key in stale_keys:
            del self.table[key]

    def is_route_known(self, identifier):
        return identifier in self.table
    
    def print_table(self):
        print(f"Current Routing Table for Router {self.router_address}:")
        for identifier, (next_hop, timestamp) in self.table.items():
            time_elapsed = time.time() - timestamp
            print(f"Identifier: {identifier.decode()}, Next Hop: {next_hop}, Last Updated: {time_elapsed:.2f} seconds ago")
