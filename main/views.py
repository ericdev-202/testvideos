from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.auth.models import User
from .models import Posts
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomSignupForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
import stripe
from django.http import HttpResponse
from django.http import HttpResponse, JsonResponse
import requests
from requests.auth import HTTPBasicAuth
import json
from .mpesa_credentials import MpesaAccessToken, LipanaMpesaPpassword
from django.views.decorators.csrf import csrf_exempt
from .models import MpesaPayment




stripe.api_key = "sk_test_IypT2bqOfu6h6xTFVr0uMfX400ziXYWvkw"

# Create your views here.
def upload(request):
	if request.method == 'POST':
		title = request.POST['title']
		description = request.POST['description']
		post = request.FILES['fileName']
		membership_type = request.POST['membership_type']
		upload_video = Posts(title=title,description=description,post=post,membership_type=membership_type)
		upload_video.save()
		messages.success(request,'Video has been uploaded')
	return render(request,'upload.html')

# @login_required()
def watch_video(request, post_id):
	try:
		post = Posts.objects.get(id=post_id)
	except ObjectDoesNotExist:
		return render(request,'404.html')
	try:	
		net = Posts.objects.all().order_by('-id')
	except:
		messages.warning(request, 'no more videos.')
		return redirect('home')

	return render(request,'watch.html',{"post":post,'net':net})

def home(request):
	all_videos = Posts.objects.all().order_by('-id')
	return render(request,'home.html',{'all_videos':all_videos})

def video(request):
	if request.method == 'GET':
		obj = Posts.objects.all()
		return render(request,'home.html',{"obj":obj})
	
def join(request):
    return render(request, 'join.html')	

def plan(request,pk):
    plan = get_object_or_404(CourseHero, pk=pk)
    if plan.premium :
        if request.user.is_authenticated:
            try:
                if request.user.customer.membership:
                    return render(request, 'plan.html', {'plan':plan})
            except Customer.DoesNotExist:
                    return redirect('join')
        return redirect('join')
    else:
        return render(request, 'plan.html', {'plan':plan})


@login_required
def checkout(request):

    coupons = {'christmas':31, 'welcome':10}

    if request.method == 'POST':
        stripe_customer = stripe.Customer.create(email=request.user.email, source=request.POST['stripeToken'])
        plan = 'price_1IhW37C4G22E1tTDA5Z5v4ij'
        if request.POST['plan'] == 'yearly':
            plan = 'price_1IhW90C4G22E1tTDkM2DTALW'
        if request.POST['coupon'] in coupons:
            percentage = coupons[request.POST['coupon'].lower()]
            try:
                coupon = stripe.Coupon.create(duration='once', id=request.POST['coupon'].lower(),
                percent_off=percentage)
            except:
                pass
            subscription = stripe.Subscription.create(customer=stripe_customer.id,
            items=[{'plan':plan}], coupon=request.POST['coupon'].lower())
        else:
            subscription = stripe.Subscription.create(customer=stripe_customer.id,
            items=[{'plan':plan}])

        customer = Customer()
        customer.user = request.user
        customer.stripeid = stripe_customer.id
        customer.membership = True
        customer.cancel_at_period_end = False
        customer.stripe_subscription_id = subscription.id
        customer.save()

        return redirect('home')
    else:
        coupon = 'none'
        plan = 'monthly'
        price = 2000
        og_dollar = 20
        coupon_dollar = 0
        final_dollar = 20
        if request.method == 'GET' and 'plan' in request.GET:
            if request.GET['plan'] == 'yearly':
                plan = 'yearly'
                price = 20000
                og_dollar = 200
                final_dollar = 200
        if request.method == 'GET' and 'coupon' in request.GET:
            print(coupons)
            if request.GET['coupon'].lower() in coupons:
                print('fam')
                coupon = request.GET['coupon'].lower()
                percentage = coupons[request.GET['coupon'].lower()]


                coupon_price = int((percentage / 100) * price)
                price = price - coupon_price
                coupon_dollar = str(coupon_price)[:-2] + '.' + str(coupon_price)[-2:]
                final_dollar = str(price)[:-2] + '.' + str(price)[-2:]

        return render(request, 'checkout.html',
        {'plan':plan,'coupon':coupon,'price':price,'og_dollar':og_dollar,
        'coupon_dollar':coupon_dollar,'final_dollar':final_dollar})

# def SignUp(request):
# 	return render(request,'register.html')
     
# class SignUp(generic.CreateView):
#     form_class = CustomSignupForm
#     success_url = reverse_lazy('home')
#     template_name = 'register.html'

#     def form_valid(self, form):
#         valid = super(SignUp, self).form_valid(form)
#         username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
#         new_user = authenticate(username=username, password=password)
#         login(self.request, new_user)
#         return valid
def SignUp(request):
	form = CustomSignupForm()

	if request.method == 'POST':
		form = CustomSignupForm(request.POST)
		if form.is_valid():
			form.save()
			

	context = {'form':form}
	return render(request,'register.html',context)

def login(request):
	return render(request,'login.html')




def settings(request):
    membership = False
    cancel_at_period_end = False
    if request.method == 'POST':
        subscription = stripe.Subscription.retrieve(request.user.customer.stripe_subscription_id)
        subscription.cancel_at_period_end = True
        request.user.customer.cancel_at_period_end = True
        cancel_at_period_end = True
        subscription.save()
        request.user.customer.save()
    else:
        try:
            if request.user.customer.membership:
                membership = True
            if request.user.customer.cancel_at_period_end:
                cancel_at_period_end = True
        except Customer.DoesNotExist:
            membership = False
    return render(request, 'settings.html', {'membership':membership,
    'cancel_at_period_end':cancel_at_period_end})

   

def getAccessToken(request):
    consumer_key = 'v20oRdzQFADypH9w1PWnEuKRjOTkTXAq'
    consumer_secret = 'z0b7w3gsuePmP9Fu'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']

    return HttpResponse(validated_mpesa_access_token)


def lipa_na_mpesa_online(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % access_token}
    request = {
        "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
        "Password": LipanaMpesaPpassword.decode_password,
        "Timestamp": LipanaMpesaPpassword.lipa_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 1,
        "PartyA": 254708374149,  # replace with your phone number to get stk push
        "PartyB": 174379,
        "PhoneNumber": 254708374149,  # replace with your phone number to get stk push
        "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
        "AccountReference": "CompanyXLTD",
        "TransactionDesc": "Testing stk push"
    }

    response = requests.post(api_url, json=request, headers=headers)
    return HttpResponse('success')


@csrf_exempt
def register_urls(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization": "Bearer %s" % access_token}
    options = {"ShortCode": LipanaMpesaPpassword.Test_c2b_shortcode,
               "ResponseType": "Completed",
               "ConfirmationURL": "https://79372821.ngrok.io/api/v1/c2b/confirmation",
               "ValidationURL": "https://79372821.ngrok.io/api/v1/c2b/validation"}
    response = requests.post(api_url, json=options, headers=headers)

    return HttpResponse(response.text)


@csrf_exempt
def call_back(request):
    pass


@csrf_exempt
def validation(request):

    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    return JsonResponse(dict(context))


@csrf_exempt
def confirmation(request):
    mpesa_body =request.body.decode('utf-8')
    mpesa_payment = json.loads(mpesa_body)

    payment = MpesaPayment(
        first_name=mpesa_payment['FirstName'],
        last_name=mpesa_payment['LastName'],
        middle_name=mpesa_payment['MiddleName'],
        description=mpesa_payment['TransID'],
        phone_number=mpesa_payment['MSISDN'],
        amount=mpesa_payment['TransAmount'],
        reference=mpesa_payment['BillRefNumber'],
        organization_balance=mpesa_payment['OrgAccountBalance'],
        type=mpesa_payment['TransactionType'],

    )
    payment.save()

    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }

    return JsonResponse(dict(context))

