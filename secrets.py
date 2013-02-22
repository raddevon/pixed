# This is a session secret key used by webapp2 framework.
SESSION_KEY = '' # Enter a long random string for the session key. http://clsc.net/tools-old/random-string-generator.php

# Google APIs. Get your ID and secret from the Google API Console @ https://code.google.com/apis/console/
GOOGLE_APP_ID = ''
GOOGLE_APP_SECRET = ''

# config that summarizes the above
AUTH_CONFIG = {
    # OAuth 2.0 providers
    'google'      : (GOOGLE_APP_ID, GOOGLE_APP_SECRET,
                     'https://www.googleapis.com/auth/userinfo.profile'),

    # OpenID doesn't need any key/secret
}
