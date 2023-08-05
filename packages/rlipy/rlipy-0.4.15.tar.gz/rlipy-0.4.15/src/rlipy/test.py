'''
Created on Nov 13, 2017

@author: rli
'''
import zmqpush
import zmq  
import datetime
import logging
import rlipy.logger
if __name__ == '__main__':
    context = zmq.Context()
    push = zmqpush.ZmqPush("push_test", context)
    push.connect("tcp://faked:1000")