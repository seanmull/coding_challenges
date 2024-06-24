import pytest
import struct
from DNS_resolver import decode_domain_name, parse_dns_response


def test_decode_domain_name_simple():
    message = b"\x03www\x06google\x03com\x00"
    domain, offset = decode_domain_name(message, 0)
    assert domain == "www.google.com"
    assert offset == len(message)


def test_decode_domain_name_with_pointer():
    message = b"\x03www\x06google\x03com\x00" + b"\xC0\x00"
    buffer_size = len(message) + 1  # Ensure buffer size is larger than the offset
    domain, offset = decode_domain_name(message, 12)
    assert domain == "www.google.com"


def test_parse_dns_response_A_record():
    response = (
        b"\x12\x34\x81\x80\x00\x01\x00\x01\x00\x00\x00\x00"  # Header
        b"\x03www\x06google\x03com\x00\x00\x01\x00\x01"  # Question
        b"\xc0\x0c\x00\x01\x00\x01\x00\x00\x00\x3c\x00\x04"  # Answer RDATA
        b"\xd8\x3a\xd3\x8e"  # Answer IP (216.58.211.142)
    )
    expected_output = (
        "DNS Response:\n  ID: 4660\n  Flags: 33152\n  QDCOUNT: 1\n  ANCOUNT: 1\n  NSCOUNT: 0\n  ARCOUNT: 0\n"
        "  QNAME: www.google.com\n  QTYPE: 1\n  QCLASS: 1\n"
        "  Answers:\n    Type: A (Address)\n    IP: 216.58.211.142\n"
    )
    parse_dns_response(response)


def test_parse_dns_response_NS_record():
    response = (
        b"\x12\x34\x81\x80\x00\x01\x00\x01\x00\x00\x00\x00"  # Header
        b"\x06google\x03com\x00\x00\x02\x00\x01"  # Question
        b"\xc0\x0c\x00\x02\x00\x01\x00\x00\x51\xe4\x00\x06"  # Answer RDATA
        b"\x03ns1\xc0\x0c"  # NS Record (ns1.google.com)
    )
    expected_output = (
        "DNS Response:\n  ID: 4660\n  Flags: 33152\n  QDCOUNT: 1\n  ANCOUNT: 1\n  NSCOUNT: 0\n  ARCOUNT: 0\n"
        "  QNAME: google.com\n  QTYPE: 2\n  QCLASS: 1\n"
        "  Answers:\n    Type: NS (Name Server)\n    NS: ns1.google.com\n"
    )
    parse_dns_response(response)


if __name__ == "__main__":
    pytest.main()
