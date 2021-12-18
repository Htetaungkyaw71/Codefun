from django import http
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from codefun.decorators import currentuser_is_entry_author
from .models import User, Code
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db import IntegrityError
from django.core.mail import send_mail
import math,random
from django.core.paginator import Paginator





def generateOTP() :
     digits = "0123456789"
     OTP = ""
     for i in range(6) :
         OTP += digits[math.floor(random.random() * 10)]
     return OTP


@login_required(login_url='login')
def index(request):  
    if request.method == "POST":
       editor = request.POST["editor"]
       name = request.POST["name"]
       postchoice = request.POST["postchoice"]
       project = Code.objects.create(name=name,user=request.user,text=editor,postchoice=postchoice)
       project.save()
       return HttpResponseRedirect(reverse("main"))          
    return render(request,"codefun/index.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user,backend='django.contrib.auth.backends.ModelBackend')
            return HttpResponseRedirect(reverse("main"))
        else:
            return render(request,"codefun/login.html",{
                "message":"invalid account"
            })
    return render(request,"codefun/login.html")


def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        cpassword = request.POST["cpassword"]
        if password != cpassword:
            return render(request,"codefun/register.html",{
                "message":"password didn't match"
            })
        else:
            try:
                n = generateOTP()
                send_mail('OTP request key',n,'htetaung200071@gmail.com',[email], fail_silently=False)              
                user = User.objects.create_user(username=username,email=email,password=password,otp=n)
                user.save()    
                login(request,user,backend='django.contrib.auth.backends.ModelBackend') 
                return HttpResponseRedirect(reverse('otp'))
            except IntegrityError:
                return render(request,"codefun/register.html",{
                    "message":"username is already exists"
                })
    return render(request,"codefun/register.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("main"))


def otp_view(request):
    if request.method == "POST":
        otp = request.POST["otp"]
        user = User.objects.filter(otp=otp).first()
        if user:                     
            return HttpResponseRedirect(reverse("main"))
        else:
            user = User.objects.filter(username=request.user.username).first()
            user.delete()
            return render(request,"codefun/register.html",{
                "message":"otp number is wrong"
            })
    return render(request,"codefun/otp.html")


def main(request):
    if request.user.is_authenticated:
        private = Code.objects.filter(user=request.user).all()
        name = request.user.username[0].upper()
    else:
        private = Code.objects.all()
        name = None
    paginator = Paginator(Code.objects.filter(postchoice="public").all(), 9) 

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,"codefun/main.html",{
        "page_obj":page_obj,
        "privateprojects":private,
        "name":name
    })

def profile(request,id):
    user = User.objects.get(id=id)
    return render(request,"codefun/profile.html",{
        'user':user,
        "name":user.username[0].upper(),
        "projects":Code.objects.filter(user=user,postchoice="public").all()
    })


def detail(request,id):
    return render(request,"codefun/detail.html",{
        "project":Code.objects.get(id=id)
    })


@login_required(login_url='login')
def edit(request,id):
    project = Code.objects.get(id=id)
    if request.method == "POST":
       editor = request.POST["editor"]
       name = request.POST["name"]
       postchoice = request.POST["postchoice"]
       project.editor = editor
       project.name = name
       project.postchoice = postchoice
       project.user = request.user
       project.save()
       return HttpResponseRedirect(reverse("main"))   
    return render(request,"codefun/edit.html",{
        "project":project
    })



@login_required(login_url='login')
def delete(request,id):
    if Code.objects.filter(user=request.user).first():
        Code.objects.get(id=id).delete()
    return HttpResponseRedirect(reverse("main"))   



@login_required(login_url='login')
def editpp(request,id):
    user = User.objects.get(id=id)
    if request.user == user:
        if request.method == "POST":
            username = request.POST["username"]
            email = request.POST["email"]
            user.username = username
            user.email = email
            user.save()
            return HttpResponseRedirect(reverse('main'))
        return render(request,"codefun/main.html",{
            'user':user
        })
    return render(request,"codefun/error.html")


@login_required(login_url='login')
def deletepp(request):
    user = User.objects.get(id=request.user.id).delete()
    return HttpResponseRedirect(reverse('main'))

@login_required(login_url='login')
def search(request):
    if request.method == "GET":
        q = request.GET["q"]
        projects = Code.objects.filter(name__contains=q,postchoice="public").all()
        paginator = Paginator(projects, 9) 

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    return render(request,"codefun/search.html",{
        "page_obj":page_obj
    })





        
    