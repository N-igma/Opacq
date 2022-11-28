# Integration: Jerome
import os
import socket
import hashlib
from tcp import start_client, start_server, broadcast_existence, listen_for_broadcasts

send_to = {}

def merge_sender_entropy(sender, entropy):
  return (hashlib.sha256((f"{sender}+{entropy}").encode('utf-8')).hexdigest())[0:6]

entropy = os.urandom(4)
who_am_i = socket.gethostbyname(socket.getfqdn())
my_fingerprint = merge_sender_entropy(who_am_i, entropy)
sender_fingerprints = {}

#sender_fingerprints[who_am_i] = my_fingerprint
known_fingerprints = []

print(sender_fingerprints)

def onconn(conn, addr):
  print(addr)
  send_to[sender_fingerprints[addr]] = lambda s: conn.sendall(s.encode('utf8'))
def onmsg(conn, msg):
  print('Message Received', msg)

def on_broadcast(content, sender):
  current_fingerprint = merge_sender_entropy(sender[0], content)
  if not current_fingerprint in known_fingerprints:
    known_fingerprints.append(current_fingerprint)
    sender_fingerprints[sender[0]] = current_fingerprint
    print(sender_fingerprints)

    if int(current_fingerprint, 16) < int(my_fingerprint, 16):
      start_client(sender[0], onconn, onmsg)

listen_for_broadcasts(on_broadcast)

start_server(onconn, onmsg)
broadcast_existence(entropy)

while True:
  command = input()
  dest, *contents = command.split('<=')
  send_to[dest]('<='.join(contents))
