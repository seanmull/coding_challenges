import socket
import struct

# Constants
QTYPE_A = 1    # IPv4 address
QCLASS_IN = 1  # Internet

# Helper function to encode domain name
def encode_domain_name(domain):
    parts = domain.split('.')
    encoded = b''.join(struct.pack('!B', len(part)) + part.encode() for part in parts)
    return encoded + b'\x00'

# Header section for a DNS query
def create_dns_header():
    ID = 1234                # Identifier
    FLAGS = 0x0100           # Standard query, recursion desired
    QDCOUNT = 1              # Number of questions
    ANCOUNT = 0              # Number of answers
    NSCOUNT = 0              # Number of authority records
    ARCOUNT = 0              # Number of additional records
    return struct.pack('!HHHHHH', ID, FLAGS, QDCOUNT, ANCOUNT, NSCOUNT, ARCOUNT)

# Question section
def create_dns_question(domain):
    QNAME = encode_domain_name(domain)
    QTYPE = QTYPE_A
    QCLASS = QCLASS_IN
    return QNAME + struct.pack('!HH', QTYPE, QCLASS)

# Build the DNS query message
def build_dns_query(domain):
    header = create_dns_header()
    question = create_dns_question(domain)
    return header + question

# Send DNS query and receive response
def send_dns_query(domain):
    # DNS server address
    server_address = ('8.8.8.8', 53)
    
    # Build DNS query
    dns_query = build_dns_query(domain)
    
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        # Send the DNS query
        sock.sendto(dns_query, server_address)
        
        # Receive the response
        data, _ = sock.recvfrom(512)  # 512 bytes is the typical max size for DNS UDP packets
        
        return data
    finally:
        sock.close()

# Print the raw response in hexadecimal format
def print_response(response):
    print(response.hex())

# Example usage
domain = 'google.com'
response = send_dns_query(domain)
print_response(response)

