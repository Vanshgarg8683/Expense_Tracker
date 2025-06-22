from django.urls import path
from tracker.views import index, remove, registration, loginpage, logoutpage
urlpatterns = [
    path('', index, name="index"),
    path('registration', registration, name="register"),
    path('login', loginpage, name="loginpage"),
    path('logout', logoutpage, name="logoutpage"),
    path('deletetransaction/<uuid>/', remove, name="remove")
]