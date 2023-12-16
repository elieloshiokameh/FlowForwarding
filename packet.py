class Packet:
    def __init__(self, packet_type, identifier, message):
        if len(identifier) != 7:
            raise ValueError("Identifier must be 7 characters long")
        self.packet_type = packet_type
        self.identifier = identifier.encode()
        self.message = message.encode()

    def to_bytes(self):
        return self.packet_type.to_bytes(1, byteorder='big') + self.identifier + self.message

    @staticmethod
    def parse(packet_bytes):
        if len(packet_bytes) < 8:  # 1 byte for type + 7 bytes for identifier
            raise ValueError("Invalid packet format")
        packet_type = int.from_bytes(packet_bytes[:1], byteorder='big')
        identifier = packet_bytes[1:8]
        message = packet_bytes[8:]
        return Packet(packet_type, identifier.decode(), message.decode())

PACKET_TYPES = {
    'ROUTE_REQUEST' : 1,
    'INITIAL_CONTACT' : 2,
    'CLIENT_RECEIVED_ACK' : 3,
    'FORWARD' : 4
}