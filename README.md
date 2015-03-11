# djangologinapp

djangologinapp, as the name refers it is just a login, signup only

  - Used with mongoengine backend also with some modifications
  - Nedd to some extra settings in settings.py

### Version
0.1.0

### Installation

You can install via pip:

```sh
$ pip install djangologinapp
```


### in project/settings.py

```sh
INSTALLED_APPS = (
    ...
    'djangologinapp',
    ...
)
```
`Then set the login url`
```sh
APP_URL_DOMAIN = '/loginapp/' #change as your wish, but need to change `GOOGLE_REDIRECT_URL` in Google developer console
LOGIN_URL = APP_URL_DOMAIN + 'login/'
```

`To enable google sign in add following to project/settings.py`
```sh
GOOGLE_SIGNIN = True
GOOGLE_CLIENT_ID = ''
GOOGLE_CLIENT_SECRET = ''
GOOGLE_REDIRECT_URL = '<domain> + APP_URL_DOMAIN + 'login/' #for development=>'http://localhost:8000' + APP_URL_DOMAIN + 'login/' #(http://localhost:8000/loginapp/login/)
GOOGLE_SCOPE = 'profile email'
GOOGLE_GRANT_TYPE = 'authorization_code'
GOOGLE_OAUTH2_URL = 'https://accounts.google.com/o/oauth2/auth?'
```
Note that the `redirect_uri` in Google dev console is must same as `GOOGLE_REDIRECT_URL`(care about trailing slash)

`Then add the following`
```
AFTER_LOGIN_URL = '/' #which url to redirect after successful login
AFTER_LOGOUT_URL = '/' #which url after logout
SIGNIN_IMAGE_URL = 'http://i.huffpost.com/gen/1995938/thumbs/o-AHS-FREAK-SHOW-facebook.jpg' #example
SIGNUP_IMAGE_URL = 'http://i.huffpost.com/gen/1995938/thumbs/o-AHS-FREAK-SHOW-facebook.jpg' #example

```
### in project/urls.py

```sh
from django.conf import settings

urlpatterns = patterns('',
    ...
    url(r'^' + settings.APP_URL_DOMAIN[1:], include('djangologinapp.urls')),
    ...
)

```
Another thing `logout url` throughout your application must be `APP_URL_DOMAIN + 'logout/' ` which you can attchach to logout button
Then put `@login_required` in all your views in  `views.py`.Ith will redirect to `LOGIN_URL` is  `settings.py` 


#FOR MONGOENGINE AS BACKEND

##in project/settings.py

```sh
from mongoengine import *
connect('djangologinapp')

INSTALLED_APPS = (
    ...
    'mongoengine.django.mongo_auth',
    'djangologinapp',
    ...
)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.dummy'
    }
}
MONGO_BACKEND = True
AUTHENTICATION_BACKENDS = (
    'mongoengine.django.auth.MongoEngineBackend',
)
AUTH_USER_MODEL = 'mongo_auth.MongoUser'
SESSION_ENGINE = 'mongoengine.django.sessions'
SESSION_SERIALIZER = 'mongoengine.django.sessions.BSONSerializer'
```
`all other settings are same above`
##in your views.py
`from mongoengine.django.auth import User`