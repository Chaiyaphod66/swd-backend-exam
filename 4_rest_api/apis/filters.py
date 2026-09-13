from django_filters import FilterSet, filters

from .models import Classroom, School, Student, Teacher


class SchoolFilter(FilterSet):
    name = filters.CharFilter(
        field_name="name",
        lookup_expr="icontains",
    )

    class Meta:
        model = School
        fields = ("name",)


class ClassroomFilter(FilterSet):
    school = filters.NumberFilter(field_name="school_id")

    class Meta:
        model = Classroom
        fields = ("school",)


class TeacherFilter(FilterSet):
    school = filters.NumberFilter(
        field_name="classrooms__school_id",
        distinct=True,
    )
    classroom = filters.NumberFilter(
        field_name="classrooms__id",
        distinct=True,
    )
    first_name = filters.CharFilter(
        field_name="first_name",
        lookup_expr="icontains",
    )
    last_name = filters.CharFilter(
        field_name="last_name",
        lookup_expr="icontains",
    )
    gender = filters.CharFilter(
        field_name="gender",
        lookup_expr="iexact",
    )

    class Meta:
        model = Teacher
        fields = ()


class StudentFilter(FilterSet):
    school = filters.NumberFilter(
        field_name="classroom__school_id",
    )
    classroom = filters.NumberFilter(
        field_name="classroom_id",
    )
    first_name = filters.CharFilter(
        field_name="first_name",
        lookup_expr="icontains",
    )
    last_name = filters.CharFilter(
        field_name="last_name",
        lookup_expr="icontains",
    )
    gender = filters.CharFilter(
        field_name="gender",
        lookup_expr="iexact",
    )

    class Meta:
        model = Student
        fields = ()