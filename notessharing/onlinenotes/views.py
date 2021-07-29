from onlinenotes.models import notes
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as loginuser,logout as logoutuser
from onlinenotes.models import signup
import datetime
from django.urls import reverse
from django.db.models import Q
from django.core.files.storage import FileSystemStorage

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
    accept = notes.objects.filter(status='accepted').count()
    all = notes.objects.all().count()
    reject = notes.objects.filter(status='rejected').count()
    pend = notes.objects.filter(status='pending').count()
    context={'alluser':alluser,'accept':accept,'all':all,'reject':reject,'pend':pend}
    return render(request,'onlinenotes/admindashboard.html',context)

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

def studashboard(request,id):
    allnote = notes.objects.all().filter(status="accepted")
    cnt = allnote.count()
    user = User.objects.get(id=id)
    mynote = notes.objects.all().filter(user=user)
    cnt1 = mynote.count()
    return render(request,'onlinenotes/studashboard.html',{'allnote':allnote,'cnt':cnt,'cnt1':cnt1,'mynote':mynote})

def stulogin(request):
    if not request.user.is_authenticated:
        if request.method=="POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                loginuser(request, user)
                return studashboard(request,user.id)
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

def stueditprofile(request,id):
    if request.method=="POST":
        email = request.POST['email']
        contact = request.POST['contact']
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        branch = request.POST['branch']
        User.objects.filter(id=id).update(first_name=first_name,last_name=last_name,email=email)
        fp = User.objects.get(id=id)
        signup.objects.filter(user=fp).update(contact=contact,branch=branch)
        user = User.objects.get(id=id)
        fm = signup.objects.get(user=user)
        return render(request,'onlinenotes/profile.html',{'fm':fm})
    user = User.objects.get(id=id)
    fm = signup.objects.get(user=user)
    return render(request,'onlinenotes/stueditprofile.html',{'fm':fm})

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
    user = User.objects.get(id=id)
    if not user.is_superuser:
        fm = signup.objects.get(user=user)
        return render(request,'onlinenotes/profile.html',{'fm':fm})
    else:
        return render(request,'onlinenotes/profile.html')

def allnotes(request):
    allnote = notes.objects.all()
    accept = notes.objects.filter(status='accepted').count()
    all = notes.objects.all().count()
    reject = notes.objects.filter(status='rejected').count()
    pend = notes.objects.filter(status='pending').count()
    context={'allnote':allnote,'accept':accept,'all':all,'reject':reject,'pend':pend}
    return render(request,'onlinenotes/allnotes.html',context)

def deletenotes(request,id):
    fm = notes.objects.get(id=id)
    fm.delete()
    return HttpResponseRedirect('/notes/allnotes/')

def pendingnotes(request):
    allnote = notes.objects.all().filter(status="pending")
    accept = notes.objects.filter(status='accepted').count()
    all = notes.objects.all().count()
    reject = notes.objects.filter(status='rejected').count()
    pend = notes.objects.filter(status='pending').count()
    context={'allnote':allnote,'accept':accept,'all':all,'reject':reject,'pend':pend}
    return render(request,'onlinenotes/pendingnotes.html',context)

def acceptednotes(request):
    allnote = notes.objects.all().filter(status="accepted")
    accept = notes.objects.filter(status='accepted').count()
    all = notes.objects.all().count()
    reject = notes.objects.filter(status='rejected').count()
    pend = notes.objects.filter(status='pending').count()
    context={'allnote':allnote,'accept':accept,'all':all,'reject':reject,'pend':pend}
    return render(request,'onlinenotes/acceptednotes.html',context)

def rejectednotes(request):
    allnote = notes.objects.all().filter(status="rejected")
    accept = notes.objects.filter(status='accepted').count()
    all = notes.objects.all().count()
    reject = notes.objects.filter(status='rejected').count()
    pend = notes.objects.filter(status='pending').count()
    context={'allnote':allnote,'accept':accept,'all':all,'reject':reject,'pend':pend}
    return render(request,'onlinenotes/rejectednotes.html',context)

def search(request):
    results = []
    if request.method == "GET":
        query = request.GET.get('subquery')
        if query == '':
            query = 'None'
        getuser = User.objects.get(first_name=query)
        results = signup.objects.filter(user=getuser)
    accept = notes.objects.filter(status='accepted').count()
    all = notes.objects.all().count()
    reject = notes.objects.filter(status='rejected').count()
    pend = notes.objects.filter(status='pending').count()
    print(query)
    print(results)
    context={'query': query, 'results': results,'accept':accept,'all':all,'reject':reject,'pend':pend}
    return render(request, 'onlinenotes/searchuser.html', context)

def assignstatus(request,id):
    if request.method=="POST":
        fm = notes.objects.filter(id=id)
        status = request.POST['status']
        fm.update(status=status)
        return HttpResponseRedirect('/notes/allnotes')
    return render(request,'onlinenotes/assignstatus.html',{'noteid':id})

def uploadnotes(request,id):
    allnote = notes.objects.all().filter(status="accepted")
    cnt = allnote.count()
    user = User.objects.get(id=id)
    mynote = notes.objects.all().filter(user=user)
    cnt1 = mynote.count()
    if request.method=="POST":
        branch = request.POST['branch']
        subject = request.POST['subject']
        filetype= request.POST['filetype']
        uploadingnotes = request.FILES.get('uploadingnotes')
        description = request.POST['description']
        status = "pending"
        date = datetime.date.today()
        user = User.objects.get(id=id)
        fm = notes.objects.create(user=user,branch=branch,subject=subject,filetype=filetype,
        uploadingnotes=uploadingnotes,description=description,status=status,date=date)
        fm.save()
        return render(request,'onlinenotes/studashboard.html',{'allnote':allnote,'cnt':cnt,'cnt1':cnt1,'mynote':mynote})
    return render(request,'onlinenotes/uploadnotes.html',{'allnote':allnote,'cnt':cnt,'cnt1':cnt1,'mynote':mynote})

def changepass(request,id):
    allnote = notes.objects.all().filter(status="accepted")
    cnt = allnote.count()
    user = User.objects.get(id=id)
    mynote = notes.objects.all().filter(user=user)
    cnt1 = mynote.count()
    if request.method=="POST":
        newpass = request.POST['newpass']
        confpass = request.POST['confpass']
        if newpass!=confpass:
            return render(request,'onlinenotes/changepass.html',{'msg':'Password is not matching','allnote':allnote,'cnt':cnt,'cnt1':cnt1,'mynote':mynote})
        user = User.objects.filter(id=id)
        user.update(password=newpass)
        return render(request,'onlinenotes/changepass.html',{'msg':'Password Updated Successfully','allnote':allnote,'cnt':cnt,'cnt1':cnt1,'mynote':mynote})
    return render(request,'onlinenotes/changepass.html',{'allnote':allnote,'cnt':cnt,'cnt1':cnt1,'mynote':mynote})

def viewallnotes(request,id):
    allnote = notes.objects.all().filter(status="accepted")
    cnt = allnote.count()
    user = User.objects.get(id=id)
    mynote = notes.objects.all().filter(user=user)
    cnt1 = mynote.count()
    return render(request,'onlinenotes/viewallnotes.html',{'allnote':allnote,'cnt':cnt,'cnt1':cnt1,'mynote':mynote})

def viewmynotes(request,id):
    allnote = notes.objects.all().filter(status="accepted")
    cnt = allnote.count()
    user = User.objects.get(id=id)
    mynote = notes.objects.all().filter(user=user)
    cnt1 = mynote.count()
    return render(request,'onlinenotes/viewmynotes.html',{'allnote':allnote,'cnt':cnt,'cnt1':cnt1,'mynote':mynote})