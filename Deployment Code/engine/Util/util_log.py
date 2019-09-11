import logging, logging.handlers
import os
from logging import FileHandler
from engine.Util import PROJECT_DIR


log_dir = PROJECT_DIR + '/logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
    
def log_format(log_path, logger):
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    logging.basicConfig(level = logging.INFO)
            
    info_formatter = logging.Formatter('%(name)s - %(asctime)s - %(levelname)s  - %(message)s')
    err_formatter = logging.Formatter('%(name)s - %(asctime)s - %(levelname)s - [line:%(lineno)d] - %(message)s')

#    handler = TimedRotatingFileHandler('{}/LogReport.log'.format(log_path),
#                                           when="m",
#                                           interval=1,
#                                           backupCount=60)
#    handler1 = TimedRotatingFileHandler('{}/ErrorReport.log'.format(log_path),
#                                           when="m",
#                                           interval=1,
#                                           backupCount=60)
    handler = FileHandler('{}/LogReport.log'.format(log_path))
    handler1 = FileHandler('{}/ErrorReport.log'.format(log_path))
    handler.setLevel(logging.INFO)
    handler1.setLevel(logging.ERROR)
    
    handler.setFormatter(info_formatter)
    handler1.setFormatter(err_formatter)
    
    logger.addHandler(handler)
    logger.addHandler(handler1)
            
    