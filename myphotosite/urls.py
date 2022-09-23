"""myphotosite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from photo_app.views import MainView, PhotoShootView, PhotoDetailsView, ReservationView, LoginView, LogoutView, \
    UserCreateView, AllReservationView, AcceptReservationView, ReservationDetailView, EditReservationView, \
    UserReservationsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainView.as_view(), name="main"),
    path('type/', PhotoShootView.as_view()),
    path('type/<int:id>/', PhotoDetailsView.as_view()),
    path('reservation/<int:id>', ReservationView.as_view()),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view()),
    path('register/', UserCreateView.as_view()),
    path('all-reservation/', AllReservationView.as_view(), name='all-reservation'),
    path('accept/<int:id>', AcceptReservationView.as_view()),
    path('reservation-details/<int:pk>', ReservationDetailView.as_view()),
    path('edit-reservation/<int:pk>', EditReservationView.as_view()),
    path('user-reservations/', UserReservationsView.as_view()),
]
