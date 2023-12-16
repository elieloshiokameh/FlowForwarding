FROM ubuntu:latest

# Update package lists
RUN apt-get update

# Install Python, pip, and tcpdump
RUN apt-get install -y python3 python3-pip tcpdump

# Install netifaces using pip
RUN pip3 install netifaces

# Remove the existing pcap file, if any
RUN rm -f /pcap/capture.pcap

# ... other instructions ...
COPY . /compnets

# Set the command to run tcpdump
CMD ["tcpdump", "-i", "any", "-nn", "-vvv", "-w", "/pcap/capture.pcap"]
