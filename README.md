# OpenEMR Product Registration

This is a very simple REST backend that allows new and current OpenEMR users to register their product with OEMR 501(c)(3). In return, they will receive important software update and security patch email updates. This service will run on AWS (EC2/EB/SES/RDS) and users of OpenEMR submit their email that will be sent to this remote server.

## REST API OVERVIEW

__HTTP POST /api/registration__
- INPUT: Unique `email` to be stored in MySQL along with a product `uuid`
- OUTPUT: `{"productId": "55cd33ef-f6dd-4d28-925d-d652da3d70b2" }` HTTP 201
- THROWS: `AlreadyRegisteredException` HTTP 500, `InvalidEmailException` HTTP 400

__HTTP POST /api/registration/broadcast__
- INPUT: `secretPin`, `title`, and `contents` to be sent to all registered users
- OUTPUT: `{"status": "sent"}` HTTP 200
- THROWS: `InvalidSecretPinException` HTTP 401, `InvalidEmailMessageException` HTTP 400

__HTTP GET /api/registration/unique__
- OUTPUT: ex: `{"count": 9001}` HTTP 200

## PREREQUISITES

- MySQL >= 14.14
- Python >= 2.7
- Pip >= 1.5.4

## RUN

__Setup up database:__

```
> mysql -u your_username -p product_registration < schema.sql
```

__Temporarily hand-edit the connection string in `app.py`:__
```
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://user:pass@localhost/product_registration"
```

__Install dependencies:__

```
> pip install -r requirements.txt
```

__Spin up server:__

```
> python app.py
```

## TODOs

- Use proper configuration for db connection and secret pin
- Document virtualenv in README
- Set up emailer
- Rate limit post endpoints
- Hook up with https://github.com/openemr/openemr/pull/257
- Split out code into proper folders
- Testing and code reviews
- Instruct OEMR board on how to use this service
- Deploy to AWS EC2 (DNS/SSL/SES/RDS/EB)

## LICENSE

GNU General Public License (https://www.gnu.org/licenses/gpl-3.0.en.html)
