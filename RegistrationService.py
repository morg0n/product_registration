from database import db
from Models import Product
from EmailerService import EmailerService
from validate_email import validate_email
from Exceptions import AlreadyRegisteredException, InvalidSecretPinException, InvalidEmailMessageException, InvalidEmailException
import uuid
import Logger

emailer = EmailerService()

class RegistrationService:
  def __init__(self):
    pass

  def registrationLookupByEmail(self, email):
    return Product.query.filter_by(email=email).first()

  def registerProduct(self, email):
    Logger.info("Attempting to register product with email: " + str(email))
    isValidEmail = validate_email(str(email))
    if isValidEmail != True:
      raise InvalidEmailException("Please supply a valid email")

    isProductRegistered = self.registrationLookupByEmail(email)
    if isProductRegistered != None:
      raise AlreadyRegisteredException(str(email) + " has already registered")

    generatedUuid = str(uuid.uuid4())

    p = Product(generatedUuid, email)
    db.session.add(p)
    db.session.commit()

    Logger.info("Email " + email + "is registered with product id: " + generatedUuid)

    return generatedUuid

  def getUniqueRegistrations(self):
    return Product.query.all()

  def broadcastToRegisteredUsers(self, secretPin, title, contents):
    # TODO: use proper config management
    if (secretPin != "my secret pin"):
      raise InvalidSecretPinException("Invalid secret pin")

    if title == None or contents == None:
      raise InvalidEmailMessageException("Include title and contents for the message")

    Logger.info("Attempting to broadcast an email with title: " + title)

    for registration in self.getUniqueRegistrations():
      emailer.send(registration.email, "no-reply@open-emr.org", title, contents)
