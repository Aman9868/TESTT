from django.contrib import admin
from django.urls import path,include
from .views import *
from django.conf.urls.static import static


urlpatterns = [
    # preurl =Organization
    path('Organization_Registraion' , Organization_Registraion , name='Organization_Registraion'),
    path('Organization_Login' , Organization_Login , name='Organization_Login'),
    path('Update_Organization' , Update_Organization , name='Update_Organization'),
    path('Upload_CSV_Data_By_Institutions',Upload_CSV_Data_By_Institutions,name='Upload_CSV_Data_By_Institutions'),
    path('Get_User_List',Get_User_List,name='Get_User_List'),
    path('Send_Login_Url_To_User',Send_Login_Url_To_User,name='Send_Login_Url_To_User'),
    path('Add_Lgog_TO_Video',Add_Lgog_TO_Video,name='Add_Lgog_TO_Video')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
