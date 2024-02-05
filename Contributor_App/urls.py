from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path('Contributor_Login',Contributor_Login,name='Contributor_Login'),
    path('Contributor_Registraion',Contributor_Registraion,name='Contributor_Registraion'),
    path('Update_Contributor',Update_Contributor,name='Update_Contributor')
]
