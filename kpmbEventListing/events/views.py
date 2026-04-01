from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from events.models import Student, Organizer, Event, Registration, Feedback

def homepage(request):
    return render(request, 'homepage.html')

def index(request):
    return render(request, 'index.html')

# Student Registration (POST)
def student_register(request):
    if request.method == 'POST':
        studid = request.POST.get('studid')
        studname = request.POST.get('studname')
        studprogramme = request.POST.get('studprogramme')
        studpass = request.POST.get('studpass')

        if Student.objects.filter(studid=studid).exists():
            return render(request, 'student_register.html', {'error': "Student ID already exists."})

        Student.objects.create(studid=studid, studname=studname, studprogramme=studprogramme, studpass=studpass)
        return redirect('student_login')

    return render(request, 'student_register.html')

# Student Login (GET and POST)
def student_login(request):
    if request.method == 'POST':
        studid = request.POST['studid']
        studpass = request.POST['studpass']
        try:
            student = Student.objects.get(studid=studid, studpass=studpass)
            return redirect('student_dashboard', student_id=student.studid)
        except Student.DoesNotExist:
            return render(request, "student_login.html", {'error': "Invalid ID or password."})

    return render(request, "student_login.html")

# Organizer Registration (POST)
def organizer_register(request):
    if request.method == 'POST':
        orgid = request.POST['orgid']
        orgname = request.POST['orgname']
        orgemail = request.POST['orgemail']
        orgpass = request.POST['orgpass']

        if Organizer.objects.filter(orgid=orgid).exists():
            return render(request, 'organizer_register.html', {'error': "Organizer ID already exists."})

        if Organizer.objects.filter(orgemail=orgemail).exists():
            return render(request, 'organizer_register.html', {'error': "Email already registered."})

        Organizer.objects.create(orgid=orgid, orgname=orgname, orgemail=orgemail, orgpass=orgpass)
        return redirect('organizer_login')

    return render(request, 'organizer_register.html')

# Organizer Login (GET and POST)
def organizer_login(request):
    if request.method == 'POST':
        orgid = request.POST['orgid']
        orgpass = request.POST['orgpass']
        try:
            organizer = Organizer.objects.get(orgid=orgid, orgpass=orgpass)
            return redirect('event_list', organizer_id=organizer.orgid)
        except Organizer.DoesNotExist:
            return render(request, "organizer_login.html", {'error': "Invalid ID or password."})

    return render(request, "organizer_login.html")

# Event List (GET)
def event_list(request, organizer_id):
    organizer = Organizer.objects.filter(orgid=organizer_id).first()  

    if organizer is None:
        return render(request, "event_list.html", {'error': "Organizer not found."})

    events = Event.objects.filter(org=organizer)

    return render(request, "event_list.html", {'organizer': organizer, 'events': events})

# Add Event (POST)
def add_event(request, organizer_id):
    organizer = Organizer.objects.filter(orgid=organizer_id).first()  
    
    if organizer is None:
        return render(request, "add_event.html", {'error': "Organizer not found."})

    if request.method == 'POST':
        event_name = request.POST['eventname']
        event_description = request.POST['description']
        event_date = request.POST['date']
        
        new_event = Event(org=organizer, eventname=event_name, description=event_description, date=event_date)
        new_event.save() 
        return redirect('event_list', organizer_id=organizer_id)
    
    return render(request, "add_event.html", {'organizer': organizer})

# Update Event Date (PUT)
def update_event_date(request, organizer_id, event_id):
    event = Event.objects.filter(id=event_id, org__orgid=organizer_id).first()

    if event is None:
        return render(request, "update_event_date.html", {'error': "Event not found."})

    if request.method == 'POST':
        new_date = request.POST['date']
        event.date = new_date
        event.save() 
        return redirect('event_list', organizer_id=organizer_id)

    return render(request, "update_event_date.html", {'event': event})

# Confirm Delete Event (DELETE)
def confirm_delete_event(request, organizer_id, event_id):
    event = Event.objects.filter(id=event_id, org__orgid=organizer_id).first() 

    if event is None:
        return render(request, "confirm_delete_event.html", {'error': "Event not found."})

    if request.method == 'POST':
        event.delete() 
        return redirect('event_list', organizer_id=organizer_id)

    return render(request, "confirm_delete_event.html", {'event': event})

# View Attendance
def view_attendance(request, organizer_id, event_id):
    event = Event.objects.filter(id=event_id, org__orgid=organizer_id).first() 

    if event is None:
        return render(request, 'attendance.html', {'error': "Event not found."})

    registrations = Registration.objects.filter(event=event)

    return render(request, 'view_attendance.html', {'event': event, 'registrations': registrations})

# Student Dashboard (GET)
def student_dashboard(request, student_id):
    student = Student.objects.filter(studid=student_id).first() 

    if student is None:
        return render(request, 'student_dashboard.html', {'error': 'Student does not exist.'})

    registrations = Registration.objects.filter(student=student)
    joined_events = [registration.event for registration in registrations]

    return render(request, 'student_dashboard.html', {'studname': student.studname, 'joined_events': joined_events, 'student': student})

# Add Feedback (POST)
def add_feedback(request, student_id, event_id):
    student = Student.objects.filter(studid=student_id).first()
    event = Event.objects.filter(id=event_id).first()

    if student is None or event is None:
        return render(request, 'add_feedback.html', {'error': "Student or event not found."})

    if request.method == 'POST':
        feedback_text = request.POST['feedback']
        Feedback.objects.create(student=student, event=event, feedback=feedback_text)
        return redirect('view_feedback', student_id=student.studid, event_id=event.id) 

    return render(request, 'add_feedback.html', {'student': student, 'event': event})

# Delete Feedback
def delete_feedback(request, student_id, event_id):
    if request.method == 'POST':
        feedback_id = request.POST.get('feedback_id')
        feedback = Feedback.objects.filter(id=feedback_id).first()

        if feedback:
            feedback.delete()  
        return redirect('view_feedback', student_id=student_id, event_id=event_id)

    return render(request, "delete_feedback.html")

# View Feedback
def view_feedback(request, student_id, event_id):
    event = Event.objects.filter(id=event_id).first()

    if event is None:
        return render(request, 'view_feedback.html', {'error': "Event not found."})
    
    feedback_list = Feedback.objects.filter(event=event)

    return render(request, 'view_feedback.html', {
        'feedback_list': feedback_list,
        'event': event,
        'student_id': student_id,
        'student': Student.objects.filter(studid=student_id).first()  # Ensure student object is available
    })

# Update Feedback
def update_feedback(request, student_id, event_id):
    student = Student.objects.get(studid=student_id)
    feedback_id = request.GET.get('feedback_id')  # Get feedback ID from query parameters
    feedback = Feedback.objects.filter(student=student, id=feedback_id, event__id=event_id).first()

    if request.method == 'POST':
        feedback_text = request.POST['feedback']
        feedback.feedback = feedback_text
        feedback.save()
        return redirect('view_feedback', student_id=student.studid, event_id=event_id)

    return render(request, 'update_feedback.html', {'student': student,'feedback': feedback,'event': Event.objects.get(id=event_id),'student_id': student_id,})


# Search Events by Organizer (GET)
def search_events_by_organizer(request, student_id):
    student = Student.objects.filter(studid=student_id).first() 
    if student is None:
        return render(request, 'student_dashboard.html', {'error': 'Student does not exist.'})

    query = request.GET.get('q', '')
    events = Event.objects.filter(org__orgname__icontains=query)

    return render(request, 'search_events_by_organizer.html', {'student': student, 'events': events})

# Confirm Join Event (POST)
# Confirm Join Event (POST)
def confirm_join_event(request, student_id, event_id):
    student = Student.objects.filter(studid=student_id).first()
    event = Event.objects.filter(id=event_id).first() 

    if student is None or event is None:
        return render(request, "confirm_join_event.html", {'error': "Student or event not found."})

    if request.method == 'POST':
        Registration.objects.create(student=student, event=event)  
        return redirect('student_dashboard', student_id=student_id)

    return render(request, "confirm_join_event.html", {'student': student, 'event': event})

