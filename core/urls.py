from django.urls import re_path

from core import views


app_name = 'core'

urlpatterns = [
    # Login urls
    re_path(
        r'^user/create/$',
        views.create_user,
        name='create_user'
    ),
    re_path(
        r'user/get/',
        views.get_user,
        name='get_user'
    ),
    re_path(
        r'user/my_profile/',
        views.get_my_profile,
        name='get_my_profile'
    ),
    re_path(
        r'^login/$',
        views.login_view,
        name='login'
    ),
    re_path(
        r'^book_movie/$',
        views.book_movie,
        name='book_movie'
    ),
    re_path(
        r'^theater/screening/add/$',
        views.create_screening,
        name='create_screening'
    ),
    re_path(
        r'^theater/screening/cancel/$',
        views.cancel_screening,
        name='cancel_screening'
    ),
    re_path(
        r'^theater/create/$',
        views.create_theater,
        name='create_theater'
    ),
]
