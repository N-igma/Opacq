from socket import *
import time
import threading

def recvall(sock):
  BUFF_SIZE = 32
  data = b''
  while True:
    part = sock.recv(BUFF_SIZE)
    data += part
    if len(part) < BUFF_SIZE:
      # either 0 or end of data
      break
  return data

class PingerThread (threading.Thread):
  def __init__(self, port, fingerprint):
    threading.Thread.__init__(self)
    self.port = port
    self.fingerprint = fingerprint

  def run (self):
    cs = socket(AF_INET, SOCK_DGRAM)
    cs.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    cs.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

    while True:
      time.sleep(0.5)
      cs.sendto(self.fingerprint, ('255.255.255.255', self.port))

def broadcast_existence(fingerprint):
  a = PingerThread(port=9375, fingerprint=fingerprint)
  a.daemon = True
  a.start()

class ListenerThread (threading.Thread):
  def __init__(self, port, onmessage):
    threading.Thread.__init__(self)
    self.port = port
    self.onmessage = onmessage

  def run (self):
    cs = socket(AF_INET, SOCK_DGRAM)
    try:
      cs.bind(('255.255.255.255', self.port))
    except:
      cs.close()

    while True:
      data, sender = cs.recvfrom(4)
      self.onmessage(data, sender)

def listen_for_broadcasts(onmessage):
  a = ListenerThread(port=9375, onmessage=onmessage)
  a.daemon = True
  a.start()
