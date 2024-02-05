from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import json
import traceback
from django.views.decorators.csrf import csrf_exempt
from Contributor_App.models import *
import csv
import io
from datetime import datetime
import pandas as pd
import numpy as np
import random
from ProjectUtilities.send_emails import *
from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip
import os


# Create your views here.

@csrf_exempt
def Organization_Registraion(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        email =data['email']
        mobile_no =data['mobile_no']
        org_type =data['org_type']
        password =data['password']
        if Organization_Detail.objects.filter(email=email).exists():
            Organization_Detail.objects.get(email=email)
            send_data = {"status": 0, "msg": f"Oops! It looks like this email is already registered. Thank you!"}
        elif Organization_Detail.objects.filter(mobile_no=mobile_no).exists():
            Organization_Detail.objects.get(mobile_no=mobile_no)
            send_data = {"status": 0, "msg": f"Oops! It looks like this mobile number is already registered. Thank you!"}
        else:
            Organization_Detail.objects.create(email=email,mobile_no=mobile_no,password=password,org_type=org_type)
            send_data = {'status':1,'msg':'organization registration done successfully'}
    except:
        traceback.print_exc()
        send_data = {'status':0,'msg':'Something went wrong','error':traceback.format_exc()}
    return JsonResponse(send_data)


@csrf_exempt
def Organization_Login(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        email =data['email']
        password =data['password']
        if Organization_Detail.objects.filter(email=email, password=password).exists():
            obj = Organization_Detail.objects.get(email=email, password=password)
            request.session['user_id'] = obj.id
            request.session['user_type'] = "Organization"
            temp_dict = {}  
            temp_dict['id'] = obj.id if obj.id else ""
            temp_dict['first_name']= obj.org_type if obj.org_type else "" #Bank , Institution , NGO
            temp_dict['email'] = obj.email if obj.email else ""
            temp_dict['mobile_no'] = obj.mobile_no if obj.mobile_no else ""
            temp_dict['first_name']= obj.company_name if obj.company_name else ""
            send_data = {"status": 1, "msg": "login succesfully",'user_details':temp_dict}
        else: 
            send_data = {"status": 0, "msg": "Invalid Credentials"}
    except:
        print(traceback.format_exc())
        send_data = {'status':0,'msg':'Something went wrong','error':traceback.format_exc()}
    return JsonResponse(send_data)

@csrf_exempt
def Update_Organization(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        user_id = data['user_id']
        state =data['state']
        city =data['city']
        company_name =data['company_name']
        mobile_no = data['mobile_no']
        obj=Organization_Detail.objects.get(id=user_id)
        obj.fk_state = state
        obj.fk_city = city
        obj.company_name = company_name
        obj.mobile_no=mobile_no
        obj.save()
        send_data = {"status": 1, "msg": "Organization Profile updated succesfully"}
    except:
        print(traceback.format_exc())
        send_data = {'status':0,'msg':'Something went wrong','error':traceback.format_exc()}
    return JsonResponse(send_data)

# genrate the age group for users
def generate_age_group(age):
    if age >=18 and age <=25:
        return '18-25'
    elif age >=26 and age <= 35:
        return '26-35'
    elif age  >= 36 and age <= 45:
        return '36-45'
    else:
        return '46-60+'

# genrate the income group for uesr income
def generate_income_group(income):
    if income >= 100000 and income <= 200000:
        return '1-2lakh'
    elif income >= 200001 and income <= 300000:
        return '2-3lakh'
    elif income >= 300001 and income <= 400000:
        return '3-4lakh'
    elif income >= 400001 and income <= 500000:
        return '4-5lakh'  
    elif income >= 500001 and income <= 600000:
        return '5-6lakh'
    elif income >= 600001 and income <= 700000:
        return '6-7lakh'
    elif 700001 >= income <= 800000:
        return '7-8lakh'
    elif income and 800001  and income <= 900000:
        return '8-9lakh'
    else:
        return '9lakh-10lakh'

@csrf_exempt
def Upload_CSV_Data_By_Institutions(request):
    try:
        if request.method == "POST":
            csv_file = request.FILES.get('csv_file')
            fk_institution_id = request.POST.get('fk_institution_id')
            print(csv_file)
            if csv_file:
                # Decode the file content and create a StringIO object
                decoded_file = csv_file.read().decode('utf-8')
                file_stream = io.StringIO(decoded_file)
                csv_dict_reader = csv.DictReader(file_stream)
                data_list = list(csv_dict_reader)
                # Accessing the list of dictionaries
                for i in data_list:
                    if not User_Details.objects.filter(mobile_number=i['Mobile Number']).exists():
                        obj =User_Details.objects.create(fk_institution_id=fk_institution_id,created_date=datetime.now().date(),name=i['Name'],age=i['Age'],mobile_number=i['Mobile Number'],income=i['Income (INR)'],Whatsapp=i['WhatsApp'],type=i['Type'],state=i['State'],city=i['City'],marital_status=i['Marital Status'],No_of_Children=i['No. of Children'],education=i['Education'],family_members=i['Family Members'],occupation=i['Occupation'],gender=i['Gender'],caste=i['Caste'],religion=i['Religion'],ngo_name=i['NGOs Name'])
                        age_group = generate_age_group(int(obj.age))
                        obj.age_group=age_group
                        income_group=generate_income_group(int(obj.income))
                        obj.income_group =income_group
                        obj.save()
                send_data = {'status': 1, 'msg': 'Data uploaded successfully'}
            else:
                send_data = {'status': 0, 'msg': 'Please upload a CSV file'}
        else:
            send_data = {'status': 0, 'msg': 'Request is not a POST request'}
    except Exception as e:
        traceback.print_exc()
        send_data = {'status': 0, 'msg': 'Something went wrong', 'error': str(e)}
    return JsonResponse(send_data)
 
@csrf_exempt
def Get_User_List(request):
    try:
        if request.method=='POST':
            data = json.loads(request.body.decode('utf-8'))
            fk_institution = data['fk_institution']
            whatsapp =  data['whatsapp']
            state = data['state']
            city = data['city']
            education = data['education']
            occupation =data['occupation']
            gender = data['gender']
            age_group = data['age_group']
            income_group = data['income_group']
            user_obj=User_Details.objects.filter(fk_institution_id=fk_institution, Whatsapp=whatsapp,state=state,city=city,education=education,occupation=occupation,gender=gender,age_group=age_group,income_group=income_group).order_by('-id')
            send_data = {'status': 1, 'obj count':user_obj.count(),'msg': 'users list','data':list(user_obj.values())}
        else:
            send_data = {'status': 1, 'msg':'Request is not post'}
    
    except Exception as e:
        traceback.print_exc()
        send_data = {'status': 0, 'msg': 'Something went wrong', 'error': str(e)}
    return JsonResponse(send_data)

# send login url to mahila user
@csrf_exempt
def Send_Login_Url_To_User(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body.decode('utf-8'))
            user_id_array = data['user_id']
            user_obj = User_Details.objects.filter(id__in=user_id_array)
            for i in user_obj:
                subject = "Your Mahila Account: Secure Access Link"
                dummy_str = render_to_string('email_rts/mahila_login.html')
                to_email = i.email
                send_html_email(subject, dummy_str, to_email)
            send_data = {'status':1,'msg':'Email sent successfully'}
        else:
            send_data = {'status':1,'msg':'Request is not post'}
    except:
        traceback.print_exc()
        send_data = {'status':0,'msg':'Something went wrong'}
    return JsonResponse(send_data)



# AI Codes By Amanpreet ############
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp4', 'png'}
def add_logo(video_path, logo_path, position):
    print(video_path,'oooooooooooooooooooooooooooooooooooooooooooooooooo')
    video = VideoFileClip(video_path)
    logo = (ImageClip(logo_path).set_duration(video.duration).margin(right=8, top=8, opacity=0).resize(width=241, height=76).set_pos(tuple(map(int, position.split(',')))))
    final = CompositeVideoClip([video, logo])
    output_path = os.path.join(UPLOAD_FOLDER, "output.mp4")
    final.write_videofile(output_path, codec='libx264', audio_codec='aac')
    return output_path

@csrf_exempt
def Add_Lgog_TO_Video(request):
    try:
        if request.method == 'POST':
            video_file = request.FILES.get('video')
            logo_file = request.FILES.get('logo')
            position = request.POST.get('position')
            print(video_file,'tttttttttttttttttttttttttt')
            print(logo_file,position)
            fs = FileSystemStorage(location=UPLOAD_FOLDER)
            video_path = fs.save("uploaded_video.mp4", video_file)
            logo_path = fs.save("uploaded_logo.png", logo_file)
            output_path = add_logo(video_path, logo_path, position)
            with open(output_path, 'rb') as file:
                response = HttpResponse(file.read(), content_type='application/video')
                response['Content-Disposition'] = 'attachment; filename=output.mp4'
                # return response
            send_data = {'status':1,'msg':'Logo Added successfully'}
        else:
            send_data = {'status':0,'msg':'Request is not post'}
    except:
        traceback.print_exc()
        send_data = {'status':0,'msg':'Something went wrong'}
    return JsonResponse(send_data)