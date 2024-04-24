from django.shortcuts import render
from Project import models
from Project import graphs

# Create your views here.
def index(request):
    return render(request,'desktop-1.html')
def login(request):
    return render(request,'login-page.html')
def signup(request):
    return render(request,'sign-up-page.html')
def dashboard(request):
    models.create_table()
    # models.insert_data()
    # graphs.bar_char()
    return render(request,'dashboard.html')
def employee(request):
    return render(request,'employees.html')
def add_new_employee(request):
    return render(request,'employee-add-a-new-employee.html')
def employee_added(request):
    return render(request,'employee-employee-added.html')
def employee_details(request):
    return render(request,'view-employee-profile.html')
def meeting_shcheduler(request):
    return render(request,'meeting-scheduler.html')
def add_new_meeting(request):
    return render(request,'add-a-new-meeting.html')
def add_new_contact(request):
    return render(request,'add-a-new-contact.html')
def project(request):
    return render(request,'projects.html')
def add_new_project(request):
    return render(request,'projects-add-a-new-project.html')
def project_added(request):
    return render(request,'projects-project-added.html')
def project_details(request):
    return render(request,'projects-view-details.html')
def leads_pipeline(request):
    return render(request,'leads-pipeline.html')
