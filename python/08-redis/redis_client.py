import requests
import utils
import json

while True:
    commands = input("127.0.0.1:6380> ")

    serialized_commands = utils.serialize_commands(commands)

    headers = {"Content-Type": "application/json"}

    r = requests.post('http://localhost:6380',
                      data=json.dumps({'commands': serialized_commands}),
                      headers=headers)
    sr = utils.sanitize_response(r.json())
    print(sr)
