import requests 
from django.http import JsonResponse  
from django.shortcuts import render, redirect  
from .models import Profile as user, Location  
from django.contrib.auth import login, logout, authenticate  
from django.contrib.auth.forms import AuthenticationForm  
from .forms import SignUpForm  
from django.contrib.gis.geos.point import Point  
from .models import Book, UserBooks  
from django.db.models import Q  
from django.core.paginator import Paginator 

# Overpass API url
OVERPASS_API_URL = "http://overpass-api.de/api/interpreter"

# Homepage if users is logged in
def index(request):
    if not request.user.is_authenticated: 
        return redirect('login')  
    return render(request, 'index.html', {'user': request.user})  

# Shows map if user is loged in
def map_view(request):
    if request.user.is_authenticated: 
        user_profile = user.objects.get(user=request.user) 
        location = user_profile.location 
        return render(request, 'map.html', {'user': request.user, 'location': location})  
    else:
        return render(request, 'login.html')  

# Handles user signup
def signup_view(request):
    if request.method == 'POST':  
        form = SignUpForm(request.POST)  
        if form.is_valid():  
            user = form.save()  
            username = form.cleaned_data.get('username') 
            password = form.cleaned_data.get('password1')  
            user = authenticate(username=username, password=password)  
            login(request, user)  
            return redirect('index')  
    else:
        form = SignUpForm()  
    return render(request, 'signup.html', {'form': form})  

# Handles user login 
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

# Handles user logout
def logout_view(request):
    logout(request)  
    return redirect('login')  

# Searches for a spcific location
def search_location(request):
    query = request.GET.get('q', '').strip()  
    latitude = request.GET.get('latitude')  
    longitude = request.GET.get('longitude')  
    radius = request.GET.get('radius', '5000') 

    if len(query) < 2: 
        return JsonResponse({'error': 'Search term is too short. Please enter at least 2 characters.'}, status=400)

    # Overpass query to search for libraries or bookstores
    overpass_query = f"""
    [out:json];
    (
        node[amenity="library"](around:{radius},{latitude},{longitude});
        node[shop="books"](around:{radius},{latitude},{longitude});
    );
    out;
    """

    try:
        response = requests.post(OVERPASS_API_URL, data={'data': overpass_query})  
        data = response.json()

        locations = [
            {
                'name': element.get('tags', {}).get('name', 'Unknown'),
                'latitude': element['lat'],
                'longitude': element['lon'],
                'address': element.get('tags', {}).get('addr:street', 'Unknown'),
                'website': element.get('tags', {}).get('website', 'Not Available'),
                'wheelchair': element.get('tags', {}).get('wheelchair', 'Not Specified'),
                'operator': element.get('tags', {}).get('operator', 'Not Specified'),
            }
            for element in data.get('elements', [])
            if query.lower() in element.get('tags', {}).get('name', '').lower()
        ]

        if locations:
            return JsonResponse({'locations': locations})  
        else:
            return JsonResponse({'error': 'Your search does not exist. Try searching for libraries or bookstores near your area.'}, status=404)

    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': 'error occured'}, status=500)

# Searches for nearby libraries or bookstores within radius
def search_nearby(request):
    query = request.GET.get('q', '')  
    latitude = request.GET.get('latitude') 
    longitude = request.GET.get('longitude')  
    radius = request.GET.get('radius', '5000')  

    tags = {
        "libraries": '[amenity="library"]',
        "bookstores": '[shop="books"]',
    }

    overpass_query = f"""
    [out:json];
    node{tags[query.lower()]}(around:{radius},{latitude},{longitude});
    out;
    """

    try:
        response = requests.post(OVERPASS_API_URL, data={'data': overpass_query})  
        data = response.json() 

        locations = [
            {
                'name': element.get('tags', {}).get('name', 'Unknown'),
                'latitude': element['lat'],
                'longitude': element['lon'],
                'address': element.get('tags', {}).get('addr:street', 'Unknown'),
                'website': element.get('tags', {}).get('website', 'Not Available'),
                'wheelchair': element.get('tags', {}).get('wheelchair', 'Not Specified'),
                'operator': element.get('tags', {}).get('operator', 'Not Specified'),
            }
            for element in data.get('elements', [])
        ]

        return JsonResponse({'locations': locations}) 
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': 'error occured'}, status=500)


# Handles book listing 
def books_list(request):
    query = request.GET.get('query', '') 
    filter_author = request.GET.get('author', '')  
    filter_genre = request.GET.get('genre', '')  
    sort_by = request.GET.get('sort', 'title')  

    books = Book.objects.all()  

    if query:
        books = books.filter(
            Q(title__icontains=query) | 
            Q(author__icontains=query) |  
            Q(genres__icontains=query)  
        )

    if filter_author:
        books = books.filter(author__icontains=filter_author)

    if filter_genre:
        books = books.filter(genres__icontains=filter_genre)

    #sorting books
    if sort_by == 'rating':
        books = books.order_by('-avg_rating')  
    elif sort_by == 'title':
        books = books.order_by('title')  
    elif sort_by == 'author':
        books = books.order_by('author')  

    paginator = Paginator(books, 50)  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number) 

    return render(request, 'booklist.html', {'page_obj': page_obj})  

# Adds books to users lists(mybooks/watchlist)
def add_to_userbooks(request):
    if request.method == "POST":  
        import json
        data = json.loads(request.body)  

        book_id = data.get('book_id')  
        status = data.get('status') 

        try:
            book = Book.objects.get(id=book_id) 
        except Book.DoesNotExist:
            return JsonResponse({'error': 'Book isnot found'}, status=404)

        userbook, created = UserBooks.objects.get_or_create(user=request.user, book=book, status=status)

        if created:
            message = "Book added to MyBooks" if status == "read" else "Book added to BookWatchlist"
        else:
            message = "Book alreadyadded to MyBooks" if status == "read" else "Book already added to BookWatchlist"

        return JsonResponse({'message': message})

    return JsonResponse({'error': 'Invalid request method'}, status=400)  

# Handles mbooks page
def mybooks(request):
    books = UserBooks.objects.filter(user=request.user, status='read')  
    return render(request, 'mybooks.html', {'books': books})  

# Handles bookwatchlit page
def bookswatchlist(request):
    books = UserBooks.objects.filter(user=request.user, status='to_read') 
    return render(request, 'bookswatchlist.html', {'books': books})

# Removes book from users lists(mybooks/watchlist)
def remove_from_userbooks(request):
    if request.method == "POST":  
        book_id = request.POST.get('book_id') 
        status = request.POST.get('status')  

        try:
            book = Book.objects.get(id=book_id) 
        except Book.DoesNotExist:
            return JsonResponse({'error': 'Book not found'}, status=404)

        UserBooks.objects.filter(user=request.user, book=book, status=status).delete()

        return redirect(request.META.get('HTTP_REFERER', 'mybooks'))