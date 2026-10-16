from django.urls import path
from .views import login_view, signup_view, profile_view, logout_view
from . import views
from .views import forgot_password, password_reset_confirm
urlpatterns = [
    path('login/',views.login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('profile/', profile_view, name='profile'),
    path('logout/', logout_view, name='logout'),
     path('forgot-password/', forgot_password, name='forgot_password'),
    path('reset/<uidb64>/<token>/', password_reset_confirm, name='password_reset_confirm'),
]
