from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('search-location/', views.search_location, name='search_location'),
    path('search-nearby/', views.search_nearby, name='search_nearby'),
    path('books/', views.books_list, name='booklist'),
    path('add-to-userbooks/', views.add_to_userbooks, name='add_to_userbooks'),
    path('mybooks/', views.mybooks, name='mybooks'),
    path('bookswatchlist/', views.bookswatchlist, name='bookswatchlist'),
    path('remove-from-userbooks/', views.remove_from_userbooks, name='remove_from_userbooks'),
    path('save-location/', views.save_location, name='save_location'),
    path('saved-locations/', views.saved_locations, name='saved_locations'),
    path('delete-location/<int:id>/', views.delete_location, name='delete_location'),
]