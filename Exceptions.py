class InvalidEmailException(Exception):
  def __init__(self, message):
    super(InvalidEmailException, self).__init__(message)
    self.httpReturnCode = 400

class AlreadyRegisteredException(Exception):
  def __init__(self, message):
    super(AlreadyRegisteredException, self).__init__(message)
    self.httpReturnCode = 500

class InvalidSecretPinException(Exception):
  def __init__(self, message):
    super(InvalidSecretPinException, self).__init__(message)
    self.httpReturnCode = 401

class InvalidEmailMessageException(Exception):
  def __init__(self, message):
    super(InvalidEmailMessageException, self).__init__(message)
    self.httpReturnCode = 400
