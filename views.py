from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages
from django.db.models import Q

# Create your views here.
#def login_view(request):
    #return render(request,"main_page/login_page.html")
def registration_view(request):
    if request.method=='POST':
        username=request.POST['first_name']
        phone_nos=request.POST['phone']
        password1=request.POST['password1']
        password2=request.POST['password2']

        if password1==password2:
            if User.objects.filter(last_name=phone_nos).exists():
                #m=messages.info(request,'sorry baby')
                m="number already registered"
                return render(request,'main_page/registration_page.html',{"messages":m})
            else:
                #hello=userno()
                #ello.username=username
                #hello.phone_no=phone_nos

                user = User.objects.create_user(username=username,password=password1,first_name=username,last_name=phone_nos)

                user.save()
                #hello.save()
                print('user created')
        else:
            print('not matching')
            return render(request,'main_page/registration_page.html')
        return redirect('/')
    else:
        return render(request,'main_page/registration_page.html')

@login_required(login_url="login/")
def hello(request):
    return render(request,'main_page/hello.html')


def otp_view(request):
    return render(request,"main_page/otp_page.html")


def login_view(request):
    data={}
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']

        user= authenticate(request,username=username,password=password)

        if user:
            login(request,user)
            return HttpResponseRedirect('/hello/')
        else:
            data['error']="invalid"
            return render(request,'main_page/login_page.html',data)
    else:
        return render(request,'main_page/login_page.html')
def user_logout(request):
    logout(request)
    x='you r SUCCESSFULLY logout'
    return render(request,'main_page/login_page.html',{'x':x})
def crop_view(request):
    crop=crops.objects.all()
    return render(request,'main_page/crop.html',{'crop':crop})
def search(request):
    if request.method=="POST":
        srch=request.POST['srh']
        if srch:
            match=crops.objects.filter(Q(crop__icontains=srch) | Q(soil__icontains=srch))
            if match:
                return render(request,'main_page/search.html',{'sr':match})
            else:
                messages.error(request,'no result found')
        else:
            return HttpResponseRedirect('/search/')
    return render(request,'main_page/search.html')
