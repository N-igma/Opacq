from tcp_broadcast import broadcast_existence, listen_for_broadcasts
from tcp_client import start_client
from tcp_server import start_server

if __name__ == '__main__':
  import time
  import socket
  import hashlib

  def four_bytes_time(offset=0):
    return int(time.time() // 5 + offset).to_bytes(4, 'big')

  def merge_sender_dob(sender, dob):
    return hashlib.sha256((f"{sender}+{dob}").encode('utf-8')).hexdigest()

  date_of_birth = four_bytes_time()
  who_am_i = socket.gethostbyname(socket.getfqdn())
  my_fingerprint = merge_sender_dob(who_am_i, date_of_birth)
  sender_fingerprints = {}
  sender_fingerprints[who_am_i] = my_fingerprint

  known_fingerprints = []
  known_fingerprints.append(my_fingerprint)

  print(sender_fingerprints)

  def on_broadcast(content, sender):
    current_fingerprint = merge_sender_dob(sender[0], content)
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
  broadcast_existence(date_of_birth)
