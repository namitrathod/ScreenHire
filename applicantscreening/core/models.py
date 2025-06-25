# core/models.py
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get("is_staff"):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('RECRUITER', 'Recruiter'),
        ('JOBSEEKER', 'Job Seeker'),
    )

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role']

    def __str__(self):
        return self.email


class Applicant(models.Model):
    user            = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    contact_number  = models.CharField(max_length=50, blank=True, null=True)
    experience      = models.IntegerField(blank=True, null=True)
    skills          = models.TextField(blank=True, null=True)
    education       = models.TextField(blank=True, null=True)

class Recruiter(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    department  = models.ForeignKey("Department", on_delete=models.RESTRICT)

class AdminManagement(models.Model):
    admin       = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    permissions = models.TextField()

class Department(models.Model):
    department_id = models.AutoField(primary_key=True)
    name          = models.CharField(max_length=100)

    def __str__(self): return self.name

class JobListings(models.Model):
    job_id      = models.AutoField(primary_key=True)
    recruiter   = models.ForeignKey(Recruiter, on_delete=models.CASCADE, related_name="jobs")
    department  = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="jobs")
    title       = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    salary      = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    requirements= models.TextField(blank=True, null=True)
    posted_date = models.DateField()

    def __str__(self): return self.title

class ScreeningCriteria(models.Model):
    criteria_id       = models.AutoField(primary_key=True)
    job               = models.OneToOneField(JobListings, on_delete=models.CASCADE, related_name="criteria")
    required_skills   = models.TextField(blank=True, null=True)
    min_experience    = models.IntegerField(blank=True, null=True)
    min_qualification = models.CharField(max_length=100, blank=True, null=True)

class Application(models.Model):
    STATUS_CHOICES = [("Pending","Pending"),("Shortlisted","Shortlisted"),
                      ("Rejected","Rejected")]
    application_id = models.AutoField(primary_key=True)
    job        = models.ForeignKey(JobListings, on_delete=models.CASCADE, related_name="applications")
    applicant  = models.ForeignKey(Applicant, on_delete=models.CASCADE, related_name="applications")
    status     = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    date_applied = models.DateField(auto_now_add=True)

class InterviewSchedule(models.Model):
    STATUS = [("Scheduled","Scheduled"),("Completed","Completed"),("Cancelled","Cancelled")]
    id = models.AutoField(primary_key=True)
    job         = models.ForeignKey(JobListings, on_delete=models.CASCADE, related_name="interviews")
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name="interviews")
    recruiter   = models.ForeignKey(Recruiter, on_delete=models.CASCADE, related_name="interviews")
    date        = models.DateField()
    time        = models.TimeField()
    status      = models.CharField(max_length=20, choices=STATUS, default="Scheduled")

class HiringDecisions(models.Model):
    id = models.BigAutoField(primary_key=True)
    job       = models.ForeignKey(JobListings, on_delete=models.CASCADE, related_name="decisions")
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE, related_name="decisions")
    final_status = models.CharField(max_length=20, choices=[("Hired","Hired"),("Rejected","Rejected")])
    decision_date= models.DateField(auto_now_add=True)

    class Meta: unique_together = ("job","applicant")

class ApplicantContactNo(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    contact_no= models.CharField(max_length=50)

    class Meta: unique_together = ("applicant","contact_no")





# from django.db import models
# from django.utils import timezone

# class User(models.Model):
#     user_id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=100)
#     email = models.EmailField(unique=True, max_length=100)
#     password = models.CharField(max_length=128)
#     ROLE_CHOICES = [
#         ('Admin', 'Admin'),
#         ('HR Recruiter', 'HR Recruiter'),
#         ('Job Seeker', 'Job Seeker'),
#     ]
#     role = models.CharField(max_length=20, choices=ROLE_CHOICES)
#     date_created = models.DateTimeField(default=timezone.now)

#     def __str__(self):
#         return f"{self.name} ({self.role})"

# class Department(models.Model):
#     department_id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.name

# class Recruiter(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     department = models.ForeignKey(Department, on_delete=models.RESTRICT)

#     def __str__(self):
#         return f"{self.user.name} ({self.department.name})"

# class Applicant(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     contact_number = models.CharField(max_length=50, blank=True, null=True)
#     experience = models.IntegerField(blank=True, null=True)
#     skills = models.TextField(blank=True, null=True)
#     education = models.TextField(blank=True, null=True)

#     def __str__(self):
#         return f"{self.user.name}"

# class JobListings(models.Model):
#     job_id = models.AutoField(primary_key=True)
#     recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE, related_name='jobs')
#     department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='jobs')
#     title = models.CharField(max_length=100)
#     description = models.TextField(blank=True, null=True)
#     salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
#     requirements = models.TextField(blank=True, null=True)
#     posted_date = models.DateField(default=timezone.now)

#     def __str__(self):
#         return self.title

# class Application(models.Model):
#     application_id = models.AutoField(primary_key=True)
#     job = models.ForeignKey(JobListings, on_delete=models.CASCADE, related_name='applications')
#     applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE, related_name='applications')
#     STATUS_CHOICES = [
#         ('Pending', 'Pending'),
#         ('Shortlisted', 'Shortlisted'),
#         ('Rejected', 'Rejected'),
#     ]
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
#     date_applied = models.DateField(default=timezone.now)

#     def __str__(self):
#         return f"App #{self.application_id} for {self.job.title}"

# class InterviewSchedule(models.Model):
#     job = models.ForeignKey(JobListings, on_delete=models.CASCADE, related_name='interviews')
#     application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='interviews')
#     recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE, related_name='interviews')
#     date = models.DateField()
#     time = models.TimeField()
#     STATUS_CHOICES = [
#         ('Scheduled', 'Scheduled'),
#         ('Completed', 'Completed'),
#         ('Cancelled', 'Cancelled'),
#     ]
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Scheduled')

#     class Meta:
#         unique_together = ('job', 'application', 'recruiter')

#     def __str__(self):
#         return f"Interview for App #{self.application.application_id}"

# class HiringDecision(models.Model):
#     job = models.ForeignKey(JobListings, on_delete=models.CASCADE, related_name='decisions')
#     applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE, related_name='decisions')
#     DECISION_CHOICES = [
#         ('Hired', 'Hired'),
#         ('Rejected', 'Rejected'),
#     ]
#     final_status = models.CharField(max_length=20, choices=DECISION_CHOICES)
#     decision_date = models.DateField(default=timezone.now)

#     class Meta:
#         unique_together = ('job', 'applicant')

#     def __str__(self):
#         return f"Decision for App #{self.applicant.user.name}: {self.final_status}"