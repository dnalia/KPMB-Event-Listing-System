from django.contrib import admin
from .models import Student, Organizer, Event, Registration, Feedback

# Register your models here
admin.site.register(Student)
admin.site.register(Organizer)
admin.site.register(Event)
admin.site.register(Registration)
admin.site.register(Feedback)