# OpenEMR Product Registration

This is a very simple REST service that allows new and current OpenEMR users to register their product with OEMR 501(c)(3). In return, they will receive important software update and security patch email updates. This service will run on AWS (EC2/EB/SES/RDS) and users of OpenEMR submit their email that will be sent to this remote server.

## REST API OVERVIEW

__HTTP POST /api/registration__
- INPUT: Unique `email` to be stored in MySQL along with a product `uuid`
- OUTPUT: `{"productId": "55cd33ef-f6dd-4d28-925d-d652da3d70b2" }` HTTP 201
- THROWS: `AlreadyRegisteredException` HTTP 409, `InvalidEmailException` HTTP 400

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

__Edit the db connection string in `config.py` (local development):__
```
DB_CONN_STR = 'mysql+pymysql://user:pass@localhost/product_registration'
```

__Install dependencies:__

```
> pip install -r requirements.txt
```

__Spin up server (local development):__

```
> python app.py --dev
```

## i18n

This service is simple enough at the moment that the HTTP return statuses will indicate what to display to a consumer with reading the contents of the message. For instance, `AlreadyRegisteredException` throws a HTTP 409 and `InvalidEmailException` throws a HTTP 400. Both of these statuses will be handled in OpenEMR layer with custom user messages that are translated.

The only exception at this time is with the `HTTP POST /api/registration/broadcast` endpoint, which returns various HTTP responses that one will need to see the contents of (which are written in english). However, this is acceptable because this endpoint is to be used exclusively by the OEMR 501(c)(3) board which is all english speaking.

## LOGS

- Local development logs are in `logger/dev.log`
- Production logs are in `/opt/python/log/openemr-product-registration.log` - can be viewed through graphical website via EB > product-registration > logs

## DEPLOY

1. Follow steps in above section with the exception of setting environment variables in config.py.
2. Go to RDS > Get started now > Mysql (free tier) > "Only show options that are eligble for RDS Free Tier"
3. Enter 5.6.27 for DB Engine version
4. Select db.t1.micro for DB instance class
5. Enter product-registration for "DB instance instance identifier"
6. Enter username/password
7. Accept default options and Launch DB instance
8. Click "View your db instances" and wait a few moments
9. Note the endpoint
10. Using your favorite database tool (e.x.: MySQL Workbench), run schema.sql against the new RDS instance
11. Go to SES > Manage Identities > Email addresses > Verify a new email address
12. Enter in "openemrnoreply@gmail.com"
13. Click verify this email address
14. Go to gmail and wait for the verification link to come in
15. `> eb init product-registration`
16. For region, enter 1
17. To get access/secret keys, go to IAM Console > Users > IAM user > Security Credentials > Create Access Key
18. Specify Python 2.7 for the platform
19. Enter n for SSH
20. `> eb create`
21. Enter product-registration for environment name
22. Enter product-registration for DNS CNAME prefix
23. Enter 1 for load balancer type and wait a few moments
24. Note the elastic beanstalk address
25. Note the elastic beanstalk security group
26. To set environment variables, go to Elastic Beanstalk > All Applications > product-registration > Configuration > Software Configuration > Environment Properties
27. To allow Elastic Beanstalk to connect to RDS, go to RDS > instances > expand instance > Instance Actions > See Details
28. Click on the security group
29. With the security group page in view, right click on the security group and select "Edit inbounds rules"
30. In the far right column, enter the EBS security group
31. To prevent RDS from being publically accessible, go to RDS > instances > expand instance > Instance Actions > Modify
32. Set publically accessible to no

_Note the following AWS gotchas:_
- You must name the main file `application.py`
- You must name the Flask object `application`
- You must call `application.run(host='0.0.0.0')` as `application.run()` doesn't expose the server properly
- If you add a new environment variable, add it to environment-variables.config as eb needs a default

## PUSHING CHANGES

When new changes are committed and need to be deployed to production, simply run `> eb deploy product-registration`.

## TODOs

- Hook up with https://github.com/openemr/openemr/pull/257
- Purchase domain name/SSL cert and setup/document Route 53 configuration
- Testing and code reviews
- Find/create "OEMR 501(c)(3) Shared Secrets" document
- Deploy service in a production context (setup RDS in production mode, move out of the Amazon SES sandbox mode, and update these docs)

## POST VERSION 1.0.0 TODOs

- Allow for custom HTML emails
- Allow users to "opt-out" of emails
- Use a open-emr.org noreply email sender instead of the gmail sender
- Store registration IP address in table to prevent spam (?)

## OEMR 501(c)(3) INSTRUCTIONS

Greetings OEMR 501(c)(3) board. This section intends to explain, in plain english, how to get information about registered users and send them important updates about OpenEMR via bulk emailing.

- To see how many users have registered their OpenEMR instance, direct your browser to [https://reg.open-emr.org/api/registration/unique](https://reg.open-emr.org/api/registration/unique). This will return a count of registered users. Please note you will need to total this number with that of SourceForge downloads (there is overlap here, of course).

- To email all registered users an important update email about OpenEMR, download and run [Postman](https://www.getpostman.com/) Chrome application. Config postman/compose your message as seen below (note the "secretPin" lives in the OEMR 501(c)(3) Shared Secrets document):

![img](instructions-for-emailer.png)

## LICENSE

GNU General Public License (https://www.gnu.org/licenses/gpl-3.0.en.html)
