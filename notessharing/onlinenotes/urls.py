from django.urls import path
from onlinenotes import views


urlpatterns = [
    path('login/',views.login,name="login"),
    path('logout/',views.logout,name="logout"),
    path('stulogin/',views.stulogin,name="stulogin"),
    path('signupuser/',views.signupuser,name="signupuser"),
    path('contact/',views.contact,name="contact"),
    path('profile/<int:id>/',views.profile,name="profile"),
    path('editprofile/<int:id>/',views.editprofile,name="editprofile"),
    path('delete/<int:id>/',views.deleteuser,name="delete"),
    path('admindashboard/',views.admindashboard,name="admindashboard"),   
    path('allnotes/',views.allnotes,name="allnotes"),
    path('deletenotes/<int:id>/',views.deletenotes,name="deletenotes"),
    path('pendingnotes/',views.pendingnotes,name="pendingnotes"),
    path('acceptednotes/',views.acceptednotes,name="acceptednotes"),
    path('rejectednotes/',views.rejectednotes,name="rejectednotes"),
    path('search/', views.search, name='search'),
    path('assignstatus/<int:id>/', views.assignstatus, name='assignstatus'),

    #student/teacher dashboard
    path('studashboard/<int:id>',views.studashboard,name="studashboard"),
    path('stueditprofile/<int:id>/',views.stueditprofile,name="stueditprofile"),
    path('uploadnotes/<int:id>/', views.uploadnotes, name='uploadnotes'),
    path('changepass/<int:id>/', views.changepass, name='changepass'),
    path('viewallnotes/<int:id>/', views.viewallnotes, name='viewallnotes'),
    path('viewmynotes/<int:id>/', views.viewmynotes, name='viewmynotes'),
    path('searchnotes/', views.searchnotes, name='searchnotes'),



]