from django.test import TestCase

# Create your tests here.
from employeeprofile.models import Position

class test_Position_creation(TestCase):

    def test_employee_creation(self):
        # Create an instance of the Employee model
        position = Position.objects.create(name="developer", position="t1")
        self.assertEqual(position.position_name ,"developer")
        self.assertEqual(position.level , "t1")
