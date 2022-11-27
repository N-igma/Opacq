# Integration: Jerome
import os
import socket
import hashlib
from tcp import start_client, start_server, broadcast_existence, listen_for_broadcasts

def merge_sender_entropy(sender, entropy):
  return hashlib.sha256((f"{sender}+{entropy}").encode('utf-8')).hexdigest()

entropy = os.urandom(4)
who_am_i = socket.gethostbyname(socket.getfqdn())
my_fingerprint = merge_sender_entropy(who_am_i, entropy)
sender_fingerprints = {}

sender_fingerprints[who_am_i] = my_fingerprint
known_fingerprints = [my_fingerprint]

print(sender_fingerprints)

def on_broadcast(content, sender):
  current_fingerprint = merge_sender_entropy(sender[0], content)
  if not current_fingerprint in known_fingerprints:
    known_fingerprints.append(current_fingerprint)
    sender_fingerprints[sender[0]] = current_fingerprint
    print(sender_fingerprints)

    def onclientconn(conn):
      print('Client Conn Received')
    def onclientmsg(conn, msg):
      print('Client Message Received', msg)
    start_client(sender[0], onclientconn, onclientmsg)

listen_for_broadcasts(on_broadcast)

def onserverconn(conn):
  print('Server Conn Received')
  conn.sendall(b'Hello world!')
def onservermsg(conn, msg):
  print('Server Message Received', msg)
start_server(onconn=onserverconn, onmessage=onservermsg)
broadcast_existence(entropy)
