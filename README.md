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
11. Go to SES > Manage Identities > SMTP Settings
12. Note the server name
13. Click Create My SMTP Credentials
14. Note SMTP user credentials
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

_Note the following AWS gotchas:_
- You must name the main file `application.py`
- You must name the Flask object `application`
- You must call `application.run(host='0.0.0.0')` as `application.run()` doesn't expose the server properly
- If you add a new environment variable, add it to environment-variables.config as eb needs a default

## LOGS

- Local development logs are in `logger/dev.log`
- Production logs are in `/opt/python/log/openemr-product-registration.log`

## TODOs
- Clean up instances from testing
- Correct SES configuration issues
- Ensure security groups/firewalls are configured securely
- Purchase domain name/SSL cert and setup/document Route 53 configuration
- Hook up with https://github.com/openemr/openemr/pull/257
- Setup RDS in production mode
- Testing and code reviews
- Instruct OEMR board on how to use this service

## LICENSE

GNU General Public License (https://www.gnu.org/licenses/gpl-3.0.en.html)
