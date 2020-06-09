from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.shortcuts import redirect, render
from .forms import SignUpForm
from django.core.cache import cache
from django.utils.datetime_safe import datetime
from datetime import timedelta
import logging
import csv


logger = logging.getLogger(__name__)
csv_log = open('log.csv', mode='a', buffering=1)
csv_writer = csv.writer(csv_log, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@login_required(login_url='/login')
def homepage_request(request):
    return render(request=request,
                  template_name="main/homepage.html")


def signup_request(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, f"Konto zostało utworzone. Witaj {username}!")
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password, backend='django.contrib.auth.backends.ModelBackend')
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect("main:homepage")

        else:
            # for msg in form.error_messages:
            #   messages.error(request, f"{msg}: {form.error_messages[msg]}")

            return render(request=request,
                          template_name="main/signup.html",
                          context={"form": form})

    return render(request=request,
                  template_name="main/signup.html",
                  context={"form": SignUpForm()})


@login_required(login_url='/login')
def logout_request(request):
    logout(request)
    messages.info(request, "Wylogowano!")
    return redirect("/")


class InvalidLoginAttemptsCache(object):
    @staticmethod
    def _key(identifier):
        return 'invalid_login_attempt_{}'.format(identifier)

    @staticmethod
    def _value(lockout_timestamp, timebucket):
        return {
            'lockout_start': lockout_timestamp,
            'invalid_attempt_timestamps': timebucket
        }

    @staticmethod
    def delete(identifier):
        try:
            cache.delete(InvalidLoginAttemptsCache._key(identifier))
        except Exception as e:
            logger.error(e.message)

    @staticmethod
    def set(identifier, timebucket, lockout_timestamp=None):
        try:
            key = InvalidLoginAttemptsCache._key(identifier)
            value = InvalidLoginAttemptsCache._value(lockout_timestamp, timebucket)
            cache.set(key, value)
        except Exception as e:
            logger.error(e.message)

    @staticmethod
    def get(identifier):
        try:
            key = InvalidLoginAttemptsCache._key(identifier)
            return cache.get(key)
        except Exception as e:
            logger.error(e.message)


def is_locked_out(identifier):
    cache_results = InvalidLoginAttemptsCache.get(identifier)
    logger.error(cache_results)
    if cache_results:
        if lockout_start := cache_results.get('lockout_start'):
            locked_out = lockout_start + timedelta(minutes=15) >= datetime.now()
            if not locked_out:
                InvalidLoginAttemptsCache.delete(identifier)
                return False
            return True
    return False


def invalid_attempt(identifier, attempts=5):
    cache_results = InvalidLoginAttemptsCache.get(identifier)
    lockout_timestamp = None
    now = datetime.now()
    invalid_attempt_timestamps = cache_results['invalid_attempt_timestamps'] if cache_results else []

    invalid_attempt_timestamps.append(now.timestamp)
    if len(invalid_attempt_timestamps) >= attempts:
        lockout_timestamp = now
        logger.error(f'LOCKING ATTEMPTS FOR {identifier}')
    InvalidLoginAttemptsCache.set(identifier, invalid_attempt_timestamps, lockout_timestamp)


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)

        # rate limits
        if form.is_bound:
            username = form['username'].value()
            password = form['password'].value()
            ip = get_client_ip(request)
            if is_locked_out(username) or is_locked_out(ip):
                messages.error(request, f"Zbyt wiele nieudanych prób. Proszę spróbować później")
                csv_writer.writerow([datetime.now().timestamp(), username, password, ip, True])
                return redirect('main:homepage')

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Jesteś zalogowany jako {username}")
                # reset login attempts
                InvalidLoginAttemptsCache.set(username, [], None)
                InvalidLoginAttemptsCache.set(ip, [], None)
                return redirect('main:homepage')
            else:
                messages.error(request, "Błędny login lub hasło.")
        else:
            invalid_attempt(ip, attempts=10)
            invalid_attempt(username)
            csv_writer.writerow([datetime.now().timestamp(), username, password, ip, False])
            messages.error(request, "Błędny login lub hasło.")
    return render(request=request,
                  template_name="main/login.html",
                  context={"form": AuthenticationForm()})
