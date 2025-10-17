from pwn import *  # pip install pwntools
import json
import base64
import codecs

r = remote('socket.cryptohack.org', 13377, level='debug')

def json_recv():
    line = r.recvline()
    return json.loads(line.decode())

def json_send(hsh):
    request = json.dumps(hsh).encode()
    r.sendline(request)

def decode_message(data_type, encoded_value):
    if data_type == "base64":
        # Decode Base64
        return base64.b64decode(encoded_value).decode('utf-8')
    elif data_type == "hex":
        # Decode Hex
        return bytes.fromhex(encoded_value).decode('utf-8')
    elif data_type == "rot13":
        # Decode ROT13
        return codecs.decode(encoded_value, 'rot_13')
    elif data_type == "bigint":
        # Decode Big Integer
        hex_value = encoded_value[2:]  # Remove the "0x" prefix
        return bytes.fromhex(hex_value).decode('utf-8')
    elif data_type == "utf-8":
        # Decode UTF-8 (just return the string as-is)
        return ''.join([chr(b) for b in encoded_value])
    else:
        raise ValueError(f"Unknown encoding type: {data_type}")

# Start receiving and decoding messages
while True:
    received = json_recv()
    print("Received:", received)

    data_type = received["type"]
    encoded_value = received["encoded"]

    try:
        decoded_value = decode_message(data_type, encoded_value)
        print("Decoded value:", decoded_value)

        to_send = {
            "decoded": decoded_value
        }
        json_send(to_send)
    except Exception as e:
        print("Error:", e)
        break