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
    path('studashboard/',views.studashboard,name="studashboard"),
    path('allnotes/',views.allnotes,name="allnotes"),
    path('deletenotes/<int:id>/',views.deletenotes,name="deletenotes"),
]