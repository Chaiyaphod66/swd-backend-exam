from rest_framework import serializers


# code here
from .models import Classroom, School, Student, Teacher


class SchoolSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ("id", "name", "abbreviation")


class ClassroomSummarySerializer(serializers.ModelSerializer):
    school = SchoolSummarySerializer(read_only=True)

    class Meta:
        model = Classroom
        fields = ("id", "school", "grade", "room")


class TeacherSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ("id", "first_name", "last_name", "gender")


class StudentSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ("id", "first_name", "last_name", "gender")


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ("id", "name", "abbreviation", "address")


class SchoolDetailSerializer(SchoolSerializer):
    classroom_count = serializers.IntegerField(read_only=True)
    teacher_count = serializers.IntegerField(read_only=True)
    student_count = serializers.IntegerField(read_only=True)

    class Meta(SchoolSerializer.Meta):
        fields = SchoolSerializer.Meta.fields + (
            "classroom_count",
            "teacher_count",
            "student_count",
        )


class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = ("id", "school", "grade", "room")


class ClassroomDetailSerializer(serializers.ModelSerializer):
    school = SchoolSummarySerializer(read_only=True)
    teachers = TeacherSummarySerializer(many=True, read_only=True)
    students = StudentSummarySerializer(many=True, read_only=True)

    class Meta:
        model = Classroom
        fields = (
            "id",
            "school",
            "grade",
            "room",
            "teachers",
            "students",
        )



class TeacherSerializer(serializers.ModelSerializer):
    classrooms = serializers.PrimaryKeyRelatedField(
        queryset=Classroom.objects.all(),
        many=True,
        required=False,
    )

    class Meta:
        model = Teacher
        fields = (
            "id",
            "first_name",
            "last_name",
            "gender",
            "classrooms",
        )


class TeacherDetailSerializer(serializers.ModelSerializer):
    classrooms = ClassroomSummarySerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Teacher
        fields = (
            "id",
            "first_name",
            "last_name",
            "gender",
            "classrooms",
        )


class StudentSerializer(serializers.ModelSerializer):
    classroom = serializers.PrimaryKeyRelatedField(
        queryset=Classroom.objects.all(),
    )

    class Meta:
        model = Student
        fields = (
            "id",
            "first_name",
            "last_name",
            "gender",
            "classroom",
        )


class StudentDetailSerializer(serializers.ModelSerializer):
    classroom = ClassroomSummarySerializer(read_only=True)

    class Meta:
        model = Student
        fields = (
            "id",
            "first_name",
            "last_name",
            "gender",
            "classroom",
        )