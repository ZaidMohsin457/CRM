from Project import views
from django.contrib import admin
from django.urls import path
from django.conf import settings # new
from  django.conf.urls.static import static #new
urlpatterns = [
    path("",views.index,name="MainPage"),
    path("login", views.login, name="Login"),
    path("signup", views.signup, name="Signup"),
    path("home", views.dashboard, name="Dashboard"),
    
    path("employee", views.employee, name="Employee"),
    path("add-new-employee", views.add_new_employee, name="AddNewEmployee"),
    path("employee-added", views.employee_added, name="EmployeeAdded"),
    
    path("meeting-scheduler", views.meeting_shcheduler, name="MeetingShcheduler"),
    path("meeting-added", views.meeting_added, name="MeetingAdded"),
    path("add-new-meeting", views.add_new_meeting, name="AddNewMeeting"),
    
    path("projects", views.project, name="Project"),
    path("add-new-project", views.add_new_project, name="AddNewProject"),
    path("project-added", views.project_added, name="ProjectAdded"),
    
    path("leads-pipeline", views.leads_pipeline, name="LeadsPipeline"),
    path("add-new-contact", views.add_new_contact, name="AddNewContact"),
    path("contact-added", views.contact_added, name="ContactAdded"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_URL)