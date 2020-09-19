from django.urls import path
from . import views
                    
urlpatterns = [
    path('', views.index),
    path('register', views.register),
    # path('shows', views.shows),
    path('logout', views.logout),
    path('login', views.login),
    path('wishes', views.wishes),
    path('wishes/new', views.new_wish),
    path('create_wish', views.create_wish),
    path('like_wish/<int:wish_id>', views.like_wish),
    path('grant_wish/<int:wish_id>', views.grant_wish),
    path('wishes/edit/<int:wish_id>', views.edit_wish),
    path('post_edit_wish/<int:wish_id>', views.post_edit),
    path('remove_wish/<int:wish_id>', views.remove),
    path('wishes/stats', views.stats)

    # path('add_book', views.add_book),
    # path('like_book/<int:book_id>', views.like_book),
    # path('unlike_book/<int:book_id>', views.unlike_book),
    
]