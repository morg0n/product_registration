from flask import Flask, jsonify
from RegistrationService import RegistrationService
from Database import db
from Exceptions import InvalidEmailMessageException, AlreadyRegisteredException, InvalidSecretPinException, InvalidEmailException
from flask_sqlalchemy import SQLAlchemy
from flask import request
import Logger
from config import Config

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = Config.DB_CONN_STR

db.init_app(app)

registrationService = RegistrationService()

@app.route("/api/registration", methods=["POST"])
def postRegistration():
  productUuid = registrationService.registerProduct(request.values.get("email"))

  return (jsonify({"productId": productUuid}), 201)

@app.route("/api/registration/broadcast", methods=["POST"])
def postRegistrationBroadcast():
  registrationService.broadcastToRegisteredUsers(request.values.get("secretPin"),
                                                 request.values.get("title"),
                                                 request.values.get("contents"))

  return (jsonify({"status": "sent"}), 200)

@app.route("/api/registration/unique", methods=["GET"])
def getRegistrationUnique():
  registrationsCount = len(registrationService.getUniqueRegistrations())
  return (jsonify({"count": registrationsCount}), 200)

@app.errorhandler(Exception)
def globalUnHandledExceptionHandler(error):
  Logger.error(error.message)

  # If the exception is custom, it will have a return code, else
  # return a generic system error message.
  if error != None and hasattr(error, 'httpReturnCode'):
    return (jsonify({"error": error.message}), error.httpReturnCode)

  return (jsonify({"error": "Server error"}), 500)

app.run()
