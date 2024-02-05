from django.db import models
class StateMaster(models.Model):
    state = models.CharField(null=True, blank=True, max_length=100)
    created_date = models.DateField(null=True , blank=True) 

class CityMaster(models.Model):
    fk_state = models.ForeignKey(StateMaster, on_delete=models.CASCADE, null=True, blank=True)
    city = models.CharField(null=True, blank=True, max_length=100)
    created_date = models.DateField(null=True , blank=True) 

class Content_Master(models.Model):
    content_type = models.CharField(null=True, blank=True, max_length=100)
    created_date = models.DateField(null=True , blank=True) 

class Sub_Content_Type(models.Model):
    fk_content = models.ForeignKey(Content_Master, on_delete=models.CASCADE,null=True,blank=True)
    sub_content_type = models.CharField(null=True, blank=True, max_length=100)
    created_date = models.DateField(null=True , blank=True) 

class Bank_Master(models.Model):
    bank_type = models.CharField(null=True, blank=True, max_length=100)
    created_date = models.DateField(null=True , blank=True) 

class Sub_Bank_Master(models.Model):
    fk_bank = models.ForeignKey(Bank_Master, on_delete=models.CASCADE,null=True,blank=True)
    bank_name = models.CharField(null=True, blank=True, max_length=100)
    created_date = models.DateField(null=True , blank=True) 

class NGO_Master(models.Model):
    ngo_type = models.CharField(null=True, blank=True, max_length=100)
    created_date = models.DateField(null=True , blank=True) 

class Contributor_Detail(models.Model):
    email = models.CharField(null=True, blank=True, max_length=100)
    mobile_no = models.CharField(null=True, blank=True, max_length=10)
    password = models.CharField(null=True, blank=True, max_length=100)
    fk_state = models.CharField(null=True, blank=True, max_length=100) 
    fk_city = models.CharField(null=True, blank=True, max_length=100) 
    first_name = models.CharField(null=True, blank=True, max_length=100)
    last_name = models.CharField(null=True, blank=True, max_length=100)
    created_date = models.DateField(null=True , blank=True) 
    
class Organization_Detail(models.Model):
    email = models.CharField(null=True, blank=True, max_length=100)
    mobile_no = models.CharField(null=True, blank=True, max_length=10)
    password = models.CharField(null=True, blank=True, max_length=100)
    fk_state = models.CharField(null=True, blank=True, max_length=100) 
    fk_city = models.CharField(null=True, blank=True, max_length=100)  
    org_type = models.CharField(null=True, blank=True, max_length=100) #Bank , Institution , NGO 
    company_name= models.CharField(null=True, blank=True, max_length=100)
    address  = models.TextField(null=True, blank=True)
    created_date = models.DateField(null=True , blank=True)
    website_url = models.CharField(null=True, blank=True, max_length=100)
    gst_no = models.CharField(null=True, blank=True, max_length=100)
    created_date = models.DateField(null=True , blank=True) 
    
    
class PostContent(models.Model):
    fk_Contributor = models.ForeignKey(Contributor_Detail, on_delete=models.CASCADE,null=True,blank=True)
    fk_sub_content = models.ForeignKey(Sub_Content_Type, on_delete=models.CASCADE,null=True,blank=True)
    title = models.CharField(null=True, blank=True, max_length=100) 
    file_type = models.CharField(null=True, blank=True, max_length=100) #file type should be audio, video, file  
    file = models.FileField(upload_to='files/', null=True, blank=True)
    created_date = models.DateField(null=True , blank=True) 

class User_Details(models.Model):
    fk_institution = models.ForeignKey(Organization_Detail, on_delete=models.CASCADE,null=True,blank=True)
    created_date = models.DateField(null=True , blank=True) 
    name = models.CharField(null=True, blank=True, max_length=100)
    email = models.CharField(null=True, blank=True, max_length=100)
    age = models.CharField(null=True, blank=True, max_length=100)
    mobile_number = models.CharField(null=True, blank=True, max_length=100)
    income = models.CharField(null=True, blank=True, max_length=100)
    Whatsapp = models.CharField(null=True, blank=True, max_length=100) #whatsapp status Yes , No
    type = models.CharField(null=True, blank=True, max_length=100)
    state = models.CharField(null=True, blank=True, max_length=100)
    city = models.CharField(null=True, blank=True, max_length=100)
    marital_status = models.CharField(null=True, blank=True, max_length=100)
    No_of_Children = models.CharField(null=True, blank=True, max_length=100)
    education = models.CharField(null=True, blank=True, max_length=100)
    family_members = models.CharField(null=True, blank=True, max_length=100)
    occupation =models.CharField(null=True, blank=True, max_length=100)
    gender = models.CharField(null=True, blank=True, max_length=100)
    caste = models.CharField(null=True, blank=True, max_length=100)
    religion = models.CharField(null=True, blank=True, max_length=100)
    ngo_name = models.CharField(null=True, blank=True, max_length=100)
    age_group = models.CharField(null=True, blank=True, max_length=100)
    income_group =models.CharField(null=True, blank=True, max_length=100)