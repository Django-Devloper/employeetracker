from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


MARITAL_STATUS_CHOICE = (('single','Single'),('married' ,'Married'),('widow','Widow'))
POSITION_LEVEL_CHOICE = (('t1','T1'),('t2','T2'),('t3','T3'),('t4','T4'),('m1','M1'),('m2','M2'),('m3','M3'),
                         ('m4','M4'),('s1','S1'),('s2','S2'),('l1','L1'),('l2','L2'))
BANK_CHOICE = (('icici','ICICI'),('hdfc','HDFC'),('iob','IOB'),('sbi','SBI'),('idfc','IDFC'))
DEPENDENT_CHOICE = (('Mother','Mother'),('Father','Father'),('Sister','Sister'),('Brother','Brother'),('Spouse','Spouse'),('Son','Son'),('Daughter','Daughter'))
# Create your models here.
class Base(models.Model):
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    create_at = models.DateTimeField(default=now)

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
        return self.employee_user_id

class ContactDetails(Base):
    employee = models.ForeignKey(User, on_delete=models.CASCADE,related_name='contact')
    contact_number = models.PositiveBigIntegerField()
    emergency_contact = models.PositiveBigIntegerField()
    personal_email = models.EmailField(max_length=50)

    def __str__(self):
        return self.contact_number

class AddressDetails(Base):
    employee = models.ForeignKey(User, on_delete=models.CASCADE,related_name='address')
    type = models.CharField(choices=(('Temporary','Temporary'),('Permanent' ,'Permanent')) , max_length=10 )
    house_no = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pin_code = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.type} : {self.house_no} , {self.city} , {self.state} , {self.pin_code}'


class AccountDetail(Base):
    employee = models.ForeignKey(User, on_delete=models.CASCADE,related_name='account')
    account_number = models.BigIntegerField()
    account_holder_name = models.CharField(max_length=100)
    bank_name = models.CharField(choices=BANK_CHOICE , max_length=50)
    ifsc_code = models.CharField(max_length=20)
    bank_address = models.CharField(max_length=100)
    cheque = models.FileField(upload_to='media/cancel_cheque')
    customer_id = models.BigIntegerField()

    def __str__(self):
        return f'{self.account_holder_name} : {self.account_number}'

class EducationDetail(Base):
    employee = models.ForeignKey(User, on_delete=models.CASCADE,related_name='education')
    qualification = models.CharField(max_length=100)
    grade = models.CharField(max_length=20)
    year_of_passing = models.CharField(max_length=4)
    year_of_enrolment = models.CharField(max_length=4)
    university = models.CharField(max_length=100)
    collage = models.CharField(max_length=100)

    def __str__(self):
        return self.qualification

class DependentDetail(Base):
    employee = models.ForeignKey(User, on_delete=models.CASCADE,related_name='dependent')
    relationship = models.CharField(choices=DEPENDENT_CHOICE,max_length=30)
    dependent_name = models.CharField(max_length=100)
    dependent_DOB = models.DateField()

    def __str__(self):
        return f'{self.relationship} : {self.dependent_name}'

class InsuranceInfo(Base):
    employee = models.ForeignKey(User, on_delete=models.CASCADE,related_name='insurance')
    insurer = models.CharField(max_length=100 , verbose_name='Policy Provider')
    insured = models.CharField(choices=(('self','self'),('dependent','dependent ')),max_length=100)
    policy_holder_name = models.ForeignKey(DependentDetail ,models.CASCADE)
    type_of_insurance = models.CharField(choices=(('individual','Individual'),('Family Floater','Family Floater')),max_length=20)
    sum_insured = models.BigIntegerField()
    policy_type = models.CharField(choices=(('health insurance','health insurance'),('life insurance','life insurance'),('general insurance','general insurance')) ,max_length = 50)
    policy_number = models.BigIntegerField()
    valid_from  = models.DateField(default=now)
    valid_till  = models.DateField()
    documentation  = models.FileField()
    card = models.FileField()

    def valid_till_method(self):
        if self.valid_from and self.valid_till is None:
            return  self.valid_from + timedelta(days=365)

    def save(self,*args,**kwargs):
        self.valid_till = self.valid_till_method()

    def __str__(self):
        return  f'{self.policy_holder_name} : {self.policy_number}'

class Group(Base):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Team(Base):
    employee = models.ForeignKey(User, on_delete=models.CASCADE,related_name='team_name')
    group = models.ForeignKey(Group,models.CASCADE)
    team_name = models.CharField(max_length=100)
    member_since = models.DateField(default=now)
    is_active = models.BooleanField(default=True)

    def get_active_members_count(cls):
        return cls.objects.filter(is_active=True).count()

    def get_total_members_count(cls):
        return cls.objects.count()

    def __str__(self):
        return self.team_name

class EmploymentDetail(Base):
    employee = models.ForeignKey(User, on_delete=models.CASCADE,related_name='rel_emp_detail')
    employer_name = models.CharField(max_length=200)
    doj = models.DateField(verbose_name='Date of Joining')
    dor = models.DateField(verbose_name='Date of Relieving')
    rol = models.CharField(max_length=100, verbose_name='Reason of Relieving')
    rm = models.CharField(max_length=100, verbose_name='Reporting Manager')
    rm_phone = models.BigIntegerField( verbose_name='Reporting Manager Contact Number')
    rm_email = models.EmailField(max_length=100, verbose_name='Reporting Manager Contact Email')

    def __str__(self):
        return self.employer_name
