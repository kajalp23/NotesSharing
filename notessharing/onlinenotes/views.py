
from onlinenotes.models import notes,Message,Room,notification
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as loginuser,logout as logoutuser
from onlinenotes.models import signup
import datetime
from django.http import HttpResponse, JsonResponse

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
    noti = notification.objects.all().order_by("date").reverse()
    return render(request,'onlinenotes/studashboard.html',{'allnote':allnote,'cnt':cnt,'cnt1':cnt1,'mynote':mynote,'noti':noti})

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
        return HttpResponseRedirect('/notes/stulogin/')
    return render(request,'onlinenotes/signup.html')

def contact(request):
    mapbox_access_token = 'pk.my_mapbox_access_token'
    return render(request, 'onlinenotes/contact.html', 
                  { 'mapbox_access_token': mapbox_access_token })

def stueditprofile(request,id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')
    if request.method=="POST":
        first_name = request.POST['fname']
        last_name = request.POST.get('lname')
        email = request.POST['email']
        contact = request.POST['contact']
        branch = request.POST['branch']
        User.objects.filter(username=request.user.username).update(first_name=first_name,last_name=last_name,email=email)
        fp = User.objects.get(id=id)
        signup.objects.filter(user=fp).update(contact=contact,branch=branch)
        user = User.objects.get(id=id)
        fm = signup.objects.get(user=user)
        return render(request,'onlinenotes/profile.html',{'fm':fm})
    user = User.objects.get(id=id)
    fm = signup.objects.get(user=user)
    return render(request,'onlinenotes/stueditprofile.html',{'fm':fm})

def editprofile(request,id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')
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
        try:
            getuser = User.objects.get(first_name=query)
        except:
            getuser = None
        if getuser is not None:
            results = signup.objects.filter(user=getuser)
        else:
            results = None
    accept = notes.objects.filter(status='accepted').count()
    all = notes.objects.all().count()
    reject = notes.objects.filter(status='rejected').count()
    pend = notes.objects.filter(status='pending').count()
    context={'query': query, 'results': results,'accept':accept,'all':all,'reject':reject,'pend':pend}
    return render(request, 'onlinenotes/searchuser.html', context)

def assignstatus(request,id):
    if request.method=="POST":
        fm = notes.objects.filter(id=id)
        status = request.POST['status']
        fm.update(status=status)
        if status=="accepted":
            fp = notes.objects.get(id=id)
            msg = fp.user.username + " added notes"
            p = notification(msg=msg,url=fp.uploadingnotes.url)
            print("url" + fp.uploadingnotes.url)
            p.save()
        return HttpResponseRedirect('/notes/allnotes')
    return render(request,'onlinenotes/assignstatus.html',{'noteid':id})

def uploadnotes(request,id): 
    if request.method=="POST":
        branch = request.POST['branch']
        subject = request.POST['subject']
        filetype= request.POST['filetype']
        uploadingnotes = request.FILES['uploadingnotes']
        description = request.POST['description']
        status = "pending"
        date = datetime.date.today()
        userp = User.objects.get(id=id)
        fm = notes.objects.create(user=userp,branch=branch,subject=subject,filetype=filetype,
        uploadingnotes=uploadingnotes,description=description,status=status,date=date)
        fm.save()
        allnote = notes.objects.all().filter(status="accepted")
        cnt = allnote.count()
        user = User.objects.get(id=id)
        mynote = notes.objects.all().filter(user=user)
        cnt1 = mynote.count()
        return render(request,'onlinenotes/studashboard.html',{'allnote':allnote,'cnt':cnt,'cnt1':cnt1,'mynote':mynote})
    allnote = notes.objects.all().filter(status="accepted")
    cnt = allnote.count()
    user = User.objects.get(id=id)
    mynote = notes.objects.all().filter(user=user)
    cnt1 = mynote.count()
    return render(request,'onlinenotes/uploadnotes.html',{'allnote':allnote,'cnt':cnt,'cnt1':cnt1,'mynote':mynote})

def changepass(request,id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')
    allnote = notes.objects.all().filter(status="accepted")
    cnt = allnote.count()
    users = User.objects.get(id=id)
    mynote = notes.objects.all().filter(user=users)
    cnt1 = mynote.count()
    if request.method=="POST":
        newpass = request.POST['newpass']
        confpass = request.POST['confpass']
        if newpass!=confpass:
            return render(request,'onlinenotes/changepass.html',{'msg':'Password is not matching','allnote':allnote,'cnt':cnt,'cnt1':cnt1,'mynote':mynote})
        myuser = User.objects.get(username__exact=request.user.username)
        myuser.set_password(newpass)
        myuser.save()
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

def searchnotes(request):
    results = []
    if request.method == "GET":
        query = request.GET.get('subquery')
        if query == '':
            query = 'None'
        try:
            results = notes.objects.filter(subject=query,status="accepted")
        except:
            results = None
    allnote = notes.objects.all().filter(status="accepted")
    cnt = allnote.count()
    user = User.objects.get(id=request.user.id)
    mynote = notes.objects.all().filter(user=user)
    cnt1 = mynote.count()
    context={'query': query, 'results': results,'allnote':allnote,'cnt':cnt,'mynote':mynote,'cnt1':cnt1}
    return render(request, 'onlinenotes/searchnotes.html', context)


#Chat App

def chat(request):
    return render(request, 'onlinenotes/chat.html')

def room(request, room):
    username = request.GET.get('username')
    try:
        room_details = Room.objects.get(name=room)
    except:
        room_details = None
    return render(request, 'onlinenotes/room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })

def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name=room).exists():
        return redirect('/'+room+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/'+room+'/?username='+username)

def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')

def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})