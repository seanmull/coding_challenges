import socket
import struct

# Constants
QTYPE_A = 1    # IPv4 address
QCLASS_IN = 1  # Internet

# Encode domain name
def encode_domain_name(domain):
    labels = domain.split('.')
    encoded_labels = []
    for label in labels:
        length = len(label)
        encoded_labels.append(struct.pack('!B', length) + label.encode())
    return b''.join(encoded_labels) + b'\x00'

# Build DNS query message
def build_dns_query(domain, qtype=QTYPE_A, qclass=QCLASS_IN):
    ID = 1234  # Transaction ID
    FLAGS = 0x0100  # Standard query
    QDCOUNT = 1  # Number of questions
    
    qname = encode_domain_name(domain)
    qtype_bytes = struct.pack('!H', qtype)
    qclass_bytes = struct.pack('!H', qclass)
    
    header = struct.pack('!HHHHHH', ID, FLAGS, QDCOUNT, 0, 0, 0)
    question = qname + qtype_bytes + qclass_bytes
    
    return header + question

# Decode domain name
def decode_domain_name(data, offset):
    labels = []
    while offset < len(data):
        length = data[offset]
        if length == 0:
            offset += 1
            break
        if length >= 192:
            pointer = struct.unpack('!H', data[offset:offset + 2])[0] & 0x3FFF
            label, _ = decode_domain_name(data, pointer)
            labels.append(label)
            offset += 2
            break
        else:
            offset += 1
            label = ''
            for _ in range(length):
                if offset < len(data):
                    label += chr(data[offset])
                    offset += 1
                else:
                    break
            labels.append(label)
    return '.'.join(labels), offset

# Parse DNS query message
def parse_dns_query(query):
    ID, FLAGS, QDCOUNT, _, _, _ = struct.unpack('!HHHHHH', query[:12])
    
    qname, offset = decode_domain_name(query, 12)
    qtype, qclass = struct.unpack('!HH', query[offset:offset + 4])
    
    return ID, FLAGS, QDCOUNT, qname, qtype, qclass

# Print DNS query in human-readable format
def print_parsed_dns_query(query):
    ID, FLAGS, QDCOUNT, qname, qtype, qclass = parse_dns_query(query)
    
    print("DNS Query:")
    print(f"  ID: {ID}")
    print(f"  Flags: {FLAGS}")
    print(f"  QDCOUNT: {QDCOUNT}")
    print(f"  QNAME: {qname}")
    print(f"  QTYPE: {qtype}")
    print(f"  QCLASS: {qclass}")

# Parse DNS response message
def parse_dns_response(response):
    try:
        if len(response) < 12:
            print("Error parsing DNS response: Response is too short.")
            return None
        
        ID, FLAGS, QDCOUNT, ANCOUNT, NSCOUNT, ARCOUNT = struct.unpack('!HHHHHH', response[:12])
        print(f"Header - ID: {ID}, FLAGS: {FLAGS}, QDCOUNT: {QDCOUNT}, ANCOUNT: {ANCOUNT}, NSCOUNT: {NSCOUNT}, ARCOUNT: {ARCOUNT}")
        
        offset = 12
        qname, offset = decode_domain_name(response, offset)
        print(f"Question - QNAME: {qname}")
        if offset + 4 > len(response):
            print("Error parsing DNS response: Question section is incomplete.")
            return None
        
        qtype, qclass = struct.unpack('!HH', response[offset:offset + 4])
        offset += 4
        
        answers = []
        for _ in range(ANCOUNT):
            print(f"Parsing answer at offset {offset}")
            if offset + 10 > len(response):
                print("Error parsing DNS response: Incomplete answer section.")
                return None
            name, offset = decode_domain_name(response, offset)
            print(f"Answer name: {name}, next offset: {offset}")
            if offset + 10 > len(response):
                print("Error parsing DNS response: Incomplete answer section.")
                return None
            
            atype, aclass, ttl, rdlength = struct.unpack('!HHIH', response[offset:offset + 10])
            print(f"Answer header - TYPE: {atype}, CLASS: {aclass}, TTL: {ttl}, RDLENGTH: {rdlength}")
            offset += 10
            if offset + rdlength > len(response):
                print("Error parsing DNS response: Incomplete answer data.")
                return None
            
            if atype == QTYPE_A:
                address = '.'.join(str(byte) for byte in response[offset:offset + rdlength])
                answers.append((atype, aclass, ttl, address))
            else:
                data = response[offset:offset + rdlength]
                answers.append((atype, aclass, ttl, data))
            offset += rdlength
        
        return ID, FLAGS, QDCOUNT, ANCOUNT, NSCOUNT, ARCOUNT, qname, qtype, qclass, answers
    
    except struct.error as e:
        print(f"Error parsing DNS response: {e}")
        return None

# Print DNS response in human-readable format
def print_parsed_dns_response(response):
    parsed_response = parse_dns_response(response)
    if parsed_response is not None:
        ID, FLAGS, QDCOUNT, ANCOUNT, NSCOUNT, ARCOUNT, qname, qtype, qclass, answers = parsed_response
        
        print("DNS Response:")
        print(f"  ID: {ID}")
        print(f"  Flags: {FLAGS}")
        print(f"  QDCOUNT: {QDCOUNT}")
        print(f"  ANCOUNT: {ANCOUNT}")
        print(f"  NSCOUNT: {NSCOUNT}")
        print(f"  ARCOUNT: {ARCOUNT}")
        print(f"  QNAME: {qname}")
        print(f"  QTYPE: {qtype}")
        print(f"  QCLASS: {qclass}")
        print("  Answers:")
        for atype, aclass, ttl, data in answers:
            if atype == 256:  # Unknown record type
                print("    Type: Unknown (256)")
                print(f"    Data: {data}")
            else:
                print(f"    Type: {atype}")
                print(f"    Class: {aclass}")
                print(f"    TTL: {ttl}")
                print(f"    Data: {data}")
    else:
        print("Error parsing DNS response. Unable to print parsed response.")

# Print bytes in hexadecimal format
def print_hex_bytes(data):
    hex_data = ' '.join(f'{byte:02x}' for byte in data)
    print(hex_data)

# Send DNS query and receive response
def send_dns_query(domain, dns_server='8.8.8.8', dns_port=53):
    query_message = build_dns_query(domain)
    
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(query_message, (dns_server, dns_port))
        print("DNS Query Sent:")
        print_hex_bytes(query_message)
        
        response, _ = sock.recvfrom(4096)
        print("\nDNS Response Received:")
        print_hex_bytes(response)
        
        return response

# Example usage
response = send_dns_query("dns.google.com")
print_parsed_dns_response(response)

