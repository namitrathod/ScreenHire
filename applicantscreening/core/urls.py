# core/urls.py
from django.urls import path
from . import views
from .views import test_api  # Import the test_api function

urlpatterns = [
    # Auth
    path("", views.login_view, name="login"),
    path('signup/', views.signup_view, name='signup'),
    path("logout/", views.logout_view, name="logout"),

    # Dashboards
    # path("admin/dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("internal/admin/dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("recruiter/dashboard/", views.recruiter_dashboard, name="recruiter_dashboard"),
    path("applicant/dashboard/", views.applicant_dashboard, name="applicant_dashboard"),
    path("dashboard/", views.dashboard, name="dashboard"),

    # Applicant
    path("jobs/", views.job_list, name="job_list"),
# core/urls.py
    path("jobs/<int:pk>/", views.job_detail, name="job_detail"),
    path("jobs/apply/<int:pk>/", views.job_apply, name="job_apply"),
    path("applications/", views.applications, name="applications"),
    path("interviews/", views.interviews, name="interview_list"),
    path("decisions/", views.decisions, name="decision_list"),

    # Recruiter
    path("recruit/shortlisted/", views.shortlisted, name="shortlisted"),
    path("recruit/interviews/", views.recruiter_interviews, name="recruiter_interviews"),
    path("recruit/schedule/<int:app_id>/", views.schedule_interview, name="schedule_interview"),
    path("recruit/hire/<int:app_id>/", views.hire, name="hire"),
    path("applications/view/<int:app_id>/", views.view_application, name="view_application"),
    path("recruit/interviews/", views.recruiter_interviews, name="recruiter_interviews"),
    path("recruit/decisions/", views.recruiter_decisions, name="recruiter_decisions"),
    path("recruit/hire/<int:app_id>/", views.hire, name="hire"),




    # Admin
    path("internal/admin/jobs/", views.admin_jobs, name="admin_jobs"),
    path("internal/admin/jobs/new/", views.job_create, name="job_add"),
    
    
    
    path("api/test/", test_api, name="test_api"),
]

# # applicantscreeningsystem/urls.py
# from django.contrib import admin
# from django.urls import path, include
# urlpatterns = [
#     path("admin/", admin.site.urls),
#     path("", include("core.urls")),
# ]

# # core/urls.py
# from django.urls import path
# from . import views
# urlpatterns = [
#     path("",          views.login_view,      name="login"),
#     path("logout/",   views.logout_view,     name="logout"),
#     path("home/",     views.dashboard,       name="dashboard"),

#     path("jobs/",                 views.job_list,    name="job_list"),
#     path("jobs/<int:pk>/",        views.job_detail,  name="job_detail"),
#     path("jobs/apply/<int:pk>/",  views.job_apply,   name="job_apply"),

#     path("applicant/dashboard/", views.dashboard, name="applicant_dashboard"),
#     path("applications/", views.applications, name="applications"),
#     path("interviews/",   views.interviews,   name="interview-list"),
#     path("decisions/",    views.decisions,    name="decision-list"),

    

#     path("recruiter/dashboard/", views.dashboard, name="recruiter_dashboard"),
#     path("recruit/shortlisted/",  views.shortlisted,            name="shortlisted"),
#     path("recruit/interviews/",   views.recruiter_interviews,   name="recruit_interviews"),
#     path("recruit/schedule/<int:app_id>/", views.schedule_interview, name="schedule"),
#     path("recruit/hire/<int:app_id>/",     views.hire,          name="hire"),

#     path("admin/dashboard/", views.admin_dashboard, name="admin_dashboard"),
#     path("admin/jobs/",  views.admin_jobs,   name="admin_jobs"),
#     path("admin/jobs/new/", views.job_create,name="job_add"),
# ]
