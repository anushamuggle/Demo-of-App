from django.shortcuts import render
from apps.backwork.models import GlobalUsers
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.auth.hashers import PBKDF2PasswordHasher
from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required

import json
import datetime 
import random
# Create your views here.

@csrf_exempt
def signup_user(request):
    request_data = json.loads(request.body)
    # request_data = request.GET
    back = ''
    data = False
    hasher =''
    verify_code = ''
    username_check = GlobalUsers.objects.filter(gus_email= request_data['email']).values_list('gus_email', flat=True)
    if request.method == 'POST' and request_data['email'] not in username_check:
        data = True
        verify_code = str(random.randint(10000,99999))
        hasher = PBKDF2PasswordHasher()
        signup_details = GlobalUsers()
        # signup_details.gus_username = str(request_data['username'])
        signup_details.gus_password = hasher.encode(password= request_data['password'] , salt='salt',iterations= 50000)
        signup_details.gus_email = request_data['email']
        signup_details.gus_address = request_data['address']
        signup_details.gus_pincode = request_data['pincode']
        signup_details.gus_createdon = datetime.datetime.now()
        signup_details.gus_isused = 0
        signup_details.gus_confirmcode = verify_code
        signup_details.gus_phone = request_data['phone']
        signup_details.save()
        subject = "email verification HUL"            
        message = "please verify your email by typing the following code in your Distributor App " + verify_code
        sender = "hul@gmail.com"
        send_mail(subject, message, sender, [request_data['email']])
        back = [{'hello':'hello'}]
        data = json.dumps(back)
        print request_data
    return HttpResponse(data)

@csrf_exempt
def user_login(request):
	# request_data = json.loads(request.body)
    request_data = json.loads(request.body)
    username = ''
    password = ''
    data = ''
    username_first =''
    username_first = GlobalUsers.objects.filter(gus_email= request_data['username'], gus_isused=0).values_list('gus_email', flat=True)

    username = request_data['username']
    password = request_data['password']
    if request.method == 'POST':
        try:
            user = authenticate(username=username, password=password)
            if user is not None:
                if username in username_first:
                    data = "verify" 
                else:    
                    data = True
                login(request, user)
            else:
                raise ObjectDoesNotExist
                data = "False"
        except  ObjectDoesNotExist:
            data = False
    return HttpResponse(data)

@login_required
def verify_code(request):
	request_data = json.loads(request.body)
	verify_code = ''
	userid= ''
	username = ''
	data = ''
	flag_code = request_data['verify']
	username = GlobalUsers.objects.get(gus_email=request.user.gus_email,isused=0)
	if flag_code == '0':
		verify_code = str(random.randint(10000,99999))	
		username.gus_confirmcode = verify_code
		username.save()
		subject = "email verification HUL"            
		message = "please verify your email by typing the following code in your Distributor App " + verify_code
		sender = "hul@gmail.com"
		send_mail(subject, message, sender, [request.user.gus_email])
		data = False
	else:
		verify_code = str(request_data['otp'])
		if verify_code == request.user.gus_confirmcode:
			data = True
		else:
			data = False
	return HttpResponse(data)




      
       
    