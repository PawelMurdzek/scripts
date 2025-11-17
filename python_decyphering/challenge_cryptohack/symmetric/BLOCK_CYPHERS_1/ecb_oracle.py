import requests
import json

BASE_URL = 'http://aes.cryptohack.org/ecb_oracle/encrypt/'
ALPHABET = 'abcdefghijklmnopqrstuvwxyz0123456789_{}'


def ascii_to_hex(string: str) -> str:
    return ''.join([hex(ord(c))[2:] for c in string])


def get_letter(block, depth=1):
    block = block[-31:]
    trail = block[:32 - depth]

    for letter in ALPHABET:
        plaintext = ascii_to_hex(block + letter + trail)

        response = requests.get(BASE_URL + plaintext)
        ciphertext = json.loads(response.text)['ciphertext']

        if ciphertext[32:64] == ciphertext[96:128]:
            current_flag = block + letter
            print(current_flag)
            if letter != '}':
                return get_letter(current_flag, depth + 1)
            else:
                return current_flag.lstrip('-')

    return block.lstrip('-')


flag = get_letter('-' * 32)
print("The flag is: " + flag)