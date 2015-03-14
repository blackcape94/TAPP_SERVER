from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.models import AnonymousUser, User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
from django.conf import settings

from forms import CreateUserForm, CreateTapperForm

import pdb
from models import Tapper

# When account is created via social, fire django-allauth signal to populate Django User record.
# from allauth.account.signals import user_signed_up
# from django.dispatch import receiver

# Create your views here.
def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('home'))
    return render(request, 'index.html', {
        'DEPLOY_MODE': settings.DEPLOY_MODE
    })

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

def login_page(request):
    """
    Page to login
    """
    user = request.user
    if user == AnonymousUser():
        return render(request, 'accounts/login.html')
    elif Tapper.objects.filter(user=user).exists():
        #User is already logged in
        return HttpResponseRedirect(reverse('home'))
    elif user.is_staff or user.is_superuser:
        messages.info(request, "Logged out as superuser. Log in as Tapper")
        logout(request)
        return render(request, 'accounts/login.html')

def signup_page(request):
    """
    Renders the signup page
    """
    if request.method =='POST':
        user_form = CreateUserForm(request.POST, prefix="user")
        tapper_form = CreateTapperForm(request.POST, prefix="tapper")
        if user_form.is_valid() and tapper_form.is_valid():
            try:
                tapper = tapper_form.save(commit=False)
                user = user_form.save(commit=True)
                tapper.user = user
                tapper.save()
            except:
                user.delete()
                tapper.delete()
            try:
                new_user = authenticate(username=request.POST['user-username'],
                                        password=request.POST['user-password'])
                login(request, new_user)
                messages.success(request, 'Succesfully registered and logged in!')
                return HttpResponseRedirect('/profile')
            except:
                message.success(request, 'Succesfully registered. Log in')
                return HttpResponseRedirect('/')
        else:
            return render(request, 'accounts/signup.html', {
                'user_form': user_form,
                'tapper_form': tapper_form
            })
    else:
        user = request.user
        user_form = CreateUserForm(prefix="user")
        tapper_form = CreateTapperForm(prefix="tapper")
        if user == AnonymousUser():
            return render(request, 'accounts/signup.html', {
                'user_form': user_form,
                'tapper_form': tapper_form
            })
        elif Tapper.objects.filter(user=user).exists():
            #User is already logged in
            return HttpResponseRedirect("/profile")
        elif user.is_staff or user.is_superuser:
            messages.info(request, "Logged out as superuser")
            logout(request)
            return render(request, 'accounts/signup.html', {
                'user_form': user_form,
                'tapper_form': tapper_form
            })

def process_login(request):
    """
    Authenticate the user
    """
    login_page = reverse_lazy("login")
    home_page = reverse_lazy("home")
    try:
        username = request.POST['username']
        password = request.POST['password']
    except KeyError:
        return HttpResponseBadRequest()

    try:
        User.objects.get(username=username)
    except ObjectDoesNotExist:
        #Wrong username
        messages.error(request, "Invalid Username and Password combination")
        return HttpResponseRedirect(login_page)

    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_staff or user.is_superuser:
            #User is staff. Cannot login as Tapper
            messages.error(request, "Cannot login as superuser. Logout or go to /admin")
            return HttpResponseRedirect(login_page)
        if user.is_active:
            try:
                #tapper = Tapper.objects.get(user=user)
                login(request, user)
                messages.success(request, "Succesfully logged in")
                return HttpResponseRedirect(request.POST.get('next', home_page))
            except ObjectDoesNotExist:
                return HttpResponseBadRequest()
        else:
            #Inactive Account
            messages.error(request, "Sorry, this account is inactive. To activate contact Support")
            return HttpResponseRedirect(login_page)
    else:
        #Wrong Password
        messages.error(request, "Invalid Username and Password combination")
        return HttpResponseRedirect(login_page)

def process_logout(request):
    """
    Logs out the current user
    """
    logout(request)
    messages.success(request,"Succesfully logged out")
    return HttpResponseRedirect("/")



# @receiver(user_signed_up)
# def create_tapper(request, user, **kwargs):
#     '''
#     When a social account is created successfully and this signal is received,
#     django-allauth passes in the sociallogin param, giving access to metadata on the remote account, e.g.:
#
#     sociallogin.account.provider  # e.g. 'twitter'
#     sociallogin.account.get_avatar_url()
#     sociallogin.account.get_profile_url()
#     sociallogin.account.extra_data['screen_name']
#
#     See the socialaccount_socialaccount table for more in the 'extra_data' field.
#     '''
#     pdb.set_trace()
#     user.first_name = sociallogin.account.extra_data['first_name']
#     user.last_name = sociallogin.account.extra_data['last_name']
#     user.save()
