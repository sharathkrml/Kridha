
from django.urls import path
from .views import addaddress, login, signup, logout, forgot, verify, reset, user, editaddress
urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('signup/', signup, name='signup'),
    path('forgot/', forgot, name='forgot'),
    path('forgot/verify', verify, name='verify'),
    path('forgot/reset', reset, name='reset'),
    path('user/', user, name='user'),
    path('addaddress/', addaddress, name='addaddress'),
    path('editaddress/', editaddress, name='editaddress'),
]
