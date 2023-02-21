from django.urls import path
from .import views


#app_name = "room_n"
urlpatterns =[
    path("", views.rooms, name="rooms"),
    path("<slug:slug>", views.room, name="room"),
    path('delete_message/<int:message_id>/', views.delete_message, name='delete_message'),
]