from django import forms
from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image_path = models.ImageField(upload_to="courses/", blank=True, null=True)
    duration = models.CharField(max_length=100, blank=True)   # e.g. "3 months"
    classes = models.PositiveIntegerField(default=0)
    team_size = models.PositiveIntegerField(default=0)
    support = models.CharField(max_length=255, blank=True)    # e.g. "24/7 mentor"
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.title


class Group(models.Model):
    title = models.CharField(max_length=255)
    starting_date = models.DateField()
    ending_date = models.DateField(blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="groups")
    archived = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} ({self.course.title})"


class User(models.Model):
    class Role(models.TextChoices):
        ADMIN = "admin", "Admin"
        STUDENT = "student", "Student"

    class Status(models.TextChoices):
        UPCOMING = "upcoming", "Upcoming"
        ACTIVE = "active", "Active"
        FINISHED = "finished", "Finished"
        PAUSED = "paused", "Paused"

    firstname = models.CharField(max_length=150)
    lastname = models.CharField(max_length=150)
    image_path = models.ImageField(upload_to="users/", blank=True, null=True)

    email = models.EmailField(unique=True)
    login = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=255)  # hashed

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STUDENT,
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        related_name="users",
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.UPCOMING,
    )

    def __str__(self):
        return f"{self.firstname} {self.lastname}"


class Test(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="tests",
    )
    title = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.title or f"Test #{self.pk} ({self.course.title})"


class Question(models.Model):
    class QuestionType(models.TextChoices):
        ONE = "one", "One correct"
        MULTI = "multi", "Multiple correct"
        TYPED = "typed", "Typed answer"

    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        related_name="questions",
    )
    title = models.TextField()
    type = models.CharField(
        max_length=10,
        choices=QuestionType.choices,
        default=QuestionType.ONE,
    )

    correct = models.CharField(max_length=255, blank=True)
    incorrect1 = models.CharField(max_length=255, blank=True)
    incorrect2 = models.CharField(max_length=255, blank=True)
    incorrect3 = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.title[:50]


class StudentSolve(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="student_solves",
        db_index=True,
    )
    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        related_name="solves",
        db_index=True,
    )
    # raw solve data (for one/multi choice, like "A,B")
    solve = models.TextField(blank=True, null=True)
    # text typed by student for typed questions
    solve_typed = models.TextField(blank=True, null=True)
    solve_status = models.BooleanField(default=False)  # True = passed/correct
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "test")

    def __str__(self):
        return f"{self.user} – {self.test} ({'OK' if self.solve_status else 'FAIL'})"


class Integration(models.Model):
    class Permission(models.TextChoices):
        READONLY = "readonly", "Read only"
        OFF = "off", "Off"

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="integrations",
    )
    title = models.CharField(max_length=255)
    api_key = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)

    permission = models.CharField(
        max_length=20,
        choices=Permission.choices,
        default=Permission.READONLY,
    )

    rate_limit_per_minute = models.PositiveIntegerField(
        default=60,
        help_text="Max API requests per minute for this integration/api_key.",
    )
    rate_limit_per_day = models.PositiveIntegerField(
        default=10000,
        help_text="Max API requests per day for this integration/api_key.",
    )

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.user.role != User.Role.ADMIN:
            raise ValidationError("Only ADMIN users can create API integrations.")

    def __str__(self):
        return f"{self.title} ({self.user})"


class Journal(models.Model):
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="journal_entries",
        db_index=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="journal_entries",
    )
    status = models.BooleanField(default=False)  # e.g. "present", "absent"
    date = models.DateField()

    class Meta:
        unique_together = ("group", "user", "date")

    def __str__(self):
        return f"{self.date} – {self.group} – {self.user} – {self.status}"


class Material(models.Model):
    class MaterialType(models.TextChoices):
        PRESENTATION = "presentation", "Presentation"
        DOCX = "docx", "DOCX"
        PDF = "pdf", "PDF"
        IMAGE = "image", "Image"
        LINK = "link", "Link"

    title = models.CharField(max_length=255)
    source = models.CharField(max_length=500)  # path or URL
    type = models.CharField(
        max_length=20,
        choices=MaterialType.choices,
        default=MaterialType.PRESENTATION,
    )

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    material = models.ForeignKey(
        Material,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="lessons",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lessons",
    )

    def __str__(self):
        return self.title


class Application(models.Model):
    firstname = models.CharField(max_length=150)
    lastname = models.CharField(max_length=150)
    email = models.EmailField()
    date = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="applications",
    )

    throttled = models.BooleanField(
        default=False,
        help_text="True if further applications from this email/user are temporarily blocked.",
    )
    throttle_until = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Datetime until which new applications from same email/IP are blocked.",
    )

    def __str__(self):
        return f"{self.firstname} {self.lastname} – {self.course}"


class Payment(models.Model):
    class PaymentType(models.TextChoices):
        CASH = "cash", "Cash"
        CARD = "card", "Card"
        TRANSFER = "transfer", "Bank transfer"

    class Status(models.TextChoices):
        UNCOMPLETED = "uncompleted", "Uncompleted"
        PARTIALLY = "partially", "Partially completed"
        COMPLETED = "completed", "Completed"

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="payments",
    )
    date = models.DateTimeField(auto_now_add=True)

    type = models.CharField(
        max_length=20,
        choices=PaymentType.choices,
    )
    payed = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        help_text="Only used for cash payments (percent or absolute, your choice).",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.UNCOMPLETED,
    )

    def __str__(self):
        return f"{self.user} – {self.payed} ({self.get_status_display()})"


class Team(models.Model):
    fullname = models.CharField(max_length=255)
    image = models.ImageField(upload_to="team/", blank=True, null=True)
    speciality = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.fullname


class Partner(models.Model):
    image = models.ImageField(upload_to="partners/", blank=True, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class FAQ(models.Model):
    question = models.CharField(max_length=500)
    answer = models.TextField()

    def __str__(self):
        return self.question[:80]


class CourseIncluded(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="included_items",
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.course}: {self.title}"


class CourseProcess(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="process_steps",
    )
    rank = models.PositiveIntegerField()  # order
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["course", "rank"]

    def __str__(self):
        return f"{self.course} – {self.rank}. {self.title}"


class ContactStats(models.Model):
    avg_response = models.FloatField(help_text="Average response time in hours or minutes.")
    satisfaction = models.FloatField(help_text="Satisfaction index, e.g. 0–100.")
    students = models.PositiveIntegerField(help_text="Number of students served.")

    def __str__(self):
        return f"Contact stats (students: {self.students})"


class ContactInfo(models.Model):
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    workTimeInDT = models.CharField(max_length=100, help_text="Work time in local timezone (DT).")
    workTimeinUST = models.CharField(max_length=100, help_text="Work time in US timezone.")

    def __str__(self):
        return self.email


class SuccessStory(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="success_stories",
    )
    description = models.TextField()
    rate = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=5.0,
        help_text="Rating from 1.0 to 5.0",
    )
    published = models.BooleanField(default=False)

    def __str__(self):
        return f"SuccessStory #{self.pk} ({'published' if self.published else 'draft'})"