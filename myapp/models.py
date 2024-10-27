from django.db import models
from django.contrib.auth.models import User
import os

class Profile(models.Model):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('faculty', 'Faculty'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} Profile"

# Model to store Departments
class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# Model to store Batches
class Batch(models.Model):
    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.start_year} - {self.end_year} ({self.department.name})"

# Custom function to generate the image file path based on admission number
def student_photo_path(instance, filename):
    # Extract the file extension from the original filename
    ext = filename.split('.')[-1]
    
    # Construct the new filename using the student's admission number
    filename = f"{instance.admission_no}.{ext}"
    
    # Return the final path for storing the image
    return os.path.join('student_photos/', filename)

# Model to store Student details
class Student(models.Model):
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    
    APPROVAL_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    admission_no = models.CharField(max_length=20, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Assuming a link to the Django User model
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    house = models.CharField(max_length=255, null=True, blank=True)
    street = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    district = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    pincode = models.IntegerField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    guardian_phone = models.CharField(max_length=15, null=True, blank=True)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    date_of_birth = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to=student_photo_path, null=True, blank=True)
    approval_status = models.CharField(max_length=20, choices=APPROVAL_STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.admission_no})"

#model for faculty
class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to the User model or Profile
    department = models.ForeignKey(Department, on_delete=models.CASCADE)  # Faculty's department

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.department.name})"