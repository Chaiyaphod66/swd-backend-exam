from django.contrib import admin

from .models import Classroom, School, Student, Teacher


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ("name", "abbreviation")
    search_fields = ("name", "abbreviation")


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ("school", "grade", "room")
    list_filter = ("school", "grade")
    search_fields = (
        "school__name",
        "school__abbreviation",
    )


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "gender")
    list_filter = ("gender", "classrooms__school")
    search_fields = ("first_name", "last_name")
    filter_horizontal = ("classrooms",)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "gender",
        "classroom",
    )
    list_filter = (
        "gender",
        "classroom__school",
        "classroom",
    )
    search_fields = ("first_name", "last_name")