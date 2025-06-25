# core/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from .models import *
from .forms import LoginForm, ApplicantForm
from .services import passes_screening
from functools import wraps
from django.shortcuts import render
from core.models import Application, InterviewSchedule
from django import template
from .forms import SignupForm
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse

from .forms import SignupForm
from django.contrib.auth import login, get_backends

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    return field.as_widget(attrs={"class": css_class})


# ---------- helpers ----------
def login_required(role=None):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if "user_id" not in request.session:
                return redirect("login")
            if role and request.session.get("role") != role:
                return redirect("dashboard")
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

# ---------- auth ----------
def login_view(request):
    request.session.flush()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                request.session["user_id"] = user.id
                request.session["role"] = user.role
                if user.role == "ADMIN":
                    return redirect("admin_dashboard")
                elif user.role == "RECRUITER":
                    return redirect("recruiter_dashboard")
                elif user.role == "JOBSEEKER":
                    return redirect("applicant_dashboard")
            else:
                messages.error(request, "Invalid email or password.")
    else:
        form = LoginForm()
        list(messages.get_messages(request))
    return render(request, "core/login.html", {"form": form})

def logout_view(request):
    request.session.flush()
    return redirect("login")

# ---------- dashboards ----------
@login_required("ADMIN")
def admin_dashboard(request):
    return render(request, "core/dashboards/admin.html")

@login_required("RECRUITER")
def recruiter_dashboard(request):
    return render(request, "core/dashboards/recruiter.html")

# @login_required("JOBSEEKER")
# def applicant_dashboard(request):
#     return render(request, "core/dashboards/applicant.html")

@login_required("JOBSEEKER")
def applicant_dashboard(request):
    user_id = request.session["user_id"]
    applicant = get_object_or_404(Applicant, user_id=user_id)

    apps_count = Application.objects.filter(applicant=applicant).count()
    interviews_count = InterviewSchedule.objects.filter(application__applicant=applicant).count()
    saved_count = 0  # You can implement saving jobs later

    return render(request, "core/dashboards/applicant.html", {
        "apps_count": apps_count,
        "interviews_count": interviews_count,
        "saved_count": saved_count
    })


@login_required()
def dashboard(request):
    role = request.session["role"]
    tpl = {
        "ADMIN": "core/dashboards/admin.html",
        "RECRUITER": "core/dashboards/recruiter.html",
        "JOBSEEKER": "core/dashboards/applicant.html"
    }[role]
    return render(request, tpl)

# ---------- applicant views ----------
@login_required("JOBSEEKER")
def job_list(request):
    jobs = JobListings.objects.select_related("department", "recruiter__user")
    return render(request, "core/jobs/list.html", {"jobs": jobs})

@login_required("JOBSEEKER")
def job_detail(request, pk):
    job = get_object_or_404(JobListings, pk=pk)
    applied = Application.objects.filter(
        job=job,
        applicant__user_id=request.session["user_id"]
    ).exists()
    return render(request, "core/jobs/detail.html", {"job": job, "applied": applied})


@login_required("JOBSEEKER")
def job_apply(request, pk):
    job = get_object_or_404(JobListings, pk=pk)
    user_id = request.session["user_id"]
    applicant, _ = Applicant.objects.get_or_create(user_id=user_id)

    if request.method == "POST":
        form = ApplicantForm(request.POST, instance=applicant)
        if form.is_valid():
            form.save()  # update applicant data
            Application.objects.get_or_create(job=job, applicant=applicant)
            
            # Check for screening only if criteria exists
            if hasattr(job, "criteria") and passes_screening(applicant, job.criteria):
                Application.objects.filter(job=job, applicant=applicant).update(status="Shortlisted")
            
            messages.success(request, "Application submitted.")
            return redirect("applications")
    else:
        form = ApplicantForm(instance=applicant)

    return render(request, "core/applications/apply_form.html", {"form": form, "job": job})


@login_required("JOBSEEKER")
def applications(request):
    applicant = Applicant.objects.filter(user_id=request.session["user_id"]).first()
    apps = Application.objects.filter(applicant=applicant).select_related("job", "job__department") if applicant else []
    return render(request, "core/applications/list.html", {"apps": apps})

@login_required("JOBSEEKER")
def interviews(request):
    applicant = Applicant.objects.filter(user_id=request.session["user_id"]).first()
    its = InterviewSchedule.objects.filter(application__applicant=applicant) if applicant else []
    return render(request, "core/interviews/list.html", {"its": its})



@login_required("JOBSEEKER")
def decisions(request):
    applicant = Applicant.objects.filter(user_id=request.session["user_id"]).first()
    decs = HiringDecisions.objects.filter(applicant=applicant) if applicant else []
    return render(request, "core/decisions/list.html", {"decs": decs})



# ---------- recruiter views ----------
@login_required("RECRUITER")
def shortlisted(request):
    recruiter = Recruiter.objects.get(pk=request.session["user_id"])
    apps = Application.objects.filter(status="Shortlisted", job__recruiter=recruiter)
    return render(request, "core/recruiter/shortlisted.html", {"apps": apps})

@login_required("RECRUITER")
def schedule_interview(request, app_id):
    app = get_object_or_404(Application, pk=app_id, job__recruiter__pk=request.session["user_id"])
    if request.method == "POST":
        InterviewSchedule.objects.create(
            job=app.job,
            application=app,
            recruiter_id=request.session["user_id"],
            date=request.POST["date"],
            time=request.POST["time"]
        )
        messages.success(request, "Interview scheduled.")
        return redirect("recruiter_interviews")
    return render(request, "core/recruiter/schedule_form.html", {"app": app})

@login_required("RECRUITER")
def recruiter_interviews(request):
    its = InterviewSchedule.objects.filter(recruiter_id=request.session["user_id"])
    return render(request, "core/recruiter/interviews.html", {"its": its})

@login_required("RECRUITER")
def hire(request, app_id):
    app = get_object_or_404(Application, pk=app_id, job__recruiter__pk=request.session["user_id"])
    HiringDecisions.objects.update_or_create(
        job=app.job, applicant=app.applicant,
        defaults={"final_status": "Hired"}
    )
    app.status = "Selected"
    app.save(update_fields=["status"])
    messages.success(request, "Applicant Hired!")
    return redirect("recruiter_decisions")



# ---------- admin views ----------
@login_required("ADMIN")
def job_create(request):
    if request.method == "POST":
        recruiter = Recruiter.objects.get(pk=request.session["user_id"])
        job = JobListings.objects.create(
            recruiter=recruiter,
            department_id=request.POST["department"],
            title=request.POST["title"],
            posted_date=request.POST["posted_date"]
        )
        ScreeningCriteria.objects.create(
            job=job,
            required_skills=request.POST["skills"],
            min_experience=request.POST["min_exp"],
            min_qualification=request.POST["qual"]
        )
        messages.success(request, "Job created")
        return redirect("admin_jobs")
    depts = Department.objects.all()
    return render(request, "core/admin/job_form.html", {"depts": depts})

@login_required("ADMIN")
def admin_jobs(request):
    jobs = JobListings.objects.all()
    return render(request, "core/admin/jobs.html", {"jobs": jobs})



@login_required("RECRUITER")
def view_application(request, app_id):
    app = get_object_or_404(Application, pk=app_id, job__recruiter__pk=request.session["user_id"])
    return render(request, "core/recruiter/view_application.html", {"app": app})


@login_required("RECRUITER")
def recruiter_interviews(request):
    recruiter = Recruiter.objects.get(pk=request.session["user_id"])
    its = InterviewSchedule.objects.filter(recruiter=recruiter).select_related("application__applicant__user", "job")
    return render(request, "core/recruiter/interviews.html", {"its": its})

# @login_required("RECRUITER")
# def recruiter_decisions(request):
#     recruiter = Recruiter.objects.get(pk=request.session["user_id"])
#     decisions = HiringDecisions.objects.filter(job__recruiter=recruiter).select_related("job", "applicant__user")
#     return render(request, "core/recruiter/decisions.html", {"decisions": decisions})
from django.db.models import OuterRef, Subquery, Exists

@login_required("RECRUITER")
def recruiter_decisions(request):
    recruiter = Recruiter.objects.get(pk=request.session["user_id"])

    # Decisions already made
    decisions = HiringDecisions.objects.filter(
        job__recruiter=recruiter
    ).select_related("job", "applicant__user")

    # Subquery to check if a decision exists for the app-job pair
    decision_exists = HiringDecisions.objects.filter(
        job=OuterRef("job"),
        applicant=OuterRef("applicant")
    )

    # Shortlisted applicants who haven't been hired/rejected yet
    undecided_apps = Application.objects.filter(
        job__recruiter=recruiter,
        status="Shortlisted"
    ).annotate(
        already_decided=Exists(decision_exists)
    ).filter(
        already_decided=False
    ).select_related("job", "applicant__user")

    return render(request, "core/recruiter/decisions.html", {
        "decisions": decisions,
        "undecided_apps": undecided_apps
    })
# def recruiter_dashboard(request):
#     shortlisted_count = Application.objects.filter(status="Shortlisted").count()
#     interviews_count = InterviewSchedule.objects.filter(status="Scheduled").count()
#     decisions_count = Application.objects.filter(status__in=["Selected", "Rejected"]).count()

#     return render(request, 'core/dashboards/recruiter.html', {
#         'shortlisted_count': shortlisted_count,
#         'interviews_count': interviews_count,
#         'decisions_count': decisions_count,
#     })
@login_required("RECRUITER")
def recruiter_dashboard(request):
    recruiter = Recruiter.objects.get(user_id=request.session["user_id"])

    shortlisted_count = Application.objects.filter(
        job__recruiter=recruiter, status="Shortlisted"
    ).count()

    interviews_count = InterviewSchedule.objects.filter(
        recruiter=recruiter, status="Scheduled"
    ).count()

    decisions_count = HiringDecisions.objects.filter(
        job__recruiter=recruiter
    ).count()

    return render(request, 'core/dashboards/recruiter.html', {
        'shortlisted_count': shortlisted_count,
        'interviews_count': interviews_count,
        'decisions_count': decisions_count,
    })
# core/views.py (add at the bottom)


def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = "JOBSEEKER"
            user.set_password(form.cleaned_data["password"])
            user.save()
            Applicant.objects.create(user=user)

            # Manually attach backend
            backend = get_backends()[0]
            user.backend = f"{backend.__module__}.{backend.__class__.__name__}"
            login(request, user)

            messages.success(request, "🎉 Signup successful! Welcome to the system.")
            return redirect("login")  # Redirect to login page
    else:
        form = SignupForm()

    return render(request, "core/signup.html", {"form": form})


def test_api(request):
    return JsonResponse({"message": "Backend is connected to React!"})