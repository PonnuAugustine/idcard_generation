from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError
from .models import Profile
from .models import Department
from .models import Batch
from .models import Student
from .models import Faculty

# Create your views here.
def index(request):
    return render(request, 'index.html')
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)  # Log in the user
            
            try:
                # Redirect to the appropriate homepage based on the user's role
                profile = Profile.objects.get(user=user)
                if profile.role == 'student':
                    return redirect('studenthome')  # Change to the URL name for student home
                elif profile.role == 'faculty':
                    return redirect('facultyhome')  # Change to the URL name for faculty home
            except Profile.DoesNotExist:
                messages.error(request, 'Profile does not exist.')
                return redirect('index')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('index')  # Redirect back to login page on error
    return render(request, 'login.html')
def register(request):
    print("Received a request to register.")
    departments = Department.objects.all() 
    if request.method == 'POST':
        print("Handling POST request.")
        username = request.POST['username']
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        password = request.POST['password']
        user_type = request.POST['userType']  # Assuming this comes from your form
        department_id = request.POST.get('department')  # Assuming department is part of the form for faculty

        print(f"User Type: {user_type}") 

        try:
            print("Attempting to create user.")
            user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
            user.save()

            profile = Profile.objects.create(user=user, role=user_type)
            profile.save()

            if user_type == 'faculty':
                department = Department.objects.get(id=department_id)  # Get the department for faculty
                faculty = Faculty.objects.create(user=user, department=department)  # Create a Faculty record
                faculty.save()
                print("Faculty data saved successfully.")

            messages.success(request, 'Account created successfully!')
            print("Redirecting to login")
            return redirect('login')
        except IntegrityError:
            messages.error(request, 'Username already exists!')
            print("Username already exists, redirecting back to register.")
            return redirect('register')
    print("Rendering registration form.")
    return render(request, 'register.html', {'departments': departments})  # Render the registration form

def studenthome(request):
    return render(request, 'studenthome.html')

def facultyhome(request):
    return render(request, 'facultyhome.html')

def studentdata(request):
    # Get the logged-in user (faculty)
    faculty = Faculty.objects.get(user=request.user)

    # Fetch the students from the same department as the faculty
    students = Student.objects.filter(department=faculty.department)

    # Pass the student data to the template
    return render(request, 'fstudentdata.html', {'students': students})

def pendingupdates(request):
    return render(request, 'f_pendingupdates.html')

def studentform(request):
    user = request.user  # Get the logged-in user
    departments = Department.objects.all()
    batches = Batch.objects.all()

    if request.method == 'POST':
        # Manually fetch form data from the POST request
        admission_no = request.POST.get('admission_no')
        department_id = request.POST.get('department')
        batch_id = request.POST.get('batch')
        house = request.POST.get('house')
        street = request.POST.get('street')
        city = request.POST.get('city')
        district = request.POST.get('district')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        phone = request.POST.get('phone')
        guardian_phone = request.POST.get('guardian_phone')
        blood_group = request.POST.get('blood_group')
        date_of_birth = request.POST.get('date_of_birth')
        photo = request.FILES.get('photo')  # Handle the uploaded file

        # Get related objects for ForeignKey fields
        department = Department.objects.get(id=department_id)
        batch = Batch.objects.get(id=batch_id)

        # Check if student record already exists
        try:
            student = Student.objects.get(user=user)
        except Student.DoesNotExist:
            student = Student(user=user)

        # Update or create student details
        student.admission_no = admission_no
        student.department = department
        student.batch = batch
        student.house = house
        student.street = street
        student.city = city
        student.district = district
        student.state = state
        student.pincode = pincode
        student.phone = phone
        student.guardian_phone = guardian_phone
        student.blood_group = blood_group
        student.date_of_birth = date_of_birth
        
        if photo:
            student.photo = photo  # Only update the photo if a new one is uploaded

        student.save()  # Save the student data

        # Add a success message
        messages.success(request, "Data submitted successfully.")

        return redirect('studentform')  # Redirect to a success page or another view

    return render(request, 'student_form.html', {
        'departments': departments,
        'batches': batches,
        'user': user  # Pass the user to the template if needed
    })

def studentprofile(request):
    return render(request, 'student_profile.html')

def adminhome(request):
    return render(request, 'adminhome.html')

def adminbase(request):
    return render(request, 'adminbase.html')

def batch(request):
    if request.method == 'POST':
        start_year = request.POST.get('start_year')
        end_year = request.POST.get('end_year')
        department_id = request.POST.get('department')

        # Validate input
        if start_year and end_year and department_id:
            try:
                department = Department.objects.get(id=department_id)
                Batch.objects.create(start_year=start_year, end_year=end_year, department=department)
                messages.success(request, 'Batch created successfully!')
                return redirect('batch')  # Redirect to the batch page or another appropriate page
            except Exception as e:
                messages.error(request, f"Error creating batch: {str(e)}")
        else:
            messages.error(request, 'Please fill in all fields.')

    # Fetch all departments to display in the form
    batches = Batch.objects.all()
    departments = Department.objects.all()
    return render(request, 'batch.html', {'departments': departments, 'batches': batches})

def department(request):
    if request.method == 'POST':
        department_name = request.POST.get('department')
        if department_name:
            try:
                Department.objects.create(name=department_name)
            except IntegrityError:
                # Handle error if department name already exists
                error_message = "Department with this name already exists."
                departments = Department.objects.all()
                return render(request, 'department.html', {'departments': departments, 'error_message': error_message})
    
    # Fetch all departments to display
    departments = Department.objects.all()
    return render(request, 'department.html', {'departments': departments})

def facultyverify(request):
    return render(request, 'faculty_verify.html')

def generateid(request):
    return render(request, 'generate_id.html')

def viewstudent(request):
    return render(request, 'view_students.html')