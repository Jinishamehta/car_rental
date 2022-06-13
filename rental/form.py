from dataclasses import field
from django.forms import IntegerField, ModelForm
from django.contrib.auth.forms import UserCreationForm,UserModel, AuthenticationForm
from django.contrib.auth.models import User
from .models import *
from django import forms
from django.contrib.auth import authenticate, login, logout

class DateInput(forms.DateInput):
    input_type = 'date'

class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'password': forms.PasswordInput
        }
        help_texts = {
            'username':None
        }

    def clean(self):
 
        # data from the form is fetched using super function
        super(LoginForm, self).clean()
        
        username = self.cleaned_data.get('username')
        username = username.lower()
        password = self.cleaned_data.get('password')

        if not authenticate(username=username,password=password):
            self._errors['username'] = self.error_class(['Username or Password is Incorrect'])
        
        return self.cleaned_data
        
class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        help_texts = {
            'username' : None,
            'password1': None,
            'password2': None,
        }

class RegisterEmployee(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'is_superuser', 'is_staff']
        help_texts = {
            'first_name': None,
             'last_name': None, 
             'username': None, 
             'email': None, 
             'password1': None, 
             'password2': None, 
             'is_superuser': None, 
             'is_staff': None,
        }

class VehicleClassForm(ModelForm):
    class Meta:
        model = rsj_vehicle_class
        fields = '__all__'

    

class LocationForm(ModelForm):
    class Meta:
        model = rsj_location
        fields = '__all__'

    def clean(self):
 
        # data from the form is fetched using super function
        super(LocationForm, self).clean()
         
        # extract the username and text field from the data
        # location_id = self.cleaned_data.get('location_id')
        phone_no = self.cleaned_data.get('phone_no')
        pincode = self.cleaned_data.get('pincode')
      
        # conditions to be met for the username length
        if len(pincode) != 5:
            self._errors['pincode'] = self.error_class([
                '5 digit Numeric Value Required'])
        if len(phone_no) != 10:
            self._errors['phone_no'] = self.error_class([
                '10 digit valid phone number required'])
        # if len(location_id) != 5:
        #     self._errors['location_id'] = self.error_class([
        #         '5 digit Numeric Value Required'])
 
        # return any errors if found
        return self.cleaned_data

class PlanForm(ModelForm):
    class Meta:
        model = rsj_plan
        fields = '__all__'

class  DisocuntForm(ModelForm):
    class Meta:
        model = rsj_discount
        fields = '__all__'
        widgets = {
            'start_date': DateInput(),
            'end_date' : DateInput(),
        }

    def clean(self):
        super(DisocuntForm, self).clean()
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')
        
        if end_date < start_date:
            self._errors['end_date'] = self.error_class(['End Date Should Greater than Start Date'])
        return self.cleaned_data



class  CompanyForm(ModelForm):
    class Meta:
        model = rsj_company
        fields = '__all__'

class  VehicleForm(ModelForm):
    class Meta:
        model = rsj_vehicle
        fields = '__all__'

class AdminServiceForm(ModelForm):
    class Meta:
        model = rsj_service
        fields = '__all__'
        widgets = {
            'start_date': DateInput(),
            'end_date' : DateInput(),
        }

    

    def clean(self):
        super(AdminServiceForm, self).clean()
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')

        start_meter = self.cleaned_data.get('odometer_start')
        end_meter = self.cleaned_data.get('odometer_end')

        if end_meter != None:
            if end_meter < start_meter:
                self._errors['odometer_end'] = self.error_class(['End Odometer should be greater than Start Odometer'])

        if end_date < start_date:
            self._errors['end_date'] = self.error_class(['End Date Should Greater than Start Date'])

        
        return self.cleaned_data

class ServiceForm(ModelForm):
    class Meta:
        model = rsj_service
        fields = '__all__'
        exclude = ['customer_id', 'coupon_code']
        widgets = {
            'start_date': DateInput(),
            'end_date' : DateInput(),
        }

    def clean(self):
        super(ServiceForm, self).clean()
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')
        print(start_date)
        if end_date < start_date:
            self._errors['end_date'] = self.error_class(['End Date Should Greater than Start Date'])
        return self.cleaned_data

class ProfileForm(ModelForm):
    class Meta:
        model = rsj_customer
        fields = '__all__'
        exclude = ['username', 'customer_id', 'type']
    
    def clean(self):
        super(ProfileForm,self).clean()
        email = self.cleaned_data.get('email')
        try:
            if User.objects.filter(email=email).exists():
                self._errors['email'] = self.error_class([
                'already exists'])
        except User.DoesNotExist:
             self._errors['email'] = self.error_class([
                'email does not exists'])
                
        return self.cleaned_data

class CorpForm(ModelForm):
    class Meta:
        model = rsj_corp_cst
        fields = '__all__'
        exclude = ['customer']

class IndForm(ModelForm):
    class Meta:
        model = rsj_ind_cst
        fields = '__all__'
        exclude = ['customer']

class PaymentForm(ModelForm):

    class Meta:
        model = rsj_payment
        exclude = ['invoice_id']
        fields = '__all__'

        widgets = {
            'date': DateInput(),
            'exp_date' : DateInput(),
        }

    # def clean(self):
    #     super(PaymentForm, self).clean()
    #     start_date = self.cleaned_data.get('date')
    #     end_date = self.cleaned_data.get('exp_date')

    #     if end_date < start_date:
    #         self._errors['exp_date'] = self.error_class(['End Date Should Greater than Start Date'])
    #     return self.cleaned_data

class SendEmail(ModelForm):
    class Meta:
        model = User
        fields = ['email']

    def clean(self):
        super(SendEmail,self).clean()
        email = self.cleaned_data.get('email')
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
             self._errors['email'] = self.error_class([
                'email does not exists'])
                
        return self.cleaned_data
