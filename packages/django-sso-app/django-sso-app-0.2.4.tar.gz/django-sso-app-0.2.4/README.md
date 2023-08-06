# django-sso-app

Django package for [django-sso][django-sso].

This is alpha software and is under heavy development.

----

### Prerequisites

When DJANGO_SSO_REPLICATE_PROFILE is set either django custom user model or related user profile model MUST declare
required fields (look at settings.py), related profile must be linked by DJANGO_SSO_USER_PROFILE_MODEL settings var.

```
# django_sso_app.settings.py

DJANGO_SSO_REQUIRED_PROFILE_FIELDS = [
    "sso_id", "sso_rev",
    "latitude", "longitude",
    "first_name", "last_name",
    "description",
    "picture",
    "birthdate",
    "address", "country",
    "language",
    "is_unsubscribed"]

# settings.py
DJANGO_SSO_USER_PROFILE_MODEL = 'apps.profiles.models.Profile'

```

### Configure SSO

```
DJANGO_SSO_COOKIE_DOMAIN = os.environ.get('COOKIE_DOMAIN', 'example.com')
DJANGO_SSO_USER_PROFILE_MODEL = getattr(settings, 'DJANGO_SSO_USER_PROFILE_MODEL', None)
DJANGO_SSO_DEACTIVATE_USER_ON_UNSUBSCRIPTION=env_to_bool('DJANGO_SSO_DEACTIVATE_USER_ON_UNSUBSCRIPTION')
DJANGO_SSO_SERVICE_SUBSCRIPTION_IS_MANDATORY=env_to_bool('DJANGO_SSO_SERVICE_SUBSCRIPTION_IS_MANDATORY')
DJANGO_SSO_STAFF_JWT = os.environ.get('DJANGO_SSO_STAFF_JWT', None)

DJANGO_SSO_URL = os.environ.get('DJANGO_SSO_URL', 'https://accounts.example.com')
DJANGO_SSO_BACKEND_URL = os.environ.get('DJANGO_SSO_BACKEND_URL', DJANGO_SSO_URL)
DJANGO_SSO_SERVICE_URL = os.environ.get('DJANGO_SSO_SERVICE_URL', 'https://protectedservice.example.com')
```

### Setup

Add **django_sso_app** to INSTALLED_APPS

```
# settings.py

INSTALLED_APPS = [
..
    'apps.profiles' # optional
    ..
    'django_sso_app'
]

```

Override Django admin urls modifying your main urls.py as follows.

```
# urls.py

urlpatterns = [
    ..
    url(r'^admin/', include('django_sso_app.urls_admin'))
    ..
    url(r'^admin/', include(admin.site.urls)),  # NOQA
    ..
]
```

Required authentication backends.

```
AUTHENTICATION_BACKENDS = (
    'django_sso_app.backends.SsoBackend',
    'django.contrib.auth.backends.ModelBackend',
)
```

Required middleware.

```
# settings.py

MIDDLEWARE = [
    ..
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_sso_app.middleware.SsoMiddleware',
    ..
] 

```

Enable logger.

```
# settings.py

LOGGING['loggers']['django_sso_app'] = {
    'handlers': ['console'],
    'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
}
```

Enable context processor.
```
# settings.py

TEMPLATES[0]['OPTIONS']['context_processors'] += [
    'django_sso_app.context_processors.sso_cookie_domain',
]
```

Enable app_directory template loader
```
TEMPLATES[0]['OPTIONS']['loaders'] += [
    'django.template.loaders.app_directories.Loader',
]
```


[django-sso]: https://bitbucket.org/pai/django-sso
[src]: https://bitbucket.org/pai/django-sso-app
[md]: https://tools.ietf.org/html/rfc7764#section-3.5 "CommonMark variant"
[md use]: https://packaging.python.org/specifications/core-metadata/#description-content-type-optional
