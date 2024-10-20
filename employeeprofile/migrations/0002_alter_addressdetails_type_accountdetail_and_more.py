# Generated by Django 5.1.2 on 2024-10-20 04:48

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employeeprofile', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='addressdetails',
            name='type',
            field=models.CharField(choices=[('Temporary', 'Temporary'), ('Permanent', 'Permanent')], max_length=10),
        ),
        migrations.CreateModel(
            name='AccountDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('account_number', models.BigIntegerField()),
                ('account_holder_name', models.CharField(max_length=100)),
                ('bank_name', models.CharField(choices=[('icici', 'ICICI'), ('hdfc', 'HDFC'), ('iob', 'IOB'), ('sbi', 'SBI'), ('idfc', 'IDFC')], max_length=50)),
                ('ifsc_code', models.CharField(max_length=20)),
                ('bank_address', models.CharField(max_length=100)),
                ('cheque', models.FileField(upload_to='media/cancel_cheque')),
                ('customer_id', models.BigIntegerField()),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='account', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DependentDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('relationship', models.CharField(choices=[('Mother', 'Mother'), ('Father', 'Father'), ('Sister', 'Sister'), ('Brother', 'Brother'), ('Spouse', 'Spouse'), ('Son', 'Son'), ('Daughter', 'Daughter')], max_length=30)),
                ('dependent_name', models.CharField(max_length=100)),
                ('dependent_DOB', models.DateField()),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dependent', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EducationDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('qualification', models.CharField(max_length=100)),
                ('grade', models.CharField(max_length=20)),
                ('year_of_passing', models.CharField(max_length=4)),
                ('year_of_enrolment', models.CharField(max_length=4)),
                ('university', models.CharField(max_length=100)),
                ('collage', models.CharField(max_length=100)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='education', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('name', models.CharField(max_length=100)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InsuranceInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('insurer', models.CharField(max_length=100, verbose_name='Policy Provider')),
                ('insured', models.CharField(choices=[('self', 'self'), ('dependent', 'dependent ')], max_length=100)),
                ('type_of_insurance', models.CharField(choices=[('individual', 'Individual'), ('Family Floater', 'Family Floater')], max_length=20)),
                ('sum_insured', models.BigIntegerField()),
                ('policy_type', models.CharField(choices=[('health insurance', 'health insurance'), ('life insurance', 'life insurance'), ('general insurance', 'general insurance')], max_length=50)),
                ('policy_number', models.BigIntegerField()),
                ('valid_from', models.DateField(default=django.utils.timezone.now)),
                ('valid_till', models.DateField()),
                ('documentation', models.FileField(upload_to='')),
                ('card', models.FileField(upload_to='')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='insurance', to=settings.AUTH_USER_MODEL)),
                ('policy_holder_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employeeprofile.dependentdetail')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('team_name', models.CharField(max_length=100)),
                ('member_since', models.DateField(default=django.utils.timezone.now)),
                ('is_active', models.BooleanField(default=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_name', to=settings.AUTH_USER_MODEL)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employeeprofile.group')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]