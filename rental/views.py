from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import Permission, Group, User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import get_user_model
from .form import *
from .models import *
from django.db.models import Q, F


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
            my_group = Group.objects.get(name='customer')
            my_group
            my_group.user_set.add(user)
            return redirect('login')
        else:
            messages.error(request, 'An error occured during registration')

    context = {'form':form}
    return render(request, 'rental/login_register.html', context)

# @login_required(login_url='login')
# @permission_required('rental.add_user')
def registerEmployee(request):
    form = RegisterEmployee()
    codename = ['add_rsj_service', 'edit_rsj_service', 'de']
    permission = Permission.objects.get(codename='add_rsj_service')
    if request.method == 'POST':            
        form = RegisterEmployee(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save() 
            my_group = Group.objects.get(name='customer')
            my_group.user_set.add(user)
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
@permission_required('rental.change_rsj_vehicle_class')
def updateClass(request, pk):
    data  = rsj_vehicle_class.objects.get(class_id=pk)
    form = VehicleClassForm(instance=data)

    if request.method == "POST":
        form = VehicleClassForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return redirect('class_page')
    context = {'form' : form}
    return render(request, 'rental/create.html', context)

@login_required(login_url='login')
@permission_required('rental.delete_rsj_vehicle_class')
def deleteClass(request, pk):
    data = rsj_vehicle_class.objects.get(class_id=pk)
    if request.method == 'POST':
        vehicle = rsj_vehicle.objects.filter(class_id=pk).exists()
        if (vehicle is not None):
             messages.error(request, "Vehicle of this class exists")
        else:
            data.delete()
        return redirect('class_page')
    return render(request, 'rental/delete.html', {'obj':data})
    

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
@permission_required('rental.change_rsj_locaiton')
def updateLocation(request, pk):
    data  = rsj_location.objects.get(location_id=pk)
    form = LocationForm(instance=data)

    if request.method == "POST":
        form = LocationForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return redirect('location_page')
    context = {'form' : form}
    return render(request, 'rental/create.html', context)

@login_required(login_url='login')
@permission_required('rental.delete_rsj_location')
def deleteLocation(request, pk):
    data = rsj_location.objects.get(location_id=pk)
    if request.method == 'POST':
        vehicle = rsj_vehicle.objects.filter(location_id=pk).exists()
        if (vehicle):
             messages.error(request, "Vehicle exists at this location change the locaiton of vehicle then delete the location")
        else:
            data.delete()
        return redirect('location_page')
    return render(request, 'rental/delete.html', {'obj':data})

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

def updateVehicle(request, pk):
    data = rsj_vehicle.objects.get(lpn=pk)
    form = VehicleForm(instance=data)

    if request.method == 'POST':
        form = VehicleForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return redirect('vehicle_page')
    context = {'form' : form}
    return render(request, 'rental/create.html', context)

def deleteVehicle(request,pk):
    data = rsj_vehicle.objects.get(lpn=pk)
    if request.method == 'POST':
        is_parent = rsj_service.objects.filter(vin=data.vin).exists()
        if is_parent:
            messages.error(request,"Vehicle is in service")
        else:
            data.delete()
        return redirect('vehicle_page')
    return render(request, 'rental/delete.html', {'obj':data})

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

def updatePlan(request, pk):
    data = rsj_plan.objects.get(plan_id=pk)
    form = PlanForm(instance=data)

    if request.method == 'POST':
        form = PlanForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return redirect('plan_page')
    context = {'form' : form}
    return render(request, 'rental/create.html', context)

def deletePlan(request,pk):
    data = rsj_plan.objects.get(plan_id=pk)
    if request.method == 'POST':
        is_parent = rsj_service.objects.filter(plan_id=pk).exists()
        if is_parent:
            messages.error(request,"Plan is in service")
        else:
            data.delete()
        return redirect('plan_page')
    return render(request, 'rental/delete.html', {'obj':data})

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

def updateDiscount(request, pk):
    data = rsj_discount.objects.get(coupon_code=pk)
    form = DisocuntForm(instance=data)

    if request.method == 'POST':
        form = DisocuntForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return redirect('discount_page')
    context = {'form' : form}
    return render(request, 'rental/create.html', context)

def deleteDiscount(request,pk):
    data = rsj_discount.objects.get(coupon_code=pk)
    if request.method == 'POST':
        is_parent = rsj_service.objects.filter(
            Q(coupon_code =pk) & Q(end_meter = None)
        ).exists()
        if is_parent:
            messages.error(request,"Disocunt is in service")
        else:
            data.delete()
        return redirect('discount_page')
    return render(request, 'rental/delete.html', {'obj':data})

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

def updateCompany(request,pk):
    data = rsj_company.objects.get(company_reg_no=pk)
    form  = CompanyForm(instance=data)
    if request.method == 'POST':
        form = CompanyForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return redirect('company_page')
    context = {'form':form}
    return render(request,'rental/create.html', context)

def deleteCompany(request,pk):
    data = rsj_company.objects.get(company_reg_no=pk)
    if request.method == 'POST':
        is_parent = rsj_corp_cst.objects.filter(company_reg_no=pk).exists()
        if is_parent:
            messages.error(request,"Employee is in service")
        else:
            data.delete()
        return redirect('company_page')

    return render(request,'rental/delete.html', {'obj':data})

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

# @login_required(login_url='login')
# def createInvoice(request):
#     form = InvoiceForm()
#     if request.method == 'POST':
#         form = InvoiceForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('index')
#     context = {'form':form}
#     return render(request,'rental/create.html', context)

# @login_required(login_url='login')
# def createSerivce(request):
#     form = ServiceForm()
#     if request.method == 'POST':
#         form = ServiceForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('index')
#     context = {'form':form}
#     return render(request,'rental/create.html', context)



# @login_required(login_url='login')
# def createPayment(request):
#     form = PaymentForm()
#     if request.method == 'POST':
#         form = PaymentForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('index')
#     context = {'form':form}
#     return render(request,'rental/create.html', context)

def listCustomer(request):
    data = rsj_customer.objects.raw('select * from rsj_customer')
    context = {'data':data}
    return render(request,'rental/customer.html',context)

def listClass(request):
    data = rsj_vehicle_class.objects.raw('select * from rsj_vehicle_class')
    context = {'data':data}
    return render(request,'rental/vehicle_class.html',context)

def listVehicle(request):
    data = rsj_vehicle.objects.raw('select * from rsj_vehicle')
    context = {'data':data}
    return render(request,'rental/vehicle.html',context)

def listLocation(request):
    data = rsj_location.objects.raw('select * from rsj_location')
    context = {'data':data}
    return render(request,'rental/location.html',context)

def listDiscount(request):
    data = rsj_discount.objects.raw('select * from rsj_discount')
    context = {'data':data}
    return render(request,'rental/discount.html',context)

def listService(request):
    data = rsj_service.objects.raw('select * from rsj_service')
    context = {'data':data}
    return render(request,'rental/service.html',context)

def listPlan(request):
    data = rsj_plan.objects.raw('select * from rsj_plan')
    context = {'data':data}
    return render(request,'rental/plan.html',context)

def listInvoice(request):
    data = rsj_invoice.objects.raw('select * from rsj_invoice')
    context = {'data':data}
    return render(request,'rental/invoice.html',context)

def listPayment(request):
    data = rsj_payment.objects.raw('select * from rsj_payment')
    context = {'data':data}
    return render(request,'rental/payment.html',context)

def listCompany(request):
    data = rsj_company.objects.raw('select * from rsj_company')
    context = {'data':data}
    return render(request,'rental/company.html',context)

def listEmployee(request):
    rental_user = get_user_model()
    data = rental_user.objects.raw('select * from rental_user where is_staff = 1')
    context = {'data':data}
    return render(request,'rental/employee.html',context)


def RegisterUser(request):
    page = 'register'
    form = UserCreationForm
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            #user.is_staff=True
            user.save()
            login(request, user)
            return redirect('prereg') #create-profile instead of prereg
        else:
            messages.error(request, 'An error occurred')
        
    return render(request, 'login_registration.html', {'form' : form})

def prereg(request):
    if request.method == 'POST':
        type = request.POST.get('csttype')
        context = { 'type' : type }
        if type == 'C':
            return redirect('create-corp-profile')
        elif type == 'I':
            return redirect('create-ind-profile')
    return render(request, 'preRegistration.html')

def home(request):
    return render(request, 'home.html')

def show(request):
    if not request.user.is_staff:
        return render(request, "not allowed")
    else:
     service_type = rsj_plan.objects.all()
     return render(request,'home.html',{'service_type':service_type})

@login_required(login_url='login')
def service(request):
    form=ServiceForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            service = form.save(commit=False)
            custid = rsj_customer.objects.get(username=request.user)
            service.customer = custid
            couponcode = request.POST.get('coupon')
            if couponcode:
                couponobj = rsj_discount.objects.get(coupon_code = couponcode)
                service.coupon_code = couponobj
            service.save()
            return redirect('home')

    context = {'form' : form }
    return  render(request, 'newService.html', context)
    

def createindprofile(request):
    form = ProfileForm(request.POST)
    form2 = IndForm(request.POST)
    type = 'I'
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        form2 = IndForm(request.POST)
        if form.is_valid() and form2.is_valid() :
            profile = form.save(commit=False)
            profile.username = User.objects.get(username=request.user.username)
            profile.type = type
            profile.save()
            indprofile = form2.save(commit=False)
            indprofile.customer = profile
            indprofile.save()

            return redirect('home')
    
    context = {'form' : form, 'form2' : form2, 'type' : type }
    return  render(request, 'newProfile.html', context)

def createcorpprofile(request):
    form = ProfileForm(request.POST)
    form1 = CorpForm(request.POST)
    type = 'C'
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        form1 = CorpForm(request.POST)
        if form.is_valid() and form1.is_valid() :
            profile = form.save(commit=False)
            profile.username = User.objects.get(username=request.user.username)
            profile.type = type
            profile.save()
            corpprofile = form1.save(commit=False)
            corpprofile.customer = profile
            corpprofile.save()

            return redirect('home')
    
    context = {'form' : form, 'form1' : form1, 'type' : type }
    return  render(request, 'newProfile.html', context)

def display(request):
    user = request.user.id
    custid = rsj_customer.objects.all().get(username__id = user)
    custno = custid.customer_id
    service = rsj_service.objects.filter(customer_id=custno)
    return render(request,'display.html', {'user':user, 'custno' : custno, 'service' : service})


def invoice(request, var1, var2):
    print(var2)
    print(var1)
    user = request.user.id
    custobj = rsj_customer.objects.all().get(username__id = user)
    custtype = custobj.type
    custno = custobj.customer_id
    serviceobj = rsj_service.objects.all().get(service_id = var1)
    serviceid = serviceobj.service_id
    servicetype = serviceobj.service_type.name
    typeobj = rsj_plan.objects.get(name=servicetype)
    premiumcost = typeobj.cost
    startodo = serviceobj.odometer_start
    endodo = serviceobj.odometer_end
    startdate = serviceobj.start_date
    enddate = serviceobj.end_date
    vinno = serviceobj.vin.vin
    vehicleobj = rsj_vehicle.objects.all().get(vin=vinno)
    vehicleclass = vehicleobj.class_id.class_id
    vehicleClassobj = rsj_vehicle_class.objects.get(class_id=vehicleclass)
    dailylim = vehicleClassobj.daily_limit
    rateperday = vehicleClassobj.rate_per_day
    overmilfee = vehicleClassobj.over_mileage_fee
    days = enddate-startdate
    total = 0
    
    print(days.days)
    if (endodo-startodo) < days.days*(dailylim):
        total = total + rateperday * days.days
    else:
        if servicetype == "premium":
            total = total + premiumcost
        else:
            diff = (endodo-startodo) - (days.days*dailylim)
            total = total + (rateperday*days.days) + (overmilfee*diff) 

    if custtype == "C":
        corpcustobj = rsj_corp_cst.objects.get(customer_id = custno)
        regno = corpcustobj.reg_no.reg_no
        companyobj = rsj_company.objects.get(reg_no = regno)
        corpdiscount = companyobj.discount_rate
        total = total - total*corpdiscount/100  
    elif custtype == "I":
        if var2 != '0':
            inddiscobj = rsj_discount.objects.get(coupon_code = var2)
            discount = inddiscobj.rate
            startval = inddiscobj.val_start
            endval = inddiscobj.val_end
            print(total)
            if inddiscobj.status == 'Y': 
                total = total - total*discount/100
                print(total)
                rsj_discount.objects.filter(coupon_code = var2).update(status='N')
            else:
                total=total
        else:
            total = total

    if serviceid not in list(rsj_invoice.objects.all().values_list('service_id', flat=True)) :
        i = rsj_invoice(invoice_id = serviceid, service = serviceobj, amount = total, pendng_amt = total)
        i.save()
    invoiceobj = rsj_invoice.objects.all().get(service_id = serviceid)
    invoiceid = invoiceobj.invoice_id
    print(total)
    context = {'total' : total, 'invoiceid' : invoiceid}
    return render(request, 'invoice.html', context)

def payment(request,var1):
    form = PaymentForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            payment = form.save(commit=False)
            payment.invoice_id = var1
            payment.save()
            rsj_invoice.objects.filter(invoice_id = var1).update(pendng_amt = F('pendng_amt') - payment.amount)
            return redirect('home')
    
    return render(request, 'payment.html', {'form': form})