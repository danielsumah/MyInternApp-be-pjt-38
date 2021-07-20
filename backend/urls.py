from django.urls import path, include

from .views import *
urlpatterns = [
    path("", home_view, name="homepage"),
    path("employer-signup/", employer_signup_view, name="employer-signup-url"),
    path("student-signup/", student_signup_view, name="student-signup-url"),
    path("login/", login_view, name="login-url"),
    path("logout/", logout_view, name="logout-url"),
    path("employer-homepage/", employer_homepage_view,
         name="employer-homepage-url"),
    path("student-homepage/", student_homepage_view, name="student-homepage-url"),

    # profile views
    path('stu-profile/', student_profile_view, name='stu-profile'),
    path('emp-profile/', employer_profile_view, name='emp-profile'),

    # profile settings
    path("student-profile/", student_profile_settings_view,
         name="student-profile-url"),
    path("employer-profile/", employer_profile_settings_view,
         name="employer-profile-url"),

    # explore-student
    path('explore-student/', explore_student_view, name='explore-student-url'),

    # explore-job
    path('explore-job/', explore_job_view, name='explore-job-url'),

    path("upload-job/", upload_job_view, name="upload-job-url"),
    path("student-upload-work/", upload_work_view,
         name="student-upload-work-url"),
    path("job-detail/<job_id>/", job_detail_view, name="job-detail-url"),


    # admin
    path('my-intern-admin/', my_intern_admin_view, name="my-intern-admin-url"),
]
