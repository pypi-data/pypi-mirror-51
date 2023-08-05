'''
Created on Nov 15, 2016

@author: rli
'''
import netrc
from ftplib import FTP_TLS
from ftplib import FTP
import sys
import os
import sftp
class FtpException(Exception):
        pass

def sftpUpload(usename, host, remotePath, localPath):
    sftp = pysftp.Connection(host=host, username=usename, private_key='~/.ssh/id_rsa_sftp')
    sftp.put(localPath, remotePath=remotePath)
    
def ftp_to_ml(localfile, remote_file):
    (user,acct,passwd)=netrc.netrc().authenticators('ftps.b2b.ml.com')
    ftp = FTP_TLS('ftps.b2b.ml.com')
    remote_dir = 'incoming/gmigefs2'
    ftp.login(user, passwd, acct)
    ftp.prot_p()
    ftp.cwd(remote_dir)
    local_fd = open(localfile, 'r')
    ftp.storlines('STOR '+remote_file, local_fd)
    local_fd.close()
    
def ftp_to_realtick(localfile, remote_file):
    (user,acct,passwd)=netrc.netrc().authenticators('client.taltrade.com')
    ftp = FTP('client.taltrade.com')
    remote_dir = 'ETB'
    ftp.login(user, passwd, acct)
    ftp.cwd(remote_dir)
    local_fd = open(localfile, 'r')
    ftp.storlines('STOR '+remote_file, local_fd)
    local_fd.close()

if __name__ == '__main__':
    local_file = sys.argv[1]
    remote_file = sys.argv[2]
    print("uploading %s as %s" % (local_file, remote_file))
    ftp_to_ml(local_file, remote_file)
    
    