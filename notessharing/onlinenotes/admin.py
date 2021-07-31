
from django.contrib import admin
from onlinenotes.models import signup,notes,Message,Room
# Register your models here.

admin.site.register(signup)
admin.site.register(notes)
admin.site.register(Message)
admin.site.register(Room)
