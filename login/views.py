import requests
import json
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse
from .models import  Tuser

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

def mpesa(request):
	
	if request.method == "POST":
		phone = request.POST['phone']
		amount = request.POST['amount']

		# import requests


		headers = {
		  'Content-Type': 'application/json',
		  'Authorization': 'Bearer cQGxbAl54zibmSJuo9e7SGNDW1AP'
		}

		payload = {
		    "BusinessShortCode": 174379,
		    "Password": "MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMjEwNjE3MTE0OTA2",
		    "Timestamp": "20210616221303",
		    "TransactionType": "CustomerPayBillOnline",
		    "Amount": amount,
		    "PartyA":phone,
		    "PartyB": 174379,
		    "PhoneNumber": phone,
		    "CallBackURL": "https://omugatvc.ac.ke/btc.html",								
		    "AccountReference": "Pacheko Inc",
		    "TransactionDesc": "Payment of goods" 
		  }
		response = requests.request("POST", 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest', headers = headers, data = payload)
		text = response.text.encode('utf8')
		print(response.text.encode('utf8'))
		context={
			'stm':text
		}

		# return JsonResponse(list(response), safe=False)
		return render(request,'login/response.html',context)

	else:
		return render(request,'login/mpesa.html')