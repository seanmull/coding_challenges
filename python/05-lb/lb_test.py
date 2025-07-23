import requests
import re
from concurrent.futures import ThreadPoolExecutor

lb_port = 8080
backend_ports = [8081, 8082, 8083]
lb_url = 'localhost:8080'
lb_request = requests.get(f'http://{lb_url}')
server_number_returned = int(
    re.search(r'(\d+)!', lb_request.text).group()[:-1])
backend_requests = [requests.get(
    f'http://localhost:{port}') for port in backend_ports]
permissable_payloads = set(
    [f'<html><body><h1>Hello from server {num}!</h1></body></html>\n' for num in [1, 2, 3]])
extra_lb_request = [requests.get(
    'http://localhost:8080').text for _ in range(10)]
sequence = []
for _ in range(10):
    server_number_returned += 1
    server_number_returned %= len(backend_ports) + 1
    if server_number_returned == 0:
        server_number_returned += 1
    sequence.append(server_number_returned)
expected_round_robin_responses = [
    f'<html><body><h1>Hello from server {num}!</h1></body></html>\n' for num in sequence]


def test_lb_connection_reachability():
    assert lb_request.status_code == 200


def test_lb_payload():
    assert lb_request.text in permissable_payloads


def test_server1_payload():
    assert (backend_requests[0].text ==
            '<html><body><h1>Hello from server 1!</h1></body></html>\n')


def test_server2_payload():
    assert (backend_requests[1].text ==
            '<html><body><h1>Hello from server 2!</h1></body></html>\n')


def test_server3_payload():
    assert (backend_requests[2].text ==
            '<html><body><h1>Hello from server 3!</h1></body></html>\n')


def test_round_robin():
    assert (str(extra_lb_request) == str(expected_round_robin_responses))


def test_concurrent_requests():
    with requests.Session() as session:
        def test_get_lb_response(_):
            return session.get(f'http://{lb_url}')

        with ThreadPoolExecutor() as executor:
            results = executor.map(test_get_lb_response, list(range(10)))
        status_codes = [result.status_code for result in list(results)]
        all_types_status_codes = set(status_codes)
        assert (200 in all_types_status_codes and len(all_types_status_codes) == 1)
