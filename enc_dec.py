# Encryption + Decryption: Alienor

import rsa
import base64

key_length = 1024
# la valeur de key_length est une puissance de 2
# la taille du message ne doit pas excéder key_length/8 - 11 bits

# Taille max d'encryption: n/8 - 11
# Taille de chaque encryption: n/8

def gen_cles():
  (cle_pub, cle_pri) = rsa.newkeys(key_length)
  return (cle_pub, cle_pri)

def taille(encrypt, chunk_size):
  result = []
  for i in range(0, len(encrypt), chunk_size):
    result.append(encrypt[i:i+chunk_size])
  return result

def encryption(message, cle_pub):
  message = message.encode('utf8')
  encrypted = []
  for chunk in taille(message, key_length // 8 - 11):
    encrypted.append(rsa.encrypt(chunk, cle_pub))
  return b''.join(encrypted)

def sign(message,cle_pri):
  signature = rsa.sign(message, cle_pri, 'SHA-256')
  signmess = signature
  return signmess

def decryption(encrypt, cle_pri):
  decrypted = []
  for chunk in taille(encrypt, key_length // 8):
    decrypted.append(rsa.decrypt(chunk, cle_pri))
  return b''.join(decrypted).decode('utf8')

def verif(message, signature, cle_pub):
  return rsa.verify(message, signature, cle_pub)

if __name__ == '__main__':
  (cle_pub, cle_pri) = gen_cles()
  message_original, signature_original = sign(base64.b64encode(encryption(input(), cle_pub)),cle_pri)
  print(message_original, base64.b64encode(signature_original).decode('ascii'))
  mess = input("message : ").encode('utf-8')
  signatur = base64.b64decode(input("signature : ").encode('ascii'))
  print(verif([mess,signatur], cle_pub))
  if verif([mess,signatur], cle_pub) == 'SHA-256':
      print(decryption(base64.b64decode(mess), cle_pri))
