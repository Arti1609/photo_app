from datetime import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import FormView, DetailView
from django.views.generic.edit import FormMixin, UpdateView

from photo_app.models import PhotoShootType, Package, Reservations
from photo_app.forms import LoginForm, UserForm, ReservationsForm
from django.urls import reverse_lazy, reverse


# Create your views here.

class SuperuserRequiredMixin(UserPassesTestMixin):
    def test_func(self): #true albo false
        """
        sprawdza czy użytkownik jest superuserem
        :return: zwraca superusera
        """
        return self.request.user.is_superuser


class MainView(View):
    def get(self, request):
        """

        :param request:
        :return: strona główna
        """
        return render(request, template_name='index.html')


class PhotoShootView(View):
    def get(self, request):
        """
        dostępne typy sesji z bazy danych.
        :param request:
        :return:Typy sesji zdjęciowych
        """
        photo_types = PhotoShootType.objects.all()
        ctx = {
            'photo_types': photo_types
        }
        return render(request, template_name='photo_types.html', context=ctx)


class PhotoDetailsView(View):
    def get(self, request, id, *args, **kwargs):
        """

        :param request:
        :param id: typ sesji
        :param args:
        :param kwargs:
        :return:szczegóły danego typu sesji
        """
        try:
            detail = PhotoShootType.objects.get(pk=id)
        except PhotoShootType.DoesNotExist:
            raise Http404("No photo session found!")
        packages = Package.objects.filter(sessions=detail)
        ctx = {
            'detail': detail,
            'packages': packages
        }
        return render(request, template_name='photo_detail.html', context=ctx)


class ReservationView(LoginRequiredMixin, View):
    login_url = '/login/' #przekierowanie do strony logowania

    def get_success_url(self):
        next_url = self.request.GET.get('next', None)
        if next_url:
            return "%s" % next_url
        else:
            return reverse('main')

    def get(self, request, id):
        """

        :param request:
        :param id:
        :return:formularz rezerwacji o ile istnieje dany pakiet
        """
        try:
            package = Package.objects.get(pk=id)
        except Reservations.DoesNotExist:
            return Http404("the package does not exist")
        ctx = {
            'package': package
        }
        return render(request, template_name="reservation_form.html", context=ctx)

    def post(self, request, id):
        phone_number = request.POST.get("phone_number")
        date = request.POST.get("date")
        time = request.POST.get("time")
        comment = request.POST.get("comment")
        user_id = request.user.id
        #date = date + "-" + time
        date = "-".join([date, time])
        user = User.objects.get(pk=user_id)
        package = Package.objects.get(pk=id)
       # if all([date, user_id, package_id]):
        if date and user_id and phone_number and user and package and time:
            if len(phone_number) < 13:
                date = datetime.strptime(date, "%Y-%m-%d-%H:%M")
                reservation = Reservations.objects.create(
                    date=date,
                    user=user,
                    package=package,
                    phone_number=phone_number,
                    comment=comment
                )
                return HttpResponse("Zarezerwowano")
            else:
                ctx = {
                    'package': package,
                    'error_message': "numer telefonu nie może mieć wiecej niż 12 znaków"
                }
                return render(request, template_name="reservation_form.html", context=ctx)
        else:
            try:
                package = Package.objects.get(pk=id)
            except Reservations.DoesNotExist:
                return HttpResponse("Nie znaleziono pakietu")
            ctx = {
                'package': package,
                'error_message': "Wypełnij poprawnie wszystkie pola"
            }
            return render(request, template_name="reservation_form.html", context=ctx)


class LoginView(FormView):

    def get_success_url(self):
        next_url = self.request.GET.get('next', None)
        if next_url:
            return "%s" % next_url
        else:
            return reverse('main')

    template_name = 'login.html'
    form_class = LoginForm

    def form_valid(self, form):
        form.cleaned_data
        login(self.request, form.user)
        return HttpResponseRedirect(self.get_success_url())


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("main")


class UserCreateView(View):
    def get(self, request):
        form = UserForm
        return render(request, 'Register_users.html', {'form': form})

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main')
        else:
            ctx = {
                'error_message': "Wypełnij poprawnie wszystkie pola",
                'form': form
            }

        return render(request, 'Register_users.html', context=ctx)


class AllReservationView(SuperuserRequiredMixin, View):
    def get(self, request):
        all_reservation = Reservations.objects.all()
        ctx = {
            'all_reservation': all_reservation
        }
        return render(request, "all_reservation.html", context=ctx)


class AcceptReservationView(SuperuserRequiredMixin, View):
    def get(self, request, id):
        reservation = Reservations.objects.get(pk=id)
        reservation.status = True
        reservation.save()
        return redirect("all-reservation")


class ReservationDetailView(SuperuserRequiredMixin, DetailView):
    model = Reservations


class EditReservationView(SuperuserRequiredMixin, UpdateView):
    model = Reservations
    fields = ("date", 'user', 'package', 'phone_number', 'comment', 'status')
    success_url = "/all-reservation/"


class UserReservationsView(View):
    def get(self, request):
        user_id = request.user.id
        user = User.objects.get(pk=user_id)
        reservations = Reservations.objects.filter(user=user)


        return render(request,"user_reservations.html", {'reservations': reservations})

