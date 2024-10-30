import pytest
from employeeprofile.models import Position
from django.contrib.auth.models import User ,Group

def user():
    user = User.objects.create(username='admin',password='123456')
    return user

@pytest.mark.django_db
def test_Position_creation():
    created_by =user()
    position = Position.objects.create(position_name="developer", level="t1" ,created_by = created_by)
    assert position.position_name == "developer"
    assert position.level == "t1"


@pytest.mark.django_db
def test_Group_creation():
    created_by =user()
    print(created_by,"r##########################")
    group = Group.objects.create(name = 'test')
    assert group.name == 'test'
