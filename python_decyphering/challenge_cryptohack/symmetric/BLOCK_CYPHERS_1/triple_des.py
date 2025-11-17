import requests

url_base = 'http://aes.cryptohack.org/triple_des'

# DES3 splits the provided key into 2 or 3 sub-keys used for encryption rounds
# (depending on whether the provided key is 16 or 24 bytes in length). Unfortunately,
# Wikipedia lists some weak keys for single DES:
#
#   https://en.wikipedia.org/wiki/Weak_key#Weak_keys_in_DES
#
# for which encrypting twice yields the plaintext -- E_k(E_k(P)) = P.
# We can construct a weak key for triple DES by concatenating two distinct
# weak keys from single DES, needed to bypass PyCryptodome's check that
# ensures that triple DES does not degenerate into single DES.
weak_key = '0101010101010101FEFEFEFEFEFEFEFE'

def hack():
  response = requests.get(url="%s/encrypt_flag/%s" % (url_base, weak_key)).json()
  ciphertext = response['ciphertext']
  
  response = requests.get(url="%s/encrypt/%s/%s" % (url_base, weak_key, ciphertext)).json()
  plaintext = bytes.fromhex(response['ciphertext']).decode()
  return plaintext

if __name__ == '__main__':
  flag = hack()
  print(flag)