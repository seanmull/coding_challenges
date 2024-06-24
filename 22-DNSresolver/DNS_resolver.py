import argparse
import socket
import struct

def build_query(domain, qtype):
    header = struct.pack('!HHHHHH', 1234, 256, 1, 0, 0, 0)  # Header
    question = b''.join((struct.pack('!B', len(label)) + label.encode() for label in domain.split('.'))) + b'\0'
    query_type = struct.pack('!H', qtype)
    query_class = struct.pack('!H', 1)
    return header + question + query_type + query_class

def decode_domain_name(message, offset):
    labels = []
    while True:
        length, = struct.unpack_from("!B", message, offset)
        if (length & 0xC0) == 0xC0:
            pointer, = struct.unpack_from("!H", message, offset)
            offset += 2
            return '.'.join(labels) + '.' + decode_domain_name(message, pointer & 0x3FFF)[0], offset
        if length == 0:
            offset += 1
            break
        offset += 1
        labels.append(message[offset:offset + length].decode())
        offset += length
    return '.'.join(labels), offset

def parse_dns_response(response):
    header = struct.unpack_from("!6H", response, 0)
    qdcount = header[2]
    ancount = header[3]
    nscount = header[4]
    arcount = header[5]

    print(f"DNS Response:\n  ID: {header[0]}\n  Flags: {header[1]}\n  QDCOUNT: {qdcount}\n  ANCOUNT: {ancount}\n  NSCOUNT: {nscount}\n  ARCOUNT: {arcount}")

    offset = 12
    for _ in range(qdcount):
        domain_name, offset = decode_domain_name(response, offset)
        qtype, qclass = struct.unpack_from("!HH", response, offset)
        offset += 4
        print(f"  QNAME: {domain_name}\n  QTYPE: {qtype}\n  QCLASS: {qclass}")

    print("  Answers:")
    for _ in range(ancount):
        domain_name, offset = decode_domain_name(response, offset)
        atype, aclass, ttl, rdlength = struct.unpack_from("!HHIH", response, offset)
        offset += 10
        if atype == 2:  # NS record
            ns_name, _ = decode_domain_name(response, offset)
            print(f"    Type: NS (Name Server)\n    NS: {ns_name}")
        offset += rdlength

def query_dns(domain, qtype):
    server = '8.8.8.8'
    port = 53

    query = build_query(domain, qtype)
    print(f"DNS Query (Hex):\n{query.hex()}\nDNS Query:\n  ID: {1234}\n  Flags: 256\n  QDCOUNT: 1\n  QNAME: {domain}\n  QTYPE: {qtype}\n  QCLASS: 1")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(5)
    sock.sendto(query, (server, port))
    response, _ = sock.recvfrom(512)
    print(f"DNS Response (Hex):\n{response.hex()}")

    parse_dns_response(response)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='DNS Query Script')
    parser.add_argument('domain', type=str, help='Domain to query')
    parser.add_argument('--qtype', type=str, default='A', help='Query type (A, NS, etc.)')

    args = parser.parse_args()

    qtype_mapping = {
        'A': 1,
        'NS': 2,
        'CNAME': 5,
        'MX': 15,
        'TXT': 16,
    }

    qtype = qtype_mapping.get(args.qtype.upper(), 1)
    query_dns(args.domain, qtype)

