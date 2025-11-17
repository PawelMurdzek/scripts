import requests
from functools import reduce
from pwn import xor


print(
    requests.get(
        "http://aes.cryptohack.org/flipping_cookie/check_admin/"
        + (
            cookie := bytes.fromhex(
                requests.get(
                    "http://aes.cryptohack.org/flipping_cookie/get_cookie"
                ).json()["cookie"]
            )
        )[16:].hex()
        + "/"
        + reduce(xor, [cookie[:16], b"admin=False;expi", b"admin=True;;expi"]).hex()
    ).json()["flag"]
)