#!/bin/bash
# curl -X POST http://localhost:6380 -H "Content-Type: application/json" -d '{"command" : "*3\r\n$3\r\nset\r\n$5\r\nhello\r\n$5\r\nworld\r\n"}'
curl -X POST http://localhost:6380 -H "Content-Type: application/json" -d '{"command" : "*2\r\n$3\r\nget\r\n$5\r\nhello\r\n"}'
