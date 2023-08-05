'''
Created on Jun 19, 2017

@author: rli
'''
'''
Created on Jun 19, 2017

@author: rli
'''
import argparse
import sys
import time

import zmq


class zpub(object):

    def __init__(self, context, address):
        self.context = context
        self.socket = self.context.socket(zmq.PUB)
        self.socket.set_hwm(1000000)
        self.socket.setsockopt(zmq.LINGER, 1000)
        self.address = address
        self.socket.bind(address)

    def send(self, msg):
        self.socket.send(msg)

    def close(self):
        self.socket.close()

    def __del__(self):
        self.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(dest = "address", type = str, help = 'zmq publish address')
    parser.add_argument('-f', dest = "file", type = str, help = 'input file')

    args = parser.parse_args()
    zcontext = zmq.Context()
    socket = zpub(zcontext, "tcp://" + args.address)
    use_stdin = False
    if(args.file is not None):
        print(("publish file " + args.file))
        fh = open(args.file, 'r')
    else:
        fh = sys.stdin
        use_stdin = True
    time.sleep(1)
    while(True):
        if(use_stdin):
            msg = input('< ')
            if(msg == 'quit'):
                break
        else:
            msg = fh.readline()
            if(len(msg) == 0):
                break;
            msg = msg.rstrip()
        print(('> ' + msg))
        socket.send(msg.encode('ascii'))
    socket.close()
