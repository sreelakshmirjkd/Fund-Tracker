
from django.urls import path
from api import views
from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = [

    path('register/', views.ApiSignupView.as_view()), # url is given in APIDOC. So, in FundTracker urls.py, we just give the api/ which is mentionned in APIDOC, not in urls.py inside api app

    path("transactions/", views.TransactionListCreateView.as_view()),

    path("transactions/<int:pk>/", views.TransactionRetrieveUpdateDestroyView.as_view()),

    path('token/', ObtainAuthToken.as_view()),
    
]