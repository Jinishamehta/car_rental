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
from django.db import connection
from django.utils import timezone
from .permission import employee_permission, customer_permission


# Create your views here.
def loginPage(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Username or Password is incorrect')

    context = {'form':form}
    return render(request, 'rental/login.html', context)

@login_required(login_url='login')
def logoutPage(request):
    logout(request)
    return redirect('index')

def registerPage(request):
    form = RegisterForm()
    permission = Permission.objects.filter(codename__in=customer_permission).all()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            user_group, created = Group.objects.get_or_create(name='customer')
            user.groups.add(user_group)
            user_group.permissions.set(permission)
            if not request.user.is_staff:
                login(request, user)
                return redirect('create_profile')
            else:
                return redirect('create_customer',id=user.id)
                # return render(request,'rental/create.html', {'username':user.username})
        else:
            messages.error(request, 'An error occured during registration')

    context = {'form':form, 'title':'Register Customer'}
    return render(request, 'rental/register.html', context)

@login_required(login_url='login')
@permission_required('rental.add_user')
def registerEmployee(request):
    form = RegisterEmployee()
    
    # permissions = ['add_rsj_service', 'change_rsj_service']
    permission = Permission.objects.filter(codename__in=employee_permission).all()

    if request.method == 'POST':            
        form = RegisterEmployee(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user_group, created = Group.objects.get_or_create(name='staff')
            user.is_staff = True
            user.save()
            user.groups.add(user_group)
            user_group.permissions.set(permission)
            return redirect('index')
        else:
            messages.error(request, 'An error occured during registration')

    context = {'form':form, 'title':'Register Employee'}
    return render(request, 'rental/register.html', context)

def index(request):
    context = {'data':"Welcome TO Wow"}
    return render(request,'rental/index.html',context)

@login_required(login_url='login')
@permission_required('rental.add_rsj_vehicle_class')
def createClass(request):
    form = VehicleClassForm()
    if request.method == 'POST':
        form = VehicleClassForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('class_page')

    context = {'form':form, 'title': 'New Class'}
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
    context = {'form' : form, 'title': 'Update Class'}
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

def listClass(request):
    data = rsj_vehicle_class.objects.raw('select * from rsj_vehicle_class')
    context = {'data':data}
    return render(request,'rental/vehicle_class.html',context)

@login_required(login_url='login')
def createLocation(request):

    if request.user.is_superuser | request.user.is_staff:
        form = LocationForm()

        if request.method == 'POST':
            form = LocationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('location_page')

        context = {'form':form, 'title': 'New Location'}
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
    context = {'form' : form, 'title': 'Update Location'}
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

def listLocation(request):
    data = rsj_location.objects.raw('select * from rsj_location')
    context = {'data':data}
    return render(request,'rental/location.html',context)

@login_required(login_url='login')
def createVehicle(request):
    form = VehicleForm()
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vehicle_page')
    context = {'form':form, 'title': 'New Vehicle'}
    return render(request,'rental/create.html', context)

def updateVehicle(request, pk):
    data = rsj_vehicle.objects.get(lpn=pk)
    form = VehicleForm(instance=data)

    if request.method == 'POST':
        form = VehicleForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return redirect('vehicle_page')
    context = {'form' : form, 'title': 'Update Vehicle'}
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

def listVehicle(request):
    data = rsj_vehicle.objects.raw('select * from rsj_vehicle')
    context = {'data':data}
    return render(request,'rental/vehicle.html',context)

@login_required(login_url='login')
def createPlan(request):
    form = PlanForm()
    if request.method == 'POST':
        form = PlanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('plan_page')
    context = {'form':form, 'title': 'New Plan'}
    return render(request,'rental/create.html', context)

def updatePlan(request, pk):
    data = rsj_plan.objects.get(plan_id=pk)
    form = PlanForm(instance=data)

    if request.method == 'POST':
        form = PlanForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return redirect('plan_page')
    context = {'form' : form, 'title': 'Update Plan'}
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

def listPlan(request):
    data = rsj_plan.objects.raw('select * from rsj_plan')
    context = {'data':data}
    return render(request,'rental/plan.html',context)

@login_required(login_url='login')
def createDiscount(request):
    form = DisocuntForm()
    if request.method == 'POST':
        form = DisocuntForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('discount_page')
    context = {'form':form, 'title': 'Add Coupon'}
    return render(request,'rental/create.html', context)

def updateDiscount(request, pk):
    data = rsj_discount.objects.get(coupon_code=pk)
    form = DisocuntForm(instance=data)

    if request.method == 'POST':
        form = DisocuntForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return redirect('discount_page')
    context = {'form' : form, 'title': 'Update Coupon'}
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

def listDiscount(request):
    data = rsj_discount.objects.raw('select * from rsj_discount')
    context = {'data':data}
    return render(request,'rental/discount.html',context)

@login_required(login_url='login')
def createCompany(request):
    form  = CompanyForm()
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('company_page')
    context = {'form':form, 'title': 'New Company'}
    return render(request,'rental/create.html', context)

def updateCompany(request,pk):
    data = rsj_company.objects.get(company_reg_no=pk)
    form  = CompanyForm(instance=data)
    if request.method == 'POST':
        form = CompanyForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return redirect('company_page')
    context = {'form':form, 'title': 'Update Company'}
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

def listCompany(request):
    data = rsj_company.objects.raw('select * from rsj_company')
    context = {'data':data}
    return render(request,'rental/company.html',context)

def createCustEmp(request, id):
    form = ProfileForm()
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.username = User.objects.get(id=id)
            profile.save()
            if profile.customer_type == 'I':
                return redirect('create_customer_ind',id=profile.customer_id)
            else:
                return redirect('create_customer_corp',id=profile.customer_id)
    context = {'form' : form, 'title': 'New Customer'}
    return render(request,'rental/create.html', context)

def createCustomer(request):
    form = ProfileForm()
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.username = User.objects.get(username=request.user.username)
            profile.username.first_name = profile.first_name
            profile.username.last_name = profile.last_name
            profile.username.email = profile.email
            profile.username.save()
            profile.save()
            if profile.customer_type == 'I':
                return redirect('create_customer_ind',id=profile.customer_id)
            else:
                return redirect('create_customer_corp',id=profile.customer_id)
    context = {'form' : form, 'title': 'New Customer'}
    return render(request,'rental/create.html', context)

def createInd(request,id):
    form = IndForm()
    if request.method == 'POST':
        form = IndForm(request.POST)
        if form.is_valid():
            indprofile = form.save(commit=False)
            indprofile.customer_id = id
            indprofile.save()
        return redirect('index')
    context = {'form':form, 'title': 'Individual'}
    return render(request,'rental/create.html', context)

def createCorp(request, id):
    form = CorpForm()
    if request.method == 'POST':
        form = CorpForm(request.POST)
        if form.is_valid():
            corpprofile = form.save(commit=False)
            corpprofile.customer_id = id
            corpprofile.save()
            return redirect('index')    

    context = {'form':form, 'title': 'Corporate'}
    return render(request,'rental/create.html', context)

def listCustomer(request):
    data = rsj_customer.objects.all()
    context = {'data':data}
    return render(request,'rental/customer.html',context)

@login_required(login_url='login')
def createSerivce(request):
    if request.user.is_staff:
        form = AdminServiceForm()
    else:
        form = ServiceForm()
    if request.method == 'POST':
        if request.user.is_staff:
            form = AdminServiceForm(request.POST)
        else:
            form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            if not request.user.is_staff:
                service.customer_id = rsj_customer.objects.get(username=request.user)
                coupon_code = request.POST.get('coupon')
                if coupon_code:
                    couponobj = rsj_discount.objects.get(coupon_code = coupon_code)
                    service.coupon_code = couponobj
            service.save()
            return redirect('home')

    context = {'form' : form, 'title': 'Book Service' }
    return  render(request,'rental/create_service.html', context)

def updateSerivce(request, pk):
    data = rsj_service.objects.get(service_id=pk)
    if request.user.is_staff:
        form = AdminServiceForm(instance=data)
    else:
        form = ServiceForm(instance=data)

    if request.method == 'POST':
        if request.user.is_staff:
            form = AdminServiceForm(request.POST, instance=data)
        else:
            form = ServiceForm(request.POST,instance=data)
        if form.is_valid():
            service = form.save(commit=False)
            if not request.user.is_staff:
                service.customer_id = rsj_customer.objects.get(username=request.user)
                coupon_code = request.POST.get('coupon')
                if coupon_code:
                    couponobj = rsj_discount.objects.get(coupon_code = coupon_code)
                    service.coupon_code = couponobj
            service.save()
            return redirect('home')

    context = {'form' : form, 'title': 'Book Service' }
    return  render(request,'rental/create_service.html', context)

def listService(request):
    data = rsj_service.objects.raw('select * from rsj_service')
    context = {'data':data}
    return render(request,'rental/service.html',context)

@login_required(login_url='login')
def generateInvoice(request, var1, var2):
    if int(var1) in list(rsj_invoice.objects.all().values_list('service_id', flat=True)):
        total = rsj_invoice.objects.all().get(service_id = var1).amount
        print("if record exists ", total)
    else:
        serviceobj = rsj_service.objects.all().get(service_id = var1)
        if request.user.is_staff:
            user = serviceobj.customer_id.customer_id
            custobj = rsj_customer.objects.get(customer_id = user)
        else:
            user = request.user.id
            custobj = rsj_customer.objects.get(username = user)
        # print(user)
        
        custtype = custobj.customer_type
        custno = custobj.customer_id
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
        today = timezone.now()
        
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
            regno = corpcustobj.reg_no.company_reg_no
            companyobj = rsj_company.objects.get(company_reg_no = regno)
            corpdiscount = companyobj.discount_rate
            total = total - total*corpdiscount/100  
        elif custtype == "I":
            if var2 != '0':
                inddiscobj = rsj_discount.objects.get(coupon_code = var2)
                discount = inddiscobj.rate
                startval = inddiscobj.val_start
                endval = inddiscobj.val_end
                print(total)
                if inddiscobj.status == 'Y' and startval <= today <= endval: 
                    total = total - total*discount/100
                    print(total)
                    rsj_discount.objects.filter(coupon_code = var2).update(status='N')
                else:
                    total=total
            else:
                total = total

        if serviceid not in list(rsj_invoice.objects.all().values_list('service_id', flat=True)) :
            i = rsj_invoice(invoice_id = serviceid, service_id = serviceobj, amount = total, pendng_amt = total)
            i.save()
            if request.user.is_staff:
                return redirect('invoice_page')
    
    invoiceobj = rsj_invoice.objects.all().get(service_id = var1)
    invoiceid = invoiceobj.invoice_id
    # context = {'total' : total, 'invoiceid' : invoiceid}
    context = {'data':invoiceobj,'total' : total}
    return render(request, 'invoice.html', context)

def listInvoice(request):
    data = []
    # if request.user.is_staff:
    data = rsj_invoice.objects.raw('select * from rsj_invoice')
    # else:
    #     cust_id = rsj_customer.objects.get(username=request.user.id)
    #     service_obj = rsj_service.objects.filter(customer_id = cust_id.customer_id)
    #     for obj in service_obj:
    #         data.append(rsj_invoice.objects.get(service_id = obj.service_id))
    
            # data = rsj_invoice.objects.get(service_id = service_obj.service_id)
    context = {'data':data}
    return render(request,'rental/invoice.html',context)

def makePayment(request,var1):
    form = PaymentForm()
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            # invoiceobj = rsj_invoice.objects.filter(invoice_id = var1)
            payment.invoice_id_id = var1
            payment.save()
            rsj_invoice.objects.filter(invoice_id = var1).update(pendng_amt = F('pendng_amt') - payment.amount)
            return redirect('home')
    
    return render(request, 'rental/payment.html', {'form': form, 'title': 'Payment'})

def listPayment(request):
    data = rsj_payment.objects.raw('select * from rsj_payment')
    context = {'data':data}
    return render(request,'rental/payment.html',context)

def listEmployee(request):
    rental_user = get_user_model()
    data = rental_user.objects.raw('select * from auth_user where is_staff = 1')
    context = {'data':data}
    return render(request,'rental/employee.html',context)

def home(request):
    return render(request, 'home.html')

def show(request):
    if not request.user.is_staff:
        return render(request, "not allowed")
    else:
     service_type = rsj_plan.objects.all()
     return render(request,'home.html',{'service_type':service_type})

def display(request):
    context = {}
    if request.user.is_staff:
        service = rsj_service.objects.order_by('start_date')
        context = {'data':service}
        return render(request,'rental/service.html', context)
    user = request.user.id
    print(user)
    custid = rsj_customer.objects.get(username = user)
    custno = custid.customer_id
    service = rsj_service.objects.filter(customer_id=custno)
    context = {'user':user, 'custno' : custno, 'data' : service}
    return render(request,'rental/service.html', context)
    # return render(request,'display.html', {'user':user, 'custno' : custno, 'service' : service})

def analysis(request):
    query = "select a.location_id,a. city, b.start_location,count(c.service_id), sum(amount) from rsj_location a join rsj_service b on a.location_id = b.start_location join rsj_invoice c on b.service_id = c.service_id group by a.location_id;"
    with connection.cursor() as cursor:
        cursor.execute(query)
        loctotal = cursor.fetchall()


    query = "select a.location_id,a.city, b.service_type, count(b.service_id), sum(c.amount) from rsj_location a join (select * from rsj_service where service_type = 2) b on a.location_id=b.start_location join rsj_invoice c on b.service_id = c.service_id group by b.start_location UNION select a.location_id,a.city, b.service_type, count(b.service_id), sum(c.amount) from rsj_location a join (select * from rsj_service where service_type = 1) b on a.location_id=b.start_location join rsj_invoice c on b.service_id = c.service_id group by b.start_location"
    with connection.cursor() as cursor:
        cursor.execute(query)
        locpremium = cursor.fetchall()

    query = "select a.location_id,a.city, count(b.service_id), sum(c.amount) from rsj_location a join (select * from rsj_service where service_type = 1) b on a.location_id=b.start_location join rsj_invoice c on b.service_id = c.service_id group by b.start_location;"
    with connection.cursor() as cursor:
        cursor.execute(query)
        locregular = cursor.fetchall()

    query = "select service_id, customer_id, odometer_end - odometer_start 'distance' from rsj_service order by distance desc limit 5;"
    with connection.cursor() as cursor:
        cursor.execute(query)
        top5dist = cursor.fetchall()

    query = "with temptable(class_id, class_name, vin) as (select a.class_id, a.name, b.vin from rsj_vehicle_class a join rsj_vehicle b on a.class_id = b.class_id) select a.class_id, a.class_name, count(b.service_id) from temptable a join rsj_service b on a.vin = b.vin group by a.class_id;"
    with connection.cursor() as cursor:
        cursor.execute(query)
        classservice = cursor.fetchall()


    return render(request, 'rental/analysis.html', {'loctotal' : loctotal, 'locpremium' : locpremium, 'locregular' : locregular, 'top5dist' : top5dist, 'classservice' : classservice})

def forgotPassoword(request):
    form = SendEmail()
    if request.method == 'POST':
        form = SendEmail(request.POST)
        if form.is_valid():
            return render(request, 'rental/password_reset_done.html')
    context = {'form':form}
    return render(request, 'rental/password_reset_form.html',context)
