# This is a session secret key used by webapp2 framework.
SESSION_KEY = "w2kc31cc7igh6mogt12034yu079r7d7xg0f8zar87184x236qz"

# Google APIs
GOOGLE_APP_ID = '559497696228.apps.googleusercontent.com'
GOOGLE_APP_SECRET = '7MSwO_pgFYTdHdbb8EBaVR45'

# config that summarizes the above
AUTH_CONFIG = {
    # OAuth 2.0 providers
    'google'      : (GOOGLE_APP_ID, GOOGLE_APP_SECRET,
                     'https://www.googleapis.com/auth/userinfo.profile'),

    # OpenID doesn't need any key/secret
}
