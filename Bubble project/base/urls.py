from django.urls import path, include
from .import views
from django.contrib.auth import views as auth_views




urlpatterns = [
    path('',views.home,name="index"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signin', views.signin, name='signin'),
    path('photo',views.photo,name="photo"),
    path('base',views.base,name="base"),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('chat',views.chat,name="chat"),
    path('create',views.create,name="create"),
    path('rooms',views.rooms,name="rooms"),
    path('chat-room/<int:chat_room_id>/', views.chat_room, name='chat-room'),
    path('dm/<str:friend_username>/',views.dm,name="dm"),
    path('follow/<str:username>/', views.follow, name='follow'),
    path('is_following/<str:username>/', views.is_following, name='is_following'),
    path('send_friend_request/<str:username>/', views.send_friend_request, name='send_friend_request'),
    path('accept_friend_request/<int:request_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('decline_friend_request/<int:request_id>/', views.decline_friend_request, name='decline_friend_request'),
    path('signup', views.signup, name='signup'),
    path('logout', views.logout_view, name='logout'),
    path('notifications',views.notifications,name="notifications"),
    path('add_post/', views.add_post, name='add_post'),
    path('chatrooms/create/', views.create_chat_room, name='create_chat_room'),
    path('add_comment/<int:post_id>/', views.add_comment, name='add_comment'),

]
