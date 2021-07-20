from django.contrib.auth.forms import UserCreationForm
from django.contrib.messages.api import error
from backend.models import StudentRegistration, EmployerRegistration, StudentProfile
from django.shortcuts import render, redirect
from .forms import *
from .forms import StudentProfileForm, StudentRegistrationForm, EmployerRegistrationForm, CreateUserForm
from .forms import JobPostForm
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def home_view(request):
    context = {}
    return render(request, "backend/index.html", context)


def student_signup_view(request):
    form = StudentRegistrationForm()
    user_creation_form = CreateUserForm()
    if request.POST:
        data = request.POST
        form = StudentRegistrationForm(data)
        if form.is_valid():

            user_creation_details = {
                'username': data.get('email'),
                'email': data.get('email'),
                'password1': data.get('password1'),
                'password2': data.get('password2')
            }

            user_creation_form = CreateUserForm(user_creation_details)
            if user_creation_form.is_valid():
                user_creation_form.save()
                print('New User Created ----------point 1')

                form.save()
                print('New student registered ------- point 2')

                # create a user out of the registration
                user = User.objects.get(
                    username=user_creation_details['username'])
                student_group = Group.objects.get(name='student')
                user.groups.add(student_group)
                print('Student added to student group ---------point 3')

                # create a profile for the user
                student_profile_creation_details = {
                    'user': user,
                    'student_reg_info': StudentRegistration.objects.get(email=user_creation_details['email']),

                }
                create_student_profile = StudentProfileForm(
                    student_profile_creation_details)
                if create_student_profile.is_valid():
                    create_student_profile.save()
                    print('New student profile created ------------ point 4')
                else:
                    print(create_student_profile.errors)

                messages.success(request, 'Account created, please login in')
                return redirect('login-url')
            else:
                print(user_creation_form.errors)
        else:
            print(form.errors)

    context = {
        'reg_form_errors': form.errors,
        'user_creation_errors': user_creation_form.errors,
    }
    return render(request, "backend/student-signup.html", context)


def employer_signup_view(request):
    form = EmployerRegistrationForm()
    user_creation_form = CreateUserForm()
    if request.POST:
        data = request.POST
        form = EmployerRegistrationForm(data)
        if form.is_valid():

            user_creation_details = {
                'username': data.get('email'),
                'email': data.get('email'),
                'password1': data.get('password1'),
                'password2': data.get('password2')
            }

            user_creation_form = CreateUserForm(user_creation_details)
            if user_creation_form.is_valid():
                user_creation_form.save()
                print('New User Created --------- point 1')

                form.save()
                print('New Employer registered --------- point 2')

                user = User.objects.get(
                    username=user_creation_details['username'])
                employer_group = Group.objects.get(name='employer')
                user.groups.add(employer_group)
                print('Employer added to employer group------ point 3')

                # create a profile for the employer
                employer_profile_creation_details = {
                    'user': request.user,
                    'employer_reg_info': EmployerRegistration.objects.get(email=user_creation_details['email']),

                }
                create_employer_profile = EmployerProfileForm(
                    employer_profile_creation_details)
                if create_employer_profile.is_valid():
                    create_employer_profile.save()
                    print('New Employer profile created ------------ point 4')
                else:
                    print(create_employer_profile.errors)

                messages.success(request, 'Account created, please login in')
                return redirect('login-url')
            else:
                print(user_creation_form.errors)
        else:
            print(form.errors)

    context = {
        'reg_form_errors': form.errors,
        'user_creation_errors': user_creation_form.errors,
    }
    return render(request, "backend/employer-signup.html", context)


def login_view(request):
    if request.method == "POST":
        user_email = request.POST.get('email')
        user_password = request.POST.get('password')
        print(user_email)
        print(user_password)

        user = authenticate(request, username=user_email,
                            password=user_password)

        if user is not None:
            login(request, user)
            if user.groups.filter(name='student').exists():
                return redirect("student-homepage-url")
            elif user.groups.filter(name='employer').exists():
                return redirect("employer-homepage-url")
            else:
                return redirect('my-intern-admin-url')
        else:
            messages.info(request, "Username or password is incorrect")
            print(messages)

    context = {

    }
    return render(request, "backend/login.html", context)


def student_homepage_view(request):
    # Get the logged in in student email
    student_email = request.user.email

    # use the email to search for student details in the StudentRegistration
    student_detail = StudentRegistration.objects.get(email=student_email)

    # bring out all job posting
    jobs = JobPost.objects.all()
    print(jobs)

    if request.method == 'POST':
        job_contains_query = request.POST.get('job_contains')
        if job_contains_query != '' and job_contains_query is not None:
            jobs = jobs.filter(title__icontains=job_contains_query)
    else:
        jobs = JobPost.objects.all()

    active_user_group = str(request.user.groups.all()[0])
    print(type(active_user_group))

    context = {
        'student_detail': student_detail,
        'jobs': jobs,
        'active_user_group': active_user_group,

    }

    return render(request, "backend/student-homepage.html", context)


def employer_homepage_view(request):
    # Get the logged in Employer email
    employer_email = request.user.email

    # use the email to search for student details in the StudentRegistration
    employer_detail = EmployerRegistration.objects.get(email=employer_email)
    employer_profile = EmployerProfile.objects.get(
        employer_reg_info=employer_detail)
    print(employer_profile.verified)

    context = {
        'employer_detail': employer_detail,
        "employer_profile": employer_profile,
    }
    return render(request, "backend/employer-homepage.html", context)


def logout_view(request):
    logout(request)
    return redirect('login-url')

# profile views


def student_profile_view(request):
    user_email = request.user.email
    # bring out uneitable details from regisration
    user_reg_details = StudentRegistration.objects.get(email=user_email)
    student_profile = StudentProfile.objects.get(
        student_reg_info=user_reg_details)

    active_user_group = str(request.user.groups.all()[0])
    context = {
        'active_user_group': active_user_group,
        'student_profile': student_profile,
    }
    return render(request, 'backend/profile-student.html', context)


def employer_profile_view(request):
    context = {}
    return render(request, 'backend/profile-employer.html', context)

# Profile settings views


def student_profile_settings_view(request):
    user_email = request.user.email

    # bring out uneitable details from regisration
    user_reg_details = StudentRegistration.objects.get(email=user_email)
    student_profile = StudentProfile.objects.get(
        student_reg_info=user_reg_details)

    if request.method == 'POST':
        form = StudentProfileUpdateForm(
            request.POST, request.FILES, instance=student_profile)
        if form.is_valid():
            form.save()
            return redirect('student-profile-url')
        else:
            print(form.errors)
    active_user_group = str(request.user.groups.all()[0])

    context = {
        'user_reg_details': user_reg_details,
        'student_profile': student_profile,
        'active_user_group': active_user_group,
    }
    return render(request, "backend/building-profile-student.html", context)


def employer_profile_settings_view(request):
    user_email = request.user.email
    employer_reg_details = EmployerRegistration.objects.get(email=user_email)
    employer_profile = EmployerProfile.objects.get(
        employer_reg_info=employer_reg_details)

    if request.method == 'POST':
        form = EmployerProfileUpdateForm(
            request.POST, request.FILES, instance=employer_profile)
        if form.is_valid():
            form.save()
            return redirect('employer-profile-url')
        else:
            print(form.errors)

    context = {
        'employer_reg_details': employer_reg_details,
        'employer_profile': employer_profile,
    }
    return render(request, "backend/building-profile-employer.html", context)


# explore student view
def explore_student_view(request):
    all_students = StudentProfile.objects.all()

    active_user_group = str(request.user.groups.all()[0])

    context = {
        'all_students': all_students,
        'active_user_group': active_user_group,
    }
    return render(request, "backend/explore-student.html", context)

# explore student view


def explore_job_view(request):
    all_jobs = JobPost.objects.all()
    active_user_group = str(request.user.groups.all()[0])
    context = {
        'all_jobs': all_jobs,
        'active_user_group': active_user_group
    }
    return render(request, "backend/explore-jobs.html", context)


def upload_job_view(request):
    form = JobPostForm
    if request.method == "POST":
        form = JobPostForm(request.POST)
        if form.is_valid():
            print('form is valid')
            employer = EmployerRegistration.objects.filter(
                email=request.user.email).first()
            print('Employer found')
            form.save(employer)
            print(employer)
            print('Job saved')
            messages.success(request, 'Job upload was successful')
            return redirect('explore-job-url')
        else:
            print(form.errors)
    active_user_group = str(request.user.groups.all()[0])
    context = {
        "form": form,
        'active_user_group': active_user_group,
    }
    return render(request, "backend/employer-upload-job.html", context)


def upload_work_view(request):
    form = StudentWorkPostForm
    if request.method == "POST":
        form = StudentWorkPostForm(request.POST)
        if form.is_valid():
            student = StudentRegistration.objects.filter(
                email=request.user.email).first()
            form.save(student)
            messages.success(request, 'Work upload was successful')
            return redirect('student-upload-work-url')
    context = {
        "form": form
    }
    return render(request, "backend/student-upload-work.html", context)


def job_detail_view(request, job_id):
    job = JobPost.objects.get(id=job_id)

    context = {
        'job': job,
    }
    return render(request, "backend/job-details.html", context)


def my_intern_admin_view(request):

    all_employers = EmployerProfile.objects.all()
    if request.method == "POST":
        data = request.POST
        if len(list(data)) > 1:
            employer_id = list(data)[1]
            status = data[employer_id]
            print(status)

            employer = EmployerProfile.objects.get(id=int(employer_id))
            employer.verified = True
            employer.save()
        # employer_id = request.post.get
    context = {
        'all_employers': all_employers,
    }
    return render(request, "backend/my-intern-admin.html", context)
