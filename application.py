from flask import Flask, jsonify
from registration.RegistrationService import RegistrationService
from database.Database import db
from logger import Logger
from config.Config import Config
from flask_sqlalchemy import SQLAlchemy
from flask import request

application = Flask(__name__)
application.config["SQLALCHEMY_DATABASE_URI"] = Config.DB_CONN_STR

db.init_app(application)

registrationService = RegistrationService()

@application.route("/")
def default():
  return (jsonify({"status": "up"}), 200)

@application.route("/api/registration", methods=["POST"])
def postRegistration():
  productUuid = registrationService.registerProduct(request.values.get("email"))

  return (jsonify({"productId": productUuid}), 201)

@application.route("/api/registration/broadcast", methods=["POST"])
def postRegistrationBroadcast():
  registrationService.broadcastToRegisteredUsers(request.values.get("secretPin"),
                                                 request.values.get("title"),
                                                 request.values.get("contents"))

  return (jsonify({"status": "sent"}), 200)

@application.route("/api/registration/unique", methods=["GET"])
def getRegistrationUnique():
  registrationsCount = len(registrationService.getUniqueRegistrations())
  return (jsonify({"count": registrationsCount}), 200)

@application.errorhandler(Exception)
def globalUnHandledExceptionHandler(error):
  Logger.error(error.message)

  # If the exception is custom, it will have a return code, else
  # return a generic system error message.
  if error != None and hasattr(error, 'httpReturnCode'):
    return (jsonify({"error": error.message}), error.httpReturnCode)

  return (jsonify({"error": "Server error"}), 500)

if __name__ == '__main__':
  Logger.info("Starting server")
  application.run(host='0.0.0.0')
