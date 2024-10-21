# Generated by Django 5.1.2 on 2024-10-20 06:03

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employeeprofile', '0002_alter_addressdetails_type_accountdetail_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='IdentityDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('identity_name', models.CharField(choices=[('Voter_ID', 'Voter_ID'), ('Passport', 'Passport'), ('Aadhar_card', 'Aadhar_card'), ('License', 'License')], max_length=100)),
                ('identity_number', models.CharField(max_length=100)),
                ('front_image', models.ImageField(upload_to='media/identity_cards')),
                ('back_image', models.ImageField(upload_to='media/identity_cards')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='identity_name', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProficiencyCertification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('name', models.CharField(max_length=200)),
                ('Since', models.DateField(blank=True, null=True)),
                ('image', models.ImageField(upload_to='media/proficiency_certification')),
                ('grade', models.CharField(max_length=20)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proficiency_certification', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
