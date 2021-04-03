from django.conf.urls import url
from .views import add_book, show_books
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index')
]

# urlpatterns = [
#    path('add_book/', add_book),
#    path('show_books/', show_books),
# ]
