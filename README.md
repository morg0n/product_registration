# OpenEMR Product Registration

This is a very simple REST service that allows new and current OpenEMR users to register their product with OEMR 501(c)(3). In return, they will receive important software update and security patch email updates. This service will run on AWS (EC2/EBS/SES/RDS) and users of OpenEMR submit their email that will be sent to this remote server.

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

## TRANSLATIONS

This service is simple enough at the moment that the HTTP return statuses will indicate what to display to a consumer with reading the contents of the message. For instance, `AlreadyRegisteredException` throws a HTTP 409 and `InvalidEmailException` throws a HTTP 400. Both of these statuses will be handled in OpenEMR layer with custom user messages that are translated.

The only exception at this time is with the `HTTP POST /api/registration/broadcast` endpoint, which returns various HTTP responses that one will need to see the contents of (which are written in english). However, this is acceptable because this endpoint is to be used exclusively by the OEMR 501(c)(3) board which is all english speaking.

## LOGS

- Local development logs are in `logger/dev.log`
- Production logs are in `/opt/python/log/openemr-product-registration.log` - can be viewed through graphical website via EB > product-registration > logs

## DEPLOY

1. Go to RDS > Get started now > Mysql Production
2. DB Engine version: 5.6.27
3. DB instance class: db.t2.micro
4. Multi-AZ Deployment: “Yes”
5. Storage Type: General Purpose SSD
6. Allocated Storage: 10GB
7. DB Instance Identifier: production-product-registration
8. Enter username/password
9. Accept default options (except for db name of product_registration, and Backup Retention Period to 3 days) and Launch DB instance
10. Click "View your db instances" and wait a few moments
11. Note the endpoint
12. Using your favorite database tool (e.x.: MySQL Workbench), run schema.sql against the new RDS instance (excluding the first line that is `CREATE SCHEMA product_registration` because RDS already created it)
13. Go to SES > Manage Identities > Email addresses > Verify a new email address
14. Enter in "openemrnoreply@gmail.com"
15. Click verify this email address
16. Go to gmail and wait for the verification link to come in
17. Visit this link to submit request to get out of SES sandbox mode: http://aws.amazon.com/ses/extendedaccessrequest/
18. Regarding: Service Limit Increase
19. Limit Type: SES Sending Limits
20. Region: US East (Northern Virginia)
21. Limit: Desired Maximum Send Rate
22. New limit rate: 300
23. Mail Type: System Notifications
24. Website URL http://open-emr.org
25. My email-sending complies with the AWS Service Terms and AUP: yes
26. I only send to recipients who have specifically requested my mail: yes
27. I have a process to handle bounces and complaints: yes
28. Use Case Description: OEMR is a non-profit organization formed to ensure that all people, regardless of race, socioeconomic status or geographic location, have access to high-quality medical care through the donation of free, open source medical software and service relating to that software. OEMR is interested in having SES deliver notifications to our registered users.
29. Support Language: English
30. Contact method: Web
31. `> eb init production-product-registration`
32. region: 1
33. aws-access-id: (IAM oemr access)
34. aws-secret-key: (IAM oemr secret)
35. Specify Python 2.7 for the platform
36. Enter n for SSH
37. `> eb create`
38. Enter production-product-registration for environment name
39. Enter production-product-registration for DNS CNAME prefix
40. Enter 1 for load balancer type and wait a few moments for environment to be provisioned
41. Note the elastic beanstalk address
42. Note the elastic beanstalk security group
43. To set environment variables, go to Elastic Beanstalk > All Applications > product-registration > Configuration > Software Configuration > Environment Properties
44. AWS_ACCESS_ID: (IAM oemr access)
45. AWS_SECRET_KEY: (IAM oemr secret)
46. DB_CONN_STR: mysql+pymysql://prod_user:prod_pass@prod_rds_endpoint/product_registration
47. SECRET_PIN: (secret pin)
48. SES_REGION: us-east-1
49. SES_SENDER: openemrnoreply@gmail.com
50. To prevent RDS from being publically accessible, go to RDS > instances > expand instance > Instance Actions > Modify
51. Set publically accessible to no
52. To allow Elastic Beanstalk to connect to RDS, go to RDS > instances > expand instance > Instance Actions > See Details
53. Click on the security group link
54. With the security group page in view, right click on the security group and select "Edit inbounds rules"
55. In the far right column, enter the EBS security group
56. To set Elastic Beanstalk to always have 1 instance up at any given time, go to Elastic Beanstalk > All Applications > product-registration > Configuration > Auto Scaling
57. Minimum instance count: 1
58. Maximum instance count: 2
59. Set https only on the load balancer. Create a SSL certificate in Certificate Manager. In Elastic Beanstalk application configuration, go to settings of Load Balancer; turn off Listener Port and turn On Secure Listener Support (and assign the SSL certificate that was created in Certificate Manager.
60. Set the database retention retention window on the RDS instance to 35 days(RDS > instances > expand instance > Instance Actions > Modify).

_Note the following about the oemr IAM user:_
- is a service user
- has the following permissions:
  - IAMFullAccess
  - AdministratorAccess
  - AWSElasticBeanstalkService

_Note the following AWS gotchas:_
- You must name the main file `application.py`
- You must name the Flask object `application`
- You must call `application.run(host='0.0.0.0')` as `application.run()` doesn't expose the server properly
- If you add a new environment variable, add it to environment-variables.config as eb needs a default
- Pay close attention to what REGION you are setting up services in. For instance `us-east-1` is where SES is ran from. If `us-west-2` is specified in the SES emailer code, emails will _not_ send.

## PUSHING CHANGES

When new changes are committed and need to be deployed to production, simply run `> eb deploy product-registration`.

## TODOs

- create "OEMR 501(c)(3) Shared Secrets" document
- migrate legimate dev data
- test emailer when in non-sandbox mode
- point domain to prod and set for https mode only (last step in deploy section)

## POST VERSION 1.0.0 TODOs

- Allow for custom HTML emails
- Allow users to re-registration of email addresses
- Allow users to "opt-out" of emails
- Use a open-emr.org noreply email sender instead of the gmail sender
- Store registration IP address in table to prevent spam (?)

## OEMR 501(c)(3) INSTRUCTIONS

Greetings OEMR 501(c)(3) board. This section intends to explain, in plain english, how to get information about registered users and send them important updates about OpenEMR via bulk emailing.

- To see how many users have registered their OpenEMR instance, direct your browser to [https://reg.open-emr.org/api/registration/unique](https://reg.open-emr.org/api/registration/unique). This will return a count of registered users. Please note you will need to total this number with that of SourceForge downloads (there is overlap here, of course).

- To email all registered users an important update email about OpenEMR, download and run [Postman](https://www.getpostman.com/) Chrome application. Configure postman/compose your message as seen below (note the "secretPin" lives in the OEMR 501(c)(3) Shared Secrets document):

![img](instructions-for-emailer.png)

## LICENSE

GNU General Public License (https://www.gnu.org/licenses/gpl-3.0.en.html)
