from django.contrib import admin
from .models import Room,Topic,message,User
# Register your models here.
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(message)
admin.site.register(User)