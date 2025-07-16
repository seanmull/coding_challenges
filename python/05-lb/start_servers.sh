#!/bin/bash
python -m http.server 8081 --directory server_1 &
python -m http.server 8082 --directory server_2 &
python -m http.server 8083 --directory server_3 &

