from socket import *
import threading

def recvall(sock):
  BUFF_SIZE = 4096
  data = b''
  while True:
    part = sock.recv(BUFF_SIZE)
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
    with socket(AF_INET, SOCK_STREAM) as s:
      s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
      s.connect((self.host, self.port))
      self.onconn(s)
      while True:
        buff = recvall(s)
        message = buff.decode('utf-8')
        if message == '':
          break
        self.onmessage(s, message)
      s.close()

def start_client(host, onconn, onmessage):
  client = ClientThread(host=host, port=9375, onconn=onconn, onmessage=onmessage)
  client.start()

if __name__ == '__main__':
  def onclientconn(conn):
    print('Client Conn Received')
  def onclientmsg(conn, msg):
    print('Client Message Received', msg)
  start_client('127.0.0.1', onclientconn, onclientmsg)
