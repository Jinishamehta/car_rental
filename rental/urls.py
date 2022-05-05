from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login',views.loginPage, name='login'),
    path('logout',views.logoutPage, name='logout'),
    path('create_class', views.createClass, name='create_class'),
    path('create_location', views.createLocation, name='create_location'),
    path('create_discount', views.createDiscount, name='create_discount'),
    path('create_plan', views.createPlan, name='create_plan'),
    path('create_customer_ind', views.createInd, name='create_customer_ind'),
    path('create_customer_corp', views.createCorp, name='create_customer_corp'),
    path('create_company', views.createCompany, name='create_company'),
    path('create_invoice', views.createInvoice, name='create_invoice'),
    path('create_service', views.createSerivce, name='create_service'),
    path('create_vehicle', views.createVehicle, name='create_vehicle'),
    path('create_payment', views.createPayment, name='create_payment'),
    path('register',views.registerPage,name='register_user'),
    path('register_employee', views.registerEmployee, name='register_employee'),
]