# Generated by Django 5.1.2 on 2024-10-14 17:10

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AddressDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('type', models.CharField(choices=[('temp', 'Temporary'), ('parmanent', 'Parmanent')], max_length=10)),
                ('house_no', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('pin_code', models.PositiveIntegerField()),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='address', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ContactDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('contact_number', models.PositiveBigIntegerField()),
                ('emergency_contact', models.PositiveBigIntegerField()),
                ('personal_email', models.EmailField(max_length=50)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contact', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('position_name', models.CharField(max_length=50)),
                ('level', models.CharField(choices=[('t1', 'T1'), ('t2', 'T2'), ('t3', 'T3'), ('t4', 'T4'), ('m1', 'M1'), ('m2', 'M2'), ('m3', 'M3'), ('m4', 'M4'), ('s1', 'S1'), ('s2', 'S2'), ('l1', 'L1'), ('l2', 'L2')], max_length=50)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EmployeeProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('marital_status', models.CharField(choices=[('single', 'Single'), ('married', 'Married'), ('widow', 'Widow')], max_length=20)),
                ('employee_user_id', models.CharField(max_length=20)),
                ('date_of_joining', models.DateField()),
                ('email_id', models.EmailField(max_length=50)),
                ('pan_number', models.CharField(max_length=10)),
                ('date_of_birth', models.DateField()),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employee_pro', to=settings.AUTH_USER_MODEL)),
                ('reporting_manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='manager', to=settings.AUTH_USER_MODEL)),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employeeprofile.position')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
