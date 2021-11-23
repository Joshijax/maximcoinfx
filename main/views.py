from django.shortcuts import render
from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
# from .forms import AgentUploadFileForm, AgentSignUpForm, ProfileUploadForm, ImageForm
import os
# from django.template import loader
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from main.models import Invest, Message, Payment_Method
from .token_generator import account_activation_token
# from PIL import Image
from functools import wraps



def wrappers(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)

    return wrapped

def is_logged_in(f):
    @wraps(f)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated == True:
            return redirect('main:dashboard')
        else:
           
            return f(request, *args, *kwargs)

    return wrap

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    # checking if the user exists, if the token is valid.
    if user is not None and account_activation_token.check_token(user, token):
        # if valid set active true
        user.is_active = True
        profile = user.profile # because of signal and one2one relation
        profile.email_confirm = True
        profile.save()
        # set signup_confirmation true

        user.save()
        
        

        messages.add_message(request, messages.SUCCESS, 'email authenticated')
        return redirect('main:login')
    else:
        messages.add_message(request, messages.WARNING, 'iNVALID LINK or EXPIRED')
        return redirect('/')

def resend(request, username):

    user = User.objects.get(username=username)
    try:
        current_site = get_current_site(request)
        email_subject = 'Activate Your Maximcoinfx Account'
        message = render_to_string('activate_account.html', {
                'user': user.username,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.id)),
                'token': account_activation_token.make_token(user),
            })
        to_email = user.email
        email = EmailMessage(email_subject, message, to=[to_email])
        email.content_subtype = 'html'
        email.send()
        messages.add_message(request, messages.SUCCESS, f'Email has been sent to {user.email}, check your email')
    except:
        messages.add_message(request, messages.ERROR, 'Something Went wrong try again...')
        return redirect('main:login')
    
    print('pomit', User.objects.get(username=username).profile.email_confirm)
    
    return redirect('main:login')

@csrf_exempt
def ContactUs(request):
    name = request.POST.get('name', None)
    phone = request.POST.get('phone', None)
    email = request.POST.get('email', None)
    message = request.POST.get('message', None)
    print(email, message)

    email_subject = f'{name} Just contacted you'
    message = render_to_string('contactemail.html', {
            'name': name,
            'phone': phone,
            'email': email,
            'message': message,
        })
    to_email = 'lavishspender210@gmail.com'
    email = EmailMessage(email_subject, message, to=[to_email])
    email.content_subtype = 'html'
    email.send()
    messages.add_message(request, messages.SUCCESS, 'Thank you for contacting us, we would get back to you soon')


    # try:
    #     current_site = get_current_site(request)
    #     email_subject = f'{name} Just contacted you'
    #     message = render_to_string('contactemail.html', {
    #             'name': name,
    #             'phone': phone,
    #             'email': email,
    #             'message': message,
    #         })
    #     to_email = email
    #     email = EmailMessage(email_subject, message, to=[to_email])
    #     email.content_subtype = 'html'
    #     email.send()
    #     messages.add_message(request, messages.SUCCESS, 'Thank you for contacting us, we would get back to you soon')

        
    # except:
    #     messages.add_message(request, messages.ERROR, 'Something Went wrong try again...')
        
    

    
    return JsonResponse({'message':'username Does not exist', 'message_type':'danger'})
    



def  Home(request):
    return render(request, 'home.html', {'media_url': settings.MEDIA_URL, 'media_root': settings.MEDIA_ROOT,})

@is_logged_in
@csrf_exempt
def  Login(request):
    
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        
        print(username, password, authenticate(username=username, password=password))
        
        if not User.objects.filter(username=username).exists():
            return JsonResponse({'message':'username Does not exist', 'message_type':'danger'})

        if not authenticate(username=username, password=password):
            return JsonResponse({'message':'password does not match', 'message_type':'warning'})

        if User.objects.get(username=username).profile.email_confirm is False:
            resend = reverse('main:resend', kwargs={'username':username})
            print(resend)
            print(User.objects.get(username=username).profile.email_confirm)
            return JsonResponse({'message': f'Email is not verified. click <a href="{resend}" style="color: blue;">here</a> to resend, if you have not recieved email-verification email...', 'message_type':'danger'})

        user = authenticate(username=username, password=password)

        login(request, user)
        request.session['username'] = username
        # if request.user.profile.role ==  'Agent':
        #     return JsonResponse({'success':'success',
        #     'redirect': reverse('main:register'),})

        return JsonResponse({'message':'success', 'redirect': reverse('main:dashboard'), 'message_type':'success'})

        # load1 = request.POST.get('load1', None)
    return render(request, 'login.html', {'media_url': settings.MEDIA_URL, 'media_root': settings.MEDIA_ROOT,})

@is_logged_in
@csrf_exempt
def Register(request):
    ref = request.GET.get('referral')
    print(ref)
    if request.method == 'POST':


        firstname = request.POST.get('name', None)
        lastname = request.POST.get('lastname', None)
        username = request.POST.get('username', None)
        emaill = request.POST.get('email', None)
        password1 = request.POST.get('password', None)
        password2 = request.POST.get('password2', None)
        phone = request.POST.get('phone', None)
        print(firstname, lastname, username, emaill, password1, password2, phone)
        if User.objects.filter(username=username).exists():
            print('1 vv')
            return JsonResponse({'message':'username already exists', 'message_type':'danger'})

        if User.objects.filter(email=emaill).exists():
            print('2 vv')
            return JsonResponse({'message':'email already in use','message_type':'danger'})

        if len(password1) < 5:
            print('3 vv')
            return JsonResponse({'message':'password should be greater than 5', 'message_type':'warning'})
        user = User.objects.create(
            first_name = firstname,
            last_name = lastname,
            username = username,
            email = emaill,
            password = make_password(password1),
        )

        current_site = get_current_site(request)
        email_subject = 'Activate Your Maximcoinfx Account'
        message = render_to_string('activate_account.html', {
                'user': user.username,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.id)),
                'token': account_activation_token.make_token(user),
            })
        to_email = emaill
        email = EmailMessage(email_subject, message, to=[to_email])
        email.content_subtype = 'html'
        email.send()


        user =  User.objects.get(username=username,)
        profile = user.profile # because of signal and one2one relation
        profile.phone = phone
        profile.save()
        messages.add_message(request, messages.SUCCESS, 'Successfully created account, confirm email to login')

        return JsonResponse({'message':'Succesfully created your account', 'redirect': reverse('main:login'), 'message_type':'success'})
    return render(request, 'register.html', {'media_url': settings.MEDIA_URL, 'media_root': settings.MEDIA_ROOT, 'ref': ref,})

@login_required(login_url='/Login')
def  Dashboard(request):
    invest = Invest.objects.all()
    user= request.user
    print(User._meta.get_fields(), user.profile.phone)
    return render(request, 'dashboard.html', {'media_url': settings.MEDIA_URL, 'invest': invest,})

def  About(request):
    return render(request, 'about.html', {'media_url': settings.MEDIA_URL, 'media_root': settings.MEDIA_ROOT,})

def  contact(request):
    return render(request, 'contact.html', {'media_url': settings.MEDIA_URL, 'media_root': settings.MEDIA_ROOT,})


@login_required(login_url='/Login')
def  Investments(request):
    invest = Invest.objects.all()
    pay = Payment_Method.objects.all()
    return render(request, 'invest.html', {'media_url': settings.MEDIA_URL, 'invest': invest, 'pay': pay,})

@login_required(login_url='/Login')
@csrf_exempt
def  Funds(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        amount = request.POST.get('amount', None)
        method1 = request.POST.get('method', None)
        des = request.POST.get('des', None)

        try:
            current_site = get_current_site(request)
            email_subject = f'{username} Just Requested withdrawal'
            message = render_to_string('requestemail.html', {
                    'username': username,
                    'amount': amount,
                    'method': method1,
                    'des': des,
                })
            to_email = 'lavishspender210@gmail.com'
            email = EmailMessage(email_subject, message, to=[to_email])
            email.content_subtype = 'html'
            email.send()
            # messages.add_message(request, messages.SUCCESS, 'Thank you for contacting us, we would get back to you soon')

            
        except:
            return JsonResponse({'message':'Something happened try again', 'redirect': reverse('main:login'), 'message_type':'danger'})
            
            



        return JsonResponse({'message':'Withdraw request has been received, Recieve response within 72 hours', 'redirect': reverse('main:login'), 'message_type':'success'})

     
    return render(request, 'funds.html', {'media_url': settings.MEDIA_URL,})


@login_required(login_url='/Login')
@csrf_exempt
def  loadmessage(request):
    current_site = get_current_site(request)
    emaill = request.POST.get('email', None)
    paymethod = request.POST.get('paymethod', None)
    user = User.objects.get(email=emaill)
    
    print(emaill, user.username)
    email_subject = f'{user.username} Just made an investment'
    message = render_to_string('investmsg.html', {
            'user': user,
            'domain': current_site.domain,
        })
    to_email = 'lavishspender210@gmail.com'
    email = EmailMessage(email_subject, message, to=[to_email])
    email.content_subtype = 'html'
    email.send()

    msg = Message.objects.all()
    main_msg = Payment_Method.objects.get(name=paymethod)
    print(paymethod, main_msg.Message)

    email_subject1 = f' Hello {user.username} Investment recieved'
    message1 = render_to_string('investmsg2.html', {
            'user': user,
            'msg': msg,
            'domain': current_site.domain,
        })
    to_email1 = emaill
    email = EmailMessage(email_subject1, message1, to=[to_email1])
    email.content_subtype = 'html'
    email.send()
    return render(request, 'includes/message.html', {'media_url': settings.MEDIA_URL,'message': msg,'mainMsg': main_msg})

def  Services(request):
    
    return render(request, 'service.html', {'media_url': settings.MEDIA_URL})

def  package(request):
    
    return render(request, 'package.html', {'media_url': settings.MEDIA_URL})

def  noti(request):
    
    return render(request, 'notification.html', {'media_url': settings.MEDIA_URL})



def handler404(request, exception):
    return render(request, '404.html')


def logout_request(request):

    logout(request)
    

    return redirect('main:login')
  

class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'registration/password_reset_form.html'
