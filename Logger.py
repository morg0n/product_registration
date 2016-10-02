import logging
import datetime
import time

rawTimestamp = time.time()
formattedTimestamp = datetime.datetime.fromtimestamp(rawTimestamp).strftime('%Y-%m-%d %H:%M:%S')

logging.basicConfig(filename="openemr-product-registration.log", level=logging.DEBUG)

def debug(message):
  print(formattedTimestamp + " DEBUG: " + message)
  logging.debug(" " + formattedTimestamp + " " + message)

def info(message):
  print(formattedTimestamp + " INFO: " + message)
  logging.info(" " + formattedTimestamp + " " + message)

def error(message):
  print(formattedTimestamp + " ERROR: " + message)
  logging.error(" " + formattedTimestamp + " " + message)
