from django.db import models

# Create your models here.
class Student(models.Model):
    studid = models.CharField(max_length=100, unique=True)
    studname = models.CharField(max_length=200)
    studprogramme = models.CharField(max_length=100)
    studpass = models.CharField(max_length=100) 

class Organizer(models.Model):
    orgid = models.CharField(max_length=100, unique=True)
    orgname = models.CharField(max_length=200)
    orgemail = models.EmailField(unique=True)
    orgpass = models.CharField(max_length=100)  

class Event(models.Model):
    org = models.ForeignKey(Organizer, on_delete=models.CASCADE)
    eventname = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()

class Registration(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

class Feedback(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    feedback = models.TextField()