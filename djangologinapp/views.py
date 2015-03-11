from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.conf import settings
import json
import requests
from mongoengine import *
from django.db import IntegrityError
try:
    if settings.MONGO_BACKEND:
        from mongoengine.django.auth import User
except AttributeError:
    pass

# Create your views here.

app_url_domain = settings.APP_URL_DOMAIN


def login_app(request):
    try:
        if settings.SIGNIN_IMAGE_URL:
            img_url = settings.SIGNIN_IMAGE_URL
    except AttributeError:
        img_url = None
    error = None if not request.GET.get("error") else request.GET.get("error")
    if error:
        try: 
            if settings.GOOGLE_SIGNIN:
                return render(request, 'login.html', {"app_url_domain": app_url_domain, 'g_signin': True, "error": error, "err_msg": "Something went wrong in server: "+str(error), "img_url": img_url})
        except AttributeError:
            return render(request, 'login.html', {"app_url_domain": app_url_domain, "error": error, "err_msg": "Something went wrong in server: "+str(error), "img_url": img_url})

    """
    if user not logged in, returns login page
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                next = request.POST.get('next')
                if not next:
                    return HttpResponseRedirect(settings.AFTER_LOGIN_URL)
                return HttpResponseRedirect(next)
            return HttpResponseRedirect(app_url_domain + "login/?error=Not Active user")
        else:
            return HttpResponseRedirect(app_url_domain + "login/?error=Invalid Credentials")

    if request.method == "GET":
        state = request.GET.get("state")
        code = request.GET.get("code")
        if all([state, code, state==request.session.session_key]):
            resp = requests.post(
                url='https://www.googleapis.com/oauth2/v3/token',
                data={
                    "code": code,
                    "client_id": settings.GOOGLE_CLIENT_ID,
                    "client_secret": settings.GOOGLE_CLIENT_SECRET,
                    "redirect_uri": settings.GOOGLE_REDIRECT_URL,
                    "grant_type": settings.GOOGLE_GRANT_TYPE
                }
            )
            access_token = resp.json().get('access_token')
            if access_token:
                resp1 = requests.get("https://www.googleapis.com/plus/v1/people/me?access_token=" +  access_token)
                email = resp1.json()["emails"][0]["value"]
                username = resp1.json().get("displayName")
                user_post = User.objects.filter(username=email)
                if user_post:
                    user = user_post[0]
                else:
                    if resp1.json().get("name"):
                        first_name = resp1.json().get("name").get("givenName")
                    else:
                        first_name = None
                    user = User()
                    user.username = email
                    if first_name:
                        user.first_name = first_name
                    user.set_password(settings.SECRET_KEY)
                    user.save()
                user = authenticate(
                    username=email, password=settings.SECRET_KEY)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return HttpResponseRedirect(settings.AFTER_LOGIN_URL)
                return HttpResponseRedirect(app_url_domain + 'login/?error=500')
            return HttpResponseRedirect(app_url_domain + 'login/?error=Invalid credentials for Google')
    try: 
        if settings.GOOGLE_SIGNIN:
            return render(request, 'login.html', {"app_url_domain": app_url_domain, 'g_signin': True, "img_url": img_url})
    except AttributeError:
        return render(request, 'login.html', {"app_url_domain": app_url_domain, "img_url": img_url})
    return render(request, 'login.html', {"app_url_domain": app_url_domain, "img_url": img_url})


def signup_app(request):
    try:
        if settings.SIGNUP_IMAGE_URL:
            img_url = settings.SIGNIN_IMAGE_URL
    except AttributeError:
        img_url = None
    error = None if not request.GET.get("error") else request.GET.get("error")
    if error:
        return render(request, 'signup.html', {"app_url_domain": app_url_domain, "error": error, "err_msg": error, "img_url": img_url})
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not all([username, password]):
            return HttpResponseRedirect(app_url_domain + "signup/?error=Please fill all the fields")    
        try:
            user = User()
            user.username = request.POST['username']
            user.set_password(request.POST['password'])
            user.save()
        except (NotUniqueError, IntegrityError):
            return HttpResponseRedirect(app_url_domain + "signup/?error=Username or email is already registered")

        user = authenticate(
            username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect("/")
            return HttpResponseRedirect(app_url_domain + "signup/?error=User not active")
        return HttpResponseRedirect(app_url_domain + "signup/?error=Invalid Credentials")    
                #request.session['user'] = {'username':
                #                           user.username, 'email': user.email}

    return render(request, 'signup.html', {"app_url_domain": app_url_domain, "img_url": img_url})


def logout_app(request):
    logout(request)
    return HttpResponseRedirect(settings.AFTER_LOGOUT_URL)


def return_resp(status, data=None):
    return HttpResponse(
        json.dumps(
            {
                "result" : status,
                "url": data 
            }
            )
        )

def get_gdata(request):
    try:
        all([settings.GOOGLE_OAUTH2_URL,
            settings.GOOGLE_CLIENT_ID,
            settings.GOOGLE_SCOPE,
            settings.GOOGLE_REDIRECT_URL])
    except AttributeError:
        return return_resp(500)
    g_url = settings.GOOGLE_OAUTH2_URL + \
    'client_id=' + settings.GOOGLE_CLIENT_ID +\
    '&scope=' + settings.GOOGLE_SCOPE +\
    '&response_type=code' +\
    '&redirect_uri=' + settings.GOOGLE_REDIRECT_URL +\
    '&state=' + str(request.session.session_key)
    
    return return_resp(200, g_url)
