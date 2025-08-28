from django.urls import path
from .views import LoginViewSet, UserViewSet, MyAccountViewSet

myaccount = MyAccountViewSet.as_view({
    'get': 'list',
    'patch': 'update',
    'delete': 'destroy'
})

users = UserViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

urlpatterns = [
    # Authentication endpoints
    path('login/', LoginViewSet.as_view({'post': 'login'})),
    path('login/refresh/', LoginViewSet.as_view({'post': 'refresh'})),

    # User management endpoints
    path('', users, name='users'),

    # My account endpoints
    path("my-account/", myaccount, name="myaccount"),
]
