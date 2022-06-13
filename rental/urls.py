from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('analysis/',views.analysis, name='analysis_page'),
    path('login',views.loginPage, name='login'),
    path('logout',views.logoutPage, name='logout'),

    path('', views.index, name='index'),

    path('register',views.registerPage,name='register_user'),
    path('register_employee', views.registerEmployee, name='register_employee'),

    path('create_customer/<id>',views.createCustEmp, name="create_customer"),

    path('create_profile', views.createCustomer, name="create_profile"),
    path('create_customer_ind/<id>', views.createInd, name='create_customer_ind'),
    path('create_customer_corp/<id>', views.createCorp, name='create_customer_corp'),
    
    path('view_customer', views.listCustomer, name="customer_page"),
    path('view_employee',views.listEmployee,name='employee_page'),

    # path('create_invoice', views.createInvoice, name='create_invoice'),
    path('create_service', views.createSerivce, name='create_service'),

   
    # path('create_payment', views.createPayment, name='create_payment'),
   
    path('view_service',views.display,name='service_page'),
     path('update_service/<str:pk>/',views.updateSerivce,name='update_service'),
    # path('delete_service/<str:pk>/',views.deleteClass,name='delete_class'),
    
    path('invoice/<var1>/<var2>', views.generateInvoice, name='invoice'),
    path('view_invoice',views.listInvoice,name='invoice_page'),
    path('view_payment',views.listPayment,name='payment_page'),
    
    path('create_class', views.createClass, name='create_class'),
    path('view_class',views.listClass,name='class_page'),
    path('update_class/<str:pk>/',views.updateClass,name='update_class'),
    path('delete_class/<str:pk>/',views.deleteClass,name='delete_class'),

    path('create_location', views.createLocation, name='create_location'),
    path('view_location',views.listLocation,name='location_page'),
    path('update_location/<str:pk>/',views.updateLocation,name='update_location'),
    path('delete_location/<str:pk>/',views.deleteLocation,name='delete_location'),

    path('create_vehicle', views.createVehicle, name='create_vehicle'),
    path('view_vehicle',views.listVehicle,name='vehicle_page'),
    path('update_vehicle/<str:pk>/',views.updateVehicle,name='update_vehicle'),
    path('delete_vehicle/<str:pk>/',views.deleteVehicle,name='delete_vehicle'),

    path('create_discount', views.createDiscount, name='create_discount'),
    path('view_discount',views.listDiscount,name='discount_page'),
    path('update_discount/<str:pk>/',views.updateDiscount,name='update_discount'),
    path('delete_discount/<str:pk>/',views.deleteDiscount,name='delete_discount'),


    path('create_plan', views.createPlan, name='create_plan'),
    path('view_plan',views.listPlan,name='plan_page'),
    path('update_plan/<str:pk>/',views.updatePlan,name='update_plan'),
    path('delete_plan/<str:pk>/',views.deletePlan,name='delete_plan'),

    path('create_company', views.createCompany, name='create_company'),
    path('view_company',views.listCompany,name='company_page'),
    path('update_company/<str:pk>/',views.updateCompany,name='update_company'),
    path('delete_company/<str:pk>/',views.deleteCompany,name='delete_company'),


    path('', views.home, name="home"),
    path('show', views.show),
    # path('service', views.service, name="service"),
    # path('register', views.RegisterUser, name="register"),
    #  path('prereg', views.prereg, name="prereg"),
    path('display', views.display, name="display"),
    # path('invoice/<var1>/<var2>', views.generateInvoice, name='invoice'),
    path('payment/<var1>', views.makePayment, name="payment"),

     # path('create_customer_ind/<id>', views.createInd, name="create-ind-profile"),
    # path('create_customer_corp/<id>', views.createcorpprofile, name="create-corp-profile"),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='rental/password_reset.html'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='rental/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='rental/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='rental/password_reset_complete.html'
         ),
         name='password_reset_complete'), 
]