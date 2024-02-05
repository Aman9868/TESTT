import traceback
from django.shortcuts import render, redirect
from MemoyoApp.models import MyUser
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from CustomAdmin.models import *
from MemoyoApp.models import *


# below code is decorator to check user login or not

def Admin_login_required_decorator(view_func):
	def _wrapped_view(request, *args, **kwargs):
		try:
			session_id = request.session.get('admisesionid')
			usertype = request.session.get('usertype')

			if session_id and usertype:
				if MemoyoAdmin.objects.filter(id=session_id).exists():
					user = MemoyoAdmin.objects.get(id=session_id)
					return view_func(request, user, *args, **kwargs) 
				else:
					return redirect('/memoyoadmin')
			else:
				return redirect('/memoyoadmin')
		except Exception as e:
			traceback.print_exc()
			return redirect('/memoyoadmin')  # Redirect or return an error page
	return _wrapped_view

### check request is authenticated or not 

def is_authenticated(request):
	try:
		session_id = request.session.get('user_id')
		if session_id is not None:
			user = MyUser.objects.filter(id=session_id)
			if user.exists():
				return user.last()
			return None
		else:
			return None
	except Exception as e:
		traceback.print_exc()
		return False



def handle_page_exception(func):
	'''Function template to handle POST request and handle exceptions...'''
	def wrapper(request, *args, **kwargs):
		try:
			user = is_authenticated(request)
			try:
				obj = UserDetails.objects.get(fk_myuser__id=user.id)
				user.profile_pic = obj.profile_pic
				user.tagline = obj.tagline
				user.bio = obj.bio
				user.tags = obj.tags
				user.reel = obj.reel
				user.looking_for_work = obj.looking_for_work
				user.website = obj.website
				user.social_1 = obj.social_1
				user.social_2 = obj.social_2
				user.social_3 = obj.social_3
				user.fk_country = obj.fk_country
				user.fk_state = obj.fk_state
				user.fk_city = obj.fk_city
				user.status = obj.status
			except:
				pass
			return func(request, user, *args, **kwargs)
		except:
			traceback.print_exc()
		return HttpResponse('Something went wrong')
	return wrapper

def handle_ajax_exception(func):
	'''Function template to handle POST request and handle exceptions...'''
	def wrapper(request, *args, **kwargs):
		send_data = {'status': 0, 'msg': 'Something went wrong.', 'errTitle' : 'error'}
		try:
			if request.method == 'POST':
				return func(request, *args, **kwargs)
			else:
				send_data['msg'] = 'POST method required.'
		except ObjectDoesNotExist:
			send_data['msg'] = 'Object not found.'
		except:
			traceback.print_exc()
		return JsonResponse(send_data)
	return wrapper