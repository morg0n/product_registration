import logging
from logging import handlers
import datetime
import time
from config.Config import Config

logFile = "./logger/dev.log" if Config.DEV_MODE else "/opt/python/log/openemr-product-registration.log"
logFormatter = logging.Formatter('%(asctime)s;%(levelname)s;%(message)s')
log = logging.handlers.TimedRotatingFileHandler(logFile, 'midnight', 1, backupCount=15)
log.setLevel(logging.DEBUG)
log.setFormatter(logFormatter)
logger = logging.getLogger()
logger.addHandler(log)
logger.setLevel(logging.DEBUG)

rawTimestamp = time.time()
formattedTimestamp = datetime.datetime.fromtimestamp(rawTimestamp).strftime('%Y-%m-%d %H:%M:%S')

def debug(message):
  print(formattedTimestamp + " DEBUG: " + message)
  logger.debug(message)

def info(message):
  print(formattedTimestamp + " INFO: " + message)
  logger.info(message)

def error(message):
  print(formattedTimestamp + " ERROR: " + message)
  logger.debug(message)
