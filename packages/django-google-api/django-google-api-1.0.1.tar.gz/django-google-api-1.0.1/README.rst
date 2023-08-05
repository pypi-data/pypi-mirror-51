.. image:: https://img.shields.io/badge/version-v1.0.1-blue.svg
    :target: https://pypi.org/project/django-google-api/
    :alt: PyPI Version

.. image:: https://img.shields.io/badge/license-GPL-blue
    :alt: GPL License

.. image:: https://img.shields.io/badge/python-3.5%20%7C%203.6%20%7C%203.7-blue
    :alt: Platform & Version Support

Installation
============

Installing from PyPI is as easy as doing:

.. code-block:: bash

  pip install django-google-api


Intigration
===========

django-google-api is a library to use Google API with Django

step:- 1
--------

create **credentials.json** file on DJango project Base Directory where your **manage.py** file exist

    | django-project
    | ├── django-project
    | │   ├── __init__.py
    | │   ├── settings.py
    | │   ├── urls.py
    | │   └── wsgi.py
    | ├── **credentials.json**
    | ├── manage.py
    | └── requirements.txt


step:- 2
--------

Add the application to ``INSTALLED_APPS`` setting, for default ORM:

.. code-block:: python

  INSTALLED_APPS = [
     ...
     'django_google.apps.DjangoGoogleConfig',
  ]

step:- 3
--------

Google OAuth credentials set ``GOOGLE_CLIENT_SECRET_FILE`` and ``GOOGLE_AUTH_SCOPES`` in **setting.py** you can add scope of your choices

.. code-block:: python

    GOOGLE_CLIENT_SECRET_FILE = os.path.join(BASE_DIR, 'credentials.json')
    GOOGLE_AUTH_SCOPES = [
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/userinfo.profile',
    ]

if you're using javascript authentication then add this line to your project also

.. code-block:: python

    GOOGLE_CLIENT_ID = "xxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxx.apps.googleusercontent.com"



Usage:
======

**execute commands**

.. code-block:: bash

    python manage.py makemigrations
    python manage.py migrate

Create Views in **views.py**

.. code-block:: python

    from django.shortcuts import reverse, redirect, render
    from django_google.flow import DjangoFlow,CLIENT_SECRET_FILE, SCOPES
    from django.http.response import JsonResponse
    from django.contrib.auth import get_user_model
    from django.conf import settings
    from django_google.models import GoogleAuth
    User = get_user_model()

    flow = DjangoFlow.from_client_secrets_file(client_secrets_file=CLIENT_SECRET_FILE, scopes=SCOPES)

    # Auto Redirect to Google Authentication URL (Using Without Javascript)
    def oAuthView(request):
            callback_url=reverse("oauth2callback") # callback Url (oAuth2CallBackView URL)
            return redirect(flow.get_auth_url(request, callback_url=callback_url))

    # Google Authentication Call Back VIEW (Using Without Javascript)
    def oAuth2CallBackView(request):
        success_url = "/dashboard/"  # redirection URL on Success reverse() can b use here
        creds = flow.get_credentails_from_response_url(response_url=request.build_absolute_uri())
        userinfo = flow.get_userinfo(creds=creds)
        try:
            user = User.objects.get(email=userinfo['email'])
        except User.DoesNotExist:
            user = User.objects.create(email=userinfo['email'],
                                               username=userinfo['email'],
                                               first_name=userinfo['given_name'],
                                               last_name=userinfo['family_name']
                                           )
        finally:
            try:
                gauth = GoogleAuth.objects.get(user=user)
            except GoogleAuth.DoesNotExist:
                gauth = GoogleAuth.objects.create(user=user, creds=creds)

        # Return Response as you want or Redirect to some URL

    def oAuthJavascriptView(request):
        if request.is_ajax():
            if request.method == "POST":
                code = request.POST.get('code')
                flow = DjangoFlow.from_client_secrets_file(client_secrets_file=CLIENT_SECRET_FILE, scopes=SCOPES)
                creds = flow.get_credentials_from_code(code=code, javascript_callback_url="https://example.org")
                userinfo = flow.get_userinfo(creds=creds)
                try:
                    user = User.objects.get(email=userinfo['email'])
                except User.DoesNotExist:
                    user = User.objects.create(email=userinfo['email'],
                                                   username=userinfo['email'],
                                                   first_name=userinfo['given_name'],
                                                   last_name=userinfo['family_name']
                                               )
                finally:
                    try:
                        gauth = GoogleAuth.objects.get(user=user)
                    except GoogleAuth.DoesNotExist:
                        gauth = GoogleAuth.objects.create(user=user, creds=creds)
                # return JSON Response with Status Code of 200 for success and 400 for errors
                return JsonResponse({}, status=200)

        else:
            context = {
                "client_id": getattr(settings, 'GOOGLE_CLIENT_ID', None),
                "scopes": " ".join(SCOPES)
            }
            # Render HTML page that havs Google Authentication Page with Javasccript
            return render(request, 'login.html', context)

Create Views in **urls.py**

.. code-block:: python

    from django.urls import path
    from .views import oAuthView, oAuth2CallBackView, oAuthJavascriptView

    urlpatterns = [
        path('', oAuthJavascriptView, name="login"),
        path('auth/', oAuthView, name="auth"),
        path('oauth2callback/', oAuth2CallBackView, name="oauth2callback"),
    ]

**login.html** file create Button of your own choice for google auth

.. code-block:: html

    <script src="https://apis.google.com/js/api:client.js"></script>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery-cookie/1.4.1/jquery.cookie.min.js"></script>
    <button id="g-auth-btn">Sign in with <b>Google</b></button>
    <script>
    function startApp() {
        gapi.load('auth2', function(){
            auth2 = gapi.auth2.init({
                client_id: '{{ client_id }}',
                cookiepolicy: 'single_host_origin',
            });
        });
    }

    $(document).on("click", "#g-auth-btn", ()=>{
        auth2.grantOfflineAccess({
            prompt:"consent",
            scope: '{{ scopes }}'
        }).then((signInCallback)=>{
            $.ajax({
                type:'post',
                data:signInCallback,
                cache: false,
                headers: {"X-CSRFToken": $.cookie('csrftoken')},
                success: function (response) {
                    console.log(response);
                    if(!!response.redirect){
                        window.location = response.redirect
                    }
                },
                error: function (error) {
                    console.log(error);
                    if(!!error.responseJSON.redirect){
                        window.location = error.responseJSON.redirect
                    }
                }
            });
        });
    });
    startApp();
    </script>


