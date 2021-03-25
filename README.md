# Toptal Application for Chris Cauley

## Installation

Before starting, please make sure you have python3 and node>14 installed. Bootstrap the environment with by running the following from the project root.

```
./bin/install
```

The test_fixtures directory contains 3 users and a large number of restaurants. All restaurants are owned by the user with urename "owner". If you want to load test data, run:

```
# load virtual environment
source .venv/bin/activate

# This will create users with usernames `user`, `owner`, `admin` with password `1viPIjbvpYcvIt`
python manage.py loaddata test_fixtures/user.json

# This will create a lot of dummy data for restaurants
python manage.py loaddata test_fixtures/restaurant.json
```

For the purposes of the Toptal demo, I will provide you with the a file `local_settings.py`. Put this in the `server/` directory. This will contain the following settings.

```
SOCIAL_AUTH_GITHUB_KEY = 'REDACTED'
SOCIAL_AUTH_GITHUB_SECRET = 'REDACTED'

SOCIAL_AUTH_TWITTER_KEY = 'REDACTED'
SOCIAL_AUTH_TWITTER_SECRET = 'REDACTED'

EMAIL_HOST_PASSWORD = 'REDACTED'
EMAIL_HOST = 'smtp.sparkpostmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'SMTP_Injection'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'REDACTED'
```

## Development

The server can be started locally with `./bin/develop`. The server will be runnin at http://toptable.localhost:8431/

## Creating new users

* To create a new superuser, run `python manage.py createsuperuser` and follow the prompts.

* To create a new owner or customer, go to the signup page in a browser. After creating a user, log in as the superuser and view the link in the email stored in the admin at http://toptable.localhost:8431/admin/mailer/message/ or run the command `python manage.py send_mail` to send the emails in the queue. (sending emails requires having the settings prefixed `EMAIL_` to be set)

* To create a customer with a github or twitter account, go make sure the `SOCIAL_AUTH_` settings are set and follow the prompts in the local app.