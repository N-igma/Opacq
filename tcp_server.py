from socket import *
import threading

def recvall(sock):
  BUFF_SIZE = 4096
  data = b''
  while True:
    part = sock.recv(BUFF_SIZE)
    print(part)
    data += part
    if len(part) < BUFF_SIZE:
      # either 0 or end of data
      break
  return data

# Create a new thread class for receiving new connections
class ServerThread(threading.Thread):
  def __init__(self, host, port, onconn, onmessage):
    threading.Thread.__init__(self)
    self.host = host
    self.port = port
    self.onconn = onconn
    self.onmessage = onmessage

  def run(self):
    while True:
      cs = socket(AF_INET, SOCK_STREAM)
      cs.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
      cs.bind((self.host, self.port))
      cs.listen(1)
      conn, address = cs.accept()
      with conn:
        self.onconn(conn, address[0])
        buff = recvall(conn)
        if not buff:
          return
        message = buff.decode('utf-8')
        self.onmessage(conn, message)
        conn.sendall(f"{message}".encode('utf-8'))

def start_server(onconn, onmessage):
  server = ServerThread(host='0.0.0.0', port=9375, onconn=onconn, onmessage=onmessage)
  server.start()

if __name__ == '__main__':
  import time

  def onserverconn(conn, addr):
    print('Server Conn Received', addr)
    #while True:
    #  conn.send(input().encode('utf-8'))
  def onservermsg(conn, msg):
    print('Server Message Received', msg)
  start_server(onconn=onserverconn, onmessage=onservermsg)
