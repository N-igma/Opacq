# Encryption + Decryption: Alienor

import rsa

# TODO
# 0. retourner des bytes
# 1. Fixer le bug des messages trop longs
# 2. Truc d'alex (Signature / Verification)

def gen_cles():
  (cle_pub, cle_pri) = rsa.newkeys(1024)
  return (cle_pub, cle_pri)

def encryption(message, cle_pub):
  message = message.encode('utf8')
  encrypt = rsa.encrypt(message, cle_pub)
  return encrypt

def decryption(encrypt, cle_pri):
  message = rsa.decrypt(encrypt, cle_pri)
  return message.decode('utf8')

if __name__ == '__main__':
  (cle_pub, cle_pri) = gen_cles()
  print(encryption(input(), cle_pub))
  print(decryption(input(), cle_pri))
