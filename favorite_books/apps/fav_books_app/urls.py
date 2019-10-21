from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^registration$', views.registration),
    url(r'^login$', views.login),
    url(r'^books$', views.welcome),
    url(r'^add_book$', views.add_book),
    url(r'^books/(?P<book_id>\d+)$', views.book_profile),
    url(r'^books/(?P<book_id>\d+)/add_to_my_favs$', views.add_to_my_favs),
    url(r'^books/(?P<book_id>\d+)/update_book$', views.update_book),
    url(r'^books/(?P<book_id>\d+)/unfavorite$', views.unfavorite),
    url(r'^books/(?P<book_id>\d+)/delete$', views.delete),
    url(r'^logout$', views.logout),
]