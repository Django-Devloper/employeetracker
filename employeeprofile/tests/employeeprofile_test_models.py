import pytest
from employeeprofile.models import Position

@pytest.mark.django_db
def test_Position_creation():
    position = Position.objects.create(name="developer", position="t1")
    assert position.position_name == "developer"
    assert position.level == "t1"
