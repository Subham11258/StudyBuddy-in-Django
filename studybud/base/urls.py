from django.urls import path
from . import views
urlpatterns=[
    path('',views.home,name='home'),
    path('logout',views.logoutUser,name='logout'),
    path('register/',views.registerPage,name='register'),
    path('profile/<str:pk>/',views.userProfile,name='user-profile'),
    path('login/',views.loginPage,name='login'),
    path('room/<str:pk>/',views.room,name='room'),
    path('create-room/',views.createRoom,name="create-room"),
    path('update-room/<str:pk>',views.updateRoom,name="update-room"),
    path('delete/<str:pk>',views.deleteRoom,name='delete'),
    path('delete-message/<str:pk>',views.deleteMessage,name='delete-message'),
    path('update-user/',views.updateUser,name='update-user'),
    path('topics/',views.topicsPage,name="topics"),
    path('activity/',views.activityPage,name="activity")
]