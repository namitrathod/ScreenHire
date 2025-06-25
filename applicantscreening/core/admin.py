# core/admin.py
from django.contrib import admin
from .models import (
    User, Department, Recruiter, Applicant,
    JobListings, Application, InterviewSchedule,
    HiringDecisions,        # ← correct spelling
)

# register everything
for m in (
    User, Department, Recruiter, Applicant,
    JobListings, Application, InterviewSchedule,
    HiringDecisions,
):
    admin.site.register(m)



# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('user_id', 'name', 'email', 'role')

# @admin.register(Department)
# class DepartmentAdmin(admin.ModelAdmin):
#     list_display = ('department_id', 'name')

# @admin.register(Recruiter)
# class RecruiterAdmin(admin.ModelAdmin):
#     list_display = ('user', 'department')

# @admin.register(Applicant)
# class ApplicantAdmin(admin.ModelAdmin):
#     list_display = ('user', 'contact_number', 'experience')

# @admin.register(JobListings)
# class JobAdmin(admin.ModelAdmin):
#     list_display = ('job_id', 'title', 'recruiter', 'posted_date')

# @admin.register(Application)
# class ApplicationAdmin(admin.ModelAdmin):
#     list_display = ('application_id', 'job', 'applicant', 'status')

# @admin.register(InterviewSchedule)
# class InterviewAdmin(admin.ModelAdmin):
#     list_display = ('job', 'application', 'recruiter', 'date', 'status')

# @admin.register(HiringDecision)
# class DecisionAdmin(admin.ModelAdmin):
#     list_display = ('job', 'applicant', 'final_status', 'decision_date')