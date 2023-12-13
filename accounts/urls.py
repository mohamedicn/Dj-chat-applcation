from unicodedata import name
from django.urls import path ,include
from . import views
from .api_view import *
from django.conf import settings
from django.conf.urls.static import static
app_name='accounts'


urlpatterns = [
    # path('signup',views.signup ,name='signup'),
    # path('signin',views.signin ,name='signin'),
    path('login/',views.signup,name='login'),
    path('activate_account/<uidb64>/<token>/', views.activate_account, name='activate'),
    path('log_out',views.log_out ,name='log_out'),
    path('password_reset/',views.password_reset ,name='password_reset'),
    path('password_change/<slug:slug>',views.password_change ,name='password_change'),
    path('password_reset_set/<uidb64>/<token>/',views.password_reset_set ,name='password_reset_set'),
    path('profile/<slug:slug>',views.profile ,name='profile'),
    path('profile/<slug:slug>/editprofile',views.edit_profile ,name='edit'),
    
    
    
    
    # api
    # path('user/list',UserViewSet.as_view({'get': 'list'}))c,
    path('api/register',RegisterUserAPIView.as_view()),
    path('api/login',LoginView.as_view(),name='login_api'),
    path('api/profile/<slug:slug>',ProfileAPi.as_view()),
    path('api/profile/<slug:slug>/editprofile',ProfileAPIUpdate.as_view()),
    path('api/password_reset', password_reset.as_view(), name='password_reset'),
    path('api/password_reset_set/<uidb64>/<token>/', password_reset_set.as_view(), name='password_reset_set'),
    
    
    # path('user/list',PropertyAPiList.as_view(),name='PropertyAPiList'),
    
    
    # path('remove_myresevation/<int:resevation_id>',views.remove_myresevation ,name='remove_myresevation'),
    # path('remove_mylisting/<int:property_id>',views.remove_mylisting ,name='remove_mylisting'),
]
