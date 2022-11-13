# Encryption + Decryption: Alienor

import rsa
import base64

def gen_cles():
  (cle_pub, cle_pri) = rsa.newkeys(1024)
  return (cle_pub, cle_pri)

def encryption(message, cle_pub):
  message = message.encode('utf8')
  encrypt = rsa.encrypt(message, cle_pub)
  return base64.b64encode(encrypt).decode('utf8')

def decryption(encrypt, cle_pri):
  encrypt = (base64.b64decode(encrypt))
  message = rsa.decrypt(encrypt, cle_pri)
  return message.decode('utf8')

if __name__ == '__main__':
  (cle_pub, cle_pri) = gen_cles()
  print(encryption(input(), cle_pub))
  print(decryption(input(), cle_pri))