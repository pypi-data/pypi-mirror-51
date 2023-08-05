import argparse
import sys
import time

import zmq


class zpull(object):

    def __init__(self, context, address):
        self.context = context
        self.socket = self.context.socket(zmq.PULL)
        self.socket.set_hwm(10000)
        self.socket.setsockopt(zmq.RCVTIMEO, 0)
        self.socket.setsockopt(zmq.LINGER, 1000)

        self.address = address
        self.socket.bind(address)

    def recv(self):
        try:
            msg = self.socket.recv()
            return msg
        except zmq.Again as e:
            return None

    def close(self):
        self.socket.close()

    def __del__(self):
        self.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(dest = "address", type = str, help = 'zmq push address')
    parser.add_argument('-f', dest = "file", type = str, help = 'input file')

    args = parser.parse_args()
    zcontext = zmq.Context()
    socket = zpull(zcontext, "tcp://" + args.address)
    zpoller = zmq.Poller()
    zpoller.register(socket.socket, zmq.POLLIN)
    while(True):
        try:
          events = dict(zpoller.poll(1000))
          if(socket.socket in events and events[socket.socket] == zmq.POLLIN):
             msg = socket.socket.recv()
             print(msg)
             sys.stdout.flush()
        except KeyboardInterrupt:
            break
        except:
            break

    socket.close()
    zcontext.term()

