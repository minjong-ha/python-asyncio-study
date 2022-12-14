import logging
import os
import json
import uuid

#Global configuration
cur = os.path.abspath(os.path.join(__file__, os.pardir))
par = os.path.abspath(os.path.join(cur, os.pardir))
gpar = os.path.abspath(os.path.join(par, os.pardir))

_level = logging.CRITICAL

conf = open(os.path.join(gpar + '/config/log.conf'), 'r')
with open(os.path.join(gpar + '/config/log.conf')) as f:
    data = json.load(f)
    _level = data['level']
    _exrecord = data['extra_record']
    _path = data['path']


def createFolder(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def setBasicConfig(root_path):
    if _exrecord == 'Y':
        tmp = root_path.split('.')[0] + '/' 
        createFolder(_path + tmp)
        file_path = _path + tmp + str(uuid.uuid1()) + '.log'
        logging.basicConfig(filename=file_path,
            format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
            datefmt='%Y-%m-%d:%H:%M:%S',
            level=logging.DEBUG)
    else:
        logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
            datefmt='%Y-%m-%d:%H:%M:%S',
            level=_level)

def get_logger(root_path):
    setBasicConfig(root_path)
    return logging.getLogger()

