# Generated by Django 5.1.6 on 2025-02-07 08:37

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('c_id', models.AutoField(primary_key=True, serialize=False)),
                ('c_name', models.CharField(max_length=255)),
                ('c_phone_no', models.CharField(max_length=255)),
                ('c_email', models.CharField(max_length=255, validators=[django.core.validators.RegexValidator(message='Enter a valid email address.', regex='^[^@]+@[^@]+\\.[^@]+$')])),
                ('company_name', models.CharField(max_length=255)),
                ('status', models.CharField(max_length=255)),
                ('stage', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'clients',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('u_id', models.AutoField(primary_key=True, serialize=False)),
                ('u_name', models.CharField(max_length=255)),
                ('u_email', models.CharField(max_length=255, validators=[django.core.validators.RegexValidator(message='Enter a valid email address.', regex='^[^@]+@[^@]+\\.[^@]+$')])),
                ('password', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('p_id', models.AutoField(primary_key=True, serialize=False)),
                ('p_name', models.CharField(max_length=255)),
                ('due_date', models.DateField()),
                ('starting_date', models.DateField()),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Project.client')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Project.user')),
            ],
            options={
                'db_table': 'projects',
            },
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('m_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('m_time', models.TimeField()),
                ('zoom_link', models.CharField(max_length=100)),
                ('meetin_date', models.DateField()),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Project.client')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Project.user')),
            ],
            options={
                'db_table': 'meetings',
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('e_id', models.AutoField(primary_key=True, serialize=False)),
                ('e_name', models.CharField(max_length=255)),
                ('designation', models.CharField(max_length=255)),
                ('e_phone_no', models.CharField(max_length=255)),
                ('e_email', models.CharField(max_length=255, validators=[django.core.validators.RegexValidator(message='Enter a valid email address.', regex='^[^@]+@[^@]+\\.[^@]+$')])),
                ('date_of_hiring', models.DateField()),
                ('gender', models.CharField(max_length=255)),
                ('salary', models.IntegerField()),
                ('country', models.CharField(max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Project.user')),
            ],
            options={
                'db_table': 'employees',
            },
        ),
        migrations.AddField(
            model_name='client',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Project.user'),
        ),
        migrations.CreateModel(
            name='Assigned',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Project.employee')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Project.project')),
            ],
            options={
                'db_table': 'assigned',
                'unique_together': {('project', 'emp')},
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('task_id', models.AutoField(primary_key=True, serialize=False)),
                ('task_name', models.CharField(max_length=255)),
                ('status', models.CharField(default='pending', max_length=100)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Project.project')),
            ],
            options={
                'db_table': 'tasks',
                'unique_together': {('project', 'task_id')},
            },
        ),
    ]
