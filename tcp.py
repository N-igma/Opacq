from tcp_broadcast import broadcast_existence, listen_for_broadcasts
from tcp_client import start_client
from tcp_server import start_server

if __name__ == '__main__':
  import time
  import socket
  import hashlib

  date_of_birth = int(time.time() // 5).to_bytes(4, 'big')
  who_am_i = socket.gethostbyname(socket.getfqdn())
  sender_fingerprint = {}
  sender_fingerprint[who_am_i] = hashlib.sha256((f"{who_am_i}+{date_of_birth}").encode('utf-8')).hexdigest()

  print(sender_fingerprint)

  def on_broadcast(content, sender):
    print(content, sender[0])
    sender_fingerprint[sender[0]] = hashlib.sha256((f"{who_am_i}+{date_of_birth}").encode('utf-8')).hexdigest()
    print(sender_fingerprint)

  listen_for_broadcasts(on_broadcast)
  broadcast_existence(date_of_birth)
