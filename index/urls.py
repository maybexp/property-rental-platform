from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.index, name="index"),
    path('privatlivspolitik', views.privacyPolicy, name="privacyPolicy"),
    path('om-os', views.about, name="about"),
    path('kontakt', views.contact, name="contact"),
    path('opret-bruger', views.signup, name="signup"),
    path('kundeservice', views.customerService, name="customerService"),
    path('opret-bolig-annonce', views.createHousingPost, name="createHousingPost"),
    path('tips-til-en-sikker-bolighandel', views.tipsTilEnSikkerBolighandel, name="tipsTilEnSikkerBolighandel"),
    path('anmeld-snyd', views.anmeldSnyd, name="anmeldSnyd"),

    path('lejebolig/<int:rentalApartmentId>', views.rentalApartment, name='rentalApartment'),
    path('lejebolig/<str:cityName>', views.search, name='search'),
    path('lejebolig/', views.search, name='searchUsingInput'),

    #User
    path('log-ind', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('login_view', views.login_view, name='login_view'),
    path('min-konto', views.myAccount, name='myAccount'),
    path('logget-ud', views.loggedOut, name='loggedOut'),

    path('bolig-opsat', views.boligOpsat, name='boligOpsat'),
    path('vilkaar', views.vilkaar, name='vilkaar'),
    path('opdateringer', views.opdateringer, name='opdateringer'),

    #These only redirect
    path('updateUserInfo', views.updateUserInfo, name='updateUserInfo'),
    path('addApartment', views.addApartment, name='addApartment'),
    path('createUser', views.createUser, name='createUser'),

    #Test
    path('test/<str:cityName>', views.test),

    #Ajax
    path('ajax/endpoint/', views.ajax_view, name='ajax_endpoint'),
    path('save-apartment-ajax/<str:apartmentId>', views.saveApartmentAjax, name='saveApartmentAjax'),
    path('report-rental-apartment-ajax/<str:apartmentId>', views.report_rental_apartment_ajax, name='reportRentalApartmentAjax'),

    #Delete on launch
    path('404', views.error404, name='error404'),
]