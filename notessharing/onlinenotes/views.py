from onlinenotes.models import notes
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as loginuser,logout as logoutuser
from onlinenotes.models import signup
from django.urls import reverse
import mimetypes

# Create your views here.

def home(request):
    return render(request,'onlinenotes/home.html')

def deleteuser(request,id):
    fm = signup.objects.get(id=id)
    fm.delete()
    # fk = User.objects.get(id=id)
    # fk.delete()
    return HttpResponseRedirect('/notes/admindashboard/')


def admindashboard(request):
    alluser = signup.objects.all()
    return render(request,'onlinenotes/admindashboard.html',{'alluser':alluser})

def login(request):
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            loginuser(request, user)
            return HttpResponseRedirect('/notes/admindashboard/')
    return render(request,'onlinenotes/login.html')

def logout(request):
    logoutuser(request)
    return HttpResponseRedirect('/')

def studashboard(request):
    return render(request,'onlinenotes/studashboard.html')

def stulogin(request):
    if not request.user.is_authenticated:
        if request.method=="POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                loginuser(request, user)
                return HttpResponseRedirect('/notes/studashboard/')
    return render(request,'onlinenotes/stulogin.html')

def signupuser(request):
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        contact = request.POST['contact']
        email = request.POST['email']
        branch = request.POST['branch']
        role = request.POST['role']
        user = User.objects.create_user(username=username,password=password,first_name=first_name,last_name=last_name,email=email)
        signup.objects.create(user=user,contact=contact,branch=branch,role=role)
       
        return render(request,'onlinenotes/stulogin.html')
    return render(request,'onlinenotes/signup.html')

def contact(request):
    mapbox_access_token = 'pk.my_mapbox_access_token'
    return render(request, 'onlinenotes/contact.html', 
                  { 'mapbox_access_token': mapbox_access_token })

def editprofilestu(request,id):
    if request.method=="POST":
        email = request.POST['email']
        contact = request.POST['contact']
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        branch = request.POST['branch']

        fm = User.objects.get(id=id).update(first_name=first_name)
        signup.objects.get(user=fm).update()

    return render(request,'onlinenotes/editprofile.html')

def editprofile(request,id):
    if request.method=="POST":
        email = request.POST['email']
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        fm = User.objects.filter(id=id)
        fm.update(first_name=first_name,last_name=last_name,email=email)
        return render(request,'onlinenotes/profile.html')
    fm = User.objects.get(id=id)
    return render(request,'onlinenotes/editprofile.html',{'fm':fm})

def profile(request,id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')
    return render(request,'onlinenotes/profile.html')

def allnotes(request):
    allnote = notes.objects.all()
    return render(request,'onlinenotes/allnotes.html',{'allnote':allnote})

def deletenotes(request,id):
    fm = notes.objects.get(id=id)
    fm.delete()
    return HttpResponseRedirect('/notes/allnotes/')