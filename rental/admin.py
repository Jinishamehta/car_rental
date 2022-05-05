from django.contrib import admin

# Register your models here.
from .models import rsj_company,rsj_corp_cust,rsj_customer,rsj_discount,rsj_ind_cust,rsj_invoice,rsj_location,rsj_payment,rsj_plan,rsj_service,rsj_vehicle,rsj_vehicle_class

admin.site.register(rsj_vehicle_class)
admin.site.register(rsj_location)
admin.site.register(rsj_discount)
admin.site.register(rsj_company)
admin.site.register(rsj_corp_cust)
admin.site.register(rsj_customer)
admin.site.register(rsj_invoice)
admin.site.register(rsj_ind_cust)
admin.site.register(rsj_payment)
admin.site.register(rsj_plan)
admin.site.register(rsj_vehicle)
admin.site.register(rsj_service)





