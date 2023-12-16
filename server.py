import socket
import time
import sys
import threading
import logging
from packet import Packet, PACKET_TYPES
from routing_table import RoutingTable
from network_utils import generate_address, get_active_interfaces

SERVER_PORT = 50000

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

def print_routing_table_every_55_seconds(routing_table):
    while True:
        time.sleep(55)
        routing_table.print_table()

def broadcast_route_request(destination, router_socket, interfaces):
    packet = Packet(PACKET_TYPES['ROUTE_REQUEST'], b'0000000', destination)
    route_request_msg = packet.to_bytes()
    for iface, ip in interfaces.items():
        broadcast_addr = ip.rsplit('.', 1)[0] + '.255'  
        router_socket.sendto(route_request_msg, (broadcast_addr, SERVER_PORT))
        logger.info(f"Broadcasting on interface {iface} to {broadcast_addr}")

def handle_received_message(router_socket, routing_table, router_address):
    while True:
        try:
            message, address = router_socket.recvfrom(1024)
            packet = Packet.parse(message)

            identifier, content = packet.identifier.decode(), packet.message.decode()

            print(f"Router {router_address}: Received message from {identifier}: {content}")

            if packet.packet_type == PACKET_TYPES['INITIAL_CONTACT']:
                routing_table.update_route(packet.identifier, address[0])
                ack_msg = Packet(PACKET_TYPES['CLIENT_RECEIVED_ACK'], packet.identifier, "ACK").to_bytes()
                router_socket.sendto(ack_msg, address)
                logger.info(f"Received initial contact from {packet.identifier}. ACK sent.")

            elif packet.packet_type == PACKET_TYPES['ROUTE_REQUEST']:
                destination = packet.message
                if not routing_table.is_route_known(destination):
                    broadcast_route_request(destination, router_socket, routing_table.interfaces)
                    logger.info(f"Broadcasting route request for {destination}.")
                else:
                    next_hop = routing_table.get_next_hop(destination)
                    forward_message(next_hop, message, router_socket, router_address)
                    logger.info(f"Forwarding route request for {destination} to next hop.")

            # Add more packet types handling as needed

            # Remove stale routes periodically
            routing_table.remove_stale_routes()

        except Exception as e:
            logger.error(f"Router {router_address}: Error in message handling: {e}")

def forward_message(next_hop, message, router_socket, router_address):
    try:
        router_socket.sendto(message, (next_hop, SERVER_PORT))
        logger.info(f"Router {router_address}: Successfully forwarded message to next hop {next_hop}.")
    except Exception as e:
        logger.error(f"Router {router_address}: Failed to forward message: {e}")

def main(router_name):
    router_address = generate_address()
    interfaces = get_active_interfaces()

    routing_table = RoutingTable(router_address, interfaces)
    router_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    router_socket.bind(('', SERVER_PORT))
    router_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    logger.info(f"Router {router_name} with address {router_address} is up and running.")

    # Start the thread to print routing table periodically
    routing_table_thread = threading.Thread(target=print_routing_table_every_55_seconds, args=(routing_table,))
    routing_table_thread.daemon = True
    routing_table_thread.start()

    handle_received_message(router_socket, routing_table, router_address)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        logger.error("Usage: python server.py <router_name>")
        sys.exit(1)
    router_name = sys.argv[1]
    main(router_name)
