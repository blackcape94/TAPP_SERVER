"""
API for TAPP
"""
import pdb, json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY, load_backend
from django.contrib.auth.models import AnonymousUser, User
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from backend.models import Tapper
from django.conf import settings
from django.utils.importlib import import_module
from django.contrib.sessions.models import Session


@csrf_exempt
def user_login(request):
    pdb.set_trace()
    message = ""
    try:
        username = request.POST.get('username')
        password = request.POST.get('password')
    except KeyError:
        return HttpResponseBadRequest()
    try:
        User.objects.get(username=username)
    except ObjectDoesNotExist:
        #Wrong username
        messages = "Invalid Username and Password combination"
        return HttpResponseRedirect(login_page)

    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_staff or user.is_superuser:
            #User is staff. Cannot login as Tapper
            message = "Cannot login as superuser. Logout or go to /admin"
            json_response = json.dumps({
                "success": "false",
                "message": message
            })
            return HttpResponse(json_response, content_type='application/json')
        if user.is_active:
            try:
                #tapper = Tapper.objects.get(user=user)
                login(request, user)
                json_response = json.dumps({
                    "success": "true",
                    "sessionid": request.COOKIES['session_id']
                })
                return HttpResponse(json_response, content_type='application/json')
            except ObjectDoesNotExist:
                return HttpResponseBadRequest()
        else:
            #Inactive Account
            message = "Sorry, this account is inactive. To activate contact Support"
            json_response = json.dumps({
                "success": "false",
                "message": message
            })
            return HttpResponse(json_response, content_type='application/json')
    else:
        #Wrong Password
        message = "Invalid Username and Password combination"
        json_response = json.dumps({
            "success": "false",
            "message": message
        })
        return HttpResponse(json_response, content_type='application/json')

@csrf_exempt
def is_logged_in(request):
    try:
        username = request.POST.get('username')
    except:
        return HttpResponseBadRequest()
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
        is_logged_in = user.is_authenticated()
        json_response = json.dumps({
            "is_logged_in": is_logged_in
        })
        return HttpResponse(json_response, content_type='application/json')
    else:
        json_response = json.dumps({
            "success": "false",
            "message": "User with that username does not exist"
        })
        return HttpResponse(json_response, content_type='application/json')


@csrf_exempt
def user_register(request):
    pdb.set_trace()
    try:
        input_first_name = request.POST.get('first_name')
        input_last_name = request.POST.get('last_name')
        input_username = request.POST.get('username')
        input_email = request.POST.get('email')
        input_password = request.POST.get('password')
        input_phone_num = request.POST.get('phone_num')
        input_pin = request.POST.get('pin')
    except KeyError:
        return HttpResponse(incomingData)

    if User.objects.filter(email=input_email).exists():
        json_response = json.dumps({
            "success": "false",
            "message": "E-mail is already taken"
        })
        return HttpResponse(json_response, content_type='application/json')
    if User.objects.filter(username=input_username).exists():
        json_response = json.dumps({
            "success": "false",
            "message": "Username is already taken"
        })
        return HttpResponse(json_response, content_type='application/json')
    try:
        user = User.objects.create_user(input_username, input_email, input_password)
        user.first_name = input_first_name
        user.last_name = input_last_name
        user.is_active = True
        user.save()
    except:
        user.delete()
        return HttpResponse("Error saving user. Please try again")
    try:
        tapper = Tapper(
            user=user,
            phone_number=input_phone_num,
        )
        tapper.save()
    except:
        tapper.delete()
        user.delete()
        return HttpResponse("Error saving tapper account. Please try again later")
    new_tapper = authenticate(username=input_username, password=input_password)
    try:
        login(request, new_tapper)
        json_response = ({
            "success": "true",
            "sessionid": request.session.session_key
        })
    except:
        return HttpResponse("Failed to login the user")


@csrf_exempt
def is_a_user(sessionid):

    engine = import_module(settings.SESSION_ENGINE)
    session = engine.SessionStore(sessionid)

    try:
        user_id = session[SESSION_KEY]
        backend_path = session[BACKEND_SESSION_KEY]
        backend = load_backend(backend_path)
        user = backend.get_user(user_id) or AnonymousUser()
    except KeyError:
        user = AnonymousUser()

    if user.is_authenticated():
        return user
    else:
        return False

@csrf_exempt
def user_logout(request):
    try:
        sessionid = request.POST.get('sessionid')
        user = is_a_user(sessionid)
        if user is False:
            return HttpResponse("Not a user")
    except KeyError:
        return HttpResponseBadRequest()
    try:
        logout(request)
        json_response = json.dumps({
            "success": "true"
        })
        return HttpResponse(json_response, content_type="application/json")
    except:
        json_response = json.dumps({
            "success": "false",
            "message": "Unable to logout user"
        })
        return HttpResponse(json_response, content_type="application/json")

@csrf_exempt
def force_logout(request):
    try:
        username = request.POST.get('username')
    except:
        return HttpResponseBadRequest()
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
        [s.delete() for s in Session.objects.all() if s.get_decoded().get('_auth_user_id') == user.id]
        json_response = json.dumps({
            "success": "true",
            "message": "Deleted all sessions for user"
        })
        return HttpResponse(json_response, content_type='application/json')
    else:
        json_response = json.dumps({
            "success": "false",
            "message": "User with that username does not exist"
        })
        return HttpResponse(json_response, content_type='application/json')

@csrf_exempt
def get_user_info(request):
    try:
        username = request.POST.get('username')
    except:
        return HttpResponseBadRequest()
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
        json_response = json.dumps({
            "success": "true",
            "first_name" : user.first_name,
            "last_name" : user.last_name,
            "username" : user.username,
            "email" : user.email,
            "phone_number" : user.tapper.phone_number
        })
        return HttpResponse(json_response, content_type='application/json')
    else:
        json_response = json.dumps({
            "success": "false",
            "message": "User with that username does not exist"
        })
