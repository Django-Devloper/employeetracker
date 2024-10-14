from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

MARITAL_STATUS_CHOICE = (('single','Single'),('married' ,'Married'),('widow','Widow'))
POSITION_LEVEL_CHOICE = (('t1','T1'),('t2','T2'),('t3','T3'),('t4','T4'),('m1','M1'),('m2','M2'),('m3','M3'),
                         ('m4','M4'),('s1','S1'),('s2','S2'),('l1','L1'),('l2','L2'))
# Create your models here.
class Base(models.Model):
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    create_at = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True

class Position(Base):
    position_name = models.CharField(max_length=50)
    level = models.CharField(choices=POSITION_LEVEL_CHOICE , max_length=50)

    def __str__(self):
        return self.position_name

class EmployeeProfile(Base):
    employee = models.ForeignKey(User, on_delete=models.CASCADE,related_name='employee_pro')
    marital_status = models.CharField(choices=MARITAL_STATUS_CHOICE ,max_length=20)
    reporting_manager = models.ForeignKey(User,on_delete=models.CASCADE,related_name='manager')
    employee_user_id = models.CharField(max_length=20)
    position = models.ForeignKey(Position ,on_delete=models.CASCADE)
    date_of_joining = models.DateField()
    email_id =  models.EmailField(max_length=50)
    pan_number = models.CharField(max_length=10)
    date_of_birth = models.DateField()

    def __str__(self):
        return self.employee_id

class ContactDetails(Base):
    employee = models.ForeignKey(User, on_delete=models.CASCADE,related_name='contact')
    contact_number = models.PositiveBigIntegerField()
    emergency_contact = models.PositiveBigIntegerField()
    personal_email = models.EmailField(max_length=50)

    def __str__(self):
        return self.contact_number

class AddressDetails(Base):
    employee = models.ForeignKey(User, on_delete=models.CASCADE,related_name='address')
    type = models.CharField(choices=(('temp','Temporary'),('parmanent' ,'Parmanent')) , max_length=10 )
    house_no = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pin_code = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.type} : {self.house_no} , {self.city} , {self.state} , {self.pin_code}'
