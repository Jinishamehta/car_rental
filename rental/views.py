from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, Permission
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from .form import *
from .models import *

# Create your views here.

def loginPage(request):

    page = 'login'
    form = LoginForm()
  
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,"User Does Not Exist. Please register")

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Username or Password is incorrect')

    context = {'page':page, 'form':form}
    return render(request, 'rental/login_register.html', context)

@login_required(login_url='login')
def logoutPage(request):
    logout(request)
    return redirect('index')

def registerPage(request):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save() 
            return redirect('login')
        else:
            messages.error(request, 'An error occured during registration')

    context = {'form':form}
    return render(request, 'rental/login_register.html', context)

@login_required(login_url='login')
@permission_required('rental.add_user')
def registerEmployee(request):
    form = RegisterEmployee()
    permission = Permission.objects.get(codename='add_rsj_service')
    if request.method == 'POST':            
        form = RegisterEmployee(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save() 
            user.user_permissions.add(permission)
            return redirect('index')
        else:
            messages.error(request, 'An error occured during registration')

    context = {'form':form}
    return render(request, 'rental/login_register.html', context)
   
def index(request):
    vehicle = rsj_vehicle.objects.raw('select * from rsj_vehicle where availability = True')
    context = {'data':vehicle}
    return render(request,'rental/index.html',context)

@login_required(login_url='login')
@permission_required('rental.add_rsj_vehicle_class')
def createClass(request):
        form = VehicleClassForm()
        if request.method == 'POST':
            form = VehicleClassForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('index')

        context = {'form':form}
        return render(request,'rental/create.html', context)
    

@login_required(login_url='login')
def createLocation(request):

    if request.user.is_superuser | request.user.is_staff:
        form = LocationForm()

        if request.method == 'POST':
            form = LocationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('index')

        context = {'form':form}
        return render(request,'rental/create.html', context)
    else:
        messages.error(request, 'Access Denied')
        return redirect('index')

@login_required(login_url='login')
def createPlan(request):
    form = PlanForm()

    if request.method == 'POST':
        form = PlanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    context = {'form':form}
    return render(request,'rental/create.html', context)

@login_required(login_url='login')
def createDiscount(request):
    form = DisocuntForm()
    if request.method == 'POST':
        form = DisocuntForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    

    context = {'form':form}
    return render(request,'rental/create.html', context)

@login_required(login_url='login')
def createCompany(request):
    form  = CompanyForm()
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    context = {'form':form}
    return render(request,'rental/create.html', context)

@login_required(login_url='login')
def createVehicle(request):
    form = VehicleForm()
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    context = {'form':form}
    return render(request,'rental/create.html', context)

def createInd(request):
    form = IndForm()
    if request.method == 'POST':
        form = IndForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    context = {'form':form}
    return render(request,'rental/create.html', context)

def createCorp(request):
    form = CorpForm()
    if request.method == 'POST':
        form = CorpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')    

    context = {'form':form}
    return render(request,'rental/create.html', context)

@login_required(login_url='login')
def createInvoice(request):
    form = InvoiceForm()
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    context = {'form':form}
    return render(request,'rental/create.html', context)

@login_required(login_url='login')
def createSerivce(request):
    form = ServiceForm()
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    context = {'form':form}
    return render(request,'rental/create.html', context)



@login_required(login_url='login')
def createPayment(request):
    form = PaymentForm()
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    context = {'form':form}
    return render(request,'rental/create.html', context)

