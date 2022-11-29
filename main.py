# Integration: Jerome
import os
import sys
import socket
import hashlib
import json
import random
import base64
import rsa
from tcp import start_client, start_server, broadcast_existence, listen_for_broadcasts
from generator import pick_emoji_name_set_seed
from enc_dec import gen_cles, encryption, sign, verif, decryption

send_to = {}
keypairs = {}

def merge_sender_entropy(sender, entropy):
  return (hashlib.sha256((f"{sender}+{entropy}").encode('utf-8')).hexdigest())[0:6]

entropy = os.urandom(4)
who_am_i = socket.gethostbyname(socket.getfqdn())
my_fingerprint = merge_sender_entropy(who_am_i, entropy)
sender_fingerprints = {}

#sender_fingerprints[who_am_i] = my_fingerprint
known_fingerprints = []

def on_broadcast(content, sender):
  current_fingerprint = merge_sender_entropy(sender[0], content)
  if not current_fingerprint in known_fingerprints:
    known_fingerprints.append(current_fingerprint)
    sender_fingerprints[sender[0]] = current_fingerprint
    (pfp, name) = pick_emoji_name_set_seed(random, current_fingerprint)
    print(json.dumps({
      "type": "NEW_MEMBER",
      "id": current_fingerprint,
      "pfp": pfp,
      "name": name,
      "me": my_fingerprint == current_fingerprint
    }))
    sys.stdout.flush()

    def create_socket(addr, data):
      def send_data(conn, addr):
        conn.sendall(data.encode('utf8'))
      start_client(addr, send_data)
    send_to[sender_fingerprints[sender[0]]] = lambda x:create_socket(sender[0], x)

    (cle_pub_a_moi, cle_priv_a_moi) = gen_cles() # cle_pub, cle_pri

    create_socket(sender[0], json.dumps({
      "type": "KEYS",
      "pubkey": base64.b64encode(cle_pub_a_moi.save_pkcs1('DER')).decode('ascii')
    }))

    if not current_fingerprint in keypairs:
      keypairs[current_fingerprint] = [None, None]
    keypairs[current_fingerprint][1] = cle_priv_a_moi

listen_for_broadcasts(on_broadcast)

def onserverconn(conn, addr):
  return
def onservermsg(conn, addr, msg):
  command = json.loads(msg)
  match command["type"]:
    case 'KEYS':
      current_fingerprint = sender_fingerprints[addr]
      if not current_fingerprint in keypairs:
        keypairs[current_fingerprint] = [None, None]
      keypairs[current_fingerprint][0] = rsa.PublicKey.load_pkcs1(base64.b64decode(command["pubkey"]), 'DER')
    case 'MESSAGE':
      signature = base64.b64decode(command["signature"])
      content_encrypted = base64.b64decode(command["content"])
      if verif(content_encrypted, signature, keypairs[sender_fingerprints[addr]][0]) == "SHA-256":
        content = decryption(content_encrypted, keypairs[sender_fingerprints[addr]][1])
        print(json.dumps({
          "type": "NEW_MESSAGE",
          "content": content
        }))
        sys.stdout.flush()

start_server(onserverconn, onservermsg)
broadcast_existence(entropy)

while True:
  command = json.loads(input())
  match command["type"]:
    case 'SEND_MESSAGE':
      content = command["content"]
      content_encrypted = encryption(content, keypairs[command["to"]][0])
      content_signature = sign(content_encrypted, keypairs[command["to"]][1])

      send_to[command["to"]](json.dumps({
        "type": "MESSAGE",
        "content": base64.b64encode(content_encrypted).decode('ascii'),
        "signature": base64.b64encode(content_signature).decode('ascii')
      }))
