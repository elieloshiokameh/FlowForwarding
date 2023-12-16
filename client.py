import socket
import sys
import threading
from packet import Packet, PACKET_TYPES
from network_utils import generate_address, get_active_interfaces

SERVER_PORT = 50000
BROADCAST_ADDRESS = '255.255.255.255'

def listen_for_messages(client_socket, client_address, ack_event):
    while True:
        try:
            message, _ = client_socket.recvfrom(1024)
            packet = Packet.parse(message)

            if packet.packet_type == PACKET_TYPES['CLIENT_RECEIVED_ACK'] and packet.identifier == client_address:
                print(f"Received ACK for message sent.")
                ack_event.set()  # Signal that ACK has been received

            elif packet.identifier != client_address:
                print(f"Received message from {packet.identifier}: {packet.message}")

        except Exception as e:
            print(f"Error receiving message: {e}")

def main():
    client_address = generate_address()
    ack_event = threading.Event()  # Event object for ACK handling
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Send initial contact message
    initial_contact_packet = Packet(PACKET_TYPES['INITIAL_CONTACT'], client_address, "").to_bytes()
    client_socket.sendto(initial_contact_packet, (BROADCAST_ADDRESS, SERVER_PORT))
    print(f"Client with address {client_address} started and sent initial contact.")

    # Start listening thread
    listener_thread = threading.Thread(target=listen_for_messages, args=(client_socket, client_address, ack_event))
    listener_thread.daemon = True
    listener_thread.start()

    try:
        while True:
            ack_event.clear()  # Reset ACK event
            dest_id = input("Enter the destination client identifier: ")
            if len(dest_id) != 7:
                print("Invalid identifier format. Please try again.")
                continue
            message = input("Enter your message: ")
            message_packet = Packet(PACKET_TYPES['FORWARD'], dest_id, message).to_bytes()
            client_socket.sendto(message_packet, (BROADCAST_ADDRESS, SERVER_PORT))

            ack_event.wait(timeout=5)  # Wait for ACK for 5 seconds
            if ack_event.is_set():
                print(f"Sent message to {dest_id}: {message}")
            else:
                print("No ACK received. Message may not have been delivered.")

    except KeyboardInterrupt:
        print("\nClient exiting.")
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
