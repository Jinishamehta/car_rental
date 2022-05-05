from string import digits
from unittest.util import _MAX_LENGTH
from django.db import models
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.forms import ValidationError


# Create your models here.

class User(AbstractUser):

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

class rsj_vehicle_class(models.Model):
    class_id = models.AutoField(primary_key=True, validators=[MaxValueValidator(999), MinValueValidator(1)],)
    name = models.CharField(max_length=30, unique=True, null=False)
    rate_per_day = models.DecimalField(max_digits=5, decimal_places=2, null=False, validators=[MaxValueValidator(999.00), MinValueValidator(1.00)] )
    over_mileage_fee = models.DecimalField(max_digits=5, decimal_places=2,  validators=[MaxValueValidator(999.00), MinValueValidator(1.00)], null=False)
    daily_limit = models.DecimalField(max_digits=7, decimal_places=2,  validators=[MaxValueValidator(99999.00), MinValueValidator(1.00)], null=False)
    # updated_at = models.DateTimeField(auto_now=True)
    # created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'rsj_vehicle_class'

class rsj_location(models.Model):
    location_id = models.AutoField(primary_key=True, validators=[MaxValueValidator(99999), MinValueValidator(1)])
    street = models.CharField(max_length=50, null=False)
    city = models.CharField(max_length=30, null=False)
    state = models.CharField(max_length=30, null=False)
    pincode = models.CharField(max_length=5, validators=[RegexValidator(regex='^[0-9]{5}$')], null=False)
    phone_no = models.BigIntegerField(validators=[RegexValidator(regex='^[0-9]{10}$')], null=False)

    def __str__(self):
        return self.street

    class Meta:
        db_table = 'rsj_location'

class rsj_discount(models.Model):
    coupon_code = models.CharField(primary_key=True, max_length=10, validators=[RegexValidator(regex='^[A-Za-z0-9]{10}$')] )
    rate = models.IntegerField(range(0, 99), null=False)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    used = models.BooleanField(default=False)

    def __str__(self):
        return self.coupon_code

    class Meta:
        db_table = 'rsj_discount'

class rsj_plan(models.Model):
    plan_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, null=False)
    cost = models.IntegerField(null=False)
    description = models.TextField(max_length=100, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'rsj_plan'

class rsj_company(models.Model):
    company_reg_no = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, null=False)
    discount_rate = models.IntegerField(range(0, 99), null=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'rsj_company'

class rsj_vehicle(models.Model):
    vin =  models.CharField(primary_key=True, max_length=17, validators=[RegexValidator(regex='^[A-Za-z0-9]{17}$')])
    make = models.CharField(max_length=30, null=False)
    model = models.CharField(max_length=30, null=False)
    year = models.IntegerField(validators= [RegexValidator(regex='^[1-9][0-9]{3}$')], null=False)
    availability = models.BooleanField(default=True)
    lpn = models.CharField(max_length=7, validators=[RegexValidator(regex='^[A-Za-z0-9]{7}$')], null=False)
    #Foriegn keys
    class_id = models.ForeignKey(rsj_vehicle_class, on_delete=models.CASCADE, db_column= 'class_id')
    location_id = models.ForeignKey(rsj_location, on_delete=models.CASCADE, db_column= 'location_id')

    def __str__(self):
        return self.lpn

    class Meta:
        db_table = 'rsj_vehicle'

class rsj_customer(models.Model):
    # TYPE_INDIVIDUAL = 'individual'
    # TYPE_CORPORATE = 'virtual'
    # TYPE_CHOICES = (
    #     (TYPE_INDIVIDUAL, 'individual'),
    #     (TYPE_CORPORATE, 'virtual'),
    # )
    # customer_type = models.CharField(
    #     max_length=20,
    #     choices=TYPE_CHOICES,
    # )

    customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    street = models.CharField(max_length=50, null=False)
    city = models.CharField(max_length=30, null=False)
    state = models.CharField(max_length=30, null=False)
    pincode = models.CharField(max_length=5, validators=[RegexValidator(regex='^[0-9]{5}$')], null=False)
    phone_no = models.IntegerField(validators=[RegexValidator(regex='^[0-9]{10}$')], null=False)
    email = models.EmailField(max_length=150)
    driver_license =  models.CharField(max_length=19, validators=[RegexValidator(regex='^[A-Za-z0-9]{19}$')])
    # is_employee = models.BooleanField(default=False)

    class Meta:
        db_table = 'rsj_customer'

    # def clean(self) -> None:
    #     if self.customer_type == rsj_customer.TYPE_INDIVIDUAL:
    #         if self.policy_no == None & self.insurance_name == None:
    #             raise ValidationError (
    #                 'Please Add Policy Number and Company'
    #             )

    #         if self.company_reg_no != None & self.emp_id != None:
    #             raise ValidationError(
    #                 'Individual Customer cannot have employee id or company name'
    #             )
    #     elif self.customer_type == rsj_customer.TYPE_CORPORATE:
    #         if self.policy_no != None & self.insurance_name != None:
    #             raise ValidationError (
    #                 'Corporate customer cannot have policy number or insurance company'
    #             )

    #         if self.company_reg_no == None & self.emp_id == None:
    #             raise ValidationError(
    #                 'Please add employee id and company name'
    #             )
    #     else:
    #         assert False, f'Unknown Customer Type "{self.customer_type}"'

class rsj_ind_cust(rsj_customer):
    policy_no = models.CharField(max_length=13, null=True)
    insurance_name = models.CharField(max_length=50, null=True)

    class Meta():
        db_table = 'rsj_ind_cust'

class rsj_corp_cust(rsj_customer):
    company_reg_no = models.ForeignKey(rsj_company, on_delete=models.RESTRICT, null=True, db_column= 'company_reg_no')
    emp_id = models.CharField(max_length=10, null=True)

    class Meta():
        db_table = 'rsj_corp_cust'

class rsj_service(models.Model):
    service_id = models.AutoField(primary_key=True, validators=[MaxValueValidator(9999999), MinValueValidator(1)])
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    start_meter = models.DecimalField(max_digits=7, decimal_places=2)
    end_meter = models.DecimalField(max_digits=7, decimal_places=2, null=True)

    customer_id = models.ForeignKey(rsj_customer, on_delete=models.RESTRICT, db_column= 'customer_id')
    vin = models.ForeignKey(rsj_vehicle, on_delete=models.RESTRICT, db_column= 'vin')
    plan_id = models.ForeignKey(rsj_plan, on_delete=models.RESTRICT, db_column= 'plan_id')
    start_location = models.ForeignKey(rsj_location, on_delete=models.RESTRICT, related_name='start', db_column= 'start_location')
    end_location = models.ForeignKey(rsj_location, on_delete=models.RESTRICT, related_name='end', db_column= 'end_location')
    coupon_code = models.ForeignKey(rsj_discount, on_delete=models.RESTRICT, db_column= 'coupon_code')

    class Meta:
        db_table = 'rsj_service'

class rsj_invoice(models.Model):
    invoice_id = models.AutoField(primary_key=True)
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    invoice_date = models.DateTimeField()
    pending_amount = models.DecimalField(max_digits=7, decimal_places=2, default=amount)

    service_id = models.ForeignKey(rsj_service,on_delete=models.RESTRICT, db_column= 'service_id')

    class Meta:
        db_table = 'rsj_invoice'

class rsj_payment(models.Model):
    CARD = 'CARD'
    CASH = 'CASH'
    payment_id = models.AutoField(primary_key=True)
    method = models.CharField(
        max_length=4,
        choices = ((CARD,'CARD') , (CASH, 'CASH')),
        default = 'CARD'
    )
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    p_date = models.DateTimeField()
    card_no = models.BigIntegerField(null=True)
    name_on_card = models.CharField(max_length=50, null=True)
    exp_date = models.DateField(null=True)
    
    invoice_id = models.ForeignKey(rsj_invoice, on_delete=models.RESTRICT, db_column='invoice_id')

    class Meta:
        db_table = 'rsj_payment'
