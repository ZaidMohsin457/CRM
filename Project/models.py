from django.db import connection

# Create your models here.
def create_table():
    with connection.cursor() as cursor:
        cursor.execute("""
                create table if not exists users
                (
                    u_id serial primary key,
                    u_name varchar(255),
                    u_email varchar(255),
                    constraint email_format_check check (u_email like '%_@__%.__%'),
                    password varchar(255)
                );
                
                create table if not exists clients
                (
                    c_id serial primary key,
                    c_name varchar(255),
                    c_phone_no varchar(255),
                    c_email varchar(255),
                    constraint email_format_check check (c_email like '%_@__%.__%'),
                    company_name varchar(255),
                    status varchar(255),
                    stage varchar(255),
                    new_or_old varchar(255),
                    country varchar(50),
                    user_id int,
                    foreign key(user_id) references users(u_id)
                );
                
                create table if not exists projects
                (
                    p_id serial primary key,
                    p_name varchar(255),
                    due_date date,
                    status varchar(100),
                    starting_date date,
                    user_id int,
                    client_id int,
                    foreign key(user_id) references users(u_id),
                    foreign key(client_id) references clients(c_id)
                );
                
                create table if not exists tasks
                (
                    task_id int,
                    project_id int,
                    task_name varchar(255),
                    foreign key(project_id) references projects(p_id),
                    primary key(project_id,task_id) 
                );
                create table if not exists meetings
                (
                    m_id serial primary key,
                    title varchar(255),
                    m_time time,
                    zoom_link varchar(100) not null ,
                    meetin_date date,
                    user_id int,
                    client_id int,
                    foreign key (user_id) references users(u_id),
                    foreign key(client_id) references clients(c_id)
                );
                
                create table if not exists employees
                (
                    e_id serial primary key,
                    e_name varchar(255),
                    designation varchar(255),
                    e_phone_no varchar(255),
                    e_email varchar(255),
                    constraint email_format_check check (e_email like '%_@__%.__%'),
                    gender varchar(255),
                    salary int,
                    user_id int,
                    country varchar(10),
                    foreign key(user_id) references users(u_id)
                );
                
                create table if not exists assigned
                (
                    project_id int,
                    emp_id int,
                    primary key(project_id,emp_id),
                    foreign key(project_id) references projects(p_id),
                    foreign key(emp_id) references employees(e_id)
                );
        """)
def insert_data_user(name,email,password):
    with connection.cursor() as cursor:
        cursor.execute(" INSERT INTO users (u_name,u_email,password) VALUES (%s,%s,%s);" ,[name,email,password])  

def retreive_data_user():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT u_email,password,u_id FROM users;
        """)
        data = cursor.fetchall()
    return data

def retrieve_emp_data(user_id):
    with connection.cursor() as cursor:
        cursor.execute("""
             SELECT e.e_name, e.designation, e_phone_no, p.p_name 
FROM employees e
LEFT JOIN assigned a ON e.e_id = a.emp_id
LEFT JOIN projects p ON p.p_id = a.project_id
GROUP BY e.e_name, e.designation, e_phone_no, p.p_name;

        """)
        data = cursor.fetchall()
    return data

def retreive_data_employee():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT e_email from employees;
        """)
        data = cursor.fetchall()
    return data

def insert_data_employee(name,designation,phone,email,gender,country,salary,user_id):
    with connection.cursor() as cursor:
        cursor.execute(" INSERT INTO employees (e_name,designation,e_phone_no,e_email,gender,country,salary,user_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);" ,[name,designation,phone,email,gender,country,salary,user_id])
        
def retreive_no_of_employee(user_id):
    with connection.cursor() as cursor:
        cursor.execute("""
            select count(e_id) from employees where user_id=%s;
        """,[user_id])
        data = cursor.fetchone()
    return data  

def retreive_projects():
    with connection.cursor() as cursor:
        cursor.execute("""
            select p_name,c_name,due_date from projects;
        """)
        data = cursor.fetchall()
    return data


def retreive_data_client():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT c_email from clients;
        """)
        data = cursor.fetchall()
    return data


def insert_data_client(name,phone,email,company,status,stage,new,user_id,country):
    with connection.cursor() as cursor:
        cursor.execute(" INSERT INTO clients (c_name,c_phone_no,c_email,company_name,status,stage,new_or_old,user_id,country) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"
                       ,[name,phone,email,company,status,stage,new,user_id,country])
        
        
        
def retreive_meeting_data():
    with connection.cursor() as cursor:
        cursor.execute("""Select m_time from meetings;""")  
        data = cursor.fetchall() 
    return data    

 
def insert_data_meeting(title,date,time,wit,link,user_id):
    with connection.cursor() as cursor:
        cursor.execute(" INSERT INTO meetings (title,meetin_date,m_time,client_id,zoom_link,user_id) VALUES (%s,%s,%s,%s,%s,%s);"
                       ,[title,date,time,wit,link,user_id])
        
def insert_data_projects(proj,std,dud,sts,user_id):
    with connection.cursor() as cursor:
        cursor.execute(" INSERT INTO projects (p_name,starting_date,due_date,status,user_id) VALUES (%s,%s,%s,%s,%s);"
                       ,[proj,std,dud,sts,user_id])
        # cursor.execute(" INSERT INTO assigned () VALUES (%s,%s,%s,%s,%s,%s);"
        #                ,[proj,cli_id,std,dud,sts,user_id])