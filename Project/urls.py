from Project import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("",views.index,name="MainPage"),
    path("login", views.login, name="Login"),
    path("signup", views.signup, name="Signup"),
    path("home", views.dashboard, name="Dashboard"),
    path("employee", views.employee, name="Employee"),
    path("add-new-employee", views.add_new_employee, name="AddNewEmployee"),
    path("employee-added", views.employee_added, name="EmployeeAdded"),
    path("employee-details", views.employee_details, name="EmployeeDetails"),
    path("meeting-scheduler", views.meeting_shcheduler, name="MeetingShcheduler"),
    path("add-new-meeting", views.add_new_meeting, name="AddNewMeeting"),
    path("meeting-added", views.meeting_added, name="MeeitngAdded"),
    # path("meeting-added", views.meeting_added, name="MeetingAdded"),
    path("add-new-contact", views.add_new_contact, name="AddNewContact"),
    path("contact-added", views.contact_added, name="ContactAdded"),
    path("add-new-meeting", views.add_new_meeting, name="AddNewMeeting"),
    path("projects", views.project, name="Project"),
    path("add-new-project", views.add_new_project, name="AddNewProject"),
    path("project-added", views.project_added, name="ProjectAdded"),
    path('project-details', views.project_details, name='ProjectDetails'),
    path("leads-pipeline", views.leads_pipeline, name="LeadsPipeline"),
]