from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import json
import traceback
from django.views.decorators.csrf import csrf_exempt
from .models import *
import pandas as pd
# Create your views here.

import csv
def Append_Country():
    # csv_file = 'static/countries.csv'
    # csv_file = 'static/state.csv'  # Replace with the path to your CSV file
    csv_file = 'static/city.csv'
    country_data = []
    print('fffffffffffffffff')
    try:
        with open(csv_file, mode='r', newline='') as file:
            csv_reader = csv.DictReader(file)
            # below code to append  country states city only
            '''for row in csv_reader: # for contry
                print(row['name'],row['phonecode'])
                if row['name']:
                    CountryMaster.objects.create(Country=row['name'],Country_code=row['phonecode'])'''
            try:
                '''for row in csv_reader: #for state
                    if row['name']:
                        # print(row['country_id'],row['name'])
                        # StateMaster.objects.create(fk_Contry_id=row['country_id'],state=row['name'])
                        # StateMaster.objects.create(state=row['name'])
                        # print(row['name'])'''

                '''for row in csv_reader:  # for city
                    if row['state_id']:
                        print(row['state_id'],row['name'])
                        CityMaster.objects.create(fk_state_id=row['state_id'],city=row['name'])'''
                pass
            except:
                traceback.print_exc()
    except FileNotFoundError:
        print(f"File '{csv_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    return HttpResponse('Done')

# Append_Country()


@csrf_exempt
def Contributor_Registraion(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        email =data['email']
        mobile_no =data['mobile_no']
        password =data['password']
        if Contributor_Detail.objects.filter(email=email).exists():
            send_data = {"status": 0, "msg": "Oops! It looks like this email is already registered. Thank you!"}
        elif Contributor_Detail.objects.filter(mobile_no=mobile_no).exists():
            send_data = {"status": 0, "msg": "Oops! It looks like this mobile number is already registered. Thank you!"}
        else:
            Contributor_Detail.objects.create(email=email,mobile_no=mobile_no,password=password)
            send_data = {'status':1,'msg':'Contributor registration done successfully'}
    except:
        print(traceback.format_exc())
        send_data = {'status':0,'msg':'Something went wrong','error':traceback.format_exc()}
    return JsonResponse(send_data)

@csrf_exempt
def Contributor_Login(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        email =data['email']
        password =data['password']
        if Contributor_Detail.objects.filter(email=email, password=password).exists():
            obj = Contributor_Detail.objects.get(email=email, password=password)
            request.session['user_id'] = obj.id
            request.session['user_type'] = "Contributor"
            temp_dict = {}  
            temp_dict['id'] = obj.id if obj.id else ""
            temp_dict['email'] = obj.email if obj.email else ""
            temp_dict['mobile_no'] = obj.mobile_no if obj.mobile_no else ""
            temp_dict['first_name']= obj.first_name if obj.first_name else ""
            temp_dict['last_name'] = obj.last_name if obj.last_name else ""
            send_data = {"status": 1, "msg": "login succesfully",'user_details':temp_dict}
        else: 
            send_data = {"status": 0, "msg": "Invalid Credentials"}
    except:
        print(traceback.format_exc())
        send_data = {'status':0,'msg':'Something went wrong','error':traceback.format_exc()}
    return JsonResponse(send_data)        


@csrf_exempt
def Update_Contributor(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        user_id = ['user_id']
        state =data['state']
        city =data['city']
        mobile_no = data['mobile_no']
        first_name =data['first_name']
        last_name = data['last_name']
        obj=Contributor_Detail.objects.get(id=user_id)
        obj.fk_state = state
        obj.fk_city = city
        obj.mobile_no=mobile_no
        obj.first_name = first_name
        obj.last_name=last_name
        obj.save()
        send_data = {"status": 1, "msg": "Organization Profile updated succesfully"}
    except:
        print(traceback.format_exc())
        send_data = {'status':0,'msg':'Something went wrong','error':traceback.format_exc()}
    return JsonResponse(send_data)