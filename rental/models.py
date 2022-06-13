from string import digits
from unittest.util import _MAX_LENGTH
from django.db import models
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.forms import ValidationError

class rsj_vehicle_class(models.Model):
    class_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, unique=True)
    rate_per_day = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(1.00)] )
    over_mileage_fee = models.DecimalField(max_digits=5, decimal_places=2,  validators=[MinValueValidator(1.00)])
    daily_limit = models.DecimalField(max_digits=7, decimal_places=2,  validators=[MinValueValidator(1.00)])
    # updated_at = models.DateTimeField(auto_now=True)
    # created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'rsj_vehicle_class'

class rsj_location(models.Model):
    location_id = models.AutoField(primary_key=True)
    street = models.CharField(max_length=50)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    pincode = models.CharField(max_length=5, validators=[RegexValidator(regex='^[0-9]{5}$')])
    phone_no = models.CharField(max_length=10,validators=[RegexValidator(regex='^[0-9]{10}$')])

    def __str__(self):
        return self.street

    class Meta:
        db_table = 'rsj_location'

class rsj_discount(models.Model):
    coupon_code = models.CharField(primary_key=True, max_length=10, validators=[RegexValidator(regex='^[A-Za-z0-9]{5,10}$')])
    rate = models.DecimalField(max_digits=4, decimal_places=2, validators=[MinValueValidator(1.00)] )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    used = models.BooleanField(default=False)

    def __str__(self):
        return self.coupon_code

    class Meta:
        db_table = 'rsj_discount'

class rsj_plan(models.Model):
    plan_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, unique=True)
    cost = models.IntegerField(validators=[MinValueValidator(1)])
    description = models.TextField(max_length=100, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'rsj_plan'

class rsj_company(models.Model):
    company_reg_no = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    discount_rate =  models.DecimalField(max_digits=4, decimal_places=2, validators=[MinValueValidator(1.00)] )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'rsj_company'

class rsj_vehicle(models.Model):
    vin =  models.CharField(primary_key=True, max_length=17, validators=[RegexValidator(regex='^[A-Za-z0-9]{17}$')])
    make = models.CharField(max_length=30)
    model = models.CharField(max_length=30)
    year = models.IntegerField(validators = [RegexValidator(regex='^[1-9][0-9]{3}$')])
    availability = models.BooleanField(default=True)
    lpn = models.CharField(max_length=7, validators=[RegexValidator(regex='^[A-Za-z0-9]{6,7}$')])
    #Foriegn keys
    class_id = models.ForeignKey(rsj_vehicle_class, on_delete=models.CASCADE, db_column= 'class_id')
    location_id = models.ForeignKey(rsj_location, on_delete=models.CASCADE, db_column= 'location_id')

    def __str__(self):
        return self.model

    class Meta:
        db_table = 'rsj_vehicle'

class rsj_customer(models.Model):
    TYPE_INDIVIDUAL = 'I'
    TYPE_CORPORATE = 'C'
    TYPE_CHOICES = (
        (TYPE_INDIVIDUAL, 'Individual'),
        (TYPE_CORPORATE, 'Corporate'),
    )

    username = models.OneToOneField(User, on_delete=models.CASCADE, db_column = 'username')
    customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=30)
    street = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    pincode = models.CharField(max_length=5, validators=[RegexValidator(regex='^[0-9]{5}$')], null=False)
    phone_no = models.CharField(validators=[RegexValidator(regex='^[0-9]{10}$')], null=False, max_length=10)
    email = models.EmailField(max_length=150)
    dr_lno =  models.CharField(max_length=19, validators=[RegexValidator(regex='^[A-Za-z0-9]{19}$')])
    customer_type = models.CharField(
        max_length=1,
        choices=TYPE_CHOICES,
        default='I'
    )
    
    def __str__(self):
        return self.username.username

    class Meta:
        db_table = 'rsj_customer'

class rsj_corp_cst(models.Model):
    customer = models.OneToOneField('rsj_customer', models.DO_NOTHING, primary_key=True)
    reg_no = models.ForeignKey(rsj_company, models.DO_NOTHING, db_column='reg_no')
    emp_id = models.CharField(max_length=10)

    class Meta:
        db_table = 'rsj_corp_cst'

class rsj_ind_cst(models.Model):
    customer = models.OneToOneField('rsj_customer', models.DO_NOTHING, primary_key=True)
    policy_no = models.CharField(max_length=13)
    insurance_name = models.CharField(max_length=50)

    class Meta:
        db_table = 'rsj_ind_cst'
        unique_together = (('customer', 'policy_no'),)


class rsj_invoice(models.Model):
    invoice_id = models.AutoField(primary_key=True)
    service_id = models.ForeignKey('rsj_service', models.DO_NOTHING, db_column= 'service_id')
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    invoice_date = models.DateTimeField(auto_now_add=True)
    pendng_amt = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)

    class Meta:
        db_table = 'rsj_invoice'

    # class __str__()


class rsj_payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    invoice_id = models.ForeignKey(rsj_invoice, models.DO_NOTHING)
    method = models.CharField(max_length=4)
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    date = models.DateTimeField(db_column='DATE')  # Field name made lowercase.
    card_no = models.CharField(max_length=16, validators=[RegexValidator(regex='^[0-9]{16}$')], null=True)
    name_on_card = models.CharField(max_length=30, null=True)
    exp_date = models.DateTimeField(null=True)

    class Meta:
        db_table = 'rsj_payment'

class rsj_service(models.Model):
    service_id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(rsj_customer, on_delete=models.RESTRICT, db_column= 'customer_id')
    vin = models.ForeignKey(rsj_vehicle, on_delete=models.RESTRICT, db_column= 'vin')
    service_type = models.ForeignKey('rsj_plan', models.DO_NOTHING, db_column='service_type')
    start_location = models.ForeignKey('rsj_location', models.DO_NOTHING, related_name='start', db_column='start_location')
    end_location_id = models.ForeignKey('rsj_location', models.DO_NOTHING, related_name='end', db_column='end_location_id')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    coupon_code = models.ForeignKey(rsj_discount, models.DO_NOTHING, db_column='coupon_code', null=True)
    odometer_start = models.IntegerField()
    odometer_end = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'rsj_service'

    def __str__(self):
        return self.customer_id.first_name