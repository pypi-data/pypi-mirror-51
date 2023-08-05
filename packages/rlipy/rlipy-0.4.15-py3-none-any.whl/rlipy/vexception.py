'''
Created on Nov 15, 2016

@author: rli
'''

class FileNotExists(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)

class ReqFileError(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)
                
class LocateRequestError(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)