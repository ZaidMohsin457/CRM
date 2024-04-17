from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'desktop-1.html')
def login(request):
    return render(request,'sign-up-page.html')
def signup(request):
    return render(request,'sign-up-page.html')
def dashboard(request):
    return render(request,'dashboard.html')
def employee(request):
    return render(request,'employees.html')
def add_new_employee(request):
    return render(request,'add-a-new-employee.html')
def employee_added(request):
    return render(request,'employee-added.html')
def employee_details(request):
    return render(request,'view-employee-profile.html')
def meeting_shcheduler(request):
    return render(request,'meeting-scheduler.html')
def add_new_meeting(request):
    return render(request,'add-a-new-meeting.html')
def add_new_contact(request):
    return render(request,'add-a-new-contact.html')
# def meeting_added(request):
#     return render(request,'meeting-added.html')
def project(request):
    return render(request,'projects.html')
def add_new_project(request):
    return render(request,'add-a-new-project.html')
def project_added(request):
    return render(request,'project-added.html')
def project_details(request):
    return render(request,'project-details.html')
def leads_pipeline(request):
    return render(request,'leads-pipeline.html')

