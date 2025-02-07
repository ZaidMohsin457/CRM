from django.contrib import admin
from .models import User, Client, Project, Task, Meeting, Employee, Assigned

# User Admin
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('u_id', 'u_name', 'u_email')  
    search_fields = ('u_name', 'u_email')  

# Client Admin
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('c_id', 'c_name', 'c_email', 'company_name', 'status', 'stage')
    search_fields = ('c_name', 'c_email', 'company_name')
    list_filter = ('status', 'stage')  

# Project Admin
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('p_id', 'p_name', 'due_date', 'starting_date', 'user', 'client')
    search_fields = ('p_name', 'client__c_name')
    list_filter = ('due_date', 'starting_date')

# Task Admin
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('task_id', 'task_name', 'status', 'project')
    search_fields = ('task_name',)
    list_filter = ('status',)

# Meeting Admin
@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ('m_id', 'title', 'meetin_date', 'm_time', 'client')
    search_fields = ('title', 'client__c_name')
    list_filter = ('meetin_date',)

# Employee Admin
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('e_id', 'e_name', 'designation', 'e_email', 'date_of_hiring', 'salary', 'user')
    search_fields = ('e_name', 'e_email', 'designation')
    list_filter = ('designation', 'date_of_hiring')

# Assigned Admin (Intermediate Table)
@admin.register(Assigned)
class AssignedAdmin(admin.ModelAdmin):
    list_display = ('project', 'emp')
    search_fields = ('project__p_name', 'emp__e_name')
