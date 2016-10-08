from logger import Logger
from config.Config import Config
import boto.ses

class EmailerService:
  def __init__(self):
    pass

  def send(self, toEmail, title, contents):
    connection = boto.ses.connect_to_region(
      Config.SES_REGION,
      aws_access_key_id=Config.SES_ACCESS_ID,
      aws_secret_access_key=Config.SES_SECRET_KEY
    )

    Logger.info("Attempting to broadcast an update email to: " + toEmail)
    connection.send_email(Config.SES_SENDER, title, contents, [toEmail])
