'''
Created on May 10, 2018

@author: rli
'''
from . import htmlmail
import logging
import argparse
from datetime import datetime as dt
import datetime
import glob
import shutil
import os
import rlipy.logger

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    #parser.add_argument("-m", "--email",    type=str)
    parser.add_argument('orig_folder',  type=str, help="orginal folder where old files resides in")
    parser.add_argument('age_days',  type=str, help="how old in days are the files to be moved")
    parser.add_argument("-a", dest='archive_folder', type=str, help="archive folder to move files into")
    parser.add_argument("-d", dest="delete", action="store_true", help="delete the old files instead of archiving" )
    parser.add_argument("-l", dest="list_only", action="store_true", help="list the old files instead of moving or deleting" )
    args = parser.parse_args()
    try:
         age = int(args.age_days)
    except:
        print("ERROR: failed to parse age_days %s" % (args.age_days))
        parser.print_usage()
        exit(-1)
    #old_files = []
    now = dt.now()
    old = now-datetime.timedelta(days=age)
    logging.info("move or delete files and folder with modify time older than %s from %s to %s" % 
                (dt.strftime(old,'%Y/%m/%d %H:%M:%S'),
                 args.orig_folder,
                 args.archive_folder
                ))
    all = glob.glob(args.orig_folder+'/*')
    for pathname in all:
        try:
            file_time = dt.fromtimestamp(os.stat(pathname).st_mtime)
            file_name = os.path.basename(pathname)
            if(file_time<old):
                if(args.list_only):
                    print(pathname, dt.strftime(file_time,'%Y/%m/%d %H:%M:%S'))
                elif(args.delete):
                    shutil.rmtree(pathname)
                    logging.info("deleted %s %s" % (pathname, dt.strftime(file_time,'%Y/%m/%d %H:%M:%S')) )
                else:
                    shutil.move(pathname, args.archive_folder+'/'+file_name)
                    logging.info("moved %s %s" % (pathname, dt.strftime(file_time,'%Y/%m/%d %H:%M:%S')) )
                #old_files.append(pathname)
        except:
            logging.error("%s failed" % pathname, exc_info=True)
        
    
