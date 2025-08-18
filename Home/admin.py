from django.contrib import admin
from Home.models import SignupData, Events, Students, Booking
# Register your models here.

admin.site.register(SignupData)
admin.site.register(Events)
admin.site.register(Students)
admin.site.register(Booking)