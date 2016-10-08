import sys
import os

class Config(object):
  if len(sys.argv) == 2 and sys.argv[1] == "--dev":
    # These configs are for local development only
    SECRET_PIN = 'secret'
    DB_CONN_STR = 'mysql+pymysql://user:pass@localhost/product_registration'
    SES_ACCESS_ID = 'id'
    SES_SECRET_KEY = 'secret'
    SES_REGION = 'us-west-2'
    SES_SENDER = 'test@test.com'

  else:
    SECRET_PIN = os.environ['SECRET_PIN']
    DB_CONN_STR = os.environ['DB_CONN_STR']
    SES_ACCESS_ID = os.environ['SES_ACCESS_ID']
    SES_SECRET_KEY = os.environ['SES_SECRET_KEY']
    SES_REGION = os.environ['SES_REGION']
    SES_SENDER = os.environ['SES_SENDER']
