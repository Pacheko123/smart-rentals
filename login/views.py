import requests
from django.http import HttpResponse, JsonResponse
from requests.auth import HTTPBasicAuth
import json
from django.shortcuts import render
from django.shortcuts import redirect
from .models import  Tuser
from . mpesa_credentials import MpesaAccessToken, LipanaMpesaPpassword
import re

# mmpesa imports


# Create your views here.
def index(request):
	context={
	'stm':'Hello There'
	}
	return render(request,'login/index.html',context)

def log(request):
	if request.method == 'POST':

		name = request.POST['username']
		username = request.POST['password']

		username = str(username)

		query = Tuser.objects.filter(username = name,password = username).exists()
		# password = Tuser.Objects.get(password = password)

		if query:
			# return HttpResponse("Details in Database")
			request.session['username'] = name
			context={
			'stm':'Details exists in the Database'
			}
			return render(request,'login/dashboard.html',context)

		else:
			return HttpResponse("Details Mismatch")
	else:
		return render(request,'login/login.html')

def register(request):
	if request.method == "POST":
		email = request.POST['mail']
		username = request.POST['username']
		password = request.POST['password']

		if password == request.POST['cpassword']:
			user1 = Tuser(username = username , password= password , mail = email)
			user1.save()
			return redirect("log")
		else:
			return HttpResponse("password does not match")
	else:
		return render(request,'login/register.html')

def dashboard(request):
	if 'username' not in request.session:
		return render(request,'login/login.html')
	else:
		return render(request,'login/dashboard.html')

def getAccessToken(request):
    consumer_key = 'EYGsE99F8jnF0smLsOF9imMwsYvA8KNA'
    consumer_secret = '2VMAr9hwlzIAJdFg'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    # global validated_mpesa_access_token
    validated_mpesa_access_token = mpesa_access_token['access_token']
    return HttpResponse(validated_mpesa_access_token)

def mpesa(request):

	if request.method == "POST":
		phone = request.POST['phone']
		amount = request.POST['amount']

		phone = re.sub('0', '254', phone, 1)
		print(phone)
		phone = int(phone)
		access_token = MpesaAccessToken.validated_mpesa_access_token
		api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
		# api_url = "https://sandbox.safaricom.co.ke/"
		auth = {
		  "Content-Type": "application/json",
		  "Authorization": "Bearer %s" % access_token
		}

		payload = {
		    "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
		    "Password": LipanaMpesaPpassword.decode_password,
		    "Timestamp": LipanaMpesaPpassword.lipa_time,
		    "TransactionType": "CustomerPayBillOnline",
		    "Amount": amount,
		    "PartyA":phone,
		    "PartyB": LipanaMpesaPpassword.Business_short_code,
		    "PhoneNumber": phone,
		    "CallBackURL": "https://pacheko.com/",
		    "AccountReference": "Pacheko Consortium",
		    "TransactionDesc": "Payment of goods"
		  }

		# response = requests.post(api_url, headers=auth, data=payload)
		payload1 = json.dumps(payload)
		response = requests.request("POST", api_url, headers = auth, data = payload1)
		return HttpResponse(response)

	else:
		return render(request,'login/mpesa.html')
