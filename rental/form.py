from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from django import forms

class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        
class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

class RegisterEmployee(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'is_superuser', 'is_staff']

class VehicleClassForm(ModelForm):
    class Meta:
        model = rsj_vehicle_class
        fields = '__all__'

class LocationForm(ModelForm):
    class Meta:
        model = rsj_location
        fields = '__all__'

class PlanForm(ModelForm):
    class Meta:
        model = rsj_plan
        fields = '__all__'

class  DisocuntForm(ModelForm):
    class Meta:
        model = rsj_discount
        fields = ['coupon_code', 'rate', 'start_date', 'end_date']

    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError('Start date is after end date')

# class  IndForm(ModelForm):
#     class Meta:
#         model = RsjIndCst
#         fields = '__all__'

# class  CorpForm(ModelForm):
#     class Meta:
#         model = RsjCorpCst
#         fields = '__all__'

class  CompanyForm(ModelForm):
    class Meta:
        model = rsj_company
        fields = '__all__'

# class  InvoiceForm(ModelForm):
#     class Meta:
#         model = rsj_invoice
#         fields = '__all__'

# class  ServiceForm(ModelForm):
#     class Meta:
#         model = rsj_service
#         fields = '__all__'

class  VehicleForm(ModelForm):
    class Meta:
        model = rsj_vehicle
        fields = '__all__'

# class  PaymentForm(ModelForm):
#     class Meta:
#         model = rsj_payment
#         fields = '__all__'

class DateInput(forms.DateInput):
    input_type = 'date'

class ServiceForm(ModelForm):
    class Meta:
        model = rsj_service
        fields = '__all__'
        exclude = ['customer', 'coupon_code']
        widgets = {
            'start_date': DateInput(),
            'end_date' : DateInput(),
        }

class ProfileForm(ModelForm):
    class Meta:
        model = rsj_customer
        fields = '__all__'
        exclude = ['username', 'customer_id', 'type']


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
        exclude = ['invoice']
        fields = '__all__'
        widgets = {
            'exp_date': DateInput(),
            'date' : DateInput(),
        }

