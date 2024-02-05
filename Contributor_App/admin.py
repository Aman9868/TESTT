from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(StateMaster)
class StateMasterAdmin(admin.ModelAdmin):
    list_display = ['id', 'state']
    
@admin.register(CityMaster)
class CityMasterAdmin(admin.ModelAdmin):
    list_display = ['id', 'fk_state', 'city']
    
@admin.register(Content_Master)
class Content_MasterAdmin(admin.ModelAdmin):
    list_display = ['id', 'content_type','created_date']
    
@admin.register(Sub_Content_Type)
class Sub_Content_TypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'fk_content','sub_content_type', 'created_date']

@admin.register(Bank_Master)
class Bank_MasterAdmin(admin.ModelAdmin):
    list_display = ['id', 'bank_type', 'created_date']

@admin.register(Sub_Bank_Master)
class Sub_Bank_MasterAdmin(admin.ModelAdmin):
    list_display = ['id', 'fk_bank', 'bank_name','created_date']

@admin.register(Contributor_Detail)
class Contributor_DetailAdmin(admin.ModelAdmin):
    list_display = ['id','first_name', 'last_name']

@admin.register(Organization_Detail)
class Organization_DetailAdmin(admin.ModelAdmin):
    list_display = ['id', 'company_name']


@admin.register(User_Details)
class User_DetailsAdmin(admin.ModelAdmin):
    list_display = ['id', 'fk_institution','name','mobile_number','Whatsapp','age','income','created_date']
