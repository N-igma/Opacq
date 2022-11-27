import socket
import threading

def recvall(sock):
  BUFF_SIZE = 32
  data = b''
  while True:
    part = sock.recv(BUFF_SIZE)
    print(part)
    data += part
    if len(part) < BUFF_SIZE:
      # either 0 or end of data
      break
  return data

class ClientThread(threading.Thread):
  def __init__(self, host, port, onconn, onmessage):
    threading.Thread.__init__(self)
    self.host = host
    self.port = port
    self.onconn = onconn
    self.onmessage = onmessage

  def run(self):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      s.connect((self.host, self.port))
      self.onconn(s)
      while True:
        self.onmessage(recvall(s))

def start_client(host, onconn, onmessage):
  client = ClientThread(host=host, port=9375, onconn=onconn, onmessage=onmessage)
  client.start()
