from django.core.validators import MinValueValidator
from django.db import models

# Create your models here.
class Gender(models.TextChoices):
    MALE = "male", "Male"
    FEMALE = "female", "Female"
    OTHER = "other", "Other"


class School(models.Model):
    name = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=50)
    address = models.TextField()

    class Meta:
        ordering = ("name", "id")

    def __str__(self):
        return self.name


class Classroom(models.Model):
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name="classrooms",
    )
    grade = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )
    room = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )

    class Meta:
        ordering = ("school", "grade", "room", "id")
        constraints = [
            models.UniqueConstraint(
                fields=("school", "grade", "room"),
                name="unique_classroom_per_school",
            )
        ]

    def __str__(self):
        return f"{self.school.abbreviation} {self.grade}/{self.room}"


class Teacher(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    gender = models.CharField(
        max_length=10,
        choices=Gender.choices,
    )
    classrooms = models.ManyToManyField(
        Classroom,
        related_name="teachers",
        blank=True,
    )

    class Meta:
        ordering = ("first_name", "last_name", "id")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Student(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    gender = models.CharField(
        max_length=10,
        choices=Gender.choices,
    )
    classroom = models.ForeignKey(
        Classroom,
        on_delete=models.CASCADE,
        related_name="students",
    )

    class Meta:
        ordering = ("first_name", "last_name", "id")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"