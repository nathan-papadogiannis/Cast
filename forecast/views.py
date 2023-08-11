from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm
from django.shortcuts import render

from forecast.forecast import get_forecast
from forecast.models import NewsPost

from django.shortcuts import render, redirect
from .forms import RegistrationForm



def calculate_sun_position():
    # Get the sunrise and sunset times (replace with your own logic)
    sunrise_time = datetime.now().replace(hour=6, minute=0, second=0)  # Example: 6:00 AM
    sunset_time = datetime.now().replace(hour=18, minute=0, second=0)  # Example: 6:00 PM

    # Get the current time
    current_time = datetime.now()

    # Calculate the duration between sunrise and sunset
    duration = sunset_time - sunrise_time

    # Calculate the elapsed time from sunrise to the current time
    elapsed_time = current_time - sunrise_time

    # Calculate the sun position as a percentage along the path
    sun_position = int((elapsed_time / duration) * 100)
    sun_position = max(0, min(sun_position, 100))  # Ensure the position is within the range [0, 100]

    return sun_position


# Create your views here.

def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to the login page after successful registration
    else:
        form = RegistrationForm()
    return render(request, 'registration.html', {'form': form})

def page_not_found_view(request):
    return render(request, '404.html', status=404)


def home(request):
    return render(request, 'home.html')


def cast_select(request):
    return render(request, 'cast_select.html')


def cast_current(request):
    forecast = get_forecast(11360)
    sp = calculate_sun_position()
    return render(request, 'cast_result.html', context={
        'current': forecast.current,
        'hourly': forecast.hourly,
        "sunPosition": sp,
    })


def cast_hourly(request):
    forecast = get_forecast(11360).hourly
    return render(request, 'cast_result.html', context={
        'hourly': forecast,
    })


def cast_daily(request):
    forecast = get_forecast(11360).daily
    return render(request, 'cast_result.html', context={
        'daily': forecast,
    })


def about(request):
    return render(request, 'about.html')


@login_required
def account(request):
    if not request.user.is_authenticated:
        return render(request, 'registration.html')
    else:
        if request.method == 'POST':
            # User wants to update their account information
            form = UserChangeForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                return redirect('account')
        else:
            # Display account information
            form = UserChangeForm(instance=request.user)
        return render(request, 'account.html', {'form': form})

def news(request):
    posts = NewsPost.objects.all()
    return render(request, 'news_page.html', {'posts': posts})
