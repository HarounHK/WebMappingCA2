from django.shortcuts import render, redirect
from .models import Profile as user
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm
from .models import Location
from django.contrib.gis.geos.point import Point
from django.http import JsonResponse

def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'index.html', {'user': request.user})

# View that reads the locations from world borders and passes on to maps
def map_view(request):
    if request.user.is_authenticated:
        user_profile = user.objects.get(user=request.user)
        location = user_profile.location
        return render(request, 'map.html', {'user': request.user, 'location': location})
    else:
        return render(request, 'login.html')

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('login')  
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


def update_location(request):
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        user = request.profile
        user.location = Point(float(longitude), float(latitude))
        user.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

# View to search for a specific location from database
def search_location(request):
    query = request.GET.get('q', '')
    
    locations = Location.objects.filter(name__icontains=query) | Location.objects.filter(address__icontains=query)
    
    location_data = []
    for location in locations:
        location_data.append({
            'name': location.name,
            'address': location.address,
            'latitude': location.latitude,
            'longitude': location.longitude
        })

    return JsonResponse({'locations': location_data})

# View to get all locations
def get_all_locations(request):
    locations = Location.objects.all()  
    location_data = []
    
    for location in locations:
        location_data.append({
            'name': location.name,
            'address': location.address,
            'latitude': location.latitude,
            'longitude': location.longitude
        })
    
    return JsonResponse({'locations': location_data})
