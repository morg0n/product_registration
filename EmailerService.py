import Logger

class EmailerService:
  def __init__(self):
    pass

  def send(self, toEmail, fromEmail, title, contents):
    # TODO: bring in boto emailer for SES
    Logger.info("Attempting to broadcast an update email to: " + toEmail)

