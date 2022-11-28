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
  def __init__(self, host, port, onconn):
    threading.Thread.__init__(self)
    self.host = host
    self.port = port
    self.onconn = onconn

  def run(self):
    with socket(AF_INET, SOCK_STREAM) as s:
      # s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
      s.connect((self.host, self.port))
      self.onconn(s, self.host)
      # buff = recvall(s)
      #message = buff.decode('utf-8')
      #threading.Thread(target=lambda:self.onmessage(s, message)).start()
      # s.shutdown(SHUT_RDWR)
      #s.close()

def start_client(host, onconn):
  client = ClientThread(host=host, port=9375, onconn=onconn)
  client.start()

if __name__ == '__main__':
  def onclientconn(conn, addr):
    print('Client Conn Received', addr)
    conn.send(b'Hi!')
    print(conn.recv(1024))
    #while True:
    #  conn.send(input().encode('utf-8'))
  start_client('127.0.0.1', onclientconn)
