from django.urls import path 
from .views import *
from . import views
# from.api_view import *
app_name='chat'


urlpatterns = [
    path('',views.home,name='home'),
    path('chat/',views.main,name='main'),
    path('chat_details/<slug:slug>',views.chat_details,name='chat_details'),
    path('send_message/<slug:slug>',views.send_message,name='send_message'),
    path('receive_message/<slug:slug>',views.receive_message,name='receive_message'),
    path('friend_request/<slug:slug>',views.friend_request,name='friend_request'),
    path('add_friend/',views.add_friend,name='add_friend'),
    path('send_request/<slug:slug>',views.send_request,name='send_request'),
    path('accecpt_friend_request/<slug:slug>',views.accecpt_friend_request,name='accecpt_friend_request'),
    # path('hotel/',PropertyList.as_view(),name='property_list'),
    # path('hotel/<slug:slug>',PropertyDetail.as_view(),name='property_detail'),
    # path('create/',PropertyCreate.as_view(),name='property_create'),
    
    
    # # api
    # path('property/list',PropertyAPiList.as_view(),name='PropertyAPiList'),
    # path('property/list/<int:pk>',PropertyAPiDetail.as_view(),name='PropertyAPiDetail'),
]
