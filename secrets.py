# This is a session secret key used by webapp2 framework.
SESSION_KEY = "24u6y2x97ecw01vw7w3611ngt7471jsk6y7au2h1xkuhit8w09"

# Google APIs
GOOGLE_APP_ID = '559497696228.apps.googleusercontent.com'
GOOGLE_APP_SECRET = '4X1RgqFiFjcrdPuaoJU2OiCx'

# config that summarizes the above
AUTH_CONFIG = {
  # OAuth 2.0 providers
  'google'      : (GOOGLE_APP_ID, GOOGLE_APP_SECRET,
                  'https://www.googleapis.com/auth/userinfo.profile'),

  # OpenID doesn't need any key/secret
}
