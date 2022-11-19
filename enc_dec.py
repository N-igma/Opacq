# Encryption + Decryption: Alienor

import rsa

key_length = 2048
# la valeur de newkeys est une puissance de 2
# la taille du message ne doit pas excéder key_length/8 - 11 bits

# TODO
# 0. retourner des bytes ''DONE''
# 1. Fixer le bug des messages trop longs
# 2. Truc d'alex (Signature / Verification)

def gen_cles():
  (cle_pub, cle_pri) = rsa.newkeys(key_length)
  return (cle_pub, cle_pri)

def encryption(message, cle_pub):
  message = message.encode('utf8')
  encrypt = rsa.encrypt(message, cle_pub)
  return encrypt

def taille(encrypt):
  chunk_size = key_length / 8 -11
  while len(encrypt) > chunk_size:
    chunks = [encrypt[i:i+chunk_size] for i in range(0, len(encrypt), chunk_size)]    


def decryption(encrypt, cle_pri):
  message = rsa.decrypt(encrypt, cle_pri)
  return message.decode('utf8')

if __name__ == '__main__':
  (cle_pub, cle_pri) = gen_cles()
  print(encryption(input(), cle_pub))
  print(decryption(input(), cle_pri))
